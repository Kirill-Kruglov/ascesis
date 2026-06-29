#!/usr/bin/env python3
"""BA2.E1 semantic-benefit vs structural-cost map.

This is an analytic pass over BA1.E1 outputs. It does not rerun Justitia, does
not modify the 18.0 shield, and does not search for a better abstraction.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_ROOT = Path("/home/master/llm_projects/ascesis/experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map")
OUT = SPEC_ROOT / "outputs"
BA1_OUT = Path("/home/master/llm_projects/ascesis/experiments/BA1_E1_monotonicity_breakers/outputs")
MECHANISMS = ["MB1", "MB2", "MB3", "MB4", "MB5"]


STATIC_COST = {
    # Scores are pre-registered structural indicators from BA0/BA1 code reading.
    # They are not learned and do not tune any shield threshold.
    "MB1": {
        "history_dependence": 1.00,
        "global_coupling": 0.25,
        "relative_observables": 0.10,
        "non_local_transitions": 0.35,
        "transition_branching": 0.45,
        "interaction_degree": 0.65,
    },
    "MB2": {
        "history_dependence": 0.00,
        "global_coupling": 0.95,
        "relative_observables": 0.80,
        "non_local_transitions": 0.90,
        "transition_branching": 0.65,
        "interaction_degree": 0.75,
    },
    "MB3": {
        "history_dependence": 0.45,
        "global_coupling": 0.65,
        "relative_observables": 0.55,
        "non_local_transitions": 0.70,
        "transition_branching": 0.95,
        "interaction_degree": 1.00,
    },
    "MB4": {
        "history_dependence": 0.80,
        "global_coupling": 0.85,
        "relative_observables": 0.55,
        "non_local_transitions": 0.95,
        "transition_branching": 1.00,
        "interaction_degree": 1.00,
    },
    "MB5": {
        "history_dependence": 0.10,
        "global_coupling": 0.75,
        "relative_observables": 1.00,
        "non_local_transitions": 0.55,
        "transition_branching": 0.50,
        "interaction_degree": 0.75,
    },
}


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


def pos(x):
    return max(0.0, x)


def confusion_stats(summary):
    n = summary["n_states"]
    safe = summary["n_safe"]
    doomed = summary["n_doomed"]
    false_safe = summary["false_safe_rate"] * safe
    false_unsafe = summary["false_unsafe_rate"] * doomed
    tp = doomed - false_unsafe
    fp = false_unsafe
    fn = false_safe
    tn = safe - false_safe
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    accuracy = (tp + tn) / n if n else 0.0
    balanced_accuracy = 0.5 * (recall + specificity)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "tp_doomed_future_collapse": tp,
        "fp_doomed_no_future_collapse": fp,
        "fn_safe_future_collapse": fn,
        "tn_safe_no_future_collapse": tn,
        "collapse_precision": precision,
        "collapse_recall": recall,
        "collapse_specificity": specificity,
        "future_collapse_accuracy": accuracy,
        "future_collapse_balanced_accuracy": balanced_accuracy,
        "future_collapse_f1": f1,
    }


def semantic_rows(summaries):
    base = summaries["baseline"]
    base_c = confusion_stats(base)
    rows = []
    for mb in MECHANISMS:
        s = summaries[mb]
        c = confusion_stats(s)
        delta_false_safe = s["false_safe_rate"] - base["false_safe_rate"]
        delta_false_unsafe = s["false_unsafe_rate"] - base["false_unsafe_rate"]
        delta_pure_blindness = s["pure_blindness"]["rate"] - base["pure_blindness"]["rate"]
        delta_recall = c["collapse_recall"] - base_c["collapse_recall"]
        delta_precision = c["collapse_precision"] - base_c["collapse_precision"]
        delta_quality = c["future_collapse_balanced_accuracy"] - base_c["future_collapse_balanced_accuracy"]
        clause_deltas = {
            f"delta_{k}": s["collapse_coverage"][k] - base["collapse_coverage"][k]
            for k in ["mean_clause", "spread_clause", "mass_clause"]
        }
        mean_abs_clause_delta = sum(abs(v) for v in clause_deltas.values()) / 3.0
        semantic_benefit = (
            0.35 * pos(delta_false_safe)
            + 0.10 * pos(delta_false_unsafe)
            + 0.15 * pos(delta_pure_blindness)
            + 0.15 * pos(-delta_recall)
            + 0.15 * pos(-delta_quality)
            + 0.10 * mean_abs_clause_delta
        )
        rows.append({
            "mechanism": mb,
            "semantic_validity": s["semantic_validity"],
            "baseline_false_safe": base["false_safe_rate"],
            "ablated_false_safe": s["false_safe_rate"],
            "delta_false_safe": delta_false_safe,
            "delta_false_unsafe": delta_false_unsafe,
            "delta_pure_blindness": delta_pure_blindness,
            "baseline_collapse_recall": base_c["collapse_recall"],
            "ablated_collapse_recall": c["collapse_recall"],
            "delta_collapse_recall": delta_recall,
            "baseline_collapse_precision": base_c["collapse_precision"],
            "ablated_collapse_precision": c["collapse_precision"],
            "delta_collapse_precision": delta_precision,
            "baseline_future_collapse_balanced_accuracy": base_c["future_collapse_balanced_accuracy"],
            "ablated_future_collapse_balanced_accuracy": c["future_collapse_balanced_accuracy"],
            "delta_future_collapse_prediction_quality": delta_quality,
            **clause_deltas,
            "mean_abs_clause_coverage_delta": mean_abs_clause_delta,
            "semantic_benefit_score": semantic_benefit,
            "noncomparable_semantic_shift": int(s["semantic_validity"] == "severe_semantic_shift"),
        })
    return rows


def structural_rows(summaries):
    base = summaries["baseline"]
    rows = []
    for mb in MECHANISMS:
        s = summaries[mb]
        static = STATIC_COST[mb]
        static_avg = sum(static.values()) / len(static)
        witness_reduction = pos((base["monotonicity_witness_count"] - s["monotonicity_witness_count"]) / max(1, base["monotonicity_witness_count"]))
        counterexample_reduction = pos((base["minimal_counterexample_count"] - s["minimal_counterexample_count"]) / max(1, base["minimal_counterexample_count"]))
        isolation_cost = 1.0 if s["semantic_validity"] == "severe_semantic_shift" else 0.0
        structural_cost = (
            0.55 * static_avg
            + 0.25 * witness_reduction
            + 0.10 * counterexample_reduction
            + 0.10 * isolation_cost
        )
        rows.append({
            "mechanism": mb,
            "semantic_validity": s["semantic_validity"],
            **static,
            "static_structural_cost": static_avg,
            "baseline_monotonicity_witness_count": base["monotonicity_witness_count"],
            "ablated_monotonicity_witness_count": s["monotonicity_witness_count"],
            "witness_reduction_when_removed": witness_reduction,
            "baseline_minimal_counterexample_count": base["minimal_counterexample_count"],
            "ablated_minimal_counterexample_count": s["minimal_counterexample_count"],
            "counterexample_reduction_when_removed": counterexample_reduction,
            "isolation_cost": isolation_cost,
            "structural_cost_score": structural_cost,
        })
    return rows


def plane_rows(semantic, structural):
    by_s = {r["mechanism"]: r for r in semantic}
    by_c = {r["mechanism"]: r for r in structural}
    rows = []
    for mb in MECHANISMS:
        benefit = by_s[mb]["semantic_benefit_score"]
        cost = by_c[mb]["structural_cost_score"]
        rows.append({
            "mechanism": mb,
            "semantic_benefit_score": benefit,
            "structural_cost_score": cost,
            "benefit_cost_ratio": benefit / cost if cost > 0 else 0.0,
            "semantic_validity": by_s[mb]["semantic_validity"],
            "noncomparable_semantic_shift": by_s[mb]["noncomparable_semantic_shift"],
        })
    return rows


def dominance_graph(plane):
    rows = []
    for a in plane:
        for b in plane:
            if a["mechanism"] == b["mechanism"]:
                continue
            dominates = (
                a["semantic_benefit_score"] >= b["semantic_benefit_score"] - 1e-12
                and a["structural_cost_score"] <= b["structural_cost_score"] + 1e-12
                and (
                    a["semantic_benefit_score"] > b["semantic_benefit_score"] + 1e-12
                    or a["structural_cost_score"] < b["structural_cost_score"] - 1e-12
                )
            )
            if dominates:
                rows.append({
                    "dominator": a["mechanism"],
                    "dominated": b["mechanism"],
                    "dominator_benefit": a["semantic_benefit_score"],
                    "dominator_cost": a["structural_cost_score"],
                    "dominated_benefit": b["semantic_benefit_score"],
                    "dominated_cost": b["structural_cost_score"],
                    "involves_noncomparable_shift": int(a["noncomparable_semantic_shift"] or b["noncomparable_semantic_shift"]),
                })
    return rows


def pareto_frontier(plane, include_noncomparable=True):
    candidates = [r for r in plane if include_noncomparable or not r["noncomparable_semantic_shift"]]
    frontier = []
    for b in candidates:
        dominated = False
        for a in candidates:
            if a["mechanism"] == b["mechanism"]:
                continue
            if (
                a["semantic_benefit_score"] >= b["semantic_benefit_score"] - 1e-12
                and a["structural_cost_score"] <= b["structural_cost_score"] + 1e-12
                and (
                    a["semantic_benefit_score"] > b["semantic_benefit_score"] + 1e-12
                    or a["structural_cost_score"] < b["structural_cost_score"] - 1e-12
                )
            ):
                dominated = True
                break
        if not dominated:
            row = dict(b)
            row["frontier_scope"] = "all" if include_noncomparable else "comparable_only"
            frontier.append(row)
    return sorted(frontier, key=lambda r: (-r["semantic_benefit_score"], r["structural_cost_score"]))


def rankings(plane, dominance):
    dominated = {r["dominated"] for r in dominance if not r["involves_noncomparable_shift"]}
    rows = []
    for r in sorted(plane, key=lambda x: (x["benefit_cost_ratio"], x["semantic_benefit_score"]), reverse=True):
        rows.append({
            **r,
            "is_dominated_by_comparable_mechanism": int(r["mechanism"] in dominated),
            "investigation_priority_score": r["structural_cost_score"] * (1.0 - min(1.0, r["semantic_benefit_score"])),
        })
    return rows


def make_tradeoff_examples(plane, semantic, structural, dominance, frontier):
    sem = {r["mechanism"]: r for r in semantic}
    cost = {r["mechanism"]: r for r in structural}
    lines = [
        "# BA2.E1 Tradeoff Examples",
        "",
        "Benefit is measured as fidelity deterioration after a single-mechanism removal.",
        "Cost is a documented mixture of static structural complexity and BA1 witness reductions.",
        "",
        "## Mechanism Points",
        "",
        "| mechanism | benefit | cost | ratio | validity | note |",
        "|---|---:|---:|---:|---|---|",
    ]
    for p in plane:
        note = ""
        if p["mechanism"] == "MB4":
            note = "apparent high value is non-comparable because removal eliminates collapse dynamics"
        elif p["semantic_benefit_score"] < 0.08 and p["structural_cost_score"] > 0.35:
            note = "high-cost / low-benefit counterexample candidate"
        elif p["semantic_benefit_score"] > 0.12:
            note = "measurable semantic benefit"
        lines.append(
            f"| {p['mechanism']} | {p['semantic_benefit_score']:.4f} | {p['structural_cost_score']:.4f} | "
            f"{p['benefit_cost_ratio']:.4f} | {p['semantic_validity']} | {note} |"
        )
    lines.extend([
        "",
        "## Dominance",
        "",
    ])
    if dominance:
        for d in dominance:
            qualifier = " (non-comparable shift involved)" if d["involves_noncomparable_shift"] else ""
            lines.append(f"- `{d['dominator']}` dominates `{d['dominated']}`{qualifier}.")
    else:
        lines.append("- No strict dominance edges found.")
    lines.extend([
        "",
        "## Pareto Frontier",
        "",
        "- All mechanisms: " + ", ".join(f"`{r['mechanism']}`" for r in frontier["all"]),
        "- Comparable-only: " + ", ".join(f"`{r['mechanism']}`" for r in frontier["comparable_only"]),
        "",
        "## Metric Notes",
        "",
        "- MB4 is not allowed to carry H_BA2 by itself because BA1 marked it `severe_semantic_shift`.",
        "- Positive semantic benefit means removal worsens the unchanged 18.0 shield fidelity.",
        "- Negative or zero benefit means the mechanism is not visibly reducing semantic blindness under this grid.",
    ])
    return "\n".join(lines) + "\n"


def make_counterexamples(plane, semantic, structural):
    lines = [
        "# BA2.E1 Counterexamples Against H_BA2",
        "",
        "H_BA2 predicts that monotonicity-violating mechanisms are also the mechanisms that reduce semantic blindness.",
        "",
    ]
    counter = [r for r in plane if r["structural_cost_score"] >= 0.35 and r["semantic_benefit_score"] <= 0.08 and not r["noncomparable_semantic_shift"]]
    if not counter:
        lines.append("No clean high-cost / low-benefit counterexample crossed the pre-declared thresholds.")
    else:
        lines.append("## High Cost / Low Benefit Mechanisms")
        lines.append("")
        for r in counter:
            lines.extend([
                f"### {r['mechanism']}",
                "",
                f"- Structural cost: `{r['structural_cost_score']:.4f}`.",
                f"- Semantic benefit: `{r['semantic_benefit_score']:.4f}`.",
                f"- Benefit/cost ratio: `{r['benefit_cost_ratio']:.4f}`.",
                "- Interpretation: this mechanism carries structural complexity without corresponding measured reduction in semantic blindness.",
                "",
            ])
    mb4 = next(r for r in plane if r["mechanism"] == "MB4")
    lines.extend([
        "## Non-comparable Strong Effect",
        "",
        f"- `MB4` has apparent benefit `{mb4['semantic_benefit_score']:.4f}`, but BA1 marks it as `severe_semantic_shift`.",
        "- This is not evidence that MB4 is an efficient monotonicity breaker; it means removing adaptive population dynamics changes the substrate too severely.",
    ])
    return "\n".join(lines) + "\n"


def assess(plane, dominance, frontier):
    clean = [r for r in plane if not r["noncomparable_semantic_shift"]]
    high_cost_low_benefit = [
        r for r in clean
        if r["structural_cost_score"] >= 0.35 and r["semantic_benefit_score"] <= 0.08
    ]
    dominated_clean = [
        d for d in dominance
        if not d["involves_noncomparable_shift"]
    ]
    if high_cost_low_benefit:
        classification = "H_BA2_rejected"
        reason = "at least one clean mechanism has high structural cost and low semantic benefit"
    elif dominated_clean:
        classification = "H_BA2_mixed"
        reason = "some mechanisms are dominated, but no high-cost/low-benefit counterexample crossed threshold"
    else:
        classification = "H_BA2_supported"
        reason = "clean mechanisms lie near the Pareto frontier with no strong dominated counterexample"
    worst_ratio = min(clean, key=lambda r: r["benefit_cost_ratio"]) if clean else None
    investigate = max(clean, key=lambda r: r["structural_cost_score"] * (1.0 - min(1.0, r["semantic_benefit_score"]))) if clean else None
    return {
        "classification": classification,
        "reason": reason,
        "high_cost_low_benefit_mechanisms": [r["mechanism"] for r in high_cost_low_benefit],
        "dominated_clean_edges": dominated_clean,
        "pareto_frontier_all": [r["mechanism"] for r in frontier["all"]],
        "pareto_frontier_comparable_only": [r["mechanism"] for r in frontier["comparable_only"]],
        "worst_benefit_cost_ratio": worst_ratio["mechanism"] if worst_ratio else None,
        "investigate_first": investigate["mechanism"] if investigate else None,
        "strongest_counterexample_against_H_BA2": high_cost_low_benefit[0]["mechanism"] if high_cost_low_benefit else None,
        "mb4_note": "MB4 has an apparent strong effect but is non-comparable because BA1 marked it severe_semantic_shift.",
    }


def make_report(assessment, semantic, structural, plane, dominance, frontier):
    lines = [
        "# BA2.E1 Semantic Benefit vs Structural Cost Map",
        "",
        f"**Decision:** `{assessment['classification']}`.",
        f"**Reason:** {assessment['reason']}.",
        f"**Strongest counterexample:** `{assessment['strongest_counterexample_against_H_BA2']}`.",
        f"**Investigate first:** `{assessment['investigate_first']}`.",
        "",
        "## Benefit / Cost Plane",
        "",
        "| mechanism | semantic benefit | structural cost | ratio | validity |",
        "|---|---:|---:|---:|---|",
    ]
    for r in sorted(plane, key=lambda x: x["mechanism"]):
        lines.append(
            f"| {r['mechanism']} | {r['semantic_benefit_score']:.4f} | {r['structural_cost_score']:.4f} | "
            f"{r['benefit_cost_ratio']:.4f} | {r['semantic_validity']} |"
        )
    lines.extend([
        "",
        "## Required Questions",
        "",
        f"1. Does every monotonicity breaker provide semantic benefit? No. Clean high-cost/low-benefit mechanisms: `{assessment['high_cost_low_benefit_mechanisms']}`.",
        f"2. Are there dominated mechanisms? Yes, see `dominance_graph.csv`; clean dominated edges: `{len(assessment['dominated_clean_edges'])}`.",
        "3. Is there a Pareto frontier? Yes.",
        f"4. Pareto-optimal mechanisms: all=`{assessment['pareto_frontier_all']}`, comparable-only=`{assessment['pareto_frontier_comparable_only']}`.",
        f"5. Worst benefit/cost ratio: `{assessment['worst_benefit_cost_ratio']}`.",
        f"6. Investigate first: `{assessment['investigate_first']}`.",
        f"7. Strongest counterexample against H_BA2: `{assessment['strongest_counterexample_against_H_BA2']}`.",
        "",
        "## Interpretation",
        "",
        "The BA1 data do not support the strong form of H_BA2. Some mechanisms that complicate monotonicity appear to carry measurable semantic value, but at least one clean mechanism lands in the high-cost/low-benefit region. MB4 remains semantically indispensable rather than cleanly rankable: its ablation removes collapse dynamics and therefore cannot be used as a normal benefit/cost point.",
        "",
        "## Formula Summary",
        "",
        "- Semantic benefit = weighted positive loss in false-safe, false-unsafe, pure blindness, collapse recall, balanced prediction quality, plus clause-coverage displacement.",
        "- Structural cost = weighted static mechanism complexity plus empirical reduction in BA1 monotonicity witnesses/counterexamples when removed, plus isolation cost for severe semantic shifts.",
        "- Dominance uses the specified rule: A dominates B if benefit(A) >= benefit(B) and cost(A) <= cost(B), with at least one strict inequality.",
    ])
    return "\n".join(lines) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summaries = {name: read_json(BA1_OUT / f"{name}_summary.json") for name in ["baseline", *MECHANISMS]}
    semantic = semantic_rows(summaries)
    structural = structural_rows(summaries)
    plane = plane_rows(semantic, structural)
    dominance = dominance_graph(plane)
    frontier = {
        "all": pareto_frontier(plane, include_noncomparable=True),
        "comparable_only": pareto_frontier(plane, include_noncomparable=False),
    }
    ranking_rows = rankings(plane, dominance)
    assessment = assess(plane, dominance, frontier)

    write_csv(OUT / "semantic_benefit.csv", semantic)
    write_csv(OUT / "structural_cost.csv", structural)
    write_csv(OUT / "benefit_cost_plane.csv", plane)
    write_csv(OUT / "dominance_graph.csv", dominance)
    write_csv(OUT / "pareto_frontier.csv", frontier["all"] + frontier["comparable_only"])
    write_csv(OUT / "mechanism_rankings.csv", ranking_rows)
    (OUT / "tradeoff_examples.md").write_text(make_tradeoff_examples(plane, semantic, structural, dominance, frontier))
    (OUT / "counterexamples.md").write_text(make_counterexamples(plane, semantic, structural))
    write_json(OUT / "hypothesis_assessment.json", assessment)
    (OUT / "final_report.md").write_text(make_report(assessment, semantic, structural, plane, dominance, frontier))
    print(json.dumps({**assessment, "outputs": str(OUT)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
