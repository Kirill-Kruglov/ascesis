#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from consequence_feature.dag import CausalDAG, generate_dag_grid  # noqa: E402
from consequence_feature.expressions import Expression, generate_expressions  # noqa: E402
from consequence_feature.metrics import class_stats, first_pair_same_key_diff_other  # noqa: E402
from consequence_feature.verifier import consequence_signature, freeze_signature  # noqa: E402


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "(empty)"
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in df.columns:
            value = row[col]
            if pd.isna(value):
                vals.append("")
            elif isinstance(value, float):
                vals.append(f"{value:.6g}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def build_records(seed: int, max_depth: int, num_dags: int, per_depth_cap: int) -> tuple[list[dict[str, Any]], dict[str, CausalDAG]]:
    dags = generate_dag_grid(seed=seed, num_dags=num_dags)
    dag_by_id = {dag.dag_id: dag for dag in dags}
    records: list[dict[str, Any]] = []
    success = 0
    errors = 0
    for dag_idx, dag in enumerate(dags, start=1):
        rng = random.Random(seed + dag_idx * 7919)
        expressions = generate_expressions(dag, max_depth=max_depth, rng=rng, per_depth_cap=per_depth_cap)
        for expr in expressions:
            try:
                sig = consequence_signature(dag, expr)
                sig_key = freeze_signature(sig)
                success += 1
                status = "success"
                err = ""
            except Exception as exc:  # pragma: no cover - reported in derivability output
                sig = {"kind": "unknown", "error": str(exc)}
                sig_key = freeze_signature(sig)
                errors += 1
                status = "unknown"
                err = str(exc)
            records.append({
                "expr": expr,
                "dag": dag,
                "dag_id": dag.dag_id,
                "dag_size": len(dag.nodes),
                "edge_probability": dag.edge_probability,
                "depth": expr.depth,
                "surface": expr.surface,
                "ast_key": expr.ast_key(),
                "feature_key": expr.feature_key(),
                "consequence_key": sig_key,
                "consequence_signature": sig,
                "derivation_status": status,
                "derivation_error": err,
            })
    return records, dag_by_id


def cumulative_rows(records: list[dict[str, Any]], max_depth: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    growth_rows = []
    stat_rows = []
    groups = defaultdict(list)
    for rec in records:
        groups[(rec["dag_size"], rec["edge_probability"])].append(rec)
    for (dag_size, p), group in sorted(groups.items()):
        for depth in range(1, max_depth + 1):
            subset = [r for r in group if r["depth"] <= depth]
            feature_keys = [r["feature_key"] for r in subset]
            consequence_keys = [r["consequence_key"] for r in subset]
            ast_keys = [(r["dag_id"], r["ast_key"]) for r in subset]
            fstats = class_stats(feature_keys)
            cstats = class_stats(consequence_keys)
            astats = class_stats(ast_keys)
            growth_rows.append({
                "dag_size": dag_size,
                "edge_probability": p,
                "depth": depth,
                "num_expressions": len(subset),
                "feature_class_count": int(fstats["class_count"]),
                "consequence_class_count": int(cstats["class_count"]),
                "ast_identity_class_count": int(astats["class_count"]),
                "feature_class_entropy": fstats["entropy"],
                "consequence_class_entropy": cstats["entropy"],
                "ast_identity_entropy": astats["entropy"],
            })
            stat_rows.append({
                "dag_size": dag_size,
                "edge_probability": p,
                "depth": depth,
                "relation": "feature",
                **{k: fstats[k] for k in fstats},
            })
            stat_rows.append({
                "dag_size": dag_size,
                "edge_probability": p,
                "depth": depth,
                "relation": "consequence",
                **{k: cstats[k] for k in cstats},
            })
            stat_rows.append({
                "dag_size": dag_size,
                "edge_probability": p,
                "depth": depth,
                "relation": "ast_identity",
                **{k: astats[k] for k in astats},
            })
    return pd.DataFrame(growth_rows), pd.DataFrame(stat_rows)


def compact_expr(rec: dict[str, Any]) -> dict[str, Any]:
    expr: Expression = rec["expr"]
    return {
        "expr_id": expr.expr_id,
        "dag_id": rec["dag_id"],
        "dag_size": rec["dag_size"],
        "edge_probability": rec["edge_probability"],
        "surface": expr.surface,
        "ast": repr(expr.ast),
        "features": expr.features,
        "consequence_signature": rec["consequence_signature"],
    }


def forgeability_examples(records: list[dict[str, Any]]) -> dict[str, Any]:
    feature_keys = [r["feature_key"] for r in records]
    consequence_keys = [r["consequence_key"] for r in records]
    same_feature = first_pair_same_key_diff_other(feature_keys, consequence_keys)
    different_feature = first_pair_same_key_diff_other(consequence_keys, feature_keys)
    return {
        "same_features_different_consequences_exists": same_feature is not None,
        "different_features_same_consequences_exists": different_feature is not None,
        "same_features_different_consequences": [] if same_feature is None else [compact_expr(records[same_feature[0]]), compact_expr(records[same_feature[1]])],
        "different_features_same_consequences": [] if different_feature is None else [compact_expr(records[different_feature[0]]), compact_expr(records[different_feature[1]])],
    }


def derivability_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)
    success = sum(1 for r in records if r["derivation_status"] == "success")
    unknown = sum(1 for r in records if r["derivation_status"] == "unknown")
    timeout = sum(1 for r in records if r["derivation_status"] == "timeout")
    return {
        "num_expressions": total,
        "success_count": success,
        "unknown_count": unknown,
        "timeout_count": timeout,
        "derivation_success_rate": success / total if total else 0.0,
        "unknown_rate": unknown / total if total else 0.0,
        "timeout_rate": timeout / total if total else 0.0,
        "kill_condition_triggered": (success / total if total else 0.0) < 0.99,
    }


def free_monoid_report(stats: pd.DataFrame) -> dict[str, Any]:
    final = stats.sort_values("depth").groupby(["relation", "dag_size", "edge_probability"], as_index=False).tail(1)
    rows = []
    relation_flags = {}
    for relation, group in final.groupby("relation"):
        mean_ratio = float(group["class_count_ratio"].mean())
        mean_singletons = float(group["singleton_fraction"].mean())
        flag = mean_ratio >= 0.95 and mean_singletons >= 0.95
        relation_flags[relation] = flag
        rows.append({
            "relation": relation,
            "mean_class_count_ratio": mean_ratio,
            "mean_singleton_fraction": mean_singletons,
            "free_monoid_like": flag,
        })
    return {"relations": rows, "relation_flags": relation_flags}


def collapse_report(stats: pd.DataFrame) -> dict[str, Any]:
    consequence = stats[stats["relation"] == "consequence"]
    collapsed = consequence[(consequence["class_count"] <= 1) | (consequence["largest_class_fraction"] > 0.95)]
    final = consequence.sort_values("depth").groupby(["dag_size", "edge_probability"], as_index=False).tail(1)
    final_collapsed = final[(final["class_count"] <= 1) | (final["largest_class_fraction"] > 0.95)]
    return {
        "collapsed_rows": int(len(collapsed)),
        "final_collapsed_rows": int(len(final_collapsed)),
        "max_largest_class_fraction": float(consequence["largest_class_fraction"].max()) if len(consequence) else 0.0,
        "mean_final_largest_class_fraction": float(final["largest_class_fraction"].mean()) if len(final) else 0.0,
        "semantic_collapse": bool(len(final_collapsed) > 0),
    }


def decide(growth: pd.DataFrame, stats: pd.DataFrame, forge: dict[str, Any], deriv: dict[str, Any], free: dict[str, Any], collapse: dict[str, Any], max_depth: int) -> dict[str, Any]:
    aggregate = growth.groupby("depth", as_index=False).agg({
        "num_expressions": "sum",
        "feature_class_count": "sum",
        "consequence_class_count": "sum",
        "ast_identity_class_count": "sum",
    })
    first = aggregate[aggregate["depth"] == 1].iloc[0]
    last = aggregate[aggregate["depth"] == max_depth].iloc[0]
    consequence_growth_ratio = float(last["consequence_class_count"] / max(1, first["consequence_class_count"]))
    consequence_vs_ast_ratio = float(last["consequence_class_count"] / max(1, last["ast_identity_class_count"]))
    consequence_vs_feature_ratio = float(last["consequence_class_count"] / max(1, last["feature_class_count"]))
    grows = consequence_growth_ratio > 1.2
    fewer_than_free_syntax = consequence_vs_ast_ratio < 0.85
    fewer_than_feature = consequence_vs_feature_ratio < 0.85
    both_forge = bool(forge["same_features_different_consequences_exists"] and forge["different_features_same_consequences_exists"])
    reliable = deriv["derivation_success_rate"] >= 0.99
    consequence_free = bool(free["relation_flags"].get("consequence"))
    feature_free = bool(free["relation_flags"].get("feature"))
    collapsed = bool(collapse["semantic_collapse"])

    if not reliable:
        label = "instrumentation_failure"
        recommendation = "Fix verifier coverage before interpreting equivalence classes."
    elif collapsed:
        label = "consequence_collapses"
        recommendation = "The consequence relation is too coarse; enrich the verifier or substrate."
    elif consequence_free:
        label = "consequence_is_syntax"
        recommendation = "The consequence signature tracks expression identity too closely; canonicalize semantics more aggressively."
    elif grows and fewer_than_free_syntax and fewer_than_feature and both_forge:
        label = "consequence_relation_viable"
        recommendation = "Proceed to richer causal-world fragments while keeping verifier-derived signatures."
    elif both_forge and grows and fewer_than_free_syntax and not consequence_free:
        label = "feature_proxy_failure"
        recommendation = "Feature equivalence is forgeable and too coarse; consequence relation works against AST syntax but is not fewer than feature classes."
    elif both_forge and grows and not consequence_free:
        label = "feature_proxy_failure"
        recommendation = "Feature equivalence is forgeable; consequence relation is promising but needs stronger compression vs syntax."
    else:
        label = "feature_proxy_failure"
        recommendation = "Feature equivalence is not sufficient; refine consequence signatures and rerun."

    return {
        "classification": label,
        "recommendation": recommendation,
        "evidence": {
            "consequence_growth_ratio_depth1_to_max": consequence_growth_ratio,
            "consequence_vs_ast_identity_ratio_at_max_depth": consequence_vs_ast_ratio,
            "consequence_vs_feature_ratio_at_max_depth": consequence_vs_feature_ratio,
            "consequence_classes_grow": grows,
            "consequence_fewer_than_free_syntax": fewer_than_free_syntax,
            "consequence_fewer_than_feature_classes": fewer_than_feature,
            "forgeability_examples_exist_both_ways": both_forge,
            "feature_free_monoid_like": feature_free,
            "consequence_free_monoid_like": consequence_free,
            "semantic_collapse": collapsed,
            "derivation_success_rate": deriv["derivation_success_rate"],
        },
    }


def plot_outputs(growth: pd.DataFrame, out: Path) -> None:
    agg = growth.groupby("depth", as_index=False).agg({
        "num_expressions": "sum",
        "feature_class_count": "sum",
        "consequence_class_count": "sum",
        "feature_class_entropy": "mean",
        "consequence_class_entropy": "mean",
        "ast_identity_class_count": "sum",
    })
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(agg["depth"], agg["feature_class_count"], marker="o", label="feature classes")
    ax.plot(agg["depth"], agg["consequence_class_count"], marker="o", label="consequence classes")
    ax.plot(agg["depth"], agg["ast_identity_class_count"], marker="o", label="AST identity")
    ax.set_xlabel("max expression depth")
    ax.set_ylabel("class count")
    ax.set_title("Feature vs consequence class growth")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "feature_vs_consequence_class_growth.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(agg["depth"], agg["feature_class_entropy"], marker="o", label="feature entropy")
    ax.plot(agg["depth"], agg["consequence_class_entropy"], marker="o", label="consequence entropy")
    ax.set_xlabel("max expression depth")
    ax.set_ylabel("entropy")
    ax.set_title("Feature vs consequence entropy")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "feature_vs_consequence_entropy.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(agg["depth"], agg["feature_class_count"] / agg["num_expressions"], marker="o", label="feature / expressions")
    ax.plot(agg["depth"], agg["consequence_class_count"] / agg["num_expressions"], marker="o", label="consequence / expressions")
    ax.plot(agg["depth"], agg["consequence_class_count"] / agg["ast_identity_class_count"], marker="o", label="consequence / AST identity")
    ax.set_xlabel("max expression depth")
    ax.set_ylabel("ratio")
    ax.set_title("Class ratios by depth")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "class_ratio_by_depth.png", dpi=130)
    plt.close(fig)


def write_summary(path: Path, decision: dict[str, Any], growth: pd.DataFrame, forge: dict[str, Any], free: dict[str, Any], collapse: dict[str, Any], deriv: dict[str, Any], args) -> None:
    agg = growth.groupby("depth", as_index=False).agg({
        "num_expressions": "sum",
        "feature_class_count": "sum",
        "consequence_class_count": "sum",
        "ast_identity_class_count": "sum",
        "feature_class_entropy": "mean",
        "consequence_class_entropy": "mean",
    })
    last = agg[agg["depth"] == args.max_depth].iloc[0]
    ev = decision["evidence"]
    lines = [
        "# Experiment 16 - Consequence vs Feature",
        "",
        "## Decision",
        "",
        f"Classification: `{decision['classification']}`.",
        "",
        decision["recommendation"],
        "",
        "## Run Parameters",
        "",
        f"- seed: {args.seed}",
        f"- max_depth: {args.max_depth}",
        f"- num_dags: {args.num_dags}",
        f"- per_depth_cap: {args.exprs_per_dag_depth}",
        "",
        "## Required Questions",
        "",
        f"1. Does feature-based equivalence behave like forgeable syntax? {'Yes' if forge['same_features_different_consequences_exists'] else 'No'}; same-feature/different-consequence examples exist = {forge['same_features_different_consequences_exists']}.",
        f"2. Does consequence-based equivalence nontrivially merge expressions? {'Yes' if forge['different_features_same_consequences_exists'] and not ev['consequence_free_monoid_like'] else 'No'}; consequence/AST ratio at max depth = {ev['consequence_vs_ast_identity_ratio_at_max_depth']:.4g}.",
        f"3. Are there same-feature/different-consequence examples? {forge['same_features_different_consequences_exists']}.",
        f"4. Are there different-feature/same-consequence examples? {forge['different_features_same_consequences_exists']}.",
        f"5. Does consequence-class count grow without becoming free syntax? {'Yes' if ev['consequence_classes_grow'] and not ev['consequence_free_monoid_like'] else 'No'}; growth ratio depth1->max = {ev['consequence_growth_ratio_depth1_to_max']:.4g}.",
        f"6. Is derivability complete enough to trust the result? {'Yes' if deriv['derivation_success_rate'] >= 0.99 else 'No'}; success rate = {deriv['derivation_success_rate']:.6g}.",
        f"7. Should we proceed to richer causal-world fragments? {'Yes' if decision['classification'] in {'consequence_relation_viable', 'feature_proxy_failure'} and deriv['derivation_success_rate'] >= 0.99 else 'No'}.",
        "",
        "## Aggregate Growth",
        "",
        markdown_table(agg),
        "",
        "## Key Evidence",
        "",
        f"- expressions at max depth: {int(last['num_expressions'])}",
        f"- feature classes at max depth: {int(last['feature_class_count'])}",
        f"- consequence classes at max depth: {int(last['consequence_class_count'])}",
        f"- AST identity classes at max depth: {int(last['ast_identity_class_count'])}",
        f"- consequence vs AST identity ratio: {ev['consequence_vs_ast_identity_ratio_at_max_depth']:.4g}",
        f"- consequence vs feature ratio: {ev['consequence_vs_feature_ratio_at_max_depth']:.4g}",
        f"- consequence fewer than feature classes: {ev['consequence_fewer_than_feature_classes']}",
        f"- semantic collapse: {collapse['semantic_collapse']}",
        f"- consequence free-monoid-like: {ev['consequence_free_monoid_like']}",
        "",
        "## Honesty Notes",
        "",
        "- Consequence signatures are verifier-derived from reachability, ancestors, d-separation, interventions and path properties.",
        "- Feature keys intentionally use shallow surface properties and do not include verifier output.",
        "- Label-free AST identity is reported only as the free-syntax baseline.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 16: consequence equivalence vs feature equivalence")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--num-dags", type=int, default=200)
    parser.add_argument("--exprs-per-dag-depth", type=int, default=120)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_16")
    args = parser.parse_args()

    out = ensure(args.outputs)
    records, _ = build_records(args.seed, args.max_depth, args.num_dags, args.exprs_per_dag_depth)
    growth, stats = cumulative_rows(records, args.max_depth)
    forge = forgeability_examples(records)
    deriv = derivability_report(records)
    free = free_monoid_report(stats)
    collapse = collapse_report(stats)
    decision = decide(growth, stats, forge, deriv, free, collapse, args.max_depth)

    growth.to_csv(out / "class_growth.csv", index=False)
    stats.to_csv(out / "equivalence_stats.csv", index=False)
    write_json(out / "forgeability_examples.json", forge)
    write_json(out / "free_monoid_report.json", free)
    write_json(out / "collapse_report.json", collapse)
    write_json(out / "derivability_report.json", deriv)
    write_json(out / "final_decision.json", decision)
    plot_outputs(growth, out)
    write_summary(out / "summary.md", decision, growth, forge, free, collapse, deriv, args)

    print(json.dumps({
        "classification": decision["classification"],
        "num_expressions": len(records),
        "derivation_success_rate": deriv["derivation_success_rate"],
        "same_features_different_consequences": forge["same_features_different_consequences_exists"],
        "different_features_same_consequences": forge["different_features_same_consequences_exists"],
        "consequence_vs_ast_ratio": decision["evidence"]["consequence_vs_ast_identity_ratio_at_max_depth"],
        "outputs": str(out),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
