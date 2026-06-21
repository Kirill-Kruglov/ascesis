#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import random
import statistics
import subprocess
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_09"
RAW = RESULTS / "raw"

SEEDS = list(range(9200, 9230))
STEPS = 90
ZONES = 9
TYPES = ["dove", "hawk", "mutant", "scavenger"]
TRIVIAL_POLICIES = {"feature_proxy", "always_cut_sagging", "always_aid_sagging", "monoculture_optimizer"}
CONSEQUENCE_NEIGHBOR_POLICIES = {"neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid"}
EPS = 1e-9


@dataclass(frozen=True)
class Params:
    world: str
    policy: str
    delay: int = 2
    t_irrev: int = 7
    adversarial_strength: float = 0.70
    catastrophe_severity: float = 0.55
    diversity_floor: float = 0.0
    channel_noise: float = 0.12
    target_mi: float = 0.25
    mi_tolerance: float = 0.06


@dataclass
class Zone:
    idx: int
    welfare: float
    productivity: float
    migration_capacity: float
    pop: dict
    observed_feature: float
    catastrophe: bool = False
    captured_signature: bool = False
    failed: bool = False
    harm_timer: int = 0
    time_failed: int = -1
    last_raw_aid: float = 0.0
    last_effective_aid: float = 0.0
    last_useful_aid: float = 0.0
    last_intercepted_aid: float = 0.0
    prev_welfare: float = 0.0
    prev_productivity: float = 0.0
    prev_migration: float = 0.0
    prev_population: float = 0.0
    prev_diversity: float = 0.0
    neighbor_welfare_delta: float = 0.0
    neighbor_productivity_delta: float = 0.0
    neighbor_migration_delta: float = 0.0
    neighbor_population_delta: float = 0.0
    neighbor_diversity_delta: float = 0.0


@dataclass(frozen=True)
class Obs:
    step: int
    welfare: tuple
    productivity: tuple
    migration: tuple
    diversity_total: tuple
    diversity_non_adv: tuple
    diversity_adv: tuple
    observed_feature: tuple
    capture_signal: tuple
    sag: tuple
    last_raw_aid: tuple
    last_effective_aid: tuple
    last_useful_aid: tuple
    last_intercepted_aid: tuple
    self_response: tuple
    neighbor_welfare_delta: tuple
    neighbor_productivity_delta: tuple
    neighbor_migration_delta: tuple
    neighbor_population_delta: tuple
    neighbor_diversity_delta: tuple
    global_welfare: float
    global_diversity_non_adv: float


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC_IMPLEMENTED_09.md").read_bytes()).hexdigest()


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def normalize(xs, total=1.0):
    s = sum(max(0.0, x) for x in xs)
    if s <= EPS:
        return [total / len(xs) for _ in xs]
    return [max(0.0, x) / s * total for x in xs]


def shannon(vals):
    total = sum(max(0.0, v) for v in vals)
    if total <= EPS:
        return 0.0
    h = 0.0
    nonzero = 0
    for v in vals:
        if v > EPS:
            nonzero += 1
            p = v / total
            h -= p * math.log(p)
    if nonzero <= 1:
        return 0.0
    return h / math.log(len(vals))


def div_total(pop):
    return shannon([pop[t] for t in TYPES])


def div_non_adv(pop):
    return shannon([pop["dove"], pop["mutant"]])


def div_adv(pop):
    return shannon([pop["hawk"], pop["scavenger"]])


def total_pop(pop):
    return sum(pop.values())


def adv_share(pop):
    return (pop["hawk"] + pop["scavenger"]) / max(EPS, total_pop(pop))


def safe_mean(xs):
    return statistics.fmean(xs) if xs else 0.0


def safe_corr(xs, ys):
    if len(xs) < 2:
        return 0.0
    mx, my = safe_mean(xs), safe_mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= EPS or vy <= EPS:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def mutual_information_binary(xs, ys):
    n = len(xs)
    if n == 0:
        return 0.0
    joint = Counter(zip(xs, ys))
    cx, cy = Counter(xs), Counter(ys)
    mi = 0.0
    for (x, y), c in joint.items():
        pxy, px, py = c / n, cx[x] / n, cy[y] / n
        mi += pxy * math.log((pxy + EPS) / (px * py + EPS), 2)
    return max(0.0, mi)


def wilson(k, n, z=1.96):
    if n <= 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - half), min(1.0, center + half)


class BreakTrivialModel:
    def __init__(self, seed, params):
        self.seed = seed
        self.params = params
        self.rng = random.Random(seed)
        self.neighbors = {i: sorted({(i - 1) % ZONES, (i + 1) % ZONES}) for i in range(ZONES)}
        self.zones = []
        self.obs_queue = deque(maxlen=max(2, params.delay + 1))
        self.first_irrev = -1
        self.signal_bins = []
        self.truth_bins = []
        self.signal_vals = []
        self.truth_vals = []
        self.last_aid_nonzero_seen = False
        self.neighbor_metric_nonzero_seen = False
        self._init_world()
        o = self._observe(0, noisy=False)
        for _ in range(params.delay + 1):
            self.obs_queue.append(o)

    def _base_zone(self, idx):
        return Zone(
            idx=idx,
            welfare=self.rng.uniform(0.68, 0.82),
            productivity=self.rng.uniform(0.66, 0.84),
            migration_capacity=self.rng.uniform(0.55, 0.75),
            pop={"dove": 24.0, "hawk": 2.0, "mutant": 3.0, "scavenger": 0.5},
            observed_feature=self.rng.uniform(0.45, 0.60),
        )

    def _init_world(self):
        self.zones = [self._base_zone(i) for i in range(ZONES)]
        if self.params.world == "T1_proxy_trap":
            for i in [1, 4, 7]:
                z = self.zones[i]
                z.pop = {"dove": 9.0, "hawk": 22.0, "mutant": 1.0, "scavenger": 1.5}
                z.observed_feature = 0.96
                z.welfare = 0.58
                z.productivity = 0.62
                z.captured_signature = True
        elif self.params.world == "T2_sag_ambiguity_trap":
            for i in [0, 3]:
                z = self.zones[i]
                z.catastrophe = True
                z.welfare = 0.28
                z.productivity = 0.31
                z.migration_capacity = 0.30
                z.pop = {"dove": 27.0, "hawk": 1.0, "mutant": 4.5, "scavenger": 0.5}
                z.observed_feature = 0.48
            for i in [1, 4]:
                z = self.zones[i]
                z.captured_signature = True
                z.welfare = 0.30
                z.productivity = 0.34
                z.migration_capacity = 0.34
                z.pop = {"dove": 8.0, "hawk": 24.0, "mutant": 1.0, "scavenger": 2.0}
                z.observed_feature = 0.50
        elif self.params.world == "T3_monoculture_trap":
            for i in range(ZONES):
                z = self.zones[i]
                if i in [0, 1, 2, 3, 4]:
                    z.productivity = 0.94
                    z.welfare = 0.82
                    z.pop = {"dove": 30.0, "hawk": 1.0, "mutant": 0.2, "scavenger": 0.0}
                    z.observed_feature = 0.72
                else:
                    z.productivity = 0.66
                    z.welfare = 0.72
                    z.pop = {"dove": 18.0, "hawk": 1.5, "mutant": 12.0, "scavenger": 0.0}
                    z.observed_feature = 0.50
        elif self.params.world == "FIXED_MI_DELAY":
            for i in [1, 4]:
                z = self.zones[i]
                z.captured_signature = True
                z.pop = {"dove": 10.0, "hawk": 18.0, "mutant": 2.0, "scavenger": 1.5}
                z.welfare = 0.44
                z.productivity = 0.48
        else:
            raise ValueError(self.params.world)
        for z in self.zones:
            z.prev_welfare = z.welfare
            z.prev_productivity = z.productivity
            z.prev_migration = z.migration_capacity
            z.prev_population = total_pop(z.pop)
            z.prev_diversity = div_total(z.pop)

    def _truth_harm(self, z):
        return max(
            0.0,
            0.55 * adv_share(z.pop) * self.params.adversarial_strength
            + (0.40 if z.catastrophe else 0.0)
            + (0.20 if z.failed else 0.0),
        )

    def _capture_signal(self, z, noisy=True):
        truth = self._truth_harm(z)
        truth_bin = 1 if truth > 0.38 else 0
        if self.params.world == "FIXED_MI_DELAY" and noisy:
            obs_bin = 1 - truth_bin if self.rng.random() < self.params.channel_noise else truth_bin
            sig = (0.72 if obs_bin else 0.16) + self.rng.uniform(-0.035, 0.035)
            sig = clamp(sig)
        else:
            noise = self.rng.uniform(-self.params.channel_noise, self.params.channel_noise) if noisy else 0.0
            sig = clamp(truth + noise)
            obs_bin = 1 if sig > 0.38 else 0
        self.truth_vals.append(truth)
        self.signal_vals.append(sig)
        self.truth_bins.append(truth_bin)
        self.signal_bins.append(obs_bin)
        return sig

    def _observe(self, step, noisy=True):
        welfare, prod, migration, dt, dna, da = [], [], [], [], [], []
        feature, cap, sag = [], [], []
        raw, eff, useful, intercepted, self_resp = [], [], [], [], []
        nwd, npd, nmd, npopd, ndivd = [], [], [], [], []
        for z in self.zones:
            welfare.append(z.welfare)
            prod.append(z.productivity)
            migration.append(z.migration_capacity)
            dt.append(div_total(z.pop))
            dna.append(div_non_adv(z.pop))
            da.append(div_adv(z.pop))
            if self.params.world == "T1_proxy_trap" and adv_share(z.pop) > 0.45:
                feature.append(clamp(z.observed_feature + 0.25 * adv_share(z.pop)))
            else:
                feature.append(z.observed_feature)
            cap.append(self._capture_signal(z, noisy=noisy))
            sag.append(1.0 if min(z.welfare, z.productivity) < 0.42 else 0.0)
            raw.append(z.last_raw_aid)
            eff.append(z.last_effective_aid)
            useful.append(z.last_useful_aid)
            intercepted.append(z.last_intercepted_aid)
            self_resp.append((z.welfare - z.prev_welfare) + (z.productivity - z.prev_productivity))
            nwd.append(z.neighbor_welfare_delta)
            npd.append(z.neighbor_productivity_delta)
            nmd.append(z.neighbor_migration_delta)
            npopd.append(z.neighbor_population_delta)
            ndivd.append(z.neighbor_diversity_delta)
        return Obs(
            step=step,
            welfare=tuple(welfare),
            productivity=tuple(prod),
            migration=tuple(migration),
            diversity_total=tuple(dt),
            diversity_non_adv=tuple(dna),
            diversity_adv=tuple(da),
            observed_feature=tuple(feature),
            capture_signal=tuple(cap),
            sag=tuple(sag),
            last_raw_aid=tuple(raw),
            last_effective_aid=tuple(eff),
            last_useful_aid=tuple(useful),
            last_intercepted_aid=tuple(intercepted),
            self_response=tuple(self_resp),
            neighbor_welfare_delta=tuple(nwd),
            neighbor_productivity_delta=tuple(npd),
            neighbor_migration_delta=tuple(nmd),
            neighbor_population_delta=tuple(npopd),
            neighbor_diversity_delta=tuple(ndivd),
            global_welfare=safe_mean(welfare),
            global_diversity_non_adv=safe_mean(dna),
        )

    def _delayed_obs(self):
        obs = self.obs_queue[0]
        assert not hasattr(obs, "pop")
        assert not hasattr(obs, "types")
        return obs

    def _score(self, obs, i):
        p = self.params.policy
        need = 1.0 - min(obs.welfare[i], obs.productivity[i])
        neighbor_response = (
            obs.neighbor_welfare_delta[i]
            + obs.neighbor_productivity_delta[i]
            + 0.5 * obs.neighbor_migration_delta[i]
            + 0.25 * obs.neighbor_population_delta[i]
            + 0.35 * obs.neighbor_diversity_delta[i]
        )
        self_response = obs.self_response[i]
        capture = obs.capture_signal[i]
        if p == "feature_proxy":
            return obs.observed_feature[i]
        if p == "always_cut_sagging":
            return -3.0 * obs.sag[i] + 0.2 * obs.productivity[i]
        if p == "always_aid_sagging":
            return 3.0 * obs.sag[i] + need
        if p == "monoculture_optimizer":
            return 2.2 * obs.productivity[i] - 1.0 * obs.diversity_non_adv[i]
        if p == "self_consequence":
            return need + 2.2 * self_response - 1.0 * capture
        if p == "neighbor_consequence":
            return 0.4 * need + 3.0 * neighbor_response - 1.1 * capture
        if p == "local_global_neighbor":
            return 0.8 * need + 1.7 * neighbor_response + 0.7 * (1.0 - obs.global_welfare) + 0.8 * max(0.0, self.params.diversity_floor - obs.diversity_non_adv[i]) - 1.0 * capture
        if p == "response_to_neighbor_aid":
            probe = 0.55 if obs.sag[i] and obs.last_raw_aid[i] < 0.04 else 0.0
            aid_response = neighbor_response / max(0.06, obs.last_useful_aid[i]) if obs.last_useful_aid[i] > 0 else 0.0
            return 0.9 * need + 1.8 * aid_response + probe - 1.25 * max(0.0, -aid_response) - 0.9 * capture
        if p == "diversity_all_types":
            return 0.6 * need + 1.2 * max(0.0, self.params.diversity_floor - obs.diversity_total[i]) - 0.7 * capture
        if p == "diversity_non_adversarial_only":
            return 0.6 * need + 1.7 * max(0.0, self.params.diversity_floor - obs.diversity_non_adv[i]) - 0.9 * capture - 0.35 * obs.diversity_adv[i]
        if p == "no_diversity_floor":
            return 0.8 * need + 1.5 * neighbor_response - 0.9 * capture
        raise ValueError(p)

    def choose_alloc(self):
        obs = self._delayed_obs()
        scores = [self._score(obs, i) for i in range(ZONES)]
        floor = 0.02 if self.params.policy in {"neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid", "self_consequence"} else 0.0
        min_s = min(scores)
        shifted = [max(0.01, s - min_s + 0.04) for s in scores]
        alloc = normalize(shifted, total=max(0.0, 1.0 - floor * ZONES))
        return [a + floor for a in alloc]

    def _apply_shock(self, step):
        if self.params.world == "T3_monoculture_trap" and step == 42:
            for z in self.zones:
                if div_non_adv(z.pop) < 0.18 and z.productivity > 0.82:
                    z.welfare *= 0.18
                    z.productivity *= 0.16
                    z.migration_capacity *= 0.28
                    z.pop["dove"] *= 0.42
        if self.params.world == "T3_monoculture_trap" and step > 42:
            for z in self.zones:
                if div_non_adv(z.pop) < 0.50:
                    z.welfare = clamp(z.welfare - 0.070)
                    z.productivity = clamp(z.productivity - 0.065)
                    z.migration_capacity = clamp(z.migration_capacity - 0.045)
                    z.pop["dove"] *= 0.970
        if self.params.world == "T2_sag_ambiguity_trap" and step in [18, 36]:
            for z in self.zones:
                if z.catastrophe:
                    z.welfare *= 0.82
                    z.productivity *= 0.84

    def _store_pre_step(self):
        for z in self.zones:
            z.prev_welfare = z.welfare
            z.prev_productivity = z.productivity
            z.prev_migration = z.migration_capacity
            z.prev_population = total_pop(z.pop)
            z.prev_diversity = div_total(z.pop)

    def _update_neighbor_metrics(self):
        for z in self.zones:
            ns = [self.zones[j] for j in self.neighbors[z.idx]]
            z.neighbor_welfare_delta = safe_mean([n.welfare - n.prev_welfare for n in ns])
            z.neighbor_productivity_delta = safe_mean([n.productivity - n.prev_productivity for n in ns])
            z.neighbor_migration_delta = safe_mean([n.migration_capacity - n.prev_migration for n in ns])
            z.neighbor_population_delta = safe_mean([(total_pop(n.pop) - n.prev_population) / max(1.0, n.prev_population) for n in ns])
            z.neighbor_diversity_delta = safe_mean([div_total(n.pop) - n.prev_diversity for n in ns])
            if abs(z.neighbor_welfare_delta) + abs(z.neighbor_productivity_delta) + abs(z.neighbor_population_delta) > 1e-5:
                self.neighbor_metric_nonzero_seen = True

    def _aid_effect(self, z, raw):
        if z.failed:
            effective = 0.12 * raw
        else:
            effective = raw
        hawk = adv_share(z.pop)
        intercepted = effective * min(0.92, self.params.adversarial_strength * (0.15 + 0.95 * hawk))
        useful = effective - intercepted
        return effective, useful, intercepted

    def _apply_zone_dynamics(self, z, raw, step):
        effective, useful, intercepted = self._aid_effect(z, raw)
        z.last_raw_aid = raw
        z.last_effective_aid = effective
        z.last_useful_aid = useful
        z.last_intercepted_aid = intercepted
        if raw > 0.001:
            self.last_aid_nonzero_seen = True
        hawk = adv_share(z.pop)
        if z.catastrophe:
            # Catastrophe victims recover from useful aid and collapse when cut too long.
            z.welfare = clamp(z.welfare + 0.34 * useful - 0.030)
            z.productivity = clamp(z.productivity + 0.27 * useful - 0.025)
            z.migration_capacity = clamp(z.migration_capacity + 0.20 * useful - 0.018)
            z.pop["dove"] *= 1.0 + 0.015 * useful - 0.008 * max(0.0, 0.35 - z.welfare)
            z.pop["mutant"] *= 1.0 + 0.012 * useful
        elif z.captured_signature or hawk > 0.36:
            # Captured zones convert aid into hawk growth and neighbor harm.
            z.welfare = clamp(z.welfare + 0.05 * useful - 0.11 * hawk * self.params.adversarial_strength)
            z.productivity = clamp(z.productivity + 0.04 * useful - 0.10 * hawk * self.params.adversarial_strength)
            z.migration_capacity = clamp(z.migration_capacity + 0.03 * useful - 0.07 * hawk)
            z.pop["hawk"] *= 1.0 + 0.055 * intercepted + 0.020 * raw
            z.pop["dove"] *= max(0.0, 1.0 - 0.045 * self.params.adversarial_strength - 0.020 * raw)
            for j in self.neighbors[z.idx]:
                n = self.zones[j]
                n.welfare = clamp(n.welfare - 0.020 * hawk * (0.5 + raw))
                n.productivity = clamp(n.productivity - 0.018 * hawk * (0.5 + raw))
        else:
            # Stable cooperative zone with neighbor-positive spillover.
            z.welfare = clamp(z.welfare + 0.18 * useful - 0.018)
            z.productivity = clamp(z.productivity + 0.15 * useful - 0.016)
            z.migration_capacity = clamp(z.migration_capacity + 0.12 * useful - 0.010)
            z.pop["dove"] *= 1.0 + 0.018 * useful + 0.004 * z.productivity
            z.pop["mutant"] *= 1.0 + 0.010 * useful
            for j in self.neighbors[z.idx]:
                n = self.zones[j]
                n.welfare = clamp(n.welfare + 0.025 * useful)
                n.productivity = clamp(n.productivity + 0.020 * useful)
                n.migration_capacity = clamp(n.migration_capacity + 0.015 * useful)
        if self.params.world == "T1_proxy_trap" and hawk > 0.35:
            z.observed_feature = clamp(z.observed_feature + 0.015 + 0.10 * raw)
        if self.params.policy == "diversity_all_types" and self.params.diversity_floor > 0 and div_total(z.pop) < self.params.diversity_floor:
            # This intentionally can preserve predators; it is a comparator.
            for t in TYPES:
                z.pop[t] += 0.020 * total_pop(z.pop)
        if self.params.policy == "diversity_non_adversarial_only" and self.params.diversity_floor > 0 and div_non_adv(z.pop) < self.params.diversity_floor:
            z.pop["mutant"] += 0.045 * max(1.0, z.pop["dove"])
        for t in TYPES:
            z.pop[t] = max(0.0, min(250.0, z.pop[t]))

    def _update_irreversibility(self, step):
        for z in self.zones:
            hard_harm = (
                z.welfare < 0.24
                or z.productivity < 0.24
                or z.pop["dove"] < 3.0
                or adv_share(z.pop) > 0.72
                or (self.params.world == "T3_monoculture_trap" and div_non_adv(z.pop) < 0.50 and z.productivity < 0.96)
            )
            if hard_harm:
                z.harm_timer += 1
            else:
                z.harm_timer = max(0, z.harm_timer - 1)
            if not z.failed and z.harm_timer >= self.params.t_irrev:
                z.failed = True
                z.time_failed = step
                if self.first_irrev < 0:
                    self.first_irrev = step

    def step(self, step):
        self._store_pre_step()
        self._apply_shock(step)
        alloc = self.choose_alloc()
        budget = 5.5
        for i, z in enumerate(self.zones):
            self._apply_zone_dynamics(z, budget * alloc[i], step)
        self._update_irreversibility(step)
        self._update_neighbor_metrics()
        self.obs_queue.append(self._observe(step, noisy=True))

    def run(self):
        for step in range(STEPS):
            self.step(step)
        return self.metrics()

    def metrics(self):
        failed = sum(1 for z in self.zones if z.failed)
        counts = {t: sum(z.pop[t] for z in self.zones) for t in TYPES}
        total = sum(counts.values()) + EPS
        welfare = safe_mean([(z.welfare + z.productivity) / 2 for z in self.zones])
        min_welfare = min((z.welfare + z.productivity) / 2 for z in self.zones)
        adv = (counts["hawk"] + counts["scavenger"]) / total
        doves = counts["dove"] / total
        capture = 1.0 if adv > 0.48 or any(adv_share(z.pop) > 0.78 for z in self.zones) else 0.0
        permanence = 1.0 if failed <= 2 and welfare > 0.48 and adv < 0.40 and doves > 0.38 and capture == 0.0 else 0.0
        collapse = 1.0 if failed >= 4 or welfare < 0.32 or doves < 0.20 else 0.0
        return {
            "permanence": permanence,
            "collapse": collapse,
            "capture": capture,
            "mean_welfare": welfare,
            "min_welfare": min_welfare,
            "adversarial_share": adv,
            "dove_share": doves,
            "total_diversity": safe_mean([div_total(z.pop) for z in self.zones]),
            "non_adv_diversity": safe_mean([div_non_adv(z.pop) for z in self.zones]),
            "adv_diversity": safe_mean([div_adv(z.pop) for z in self.zones]),
            "irreversible_zone_failures": failed,
            "time_to_first_irreversible_failure": self.first_irrev if self.first_irrev >= 0 else STEPS,
            "fraction_irreversible_zones": failed / ZONES,
            "last_aid_updates_nonzero": 1.0 if self.last_aid_nonzero_seen else 0.0,
            "neighbor_metrics_nonzero": 1.0 if self.neighbor_metric_nonzero_seen else 0.0,
            "signal_truth_corr": safe_corr(self.signal_vals, self.truth_vals),
            "mutual_information": mutual_information_binary(self.signal_bins, self.truth_bins),
        }


def synthetic_mi_for_noise(seed, noise, n=600):
    rng = random.Random(seed)
    truth = [1 if rng.random() < 0.38 else 0 for _ in range(n)]
    obs = []
    flip = min(0.49, max(0.0, noise))
    for t in truth:
        obs.append(1 - t if rng.random() < flip else t)
    return mutual_information_binary(obs, truth)


def select_noise_for_target(delay, target=0.25, tolerance=0.06):
    candidates = [i / 100 for i in range(5, 46, 2)]
    scored = []
    for noise in candidates:
        mi = synthetic_mi_for_noise(7000 + delay, noise)
        scored.append((abs(mi - target), noise, mi))
    _, noise, mi = min(scored)
    return noise, mi, abs(mi - target) <= tolerance


def run_one(seed, params):
    m = BreakTrivialModel(seed, params)
    out = m.run()
    return {
        "seed": seed,
        "world": params.world,
        "policy": params.policy,
        "delay": params.delay,
        "t_irrev": params.t_irrev,
        "R": params.t_irrev / max(1, params.delay),
        "target_mi": params.target_mi,
        "mi_tolerance": params.mi_tolerance,
        "adversarial_strength": params.adversarial_strength,
        "catastrophe_severity": params.catastrophe_severity,
        "diversity_floor": params.diversity_floor,
        "channel_noise": params.channel_noise,
        **out,
    }


def scenario_grid():
    rows = []
    trap_policies = [
        "feature_proxy",
        "always_cut_sagging",
        "always_aid_sagging",
        "monoculture_optimizer",
        "self_consequence",
        "neighbor_consequence",
        "local_global_neighbor",
        "response_to_neighbor_aid",
        "diversity_all_types",
        "diversity_non_adversarial_only",
        "no_diversity_floor",
    ]
    for world in ["T1_proxy_trap", "T2_sag_ambiguity_trap", "T3_monoculture_trap"]:
        for policy in trap_policies:
            floor = 0.35 if "diversity" in policy or policy in {"local_global_neighbor", "monoculture_optimizer"} else 0.0
            rows.append(Params(world=world, policy=policy, diversity_floor=floor))
    for delay in [1, 2, 4, 7, 10]:
        noise, mi, ok = select_noise_for_target(delay, target=0.18, tolerance=0.06)
        for policy in ["neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid"]:
            rows.append(Params(world="FIXED_MI_DELAY", policy=policy, delay=delay, t_irrev=8, channel_noise=noise, target_mi=0.13, mi_tolerance=0.03))
    return rows


def summarize(rows):
    grouped = defaultdict(list)
    for r in rows:
        grouped[(r["world"], r["policy"], r["delay"], r["t_irrev"], r["diversity_floor"], r["channel_noise"])].append(r)
    out = []
    for key, vals in grouped.items():
        world, policy, delay, t_irrev, floor, noise = key
        k = int(sum(v["permanence"] for v in vals))
        lo, hi = wilson(k, len(vals))
        out.append({
            "world": world,
            "policy": policy,
            "delay": delay,
            "t_irrev": t_irrev,
            "R": t_irrev / max(1, delay),
            "target_mi": safe_mean([v["target_mi"] for v in vals]),
            "mi_tolerance": safe_mean([v["mi_tolerance"] for v in vals]),
            "diversity_floor": floor,
            "channel_noise": noise,
            "n": len(vals),
            "permanence_probability": safe_mean([v["permanence"] for v in vals]),
            "permanence_wilson_lo": lo,
            "permanence_wilson_hi": hi,
            "collapse_probability": safe_mean([v["collapse"] for v in vals]),
            "capture_probability": safe_mean([v["capture"] for v in vals]),
            "irreversible_zone_failures_mean": safe_mean([v["irreversible_zone_failures"] for v in vals]),
            "time_to_first_irreversible_failure_mean": safe_mean([v["time_to_first_irreversible_failure"] for v in vals]),
            "fraction_irreversible_zones_mean": safe_mean([v["fraction_irreversible_zones"] for v in vals]),
            "mean_welfare": safe_mean([v["mean_welfare"] for v in vals]),
            "adversarial_share": safe_mean([v["adversarial_share"] for v in vals]),
            "total_diversity": safe_mean([v["total_diversity"] for v in vals]),
            "non_adv_diversity": safe_mean([v["non_adv_diversity"] for v in vals]),
            "adv_diversity": safe_mean([v["adv_diversity"] for v in vals]),
            "last_aid_updates_nonzero": safe_mean([v["last_aid_updates_nonzero"] for v in vals]),
            "neighbor_metrics_nonzero": safe_mean([v["neighbor_metrics_nonzero"] for v in vals]),
            "signal_truth_corr": safe_mean([v["signal_truth_corr"] for v in vals]),
            "mutual_information": safe_mean([v["mutual_information"] for v in vals]),
        })
    return out


def validation(summary):
    by = {(r["world"], r["policy"]): r for r in summary if r["world"] != "FIXED_MI_DELAY"}
    fixed = [r for r in summary if r["world"] == "FIXED_MI_DELAY"]
    feature_fail = by[("T1_proxy_trap", "feature_proxy")]["permanence_probability"] < 0.25
    cut_fail = by[("T2_sag_ambiguity_trap", "always_cut_sagging")]["permanence_probability"] < 0.25
    aid_fail = by[("T2_sag_ambiguity_trap", "always_aid_sagging")]["permanence_probability"] < 0.25
    mono_fail = by[("T3_monoculture_trap", "monoculture_optimizer")]["permanence_probability"] < 0.25
    consequence_survives = any(r["policy"] in CONSEQUENCE_NEIGHBOR_POLICIES and r["permanence_probability"] >= 0.60 for r in summary if r["world"] in {"T1_proxy_trap", "T2_sag_ambiguity_trap", "T3_monoculture_trap"})
    fixed_mi_ok = all(abs(r["mutual_information"] - r["target_mi"]) <= r["mi_tolerance"] for r in fixed) if fixed else False
    checks = {
        "t_irrev_used_in_dynamics": any(r["time_to_first_irreversible_failure_mean"] < STEPS for r in summary),
        "irreversible_failures_possible": any(r["irreversible_zone_failures_mean"] > 0 for r in summary),
        "last_aid_updates_nonzero": all(r["last_aid_updates_nonzero"] > 0.5 for r in summary),
        "neighbor_metrics_use_neighbors": any(r["neighbor_metrics_nonzero"] > 0.5 for r in summary),
        "feature_proxy_trap_active": feature_fail,
        "sag_ambiguity_trap_active": cut_fail and aid_fail,
        "monoculture_trap_active": mono_fail,
        "fixed_mi_target_achieved": fixed_mi_ok,
        "trivial_policy_break_test_passed": feature_fail and cut_fail and aid_fail and mono_fail,
        "consequence_neighbor_policy_survives": consequence_survives,
    }
    if not all(v for k, v in checks.items() if k != "consequence_neighbor_policy_survives"):
        verdict = "D. Implementation invalid due to failed validation."
    elif not checks["trivial_policy_break_test_passed"]:
        verdict = "C. Trivial policies not broken; substrate still too easy."
    elif checks["consequence_neighbor_policy_survives"]:
        verdict = "A. Trivial policies broken; at least one consequence-neighbor policy survives."
    else:
        verdict = "B. Trivial policies broken; no consequence-neighbor policy survives."
    return checks, verdict


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def svg_bar(path, title, labels, values, ylabel):
    width, height = 900, 520
    ml, mr, mt, mb = 80, 30, 60, 120
    ymax = max(1.0, max(values) if values else 1.0)
    bw = (width - ml - mr) / max(1, len(labels))
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="{width/2}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>', f'<line x1="{ml}" y1="{height-mb}" x2="{width-mr}" y2="{height-mb}" stroke="#111"/>', f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}" stroke="#111"/>', f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" font-family="sans-serif" font-size="12">{ylabel}</text>']
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = ml + i * bw + bw * 0.12
        h = (val / ymax) * (height - mt - mb)
        y = height - mb - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*0.76:.1f}" height="{h:.1f}" fill="#1d4ed8"/>')
        parts.append(f'<text x="{x+bw*0.38:.1f}" y="{height-mb+14}" transform="rotate(45 {x+bw*0.38:.1f} {height-mb+14})" font-family="sans-serif" font-size="10">{lab}</text>')
        parts.append(f'<text x="{x+bw*0.38:.1f}" y="{y-4:.1f}" text-anchor="middle" font-family="sans-serif" font-size="10">{val:.2f}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n")


def svg_line(path, title, series, xlabel, ylabel):
    width, height = 900, 520
    ml, mr, mt, mb = 70, 30, 50, 60
    allx = [x for pts in series.values() for x, _ in pts] or [0, 1]
    ally = [y for pts in series.values() for _, y in pts] or [0, 1]
    xmin, xmax = min(allx), max(allx)
    ymin, ymax = min(0.0, min(ally)), max(1.0, max(ally))
    if abs(xmax - xmin) < EPS:
        xmax += 1
    def tx(x): return ml + (x - xmin) / (xmax - xmin) * (width - ml - mr)
    def ty(y): return height - mb - (y - ymin) / (ymax - ymin + EPS) * (height - mt - mb)
    colors = ["#1d4ed8", "#b45309", "#047857", "#7c3aed"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="{width/2}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>', f'<line x1="{ml}" y1="{height-mb}" x2="{width-mr}" y2="{height-mb}" stroke="#111"/>', f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}" stroke="#111"/>', f'<text x="{width/2}" y="{height-16}" text-anchor="middle" font-family="sans-serif" font-size="12">{xlabel}</text>', f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" font-family="sans-serif" font-size="12">{ylabel}</text>']
    for idx, (name, pts) in enumerate(series.items()):
        pts = sorted(pts)
        color = colors[idx % len(colors)]
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="' + ' '.join(f'{tx(x):.1f},{ty(y):.1f}' for x, y in pts) + '"/>')
        parts.append(f'<text x="{width-280}" y="{mt+16+idx*18}" font-family="sans-serif" font-size="11" fill="{color}">{name}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n")


def plots(summary):
    for world in ["T1_proxy_trap", "T2_sag_ambiguity_trap", "T3_monoculture_trap"]:
        rows = [r for r in summary if r["world"] == world]
        svg_bar(RESULTS / f"trivial_policy_survival_{world}.svg", f"Trivial Policy Survival: {world}", [r["policy"] for r in rows], [float(r["permanence_probability"]) for r in rows], "permanence")
    rows = [r for r in summary if r["world"] in {"T1_proxy_trap", "T2_sag_ambiguity_trap", "T3_monoculture_trap"}]
    feat = defaultdict(list)
    cons = defaultdict(list)
    for r in rows:
        if r["policy"] == "feature_proxy":
            feat[r["world"]].append(float(r["permanence_probability"]))
        if r["policy"] in CONSEQUENCE_NEIGHBOR_POLICIES:
            cons[r["world"]].append(float(r["permanence_probability"]))
    labels = sorted(feat)
    svg_bar(RESULTS / "consequence_vs_feature_permanence.svg", "Consequence vs Feature Permanence", labels + [l + " cons" for l in labels], [safe_mean(feat[l]) for l in labels] + [safe_mean(cons[l]) for l in labels], "permanence")
    fixed = [r for r in summary if r["world"] == "FIXED_MI_DELAY"]
    byp = defaultdict(list)
    for r in fixed:
        byp[r["policy"]].append((float(r["R"]), float(r["permanence_probability"])))
    svg_line(RESULTS / "fixed_MI_delay_R_plot.svg", "Fixed-MI Delay/R Plot", byp, "R", "permanence")
    byp2 = defaultdict(list)
    for r in fixed:
        byp2[r["policy"]].append((float(r["R"]), float(r["irreversible_zone_failures_mean"])))
    svg_line(RESULTS / "irreversible_failures_vs_R.svg", "Irreversible Failures vs R", byp2, "R", "mean irreversible failures")
    divrows = [r for r in summary if r["world"] == "T3_monoculture_trap" and "diversity" in r["policy"] or r["policy"] == "no_diversity_floor"]
    svg_bar(RESULTS / "diversity_floor_vs_shock_survival.svg", "Diversity Policy vs Shock Survival", [r["policy"] for r in divrows], [float(r["permanence_probability"]) for r in divrows], "permanence")
    nrows = [r for r in summary if r["policy"] in {"self_consequence", "neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid"} and r["world"] != "FIXED_MI_DELAY"]
    svg_bar(RESULTS / "neighbor_vs_self_consequence_performance.svg", "Neighbor vs Self Consequence", [r["world"] + ":" + r["policy"] for r in nrows], [float(r["permanence_probability"]) for r in nrows], "permanence")


def report(summary, checks, verdict):
    lines = [
        "# Experiment 09 Report: Break Trivial Policies",
        "",
        f"Final verdict: **{verdict}**",
        "",
        "## Validation Checks",
        "",
        "| check | result |",
        "|---|---:|",
    ]
    for k, v in checks.items():
        lines.append(f"| {k} | `{v}` |")
    lines += ["", "## World Outcomes", "", "| world | policy | permanence | collapse | capture | irrev failures | R | MI |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in sorted(summary, key=lambda x: (x["world"], x["policy"])):
        lines.append(f"| {r['world']} | {r['policy']} | {float(r['permanence_probability']):.3f} | {float(r['collapse_probability']):.3f} | {float(r['capture_probability']):.3f} | {float(r['irreversible_zone_failures_mean']):.2f} | {float(r['R']):.2f} | {float(r['mutual_information']):.3f} |")
    lines += [
        "",
        "## Interpretation",
        "",
        "Experiment 09 is a semantics repair pass, not a larger simulator. The key question is whether the toy substrate now breaks the policies that made experiment 08 fragile.",
        "",
        "If the verdict is A, the trivial comparators failed in their target traps and at least one neighbor-consequence policy survived. If B, trivial policies were broken but the consequence-neighbor construction still failed. If C or D, the substrate is still not suitable for reading the intended question.",
    ]
    (RESULTS / "report.md").write_text("\n".join(lines) + "\n")
    vlines = ["# Experiment 09 Validation Report", "", "| check | result |", "|---|---:|"]
    for k, v in checks.items():
        vlines.append(f"| {k} | `{v}` |")
    vlines += ["", f"Final verdict: **{verdict}**"]
    (RESULTS / "validation_report.md").write_text("\n".join(vlines) + "\n")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    params = scenario_grid()
    rows = []
    for p in params:
        for seed in SEEDS:
            rows.append(run_one(seed, p))
    summary = summarize(rows)
    checks, verdict = validation(summary)
    write_csv(RAW / "runs.csv", rows)
    write_csv(RAW / "summary.csv", summary)
    plots(summary)
    report(summary, checks, verdict)
    manifest = {
        "git_head": git_value(["rev-parse", "HEAD"]),
        "git_status_short": git_value(["status", "--short"]),
        "spec_implemented_09_sha256": spec_hash(),
        "seeds": SEEDS,
        "num_cells": len(summary),
        "num_runs": len(rows),
        "validation_checks": checks,
        "final_verdict": verdict,
    }
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"verdict": verdict, "cells": len(summary), "runs": len(rows), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
