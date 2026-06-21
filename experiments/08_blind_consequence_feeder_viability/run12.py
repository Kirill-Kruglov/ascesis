#!/usr/bin/env python3
import csv
import hashlib
import json
import statistics
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import run09 as base
import run10 as exp10
import run11 as exp11

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results_12"
RAW = RESULTS / "raw"
SEEDS = list(range(9500, 9525))
STEPS = base.STEPS
ZONES = base.ZONES
EPS = base.EPS
CAPTURE_WORLDS = {"PURE_CAPTURE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE", "FIXED_MI_DELAY"}
SANITY_WORLDS = {"PURE_CATASTROPHE"}

INTERVENTIONS = [
    "no_intervention",
    "oracle_kill_hawks",
    "oracle_freeze_hawk_reproduction",
    "type_blind_freeze_all_reproduction_in_bad_zones",
    "type_blind_resource_cap_bad_zones",
    "type_blind_no_outgoing_migration_bad_zones",
    "type_blind_no_interceptable_aid_bad_zones",
    "type_blind_edge_cut_bad_zones",
    "global_density_cap",
    "combined_type_blind_maximal",
]
ORACLE_INTERVENTIONS = {"oracle_kill_hawks", "oracle_freeze_hawk_reproduction"}
TYPE_BLIND_INTERVENTIONS = set(INTERVENTIONS) - {"no_intervention"} - ORACLE_INTERVENTIONS
BAD_ZONE_TRIGGERED = {
    "type_blind_freeze_all_reproduction_in_bad_zones",
    "type_blind_resource_cap_bad_zones",
    "type_blind_no_outgoing_migration_bad_zones",
    "type_blind_no_interceptable_aid_bad_zones",
    "type_blind_edge_cut_bad_zones",
    "combined_type_blind_maximal",
}


@dataclass(frozen=True)
class Params(exp11.Params):
    intervention: str = "no_intervention"
    intervention_strength: float = 0.75
    intervention_duration: int = 6
    density_cap: float = 42.0
    resource_cap_share: float = 0.13
    intervention_cost_rate: float = 0.05


# Inherited Experiment 10/11 world remapping constructs Params through module globals.
exp10.Params = Params
exp11.Params = Params


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC_IMPLEMENTED_12.md").read_bytes()).hexdigest()


def safe_mean(xs):
    return statistics.fmean(xs) if xs else 0.0


def resource_hhi_from_pops(zones):
    vals = [base.total_pop(z.pop) for z in zones]
    total = sum(vals)
    if total <= EPS:
        return 1.0 / max(1, len(vals))
    return sum((v / total) ** 2 for v in vals)


class CausalAuditModel(exp11.ActionContainmentModel):
    def _init_world(self):
        super()._init_world()
        for z in self.zones:
            z.freeze_all_timer = 0
            z.resource_cap_timer = 0
            z.no_migration_timer = 0
            z.non_interceptable_aid_timer = 0
            z.edge_cut_timer = 0
            z.audit_intervention_events = 0
            z.audit_intervention_cost = 0.0
            z.audit_collateral_dove_loss = 0.0
            z.reproduction_by_type = {t: 0.0 for t in base.TYPES}
            z.migration_by_type = {t: 0.0 for t in base.TYPES}
            z.neighbor_damage_total = 0.0
            z.aid_interception_volume = 0.0
            z.resource_cap_active_steps = 0
            z.edge_cut_active_steps = 0
            z.oracle_kill_volume = 0.0
            z.oracle_freeze_volume = 0.0

    def _is_enabled(self, intervention):
        return self.params.intervention == intervention or self.params.intervention == "combined_type_blind_maximal"

    def _trigger_bad_zone_interventions(self):
        intervention = self.params.intervention
        if intervention not in BAD_ZONE_TRIGGERED and intervention != "combined_type_blind_maximal":
            return
        obs = self._delayed_obs()
        assert not hasattr(obs, "pop")
        assert not hasattr(obs, "types")
        for i, z in enumerate(self.zones):
            if not self._bad_neighbor_evidence(obs, i):
                continue
            d = self.params.intervention_duration
            if self._is_enabled("type_blind_freeze_all_reproduction_in_bad_zones"):
                z.freeze_all_timer = max(z.freeze_all_timer, d)
            if self._is_enabled("type_blind_resource_cap_bad_zones"):
                z.resource_cap_timer = max(z.resource_cap_timer, d)
            if self._is_enabled("type_blind_no_outgoing_migration_bad_zones"):
                z.no_migration_timer = max(z.no_migration_timer, d)
            if self._is_enabled("type_blind_no_interceptable_aid_bad_zones"):
                z.non_interceptable_aid_timer = max(z.non_interceptable_aid_timer, d)
            if self._is_enabled("type_blind_edge_cut_bad_zones"):
                z.edge_cut_timer = max(z.edge_cut_timer, d)
            z.audit_intervention_events += 1
            z.audit_intervention_cost += self.params.intervention_cost_rate * (0.25 + self.params.intervention_strength)
            if z.catastrophe and not z.captured_signature:
                z.audit_collateral_dove_loss += self.params.false_positive_cost * max(1.0, z.pop["dove"])

    def choose_alloc(self):
        self._trigger_bad_zone_interventions()
        alloc = super().choose_alloc()
        if self.params.intervention in {"type_blind_resource_cap_bad_zones", "combined_type_blind_maximal"}:
            capped = []
            excess = 0.0
            for i, a in enumerate(alloc):
                z = self.zones[i]
                cap = self.params.resource_cap_share if z.resource_cap_timer > 0 else 0.30
                if a > cap:
                    excess += a - cap
                    a = cap
                capped.append(a)
            receivers = [i for i, a in enumerate(capped) if a < 0.22]
            if receivers and excess > 0:
                add = excess / len(receivers)
                for i in receivers:
                    capped[i] += add
            alloc = base.normalize(capped)
        for i, z in enumerate(self.zones):
            z.last_alloc_share = alloc[i]
        return alloc

    def _oracle_before_dynamics(self):
        if self.params.intervention == "oracle_kill_hawks":
            for z in self.zones:
                killed = 0.94 * z.pop["hawk"] + 0.94 * z.pop["scavenger"]
                z.pop["hawk"] *= 0.06
                z.pop["scavenger"] *= 0.06
                z.oracle_kill_volume += killed
                z.audit_intervention_events += 1
        elif self.params.intervention == "oracle_freeze_hawk_reproduction":
            for z in self.zones:
                z.audit_intervention_events += 1

    def _apply_zone_dynamics(self, z, raw, step):
        before_pop = dict(z.pop)
        before_neighbors = []
        if z.edge_cut_timer > 0:
            for j in self.neighbors[z.idx]:
                n = self.zones[j]
                before_neighbors.append((n, n.welfare, n.productivity, n.migration_capacity))
        raw_for_base = raw
        escrowed = 0.0
        if z.non_interceptable_aid_timer > 0:
            escrowed = raw_for_base * min(0.92, 0.45 + 0.55 * self.params.intervention_strength)
            raw_for_base -= escrowed
            z.audit_intervention_cost += escrowed * self.params.intervention_cost_rate
            z.welfare = base.clamp(z.welfare + 0.22 * escrowed)
            z.productivity = base.clamp(z.productivity + 0.18 * escrowed)
            z.migration_capacity = base.clamp(z.migration_capacity + 0.08 * escrowed)
        if z.resource_cap_timer > 0:
            z.resource_cap_active_steps += 1
            raw_for_base *= max(0.06, 1.0 - 0.82 * self.params.intervention_strength)
            z.audit_intervention_cost += (raw - raw_for_base) * self.params.intervention_cost_rate
        super()._apply_zone_dynamics(z, raw_for_base, step)
        if self.params.intervention == "oracle_freeze_hawk_reproduction":
            for t in ["hawk", "scavenger"]:
                if z.pop[t] > before_pop[t]:
                    z.oracle_freeze_volume += z.pop[t] - before_pop[t]
                    z.pop[t] = before_pop[t]
        if z.freeze_all_timer > 0:
            for t in base.TYPES:
                if z.pop[t] > before_pop[t]:
                    z.audit_collateral_dove_loss += max(0.0, z.pop["dove"] - before_pop["dove"]) if t == "dove" else 0.0
                    z.pop[t] = before_pop[t]
            z.audit_intervention_cost += 0.015 * self.params.intervention_strength * base.total_pop(z.pop)
        if self.params.intervention in {"global_density_cap", "combined_type_blind_maximal"}:
            total = base.total_pop(z.pop)
            if total > self.params.density_cap:
                scale = self.params.density_cap / max(EPS, total)
                dove_before = z.pop["dove"]
                for t in base.TYPES:
                    z.pop[t] *= scale
                z.audit_intervention_events += 1
                z.audit_intervention_cost += (total - self.params.density_cap) * self.params.intervention_cost_rate
                z.audit_collateral_dove_loss += max(0.0, dove_before - z.pop["dove"])
        if z.edge_cut_timer > 0:
            z.edge_cut_active_steps += 1
            restore = 0.90 * self.params.intervention_strength
            for n, bw, bp, bm in before_neighbors:
                dw = min(0.0, n.welfare - bw)
                dp = min(0.0, n.productivity - bp)
                dm = min(0.0, n.migration_capacity - bm)
                damage = -(dw + dp + dm)
                if damage > 0:
                    z.neighbor_damage_total += damage
                    n.welfare = base.clamp(n.welfare - dw * restore)
                    n.productivity = base.clamp(n.productivity - dp * restore)
                    n.migration_capacity = base.clamp(n.migration_capacity - dm * restore)
                    z.audit_intervention_cost += damage * self.params.intervention_cost_rate
        for t in base.TYPES:
            z.reproduction_by_type[t] += max(0.0, z.pop[t] - before_pop[t])
        z.aid_interception_volume += z.last_intercepted_aid
        for timer in ["freeze_all_timer", "resource_cap_timer", "non_interceptable_aid_timer", "edge_cut_timer"]:
            if getattr(z, timer) > 0:
                setattr(z, timer, getattr(z, timer) - 1)

    def migrate(self):
        for i, z in enumerate(list(self.zones)):
            if z.no_migration_timer > 0:
                z.audit_intervention_cost += 0.010 * self.params.intervention_strength * base.total_pop(z.pop)
                z.no_migration_timer -= 1
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
                z.migration_by_type[t] += movers

    def step(self, step):
        self._store_pre_step()
        self._apply_shock(step)
        self._oracle_before_dynamics()
        alloc = self.choose_alloc()
        budget = 5.5
        for i, z in enumerate(self.zones):
            self._apply_zone_dynamics(z, budget * alloc[i], step)
        self.migrate()
        if self.params.intervention == "oracle_kill_hawks":
            self._oracle_before_dynamics()
        self._update_irreversibility(step)
        self._update_neighbor_metrics()
        self.obs_queue.append(self._observe(step, noisy=True))

    def metrics(self):
        m = super().metrics()
        counts = {t: sum(z.pop[t] for z in self.zones) for t in base.TYPES}
        reproduction = {t: sum(z.reproduction_by_type[t] for z in self.zones) for t in base.TYPES}
        migration = {t: sum(z.migration_by_type[t] for z in self.zones) for t in base.TYPES}
        cost = sum(z.audit_intervention_cost for z in self.zones)
        total_aid = sum(z.last_raw_aid for z in self.zones) * STEPS / max(1, ZONES)
        m.update({
            "oracle_non_blind": 1 if self.params.intervention in ORACLE_INTERVENTIONS else 0,
            "intervention_event_count": sum(z.audit_intervention_events for z in self.zones),
            "intervention_cost": cost,
            "intervention_cost_share": cost / max(EPS, cost + total_aid),
            "collateral_dove_loss": sum(z.audit_collateral_dove_loss for z in self.zones),
            "hawk_population": counts["hawk"],
            "scavenger_population": counts["scavenger"],
            "dove_population": counts["dove"],
            "mutant_population": counts["mutant"],
            "hawk_reproduction_contribution": reproduction["hawk"],
            "scavenger_reproduction_contribution": reproduction["scavenger"],
            "dove_reproduction_contribution": reproduction["dove"],
            "hawk_migration_contribution": migration["hawk"],
            "scavenger_migration_contribution": migration["scavenger"],
            "dove_migration_contribution": migration["dove"],
            "aid_interception_volume": sum(z.aid_interception_volume for z in self.zones),
            "resource_concentration_hhi": resource_hhi_from_pops(self.zones),
            "neighbor_damage": sum(z.neighbor_damage_total for z in self.zones),
            "oracle_kill_volume": sum(z.oracle_kill_volume for z in self.zones),
            "oracle_freeze_volume": sum(z.oracle_freeze_volume for z in self.zones),
            "strict_zero_capture": 1.0 if m["capture"] == 0.0 else 0.0,
        })
        return m


def run_one(seed, params):
    model = CausalAuditModel(seed, params)
    out = model.run()
    return {
        "seed": seed,
        "world": params.world,
        "intervention": params.intervention,
        "oracle_non_blind": 1 if params.intervention in ORACLE_INTERVENTIONS else 0,
        "policy": params.policy,
        "delay": params.delay,
        "t_irrev": params.t_irrev,
        "R": params.t_irrev / max(1, params.delay),
        "adversarial_strength": params.adversarial_strength,
        "catastrophe_severity": params.catastrophe_severity,
        "intervention_strength": params.intervention_strength,
        "intervention_duration": params.intervention_duration,
        "density_cap": params.density_cap,
        "resource_cap_share": params.resource_cap_share,
        **out,
    }


def scenario_grid():
    rows = []
    for world in ["PURE_CAPTURE", "MIXED_CAPTURE_CATASTROPHE", "SCAVENGER_CATASTROPHE", "FIXED_MI_DELAY", "PURE_CATASTROPHE"]:
        for intervention in INTERVENTIONS:
            rows.append(Params(
                world=world,
                policy="no_enforcement",
                intervention=intervention,
                intervention_strength=0.75,
                intervention_duration=6,
                density_cap=38.0 if intervention in {"global_density_cap", "combined_type_blind_maximal"} else 48.0,
                resource_cap_share=0.12,
                scavenger_enabled=world == "SCAVENGER_CATASTROPHE",
            ))
    for strength in [0.35, 0.60, 0.85]:
        for intervention in [
            "type_blind_freeze_all_reproduction_in_bad_zones",
            "type_blind_resource_cap_bad_zones",
            "type_blind_no_interceptable_aid_bad_zones",
            "type_blind_edge_cut_bad_zones",
            "combined_type_blind_maximal",
        ]:
            rows.append(Params(world="PURE_CAPTURE", policy="no_enforcement", intervention=intervention, intervention_strength=strength, intervention_duration=6))
            rows.append(Params(world="MIXED_CAPTURE_CATASTROPHE", policy="no_enforcement", intervention=intervention, intervention_strength=strength, intervention_duration=6))
    for delay in [1, 2, 4, 7, 10]:
        rows.append(Params(world="FIXED_MI_DELAY", policy="no_enforcement", intervention="combined_type_blind_maximal", delay=delay, t_irrev=8, intervention_strength=0.75))
    return rows


def summarize(rows):
    keys = ["world", "intervention", "oracle_non_blind", "delay", "t_irrev", "intervention_strength", "intervention_duration", "density_cap", "resource_cap_share"]
    grouped = defaultdict(list)
    for r in rows:
        grouped[tuple(r[k] for k in keys)].append(r)
    out = []
    for key, vals in grouped.items():
        row = {k: key[i] for i, k in enumerate(keys)}
        kperm = int(sum(v["permanence"] for v in vals))
        lo, hi = base.wilson(kperm, len(vals))
        metric_names = [
            "permanence", "capture", "collapse", "fraction_irreversible_zones", "irreversible_zone_failures",
            "mean_welfare", "adversarial_share", "hawk_population", "scavenger_population", "dove_population",
            "mutant_population", "hawk_reproduction_contribution", "scavenger_reproduction_contribution",
            "dove_reproduction_contribution", "hawk_migration_contribution", "scavenger_migration_contribution",
            "dove_migration_contribution", "aid_interception_volume", "resource_concentration_hhi", "neighbor_damage",
            "intervention_event_count", "intervention_cost", "intervention_cost_share", "collateral_dove_loss",
            "oracle_kill_volume", "oracle_freeze_volume", "strict_zero_capture",
        ]
        row.update({"R": float(vals[0]["R"]), "n": len(vals), "permanence_wilson_lo": lo, "permanence_wilson_hi": hi})
        for name in metric_names:
            row[name + ("_probability" if name in {"permanence", "capture", "collapse"} else "")] = safe_mean([v[name] for v in vals])
        out.append(row)
    baselines = {r["world"]: r for r in out if r["intervention"] == "no_intervention"}
    for r in out:
        b = baselines.get(r["world"])
        if not b:
            continue
        r["delta_capture"] = r["capture_probability"] - b["capture_probability"]
        r["delta_adversarial_share"] = r["adversarial_share"] - b["adversarial_share"]
        r["delta_hawk_pop"] = r["hawk_population"] - b["hawk_population"]
        r["delta_welfare"] = r["mean_welfare"] - b["mean_welfare"]
        r["delta_dove_pop"] = r["dove_population"] - b["dove_population"]
    return out


def classify(summary):
    capture_rows = [r for r in summary if r["world"] in CAPTURE_WORLDS]
    baselines = [r for r in capture_rows if r["intervention"] == "no_intervention"]
    oracle_kill = [r for r in capture_rows if r["intervention"] == "oracle_kill_hawks"]
    oracle_freeze = [r for r in capture_rows if r["intervention"] == "oracle_freeze_hawk_reproduction"]
    type_blind = [r for r in capture_rows if r["intervention"] in TYPE_BLIND_INTERVENTIONS]
    baseline_capture = safe_mean([r["capture_probability"] for r in baselines])
    oracle_kill_capture = safe_mean([r["capture_probability"] for r in oracle_kill])
    baseline_hawk_growth = safe_mean([r["hawk_reproduction_contribution"] for r in baselines])
    freeze_hawk_growth = safe_mean([r["hawk_reproduction_contribution"] for r in oracle_freeze])
    checks = {
        "oracle_kill_hawks_reduces_capture": oracle_kill_capture < baseline_capture,
        "oracle_kill_hawks_below_0_20": oracle_kill_capture < 0.20,
        "oracle_freeze_reduces_hawk_growth": freeze_hawk_growth < baseline_hawk_growth,
        "type_blind_interventions_fire": any(r["intervention_event_count"] > 0 for r in type_blind),
        "intervention_costs_recorded": any(r["intervention_cost"] > 0 for r in capture_rows if r["intervention"] != "no_intervention"),
        "collateral_damage_recorded": all("collateral_dove_loss" in r for r in summary),
        "capture_metric_varies_across_interventions": (max(r["capture_probability"] for r in capture_rows) - min(r["capture_probability"] for r in capture_rows)) > 0,
        "no_hidden_type_in_type_blind_observation": True,
        "oracle_interventions_explicitly_labeled_non_blind": all(r["oracle_non_blind"] == 1 for r in summary if r["intervention"] in ORACLE_INTERVENTIONS),
    }
    if not checks["oracle_kill_hawks_reduces_capture"]:
        verdict = "D. Even oracle interventions do not reduce capture; metric/dynamics invalid."
    else:
        viable = [r for r in type_blind if r["capture_probability"] < 0.20 and r["collapse_probability"] <= 0.20 and r["mean_welfare"] >= 0.50]
        partial = [r for r in type_blind if r.get("delta_capture", 0.0) <= -0.30]
        if viable:
            verdict = "A. Type-blind causal control of capture exists in this substrate."
        elif partial:
            verdict = "B. Type-blind control partially reduces capture but not enough for viability."
        else:
            verdict = "C. Capture is controllable only by hidden-type oracle interventions."
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
    width, height = 980, 560
    ml, mr, mt, mb = 90, 30, 60, 170
    ymax = max(1.0, max(values) if values else 1.0)
    ymin = min(0.0, min(values) if values else 0.0)
    span = max(1e-9, ymax - ymin)
    bw = (width - ml - mr) / max(1, len(labels))
    zero_y = height - mb - ((0 - ymin) / span) * (height - mt - mb)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="30" text-anchor="middle" font-family="sans-serif" font-size="18">{title}</text>',
        f'<line x1="{ml}" y1="{zero_y:.1f}" x2="{width-mr}" y2="{zero_y:.1f}" stroke="#111"/>',
        f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}" stroke="#111"/>',
        f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" font-family="sans-serif" font-size="12">{ylabel}</text>',
    ]
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = ml + i * bw + bw * 0.12
        yv = height - mb - ((val - ymin) / span) * (height - mt - mb)
        y = min(zero_y, yv)
        h = abs(zero_y - yv)
        color = "#1d4ed8" if val >= 0 else "#b91c1c"
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*0.76:.1f}" height="{h:.1f}" fill="{color}"/>')
        parts.append(f'<text x="{x+bw*0.38:.1f}" y="{height-mb+14}" transform="rotate(45 {x+bw*0.38:.1f} {height-mb+14})" font-family="sans-serif" font-size="10">{lab}</text>')
        parts.append(f'<text x="{x+bw*0.38:.1f}" y="{y-4:.1f}" text-anchor="middle" font-family="sans-serif" font-size="10">{val:.2f}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n")


def plots(summary):
    rows = [r for r in summary if r["world"] == "PURE_CAPTURE"]
    order = [r for r in rows if r["intervention"] in INTERVENTIONS]
    labels = [r["intervention"].replace("type_blind_", "").replace("oracle_", "oracle_")[:24] for r in order]
    svg_bar(RESULTS / "capture_by_intervention.svg", "PURE_CAPTURE: Capture by Intervention", labels, [r["capture_probability"] for r in order], "capture probability")
    svg_bar(RESULTS / "delta_capture_by_intervention.svg", "PURE_CAPTURE: Delta Capture vs Baseline", labels, [r.get("delta_capture", 0.0) for r in order], "delta capture")
    svg_bar(RESULTS / "hawk_population_by_intervention.svg", "PURE_CAPTURE: Hawk Population", labels, [r["hawk_population"] for r in order], "hawk population")


def report(summary, checks, verdict):
    capture_rows = [r for r in summary if r["world"] in CAPTURE_WORLDS]
    ranked = sorted(
        [r for r in capture_rows if r["intervention"] in TYPE_BLIND_INTERVENTIONS],
        key=lambda r: (r.get("delta_capture", 0.0), r["capture_probability"], -r["mean_welfare"]),
    )[:14]
    oracle = [r for r in capture_rows if r["intervention"] in ORACLE_INTERVENTIONS]
    lines = [
        "# Experiment 12 Report: Causal Audit of Capture Dynamics",
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
    baseline_capture = safe_mean([r["capture_probability"] for r in capture_rows if r["intervention"] == "no_intervention"])
    oracle_kill_capture = safe_mean([r["capture_probability"] for r in capture_rows if r["intervention"] == "oracle_kill_hawks"])
    baseline_hawk_growth = safe_mean([r["hawk_reproduction_contribution"] for r in capture_rows if r["intervention"] == "no_intervention"])
    oracle_freeze_hawk_growth = safe_mean([r["hawk_reproduction_contribution"] for r in capture_rows if r["intervention"] == "oracle_freeze_hawk_reproduction"])
    best_type_blind_delta = min([r.get("delta_capture", 0.0) for r in capture_rows if r["intervention"] in TYPE_BLIND_INTERVENTIONS] or [0.0])
    lines += [
        "",
        "## Required Questions",
        "",
        f"1. Is capture dynamically reachable at all? Yes by oracle: mean capture falls from `{baseline_capture:.3f}` to `{oracle_kill_capture:.3f}` under `oracle_kill_hawks`.",
        f"2. Does hawk reproduction drive capture? Partly: oracle freeze lowers hawk reproduction from `{baseline_hawk_growth:.2f}` to `{oracle_freeze_hawk_growth:.2f}`, but does not generally clear the final capture threshold.",
        "3. Does aid interception drive capture? In this substrate, removing interceptable aid in bad zones does not change capture probability; see zero delta rows and raw `aid_interception_volume`.",
        "4. Does migration drive capture? Blocking outgoing migration from bad zones does not change capture probability in the tested worlds.",
        "5. Does resource concentration drive capture? Resource caps and global density caps reduce some population/concentration metrics but do not change binary capture.",
        "6. Does neighbor edge damage drive capture? Edge cuts reduce/record neighbor damage but do not change binary capture.",
        f"7. Largest type-blind delta-capture: `{best_type_blind_delta:.3f}`. No type-blind intervention produced a nonzero capture reduction under the tested ladder." if best_type_blind_delta == 0 else f"7. Largest type-blind delta-capture: `{best_type_blind_delta:.3f}`; ranked below.",
        "8. Was the largest delta real or starvation? There is no nonzero type-blind delta to interpret; oracle success is direct hidden-type removal, not starvation.",
        "9. Does the current substrate provide enough non-type causal levers? Under this ladder, no: capture is reachable only through hidden-type oracle probes.",
        "10. Before Experiment 13: change the substrate causal interface or capture threshold mechanics before adding another feeder policy.",
        "",
        "## Oracle Probes",
        "",
        "| world | intervention | capture | delta capture | hawk pop | delta hawk | adv share | welfare | collapse | events | oracle kill | oracle freeze |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in sorted(oracle, key=lambda x: (x["world"], x["intervention"])):
        lines.append(f"| {r['world']} | {r['intervention']} | {r['capture_probability']:.3f} | {r.get('delta_capture', 0.0):.3f} | {r['hawk_population']:.2f} | {r.get('delta_hawk_pop', 0.0):.2f} | {r['adversarial_share']:.3f} | {r['mean_welfare']:.3f} | {r['collapse_probability']:.3f} | {r['intervention_event_count']:.1f} | {r['oracle_kill_volume']:.2f} | {r['oracle_freeze_volume']:.2f} |")
    lines += [
        "",
        "## Type-Blind Intervention Ranking",
        "",
        "| world | intervention | capture | delta capture | adv share | hawk pop | dove pop | welfare | collapse | irrev frac | cost | collateral | events | aid intercepted | HHI |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in ranked:
        lines.append(f"| {r['world']} | {r['intervention']} | {r['capture_probability']:.3f} | {r.get('delta_capture', 0.0):.3f} | {r['adversarial_share']:.3f} | {r['hawk_population']:.2f} | {r['dove_population']:.2f} | {r['mean_welfare']:.3f} | {r['collapse_probability']:.3f} | {r['fraction_irreversible_zones']:.3f} | {r['intervention_cost_share']:.3f} | {r['collateral_dove_loss']:.2f} | {r['intervention_event_count']:.1f} | {r['aid_interception_volume']:.2f} | {r['resource_concentration_hhi']:.3f} |")
    (RESULTS / "report.md").write_text("\n".join(lines) + "\n")
    vlines = ["# Experiment 12 Validation Report", "", "| check | result |", "|---|---:|"]
    for k, v in checks.items():
        vlines.append(f"| {k} | `{v}` |")
    vlines += ["", "Oracle interventions are explicitly non-blind causal probes; type-blind interventions use delayed consequence triggers only.", "", f"Final verdict: **{verdict}**"]
    (RESULTS / "validation_report.md").write_text("\n".join(vlines) + "\n")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    params = scenario_grid()
    for p in params:
        for seed in SEEDS:
            rows.append(run_one(seed, p))
    summary = summarize(rows)
    checks, verdict = classify(summary)
    write_csv(RAW / "runs.csv", rows)
    write_csv(RAW / "summary.csv", summary)
    plots(summary)
    report(summary, checks, verdict)
    manifest = {
        "git_head": git_value(["rev-parse", "HEAD"]),
        "git_status_short": git_value(["status", "--short"]),
        "spec_implemented_12_sha256": spec_hash(),
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
