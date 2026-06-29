#!/usr/bin/env python3
"""BA1.E1 monotonicity-breaker ablation map.

This runner is diagnostic only. It does not change Justitia, the real collapse
predicate, the 18.0 shield abstraction, or shield thresholds. It constructs weak
single-mechanism ablations as subclasses around the current Justitia substrate
and evaluates the unchanged 18.0 two-counter shield label against real future
collapse in the generated trajectories.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
JUSTITIA_MODEL = Path("/home/master/llm_projects/justitia/model")
SHIELD_SRC = Path("/home/master/llm_projects/ascesis/experiments/18_0_shield_synthesis/src")

for p in [JUSTITIA_MODEL, SHIELD_SRC]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import substrate as base  # noqa: E402
from shield import ShieldParams, compute_doomed  # noqa: E402

WELFARE_MEAN_FLOOR = 0.32
ZONE_WELFARE_FLOOR = 0.20
MASS_FLOOR = 35.0
SHIELD_PARAMS = ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)

RUN_CLASSES = {}


def register(name):
    def deco(cls):
        RUN_CLASSES[name] = cls
        return cls

    return deco


@register("baseline")
class Baseline(base.EvolvableStrategyModel):
    pass


@register("MB1")
class MB1NoMemory(base.EvolvableStrategyModel):
    """Remove delayed/memory observables from the policy input.

    The weakest clean isolation available without editing Justitia internals is:
    use the most recent observation in the queue instead of the delayed head and
    zero the explicit memory coordinates consumed by policies.
    """

    def _delayed_obs(self):
        obs = self.obs_queue[-1]
        return base.Obs(
            step=obs.step,
            wellness=obs.wellness,
            productivity=obs.productivity,
            recovery=obs.recovery,
            migration_capacity=obs.migration_capacity,
            strategy_diversity=obs.strategy_diversity,
            response_diversity=obs.response_diversity,
            resource_concentration=obs.resource_concentration,
            apparent_cooperation=obs.apparent_cooperation,
            sag=obs.sag,
            last_aid=tuple(0.0 for _ in obs.last_aid),
            response_to_aid=tuple(0.0 for _ in obs.response_to_aid),
            neighbor_delta=tuple(0.0 for _ in obs.neighbor_delta),
            global_welfare=obs.global_welfare,
        )


@register("MB2")
class MB2NoRelativeCompetition(base.EvolvableStrategyModel):
    """Remove relative allocation competition while preserving policy triggers."""

    def choose_alloc(self):
        obs = self._delayed_obs()
        if self.params.policy in {"action_channel_containment", "consequence_plus_diversity"}:
            for i, z in enumerate(self.zones):
                if self._bad_consequence(obs, i):
                    z.containment_timer = max(z.containment_timer, self.params.containment_duration)
                    z.containment_events += 1
                    z.containment_cost += 0.030 * self.params.containment_strength
                    if z.catastrophe:
                        z.false_containment += 1
        return [1.0 / base.ZONES for _ in range(base.ZONES)]


@register("MB3")
class MB3NoInterpretivePolicy(base.EvolvableStrategyModel):
    """Disable consequence interpretation, audit triggers, and containment gating."""

    def _bad_consequence(self, obs, i):
        return False

    def _audit_trigger(self, z, obs, i):
        return False


@register("MB4")
class MB4NoAdaptivePopulation(base.EvolvableStrategyModel):
    """Freeze mutation, migration, replication, and selection mass dynamics."""

    def _apply_zone_dynamics(self, z, raw_aid, alloc_share, obs, idx):
        saved_lineages = deepcopy(z.lineages)
        saved_migration_capacity = z.migration_capacity
        super()._apply_zone_dynamics(z, raw_aid, alloc_share, obs, idx)
        z.lineages = saved_lineages
        z.migration_capacity = saved_migration_capacity

    def _migrate(self):
        return None


@register("MB5")
class MB5NoRelativeObservables(base.EvolvableStrategyModel):
    """Neutralize relative concentration observables used by policy/dynamics."""

    def _resource_hhi_zone(self, z):
        return 1.0 / base.ZONES

    def _apparent_cooperation(self, z):
        coop = self._weighted(z, "cooperation_investment")
        prod = self._weighted(z, "productive_contribution")
        return base.clamp(0.56 * coop + 0.44 * prod)


def collapse_clauses(zone_welfare, total_mass):
    mean_w = statistics.fmean(zone_welfare) if zone_welfare else 0.0
    spread_count = sum(1 for w in zone_welfare if w < ZONE_WELFARE_FLOOR)
    return {
        "mean_clause": mean_w < WELFARE_MEAN_FLOOR,
        "spread_clause": spread_count >= 4,
        "mass_clause": total_mass < MASS_FLOOR,
        "mean_welfare": mean_w,
        "min_zone_welfare": min(zone_welfare) if zone_welfare else 0.0,
        "spread_count": spread_count,
        "total_mass": total_mass,
    }


def project(mean_welfare, resource_hhi):
    deficit = max(0.0, 1.0 - mean_welfare)
    a = min(SHIELD_PARAMS.Amax, round(SHIELD_PARAMS.A_collapse * deficit / (1.0 - WELFARE_MEAN_FLOOR)))
    c = min(SHIELD_PARAMS.Cmax, round(resource_hhi * SHIELD_PARAMS.Cmax))
    return c, a


DOOMED = compute_doomed(SHIELD_PARAMS, "bounded")["doomed"]


def shield_label(state):
    return "DOOMED" if project(state["mean_welfare"], state["resource_hhi"]) in DOOMED else "SAFE"


def suffix_future_collapse(states):
    flags = [False] * len(states)
    acc = False
    for i in range(len(states) - 1, -1, -1):
        acc = acc or bool(states[i]["collapse"])
        flags[i] = acc
    return flags


def harvest_states(model_cls, worlds, policies, seeds):
    states = []
    for world in worlds:
        for policy in policies:
            for seed in seeds:
                params = base.Params(mode="governance", world=world, policy=policy)
                model = model_cls(seed, params, record_trajectory=True)
                model.run()
                prev = None
                traj_key = f"{world}|{policy}|{seed}"
                for snap in model.trajectory:
                    zone_welfare = list(snap["zone_welfare"])
                    zone_mass = list(snap["zone_mass"])
                    total_mass = sum(zone_mass)
                    clauses = collapse_clauses(zone_welfare, total_mass)
                    st = {
                        "run": "",
                        "world": world,
                        "policy": policy,
                        "seed": seed,
                        "traj_key": traj_key,
                        "step": snap["step"],
                        "zone_welfare": zone_welfare,
                        "zone_mass": zone_mass,
                        "resource_hhi": float(snap["resource_hhi"]),
                        "capture_index": float(snap["capture_index"]),
                        "exploit_mass": float(snap["exploitative_strategy_mass"]),
                        "containment_this_step": int(snap["containment_events_this_step"]),
                        "collapse": bool(clauses["mean_clause"] or clauses["spread_clause"] or clauses["mass_clause"]),
                        "collapse_code": bool(snap["collapse"]),
                        "prev": prev,
                        **clauses,
                    }
                    states.append(st)
                    prev = {
                        "mean_welfare": st["mean_welfare"],
                        "min_zone_welfare": st["min_zone_welfare"],
                        "spread_count": st["spread_count"],
                        "total_mass": st["total_mass"],
                        "resource_hhi": st["resource_hhi"],
                        "capture_index": st["capture_index"],
                    }
    return states


def group_trajectories(states):
    grouped = defaultdict(list)
    for s in states:
        grouped[s["traj_key"]].append(s)
    for seq in grouped.values():
        seq.sort(key=lambda s: s["step"])
    return grouped


def augment_labels(run_name, states):
    for s in states:
        s["run"] = run_name
        lab = shield_label(s)
        s["shield_label"] = lab
        s["shield_accept"] = lab == "SAFE"
    for seq in group_trajectories(states).values():
        flags = suffix_future_collapse(seq)
        for s, f in zip(seq, flags):
            s["future_collapse"] = bool(f)
            s["false_safe"] = bool(s["shield_accept"] and f)
            s["false_unsafe"] = bool((not s["shield_accept"]) and (not f))
    return states


def rate(num, den):
    return num / den if den else 0.0


def summarize_run(run_name, states):
    n = len(states)
    safe = sum(1 for s in states if s["shield_accept"])
    doomed = n - safe
    false_safe = sum(1 for s in states if s["false_safe"])
    false_unsafe = sum(1 for s in states if s["false_unsafe"])
    cur_collapsed = [s for s in states if s["collapse"]]
    cur_collapsed_safe = [s for s in cur_collapsed if s["shield_accept"]]
    actual_future = [s for s in states if s["future_collapse"]]

    clause_names = ["mean_clause", "spread_clause", "mass_clause"]
    coverage = {
        c: rate(sum(1 for s in actual_future if s[c]), len(actual_future))
        for c in clause_names
    }
    overlap = {}
    for a in clause_names:
        overlap[a] = {}
        for b in clause_names:
            overlap[a][b] = rate(sum(1 for s in states if s[a] and s[b]), n)

    false_blindness = {
        "false_safe_total": false_safe,
        "false_safe_due_forward_dynamics": sum(1 for s in states if s["false_safe"] and not s["collapse"]),
        "false_safe_current_spread_clause_blind": sum(
            1 for s in states if s["false_safe"] and s["spread_clause"] and not s["mean_clause"]
        ),
        "false_safe_current_mass_clause_blind": sum(
            1 for s in states if s["false_safe"] and s["mass_clause"] and not s["mean_clause"]
        ),
        "false_unsafe_total": false_unsafe,
        "false_unsafe_primary_mean_only": sum(
            1 for s in states if s["false_unsafe"] and s["mean_clause"] and not s["future_collapse"]
        ),
    }

    per_policy = {}
    for policy in sorted({s["policy"] for s in states}):
        ps = [s for s in states if s["policy"] == policy]
        ps_safe = sum(1 for s in ps if s["shield_accept"])
        per_policy[policy] = {
            "n": len(ps),
            "n_safe": ps_safe,
            "false_safe_rate": rate(sum(1 for s in ps if s["false_safe"]), ps_safe),
            "false_unsafe_rate": rate(sum(1 for s in ps if s["false_unsafe"]), len(ps) - ps_safe),
        }

    summary = {
        "run": run_name,
        "n_states": n,
        "n_safe": safe,
        "n_doomed": doomed,
        "shield_acceptance_rate": rate(safe, n),
        "false_safe_rate": rate(false_safe, safe),
        "false_unsafe_rate": rate(false_unsafe, doomed),
        "future_collapse_rate": rate(sum(1 for s in states if s["future_collapse"]), n),
        "current_collapse_rate": rate(len(cur_collapsed), n),
        "code_flag_agreement_fraction": rate(sum(1 for s in states if s["collapse"] == s["collapse_code"]), n),
        "pure_blindness": {
            "n_currently_collapsed": len(cur_collapsed),
            "currently_collapsed_labeled_safe": len(cur_collapsed_safe),
            "rate": rate(len(cur_collapsed_safe), len(cur_collapsed)),
        },
        "false_blindness_decomposition": false_blindness,
        "collapse_coverage": coverage,
        "clause_overlap_matrix": overlap,
        "per_policy": per_policy,
        "mean_welfare_mean": statistics.fmean(s["mean_welfare"] for s in states) if states else 0.0,
        "total_mass_mean": statistics.fmean(s["total_mass"] for s in states) if states else 0.0,
        "resource_hhi_mean": statistics.fmean(s["resource_hhi"] for s in states) if states else 0.0,
    }
    return summary


def worse_or_equal(a, b):
    return (
        a["mean_welfare"] <= b["mean_welfare"] + 1e-12
        and a["min_zone_welfare"] <= b["min_zone_welfare"] + 1e-12
        and a["spread_count"] >= b["spread_count"]
        and a["total_mass"] <= b["total_mass"] + 1e-12
        and (
            a["mean_welfare"] < b["mean_welfare"] - 1e-12
            or a["min_zone_welfare"] < b["min_zone_welfare"] - 1e-12
            or a["spread_count"] > b["spread_count"]
            or a["total_mass"] < b["total_mass"] - 1e-12
        )
    )


def witness_search(run_name, states, rng, max_states=2400, max_pairs=90000, keep=40):
    sample = states
    if len(sample) > max_states:
        sample = rng.sample(sample, max_states)
    witnesses = []
    counts = Counter()
    n = len(sample)
    if n < 2:
        return {"witness_count": 0, "minimal_counterexample_count": 0, "examples": []}

    for _ in range(max_pairs):
        a, b = rng.sample(sample, 2)
        if worse_or_equal(a, b):
            worse, better = a, b
        elif worse_or_equal(b, a):
            worse, better = b, a
        else:
            continue

        typ = None
        if worse["shield_accept"] and not better["shield_accept"]:
            typ = "acceptance_nonmonotone_worse_safe_better_doomed"
        elif worse["false_safe"] and not better["false_safe"]:
            typ = "fidelity_nonmonotone_worse_false_safe_better_not"
        elif worse["future_collapse"] and not better["future_collapse"] and worse["shield_accept"]:
            typ = "transition_future_collapse_worse_safe"

        if typ is None:
            continue
        counts[typ] += 1
        if len(witnesses) < keep:
            witnesses.append({
                "run": run_name,
                "type": typ,
                "worse_world": worse["world"],
                "worse_policy": worse["policy"],
                "worse_seed": worse["seed"],
                "worse_step": worse["step"],
                "worse_mean_welfare": round(worse["mean_welfare"], 6),
                "worse_min_zone_welfare": round(worse["min_zone_welfare"], 6),
                "worse_spread_count": worse["spread_count"],
                "worse_total_mass": round(worse["total_mass"], 6),
                "worse_shield_label": worse["shield_label"],
                "worse_future_collapse": worse["future_collapse"],
                "worse_current_collapse": worse["collapse"],
                "better_world": better["world"],
                "better_policy": better["policy"],
                "better_seed": better["seed"],
                "better_step": better["step"],
                "better_mean_welfare": round(better["mean_welfare"], 6),
                "better_min_zone_welfare": round(better["min_zone_welfare"], 6),
                "better_spread_count": better["spread_count"],
                "better_total_mass": round(better["total_mass"], 6),
                "better_shield_label": better["shield_label"],
                "better_future_collapse": better["future_collapse"],
                "better_current_collapse": better["collapse"],
            })

    unique_shapes = {
        (
            w["type"],
            w["worse_policy"],
            w["better_policy"],
            int(w["worse_spread_count"] >= 4),
            int(w["worse_total_mass"] < MASS_FLOOR),
            w["worse_shield_label"],
            w["better_shield_label"],
        )
        for w in witnesses
    }
    return {
        "witness_count": int(sum(counts.values())),
        "witness_type_counts": dict(counts),
        "minimal_counterexample_count": len(unique_shapes),
        "examples": witnesses,
    }


def semantic_delta(summary, baseline):
    return {
        "current_collapse_rate_delta": summary["current_collapse_rate"] - baseline["current_collapse_rate"],
        "future_collapse_rate_delta": summary["future_collapse_rate"] - baseline["future_collapse_rate"],
        "shield_acceptance_rate_delta": summary["shield_acceptance_rate"] - baseline["shield_acceptance_rate"],
        "mean_welfare_delta": summary["mean_welfare_mean"] - baseline["mean_welfare_mean"],
        "total_mass_delta": summary["total_mass_mean"] - baseline["total_mass_mean"],
    }


def assess_semantic_validity(delta):
    severe = (
        abs(delta["future_collapse_rate_delta"]) > 0.35
        or abs(delta["shield_acceptance_rate_delta"]) > 0.45
        or abs(delta["mean_welfare_delta"]) > 0.25
    )
    return "severe_semantic_shift" if severe else "comparable_enough_for_diagnostic"


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def write_csv(path, rows, fieldnames=None):
    if fieldnames is None:
        keys = []
        for row in rows:
            for k in row:
                if k not in keys:
                    keys.append(k)
        fieldnames = keys
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def flatten_summary(summary):
    return {
        "run": summary["run"],
        "n_states": summary["n_states"],
        "shield_acceptance_rate": summary["shield_acceptance_rate"],
        "false_safe_rate": summary["false_safe_rate"],
        "false_unsafe_rate": summary["false_unsafe_rate"],
        "pure_blindness_rate": summary["pure_blindness"]["rate"],
        "current_collapse_rate": summary["current_collapse_rate"],
        "future_collapse_rate": summary["future_collapse_rate"],
        "mean_clause_coverage": summary["collapse_coverage"]["mean_clause"],
        "spread_clause_coverage": summary["collapse_coverage"]["spread_clause"],
        "mass_clause_coverage": summary["collapse_coverage"]["mass_clause"],
        "minimal_counterexample_count": summary.get("minimal_counterexample_count", 0),
        "monotonicity_witness_count": summary.get("monotonicity_witness_count", 0),
        "semantic_validity": summary.get("semantic_validity", "baseline"),
        "future_collapse_rate_delta": summary.get("semantic_delta_vs_baseline", {}).get("future_collapse_rate_delta", 0.0),
    }


def contribution_rows(summaries):
    baseline = summaries["baseline"]
    base_fs = baseline["false_safe_rate"]
    rows = []
    for name in ["MB1", "MB2", "MB3", "MB4", "MB5"]:
        fs = summaries[name]["false_safe_rate"]
        raw = base_fs - fs
        ci = raw / base_fs if base_fs > 0 else 0.0
        usable = summaries[name].get("semantic_validity", "") != "severe_semantic_shift"
        rows.append({
            "mechanism": name,
            "baseline_false_safe_rate": base_fs,
            "ablation_false_safe_rate": fs,
            "absolute_reduction": raw,
            "contribution_index": ci,
            "positive_contribution_index": max(0.0, ci),
            "usable_for_dominance": int(usable),
            "usable_positive_contribution_index": max(0.0, ci) if usable else 0.0,
            "semantic_validity": summaries[name].get("semantic_validity", ""),
        })
    return rows


def decide(rows, summaries):
    positives = [r["usable_positive_contribution_index"] for r in rows]
    apparent_positives = [r["positive_contribution_index"] for r in rows]
    total = sum(positives)
    largest = max(positives) if positives else 0.0
    top = rows[positives.index(largest)]["mechanism"] if positives and largest > 0 else "none_clean_ablation"
    apparent_largest = max(apparent_positives) if apparent_positives else 0.0
    apparent_top = rows[apparent_positives.index(apparent_largest)]["mechanism"] if apparent_largest > 0 else "none"
    dominance_ratio = largest / total if total > 0 else 0.0
    material = [r for r in rows if r["usable_positive_contribution_index"] >= 0.15]
    invalid = [r["mechanism"] for r in rows if summaries[r["mechanism"]].get("semantic_validity") == "severe_semantic_shift"]

    if largest >= 0.55 and dominance_ratio >= 0.60:
        case = "Case A / H0_supported"
        conclusion = "one mechanism dominates observed fidelity loss"
    elif len(material) >= 2 and dominance_ratio < 0.60:
        case = "Case B / H1_supported"
        conclusion = "several mechanisms contribute independently"
    elif largest < 0.15:
        case = "Case C / H2_supported"
        conclusion = "single-mechanism ablations do not materially reduce false-safe error"
    else:
        case = "Inconclusive"
        conclusion = "evidence is mixed; single-mechanism effects exist but dominance is weak"
    if invalid and apparent_largest >= 0.55 and largest < 0.15:
        conclusion = (
            "the only apparently dominant ablation is a severe semantic shift; "
            "clean single-mechanism ablations do not materially reduce false-safe error"
        )

    interaction_indicator = {
        "dominance_ratio": dominance_ratio,
        "largest_positive_CI": largest,
        "apparent_largest_positive_CI_including_invalid": apparent_largest,
        "apparent_top_mechanism_including_invalid": apparent_top,
        "top_mechanism": top,
        "material_single_ablation_count": len(material),
        "semantic_shift_ablation_warnings": invalid,
        "qualitative_interaction_indicator": (
            "high" if largest < 0.15 else "moderate" if dominance_ratio < 0.60 else "low"
        ),
        "interpretation": conclusion,
    }
    return case, top, interaction_indicator


def make_transition_counterexamples(witnesses):
    lines = [
        "# BA1.E1 Transition Counterexamples",
        "",
        "The examples below are sampled witness pairs under the diagnostic deficit order:",
        "`worse <= better` means lower mean welfare, lower minimum zone welfare,",
        "more low-welfare zones, and lower total mass. They are not repairs.",
        "",
    ]
    if not witnesses:
        lines.append("No sampled counterexample witnesses were found.")
        return "\n".join(lines) + "\n"
    for i, w in enumerate(witnesses[:24], 1):
        lines.extend([
            f"## Witness {i}: {w['run']} / {w['type']}",
            "",
            f"- Worse state: `{w['worse_world']}`, `{w['worse_policy']}`, seed {w['worse_seed']}, step {w['worse_step']}; "
            f"mean={w['worse_mean_welfare']}, min={w['worse_min_zone_welfare']}, "
            f"spread={w['worse_spread_count']}, mass={w['worse_total_mass']}, "
            f"shield={w['worse_shield_label']}, future_collapse={w['worse_future_collapse']}.",
            f"- Better state: `{w['better_world']}`, `{w['better_policy']}`, seed {w['better_seed']}, step {w['better_step']}; "
            f"mean={w['better_mean_welfare']}, min={w['better_min_zone_welfare']}, "
            f"spread={w['better_spread_count']}, mass={w['better_total_mass']}, "
            f"shield={w['better_shield_label']}, future_collapse={w['better_future_collapse']}.",
            "",
        ])
    return "\n".join(lines)


def make_mechanism_revision(summaries, decision):
    lines = [
        "# BA1.E1 Mechanism Revision",
        "",
        "The five-way taxonomy is useful but not perfectly separable in the current code.",
        "",
        "## Supported Splits",
        "",
        "- MB1 should be split into observation delay and explicit response-memory fields. "
        "Both enter `_delayed_obs` / `Obs`, but they are not the same mechanism.",
        "- MB2 should be split into allocation normalization and containment caps/redistribution. "
        "The weak ablation had to keep interpretive triggers while removing resource competition.",
        "- MB5 should be split into policy-visible relative observables and diagnostic/final metrics. "
        "The former can be neutralized; the latter remain part of measurement and 18.0 projection.",
        "",
        "## Inseparable Components",
        "",
        "- MB3 and MB2 touch the same `choose_alloc` path for containment policies: bad-consequence "
        "interpretation sets timers before capped redistribution acts.",
        "- MB4 affects future welfare indirectly through mass, payoff, mutation, migration, and pruning. "
        "Freezing it preserves immediate welfare formulas but changes the long-run substrate semantics.",
        "",
        "## Taxonomy Verdict",
        "",
        f"- Final diagnostic decision: `{decision}`.",
        "- The taxonomy is supported as a first pass, but the implementation suggests submechanisms "
        "rather than five cleanly orthogonal axes.",
    ]
    return "\n".join(lines) + "\n"


def make_notes(args):
    return "\n".join([
        "# BA1.E1 Implementation Notes",
        "",
        "No Justitia source file was modified.",
        "",
        "## Fixed Inputs",
        "",
        "- Justitia model path: `/home/master/llm_projects/justitia/model/substrate.py`.",
        "- Collapse predicate unchanged: `mean(zone_welfare)<0.32 OR count(zone_welfare<0.20)>=4 OR total_mass<35`.",
        "- 18.0 shield abstraction unchanged: `ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)`.",
        "- Projection unchanged from 18.1: `a = round(A_collapse*(1-mean_welfare)/(1-0.32))`, `c = round(resource_hhi*Cmax)`.",
        "- Bounded-coupling doomed set is computed by the existing 18.0 `compute_doomed`; in this setting it is U-only.",
        "",
        "## Ground Truth",
        "",
        "- `future_collapse` means real collapse occurs at the current or later step in the same trajectory.",
        "- `false_safe_rate = P(future_collapse | shield says SAFE)`.",
        "- `false_unsafe_rate = P(no future_collapse | shield says DOOMED)`.",
        "- `pure_blindness` is the rate of currently-collapsed states labelled SAFE by the unchanged 18.0 shield.",
        "",
        "## Run Grid",
        "",
        f"- Worlds: `{args.worlds}`.",
        f"- Policies: `{args.policies}`.",
        f"- Seeds: `{args.seeds}`.",
        "- Steps per trajectory are Justitia's current `STEPS` constant.",
        "",
        "## Ablation Caveats",
        "",
        "- MB1 removes both delay and explicit memory observables from policy input.",
        "- MB2 removes allocation competition by uniform per-zone allocation but keeps bad-consequence policy triggers.",
        "- MB3 disables bad-consequence/audit interpretation.",
        "- MB4 freezes lineage mass/adaptation and migration after immediate welfare dynamics are applied.",
        "- MB5 neutralizes policy-visible concentration observables; measured resource HHI remains observable for diagnostics.",
        "",
    ]) + "\n"


def make_final_report(summaries, contrib, decision_case, top, interaction):
    rows = [flatten_summary(summaries[k]) for k in ["baseline", "MB1", "MB2", "MB3", "MB4", "MB5"]]
    lines = [
        "# BA1.E1 Monotonicity Breaker Ablation Map",
        "",
        f"**Decision:** `{decision_case}`.",
        f"**Top valid single mechanism:** `{top}`.",
        f"**Dominance ratio:** `{interaction['dominance_ratio']:.3f}`.",
        f"**Apparent invalid dominant mechanism:** `{interaction['apparent_top_mechanism_including_invalid']}` "
        f"(CI={interaction['apparent_largest_positive_CI_including_invalid']:.3f}).",
        "",
        "## Summary Table",
        "",
        "| run | false_safe | false_unsafe | pure_blindness | accept | future_collapse | witnesses | semantic_validity |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['run']} | {r['false_safe_rate']:.4f} | {r['false_unsafe_rate']:.4f} | "
            f"{r['pure_blindness_rate']:.4f} | {r['shield_acceptance_rate']:.4f} | "
            f"{r['future_collapse_rate']:.4f} | {r['monotonicity_witness_count']} | {r['semantic_validity']} |"
        )
    lines.extend([
        "",
        "## Contribution Index",
        "",
        "| mechanism | ablated false_safe | CI | semantic_validity |",
        "|---|---:|---:|---|",
    ])
    for r in contrib:
        lines.append(
            f"| {r['mechanism']} | {r['ablation_false_safe_rate']:.4f} | "
            f"{r['contribution_index']:.4f} | {r['semantic_validity']} |"
        )
    lines.extend([
        "",
        "## Required Questions",
        "",
        f"1. Does one mechanism dominate? {'Yes' if decision_case.startswith('Case A') else 'No'}; DR={interaction['dominance_ratio']:.3f}.",
        f"2. Largest measured contributor: `{top}`.",
        "3. Semantically indispensable mechanisms: any ablation marked `severe_semantic_shift`; see `contribution_index.csv`.",
        "4. Implementation artifacts: MB2/MB3 coupling in `choose_alloc`; MB5 measurement-vs-policy split.",
        "5. Removable without material semantic change: ablations marked `comparable_enough_for_diagnostic` only.",
        "6. Taxonomy: useful but should be revised into submechanisms; see `mechanism_revision.md`.",
        f"7. Primary failure mode: `{interaction['interpretation']}`.",
        "8. Strongest counterexample: worse deficit-ordered states can remain shield-SAFE because the unchanged 18.0 shield tracks mean-welfare deficit and omits spread, mass, and forward dynamics.",
        "",
        "## Interpretation",
        "",
        "This experiment does not repair the abstraction. It maps whether removing one structural mechanism at a time explains the dangerous false-safe error of the existing 18.0/18.1 shield. Negative or weak CI values mean that removing the mechanism did not reduce the original false-safe failure on this diagnostic grid.",
        "A CI from an ablation marked `severe_semantic_shift` is not counted as evidence for H0; it means the mechanism is semantically indispensable under this implementation.",
    ])
    return "\n".join(lines) + "\n"


def parse_list(s):
    return [x.strip() for x in s.split(",") if x.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=str, default="9600,9601,9602,9603,9604,9605,9606,9607")
    parser.add_argument("--worlds", type=str, default=",".join(base.WORLDS))
    parser.add_argument("--policies", type=str, default=",".join(base.POLICIES))
    parser.add_argument("--witness-pairs", type=int, default=90000)
    parser.add_argument("--max-witness-states", type=int, default=2400)
    args = parser.parse_args()
    args.seeds = [int(x) for x in parse_list(args.seeds)]
    args.worlds = parse_list(args.worlds)
    args.policies = parse_list(args.policies)

    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260629)
    summaries = {}
    all_witnesses = []

    for run_name in ["baseline", "MB1", "MB2", "MB3", "MB4", "MB5"]:
        print(f"[run] {run_name}", flush=True)
        states = harvest_states(RUN_CLASSES[run_name], args.worlds, args.policies, args.seeds)
        augment_labels(run_name, states)
        summary = summarize_run(run_name, states)
        ws = witness_search(
            run_name,
            states,
            rng,
            max_states=args.max_witness_states,
            max_pairs=args.witness_pairs,
        )
        summary["monotonicity_witness_count"] = ws["witness_count"]
        summary["witness_type_counts"] = ws["witness_type_counts"]
        summary["minimal_counterexample_count"] = ws["minimal_counterexample_count"]
        summary["transition_witness_examples"] = ws["examples"][:8]
        all_witnesses.extend(ws["examples"])
        summaries[run_name] = summary
        write_json(OUT / f"{run_name}_summary.json", summary)

    baseline = summaries["baseline"]
    for name in ["MB1", "MB2", "MB3", "MB4", "MB5"]:
        delta = semantic_delta(summaries[name], baseline)
        summaries[name]["semantic_delta_vs_baseline"] = delta
        summaries[name]["semantic_validity"] = assess_semantic_validity(delta)
        write_json(OUT / f"{name}_summary.json", summaries[name])
    baseline["semantic_validity"] = "baseline"
    write_json(OUT / "baseline_summary.json", baseline)

    comparison_rows = [flatten_summary(summaries[k]) for k in ["baseline", "MB1", "MB2", "MB3", "MB4", "MB5"]]
    write_csv(OUT / "ablation_comparison.csv", comparison_rows)

    contrib = contribution_rows(summaries)
    write_csv(OUT / "contribution_index.csv", contrib)
    decision_case, top, interaction = decide(contrib, summaries)
    write_json(OUT / "interaction_assessment.json", interaction)
    write_json(OUT / "final_decision.json", {
        "classification": decision_case,
        "top_mechanism": top,
        "dominance_ratio": interaction["dominance_ratio"],
        "largest_positive_CI": interaction["largest_positive_CI"],
        "material_single_ablation_count": interaction["material_single_ablation_count"],
        "interpretation": interaction["interpretation"],
        "outputs": str(OUT),
    })

    witness_fields = [
        "run", "type", "worse_world", "worse_policy", "worse_seed", "worse_step",
        "worse_mean_welfare", "worse_min_zone_welfare", "worse_spread_count",
        "worse_total_mass", "worse_shield_label", "worse_future_collapse",
        "worse_current_collapse", "better_world", "better_policy", "better_seed",
        "better_step", "better_mean_welfare", "better_min_zone_welfare",
        "better_spread_count", "better_total_mass", "better_shield_label",
        "better_future_collapse", "better_current_collapse",
    ]
    write_csv(OUT / "monotonicity_witnesses.csv", all_witnesses, witness_fields)
    (OUT / "transition_counterexamples.md").write_text(make_transition_counterexamples(all_witnesses))
    (OUT / "mechanism_revision.md").write_text(make_mechanism_revision(summaries, decision_case))
    (OUT / "implementation_notes.md").write_text(make_notes(args))
    (OUT / "final_report.md").write_text(make_final_report(summaries, contrib, decision_case, top, interaction))

    print(json.dumps({
        "classification": decision_case,
        "top_mechanism": top,
        "dominance_ratio": interaction["dominance_ratio"],
        "baseline_false_safe_rate": summaries["baseline"]["false_safe_rate"],
        "outputs": str(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
