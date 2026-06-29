#!/usr/bin/env python3
"""BA3.E1 MB5 surrogate replacement test.

Experiment-local Justitia subclasses/wrappers only. The real collapse predicate,
18.0 shield abstraction, and shield thresholds are reused from BA1.E1.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
BA1_SCRIPT = Path("/home/master/llm_projects/ascesis/experiments/BA1_E1_monotonicity_breakers/scripts/run_ablation_map.py")
BA1_OUT = Path("/home/master/llm_projects/ascesis/experiments/BA1_E1_monotonicity_breakers/outputs")
BA2_OUT = Path("/home/master/llm_projects/ascesis/experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs")

spec = importlib.util.spec_from_file_location("ba1_ablation", BA1_SCRIPT)
ba1 = importlib.util.module_from_spec(spec)
sys.modules["ba1_ablation"] = ba1
spec.loader.exec_module(ba1)
base = ba1.base

RUNS = [
    "baseline",
    "MB5_removal",
    "S1_absolute_deficit",
    "S2_threshold_boolean",
    "S3_conservative_upper_bound",
    "S4a_policy_visible_concentration",
    "S4b_reporting_ratios",
    "S4c_projection_resource_hhi",
    "S4d_capture_components",
]


class S1AbsoluteDeficit(base.EvolvableStrategyModel):
    """Replace HHI-like concentration with absolute harmful mass/volume pressure."""

    def _resource_hhi_zone(self, z):
        exploit_mass = sum(l.mass for l in z.lineages if self._exploit_score(l) > 0.42)
        harmful_volume = z.neighbor_harm_volume + z.aid_interception_volume + z.extraction_volume
        mass_deficit = max(0.0, 35.0 / base.ZONES - self._zone_mass(z))
        return base.clamp((exploit_mass + 6.0 * harmful_volume + 4.0 * mass_deficit) / 120.0)

    def _apparent_cooperation(self, z):
        coop_abs = sum(l.mass * l.strategy["cooperation_investment"] for l in z.lineages)
        prod_abs = sum(l.mass * l.strategy["productive_contribution"] for l in z.lineages)
        harm_abs = sum(l.mass * (l.strategy["extraction_rate"] + l.strategy["neighbor_harm_rate"]) for l in z.lineages)
        return base.clamp((0.55 * coop_abs + 0.45 * prod_abs - 0.20 * harm_abs) / 60.0)


class S2ThresholdBoolean(base.EvolvableStrategyModel):
    """Replace relative concentration by coarse monotone-ish threshold flags."""

    def _resource_hhi_zone(self, z):
        harmful_mass = sum(l.mass for l in z.lineages if self._exploit_score(l) > 0.42)
        high_extract = any(l.strategy["extraction_rate"] > 0.62 for l in z.lineages)
        high_intercept = any(l.strategy["aid_interception_rate"] > 0.62 for l in z.lineages)
        high_harm = any(l.strategy["neighbor_harm_rate"] > 0.55 for l in z.lineages)
        low_mass = self._zone_mass(z) < 35.0 / base.ZONES
        failed_zone = min(z.wellness, z.productivity, z.recovery) < 0.20
        score = sum([harmful_mass > 12.0, high_extract, high_intercept, high_harm, low_mass, failed_zone]) / 6.0
        return base.clamp(score)

    def _apparent_cooperation(self, z):
        good = any(
            l.strategy["cooperation_investment"] > 0.60
            and l.strategy["productive_contribution"] > 0.50
            for l in z.lineages
        )
        bad = any(self._exploit_score(l) > 0.55 for l in z.lineages)
        return 0.75 if good and not bad else 0.35 if good else 0.10


class S3ConservativeUpperBound(base.EvolvableStrategyModel):
    """Replace ratio observables by conservative absolute upper-bound risk."""

    def _resource_hhi_zone(self, z):
        if not z.lineages:
            return 1.0
        max_exploit = max(self._exploit_score(l) for l in z.lineages)
        max_harm = max(
            l.strategy["neighbor_harm_rate"] + l.strategy["aid_interception_rate"] + l.strategy["extraction_rate"]
            for l in z.lineages
        ) / 3.0
        low_welfare = max(0.0, 0.55 - min(z.wellness, z.productivity, z.recovery)) / 0.55
        low_mass = max(0.0, 35.0 / base.ZONES - self._zone_mass(z)) / (35.0 / base.ZONES)
        return base.clamp(max(max_exploit, max_harm, low_welfare, low_mass))

    def _apparent_cooperation(self, z):
        best_coop = max((self._cooperative_score(l) for l in z.lineages), default=0.0)
        worst_exploit = max((self._exploit_score(l) for l in z.lineages), default=0.0)
        return base.clamp(best_coop - 0.35 * worst_exploit)


class S4aPolicyVisibleConcentration(base.EvolvableStrategyModel):
    """Neutralize only policy-visible Obs.resource_concentration."""

    def _observe(self, step):
        obs = super()._observe(step)
        return base.Obs(
            step=obs.step,
            wellness=obs.wellness,
            productivity=obs.productivity,
            recovery=obs.recovery,
            migration_capacity=obs.migration_capacity,
            strategy_diversity=obs.strategy_diversity,
            response_diversity=obs.response_diversity,
            resource_concentration=tuple(1.0 / base.ZONES for _ in obs.resource_concentration),
            apparent_cooperation=obs.apparent_cooperation,
            sag=obs.sag,
            last_aid=obs.last_aid,
            response_to_aid=obs.response_to_aid,
            neighbor_delta=obs.neighbor_delta,
            global_welfare=obs.global_welfare,
        )


class S4bReportingRatios(base.EvolvableStrategyModel):
    """Neutralize final/reporting ratio fields; transition behavior is unchanged."""

    def _trajectory_snapshot(self, step, containment_events_this_step):
        snap = super()._trajectory_snapshot(step, containment_events_this_step)
        snap["resource_hhi"] = 1.0 / base.ZONES
        snap["capture_index"] = 0.0
        snap["exploitative_strategy_mass"] = 0.0
        snap["cooperative_strategy_mass"] = 0.0
        return snap

    def metrics(self):
        out = super().metrics()
        for k in [
            "resource_hhi",
            "max_lineage_share",
            "exploitative_strategy_mass",
            "cooperative_strategy_mass",
            "capture_index",
            "capture_component_resource_concentration",
            "capture_component_exploit_mass",
            "capture_component_neighbor_harm",
            "capture_component_aid_interception",
            "capture_component_coop_loss",
        ]:
            out[k] = 0.0
        return out


class S4dCaptureComponents(base.EvolvableStrategyModel):
    """Replace capture-index ratio components in reporting with monotone deficits."""

    def _trajectory_snapshot(self, step, containment_events_this_step):
        snap = super()._trajectory_snapshot(step, containment_events_this_step)
        zw = list(snap["zone_welfare"])
        zm = list(snap["zone_mass"])
        welfare_deficit = base.clamp((0.55 - statistics.fmean(zw)) / 0.55)
        spread_risk = sum(1 for w in zw if w < 0.20) / base.ZONES
        mass_deficit = base.clamp((35.0 - sum(zm)) / 35.0)
        snap["capture_index"] = base.clamp(0.45 * welfare_deficit + 0.35 * spread_risk + 0.20 * mass_deficit)
        return snap

    def metrics(self):
        out = super().metrics()
        out["capture_index"] = base.clamp(
            0.55 * base.clamp((0.55 - out["welfare"]) / 0.55)
            + 0.25 * base.clamp((0.20 - out["minimum_zone_welfare"]) / 0.20)
            + 0.20 * out["collapse"]
        )
        return out


SURROGATE_CLASSES = {
    "S1_absolute_deficit": S1AbsoluteDeficit,
    "S2_threshold_boolean": S2ThresholdBoolean,
    "S3_conservative_upper_bound": S3ConservativeUpperBound,
    "S4a_policy_visible_concentration": S4aPolicyVisibleConcentration,
    "S4b_reporting_ratios": S4bReportingRatios,
    "S4d_capture_components": S4dCaptureComponents,
}


STATIC_COST = {
    "baseline": 0.3908,
    "MB5_removal": 0.1200,
    "S1_absolute_deficit": 0.2400,
    "S2_threshold_boolean": 0.1800,
    "S3_conservative_upper_bound": 0.2600,
    "S4a_policy_visible_concentration": 0.2200,
    "S4b_reporting_ratios": 0.1000,
    "S4c_projection_resource_hhi": 0.0800,
    "S4d_capture_components": 0.1600,
}


def parse_list(s):
    return [x.strip() for x in s.split(",") if x.strip()]


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def write_csv(path, rows, fieldnames=None):
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for k in row:
                if k not in fieldnames:
                    fieldnames.append(k)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def copy_baseline_summaries():
    baseline = read_json(BA1_OUT / "baseline_summary.json")
    mb5 = read_json(BA1_OUT / "MB5_summary.json")
    mb5["run"] = "MB5_removal"
    return baseline, mb5


def semantic_validity(summary, baseline):
    reasons = []
    if abs(summary["future_collapse_rate"] - baseline["future_collapse_rate"]) > 0.35:
        reasons.append("future_collapse_rate_delta_gt_0.35")
    if abs(summary["shield_acceptance_rate"] - baseline["shield_acceptance_rate"]) > 0.45:
        reasons.append("shield_acceptance_rate_delta_gt_0.45")
    if abs(summary["mean_welfare_mean"] - baseline["mean_welfare_mean"]) > 0.25:
        reasons.append("mean_welfare_delta_gt_0.25")
    if summary["future_collapse_rate"] <= 1e-12 or summary["current_collapse_rate"] <= 1e-12:
        reasons.append("collapse_disappears")
    per_policy = summary.get("per_policy", {})
    if per_policy:
        all_safe = all(v["n_safe"] == v["n"] for v in per_policy.values())
        all_doomed = all(v["n_safe"] == 0 for v in per_policy.values())
        if all_safe:
            reasons.append("all_policies_trivially_safe")
        if all_doomed:
            reasons.append("all_policies_trivially_doomed")
    return {
        "semantic_validity": "severe_semantic_shift" if reasons else "valid",
        "semantic_validity_reasons": reasons,
    }


def confusion_stats(summary):
    safe = summary["n_safe"]
    doomed = summary["n_doomed"]
    n = summary["n_states"]
    false_safe = summary["false_safe_rate"] * safe
    false_unsafe = summary["false_unsafe_rate"] * doomed
    tp = doomed - false_unsafe
    fp = false_unsafe
    fn = false_safe
    tn = safe - false_safe
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    balanced = 0.5 * (recall + specificity)
    accuracy = (tp + tn) / n if n else 0.0
    return {
        "collapse_precision": precision,
        "collapse_recall": recall,
        "collapse_specificity": specificity,
        "balanced_collapse_prediction_quality": balanced,
        "future_collapse_prediction_accuracy": accuracy,
    }


def projection_neutralize(states):
    for s in states:
        s["resource_hhi"] = 1.0 / base.ZONES
    return states


def run_variant(run_name, cls, args):
    states = ba1.harvest_states(cls, args.worlds, args.policies, args.seeds)
    if run_name == "S4c_projection_resource_hhi":
        projection_neutralize(states)
    ba1.augment_labels(run_name, states)
    summary = ba1.summarize_run(run_name, states)
    ws = ba1.witness_search(
        run_name,
        states,
        args.rng,
        max_states=args.max_witness_states,
        max_pairs=args.witness_pairs,
    )
    summary["monotonicity_witness_count"] = ws["witness_count"]
    summary["witness_type_counts"] = ws["witness_type_counts"]
    summary["minimal_counterexample_count"] = ws["minimal_counterexample_count"]
    summary["transition_witness_examples"] = ws["examples"][:8]
    return summary, ws["examples"]


def add_derived(summary, baseline):
    validity = semantic_validity(summary, baseline)
    summary.update(validity)
    summary.update(confusion_stats(summary))
    delta = {
        "future_collapse_rate_delta": summary["future_collapse_rate"] - baseline["future_collapse_rate"],
        "shield_acceptance_rate_delta": summary["shield_acceptance_rate"] - baseline["shield_acceptance_rate"],
        "mean_welfare_delta": summary["mean_welfare_mean"] - baseline["mean_welfare_mean"],
    }
    summary["semantic_delta_vs_baseline"] = delta
    return summary


def structural_cost(summary, baseline):
    witness_norm = summary["monotonicity_witness_count"] / max(1, baseline["monotonicity_witness_count"])
    cx_norm = summary["minimal_counterexample_count"] / max(1, baseline["minimal_counterexample_count"])
    isolation = 1.0 if summary["semantic_validity"] == "severe_semantic_shift" else 0.0
    return 0.50 * STATIC_COST[summary["run"]] + 0.35 * witness_norm + 0.10 * cx_norm + 0.05 * isolation


def semantic_quality(summary, baseline):
    c = confusion_stats(summary)
    bc = confusion_stats(baseline)
    penalty = (
        0.35 * max(0.0, summary["false_safe_rate"] - baseline["false_safe_rate"])
        + 0.10 * max(0.0, summary["pure_blindness"]["rate"] - baseline["pure_blindness"]["rate"])
        + 0.15 * max(0.0, bc["collapse_recall"] - c["collapse_recall"])
        + 0.15 * max(0.0, bc["balanced_collapse_prediction_quality"] - c["balanced_collapse_prediction_quality"])
        + 0.10 * abs(summary["future_collapse_rate"] - baseline["future_collapse_rate"])
        + 0.05 * abs(summary["current_collapse_rate"] - baseline["current_collapse_rate"])
        + 0.10 * sum(
            abs(summary["collapse_coverage"][k] - baseline["collapse_coverage"][k])
            for k in ["mean_clause", "spread_clause", "mass_clause"]
        ) / 3.0
    )
    return max(0.0, 1.0 - penalty)


def comparison_rows(summaries, baseline):
    rows = []
    for run in RUNS:
        s = summaries[run]
        sc = structural_cost(s, baseline)
        sq = semantic_quality(s, baseline)
        row = {
            "run": run,
            "false_safe_rate": s["false_safe_rate"],
            "false_unsafe_rate": s["false_unsafe_rate"],
            "pure_blindness_rate": s["pure_blindness"]["rate"],
            "future_collapse_rate": s["future_collapse_rate"],
            "current_collapse_rate": s["current_collapse_rate"],
            "collapse_recall": s["collapse_recall"],
            "collapse_precision": s["collapse_precision"],
            "balanced_collapse_prediction_quality": s["balanced_collapse_prediction_quality"],
            "mean_clause_coverage": s["collapse_coverage"]["mean_clause"],
            "spread_clause_coverage": s["collapse_coverage"]["spread_clause"],
            "mass_clause_coverage": s["collapse_coverage"]["mass_clause"],
            "monotonicity_witness_count": s["monotonicity_witness_count"],
            "minimal_counterexample_count": s["minimal_counterexample_count"],
            "structural_cost_proxy": sc,
            "semantic_benefit_proxy": sq,
            "benefit_cost_ratio": sq / sc if sc > 0 else 0.0,
            "semantic_validity": s["semantic_validity"],
            "semantic_validity_reasons": ";".join(s["semantic_validity_reasons"]),
            "false_safe_delta_vs_baseline": s["false_safe_rate"] - baseline["false_safe_rate"],
            "witness_delta_vs_baseline": s["monotonicity_witness_count"] - baseline["monotonicity_witness_count"],
        }
        rows.append(row)
    return rows


def dominance_graph(rows):
    out = []
    for a in rows:
        for b in rows:
            if a["run"] == b["run"]:
                continue
            if (
                a["semantic_benefit_proxy"] >= b["semantic_benefit_proxy"] - 1e-12
                and a["structural_cost_proxy"] <= b["structural_cost_proxy"] + 1e-12
                and (
                    a["semantic_benefit_proxy"] > b["semantic_benefit_proxy"] + 1e-12
                    or a["structural_cost_proxy"] < b["structural_cost_proxy"] - 1e-12
                )
            ):
                out.append({
                    "dominator": a["run"],
                    "dominated": b["run"],
                    "dominator_semantic_benefit_proxy": a["semantic_benefit_proxy"],
                    "dominator_structural_cost_proxy": a["structural_cost_proxy"],
                    "dominated_semantic_benefit_proxy": b["semantic_benefit_proxy"],
                    "dominated_structural_cost_proxy": b["structural_cost_proxy"],
                    "dominator_valid": int(a["semantic_validity"] == "valid"),
                    "dominated_valid": int(b["semantic_validity"] == "valid"),
                })
    return out


def pareto_frontier(rows):
    valid = [r for r in rows if r["semantic_validity"] == "valid"]
    frontier = []
    for b in valid:
        dominated = False
        for a in valid:
            if a["run"] == b["run"]:
                continue
            if (
                a["semantic_benefit_proxy"] >= b["semantic_benefit_proxy"] - 1e-12
                and a["structural_cost_proxy"] <= b["structural_cost_proxy"] + 1e-12
                and (
                    a["semantic_benefit_proxy"] > b["semantic_benefit_proxy"] + 1e-12
                    or a["structural_cost_proxy"] < b["structural_cost_proxy"] - 1e-12
                )
            ):
                dominated = True
                break
        if not dominated:
            frontier.append(b)
    return sorted(frontier, key=lambda r: (-r["semantic_benefit_proxy"], r["structural_cost_proxy"]))


def classify(rows, baseline):
    baseline_row = next(r for r in rows if r["run"] == "baseline")
    valid_surrogates = [r for r in rows if r["run"].startswith("S") and r["semantic_validity"] == "valid"]
    transition_surrogates = [r for r in valid_surrogates if r["run"] in {
        "S1_absolute_deficit",
        "S2_threshold_boolean",
        "S3_conservative_upper_bound",
        "S4a_policy_visible_concentration",
    }]
    reporting_projection_surrogates = [r for r in valid_surrogates if r["run"] in {
        "S4b_reporting_ratios",
        "S4c_projection_resource_hhi",
        "S4d_capture_components",
    }]
    transition_success = [
        r for r in transition_surrogates
        if r["false_safe_rate"] <= baseline["false_safe_rate"] + 0.01
        and r["pure_blindness_rate"] <= baseline["pure_blindness"]["rate"] + 0.02
        and (
            r["structural_cost_proxy"] < baseline_row["structural_cost_proxy"]
            or r["monotonicity_witness_count"] < baseline["monotonicity_witness_count"]
        )
    ]
    fidelity_useful_but_costly = [
        r for r in transition_surrogates
        if r["false_safe_rate"] <= baseline["false_safe_rate"] + 0.01
        and r["pure_blindness_rate"] <= baseline["pure_blindness"]["rate"] + 0.02
        and r not in transition_success
    ]
    non_transition_overhead = [
        r for r in reporting_projection_surrogates
        if r["false_safe_rate"] <= baseline["false_safe_rate"] + 0.01
        and r["pure_blindness_rate"] <= baseline["pure_blindness"]["rate"] + 0.02
        and r["structural_cost_proxy"] < baseline_row["structural_cost_proxy"]
    ]
    invalid = [r for r in rows if r["run"].startswith("S") and r["semantic_validity"] != "valid"]
    full_failures = [
        r for r in transition_surrogates
        if r["false_safe_rate"] > baseline["false_safe_rate"] + 0.01
        or r["pure_blindness_rate"] > baseline["pure_blindness"]["rate"] + 0.02
    ]

    if transition_success:
        decision = "MB5_representational_overhead"
    elif non_transition_overhead and (fidelity_useful_but_costly or full_failures):
        decision = "MB5_functionally_split"
    elif valid_surrogates and len(full_failures) == len(transition_surrogates) and not non_transition_overhead:
        decision = "MB5_necessary"
    else:
        decision = "Inconclusive"

    best_false_safe = min(valid_surrogates, key=lambda r: r["false_safe_rate"]) if valid_surrogates else None
    best_ratio = max(valid_surrogates, key=lambda r: r["benefit_cost_ratio"]) if valid_surrogates else None
    best_transition_ratio = max(transition_surrogates, key=lambda r: r["benefit_cost_ratio"]) if transition_surrogates else None
    reduce_witness = [r["run"] for r in valid_surrogates if r["monotonicity_witness_count"] < baseline["monotonicity_witness_count"]]
    return {
        "decision": decision,
        "successful_surrogates": [r["run"] for r in transition_success],
        "successful_transition_surrogates": [r["run"] for r in transition_success],
        "successful_subfamily_replacements": [r["run"] for r in non_transition_overhead],
        "fidelity_useful_but_costly_transition_surrogates": [r["run"] for r in fidelity_useful_but_costly],
        "failed_transition_surrogates": [r["run"] for r in full_failures],
        "invalid_surrogates": [r["run"] for r in invalid],
        "best_false_safe_surrogate": best_false_safe["run"] if best_false_safe else None,
        "best_false_safe_rate": best_false_safe["false_safe_rate"] if best_false_safe else None,
        "best_benefit_cost_surrogate": best_ratio["run"] if best_ratio else None,
        "best_benefit_cost_ratio": best_ratio["benefit_cost_ratio"] if best_ratio else None,
        "best_transition_benefit_cost_surrogate": best_transition_ratio["run"] if best_transition_ratio else None,
        "best_transition_benefit_cost_ratio": best_transition_ratio["benefit_cost_ratio"] if best_transition_ratio else None,
        "surrogates_reducing_witness_count": reduce_witness,
        "strongest_counterexample_against_H1": full_failures[0]["run"] if full_failures else "no_valid_transition_failure",
        "strongest_counterexample_against_H0": non_transition_overhead[0]["run"] if non_transition_overhead else (transition_success[0]["run"] if transition_success else None),
    }


def make_counterexamples(rows, assessment):
    lines = [
        "# BA3.E1 Counterexamples",
        "",
        "## Against H1: MB5 Representational Overhead",
        "",
    ]
    failures = [
        r for r in rows
        if r["run"].startswith("S") and r["semantic_validity"] == "valid"
        and r["false_safe_rate"] > next(x for x in rows if x["run"] == "baseline")["false_safe_rate"] + 0.01
    ]
    if failures:
        for r in failures:
            lines.append(f"- `{r['run']}` worsens false-safe to `{r['false_safe_rate']:.4f}` while baseline is `{next(x for x in rows if x['run'] == 'baseline')['false_safe_rate']:.4f}`.")
    else:
        lines.append("- No valid surrogate worsened false-safe beyond the materiality band.")
    lines.extend(["", "## Against H0: MB5 Necessary", ""])
    successes = [r for r in rows if r["run"] in assessment["successful_transition_surrogates"]]
    subfamily = [r for r in rows if r["run"] in assessment["successful_subfamily_replacements"]]
    if successes:
        for r in successes:
            lines.append(f"- `{r['run']}` is a transition-level surrogate that matches/improves false-safe and reduces structural cost or witness count.")
    elif subfamily:
        for r in subfamily:
            lines.append(f"- `{r['run']}` is a subfamily replacement that preserves fidelity with lower structural cost; it is not a full transition-level replacement.")
    else:
        lines.append("- No valid surrogate fully passed the success gate.")
    return "\n".join(lines) + "\n"


def make_split_assessment(rows):
    lines = [
        "# BA3.E1 Mechanism Split Assessment",
        "",
        "MB5 is not a single clean implementation mechanism.",
        "",
        "| subfamily | run | interpretation |",
        "|---|---|---|",
    ]
    interpretations = {
        "S4a_policy_visible_concentration": "policy-visible concentration can be isolated via `Obs.resource_concentration`; compare false-safe and witness deltas.",
        "S4b_reporting_ratios": "reporting ratios affect diagnostics/output only; success here is not transition-level evidence.",
        "S4c_projection_resource_hhi": "18.0 projection-visible `resource_hhi`; expected weak effect because current doomed set is U-only.",
        "S4d_capture_components": "capture-index components are reporting/diagnostic unless fed into a policy.",
    }
    by_run = {r["run"]: r for r in rows}
    for run, text in interpretations.items():
        r = by_run[run]
        lines.append(f"| {run[0:3]} | `{run}` | {text} Observed false-safe `{r['false_safe_rate']:.4f}`, witnesses `{r['monotonicity_witness_count']}`. |")
    lines.extend([
        "",
        "Split verdict: policy-visible and projection/reporting roles should be kept separate in future taxonomy. A reporting-only win is not evidence that transition-level MB5 is safe to remove.",
    ])
    return "\n".join(lines) + "\n"


def make_notes(args):
    return "\n".join([
        "# BA3.E1 Implementation Notes",
        "",
        "- Justitia source files were not modified.",
        "- BA1 baseline and BA1 MB5 removal summaries were reused exactly and copied into BA3 outputs.",
        "- New surrogate variants were run on the BA1 diagnostic grid unless otherwise noted.",
        f"- Worlds: `{args.worlds}`.",
        f"- Policies: `{args.policies}`.",
        f"- Seeds: `{args.seeds}`.",
        "- 18.0 shield parameters/projection are reused from BA1.",
        "- `S4c_projection_resource_hhi` is implemented as a harness-side projection wrapper, not a Justitia transition subclass.",
        "",
        "## Wrapper Functions",
        "",
        "- S1/S2/S3 override `_resource_hhi_zone` and `_apparent_cooperation`.",
        "- S4a overrides `_observe` only.",
        "- S4b overrides `_trajectory_snapshot` and `metrics` only.",
        "- S4d overrides capture-index reporting in `_trajectory_snapshot` and `metrics`.",
    ]) + "\n"


def make_report(rows, assessment, frontier):
    lines = [
        "# BA3.E1 MB5 Surrogate Replacement Test",
        "",
        f"**Decision:** `{assessment['decision']}`.",
        f"**Successful transition surrogates:** `{assessment['successful_transition_surrogates']}`.",
        f"**Successful subfamily replacements:** `{assessment['successful_subfamily_replacements']}`.",
        f"**Best false-safe surrogate:** `{assessment['best_false_safe_surrogate']}` = `{assessment['best_false_safe_rate']}`.",
        f"**Best benefit/cost surrogate:** `{assessment['best_benefit_cost_surrogate']}` = `{assessment['best_benefit_cost_ratio']}`.",
        f"**Best transition benefit/cost surrogate:** `{assessment['best_transition_benefit_cost_surrogate']}` = `{assessment['best_transition_benefit_cost_ratio']}`.",
        "",
        "## Summary",
        "",
        "| run | false-safe | pure blindness | future collapse | witnesses | cost | benefit | ratio | validity |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['run']} | {r['false_safe_rate']:.4f} | {r['pure_blindness_rate']:.4f} | "
            f"{r['future_collapse_rate']:.4f} | {r['monotonicity_witness_count']} | "
            f"{r['structural_cost_proxy']:.4f} | {r['semantic_benefit_proxy']:.4f} | "
            f"{r['benefit_cost_ratio']:.4f} | {r['semantic_validity']} |"
        )
    lines.extend([
        "",
        "## Required Questions",
        "",
        f"1. Can MB5 be replaced by any valid surrogate? Full transition-level replacement: `{bool(assessment['successful_transition_surrogates'])}`; subfamily replacement: `{bool(assessment['successful_subfamily_replacements'])}`.",
        f"2. Best false-safe behavior: `{assessment['best_false_safe_surrogate']}`.",
        f"3. Best benefit/cost ratio: `{assessment['best_benefit_cost_surrogate']}` overall; `{assessment['best_transition_benefit_cost_surrogate']}` among transition-level surrogates.",
        f"4. Surrogates reducing witness count: `{assessment['surrogates_reducing_witness_count']}`.",
        "5. Collapse distribution preservation is reported in `semantic_validity.csv`; severe shifts are excluded from success.",
        f"6. MB5 status: `{assessment['decision']}`.",
        "7. Most suspicious subfamily: projection/reporting `resource_hhi` if it changes little while retaining structural cost.",
        "8. Indispensable subfamily: any S4 variant whose replacement worsens false-safe materially; see `surrogate_comparison.csv`.",
        f"9. Strongest counterexample against H1: `{assessment['strongest_counterexample_against_H1']}`.",
        f"10. Strongest counterexample against H0: `{assessment['strongest_counterexample_against_H0']}`.",
        "",
        "## Interpretation",
        "",
        "A transition-level surrogate is counted as successful only if it is semantically valid, matches or improves baseline false-safe within the materiality band, does not materially increase pure blindness, and reduces structural cost or monotonicity witnesses. Reporting/projection-only variants are counted only as subfamily replacements, not as full MB5 replacements.",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="9600,9601,9602,9603,9604,9605,9606,9607")
    parser.add_argument("--worlds", default=",".join(base.WORLDS))
    parser.add_argument("--policies", default=",".join(base.POLICIES))
    parser.add_argument("--witness-pairs", type=int, default=90000)
    parser.add_argument("--max-witness-states", type=int, default=2400)
    args = parser.parse_args()
    args.seeds = [int(x) for x in parse_list(args.seeds)]
    args.worlds = parse_list(args.worlds)
    args.policies = parse_list(args.policies)
    args.rng = ba1.random.Random(20260630)
    OUT.mkdir(parents=True, exist_ok=True)

    baseline, mb5 = copy_baseline_summaries()
    baseline["run"] = "baseline"
    summaries = {
        "baseline": add_derived(baseline, baseline),
        "MB5_removal": add_derived(mb5, baseline),
    }
    all_witnesses = []

    for run_name, cls in SURROGATE_CLASSES.items():
        print(f"[run] {run_name}", flush=True)
        summary, witnesses = run_variant(run_name, cls, args)
        summaries[run_name] = add_derived(summary, baseline)
        all_witnesses.extend(witnesses)

    print("[run] S4c_projection_resource_hhi", flush=True)
    s4c_summary, s4c_witnesses = run_variant("S4c_projection_resource_hhi", base.EvolvableStrategyModel, args)
    summaries["S4c_projection_resource_hhi"] = add_derived(s4c_summary, baseline)
    all_witnesses.extend(s4c_witnesses)

    for run in RUNS:
        name = "MB5_removal_summary.json" if run == "MB5_removal" else f"{run}_summary.json"
        write_json(OUT / name, summaries[run])

    rows = comparison_rows(summaries, baseline)
    dominance = dominance_graph(rows)
    frontier = pareto_frontier(rows)
    assessment = classify(rows, baseline)

    write_csv(OUT / "surrogate_comparison.csv", rows)
    write_csv(OUT / "semantic_validity.csv", [
        {
            "run": r["run"],
            "semantic_validity": r["semantic_validity"],
            "reasons": r["semantic_validity_reasons"],
            "future_collapse_rate": r["future_collapse_rate"],
            "current_collapse_rate": r["current_collapse_rate"],
            "false_safe_rate": r["false_safe_rate"],
        }
        for r in rows
    ])
    write_csv(OUT / "benefit_cost_surrogate_plane.csv", [
        {
            "run": r["run"],
            "semantic_benefit_proxy": r["semantic_benefit_proxy"],
            "structural_cost_proxy": r["structural_cost_proxy"],
            "benefit_cost_ratio": r["benefit_cost_ratio"],
            "semantic_validity": r["semantic_validity"],
        }
        for r in rows
    ])
    write_csv(OUT / "dominance_graph.csv", dominance)
    write_csv(OUT / "pareto_frontier.csv", frontier)
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
    (OUT / "counterexamples.md").write_text(make_counterexamples(rows, assessment))
    (OUT / "mechanism_split_assessment.md").write_text(make_split_assessment(rows))
    write_json(OUT / "hypothesis_assessment.json", assessment)
    (OUT / "implementation_notes.md").write_text(make_notes(args))
    (OUT / "final_report.md").write_text(make_report(rows, assessment, frontier))

    print(json.dumps({**assessment, "outputs": str(OUT)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
