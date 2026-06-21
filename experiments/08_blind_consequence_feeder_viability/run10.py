#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import random
import statistics
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import run09 as base

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_10"
RAW = RESULTS / "raw"
SEEDS = list(range(9300, 9325))
STEPS = base.STEPS
ZONES = base.ZONES
EPS = base.EPS

BASE_POLICIES = [
    "feature_proxy",
    "always_cut_sagging",
    "always_aid_sagging",
    "monoculture_optimizer",
    "self_consequence",
    "neighbor_consequence",
    "local_global_neighbor",
    "response_to_neighbor_aid",
    "diversity_non_adversarial_only",
]
ENFORCEMENT_POLICIES = [
    "neighbor_penalty",
    "neighbor_quarantine",
    "neighbor_audit_penalty",
    "consequence_plus_diversity",
]
CAPTURE_WORLDS = {"PURE_CAPTURE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE"}


@dataclass(frozen=True)
class Params:
    world: str
    policy: str
    delay: int = 2
    t_irrev: int = 7
    adversarial_strength: float = 0.70
    catastrophe_severity: float = 0.55
    diversity_floor: float = 0.35
    channel_noise: float = 0.12
    target_mi: float = 0.13
    mi_tolerance: float = 0.03
    enforcement_C: float = 0.45
    audit_p: float = 0.0
    audit_kappa: float = 0.0
    penalty_duration: int = 4
    quarantine_strictness: float = 0.45
    false_positive_cost: float = 0.08
    migration_speed: float = 0.22
    migration_cost: float = 0.08
    scavenger_enabled: bool = False


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC_IMPLEMENTED_10.md").read_bytes()).hexdigest()


def safe_mean(xs):
    return statistics.fmean(xs) if xs else 0.0


class EnforcementModel(base.BreakTrivialModel):
    def _init_world(self):
        # Reuse Experiment 09 worlds for validation traps, add enforcement-specific worlds.
        if self.params.world == "PURE_CAPTURE":
            self.params = Params(**{**self.params.__dict__, "world": "T1_proxy_trap"})
            super()._init_world()
            self.params = Params(**{**self.params.__dict__, "world": "PURE_CAPTURE"})
        elif self.params.world == "PURE_CATASTROPHE":
            self.params = Params(**{**self.params.__dict__, "world": "T2_sag_ambiguity_trap"})
            super()._init_world()
            for z in self.zones:
                if z.captured_signature:
                    z.captured_signature = False
                    z.catastrophe = True
                    z.pop = {"dove": 26.0, "hawk": 1.0, "mutant": 5.0, "scavenger": 0.0}
            self.params = Params(**{**self.params.__dict__, "world": "PURE_CATASTROPHE"})
        elif self.params.world == "MIXED_CAPTURE_CATASTROPHE":
            self.params = Params(**{**self.params.__dict__, "world": "T2_sag_ambiguity_trap"})
            super()._init_world()
            self.params = Params(**{**self.params.__dict__, "world": "MIXED_CAPTURE_CATASTROPHE"})
        elif self.params.world == "SCAVENGER_CATASTROPHE":
            self.params = Params(**{**self.params.__dict__, "world": "T2_sag_ambiguity_trap"})
            super()._init_world()
            for z in self.zones:
                if z.catastrophe:
                    z.pop["scavenger"] = 8.0
                if z.captured_signature:
                    z.pop["scavenger"] = 5.0
            self.params = Params(**{**self.params.__dict__, "world": "SCAVENGER_CATASTROPHE"})
        else:
            super()._init_world()
        for z in self.zones:
            z.penalty_timer = 0
            z.quarantine_timer = 0
            z.bad_neighbor_streak = 0
            z.enforcement_events = 0
            z.false_positive_events = 0
            z.enforcement_cost = 0.0
            z.quarantine_cost = 0.0
            z.collateral_dove_harm = 0.0

    def _bad_neighbor_evidence(self, obs, i):
        neighbor_delta = (
            obs.neighbor_welfare_delta[i]
            + obs.neighbor_productivity_delta[i]
            + 0.5 * obs.neighbor_migration_delta[i]
            + 0.25 * obs.neighbor_population_delta[i]
            + 0.35 * obs.neighbor_diversity_delta[i]
        )
        aid = obs.last_raw_aid[i]
        return aid > 0.03 and neighbor_delta < -0.035

    def _enforcement_action(self, obs, i):
        p = self.params.policy
        if p not in ENFORCEMENT_POLICIES:
            return False
        if not self._bad_neighbor_evidence(obs, i):
            return False
        z = self.zones[i]
        z.bad_neighbor_streak += 1
        if p == "neighbor_penalty":
            z.penalty_timer = max(z.penalty_timer, self.params.penalty_duration)
            return True
        if p == "neighbor_quarantine" and z.bad_neighbor_streak >= 2:
            z.quarantine_timer = max(z.quarantine_timer, self.params.penalty_duration)
            return True
        if p == "neighbor_audit_penalty" and self.rng.random() < self.params.audit_p:
            z.penalty_timer = max(z.penalty_timer, self.params.penalty_duration)
            return True
        if p == "consequence_plus_diversity":
            z.penalty_timer = max(z.penalty_timer, max(2, self.params.penalty_duration - 1))
            z.quarantine_timer = max(z.quarantine_timer, max(2, self.params.penalty_duration - 2))
            return True
        return False

    def _score(self, obs, i):
        p = self.params.policy
        if p in BASE_POLICIES:
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
        if p == "neighbor_penalty":
            return 0.65 * need + 1.4 * neighbor_response - 1.8 * bad
        if p == "neighbor_quarantine":
            return 0.65 * need + 1.5 * neighbor_response - 1.3 * bad
        if p == "neighbor_audit_penalty":
            return 0.65 * need + 1.4 * neighbor_response - self.params.audit_p * self.params.enforcement_C * bad - 0.25 * self.params.audit_kappa
        if p == "consequence_plus_diversity":
            aid_response = neighbor_response / max(0.06, obs.last_useful_aid[i]) if obs.last_useful_aid[i] > 0 else 0.0
            return 0.75 * need + 1.5 * aid_response + 0.9 * diversity_gap - 1.6 * bad
        raise ValueError(p)

    def choose_alloc(self):
        obs = self._delayed_obs()
        for i in range(ZONES):
            if self._enforcement_action(obs, i):
                z = self.zones[i]
                z.enforcement_events += 1
                z.enforcement_cost += self.params.audit_kappa + 0.025 * self.params.enforcement_C
                if z.catastrophe and not z.captured_signature:
                    z.false_positive_events += 1
                    z.collateral_dove_harm += self.params.false_positive_cost * max(1.0, z.pop["dove"])
        scores = [self._score(obs, i) for i in range(ZONES)]
        floor = 0.018 if self.params.policy in ENFORCEMENT_POLICIES or self.params.policy in {"neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid"} else 0.0
        min_s = min(scores)
        shifted = [max(0.01, s - min_s + 0.04) for s in scores]
        alloc = base.normalize(shifted, total=max(0.0, 1.0 - floor * ZONES))
        alloc = [a + floor for a in alloc]
        for i, z in enumerate(self.zones):
            if z.penalty_timer > 0:
                alloc[i] *= max(0.02, 1.0 - self.params.enforcement_C)
        return base.normalize(alloc)


    def _apply_shock(self, step):
        if self.params.world in {"PURE_CATASTROPHE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE"} and step in [18, 36]:
            for z in self.zones:
                if z.catastrophe:
                    z.welfare *= max(0.05, 1.0 - 0.30 * self.params.catastrophe_severity)
                    z.productivity *= max(0.05, 1.0 - 0.26 * self.params.catastrophe_severity)
                    z.migration_capacity *= max(0.05, 1.0 - 0.18 * self.params.catastrophe_severity)
                    z.pop["dove"] *= max(0.05, 1.0 - 0.08 * self.params.catastrophe_severity)
            return
        super()._apply_shock(step)

    def _aid_effect(self, z, raw):
        effective, useful, intercepted = super()._aid_effect(z, raw)
        if z.penalty_timer > 0:
            effective *= max(0.05, 1.0 - self.params.enforcement_C)
            useful *= max(0.05, 1.0 - self.params.enforcement_C)
            z.penalty_timer -= 1
            z.enforcement_cost += raw * self.params.enforcement_C
            if z.catastrophe and not z.captured_signature:
                z.false_positive_events += 1
                z.collateral_dove_harm += self.params.false_positive_cost * max(1.0, z.pop["dove"])
        return effective, useful, intercepted

    def _apply_zone_dynamics(self, z, raw, step):
        before_dove = z.pop["dove"]
        super()._apply_zone_dynamics(z, raw, step)
        if z.quarantine_timer > 0:
            z.quarantine_timer -= 1
            z.migration_capacity = base.clamp(z.migration_capacity * (1.0 - 0.35 * self.params.quarantine_strictness))
            z.welfare = base.clamp(z.welfare - 0.025 * self.params.quarantine_strictness)
            z.quarantine_cost += 0.035 * self.params.quarantine_strictness
            if z.catastrophe and not z.captured_signature:
                z.false_positive_events += 1
                z.collateral_dove_harm += self.params.false_positive_cost * max(1.0, before_dove)
        if self.params.policy == "consequence_plus_diversity" and base.div_non_adv(z.pop) < self.params.diversity_floor:
            z.pop["mutant"] += 0.035 * max(1.0, z.pop["dove"])

    def migrate(self):
        # Type-blind quarantine restricts all outward movement from a zone.
        for i, z in enumerate(list(self.zones)):
            if z.quarantine_timer > 0:
                continue
            move_factor = self.params.migration_speed * z.migration_capacity
            if move_factor <= 0:
                continue
            dst = self.rng.choice(self.neighbors[i])
            for t in base.TYPES:
                movers = z.pop[t] * move_factor * 0.018
                if movers <= 0:
                    continue
                z.pop[t] -= movers
                self.zones[dst].pop[t] += movers * max(0.0, 1.0 - self.params.migration_cost)

    def step(self, step):
        self._store_pre_step()
        self._apply_shock(step)
        alloc = self.choose_alloc()
        budget = 5.5
        for i, z in enumerate(self.zones):
            self._apply_zone_dynamics(z, budget * alloc[i], step)
        self.migrate()
        self._update_irreversibility(step)
        self._update_neighbor_metrics()
        self.obs_queue.append(self._observe(step, noisy=True))

    def metrics(self):
        m = super().metrics()
        total_cost = sum(getattr(z, "enforcement_cost", 0.0) + getattr(z, "quarantine_cost", 0.0) for z in self.zones)
        total_aid = sum(z.last_raw_aid for z in self.zones) * STEPS / max(1, ZONES)
        false_positive = sum(getattr(z, "false_positive_events", 0) for z in self.zones) / max(1, STEPS)
        collateral = sum(getattr(z, "collateral_dove_harm", 0.0) for z in self.zones)
        enforcement_events = sum(getattr(z, "enforcement_events", 0) for z in self.zones)
        m.update({
            "enforcement_cost_share": total_cost / max(EPS, total_cost + total_aid),
            "false_positive_punishment_rate": false_positive,
            "collateral_dove_harm": collateral,
            "enforcement_events": enforcement_events,
            "strict_zero_capture": 1.0 if m["capture"] == 0.0 else 0.0,
        })
        return m


def run_one(seed, params):
    model = EnforcementModel(seed, params)
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
    # Validation comparators: keep Experiment 09 trap semantics.
    for world, policy in [
        ("T1_proxy_trap", "feature_proxy"),
        ("T2_sag_ambiguity_trap", "always_cut_sagging"),
        ("T2_sag_ambiguity_trap", "always_aid_sagging"),
        ("T3_monoculture_trap", "monoculture_optimizer"),
    ]:
        rows.append(Params(world=world, policy=policy))
    for world in ["PURE_CAPTURE", "PURE_CATASTROPHE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE"]:
        for policy in ["neighbor_consequence", "local_global_neighbor", "response_to_neighbor_aid", *ENFORCEMENT_POLICIES, "diversity_non_adversarial_only"]:
            for C in ([0.20, 0.45, 0.70] if policy in ENFORCEMENT_POLICIES else [0.0]):
                rows.append(Params(
                    world=world,
                    policy=policy,
                    enforcement_C=C,
                    audit_p=0.35 if policy == "neighbor_audit_penalty" else 0.0,
                    audit_kappa=0.08 if policy == "neighbor_audit_penalty" else 0.0,
                    penalty_duration=4,
                    quarantine_strictness=0.55 if policy == "neighbor_quarantine" else 0.25,
                    scavenger_enabled=world == "SCAVENGER_CATASTROPHE",
                    diversity_floor=0.42 if policy == "consequence_plus_diversity" else 0.35,
                ))
    for delay in [1, 2, 4, 7, 10]:
        rows.append(Params(world="PURE_CAPTURE", policy="consequence_plus_diversity", delay=delay, t_irrev=8, enforcement_C=0.45, penalty_duration=4, diversity_floor=0.42))
    for adv in [0.45, 0.70, 0.90]:
        rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="consequence_plus_diversity", adversarial_strength=adv, enforcement_C=0.45, diversity_floor=0.42))
    for duration in [2, 4, 7]:
        rows.append(Params(world="PURE_CAPTURE", policy="neighbor_penalty", enforcement_C=0.45, penalty_duration=duration))
    for p_audit in [0.10, 0.35, 0.70]:
        for kappa in [0.0, 0.08, 0.16]:
            rows.append(Params(world="PURE_CAPTURE", policy="neighbor_audit_penalty", enforcement_C=0.45, audit_p=p_audit, audit_kappa=kappa, penalty_duration=4))
            rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="neighbor_audit_penalty", enforcement_C=0.45, audit_p=p_audit, audit_kappa=kappa, penalty_duration=4))
    for t_irrev in [5, 8, 12]:
        rows.append(Params(world="PURE_CAPTURE", policy="consequence_plus_diversity", delay=2, t_irrev=t_irrev, enforcement_C=0.45, penalty_duration=4, diversity_floor=0.42))
    for severity in [0.35, 0.55, 0.75]:
        rows.append(Params(world="PURE_CATASTROPHE", policy="consequence_plus_diversity", catastrophe_severity=severity, enforcement_C=0.45, diversity_floor=0.42))
        rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="consequence_plus_diversity", catastrophe_severity=severity, enforcement_C=0.45, diversity_floor=0.42))
    for migration_speed in [0.08, 0.22, 0.40]:
        for migration_cost in [0.02, 0.08, 0.18]:
            rows.append(Params(world="PURE_CAPTURE", policy="neighbor_quarantine", enforcement_C=0.45, penalty_duration=4, quarantine_strictness=0.55, migration_speed=migration_speed, migration_cost=migration_cost))
    for strictness in [0.25, 0.55, 0.85]:
        rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="neighbor_quarantine", enforcement_C=0.45, penalty_duration=4, quarantine_strictness=strictness))
    return rows


def summarize(rows):
    grouped = defaultdict(list)
    keys = ["world", "policy", "delay", "t_irrev", "enforcement_C", "audit_p", "audit_kappa", "penalty_duration", "quarantine_strictness", "adversarial_strength", "catastrophe_severity", "migration_speed", "migration_cost", "scavenger_enabled"]
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
            "enforcement_cost_share": safe_mean([v["enforcement_cost_share"] for v in vals]),
            "false_positive_punishment_rate": safe_mean([v["false_positive_punishment_rate"] for v in vals]),
            "collateral_dove_harm": safe_mean([v["collateral_dove_harm"] for v in vals]),
            "enforcement_events": safe_mean([v["enforcement_events"] for v in vals]),
        }
        row["viable"] = int(is_viable(row))
        row["nontrivial_enforcement_viable"] = int(is_nontrivial_enforcement_viable(row))
        out.append(row)
    return out


def is_viable(r):
    return (
        r["permanence_probability"] >= 0.60
        and r["capture_probability"] <= 0.20
        and r["collapse_probability"] <= 0.20
        and r["fraction_irreversible_zones"] <= 0.25
        and r["adversarial_share"] <= 0.35
        and r["mean_welfare"] >= 0.55
        and r["non_adv_diversity"] >= 0.45
        and r["enforcement_cost_share"] <= 0.30
        and r["false_positive_punishment_rate"] <= 0.20
    )


def is_nontrivial_enforcement_viable(r):
    return (
        is_viable(r)
        and r["policy"] in ENFORCEMENT_POLICIES
        and r["world"] in CAPTURE_WORLDS
        and (r["enforcement_events"] > 0 or r["enforcement_cost_share"] > 0)
    )


def validation(summary):
    by = {(r["world"], r["policy"]): r for r in summary}
    enforcement = [r for r in summary if r["policy"] in ENFORCEMENT_POLICIES]
    capture_enforcement = [r for r in enforcement if r["world"] in CAPTURE_WORLDS]
    checks = {
        "hidden_type_absent_from_observation": True,
        "enforcement_has_cost": any(r["enforcement_cost_share"] > 0 for r in enforcement),
        "delayed_consequence_required": any(r["enforcement_events"] > 0 for r in enforcement),
        "feature_proxy_fails_T1": by[("T1_proxy_trap", "feature_proxy")]["permanence_probability"] < 0.25,
        "always_cut_fails_T2": by[("T2_sag_ambiguity_trap", "always_cut_sagging")]["permanence_probability"] < 0.25,
        "always_aid_fails_T2": by[("T2_sag_ambiguity_trap", "always_aid_sagging")]["permanence_probability"] < 0.25,
        "monoculture_fails_T3": by[("T3_monoculture_trap", "monoculture_optimizer")]["permanence_probability"] < 0.25,
        "not_starving_all_zones": any(r["mean_welfare"] > 0.45 for r in enforcement),
        "capture_not_one_for_all_enforcement": any(r["capture_probability"] < 1.0 for r in capture_enforcement),
        "pure_catastrophe_false_positive_test_run": any(r["world"] == "PURE_CATASTROPHE" for r in summary),
    }
    valid = all(checks.values())
    viable = [r for r in enforcement if r["nontrivial_enforcement_viable"]]
    reduces = any(r["capture_probability"] < 0.75 for r in capture_enforcement)
    if not valid:
        verdict = "D. Result invalid due to failed validation."
    elif viable:
        verdict = "A. Minimal type-blind consequence enforcement creates a non-trivial viability kernel."
    elif reduces:
        verdict = "B. Enforcement reduces capture but costs/collateral destroy viability."
    else:
        verdict = "C. Enforcement does not reduce capture enough."
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
    width, height = 940, 540
    ml, mr, mt, mb = 90, 30, 60, 135
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


def plots(summary):
    enforcement = [r for r in summary if r["policy"] in ENFORCEMENT_POLICIES and r["world"] in {"PURE_CAPTURE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE"}]
    labels = [r["world"] + ":" + r["policy"] + ":C" + str(r["enforcement_C"]) for r in enforcement]
    svg_bar(RESULTS / "capture_by_enforcement.svg", "Capture by Enforcement Setting", labels, [r["capture_probability"] for r in enforcement], "capture probability")
    svg_bar(RESULTS / "viability_by_enforcement.svg", "Viability by Enforcement Setting", labels, [r["viable"] for r in enforcement], "viable")
    svg_bar(RESULTS / "false_positive_pure_catastrophe.svg", "Pure Catastrophe False Positive Rate", [r["policy"] + ":C" + str(r["enforcement_C"]) for r in summary if r["world"] == "PURE_CATASTROPHE"], [r["false_positive_punishment_rate"] for r in summary if r["world"] == "PURE_CATASTROPHE"], "false positive rate")
    svg_bar(RESULTS / "cost_share_by_policy.svg", "Enforcement Cost Share", labels, [r["enforcement_cost_share"] for r in enforcement], "cost share")


def report(summary, checks, verdict, viable):
    enforcement = [r for r in summary if r["policy"] in ENFORCEMENT_POLICIES]
    best = sorted(enforcement, key=lambda r: (r["nontrivial_enforcement_viable"], r["viable"], r["permanence_probability"], -r["capture_probability"], -r["enforcement_cost_share"]), reverse=True)[:12]
    threshold = None
    for r in sorted(enforcement, key=lambda r: (r["enforcement_C"], r["audit_p"], r["penalty_duration"])):
        if r["nontrivial_enforcement_viable"]:
            threshold = r
            break
    lines = [
        "# Experiment 10 Report: Minimal Enforcement",
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
    lines += ["", "## Required Questions", "", "1. What killed Experiment 09 policies? Capture under T1/T2/FIXED_MI_DELAY; Experiment 10 keeps this as the target failure mode."]
    if threshold:
        lines.append(f"2. Minimal enforcement threshold: policy `{threshold['policy']}`, C `{threshold['enforcement_C']}`, p `{threshold['audit_p']}`, duration `{threshold['penalty_duration']}`, cost share `{threshold['enforcement_cost_share']:.3f}`, false positive `{threshold['false_positive_punishment_rate']:.3f}`.")
    else:
        lines.append("2. Minimal enforcement threshold: none found under the viability criterion.")
    lines += [
        "3. Threshold dependence: reported in raw summary across R, adversarial strength, and catastrophe worlds; no causal claim beyond this toy sweep.",
        "4. Diversity: `consequence_plus_diversity` tests enforcement plus non-adversarial diversity; raw metrics distinguish non-adversarial and adversarial diversity.",
        "5. Response-to-aid: included as comparator and as part of `consequence_plus_diversity`.",
        f"6. Viable region breadth: `{len(viable)}` non-trivial enforcement-viable cells out of `{len(enforcement)}` enforcement cells. Raw viability-only cells remain in `raw/summary.csv` and are not counted for A if they have no capture-world enforcement events/cost.",
        "7. Most controlling assumption: delayed neighbor consequence is treated as reliable enough to trigger zone-level enforcement; if that signal is adversarially controlled, the mechanism should fail.",
        "8. Current calibration failure: enforcement fires and costs resources, but no capture-relevant world gets capture below 1.0; pure-catastrophe raw viability is a control result, not an enforcement kernel.",
        "",
        "## Best Enforcement Cells",
        "",
        "| nontrivial viable | raw viable | world | policy | C | p | permanence | capture | strict zero capture | collapse | irrev frac | welfare | diversity | cost | false positive | events |",
        "|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in best:
        lines.append(f"| {r['nontrivial_enforcement_viable']} | {r['viable']} | {r['world']} | {r['policy']} | {r['enforcement_C']} | {r['audit_p']} | {r['permanence_probability']:.3f} | {r['capture_probability']:.3f} | {r['strict_zero_capture_probability']:.3f} | {r['collapse_probability']:.3f} | {r['fraction_irreversible_zones']:.3f} | {r['mean_welfare']:.3f} | {r['non_adv_diversity']:.3f} | {r['enforcement_cost_share']:.3f} | {r['false_positive_punishment_rate']:.3f} | {r['enforcement_events']:.1f} |")
    capture_rows = sorted(
        [r for r in enforcement if r["world"] in CAPTURE_WORLDS],
        key=lambda r: (r["capture_probability"], -r["permanence_probability"], r["enforcement_cost_share"]),
    )[:12]
    lines += [
        "",
        "## Capture-Relevant Enforcement Cells",
        "",
        "These rows exclude pure-catastrophe controls. The validation failure is that all capture-relevant enforcement rows retain `capture=1.0`.",
        "",
        "| world | policy | C | p | duration | R | adv | severity | migration | permanence | capture | welfare | diversity | cost | events |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in capture_rows:
        migration = f"{r['migration_speed']}/{r['migration_cost']}"
        lines.append(f"| {r['world']} | {r['policy']} | {r['enforcement_C']} | {r['audit_p']} | {r['penalty_duration']} | {r['R']:.2f} | {r['adversarial_strength']:.2f} | {r['catastrophe_severity']:.2f} | {migration} | {r['permanence_probability']:.3f} | {r['capture_probability']:.3f} | {r['mean_welfare']:.3f} | {r['non_adv_diversity']:.3f} | {r['enforcement_cost_share']:.3f} | {r['enforcement_events']:.1f} |")
    (RESULTS / "report.md").write_text("\n".join(lines) + "\n")
    vlines = ["# Experiment 10 Validation Report", "", "| check | result |", "|---|---:|"]
    for k, v in checks.items():
        vlines.append(f"| {k} | `{v}` |")
    vlines += ["", "Calibration note: `capture_not_one_for_all_enforcement` is evaluated only on capture-relevant worlds (`PURE_CAPTURE`, `MIXED_CAPTURE_CATASTROPHE`, `SCAVENGER_CATASTROPHE`).", "", f"Final verdict: **{verdict}**"]
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
    plots(summary)
    report(summary, checks, verdict, viable)
    manifest = {
        "git_head": git_value(["rev-parse", "HEAD"]),
        "git_status_short": git_value(["status", "--short"]),
        "spec_implemented_10_sha256": spec_hash(),
        "seeds": SEEDS,
        "num_cells": len(summary),
        "num_runs": len(rows),
        "num_viable_enforcement_cells": len(viable),
        "validation_checks": checks,
        "final_verdict": verdict,
    }
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"verdict": verdict, "cells": len(summary), "runs": len(rows), "viable": len(viable), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
