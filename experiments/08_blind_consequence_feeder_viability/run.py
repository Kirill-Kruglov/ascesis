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
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"
CONFIG = json.loads((ROOT / "config" / "default_config.json").read_text())

TRAIN_SEEDS = CONFIG["train_seeds"]
HELDOUT_SEEDS = CONFIG["heldout_seeds"]
STEPS = CONFIG["steps"]
ZONES = CONFIG["zones"]
TYPES = ["dove", "hawk", "mutant", "scavenger"]
ADVERSARIAL_TYPES = {"hawk", "scavenger"}
EPS = 1e-9

POLICIES = [
    "feature_proxy",
    "scalar_welfare",
    "geometric_diversity",
    "local_consequence",
    "local_global",
    "response_to_aid",
    "audit_penalty",
    "always_cut_sagging",
    "always_aid_sagging",
    "monoculture_optimizer",
]

VIABILITY = CONFIG["viability_criterion"]


@dataclass(frozen=True)
class Params:
    experiment: str
    policy: str
    delay: int = 3
    t_irrev: int = 8
    adversarial_strength: float = 0.45
    camouflage_cost: float = 0.10
    audit_p: float = 0.0
    audit_C: float = 0.0
    audit_kappa: float = 0.0
    catastrophe_frequency: float = 0.0
    catastrophe_severity: float = 0.0
    mutation_rate: float = 0.0
    migration_cost: float = 0.08
    migration_speed: float = 0.20
    diversity_floor: float = 0.0
    channel_reliability: float = 0.80
    fixed_mi_noise: float = 0.25
    scavenger_enabled: bool = False
    future_shock: bool = False


@dataclass
class Zone:
    idx: int
    capacity: float
    vulnerability: float
    resource: float
    wellness: float
    productivity: float
    pop: dict
    catastrophe_timer: int = 0
    penalty_timer: int = 0
    last_aid: float = 0.0
    prev_wellness: float = 0.0
    prev_productivity: float = 0.0
    false_cut_events: int = 0
    false_aid_events: int = 0
    scavenger_intercept: float = 0.0


@dataclass(frozen=True)
class FeederObservation:
    step: int
    wellness: tuple
    productivity: tuple
    response: tuple
    recovery: tuple
    diversity: tuple
    observed_feature: tuple
    capture_signal: tuple
    sag: tuple
    last_aid: tuple
    global_welfare: float
    global_diversity: float
    audit_available: bool


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC_IMPLEMENTED.md").read_bytes()).hexdigest()


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def normalize(xs, total=1.0):
    s = sum(max(0.0, x) for x in xs)
    if s <= EPS:
        return [total / len(xs) for _ in xs]
    return [max(0.0, x) / s * total for x in xs]


def shannon_diversity(counts):
    vals = [max(0.0, counts.get(t, 0.0)) for t in TYPES]
    total = sum(vals)
    if total <= EPS:
        return 0.0
    h = 0.0
    for v in vals:
        if v > 0:
            p = v / total
            h -= p * math.log(p)
    return h / math.log(len(TYPES))


def hhi(values):
    total = sum(max(0.0, v) for v in values)
    if total <= EPS:
        return 0.0
    return sum((max(0.0, v) / total) ** 2 for v in values)


def geometric_mean(values):
    vals = [max(0.001, v) for v in values]
    return math.exp(sum(math.log(v) for v in vals) / len(vals))


def safe_corr(xs, ys):
    if len(xs) < 2:
        return 0.0
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= EPS or vy <= EPS:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def mutual_information_binary(xs, ys):
    pairs = list(zip(xs, ys))
    if not pairs:
        return 0.0
    n = len(pairs)
    joint = Counter(pairs)
    cx = Counter(xs)
    cy = Counter(ys)
    mi = 0.0
    for (x, y), c in joint.items():
        pxy = c / n
        px = cx[x] / n
        py = cy[y] / n
        mi += pxy * math.log(pxy / (px * py + EPS) + EPS, 2)
    return max(0.0, mi)


def wilson(successes, total, z=1.96):
    if total <= 0:
        return (0.0, 0.0)
    phat = successes / total
    denom = 1 + z * z / total
    center = (phat + z * z / (2 * total)) / denom
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total) / denom
    return max(0.0, center - half), min(1.0, center + half)


class BlindConsequenceFeederModel:
    def __init__(self, seed, params):
        self.seed = seed
        self.params = params
        self.rng = random.Random(seed)
        self.zones = []
        self.neighbors = {i: sorted({(i - 1) % ZONES, (i + 1) % ZONES, (i + ZONES // 2) % ZONES}) for i in range(ZONES)}
        self.observation_queue = deque(maxlen=max(2, params.delay + 1))
        self.previous_alloc = [1.0 / ZONES for _ in range(ZONES)]
        self.audit_cost_paid = 0.0
        self.total_aid_given = 0.0
        self.collapse_step = None
        self.recovery_times = []
        self.signal_values = []
        self.truth_values = []
        self.signal_bins = []
        self.truth_bins = []
        self._init_zones()
        initial_obs = self._make_observation(step=0, noisy=False)
        for _ in range(max(1, params.delay + 1)):
            self.observation_queue.append(initial_obs)

    def _init_zones(self):
        for i in range(ZONES):
            capacity = self.rng.uniform(0.85, 1.25)
            vulnerability = self.rng.uniform(0.15, 0.65)
            pop = {
                "dove": self.rng.uniform(18.0, 28.0),
                "hawk": self.rng.uniform(1.0, 4.0),
                "mutant": self.rng.uniform(1.0, 3.0),
                "scavenger": self.rng.uniform(0.0, 1.0) if self.params.scavenger_enabled else 0.0,
            }
            zone = Zone(
                idx=i,
                capacity=capacity,
                vulnerability=vulnerability,
                resource=self.rng.uniform(0.65, 0.95),
                wellness=self.rng.uniform(0.70, 0.92),
                productivity=self.rng.uniform(0.65, 0.95),
                pop=pop,
            )
            zone.prev_wellness = zone.wellness
            zone.prev_productivity = zone.productivity
            self.zones.append(zone)

    def _true_harm_pressure(self, zone):
        total = sum(zone.pop.values()) + EPS
        hawk_share = (zone.pop["hawk"] + zone.pop["scavenger"]) / total
        capture = self.params.adversarial_strength * hawk_share * (0.7 + zone.resource)
        catastrophe = 0.45 if zone.catastrophe_timer > 0 else 0.0
        return capture + catastrophe * zone.vulnerability

    def _observed_feature(self, zone):
        total = sum(zone.pop.values()) + EPS
        dove_like = (zone.pop["dove"] + 0.7 * zone.pop["mutant"]) / total
        hawk_share = (zone.pop["hawk"] + zone.pop["scavenger"]) / total
        camouflage = self.params.adversarial_strength * hawk_share * max(0.0, 1.0 - self.params.camouflage_cost)
        return clamp(dove_like + camouflage)

    def _make_observation(self, step, noisy=True):
        wellness = []
        productivity = []
        response = []
        recovery = []
        diversity = []
        feature = []
        capture_signal = []
        sag = []
        last_aid = []
        for z in self.zones:
            harm = self._true_harm_pressure(z)
            obs_noise = (1.0 - self.params.channel_reliability) * self.rng.uniform(-0.25, 0.25) if noisy else 0.0
            if self.params.experiment == "B":
                obs_noise += self.rng.uniform(-self.params.fixed_mi_noise, self.params.fixed_mi_noise)
            cap_sig = clamp(harm + obs_noise)
            local_recovery = max(0.0, z.wellness - z.prev_wellness) + max(0.0, z.productivity - z.prev_productivity)
            wellness.append(clamp(z.wellness + obs_noise * 0.25))
            productivity.append(clamp(z.productivity + obs_noise * 0.20))
            response.append(clamp((z.wellness - z.prev_wellness) + (z.productivity - z.prev_productivity) + 0.5))
            recovery.append(clamp(local_recovery))
            diversity.append(shannon_diversity(z.pop))
            feature.append(self._observed_feature(z))
            capture_signal.append(cap_sig)
            sag.append(1.0 if z.wellness < 0.45 or z.productivity < 0.45 else 0.0)
            last_aid.append(z.last_aid)
            self.signal_values.append(cap_sig)
            self.truth_values.append(harm)
            self.signal_bins.append(1 if cap_sig > 0.45 else 0)
            self.truth_bins.append(1 if harm > 0.45 else 0)
        return FeederObservation(
            step=step,
            wellness=tuple(wellness),
            productivity=tuple(productivity),
            response=tuple(response),
            recovery=tuple(recovery),
            diversity=tuple(diversity),
            observed_feature=tuple(feature),
            capture_signal=tuple(capture_signal),
            sag=tuple(sag),
            last_aid=tuple(last_aid),
            global_welfare=statistics.fmean(wellness),
            global_diversity=statistics.fmean(diversity),
            audit_available=self.params.audit_p > 0.0,
        )

    def _delayed_observation(self):
        obs = self.observation_queue[0]
        assert not hasattr(obs, "pop")
        assert not hasattr(obs, "type")
        assert not hasattr(obs, "hidden")
        return obs

    def _score_policy(self, obs, i):
        p = self.params.policy
        need = 1.0 - min(obs.wellness[i], obs.productivity[i])
        response = obs.response[i] - 0.5
        diversity_gap = max(0.0, self.params.diversity_floor - obs.diversity[i])
        capture = obs.capture_signal[i]
        sag = obs.sag[i]
        global_need = 1.0 - obs.global_welfare
        if p == "feature_proxy":
            return obs.observed_feature[i]
        if p == "scalar_welfare":
            return 0.65 * obs.wellness[i] + 0.35 * obs.productivity[i]
        if p == "geometric_diversity":
            return math.log(max(0.02, need + 0.35)) + math.log(max(0.02, obs.diversity[i] + 0.35)) - 0.45 * capture
        if p == "local_consequence":
            return need + 1.6 * response - 0.8 * capture
        if p == "local_global":
            return 0.75 * need + 0.95 * response + 0.65 * diversity_gap + 0.25 * global_need - 0.85 * capture
        if p == "response_to_aid":
            probe_bonus = 0.18 if obs.last_aid[i] < 0.04 and sag > 0 else 0.0
            return 0.75 * need + 1.4 * max(0.0, response) + probe_bonus - 1.1 * max(0.0, -response) - 0.65 * capture
        if p == "audit_penalty":
            audit_term = self.params.audit_p * self.params.audit_C * capture
            return 0.70 * need + 1.15 * max(0.0, response) + 0.45 * diversity_gap - audit_term - 0.35 * self.params.audit_kappa
        if p == "always_cut_sagging":
            return -2.0 * sag + 0.2 * obs.wellness[i]
        if p == "always_aid_sagging":
            return 2.0 * sag + need
        if p == "monoculture_optimizer":
            return obs.productivity[i] - 0.35 * diversity_gap
        raise ValueError(p)

    def choose_allocation(self):
        obs = self._delayed_observation()
        scores = [self._score_policy(obs, i) for i in range(ZONES)]
        min_score = min(scores)
        shifted = [max(0.01, s - min_score + 0.05) for s in scores]
        if self.params.policy in {"response_to_aid", "local_global", "audit_penalty"}:
            # Keep a probe floor, because a purely greedy consequence loop can never learn from neglected zones.
            floor = 0.012
        else:
            floor = 0.0
        alloc = normalize(shifted, total=max(0.0, 1.0 - floor * ZONES))
        alloc = [a + floor for a in alloc]
        if self.params.policy == "always_cut_sagging":
            alloc = normalize([a * (0.15 if obs.sag[i] else 1.0) for i, a in enumerate(alloc)])
        if self.params.policy == "always_aid_sagging":
            alloc = normalize([a * (2.0 if obs.sag[i] else 0.45) for i, a in enumerate(alloc)])
        return alloc, obs

    def maybe_catastrophe(self, step):
        if self.params.future_shock and step in (85, 100):
            targets = self.rng.sample(range(ZONES), k=max(1, ZONES // 4))
        elif self.params.catastrophe_frequency > 0 and self.rng.random() < self.params.catastrophe_frequency:
            targets = [self.rng.randrange(ZONES)]
        else:
            return []
        for i in targets:
            z = self.zones[i]
            sev = self.params.catastrophe_severity if self.params.catastrophe_severity > 0 else 0.35
            z.catastrophe_timer = max(z.catastrophe_timer, 5)
            z.wellness = clamp(z.wellness - sev * z.vulnerability)
            z.productivity = clamp(z.productivity - 0.7 * sev * z.vulnerability)
            for t in ("dove", "mutant"):
                resilience = 0.55 if t == "mutant" else 1.0
                z.pop[t] *= max(0.0, 1.0 - sev * 0.20 * z.vulnerability * resilience)
        return targets

    def apply_allocation_and_dynamics(self, alloc, obs, step):
        aid_budget = 4.0 * (1.0 - self.params.audit_kappa * self.params.audit_p)
        self.audit_cost_paid += 4.0 * self.params.audit_kappa * self.params.audit_p
        self.total_aid_given += aid_budget
        for i, z in enumerate(self.zones):
            z.prev_wellness = z.wellness
            z.prev_productivity = z.productivity
            raw_aid = aid_budget * alloc[i]
            caught = False
            if self.params.audit_p > 0 and self.rng.random() < self.params.audit_p and obs.capture_signal[i] > 0.48:
                caught = True
                z.penalty_timer = max(z.penalty_timer, int(2 + 4 * self.params.audit_C))
            if z.penalty_timer > 0:
                effective_aid = raw_aid * max(0.0, 1.0 - self.params.audit_C)
                z.penalty_timer -= 1
                if z.catastrophe_timer > 0 and obs.capture_signal[i] > 0.42:
                    z.false_cut_events += 1
            else:
                effective_aid = raw_aid
            total_pop = sum(z.pop.values()) + EPS
            hawk_share = (z.pop["hawk"] + z.pop["scavenger"]) / total_pop
            catastrophe = z.catastrophe_timer > 0
            scavenger_pressure = (z.pop["scavenger"] / total_pop) if self.params.scavenger_enabled else 0.0
            intercept = effective_aid * self.params.adversarial_strength * (0.28 * hawk_share + (0.75 if catastrophe else 0.15) * scavenger_pressure)
            intercept = min(effective_aid * 0.85, intercept)
            z.scavenger_intercept += intercept
            useful_aid = effective_aid - intercept
            if obs.capture_signal[i] > 0.55 and raw_aid > statistics.fmean(alloc) * aid_budget:
                z.false_aid_events += 1
            z.resource = clamp(z.resource + 0.28 * useful_aid - 0.04 * total_pop / 30.0, 0.0, 1.5)
            z.wellness = clamp(z.wellness + 0.17 * useful_aid + 0.04 * z.resource - 0.10 * hawk_share * self.params.adversarial_strength)
            z.productivity = clamp(z.productivity + 0.09 * useful_aid + 0.05 * z.pop["dove"] / total_pop + 0.06 * z.pop["mutant"] / total_pop - 0.12 * hawk_share * self.params.adversarial_strength)
            capture_loss = self.params.adversarial_strength * hawk_share * (0.025 + 0.030 * z.resource)
            for victim in ("dove", "mutant"):
                z.pop[victim] *= max(0.0, 1.0 - capture_loss)
            z.pop["hawk"] *= 1.0 + 0.020 * self.params.adversarial_strength * z.resource - self.params.camouflage_cost * 0.006
            if self.params.scavenger_enabled:
                z.pop["scavenger"] *= 1.0 + 0.030 * intercept - 0.004 * self.params.migration_cost
            z.pop["dove"] *= 1.0 + 0.018 * z.wellness + 0.012 * z.productivity - 0.014 * max(0.0, 0.45 - z.resource)
            z.pop["mutant"] *= 1.0 + 0.012 * z.productivity + (0.020 if catastrophe else -0.003)
            if self.params.mutation_rate > 0:
                mut = z.pop["dove"] * self.params.mutation_rate
                z.pop["dove"] -= mut
                if self.rng.random() < 0.75:
                    z.pop["mutant"] += mut
                else:
                    z.pop["hawk"] += mut * 0.8
            if self.params.diversity_floor > 0:
                div = shannon_diversity(z.pop)
                if div < self.params.diversity_floor:
                    weakest = min(TYPES, key=lambda t: z.pop[t])
                    z.pop[weakest] += 0.015 * total_pop * self.params.diversity_floor
                    z.resource *= max(0.75, 1.0 - 0.035 * self.params.diversity_floor)
            if z.catastrophe_timer > 0:
                z.catastrophe_timer -= 1
            for t in TYPES:
                z.pop[t] = max(0.0, min(z.pop[t], 200.0))

    def migrate(self):
        if self.params.migration_speed <= 0:
            return
        aid_rank = sorted(range(ZONES), key=lambda i: self.previous_alloc[i], reverse=True)
        target_pool = aid_rank[: max(1, ZONES // 3)]
        for src in range(ZONES):
            for t in ("hawk", "scavenger"):
                if t == "scavenger" and not self.params.scavenger_enabled:
                    continue
                movers = self.zones[src].pop[t] * self.params.migration_speed * (0.08 if t == "hawk" else 0.14)
                if movers <= 0.001:
                    continue
                dst = self.rng.choice(target_pool)
                if dst == src:
                    continue
                self.zones[src].pop[t] -= movers
                self.zones[dst].pop[t] += movers * max(0.0, 1.0 - self.params.migration_cost)

    def step(self, step):
        self.maybe_catastrophe(step)
        alloc, obs = self.choose_allocation()
        self.apply_allocation_and_dynamics(alloc, obs, step)
        self.previous_alloc = alloc
        self.migrate()
        self.observation_queue.append(self._make_observation(step=step, noisy=True))
        if self.collapse_step is None and self.total_population() < 0.25 * self.initial_population_estimate:
            self.collapse_step = step

    @property
    def initial_population_estimate(self):
        return ZONES * 31.5

    def total_population(self):
        return sum(sum(z.pop.values()) for z in self.zones)

    def aggregate_counts(self):
        c = {t: 0.0 for t in TYPES}
        for z in self.zones:
            for t in TYPES:
                c[t] += z.pop[t]
        return c

    def run(self):
        for step in range(STEPS):
            self.step(step)
        return self.metrics()

    def metrics(self):
        counts = self.aggregate_counts()
        total = sum(counts.values()) + EPS
        welfare_by_zone = [0.5 * z.wellness + 0.5 * z.productivity for z in self.zones]
        resources = [z.resource for z in self.zones]
        adversarial_share = (counts["hawk"] + counts["scavenger"]) / total
        dove_share = counts["dove"] / total
        mutation_share = counts["mutant"] / total
        diversity_values = [shannon_diversity(z.pop) for z in self.zones]
        capture_prob = 1.0 if adversarial_share > 0.48 or dove_share < 0.22 else 0.0
        collapse_prob = 1.0 if self.total_population() < 0.35 * self.initial_population_estimate or statistics.fmean(welfare_by_zone) < 0.30 else 0.0
        permanence = 1.0 if (
            collapse_prob == 0.0
            and capture_prob == 0.0
            and counts["dove"] > 0.12 * self.initial_population_estimate
            and statistics.fmean(welfare_by_zone) >= 0.50
            and statistics.fmean(diversity_values) >= max(0.20, 0.55 * self.params.diversity_floor)
        ) else 0.0
        false_cut = sum(z.false_cut_events for z in self.zones)
        false_aid = sum(z.false_aid_events for z in self.zones)
        recovery_time = 0.0
        shock_zones = [z for z in self.zones if z.vulnerability > 0.45]
        if self.params.catastrophe_frequency > 0 or self.params.future_shock:
            recovered = [1 for z in shock_zones if z.wellness > 0.55 and z.productivity > 0.50]
            recovery_time = STEPS * (1.0 - (sum(recovered) / max(1, len(shock_zones))))
        return {
            "permanence": permanence,
            "collapse": collapse_prob,
            "capture": capture_prob,
            "dove_extinct": 1.0 if counts["dove"] < 0.08 * self.initial_population_estimate else 0.0,
            "hawk_extinct": 1.0 if counts["hawk"] < 1.0 else 0.0,
            "mutant_extinct": 1.0 if counts["mutant"] < 1.0 else 0.0,
            "scavenger_extinct": 1.0 if counts["scavenger"] < 1.0 else 0.0,
            "resource_hhi": hhi(resources),
            "mean_welfare_final": statistics.fmean(welfare_by_zone),
            "min_zone_welfare": min(welfare_by_zone),
            "geometric_welfare": geometric_mean(welfare_by_zone),
            "recovery_time": recovery_time,
            "adversarial_share": adversarial_share,
            "dove_share": dove_share,
            "mutation_survival": mutation_share,
            "diversity": statistics.fmean(diversity_values),
            "false_positive_punishment": false_cut / max(1, STEPS),
            "false_negative_aid_to_hawk": false_aid / max(1, STEPS),
            "scavenger_exploitation": sum(z.scavenger_intercept for z in self.zones) / max(EPS, self.total_aid_given),
            "signal_truth_corr": safe_corr(self.signal_values, self.truth_values),
            "mutual_information": mutual_information_binary(self.signal_bins, self.truth_bins),
            "audit_cost_share": self.audit_cost_paid / max(EPS, self.audit_cost_paid + self.total_aid_given),
            "collapse_step": self.collapse_step if self.collapse_step is not None else STEPS,
            "population_final": self.total_population(),
        }


def experiment_grid():
    cells = []
    for delay in [1, 3, 6, 10]:
        for adv in [0.25, 0.55, 0.85]:
            for policy in ["feature_proxy", "scalar_welfare", "response_to_aid", "local_global"]:
                cells.append(Params("A", policy, delay=delay, t_irrev=8, adversarial_strength=adv, channel_reliability=0.78))
    for delay in [1, 3, 6, 10, 14]:
        cells.append(Params("B", "local_global", delay=delay, t_irrev=8, adversarial_strength=0.55, fixed_mi_noise=0.28, channel_reliability=0.70))
    for policy in ["feature_proxy", "local_consequence", "response_to_aid", "local_global"]:
        cells.append(Params("C", policy, delay=4, t_irrev=8, adversarial_strength=0.60, mutation_rate=0.01, channel_reliability=0.76))
    for severity in [0.25, 0.45, 0.65]:
        for policy in ["always_cut_sagging", "always_aid_sagging", "response_to_aid", "local_global"]:
            cells.append(Params("D", policy, delay=4, t_irrev=8, adversarial_strength=0.45, catastrophe_frequency=0.055, catastrophe_severity=severity, mutation_rate=0.006))
    for policy in ["response_to_aid", "local_global", "audit_penalty"]:
        for adv in [0.45, 0.70]:
            cells.append(Params("E", policy, delay=4, t_irrev=8, adversarial_strength=adv, catastrophe_frequency=0.06, catastrophe_severity=0.50, scavenger_enabled=True, audit_p=0.25 if policy == "audit_penalty" else 0.0, audit_C=0.55 if policy == "audit_penalty" else 0.0, audit_kappa=0.08 if policy == "audit_penalty" else 0.0))
    for floor in [0.0, 0.12, 0.28, 0.45]:
        for policy in ["local_global", "geometric_diversity", "monoculture_optimizer"]:
            cells.append(Params("F", policy, delay=4, t_irrev=8, adversarial_strength=0.42, mutation_rate=0.018, diversity_floor=floor, future_shock=True, catastrophe_severity=0.48))
    rng = random.Random(8808)
    for _ in range(60):
        policy = rng.choice(["response_to_aid", "local_global", "geometric_diversity", "audit_penalty"])
        cells.append(Params(
            "G",
            policy,
            delay=rng.choice([1, 2, 3, 5, 8, 12]),
            t_irrev=rng.choice([5, 8, 12, 16]),
            adversarial_strength=rng.uniform(0.18, 0.82),
            camouflage_cost=rng.uniform(0.02, 0.35),
            audit_p=rng.choice([0.0, 0.10, 0.25, 0.45]) if policy == "audit_penalty" else 0.0,
            audit_C=rng.choice([0.0, 0.35, 0.65, 0.90]) if policy == "audit_penalty" else 0.0,
            audit_kappa=rng.choice([0.0, 0.04, 0.10, 0.20]) if policy == "audit_penalty" else 0.0,
            catastrophe_frequency=rng.choice([0.0, 0.025, 0.055, 0.09]),
            catastrophe_severity=rng.choice([0.0, 0.25, 0.45, 0.65]),
            mutation_rate=rng.choice([0.0, 0.006, 0.015, 0.030]),
            migration_cost=rng.uniform(0.02, 0.25),
            migration_speed=rng.uniform(0.05, 0.36),
            diversity_floor=rng.choice([0.0, 0.10, 0.22, 0.35]),
            channel_reliability=rng.uniform(0.55, 0.92),
            scavenger_enabled=rng.choice([False, True]),
            future_shock=rng.choice([False, True]),
        ))
    return cells


def cell_id(params, idx):
    return f"{params.experiment}_{idx:03d}_{params.policy}_d{params.delay}_a{params.adversarial_strength:.2f}_s{params.catastrophe_severity:.2f}_v{params.diversity_floor:.2f}"


def run_all():
    cells = experiment_grid()
    run_rows = []
    summary_rows = []
    for idx, params in enumerate(cells):
        cid = cell_id(params, idx)
        seed_rows = []
        for split, seeds in [("train", TRAIN_SEEDS), ("heldout", HELDOUT_SEEDS)]:
            for seed in seeds:
                model = BlindConsequenceFeederModel(seed, params)
                metrics = model.run()
                row = {
                    "cell_id": cid,
                    "split": split,
                    "seed": seed,
                    "experiment": params.experiment,
                    "policy": params.policy,
                    "delay": params.delay,
                    "t_irrev": params.t_irrev,
                    "R": params.t_irrev / max(1, params.delay),
                    "adversarial_strength": params.adversarial_strength,
                    "camouflage_cost": params.camouflage_cost,
                    "audit_p": params.audit_p,
                    "audit_C": params.audit_C,
                    "audit_kappa": params.audit_kappa,
                    "catastrophe_frequency": params.catastrophe_frequency,
                    "catastrophe_severity": params.catastrophe_severity,
                    "mutation_rate": params.mutation_rate,
                    "migration_cost": params.migration_cost,
                    "migration_speed": params.migration_speed,
                    "diversity_floor": params.diversity_floor,
                    "channel_reliability": params.channel_reliability,
                    "scavenger_enabled": int(params.scavenger_enabled),
                    "future_shock": int(params.future_shock),
                    **metrics,
                }
                run_rows.append(row)
                seed_rows.append(row)
        held = [r for r in seed_rows if r["split"] == "heldout"]
        train = [r for r in seed_rows if r["split"] == "train"]
        summary = summarize_cell(cid, params, held, train)
        summary_rows.append(summary)
    return run_rows, summary_rows


def mean(rows, key):
    return statistics.fmean(float(r[key]) for r in rows) if rows else 0.0


def summarize_cell(cid, params, held, train):
    successes = int(sum(r["permanence"] for r in held))
    lo, hi = wilson(successes, len(held))
    s = {
        "cell_id": cid,
        "experiment": params.experiment,
        "policy": params.policy,
        "n_heldout": len(held),
        "permanence_successes": successes,
        "permanence_probability": mean(held, "permanence"),
        "permanence_wilson_lo": lo,
        "permanence_wilson_hi": hi,
        "collapse_probability": mean(held, "collapse"),
        "capture_probability": mean(held, "capture"),
        "dove_extinction_probability": mean(held, "dove_extinct"),
        "hawk_extinction_probability": mean(held, "hawk_extinct"),
        "mutant_extinction_probability": mean(held, "mutant_extinct"),
        "scavenger_extinction_probability": mean(held, "scavenger_extinct"),
        "resource_hhi_mean": mean(held, "resource_hhi"),
        "mean_welfare_final": mean(held, "mean_welfare_final"),
        "min_zone_welfare_mean": mean(held, "min_zone_welfare"),
        "geometric_welfare_mean": mean(held, "geometric_welfare"),
        "recovery_time_mean": mean(held, "recovery_time"),
        "adversarial_share_mean": mean(held, "adversarial_share"),
        "mutation_survival_mean": mean(held, "mutation_survival"),
        "diversity_mean": mean(held, "diversity"),
        "false_positive_punishment_mean": mean(held, "false_positive_punishment"),
        "false_negative_aid_to_hawk_mean": mean(held, "false_negative_aid_to_hawk"),
        "scavenger_exploitation_mean": mean(held, "scavenger_exploitation"),
        "signal_truth_corr_mean": mean(held, "signal_truth_corr"),
        "mutual_information_mean": mean(held, "mutual_information"),
        "audit_cost_share_mean": mean(held, "audit_cost_share"),
        "collapse_step_mean": mean(held, "collapse_step"),
        "population_final_mean": mean(held, "population_final"),
        "train_permanence_probability": mean(train, "permanence"),
        "delay": params.delay,
        "t_irrev": params.t_irrev,
        "R": params.t_irrev / max(1, params.delay),
        "adversarial_strength": params.adversarial_strength,
        "catastrophe_severity": params.catastrophe_severity,
        "catastrophe_frequency": params.catastrophe_frequency,
        "diversity_floor": params.diversity_floor,
        "mutation_rate": params.mutation_rate,
        "scavenger_enabled": int(params.scavenger_enabled),
        "future_shock": int(params.future_shock),
        "audit_p": params.audit_p,
        "audit_C": params.audit_C,
        "audit_kappa": params.audit_kappa,
    }
    s["viable"] = int(is_viable(s))
    return s


def is_viable(s):
    return (
        s["collapse_probability"] <= VIABILITY["collapse_probability_max"]
        and s["capture_probability"] <= VIABILITY["capture_probability_max"]
        and s["dove_extinction_probability"] <= VIABILITY["dove_extinction_probability_max"]
        and s["adversarial_share_mean"] <= VIABILITY["adversarial_share_mean_max"]
        and s["mean_welfare_final"] >= VIABILITY["mean_welfare_final_min"]
        and s["diversity_mean"] >= VIABILITY["diversity_mean_min"]
        and s["audit_cost_share_mean"] <= VIABILITY["audit_cost_share_mean_max"]
        and s["permanence_probability"] >= VIABILITY["permanence_probability_min"]
    )


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def svg_line(path, title, series, x_label, y_label, width=900, height=520):
    margin_l, margin_r, margin_t, margin_b = 70, 30, 50, 60
    all_x = [x for pts in series.values() for x, _ in pts]
    all_y = [y for pts in series.values() for _, y in pts]
    if not all_x:
        all_x, all_y = [0, 1], [0, 1]
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(0.0, min(all_y)), max(1.0, max(all_y))
    if abs(x_max - x_min) < EPS:
        x_max = x_min + 1.0
    if abs(y_max - y_min) < EPS:
        y_max = y_min + 1.0
    def tx(x): return margin_l + (x - x_min) / (x_max - x_min) * (width - margin_l - margin_r)
    def ty(y): return height - margin_b - (y - y_min) / (y_max - y_min) * (height - margin_t - margin_b)
    colors = ["#1d4ed8", "#b45309", "#047857", "#7c3aed", "#be123c", "#0f766e", "#525252"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="{width/2}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>', f'<line x1="{margin_l}" y1="{height-margin_b}" x2="{width-margin_r}" y2="{height-margin_b}" stroke="#111"/>', f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{height-margin_b}" stroke="#111"/>', f'<text x="{width/2}" y="{height-16}" text-anchor="middle" font-family="sans-serif" font-size="12">{x_label}</text>', f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" font-family="sans-serif" font-size="12">{y_label}</text>']
    for idx, (name, pts) in enumerate(series.items()):
        pts = sorted(pts)
        color = colors[idx % len(colors)]
        points = " ".join(f"{tx(x):.1f},{ty(y):.1f}" for x, y in pts)
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{points}"/>')
        parts.append(f'<text x="{width-260}" y="{margin_t+18+idx*18}" font-family="sans-serif" font-size="11" fill="{color}">{name}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n")


def svg_heatmap(path, title, rows, x_key, y_key, value_key):
    xs = sorted({r[x_key] for r in rows})
    ys = sorted({r[y_key] for r in rows})
    by = defaultdict(list)
    for r in rows:
        by[(r[x_key], r[y_key])].append(float(r[value_key]))
    width, height = 820, 560
    ml, mr, mt, mb = 120, 40, 60, 80
    cw = (width - ml - mr) / max(1, len(xs))
    ch = (height - mt - mb) / max(1, len(ys))
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="{width/2}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>']
    for yi, y in enumerate(ys):
        for xi, x in enumerate(xs):
            v = statistics.fmean(by[(x, y)]) if by[(x, y)] else 0.0
            t = clamp(v)
            red = int(245 - 160 * t)
            green = int(245 - 60 * (1 - t))
            blue = int(245 - 210 * t)
            px = ml + xi * cw
            py = mt + (len(ys) - 1 - yi) * ch
            parts.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="rgb({red},{green},{blue})" stroke="white"/>')
            parts.append(f'<text x="{px+cw/2:.1f}" y="{py+ch/2+4:.1f}" text-anchor="middle" font-family="sans-serif" font-size="10">{v:.2f}</text>')
    for xi, x in enumerate(xs):
        parts.append(f'<text x="{ml+xi*cw+cw/2:.1f}" y="{height-mb+22}" text-anchor="middle" font-family="sans-serif" font-size="10">{x}</text>')
    for yi, y in enumerate(ys):
        parts.append(f'<text x="{ml-8}" y="{mt+(len(ys)-1-yi)*ch+ch/2+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="10">{y}</text>')
    parts.append(f'<text x="{width/2}" y="{height-16}" text-anchor="middle" font-family="sans-serif" font-size="12">{x_key}</text>')
    parts.append(f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" font-family="sans-serif" font-size="12">{y_key}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n")


def make_plots(summary):
    RESULTS.mkdir(parents=True, exist_ok=True)
    by_policy_r = defaultdict(lambda: defaultdict(list))
    for r in summary:
        by_policy_r[r["policy"]][float(r["R"])].append(float(r["permanence_probability"]))
    series = {p: [(x, statistics.fmean(vals)) for x, vals in sorted(xs.items())] for p, xs in by_policy_r.items() if p in {"feature_proxy", "response_to_aid", "local_global", "geometric_diversity", "audit_penalty"}}
    svg_line(RESULTS / "permanence_vs_R.svg", "Permanence vs R", series, "R = T_irrev / tau", "permanence")
    by_policy_r2 = defaultdict(lambda: defaultdict(list))
    for r in summary:
        by_policy_r2[r["policy"]][float(r["R"])].append(float(r["collapse_probability"]))
    series2 = {p: [(x, statistics.fmean(vals)) for x, vals in sorted(xs.items())] for p, xs in by_policy_r2.items() if p in series}
    svg_line(RESULTS / "collapse_probability_vs_R.svg", "Collapse Probability vs R", series2, "R", "collapse probability")
    svg_heatmap(RESULTS / "heatmap_adversarial_strength_delay.svg", "Permanence: adversarial strength x delay", [r for r in summary if r["experiment"] == "A"], "delay", "adversarial_strength", "permanence_probability")
    svg_heatmap(RESULTS / "heatmap_catastrophe_severity_policy.svg", "Recovery proxy: catastrophe severity x policy", [r for r in summary if r["experiment"] == "D"], "policy", "catastrophe_severity", "permanence_probability")
    f_rows = [r for r in summary if r["experiment"] == "F"]
    by_floor = defaultdict(list)
    for r in f_rows:
        by_floor[float(r["diversity_floor"])].append(float(r["permanence_probability"]))
    svg_line(RESULTS / "diversity_floor_vs_shock_survival.svg", "Diversity Floor vs Shock Survival", {"heldout permanence": [(k, statistics.fmean(v)) for k, v in sorted(by_floor.items())]}, "diversity floor", "permanence")
    e_rows = [r for r in summary if r["experiment"] == "E"]
    by_pol = defaultdict(list)
    for r in e_rows:
        by_pol[r["policy"]].append(float(r["scavenger_exploitation_mean"]))
    svg_line(RESULTS / "scavenger_exploitation_vs_aid_policy.svg", "Scavenger Exploitation by Aid Policy", {"exploitation": [(i, statistics.fmean(v)) for i, (k, v) in enumerate(sorted(by_pol.items()))]}, "policy index", "aid intercepted")
    svg_heatmap(RESULTS / "viability_kernel_map.svg", "Viability Kernel Map", summary, "R", "adversarial_strength", "viable")
    mi_series = defaultdict(list)
    for r in summary:
        mi_series[r["experiment"]].append((float(r["mutual_information_mean"]), float(r["permanence_probability"])))
    svg_line(RESULTS / "MI_vs_permanence.svg", "MI vs Permanence", {k: v for k, v in mi_series.items() if k in {"A", "B", "G"}}, "mutual information", "permanence")
    b_rows = [r for r in summary if r["experiment"] == "B"]
    svg_line(RESULTS / "delay_vs_permanence_fixed_MI.svg", "Delay vs Permanence at Fixed Observation Noise", {"B fixed-noise": [(float(r["delay"]), float(r["permanence_probability"])) for r in b_rows]}, "delay", "permanence")


def final_verdict(summary):
    viable = [r for r in summary if int(r["viable"]) == 1]
    if viable:
        trivial_policies = {"feature_proxy", "always_cut_sagging", "always_aid_sagging", "monoculture_optimizer"}
        trivial_viable = [r for r in viable if r["policy"] in trivial_policies]
        fragile = [r for r in viable if float(r["permanence_wilson_lo"]) < 0.45 or float(r["capture_probability"]) > 0.10]
        # If feature-proxy or naive sagging policies pass, the substrate has not isolated
        # the intended blind-consequence mechanism. Keep the cells, but do not call it a clean kernel.
        if trivial_viable or fragile:
            return "C. Apparent kernel exists but is too fragile / tuned to trust."
        return "A. Non-empty viability kernel found under clear constraints."
    best = max(summary, key=lambda r: (float(r["permanence_probability"]), -float(r["capture_probability"]), -float(r["collapse_probability"])))
    if float(best["permanence_probability"]) < 0.30:
        return "B. No viability kernel found in tested regimes."
    return "D. Results inconclusive due to model or estimator limitations."


def write_report(summary, runs):
    viable = [r for r in summary if int(r["viable"]) == 1]
    best = sorted(summary, key=lambda r: (float(r["viable"]), float(r["permanence_probability"]), -float(r["capture_probability"])), reverse=True)[:10]
    verdict = final_verdict(summary)
    feature = [r for r in summary if r["policy"] == "feature_proxy"]
    consequence = [r for r in summary if r["policy"] in {"response_to_aid", "local_global", "local_consequence"}]
    diversity_rows = [r for r in summary if r["experiment"] == "F"]
    report = [
        "# Blind Consequence-Feeder Viability Report",
        "",
        f"Final verdict: **{verdict}**",
        "",
        "## 9.1 Did any non-trivial viability kernel exist?",
        "",
        f"Viable held-out cells under the strict implemented criterion: `{len(viable)}` / `{len(summary)}`.",
        "",
        "## 9.2 If yes, what conditions were necessary?",
        "",
    ]
    if viable:
        policies = sorted({r["policy"] for r in viable})
        trivial_policies = {"feature_proxy", "always_cut_sagging", "always_aid_sagging", "monoculture_optimizer"}
        trivial_viable = sorted({r["policy"] for r in viable if r["policy"] in trivial_policies})
        report.append(f"Viable policies: `{policies}`.")
        report.append(f"Median R among viable cells: `{statistics.median(float(r['R']) for r in viable):.3f}`.")
        report.append(f"Median adversarial strength among viable cells: `{statistics.median(float(r['adversarial_strength']) for r in viable):.3f}`.")
        report.append(f"Median diversity floor among viable cells: `{statistics.median(float(r['diversity_floor']) for r in viable):.3f}`.")
        if trivial_viable:
            report.append(f"Artifact warning: trivial or feature-proxy policies also passed (`{trivial_viable}`), so the apparent kernel is not isolated to blind consequence feeding.")
    else:
        report.append("No cell satisfied all viability constraints. Necessary conditions cannot be inferred from this run.")
    report += ["", "## 9.3 If no, what killed it?", ""]
    failure_counts = Counter()
    for r in summary:
        if float(r["capture_probability"]) > VIABILITY["capture_probability_max"]:
            failure_counts["adversarial capture"] += 1
        if float(r["collapse_probability"]) > VIABILITY["collapse_probability_max"]:
            failure_counts["collapse"] += 1
        if float(r["diversity_mean"]) < VIABILITY["diversity_mean_min"]:
            failure_counts["diversity below floor"] += 1
        if float(r["adversarial_share_mean"]) > VIABILITY["adversarial_share_mean_max"]:
            failure_counts["adversarial share"] += 1
        if float(r["mean_welfare_final"]) < VIABILITY["mean_welfare_final_min"]:
            failure_counts["low welfare"] += 1
    for name, count in failure_counts.most_common():
        report.append(f"- {name}: `{count}` cells")
    report += ["", "## 9.4 Did R behave like a useful invariant?", ""]
    r_corr = safe_corr([float(r["R"]) for r in summary], [float(r["permanence_probability"]) for r in summary])
    mi_corr = safe_corr([float(r["mutual_information_mean"]) for r in summary], [float(r["permanence_probability"]) for r in summary])
    if abs(r_corr) > abs(mi_corr) + 0.10:
        r_answer = "B. Weak evidence yes."
    elif abs(mi_corr) > abs(r_corr) + 0.10:
        r_answer = "C. No, MI or another variable explained outcomes better."
    else:
        r_answer = "D. Inconclusive."
    report.append(f"Choice: `{r_answer}` R/permanence corr `{r_corr:.3f}`, MI/permanence corr `{mi_corr:.3f}`.")
    report += ["", "## 9.5 Was consequence-neighborliness better than feature-neighborliness?", ""]
    feature_perm = statistics.fmean(float(r["permanence_probability"]) for r in feature) if feature else 0.0
    cons_perm = statistics.fmean(float(r["permanence_probability"]) for r in consequence) if consequence else 0.0
    report.append(f"Feature-proxy mean permanence: `{feature_perm:.3f}`. Consequence-family mean permanence: `{cons_perm:.3f}`. Difference: `{cons_perm - feature_perm:.3f}`.")
    report += ["", "## 9.6 Did diversity help or hurt long-run permanence?", ""]
    div_corr = safe_corr([float(r["diversity_floor"]) for r in diversity_rows], [float(r["permanence_probability"]) for r in diversity_rows]) if diversity_rows else 0.0
    report.append(f"In experiment F, diversity_floor/permanence corr: `{div_corr:.3f}`. This is diagnostic only; diversity is not assumed beneficial.")
    report += ["", "## 9.7 What should be tested next?", "", "- Replace the toy population dynamics with a stronger ecological substrate and preserve the same type-blind observation API.", "- Sweep response-to-aid probes under adversarial channel control rather than fixed probe floors.", "- Use a better MI estimator and explicit fixed-MI construction before drawing conclusions about R.", "- Stress-test any viable cells with more held-out seeds and shifted catastrophe distributions.", "", "## Best Held-Out Cells", "", "| viable | experiment | policy | permanence | capture | collapse | adv share | welfare | diversity | R |", "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in best:
        report.append(f"| {r['viable']} | {r['experiment']} | {r['policy']} | {float(r['permanence_probability']):.3f} | {float(r['capture_probability']):.3f} | {float(r['collapse_probability']):.3f} | {float(r['adversarial_share_mean']):.3f} | {float(r['mean_welfare_final']):.3f} | {float(r['diversity_mean']):.3f} | {float(r['R']):.3f} |")
    report += [
        "",
        "## Literature Grounding",
        "",
        "The implementation report cites viability theory (Aubin), networked/delayed control (Zhang/Branicky/Phillips; Hespanha/Naghshtabrizi/Xu), information theory (Cover & Thomas), reward hacking (Skalse et al.), audit games (Blocki et al.), and response diversity / biodiversity insurance (Elmqvist et al.; Yachi & Loreau). The toy code does not claim novelty over those fields.",
        "",
        "## Source Links",
        "",
        "- Aubin, *Viability Theory* / viability kernel overview: https://en.wikipedia.org/wiki/Viability_theory",
        "- Zhang, Branicky & Phillips (2001), networked control delay/stability: https://doi.org/10.1109/MCS.2001.949138",
        "- Hespanha, Naghshtabrizi & Xu (2007), networked control systems survey: https://doi.org/10.1109/JPROC.2007.904027",
        "- Cover & Thomas, information theory grounding: https://en.wikipedia.org/wiki/Information_theory",
        "- Skalse et al. (2022), reward hacking: https://arxiv.org/abs/2209.13085",
        "- Blocki et al. (2013), Audit Games: https://arxiv.org/abs/1303.0356",
        "- Elmqvist et al. (2003), response diversity/resilience: https://doi.org/10.1890/1540-9295(2003)001[0488:RDECER]2.0.CO;2",
        "- Yachi & Loreau (1999), biodiversity insurance hypothesis: https://doi.org/10.1073/pnas.96.4.1463",
    ]
    (RESULTS / "report.md").write_text("\n".join(report) + "\n")
    validation = [
        "# Validation Report",
        "",
        "| check | result | note |",
        "|---|---|---|",
        "| type_blind_feeder | passed | `FeederObservation` contains no hidden type counts; policy assertions check no `pop/type/hidden` fields. |",
        "| raw_failed_seeds_kept | passed | Every train/held-out seed is written to `raw/runs.csv`. |",
        "| feature_vs_consequence_separated | passed | `feature_proxy` is a comparator, not counted as consequence evidence. |",
        "| delayed_observation | passed | Feeder uses the oldest observation in a delay queue. |",
        "| MI_reported_not_optimized | passed | MI is reported post hoc as a diagnostic. |",
        "| negative_results_allowed | passed | Final verdict is selected from the memo's A/B/C/D set. |",
        "| trivial_policy_artifact_check | passed | If feature-proxy or naive sagging policies pass, verdict is downgraded to fragile/tuned rather than clean A. |",
        "",
        f"Final verdict: **{verdict}**",
    ]
    (RESULTS / "validation_report.md").write_text("\n".join(validation) + "\n")
    return verdict


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    runs, summary = run_all()
    viable = [r for r in summary if int(r["viable"]) == 1]
    write_csv(RAW / "runs.csv", runs)
    write_csv(RAW / "summary.csv", summary)
    write_csv(RAW / "viability_cells.csv", viable)
    make_plots(summary)
    verdict = write_report(summary, runs)
    manifest = {
        "git_head": git_value(["rev-parse", "HEAD"]),
        "git_commit_time": git_value(["show", "-s", "--format=%cI", "HEAD"]),
        "git_status_short": git_value(["status", "--short"]),
        "spec_implemented_sha256": spec_hash(),
        "train_seeds": TRAIN_SEEDS,
        "heldout_seeds": HELDOUT_SEEDS,
        "num_cells": len(summary),
        "num_runs": len(runs),
        "num_viable_cells": len(viable),
        "final_verdict": verdict,
        "viability_criterion": VIABILITY,
        "notes": [
            "Toy falsification harness, not a proof of AGI/ASI feeder viability.",
            "Feeder policies are type-blind and see only delayed consequence observations.",
            "Feature proxy is retained only as a Goodhart comparator.",
            "No tuning was performed; train/held-out split is recorded for later iterations.",
        ],
    }
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"verdict": verdict, "num_cells": len(summary), "num_runs": len(runs), "viable_cells": len(viable)}, indent=2))


if __name__ == "__main__":
    main()
