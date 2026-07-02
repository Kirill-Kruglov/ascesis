#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXP16_SRC = ROOT.parents[0] / "16_consequence_vs_feature" / "src"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(EXP16_SRC))

from backbone_consequence.perturb import perturbation_samples  # noqa: E402
from consequence_feature.dag import CausalDAG, generate_dag_grid  # noqa: E402
from consequence_feature.expressions import Expression, generate_expressions  # noqa: E402
from consequence_feature.verifier import consequence_signature, freeze_signature  # noqa: E402

K_VALUES = [0, 1, 2, 3, 4]
GNS_WEIGHTS = {1: 0.40, 2: 0.30, 3: 0.20, 4: 0.10}


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def stable_id(value: Any) -> str:
    raw = repr(value).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def mentioned(expr: Expression) -> set[str]:
    return {expr.x, expr.y, *expr.conditioning, *expr.interventions}


def is_operator_alias_pair(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ea: Expression = a["expr"]
    eb: Expression = b["expr"]
    alias_ops = {"Reachable", "Effect", "Ancestor"}
    return (
        ea.operator in alias_ops
        and eb.operator in alias_ops
        and ea.x == eb.x
        and ea.y == eb.y
        and ea.conditioning == eb.conditioning
        and ea.interventions == eb.interventions
    )


def pair_score(a: dict[str, Any], b: dict[str, Any]) -> tuple[int, int, int, int, str]:
    ea: Expression = a["expr"]
    eb: Expression = b["expr"]
    non_alias = int(not is_operator_alias_pair(a, b))
    different_operands = int((ea.x, ea.y, ea.conditioning, ea.interventions) != (eb.x, eb.y, eb.conditioning, eb.interventions))
    different_depth = int(ea.depth != eb.depth)
    different_operator = int(ea.operator != eb.operator)
    return (non_alias, different_operands, different_depth, different_operator, ea.surface + "|" + eb.surface)


def expr_record(expr: Expression, dag: CausalDAG, sig_key: tuple[Any, ...]) -> dict[str, Any]:
    return {
        "expr": expr,
        "dag": dag,
        "dag_id": dag.dag_id,
        "dag_size": len(dag.nodes),
        "edge_probability": dag.edge_probability,
        "depth": expr.depth,
        "operator": expr.operator,
        "feature_key": expr.feature_key(),
        "ast_key": expr.ast_key(),
        "consequence_key": sig_key,
        "surface": expr.surface,
    }


def build_records(seed: int, num_dags: int, max_depth: int, per_depth_cap: int) -> list[dict[str, Any]]:
    records = []
    dags = generate_dag_grid(seed=seed, num_dags=num_dags)
    for idx, dag in enumerate(dags, start=1):
        rng = random.Random(seed + idx * 104729)
        for expr in generate_expressions(dag, max_depth=max_depth, rng=rng, per_depth_cap=per_depth_cap):
            sig_key = freeze_signature(consequence_signature(dag, expr))
            records.append(expr_record(expr, dag, sig_key))
    return records


def same_dag_pairs(group: list[dict[str, Any]], max_pairs: int, rng: random.Random) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_dag: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in group:
        by_dag[rec["dag_id"]].append(rec)
    candidates: list[tuple[tuple[int, int, int, int, str], tuple[dict[str, Any], dict[str, Any]]]] = []
    for items in by_dag.values():
        if len(items) < 2:
            continue
        sorted_items = sorted(items, key=lambda r: (r["depth"], r["operator"], r["surface"]))
        # Classes are usually small per DAG; cap pair enumeration to avoid quadratic blow-up.
        capped = sorted_items[:16] + sorted_items[-16:] if len(sorted_items) > 32 else sorted_items
        for i in range(len(capped)):
            for j in range(i + 1, len(capped)):
                a, b = capped[i], capped[j]
                candidates.append((pair_score(a, b), (a, b)))
    candidates.sort(key=lambda item: item[0], reverse=True)
    pairs = [pair for _, pair in candidates[:max_pairs]]
    if len(pairs) > max_pairs:
        pairs = rng.sample(pairs, max_pairs)
    return pairs


def pair_persistence(pair: tuple[dict[str, Any], dict[str, Any]], k: int, seed: int, perturb_samples_per_k: int) -> dict[str, Any]:
    a, b = pair
    dag: CausalDAG = a["dag"]
    protected = mentioned(a["expr"]) | mentioned(b["expr"])
    seed_material = f"{seed}|{a['surface']}|{b['surface']}|{dag.dag_id}|{k}"
    local_seed = int(hashlib.sha1(seed_material.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(local_seed)
    perturbed = perturbation_samples(dag, k, protected=protected, rng=rng, samples=perturb_samples_per_k)
    if not perturbed:
        return {"persistence": None, "tested": 0, "equal": 0, "runtime_sec": 0.0, "op_counts": Counter()}
    equal = 0
    op_counts: Counter[str] = Counter()
    t0 = time.perf_counter()
    for item in perturbed:
        op_counts.update(item.operations)
        try:
            sa = freeze_signature(consequence_signature(item.dag, a["expr"]))
            sb = freeze_signature(consequence_signature(item.dag, b["expr"]))
            equal += int(sa == sb)
        except Exception:
            pass
    elapsed = time.perf_counter() - t0
    return {"persistence": equal / len(perturbed), "tested": len(perturbed), "equal": equal, "runtime_sec": elapsed, "op_counts": op_counts}


def class_backbone(records: list[dict[str, Any]], args) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = random.Random(args.seed)
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        groups[rec["consequence_key"]].append(rec)

    class_items = sorted(groups.items(), key=lambda kv: (-len(kv[1]), stable_id(kv[0])))
    rows = []
    curve_rows = []
    sensitivity = defaultdict(lambda: {"equal": 0, "tested": 0})
    analyzed = 0
    for sig_key, group in class_items:
        class_id = stable_id(sig_key)
        pairs = same_dag_pairs(group, args.pairs_per_class, rng)
        can_analyze = bool(pairs) and analyzed < args.max_analyzed_classes
        persist = {k: None for k in K_VALUES}
        tested_total = {k: 0 for k in K_VALUES}
        equal_total = {k: 0 for k in K_VALUES}
        runtime = 0.0
        alias_pair_count = sum(1 for pair in pairs if is_operator_alias_pair(pair[0], pair[1]))
        nontrivial_pair_count = len(pairs) - alias_pair_count
        if can_analyze:
            analyzed += 1
            for k in K_VALUES:
                vals = []
                for pair in pairs:
                    res = pair_persistence(pair, k, args.seed, args.perturbations_per_k)
                    runtime += res["runtime_sec"]
                    tested_total[k] += res["tested"]
                    equal_total[k] += res["equal"]
                    if res["persistence"] is not None:
                        vals.append(res["persistence"])
                    for op, count in res["op_counts"].items():
                        sensitivity[(k, op)]["tested"] += res["tested"]
                        sensitivity[(k, op)]["equal"] += res["equal"]
                persist[k] = sum(vals) / len(vals) if vals else None
        gns = None
        if all(persist[k] is not None for k in (1, 2, 3, 4)):
            gns = sum(GNS_WEIGHTS[k] * float(persist[k]) for k in GNS_WEIGHTS)
        frozen = bool(gns is not None and all(float(persist[k]) > args.frozen_threshold for k in (1, 2, 3, 4)))
        weak = bool(persist[1] is not None and float(persist[1]) < args.weak_threshold)
        min_destroy = None
        for k in (1, 2, 3, 4):
            if persist[k] is not None and float(persist[k]) < args.frozen_threshold:
                min_destroy = k
                break
        ops = sorted({r["operator"] for r in group})
        depths = sorted({int(r["depth"]) for r in group})
        dags = {r["dag_id"] for r in group}
        dag_sizes = sorted({int(r["dag_size"]) for r in group})
        reps = sorted(group, key=lambda r: (r["depth"], r["operator"], r["surface"]))[:3]
        row = {
            "class_id": class_id,
            "class_size": len(group),
            "analyzed": can_analyze,
            "pair_count": len(pairs),
            "alias_pair_count": alias_pair_count,
            "nontrivial_pair_count": nontrivial_pair_count,
            "alias_pair_fraction": alias_pair_count / len(pairs) if pairs else None,
            "gns": gns,
            "frozen": frozen,
            "weak": weak,
            "min_perturbation_to_destroy": min_destroy,
            "persistence_k0": persist[0],
            "persistence_k1": persist[1],
            "persistence_k2": persist[2],
            "persistence_k3": persist[3],
            "persistence_k4": persist[4],
            "tested_perturbations": sum(tested_total.values()),
            "runtime_sec": runtime,
            "expression_depth_min": min(depths),
            "expression_depth_max": max(depths),
            "operator_diversity": len(ops),
            "operators": ";".join(ops),
            "dag_diversity": len(dags),
            "dag_size_min": min(dag_sizes),
            "dag_size_max": max(dag_sizes),
            "representative_expressions": " | ".join(r["surface"] for r in reps),
        }
        rows.append(row)
        for k in K_VALUES:
            curve_rows.append({"class_id": class_id, "k": k, "persistence": persist[k], "class_size": len(group), "analyzed": can_analyze})
    sensitivity_rows = []
    for (k, op), val in sorted(sensitivity.items()):
        tested = val["tested"]
        sensitivity_rows.append({"k": k, "operation": op, "persistence": val["equal"] / tested if tested else None, "tested": tested})
    return pd.DataFrame(rows), pd.DataFrame(curve_rows), pd.DataFrame(sensitivity_rows)


def sample_pairs_by_key(records: list[dict[str, Any]], key_name: str, max_pairs: int, rng: random.Random) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        groups[rec[key_name]].append(rec)
    pairs = []
    for group in groups.values():
        pairs.extend(same_dag_pairs(group, 2, rng))
        if len(pairs) >= max_pairs:
            break
    return pairs[:max_pairs]


def baseline_persistence(records: list[dict[str, Any]], class_df: pd.DataFrame, args) -> dict[str, Any]:
    rng = random.Random(args.seed + 17)
    baselines = {}
    for name, key in [("feature", "feature_key"), ("random", None)]:
        if key is None:
            shuffled = records[:]
            rng.shuffle(shuffled)
            pairs = []
            for i in range(0, min(len(shuffled) - 1, args.baseline_pairs * 2), 2):
                if shuffled[i]["dag_id"] == shuffled[i + 1]["dag_id"]:
                    pairs.append((shuffled[i], shuffled[i + 1]))
            if len(pairs) < args.baseline_pairs:
                by_dag = defaultdict(list)
                for r in records:
                    by_dag[r["dag_id"]].append(r)
                for items in by_dag.values():
                    if len(items) >= 2:
                        a, b = rng.sample(items, 2)
                        pairs.append((a, b))
                    if len(pairs) >= args.baseline_pairs:
                        break
        else:
            pairs = sample_pairs_by_key(records, key, args.baseline_pairs, rng)
        vals = []
        for pair in pairs:
            for k in (1, 2, 3, 4):
                res = pair_persistence(pair, k, args.seed + 101, args.perturbations_per_k)
                if res["persistence"] is not None:
                    vals.append(res["persistence"])
        baselines[name] = {
            "pair_count": len(pairs),
            "mean_persistence": sum(vals) / len(vals) if vals else None,
            "high_persistence_fraction": sum(1 for v in vals if v > args.frozen_threshold) / len(vals) if vals else None,
        }

    # AST baseline: identity-as-meaning; does one expression keep its own consequence signature under perturbation?
    ast_vals = []
    for rec in rng.sample(records, min(args.baseline_pairs, len(records))):
        original = rec["consequence_key"]
        for k in (1, 2, 3, 4):
            perturbed = perturbation_samples(rec["dag"], k, protected=mentioned(rec["expr"]), rng=rng, samples=args.perturbations_per_k)
            if not perturbed:
                continue
            same = 0
            for item in perturbed:
                same += int(freeze_signature(consequence_signature(item.dag, rec["expr"])) == original)
            ast_vals.append(same / len(perturbed))
    baselines["ast_identity"] = {
        "expression_count": min(args.baseline_pairs, len(records)),
        "mean_persistence": sum(ast_vals) / len(ast_vals) if ast_vals else None,
        "high_persistence_fraction": sum(1 for v in ast_vals if v > args.frozen_threshold) / len(ast_vals) if ast_vals else None,
    }
    analyzed = class_df[class_df["analyzed"] == True]
    baselines["consequence"] = {
        "class_count": int(len(analyzed)),
        "mean_gns": float(analyzed["gns"].dropna().mean()) if len(analyzed) else None,
        "high_gns_fraction": float((analyzed["gns"] > args.frozen_threshold).mean()) if len(analyzed) else None,
    }
    return baselines


def coverage_reports(class_df: pd.DataFrame) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    analyzed = class_df[class_df["analyzed"] == True].copy()
    total = len(analyzed)
    frozen = analyzed[analyzed["frozen"] == True]
    coverage = {
        "analyzed_class_count": int(total),
        "total_class_count": int(len(class_df)),
        "frozen_class_count": int(len(frozen)),
        "weak_class_count": int((analyzed["weak"] == True).sum()) if total else 0,
        "frozen_coverage": float(len(frozen) / total) if total else 0.0,
        "weighted_frozen_coverage": float(frozen["class_size"].sum() / analyzed["class_size"].sum()) if total and analyzed["class_size"].sum() else 0.0,
    }
    depth_rows = []
    for depth in sorted(set(class_df["expression_depth_max"])):
        subset = analyzed[analyzed["expression_depth_max"] == depth]
        depth_rows.append({"depth": int(depth), "analyzed_classes": int(len(subset)), "frozen_coverage": float((subset["frozen"] == True).mean()) if len(subset) else 0.0})
    size_rows = []
    for size in sorted(set(class_df["dag_size_max"])):
        subset = analyzed[analyzed["dag_size_max"] == size]
        size_rows.append({"dag_size": int(size), "analyzed_classes": int(len(subset)), "frozen_coverage": float((subset["frozen"] == True).mean()) if len(subset) else 0.0})
    return coverage, pd.DataFrame(depth_rows), pd.DataFrame(size_rows)


def diversity_report(class_df: pd.DataFrame) -> dict[str, Any]:
    frozen = class_df[(class_df["analyzed"] == True) & (class_df["frozen"] == True)]
    high = class_df[(class_df["analyzed"] == True) & (class_df["gns"].fillna(0) > 0.8)]
    frozen_nontrivial = frozen[frozen["nontrivial_pair_count"].fillna(0) > 0] if len(frozen) else frozen
    high_nontrivial = high[high["nontrivial_pair_count"].fillna(0) > 0] if len(high) else high
    return {
        "frozen_class_count": int(len(frozen)),
        "high_gns_class_count": int(len(high)),
        "frozen_nontrivial_class_count": int(len(frozen_nontrivial)),
        "high_gns_nontrivial_class_count": int(len(high_nontrivial)),
        "frozen_alias_pair_fraction_mean": float(frozen["alias_pair_fraction"].dropna().mean()) if len(frozen) else 0.0,
        "frozen_mean_operator_diversity": float(frozen["operator_diversity"].mean()) if len(frozen) else 0.0,
        "frozen_mean_dag_diversity": float(frozen["dag_diversity"].mean()) if len(frozen) else 0.0,
        "frozen_depth_range": [int(frozen["expression_depth_min"].min()), int(frozen["expression_depth_max"].max())] if len(frozen) else [],
        "high_gns_mean_operator_diversity": float(high["operator_diversity"].mean()) if len(high) else 0.0,
        "high_gns_mean_dag_diversity": float(high["dag_diversity"].mean()) if len(high) else 0.0,
    }


def decide(class_df: pd.DataFrame, coverage: dict[str, Any], baselines: dict[str, Any], diversity: dict[str, Any]) -> dict[str, Any]:
    analyzed = class_df[class_df["analyzed"] == True]
    if len(analyzed) == 0:
        label = "Instrumentation_failure"
        reason = "No analyzable same-DAG consequence-equivalent pairs were found."
    elif bool((analyzed["persistence_k1"].fillna(0) < 0.5).all()):
        label = "H2_not_supported"
        reason = "All analyzed classes become fragile after one perturbation."
    elif coverage["frozen_class_count"] > 0 and diversity["frozen_nontrivial_class_count"] == 0:
        label = "Trivial_backbone"
        reason = "Frozen stability is explained by operator-alias pairs only."
    elif coverage["frozen_class_count"] > 0 and diversity["frozen_mean_operator_diversity"] <= 1.0 and diversity["frozen_mean_dag_diversity"] <= 1.0:
        label = "Trivial_backbone"
        reason = "Only structurally narrow frozen classes survived."
    else:
        cons_mean = baselines["consequence"].get("mean_gns") or 0.0
        feat_mean = baselines["feature"].get("mean_persistence") or 0.0
        has_nontrivial_high = bool((analyzed["gns"].fillna(0) > 0.8).any()) and diversity["high_gns_nontrivial_class_count"] > 0
        if has_nontrivial_high and cons_mean > feat_mean + 0.05:
            label = "H2_supported"
            reason = "Nontrivial high-GNS consequence classes exist and outperform feature baseline."
        elif coverage["frozen_class_count"] > 0 or bool((analyzed["gns"].fillna(0) > 0.8).any()):
            label = "H2_supported"
            reason = "High-stability consequence backbone exists, though baseline separation is modest."
        else:
            label = "H2_not_supported"
            reason = "Consequence classes are mostly fragile under perturbation."
    return {
        "classification": label,
        "reason": reason,
        "evidence": {
            "analyzed_class_count": coverage["analyzed_class_count"],
            "total_class_count": coverage["total_class_count"],
            "frozen_class_count": coverage["frozen_class_count"],
            "weak_class_count": coverage["weak_class_count"],
            "frozen_coverage": coverage["frozen_coverage"],
            "weighted_frozen_coverage": coverage["weighted_frozen_coverage"],
            "consequence_mean_gns": baselines["consequence"].get("mean_gns"),
            "feature_mean_persistence": baselines["feature"].get("mean_persistence"),
            "ast_identity_mean_persistence": baselines["ast_identity"].get("mean_persistence"),
            "random_mean_persistence": baselines["random"].get("mean_persistence"),
            "frozen_nontrivial_class_count": diversity["frozen_nontrivial_class_count"],
            "frozen_alias_pair_fraction_mean": diversity["frozen_alias_pair_fraction_mean"],
            "frozen_mean_operator_diversity": diversity["frozen_mean_operator_diversity"],
            "frozen_mean_dag_diversity": diversity["frozen_mean_dag_diversity"],
        },
        "recommendation": "Use Global Necessity alongside consequence class identity; proceed to richer fragments only if high-GNS diversity persists.",
    }


def plot_outputs(class_df: pd.DataFrame, curves: pd.DataFrame, depth_cov: pd.DataFrame, size_cov: pd.DataFrame, sensitivity: pd.DataFrame, out: Path) -> None:
    analyzed = class_df[class_df["analyzed"] == True].copy()
    if len(analyzed):
        mean_curve = curves[curves["analyzed"] == True].groupby("k", as_index=False)["persistence"].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(mean_curve["k"], mean_curve["persistence"], marker="o")
        ax.set_ylim(-0.02, 1.02)
        ax.set_xlabel("perturbation budget k")
        ax.set_ylabel("mean persistence")
        ax.set_title("Persistence curves")
        ax.grid(True, alpha=0.3)
        fig.tight_layout(); fig.savefig(out / "persistence_curves.png", dpi=130); plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(analyzed["gns"].dropna(), bins=20, color="tab:blue", alpha=0.8)
        ax.set_xlabel("Global Necessity Score")
        ax.set_ylabel("class count")
        ax.set_title("GNS histogram")
        fig.tight_layout(); fig.savefig(out / "gns_histogram.png", dpi=130); plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(analyzed["class_size"], analyzed["gns"], c=analyzed["expression_depth_max"], cmap="viridis", s=18, alpha=0.75)
        ax.set_xscale("log")
        ax.set_xlabel("class size")
        ax.set_ylabel("GNS")
        ax.set_title("Frozen vs weak scatter")
        ax.grid(True, alpha=0.3)
        fig.tight_layout(); fig.savefig(out / "frozen_vs_weak_scatter.png", dpi=130); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    if len(depth_cov):
        ax.bar(depth_cov["depth"].astype(str), depth_cov["frozen_coverage"])
    ax.set_xlabel("max expression depth in class")
    ax.set_ylabel("frozen coverage")
    ax.set_title("Coverage by depth")
    fig.tight_layout(); fig.savefig(out / "coverage_by_depth.png", dpi=130); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    if len(size_cov):
        ax.bar(size_cov["dag_size"].astype(str), size_cov["frozen_coverage"])
    ax.set_xlabel("DAG size")
    ax.set_ylabel("frozen coverage")
    ax.set_title("Coverage by DAG size")
    fig.tight_layout(); fig.savefig(out / "coverage_by_dag_size.png", dpi=130); plt.close(fig)

    if len(sensitivity):
        pivot = sensitivity.pivot_table(index="operation", columns="k", values="persistence", aggfunc="mean")
        fig, ax = plt.subplots(figsize=(8, 5))
        im = ax.imshow(pivot.fillna(0).values, aspect="auto", cmap="magma", vmin=0, vmax=1)
        ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels([str(c) for c in pivot.columns])
        ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels(pivot.index)
        ax.set_xlabel("k"); ax.set_title("Perturbation sensitivity matrix")
        fig.colorbar(im, ax=ax, label="persistence")
        fig.tight_layout(); fig.savefig(out / "perturbation_sensitivity_matrix.png", dpi=130); plt.close(fig)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "(empty)"
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in df.columns:
            v = row[col]
            if pd.isna(v): vals.append("")
            elif isinstance(v, float):
                vals.append(f"{v:.6g}")
            else:
                vals.append(str(v).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_summary(path: Path, args, decision: dict[str, Any], coverage: dict[str, Any], baselines: dict[str, Any], diversity: dict[str, Any], class_df: pd.DataFrame) -> None:
    analyzed = class_df[class_df["analyzed"] == True]
    corr_df = analyzed[["expression_depth_max", "class_size", "gns"]].dropna()
    if len(corr_df) > 2 and corr_df["gns"].nunique() > 1:
        corr_depth = float(corr_df[["expression_depth_max", "gns"]].corr().iloc[0, 1])
        corr_size = float(corr_df[["class_size", "gns"]].corr().iloc[0, 1])
    else:
        corr_depth = None
        corr_size = None
    top = analyzed.sort_values(["gns", "nontrivial_pair_count", "class_size"], ascending=False).head(8)[["class_id", "class_size", "gns", "frozen", "weak", "nontrivial_pair_count", "alias_pair_fraction", "operator_diversity", "dag_diversity", "representative_expressions"]]
    ev = decision["evidence"]
    lines = [
        "# Experiment 17 - Backbone Consequence",
        "",
        "## Decision",
        "",
        f"Classification: `{decision['classification']}`.",
        "",
        decision["reason"],
        "",
        "## Run Parameters",
        "",
        f"- seed: {args.seed}",
        f"- num_dags: {args.num_dags}",
        f"- max_depth: {args.max_depth}",
        f"- expressions_per_dag_depth: {args.exprs_per_dag_depth}",
        f"- max_analyzed_classes: {args.max_analyzed_classes}",
        f"- perturbations_per_k: {args.perturbations_per_k}",
        "- GNS definition: weighted average of Persistence(k=1..4), weights 0.40/0.30/0.20/0.10, emphasizing lower-budget perturbations.",
        "",
        "## Required Questions",
        "",
        f"1. Do frozen consequence classes exist? {'Yes' if coverage['frozen_class_count'] > 0 else 'No'}.",
        f"2. Are they nontrivial? {'Yes' if diversity['frozen_mean_operator_diversity'] > 1.0 or diversity['frozen_mean_dag_diversity'] > 1.0 else 'No'}.",
        f"3. How many? {coverage['frozen_class_count']} frozen classes among {coverage['analyzed_class_count']} analyzed classes.",
        f"4. Are they more stable than feature classes? {'Yes' if (ev['consequence_mean_gns'] or 0) > (ev['feature_mean_persistence'] or 0) else 'No'}; consequence mean GNS={ev['consequence_mean_gns']:.6g}, feature baseline={ev['feature_mean_persistence']:.6g}.",
        f"5. Are they more stable than AST identity? {'Yes' if (ev['consequence_mean_gns'] or 0) > (ev['ast_identity_mean_persistence'] or 0) else 'No'}; AST baseline={ev['ast_identity_mean_persistence']:.6g}.",
        f"6. Does stability correlate with expression depth? {'undefined: GNS is constant across analyzed classes' if corr_depth is None else f'correlation={corr_depth:.4g}'}.",
        f"7. Does stability correlate with consequence class size? {'undefined: GNS is constant across analyzed classes' if corr_size is None else f'correlation={corr_size:.4g}'}.",
        "8. Should Global Necessity replace class cardinality as primary invariant? Yes as a stability invariant, but it should be tracked alongside class diversity/cardinality rather than replacing them entirely.",
        "",
        "## Coverage",
        "",
        f"- total consequence classes: {coverage['total_class_count']}",
        f"- analyzed classes: {coverage['analyzed_class_count']}",
        f"- frozen classes: {coverage['frozen_class_count']}",
        f"- nontrivial frozen classes: {diversity['frozen_nontrivial_class_count']}",
        f"- mean frozen alias-pair fraction: {diversity['frozen_alias_pair_fraction_mean']:.6g}",
        f"- weak classes: {coverage['weak_class_count']}",
        f"- frozen coverage: {coverage['frozen_coverage']:.6g}",
        f"- weighted frozen coverage: {coverage['weighted_frozen_coverage']:.6g}",
        "",
        "## Baselines",
        "",
        f"- consequence mean GNS: {ev['consequence_mean_gns']:.6g}",
        f"- feature mean persistence: {ev['feature_mean_persistence']:.6g}",
        f"- AST identity mean persistence: {ev['ast_identity_mean_persistence']:.6g}",
        f"- random mean persistence: {ev['random_mean_persistence']:.6g}",
        "",
        "## Top High-GNS Classes",
        "",
        markdown_table(top),
        "",
        "## Honesty Notes",
        "",
        "- The causal DAG generator and verifier are reused from Experiment 16 unchanged.",
        "- Persistence is estimated from deterministic representative same-DAG pairs per class and bounded perturbation samples, not exhaustive pair enumeration.",
        "- Feature, random, and AST baselines are evaluated by verifier consequence equality under perturbation, not by tautological key equality.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 17: backbone consequence stability")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-dags", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--exprs-per-dag-depth", type=int, default=80)
    parser.add_argument("--max-analyzed-classes", type=int, default=1000)
    parser.add_argument("--pairs-per-class", type=int, default=2)
    parser.add_argument("--perturbations-per-k", type=int, default=5)
    parser.add_argument("--baseline-pairs", type=int, default=500)
    parser.add_argument("--frozen-threshold", type=float, default=0.95)
    parser.add_argument("--weak-threshold", type=float, default=0.5)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17")
    args = parser.parse_args()

    out = ensure(args.outputs)
    t0 = time.perf_counter()
    records = build_records(args.seed, args.num_dags, args.max_depth, args.exprs_per_dag_depth)
    build_sec = time.perf_counter() - t0
    t1 = time.perf_counter()
    class_df, curves, sensitivity = class_backbone(records, args)
    backbone_sec = time.perf_counter() - t1
    t2 = time.perf_counter()
    baselines = baseline_persistence(records, class_df, args)
    baseline_sec = time.perf_counter() - t2
    coverage, depth_cov, size_cov = coverage_reports(class_df)
    diversity = diversity_report(class_df)
    decision = decide(class_df, coverage, baselines, diversity)

    class_df.to_csv(out / "class_backbone.csv", index=False)
    curves.to_csv(out / "persistence_curves.csv", index=False)
    sensitivity.to_csv(out / "perturbation_sensitivity.csv", index=False)
    depth_cov.to_csv(out / "coverage_by_depth.csv", index=False)
    size_cov.to_csv(out / "coverage_by_dag_size.csv", index=False)
    complexity = pd.DataFrame([
        {"stage": "build_records", "runtime_sec": build_sec, "items": len(records), "runtime_per_item_sec": build_sec / max(1, len(records))},
        {"stage": "class_backbone", "runtime_sec": backbone_sec, "items": int((class_df["analyzed"] == True).sum()), "runtime_per_item_sec": backbone_sec / max(1, int((class_df["analyzed"] == True).sum()))},
        {"stage": "baselines", "runtime_sec": baseline_sec, "items": args.baseline_pairs, "runtime_per_item_sec": baseline_sec / max(1, args.baseline_pairs)},
    ])
    complexity.to_csv(out / "complexity_report.csv", index=False)
    write_json(out / "coverage_report.json", coverage)
    write_json(out / "baseline_report.json", baselines)
    write_json(out / "diversity_report.json", diversity)
    write_json(out / "final_decision.json", decision)
    plot_outputs(class_df, curves, depth_cov, size_cov, sensitivity, out)
    write_summary(out / "summary.md", args, decision, coverage, baselines, diversity, class_df)

    print(json.dumps({
        "classification": decision["classification"],
        "num_expressions": len(records),
        "total_classes": coverage["total_class_count"],
        "analyzed_classes": coverage["analyzed_class_count"],
        "frozen_classes": coverage["frozen_class_count"],
        "weak_classes": coverage["weak_class_count"],
        "consequence_mean_gns": decision["evidence"]["consequence_mean_gns"],
        "feature_mean_persistence": decision["evidence"]["feature_mean_persistence"],
        "outputs": str(out),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
