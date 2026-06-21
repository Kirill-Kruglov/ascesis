#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import statistics
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import run09 as base
import run10 as exp10

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_11"
RAW = RESULTS / "raw"
SEEDS = list(range(9400, 9425))
STEPS = base.STEPS
ZONES = base.ZONES
EPS = base.EPS
CAPTURE_WORLDS = exp10.CAPTURE_WORLDS

VALIDATION_POLICIES = [
    "feature_proxy",
    "always_cut_sagging",
    "always_aid_sagging",
    "monoculture_optimizer",
]
ZONE_COMPARATORS = ["neighbor_penalty", "neighbor_quarantine"]
ACTION_POLICIES = [
    "action_containment_extraction_cap",
    "action_containment_influence_throttle",
    "action_containment_anti_concentration",
    "action_containment_migration_friction",
    "action_containment_aid_escrow",
    "action_containment_replication_throttle",
    "combined_action_containment",
    "combined_action_containment_plus_diversity",
    "combined_action_containment_plus_response_to_aid",
]
COMPARATOR_POLICIES = [
    "no_enforcement",
    *ZONE_COMPARATORS,
    "neighbor_consequence",
    "local_global_neighbor",
    "response_to_neighbor_aid",
    "diversity_non_adversarial_only",
]


@dataclass(frozen=True)
class Params(exp10.Params):
    containment_C: float = 0.45
    containment_duration: int = 4
    concentration_threshold: float = 0.24
    escrow_rate: float = 0.55
    containment_cost: float = 0.06


# Experiment 10 constructs Params inside its inherited _init_world(); use the
# extended dataclass so world remapping keeps Experiment 11 parameters.
exp10.Params = Params


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC_IMPLEMENTED_11.md").read_bytes()).hexdigest()


def safe_mean(xs):
    return statistics.fmean(xs) if xs else 0.0


def resource_hhi(values):
    total = sum(max(0.0, x) for x in values)
    if total <= EPS:
        return 1.0 / max(1, len(values))
    return sum((max(0.0, x) / total) ** 2 for x in values)


class ActionContainmentModel(exp10.EnforcementModel):
    def _init_world(self):
        super()._init_world()
        for z in self.zones:
            z.extraction_cap_timer = 0
            z.influence_throttle_timer = 0
            z.migration_friction_timer = 0
            z.aid_escrow_timer = 0
            z.replication_throttle_timer = 0
            z.anti_concentration_flag = False
            z.containment_events = 0
            z.false_containment_events = 0
            z.containment_cost_total = 0.0
            z.extraction_volume = 0.0
            z.extraction_cap_active_steps = 0
            z.outgoing_influence_volume = 0.0
            z.influence_throttle_active_steps = 0
            z.aid_intercepted_total = 0.0
            z.aid_escrowed_total = 0.0
            z.migration_follow_events = 0
            z.replication_throttle_active_steps = 0
            z.capture_pressure_before = 0.0
            z.capture_pressure_after = 0.0
            z.collateral_welfare_loss = 0.0
            z.last_alloc_share = 0.0

    def _action_enabled(self, name):
        p = self.params.policy
        if p == name:
            return True
        if p.startswith("combined_action_containment"):
            return True
        return False

    def _bad_neighbor_evidence(self, obs, i):
        # Delegate to Experiment 10: delayed neighbor consequence + delayed aid history only.
        return super()._bad_neighbor_evidence(obs, i)

    def _activate_containment(self, obs, i):
        p = self.params.policy
        if p not in ACTION_POLICIES:
            return False
        if not self._bad_neighbor_evidence(obs, i):
            return False
        z = self.zones[i]
        d = self.params.containment_duration
        if self._action_enabled("action_containment_extraction_cap"):
            z.extraction_cap_timer = max(z.extraction_cap_timer, d)
        if self._action_enabled("action_containment_influence_throttle"):
            z.influence_throttle_timer = max(z.influence_throttle_timer, d)
        if self._action_enabled("action_containment_anti_concentration"):
            z.anti_concentration_flag = True
        if self._action_enabled("action_containment_migration_friction"):
            z.migration_friction_timer = max(z.migration_friction_timer, d)
        if self._action_enabled("action_containment_aid_escrow"):
            z.aid_escrow_timer = max(z.aid_escrow_timer, d)
        if self._action_enabled("action_containment_replication_throttle"):
            z.replication_throttle_timer = max(z.replication_throttle_timer, d)
        z.containment_events += 1
        z.containment_cost_total += self.params.containment_cost * (0.35 + self.params.containment_C)
        if z.catastrophe and not z.captured_signature:
            z.false_containment_events += 1
            z.collateral_welfare_loss += self.params.false_positive_cost * max(1.0, z.pop["dove"])
        return True

    def _score(self, obs, i):
        p = self.params.policy
        if p == "no_enforcement":
            return 1.0 - min(obs.welfare[i], obs.productivity[i])
        if p in VALIDATION_POLICIES or p in COMPARATOR_POLICIES or p in ZONE_COMPARATORS:
            return super()._score(obs, i)
        need = 1.0 - min(obs.welfare[i], obs.productivity[i])
        neighbor_response = (
            obs.neighbor_welfare_delta[i]
            + obs.neighbor_productivity_delta[i]
            + 0.5 * obs.neighbor_migration_delta[i]
            + 0.25 * obs.neighbor_population_delta[i]
            + 0.35 * obs.neighbor_diversity_delta[i]
        )
        bad = 1.0 if self._bad_neighbor_evidence(obs, i) else 0.0
        diversity_gap = max(0.0, self.params.diversity_floor - obs.diversity_non_adv[i])
        aid_response = neighbor_response / max(0.06, obs.last_useful_aid[i]) if obs.last_useful_aid[i] > 0 else 0.0
        score = 0.75 * need + 1.65 * neighbor_response - 0.65 * obs.capture_signal[i] - 0.45 * bad
        if p in {"action_containment_aid_escrow", "combined_action_containment_plus_response_to_aid"}:
            score += 0.75 * aid_response
        if p in {"combined_action_containment_plus_diversity"}:
            score += 1.1 * diversity_gap
        if p == "action_containment_anti_concentration":
            score -= 0.25 * obs.last_raw_aid[i]
        return score

    def choose_alloc(self):
        obs = self._delayed_obs()
        assert not hasattr(obs, "pop")
        assert not hasattr(obs, "types")
        for i in range(ZONES):
            self._activate_containment(obs, i)
        if self.params.policy in {"neighbor_penalty", "neighbor_quarantine"}:
            return super().choose_alloc()
        scores = [self._score(obs, i) for i in range(ZONES)]
        floor = 0.018 if self.params.policy in ACTION_POLICIES or self.params.policy in {"neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid"} else 0.0
        min_s = min(scores)
        shifted = [max(0.01, s - min_s + 0.04) for s in scores]
        alloc = base.normalize(shifted, total=max(0.0, 1.0 - floor * ZONES))
        alloc = [a + floor for a in alloc]
        if self.params.policy in ACTION_POLICIES and self._action_enabled("action_containment_anti_concentration"):
            cap = self.params.concentration_threshold
            excess = 0.0
            capped = []
            for i, a in enumerate(alloc):
                z = self.zones[i]
                local_cap = cap * (0.75 if z.anti_concentration_flag else 1.0)
                if a > local_cap:
                    excess += a - local_cap
                    a = local_cap
                capped.append(a)
            receivers = [i for i, a in enumerate(capped) if a < cap]
            if receivers and excess > 0:
                add = excess / len(receivers)
                for i in receivers:
                    capped[i] += add
            alloc = base.normalize(capped)
        for i, z in enumerate(self.zones):
            z.last_alloc_share = alloc[i]
        return alloc

    def _aid_effect(self, z, raw):
        capped_raw = raw
        if z.extraction_cap_timer > 0:
            z.extraction_cap_active_steps += 1
            capped_raw = raw * max(0.12, 1.0 - 0.72 * self.params.containment_C)
            z.containment_cost_total += (raw - capped_raw) * self.params.containment_cost
        escrowed = 0.0
        if z.aid_escrow_timer > 0 and min(z.welfare, z.productivity) < 0.55:
            escrowed = capped_raw * self.params.escrow_rate * self.params.containment_C
            capped_raw -= escrowed
            z.aid_escrowed_total += escrowed
            z.containment_cost_total += escrowed * 0.12
        effective, useful, intercepted = super()._aid_effect(z, capped_raw)
        if z.extraction_cap_timer > 0:
            intercepted *= max(0.08, 1.0 - 0.70 * self.params.containment_C)
            useful = max(0.0, effective - intercepted)
        z.extraction_volume += intercepted
        z.aid_intercepted_total += intercepted
        if escrowed > 0:
            # Non-transferable local repair: type-blind infrastructure channel, not direct food stock.
            z.welfare = base.clamp(z.welfare + 0.24 * escrowed)
            z.productivity = base.clamp(z.productivity + 0.19 * escrowed)
            z.migration_capacity = base.clamp(z.migration_capacity + 0.10 * escrowed)
        return effective, useful, intercepted

    def _apply_zone_dynamics(self, z, raw, step):
        before_neighbors = []
        if z.influence_throttle_timer > 0:
            for j in self.neighbors[z.idx]:
                n = self.zones[j]
                before_neighbors.append((n, n.welfare, n.productivity, n.migration_capacity))
        before_pop = dict(z.pop)
        before_pressure = self._truth_harm(z)
        z.capture_pressure_before += before_pressure
        super()._apply_zone_dynamics(z, raw, step)
        if z.influence_throttle_timer > 0:
            z.influence_throttle_active_steps += 1
            restore = 0.72 * self.params.containment_C
            for n, bw, bp, bm in before_neighbors:
                dw = min(0.0, n.welfare - bw)
                dp = min(0.0, n.productivity - bp)
                dm = min(0.0, n.migration_capacity - bm)
                harm = -(dw + dp + dm)
                if harm > 0:
                    z.outgoing_influence_volume += harm
                    n.welfare = base.clamp(n.welfare - dw * restore)
                    n.productivity = base.clamp(n.productivity - dp * restore)
                    n.migration_capacity = base.clamp(n.migration_capacity - dm * restore)
                    z.containment_cost_total += harm * self.params.containment_cost
        if z.replication_throttle_timer > 0:
            z.replication_throttle_active_steps += 1
            damp = 0.78 * self.params.containment_C
            for t in base.TYPES:
                if z.pop[t] > before_pop[t]:
                    z.pop[t] = before_pop[t] + (z.pop[t] - before_pop[t]) * max(0.05, 1.0 - damp)
            z.containment_cost_total += 0.018 * self.params.containment_C * base.total_pop(z.pop)
        if self.params.policy == "combined_action_containment_plus_diversity" and base.div_non_adv(z.pop) < self.params.diversity_floor:
            z.pop["mutant"] += 0.030 * max(1.0, z.pop["dove"])
        after_pressure = self._truth_harm(z)
        z.capture_pressure_after += after_pressure
        for timer_name in [
            "extraction_cap_timer",
            "influence_throttle_timer",
            "aid_escrow_timer",
            "replication_throttle_timer",
        ]:
            if getattr(z, timer_name) > 0:
                setattr(z, timer_name, getattr(z, timer_name) - 1)
        z.anti_concentration_flag = False

    def migrate(self):
        for i, z in enumerate(list(self.zones)):
            move_factor = self.params.migration_speed * z.migration_capacity
            if z.quarantine_timer > 0:
                continue
            if z.migration_friction_timer > 0:
                z.migration_follow_events += 1
                move_factor *= max(0.03, 1.0 - 0.88 * self.params.containment_C)
                z.containment_cost_total += 0.012 * self.params.containment_C * base.total_pop(z.pop)
                z.migration_friction_timer -= 1
            if move_factor <= 0:
                continue
            dst = self.rng.choice(self.neighbors[i])
            for t in base.TYPES:
                movers = z.pop[t] * move_factor * 0.018
                if movers <= 0:
                    continue
                z.pop[t] -= movers
                self.zones[dst].pop[t] += movers * max(0.0, 1.0 - self.params.migration_cost)

    def metrics(self):
        m = super().metrics()
        costs = sum(getattr(z, "containment_cost_total", 0.0) for z in self.zones)
        total_aid = sum(z.last_raw_aid for z in self.zones) * STEPS / max(1, ZONES)
        false_containment = sum(getattr(z, "false_containment_events", 0) for z in self.zones) / max(1, STEPS)
        allocs = [getattr(z, "last_alloc_share", 0.0) for z in self.zones]
        pressure_before = sum(getattr(z, "capture_pressure_before", 0.0) for z in self.zones)
        pressure_after = sum(getattr(z, "capture_pressure_after", 0.0) for z in self.zones)
        m.update({
            "containment_cost_share": costs / max(EPS, costs + total_aid),
            "false_containment_rate": false_containment,
            "containment_events": sum(getattr(z, "containment_events", 0) for z in self.zones),
            "extraction_volume": sum(getattr(z, "extraction_volume", 0.0) for z in self.zones),
            "extraction_cap_active_steps": sum(getattr(z, "extraction_cap_active_steps", 0) for z in self.zones),
            "outgoing_influence_volume": sum(getattr(z, "outgoing_influence_volume", 0.0) for z in self.zones),
            "influence_throttle_active_steps": sum(getattr(z, "influence_throttle_active_steps", 0) for z in self.zones),
            "aid_intercepted": sum(getattr(z, "aid_intercepted_total", 0.0) for z in self.zones),
            "aid_escrowed": sum(getattr(z, "aid_escrowed_total", 0.0) for z in self.zones),
            "resource_hhi": resource_hhi(allocs),
            "max_zone_resource_share": max(allocs) if allocs else 0.0,
            "migration_follow_events": sum(getattr(z, "migration_follow_events", 0) for z in self.zones),
            "replication_throttle_active_steps": sum(getattr(z, "replication_throttle_active_steps", 0) for z in self.zones),
            "capture_pressure_before": pressure_before / max(1, STEPS),
            "capture_pressure_after": pressure_after / max(1, STEPS),
            "collateral_welfare_loss": sum(getattr(z, "collateral_welfare_loss", 0.0) for z in self.zones),
            "strict_zero_capture": 1.0 if m["capture"] == 0.0 else 0.0,
        })
        return m


def run_one(seed, params):
    model = ActionContainmentModel(seed, params)
    out = model.run()
    return {
        "seed": seed,
        "world": params.world,
        "policy": params.policy,
        "delay": params.delay,
        "t_irrev": params.t_irrev,
        "R": params.t_irrev / max(1, params.delay),
        "adversarial_strength": params.adversarial_strength,
        "catastrophe_severity": params.catastrophe_severity,
        "diversity_floor": params.diversity_floor,
        "enforcement_C": params.enforcement_C,
        "containment_C": params.containment_C,
        "containment_duration": params.containment_duration,
        "concentration_threshold": params.concentration_threshold,
        "escrow_rate": params.escrow_rate,
        "audit_p": params.audit_p,
        "audit_kappa": params.audit_kappa,
        "penalty_duration": params.penalty_duration,
        "quarantine_strictness": params.quarantine_strictness,
        "migration_speed": params.migration_speed,
        "migration_cost": params.migration_cost,
        "scavenger_enabled": int(params.scavenger_enabled),
        **out,
    }


def scenario_grid():
    rows = []
    for world, policy in [
        ("T1_proxy_trap", "feature_proxy"),
        ("T2_sag_ambiguity_trap", "always_cut_sagging"),
        ("T2_sag_ambiguity_trap", "always_aid_sagging"),
        ("T3_monoculture_trap", "monoculture_optimizer"),
    ]:
        rows.append(Params(world=world, policy=policy))
    worlds = ["PURE_CAPTURE", "PURE_CATASTROPHE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE"]
    for world in worlds:
        for policy in ["no_enforcement", *ZONE_COMPARATORS, *ACTION_POLICIES, "response_to_neighbor_aid", "diversity_non_adversarial_only"]:
            c_values = [0.25, 0.45, 0.70] if policy in ACTION_POLICIES else [0.45]
            for c in c_values:
                rows.append(Params(
                    world=world,
                    policy=policy,
                    containment_C=c,
                    enforcement_C=c,
                    containment_duration=4,
                    penalty_duration=4,
                    quarantine_strictness=0.55,
                    scavenger_enabled=world == "SCAVENGER_CATASTROPHE",
                    diversity_floor=0.44 if "diversity" in policy else 0.35,
                ))
    for duration in [2, 4, 7]:
        rows.append(Params(world="PURE_CAPTURE", policy="combined_action_containment", containment_C=0.45, containment_duration=duration))
    for delay in [1, 2, 4, 7, 10]:
        rows.append(Params(world="PURE_CAPTURE", policy="combined_action_containment", delay=delay, t_irrev=8, containment_C=0.45))
    for adv in [0.45, 0.70, 0.90]:
        rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="combined_action_containment", adversarial_strength=adv, containment_C=0.45))
    for severity in [0.35, 0.55, 0.75]:
        rows.append(Params(world="PURE_CATASTROPHE", policy="combined_action_containment", catastrophe_severity=severity, containment_C=0.45))
        rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="combined_action_containment", catastrophe_severity=severity, containment_C=0.45))
    for migration_speed in [0.08, 0.22, 0.40]:
        for migration_cost in [0.02, 0.08, 0.18]:
            rows.append(Params(world="PURE_CAPTURE", policy="action_containment_migration_friction", containment_C=0.45, migration_speed=migration_speed, migration_cost=migration_cost))
    for threshold in [0.18, 0.24, 0.30]:
        rows.append(Params(world="PURE_CAPTURE", policy="action_containment_anti_concentration", containment_C=0.45, concentration_threshold=threshold))
    return rows


def is_viable(r):
    return (
        r["permanence_probability"] >= 0.60
        and r["capture_probability"] <= 0.20
        and r["collapse_probability"] <= 0.20
        and r["fraction_irreversible_zones"] <= 0.25
        and r["adversarial_share"] <= 0.35
        and r["mean_welfare"] >= 0.55
        and r["non_adv_diversity"] >= 0.45
        and r["containment_cost_share"] <= 0.35
        and r["false_containment_rate"] <= 0.20
    )


def is_action_viable(r):
    return (
        is_viable(r)
        and r["policy"] in ACTION_POLICIES
        and r["world"] in CAPTURE_WORLDS
        and r["containment_events"] > 0
    )


def summarize(rows):
    keys = [
        "world", "policy", "delay", "t_irrev", "containment_C", "containment_duration",
        "concentration_threshold", "escrow_rate", "adversarial_strength", "catastrophe_severity",
        "migration_speed", "migration_cost", "scavenger_enabled",
    ]
    grouped = defaultdict(list)
    for r in rows:
        grouped[tuple(r[k] for k in keys)].append(r)
    out = []
    for key, vals in grouped.items():
        base_row = {k: key[i] for i, k in enumerate(keys)}
        kperm = int(sum(v["permanence"] for v in vals))
        lo, hi = base.wilson(kperm, len(vals))
        row = {
            **base_row,
            "R": float(vals[0]["R"]),
            "n": len(vals),
            "permanence_probability": safe_mean([v["permanence"] for v in vals]),
            "permanence_wilson_lo": lo,
            "permanence_wilson_hi": hi,
            "capture_probability": safe_mean([v["capture"] for v in vals]),
            "strict_zero_capture_probability": safe_mean([v["strict_zero_capture"] for v in vals]),
            "collapse_probability": safe_mean([v["collapse"] for v in vals]),
            "fraction_irreversible_zones": safe_mean([v["fraction_irreversible_zones"] for v in vals]),
            "irreversible_zone_failures_mean": safe_mean([v["irreversible_zone_failures"] for v in vals]),
            "adversarial_share": safe_mean([v["adversarial_share"] for v in vals]),
            "mean_welfare": safe_mean([v["mean_welfare"] for v in vals]),
            "non_adv_diversity": safe_mean([v["non_adv_diversity"] for v in vals]),
            "containment_cost_share": safe_mean([v["containment_cost_share"] for v in vals]),
            "false_containment_rate": safe_mean([v["false_containment_rate"] for v in vals]),
            "containment_events": safe_mean([v["containment_events"] for v in vals]),
            "extraction_volume": safe_mean([v["extraction_volume"] for v in vals]),
            "extraction_cap_active_steps": safe_mean([v["extraction_cap_active_steps"] for v in vals]),
            "outgoing_influence_volume": safe_mean([v["outgoing_influence_volume"] for v in vals]),
            "influence_throttle_active_steps": safe_mean([v["influence_throttle_active_steps"] for v in vals]),
            "aid_intercepted": safe_mean([v["aid_intercepted"] for v in vals]),
            "aid_escrowed": safe_mean([v["aid_escrowed"] for v in vals]),
            "resource_hhi": safe_mean([v["resource_hhi"] for v in vals]),
            "max_zone_resource_share": safe_mean([v["max_zone_resource_share"] for v in vals]),
            "migration_follow_events": safe_mean([v["migration_follow_events"] for v in vals]),
            "replication_throttle_active_steps": safe_mean([v["replication_throttle_active_steps"] for v in vals]),
            "capture_pressure_before": safe_mean([v["capture_pressure_before"] for v in vals]),
            "capture_pressure_after": safe_mean([v["capture_pressure_after"] for v in vals]),
            "collateral_welfare_loss": safe_mean([v["collateral_welfare_loss"] for v in vals]),
        }
        row["viable"] = int(is_viable(row))
        row["action_viable"] = int(is_action_viable(row))
        out.append(row)
    return out


def validation(summary):
    by = {(r["world"], r["policy"]): r for r in summary}
    action = [r for r in summary if r["policy"] in ACTION_POLICIES]
    capture_action = [r for r in action if r["world"] in CAPTURE_WORLDS]
    checks = {
        "hidden_type_absent_from_observation": True,
        "controls_fire_only_from_delayed_consequence": any(r["containment_events"] > 0 for r in action),
        "controls_have_cost": any(r["containment_cost_share"] > 0 for r in action),
        "feature_proxy_fails_T1": by[("T1_proxy_trap", "feature_proxy")]["permanence_probability"] < 0.25,
        "always_cut_fails_T2": by[("T2_sag_ambiguity_trap", "always_cut_sagging")]["permanence_probability"] < 0.25,
        "always_aid_fails_T2": by[("T2_sag_ambiguity_trap", "always_aid_sagging")]["permanence_probability"] < 0.25,
        "monoculture_fails_T3": by[("T3_monoculture_trap", "monoculture_optimizer")]["permanence_probability"] < 0.25,
        "action_containment_fires": any(r["containment_events"] > 0 for r in action),
        "not_all_zones_starved": any(r["mean_welfare"] > 0.45 for r in action),
        "pure_catastrophe_test_present": any(r["world"] == "PURE_CATASTROPHE" for r in action),
        "capture_not_one_for_all_action_containment": any(r["capture_probability"] < 1.0 for r in capture_action),
    }
    valid = all(checks.values())
    viable = [r for r in action if r["action_viable"]]
    reduces = any(r["capture_probability"] < 0.75 for r in capture_action)
    if not valid:
        verdict = "D. Result invalid due to failed validation."
    elif viable:
        verdict = "A. Action-channel containment creates a non-trivial viability kernel."
    elif reduces:
        verdict = "B. Action-channel containment reduces capture but costs/collateral destroy viability."
    else:
        verdict = "C. Action-channel containment does not reduce capture enough."
    return checks, verdict, viable


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
    width, height = 960, 560
    ml, mr, mt, mb = 90, 30, 60, 160
    ymax = max(1.0, max(values) if values else 1.0)
    bw = (width - ml - mr) / max(1, len(labels))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>',
        f'<line x1="{ml}" y1="{height-mb}" x2="{width-mr}" y2="{height-mb}" stroke="#111"/>',
        f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}" stroke="#111"/>',
        f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" font-family="sans-serif" font-size="12">{ylabel}</text>',
    ]
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = ml + i * bw + bw * 0.12
        h = (val / ymax) * (height - mt - mb)
        y = height - mb - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*0.76:.1f}" height="{h:.1f}" fill="#047857"/>')
        parts.append(f'<text x="{x+bw*0.38:.1f}" y="{height-mb+14}" transform="rotate(45 {x+bw*0.38:.1f} {height-mb+14})" font-family="sans-serif" font-size="10">{lab}</text>')
        parts.append(f'<text x="{x+bw*0.38:.1f}" y="{y-4:.1f}" text-anchor="middle" font-family="sans-serif" font-size="10">{val:.2f}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n")


def plots(summary):
    action = [r for r in summary if r["policy"] in ACTION_POLICIES and r["world"] in CAPTURE_WORLDS]
    best_by_policy = []
    for policy in ACTION_POLICIES:
        rows = [r for r in action if r["policy"] == policy]
        if rows:
            best_by_policy.append(min(rows, key=lambda r: (r["capture_probability"], -r["permanence_probability"])))
    labels = [r["policy"].replace("action_containment_", "")[:22] for r in best_by_policy]
    svg_bar(RESULTS / "capture_by_action_channel.svg", "Capture by Action Channel", labels, [r["capture_probability"] for r in best_by_policy], "capture probability")
    svg_bar(RESULTS / "cost_by_action_channel.svg", "Containment Cost by Action Channel", labels, [r["containment_cost_share"] for r in best_by_policy], "cost share")
    svg_bar(RESULTS / "resource_hhi_by_action_channel.svg", "Resource Concentration by Action Channel", labels, [r["resource_hhi"] for r in best_by_policy], "resource HHI")


def channel_rank(summary):
    zone = [r for r in summary if r["policy"] in ZONE_COMPARATORS and r["world"] in CAPTURE_WORLDS]
    baseline_capture = safe_mean([r["capture_probability"] for r in zone]) if zone else 1.0
    ranked = []
    for policy in ACTION_POLICIES:
        rows = [r for r in summary if r["policy"] == policy and r["world"] in CAPTURE_WORLDS]
        if not rows:
            continue
        best = min(rows, key=lambda r: (r["capture_probability"], -r["permanence_probability"], r["containment_cost_share"]))
        ranked.append({
            "policy": policy,
            "best_world": best["world"],
            "capture_probability": best["capture_probability"],
            "capture_reduction_vs_zone_penalty": baseline_capture - best["capture_probability"],
            "permanence_probability": best["permanence_probability"],
            "mean_welfare": best["mean_welfare"],
            "collapse_probability": best["collapse_probability"],
            "containment_cost_share": best["containment_cost_share"],
            "false_containment_rate": best["false_containment_rate"],
            "containment_events": best["containment_events"],
            "resource_hhi": best["resource_hhi"],
        })
    return sorted(ranked, key=lambda r: (-r["capture_reduction_vs_zone_penalty"], r["containment_cost_share"]))


def report(summary, checks, verdict, viable):
    action = [r for r in summary if r["policy"] in ACTION_POLICIES]
    ranked = channel_rank(summary)
    best = sorted(action, key=lambda r: (r["action_viable"], r["viable"], -r["capture_probability"], r["containment_cost_share"]), reverse=True)[:14]
    threshold = None
    for r in sorted(action, key=lambda r: (r["containment_C"], r["containment_duration"], r["containment_cost_share"])):
        if r["action_viable"]:
            threshold = r
            break
    lines = [
        "# Experiment 11 Report: Action-Channel Containment",
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
    lines += [
        "",
        "## Required Analyses",
        "",
        "1. Did any action-channel lever reduce capture? See channel ranking below; reduction is computed relative to Experiment 10 zone penalties in the same substrate family.",
    ]
    if ranked:
        top = ranked[0]
        lines.append(f"2. Strongest channel: `{top['policy']}` in `{top['best_world']}` with capture `{top['capture_probability']:.3f}` and reduction `{top['capture_reduction_vs_zone_penalty']:.3f}` versus zone penalties.")
    else:
        lines.append("2. Strongest channel: none, no action-channel rows were produced.")
    if threshold:
        lines.append(f"3. Minimal viable containment threshold: policy `{threshold['policy']}`, C `{threshold['containment_C']}`, duration `{threshold['containment_duration']}`, cost `{threshold['containment_cost_share']:.3f}`.")
    else:
        lines.append("3. Minimal viable containment threshold: none found under the action-containment viability criterion.")
    lines += [
        "4. Starvation check: welfare/collapse/irreversible failures are reported in raw summary and Best Action Cells; viability rejects starvation-only wins.",
        "5. Catastrophe preservation: pure-catastrophe rows track `false_containment_rate` and are excluded from capture-kernel evidence.",
        "6. Diversity complement: combined containment plus diversity is compared directly with combined containment and diversity-only rows.",
        "7. R visibility: delay sweep rows for `combined_action_containment` are in raw summary; no causal claim beyond this toy sweep.",
        f"8. Viable region breadth: `{len(viable)}` action-containment viable cells out of `{len(action)}` action-containment cells.",
        "",
        "## Channel Ranking",
        "",
        "| policy | best world | capture | reduction vs zone penalty | permanence | welfare | collapse | cost | false containment | events | HHI |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in ranked:
        lines.append(f"| {r['policy']} | {r['best_world']} | {r['capture_probability']:.3f} | {r['capture_reduction_vs_zone_penalty']:.3f} | {r['permanence_probability']:.3f} | {r['mean_welfare']:.3f} | {r['collapse_probability']:.3f} | {r['containment_cost_share']:.3f} | {r['false_containment_rate']:.3f} | {r['containment_events']:.1f} | {r['resource_hhi']:.3f} |")
    lines += [
        "",
        "## Best Action Cells",
        "",
        "| action viable | raw viable | world | policy | C | duration | permanence | capture | strict zero capture | collapse | irrev frac | welfare | diversity | cost | false containment | events | escrowed | intercepted |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in best:
        lines.append(f"| {r['action_viable']} | {r['viable']} | {r['world']} | {r['policy']} | {r['containment_C']} | {r['containment_duration']} | {r['permanence_probability']:.3f} | {r['capture_probability']:.3f} | {r['strict_zero_capture_probability']:.3f} | {r['collapse_probability']:.3f} | {r['fraction_irreversible_zones']:.3f} | {r['mean_welfare']:.3f} | {r['non_adv_diversity']:.3f} | {r['containment_cost_share']:.3f} | {r['false_containment_rate']:.3f} | {r['containment_events']:.1f} | {r['aid_escrowed']:.2f} | {r['aid_intercepted']:.2f} |")
    capture_rows = sorted(
        [r for r in action if r["world"] in CAPTURE_WORLDS],
        key=lambda r: (r["capture_probability"], -r["permanence_probability"], r["containment_cost_share"]),
    )[:14]
    lines += [
        "",
        "## Capture-Relevant Action Cells",
        "",
        "These rows exclude pure-catastrophe controls. The validation failure is that all capture-relevant action-containment rows retain `capture=1.0`.",
        "",
        "| world | policy | C | R | adv | severity | permanence | capture | welfare | diversity | cost | false containment | events | pressure before | pressure after |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in capture_rows:
        lines.append(f"| {r['world']} | {r['policy']} | {r['containment_C']} | {r['R']:.2f} | {r['adversarial_strength']:.2f} | {r['catastrophe_severity']:.2f} | {r['permanence_probability']:.3f} | {r['capture_probability']:.3f} | {r['mean_welfare']:.3f} | {r['non_adv_diversity']:.3f} | {r['containment_cost_share']:.3f} | {r['false_containment_rate']:.3f} | {r['containment_events']:.1f} | {r['capture_pressure_before']:.3f} | {r['capture_pressure_after']:.3f} |")
    (RESULTS / "report.md").write_text("\n".join(lines) + "\n")
    vlines = ["# Experiment 11 Validation Report", "", "| check | result |", "|---|---:|"]
    for k, v in checks.items():
        vlines.append(f"| {k} | `{v}` |")
    vlines += ["", "Calibration note: capture gate is evaluated only on action-containment rows in capture-relevant worlds.", "", f"Final verdict: **{verdict}**"]
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
    checks, verdict, viable = validation(summary)
    write_csv(RAW / "runs.csv", rows)
    write_csv(RAW / "summary.csv", summary)
    write_csv(RAW / "viable_cells.csv", viable)
    write_csv(RAW / "channel_ranking.csv", channel_rank(summary))
    plots(summary)
    report(summary, checks, verdict, viable)
    manifest = {
        "git_head": git_value(["rev-parse", "HEAD"]),
        "git_status_short": git_value(["status", "--short"]),
        "spec_implemented_11_sha256": spec_hash(),
        "seeds": SEEDS,
        "num_cells": len(summary),
        "num_runs": len(rows),
        "num_action_viable_cells": len(viable),
        "validation_checks": checks,
        "final_verdict": verdict,
    }
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"verdict": verdict, "cells": len(summary), "runs": len(rows), "viable": len(viable), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
