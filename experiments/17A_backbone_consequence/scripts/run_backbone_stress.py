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

from backbone_stress.adversary import AttackDAG, adversarial_candidates  # noqa: E402
from consequence_feature.dag import CausalDAG, generate_dag_grid  # noqa: E402
from consequence_feature.expressions import Expression, generate_expressions  # noqa: E402
from consequence_feature.verifier import consequence_signature, freeze_signature  # noqa: E402

K_VALUES = [0, 1, 2, 3, 4]


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def stable_id(value: Any) -> str:
    return hashlib.sha1(repr(value).encode("utf-8")).hexdigest()[:16]


def mentioned(expr: Expression) -> set[str]:
    return {expr.x, expr.y, *expr.conditioning, *expr.interventions}


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


def is_operator_alias_pair(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ea: Expression = a["expr"]
    eb: Expression = b["expr"]
    alias_ops = {"Reachable", "Effect", "Ancestor", "Independent", "Blocked"}
    return (
        ea.operator in alias_ops
        and eb.operator in alias_ops
        and ea.x == eb.x
        and ea.y == eb.y
        and ea.conditioning == eb.conditioning
        and ea.interventions == eb.interventions
    )


def pair_score(a: dict[str, Any], b: dict[str, Any]) -> tuple[int, int, int, int, str]:
    ea, eb = a["expr"], b["expr"]
    return (
        int(not is_operator_alias_pair(a, b)),
        int((ea.x, ea.y, ea.conditioning, ea.interventions) != (eb.x, eb.y, eb.conditioning, eb.interventions)),
        int(ea.depth != eb.depth),
        int(ea.operator != eb.operator),
        ea.surface + "|" + eb.surface,
    )


def same_dag_pairs(group: list[dict[str, Any]], max_pairs: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_dag: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in group:
        by_dag[rec["dag_id"]].append(rec)
    candidates = []
    for items in by_dag.values():
        if len(items) < 2:
            continue
        items = sorted(items, key=lambda r: (r["depth"], r["operator"], r["surface"]))
        capped = items[:14] + items[-14:] if len(items) > 28 else items
        for i in range(len(capped)):
            for j in range(i + 1, len(capped)):
                candidates.append((pair_score(capped[i], capped[j]), (capped[i], capped[j])))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [pair for _, pair in candidates[:max_pairs]]


def cross_dag_pairs(group: list[dict[str, Any]], max_pairs: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_dag: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in group:
        by_dag[rec["dag_id"]].append(rec)
    dag_ids = sorted(by_dag)
    pairs = []
    for i in range(len(dag_ids)):
        for j in range(i + 1, len(dag_ids)):
            a_items = sorted(by_dag[dag_ids[i]], key=lambda r: (r["operator"], r["surface"]))
            b_items = sorted(by_dag[dag_ids[j]], key=lambda r: (r["operator"], r["surface"]))
            best = max(((pair_score(a, b), (a, b)) for a in a_items[:8] for b in b_items[:8]), key=lambda x: x[0], default=None)
            if best is not None:
                pairs.append(best)
            if len(pairs) >= max_pairs:
                break
        if len(pairs) >= max_pairs:
            break
    pairs.sort(key=lambda x: x[0], reverse=True)
    return [pair for _, pair in pairs[:max_pairs]]


def equivalent(a_dag: CausalDAG, a_expr: Expression, b_dag: CausalDAG, b_expr: Expression) -> bool | None:
    try:
        return freeze_signature(consequence_signature(a_dag, a_expr)) == freeze_signature(consequence_signature(b_dag, b_expr))
    except Exception:
        return None


def candidate_score(item: AttackDAG, a_expr: Expression, b_expr: Expression, other_dag: CausalDAG | None, mode: str) -> tuple[int, int, int]:
    if mode == "same_sync":
        eq = equivalent(item.dag, a_expr, item.dag, b_expr)
    elif mode == "left_only":
        eq = equivalent(item.dag, a_expr, other_dag, b_expr)  # type: ignore[arg-type]
    else:
        eq = equivalent(other_dag, a_expr, item.dag, b_expr)  # type: ignore[arg-type]
    # Broken candidates sort first. Prefer operations touching smaller graphs less only after break status.
    return (0 if eq is False else 1, len(item.dag.directed_edges), len(item.dag.nodes))


def attack_ast_identity(rec: dict[str, Any], max_budget: int, beam_width: int, max_candidates: int) -> dict[str, Any]:
    expr: Expression = rec["expr"]
    original = rec["consequence_key"]
    protected = mentioned(expr)
    states = [AttackDAG(rec["dag"], tuple())]
    seen = {(states[0].dag.nodes, states[0].dag.directed_edges)}
    tested = 0
    best_ops: tuple[str, ...] = tuple()
    for cost in range(1, max_budget + 1):
        candidates: list[AttackDAG] = []
        for state in states:
            for cand in adversarial_candidates(state.dag, protected=protected, limit_per_family=max(4, max_candidates // 12)):
                key = (cand.dag.nodes, cand.dag.directed_edges)
                if key in seen:
                    continue
                seen.add(key)
                candidates.append(AttackDAG(cand.dag, state.operations + cand.operations))
        if not candidates:
            break
        scored = []
        for cand in candidates[: max_candidates * 2]:
            try:
                changed = freeze_signature(consequence_signature(cand.dag, expr)) != original
            except Exception:
                continue
            scored.append((0 if changed else 1, len(cand.dag.directed_edges), len(cand.dag.nodes), cand, changed))
        scored.sort(key=lambda x: x[:3])
        next_states = []
        for _, _, _, cand, changed in scored[:max_candidates]:
            tested += 1
            if changed:
                return {"broken": True, "cost": cost, "operations": list(cand.operations), "tested": tested, "valid": True}
            next_states.append(cand)
            best_ops = cand.operations
        states = next_states[:beam_width]
        if not states:
            break
    return {"broken": False, "cost": None, "operations": list(best_ops), "tested": tested, "valid": True}


def attack_pair(pair: tuple[dict[str, Any], dict[str, Any]], max_budget: int, beam_width: int, max_candidates: int, mode: str) -> dict[str, Any]:
    a, b = pair
    a_expr: Expression = a["expr"]
    b_expr: Expression = b["expr"]
    if mode == "same_sync":
        if a["dag_id"] != b["dag_id"]:
            return {"broken": False, "cost": None, "operations": [], "tested": 0, "mode": mode, "valid": False}
        base_states = [AttackDAG(a["dag"], tuple())]
        other_dag = None
        protected = mentioned(a_expr) | mentioned(b_expr)
    elif mode == "left_only":
        base_states = [AttackDAG(a["dag"], tuple())]
        other_dag = b["dag"]
        protected = mentioned(a_expr)
    elif mode == "right_only":
        base_states = [AttackDAG(b["dag"], tuple())]
        other_dag = a["dag"]
        protected = mentioned(b_expr)
    else:
        raise ValueError(mode)

    initial_eq = equivalent(a["dag"], a_expr, b["dag"], b_expr)
    if initial_eq is not True:
        return {"broken": False, "cost": None, "operations": [], "tested": 0, "mode": mode, "valid": False}

    tested = 0
    states = base_states
    seen = {(states[0].dag.nodes, states[0].dag.directed_edges)}
    best_ops: tuple[str, ...] = tuple()
    for cost in range(1, max_budget + 1):
        candidates: list[AttackDAG] = []
        for state in states:
            for cand in adversarial_candidates(state.dag, protected=protected, limit_per_family=max(4, max_candidates // 12)):
                key = (cand.dag.nodes, cand.dag.directed_edges)
                if key in seen:
                    continue
                seen.add(key)
                candidates.append(AttackDAG(cand.dag, state.operations + cand.operations))
        if not candidates:
            break
        candidates = sorted(candidates, key=lambda c: candidate_score(c, a_expr, b_expr, other_dag, mode))[:max_candidates]
        next_states = []
        for cand in candidates:
            tested += 1
            if mode == "same_sync":
                eq = equivalent(cand.dag, a_expr, cand.dag, b_expr)
            elif mode == "left_only":
                eq = equivalent(cand.dag, a_expr, other_dag, b_expr)  # type: ignore[arg-type]
            else:
                eq = equivalent(other_dag, a_expr, cand.dag, b_expr)  # type: ignore[arg-type]
            if eq is False:
                return {"broken": True, "cost": cost, "operations": list(cand.operations), "tested": tested, "mode": mode, "valid": True}
            if eq is True:
                next_states.append(cand)
                best_ops = cand.operations
        states = next_states[:beam_width]
        if not states:
            break
    return {"broken": False, "cost": None, "operations": list(best_ops), "tested": tested, "mode": mode, "valid": True}


def analyze_classes(records: list[dict[str, Any]], args) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        groups[rec["consequence_key"]].append(rec)
    class_items = sorted(groups.items(), key=lambda kv: (-len(kv[1]), stable_id(kv[0])))
    attack_rows = []
    curve_rows = []
    cross_rows = []
    examples = []
    op_counter: Counter[str] = Counter()
    analyzed = 0
    for sig_key, group in class_items:
        if analyzed >= args.max_analyzed_classes:
            break
        same_pairs = same_dag_pairs(group, args.pairs_per_class)
        cross_pairs = cross_dag_pairs(group, args.cross_pairs_per_class)
        if not same_pairs and not cross_pairs:
            continue
        analyzed += 1
        class_id = stable_id(sig_key)
        all_results = []
        alias_pairs = 0
        nontrivial_pairs = 0
        for pair in same_pairs:
            alias = is_operator_alias_pair(pair[0], pair[1])
            alias_pairs += int(alias)
            nontrivial_pairs += int(not alias)
            res = attack_pair(pair, args.max_attack_budget, args.beam_width, args.candidate_budget, "same_sync")
            res.update({"pair_type": "same_dag", "alias_pair": alias})
            all_results.append(res)
        for pair in cross_pairs:
            alias = is_operator_alias_pair(pair[0], pair[1])
            alias_pairs += int(alias)
            nontrivial_pairs += int(not alias)
            left = attack_pair(pair, args.max_attack_budget, args.beam_width, args.candidate_budget, "left_only")
            right = attack_pair(pair, args.max_attack_budget, args.beam_width, args.candidate_budget, "right_only")
            res = left if (left["broken"] or not right["broken"] or (left.get("cost") or 999) <= (right.get("cost") or 999)) else right
            res.update({"pair_type": "cross_dag", "alias_pair": alias})
            all_results.append(res)
            cross_rows.append({
                "class_id": class_id,
                "broken": res["broken"],
                "attack_cost": res["cost"],
                "mode": res["mode"],
                "alias_pair": alias,
                "operations": ";".join(res["operations"]),
            })
        valid = [r for r in all_results if r["valid"]]
        broken = [r for r in valid if r["broken"]]
        costs = [int(r["cost"]) for r in broken if r["cost"] is not None]
        min_cost = min(costs) if costs else None
        for r in broken:
            op_counter.update(r["operations"])
        for k in K_VALUES:
            if k == 0:
                persistence = 1.0
            elif valid:
                persistence = sum(1 for r in valid if not (r["broken"] and r["cost"] is not None and int(r["cost"]) <= k)) / len(valid)
            else:
                persistence = None
            curve_rows.append({"class_id": class_id, "k": k, "persistence": persistence, "class_size": len(group)})
        old_gns = 1.0
        vals = [row["persistence"] for row in curve_rows if row["class_id"] == class_id and row["k"] > 0 and row["persistence"] is not None]
        attack_auc_gns = sum(vals) / len(vals) if vals else None
        ops = sorted({r["operator"] for r in group})
        depths = sorted({int(r["depth"]) for r in group})
        dags = sorted({r["dag_id"] for r in group})
        row = {
            "class_id": class_id,
            "class_size": len(group),
            "analyzed_pair_count": len(valid),
            "same_dag_pair_count": len(same_pairs),
            "cross_dag_pair_count": len(cross_pairs),
            "alias_pair_count": alias_pairs,
            "nontrivial_pair_count": nontrivial_pairs,
            "alias_pair_fraction": alias_pairs / max(1, alias_pairs + nontrivial_pairs),
            "broken": bool(broken),
            "attack_cost": min_cost,
            "old_gns": old_gns,
            "attack_auc_gns": attack_auc_gns,
            "persistence_k1": next(c["persistence"] for c in curve_rows if c["class_id"] == class_id and c["k"] == 1),
            "persistence_k2": next(c["persistence"] for c in curve_rows if c["class_id"] == class_id and c["k"] == 2),
            "persistence_k3": next(c["persistence"] for c in curve_rows if c["class_id"] == class_id and c["k"] == 3),
            "persistence_k4": next(c["persistence"] for c in curve_rows if c["class_id"] == class_id and c["k"] == 4),
            "operator_diversity": len(ops),
            "operators": ";".join(ops),
            "depth_min": min(depths),
            "depth_max": max(depths),
            "dag_diversity": len(dags),
            "representative": " || ".join(sorted({r["surface"] for r in group})[:3]),
        }
        attack_rows.append(row)
        if broken and len(examples) < args.max_examples:
            first = broken[0]
            examples.append({
                "class_id": class_id,
                "attack_cost": first["cost"],
                "mode": first["mode"],
                "pair_type": first["pair_type"],
                "alias_pair": first["alias_pair"],
                "operations": first["operations"],
                "representative": row["representative"],
            })
    op_rows = [{"operation": op, "broken_pair_count": count} for op, count in op_counter.most_common()]
    return pd.DataFrame(attack_rows), pd.DataFrame(curve_rows), pd.DataFrame(cross_rows), {"operation_counts": op_rows}, examples


def baseline_attacks(records: list[dict[str, Any]], args) -> dict[str, Any]:
    rng = random.Random(args.seed + 1701)
    by_feature: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        by_feature[rec["feature_key"]].append(rec)

    def collect_pairs(groups, max_pairs):
        pairs = []
        for group in groups:
            pairs.extend(same_dag_pairs(group, 1))
            if len(pairs) >= max_pairs:
                break
        return pairs[:max_pairs]

    feature_pairs = collect_pairs(list(by_feature.values()), args.baseline_pairs)
    random_pairs = []
    by_dag = defaultdict(list)
    for r in records:
        by_dag[r["dag_id"]].append(r)
    for items in by_dag.values():
        if len(items) >= 2:
            random_pairs.append(tuple(rng.sample(items, 2)))
        if len(random_pairs) >= args.baseline_pairs:
            break
    ast_records = rng.sample(records, min(args.baseline_pairs, len(records)))

    out = {}
    for name, pairs in (("feature", feature_pairs), ("random", random_pairs)):
        costs = []
        initially_equal = 0
        broken = 0
        invalid_or_prebroken = 0
        for pair in pairs:
            base_eq = equivalent(pair[0]["dag"], pair[0]["expr"], pair[1]["dag"], pair[1]["expr"])
            if base_eq is not True:
                invalid_or_prebroken += 1
                broken += 1
                costs.append(0)
                continue
            initially_equal += 1
            res = attack_pair(pair, args.max_attack_budget, args.beam_width, max(8, args.candidate_budget // 2), "same_sync")
            if res["broken"]:
                broken += 1
                costs.append(res["cost"])
        out[name] = {
            "pair_count": len(pairs),
            "initially_equal_count": initially_equal,
            "invalid_or_prebroken_count": invalid_or_prebroken,
            "initial_equivalence_rate": initially_equal / len(pairs) if pairs else None,
            "broken_fraction": broken / len(pairs) if pairs else None,
            "mean_attack_cost": sum(costs) / len(costs) if costs else None,
            "min_attack_cost": min(costs) if costs else None,
        }

    ast_costs = []
    ast_broken = 0
    for rec in ast_records:
        res = attack_ast_identity(rec, args.max_attack_budget, args.beam_width, max(8, args.candidate_budget // 2))
        if res["broken"]:
            ast_broken += 1
            ast_costs.append(res["cost"])
    out["ast_identity"] = {
        "expression_count": len(ast_records),
        "initial_equivalence_rate": 1.0 if ast_records else None,
        "broken_fraction": ast_broken / len(ast_records) if ast_records else None,
        "mean_attack_cost": sum(ast_costs) / len(ast_costs) if ast_costs else None,
        "min_attack_cost": min(ast_costs) if ast_costs else None,
    }
    return out


def decide(df: pd.DataFrame, cross: pd.DataFrame, baselines: dict[str, Any]) -> dict[str, Any]:
    analyzed = len(df)
    broken = int(df["broken"].sum()) if analyzed else 0
    survive_frac = 1 - broken / analyzed if analyzed else 0.0
    costs = [int(v) for v in df["attack_cost"].dropna()]
    low_cost_frac = sum(1 for c in costs if c <= 1) / analyzed if analyzed else 0.0
    spectrum = len(set(costs)) >= 3 or (df["attack_auc_gns"].nunique() > 5 if len(df) else False)
    nontrivial_broken = int(((df["broken"] == True) & (df["nontrivial_pair_count"] > 0)).sum()) if analyzed else 0
    if analyzed == 0:
        label = "Verifier_artifact"
        reason = "No analyzable classes."
    elif survive_frac > 0.95:
        label = "Backbone_survives"
        reason = ">95% of classes remain frozen under adversarial search."
    elif low_cost_frac > 0.5:
        label = "Weak_backbone"
        reason = "Most analyzed classes fail under low-cost adversarial attacks."
    elif spectrum:
        label = "Backbone_spectrum"
        reason = "A nontrivial attack-cost spectrum emerged."
    else:
        label = "Backbone_spectrum"
        reason = "Some classes break but not enough for weak-backbone classification."
    return {
        "classification": label,
        "reason": reason,
        "evidence": {
            "analyzed_class_count": analyzed,
            "broken_class_count": broken,
            "surviving_class_count": analyzed - broken,
            "surviving_fraction": survive_frac,
            "min_attack_cost": min(costs) if costs else None,
            "mean_attack_cost_broken": sum(costs) / len(costs) if costs else None,
            "nontrivial_broken_class_count": nontrivial_broken,
            "mean_attack_auc_gns": float(df["attack_auc_gns"].dropna().mean()) if analyzed else None,
            "old_gns_mean": float(df["old_gns"].mean()) if analyzed else None,
            "cross_dag_broken_fraction": float(cross["broken"].mean()) if len(cross) else None,
            "feature_broken_fraction": baselines.get("feature", {}).get("broken_fraction"),
            "ast_broken_fraction": baselines.get("ast_identity", {}).get("broken_fraction"),
            "random_broken_fraction": baselines.get("random", {}).get("broken_fraction"),
        },
    }


def plot_outputs(df: pd.DataFrame, curves: pd.DataFrame, out: Path) -> None:
    if len(curves):
        mean_curve = curves.groupby("k", as_index=False)["persistence"].mean()
        fig, ax = plt.subplots(figsize=(8, 5)); ax.plot(mean_curve["k"], mean_curve["persistence"], marker="o")
        ax.set_ylim(-0.02, 1.02); ax.set_xlabel("attack budget"); ax.set_ylabel("mean persistence"); ax.set_title("Attack curves")
        ax.grid(True, alpha=0.3); fig.tight_layout(); fig.savefig(out / "attack_curves.png", dpi=130); plt.close(fig)
        fig, ax = plt.subplots(figsize=(8, 5)); ax.plot(mean_curve["k"], mean_curve["persistence"], marker="o", color="tab:red")
        ax.set_ylim(-0.02, 1.02); ax.set_xlabel("attack budget"); ax.set_ylabel("persistence"); ax.set_title("Persistence vs attack budget")
        ax.grid(True, alpha=0.3); fig.tight_layout(); fig.savefig(out / "persistence_vs_attack_budget.png", dpi=130); plt.close(fig)
    if len(df):
        fig, ax = plt.subplots(figsize=(8, 5)); ax.hist(df["attack_cost"].dropna(), bins=range(1, 7), align="left")
        ax.set_xlabel("attack cost"); ax.set_ylabel("class count"); ax.set_title("Attack-cost histogram")
        fig.tight_layout(); fig.savefig(out / "attack_cost_histogram.png", dpi=130); plt.close(fig)
        for xcol, fname, title in [
            ("depth_max", "attack_cost_vs_depth.png", "Attack cost vs depth"),
            ("dag_diversity", "attack_cost_vs_dag_diversity.png", "Attack cost vs DAG diversity"),
            ("operator_diversity", "attack_cost_vs_operator_diversity.png", "Attack cost vs operator diversity"),
        ]:
            fig, ax = plt.subplots(figsize=(8, 5));
            ax.scatter(df[xcol], df["attack_auc_gns"], s=12, alpha=0.7)
            ax.set_xlabel(xcol); ax.set_ylabel("attack AUC GNS"); ax.set_title(title); ax.grid(True, alpha=0.3)
            fig.tight_layout(); fig.savefig(out / fname, dpi=130); plt.close(fig)


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
            elif isinstance(v, float): vals.append(f"{v:.6g}")
            else: vals.append(str(v).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_summary(path: Path, args, decision, df: pd.DataFrame, curves: pd.DataFrame, cross: pd.DataFrame, baselines, alias_report, op_report) -> None:
    ev = decision["evidence"]
    top_broken = df[df["broken"] == True].sort_values("attack_cost").head(8)
    lines = [
        "# Experiment 17A.1 - Adversarial Backbone Stress Test",
        "",
        "## Decision",
        "",
        f"Classification: `{decision['classification']}`.",
        "",
        decision["reason"],
        "",
        "## Run Parameters",
        "",
        f"- seed: {args.seed}", f"- num_dags: {args.num_dags}", f"- max_depth: {args.max_depth}",
        f"- max_analyzed_classes: {args.max_analyzed_classes}", f"- candidate_budget: {args.candidate_budget}",
        f"- beam_width: {args.beam_width}", f"- max_attack_budget: {args.max_attack_budget}",
        "",
        "## Required Questions",
        "",
        f"1. Can any frozen class be broken? {'Yes' if ev['broken_class_count'] else 'No'}.",
        f"2. If yes, what is minimum attack cost? {ev['min_attack_cost'] if ev['min_attack_cost'] is not None else 'none found'}.",
        f"3. How many classes remain frozen under adversarial search? {ev['surviving_class_count']} / {ev['analyzed_class_count']}.",
        f"4. Does a spectrum emerge? {'Yes' if decision['classification'] == 'Backbone_spectrum' else 'No'}.",
        f"5. Is GNS still constant? {'Yes' if df['attack_auc_gns'].nunique() <= 1 else 'No'}; mean attack-AUC GNS={ev['mean_attack_auc_gns']:.6g}.",
        f"6. Which perturbation family is most destructive? {op_report['operation_counts'][0]['operation'] if op_report['operation_counts'] else 'none'}.",
        f"7. Do attacks mostly break aliases or genuinely semantic classes? nontrivial broken classes={ev['nontrivial_broken_class_count']}, alias pair mean={alias_report['alias_pair_fraction_mean']:.6g}.",
        f"8. Do cross-DAG attacks behave differently? cross-DAG broken fraction={ev['cross_dag_broken_fraction'] if ev['cross_dag_broken_fraction'] is not None else 'none'}.",
        "",
        "## Core Evidence",
        "",
        f"- analyzed classes: {ev['analyzed_class_count']}",
        f"- broken classes: {ev['broken_class_count']}",
        f"- surviving fraction: {ev['surviving_fraction']:.6g}",
        f"- old GNS mean: {ev['old_gns_mean']:.6g}",
        f"- attack-AUC GNS mean: {ev['mean_attack_auc_gns']:.6g}",
        "",
        "## Baselines",
        "",
        f"- feature broken fraction: {ev['feature_broken_fraction']}",
        f"- AST identity broken fraction: {ev['ast_broken_fraction']}",
        f"- random broken fraction: {ev['random_broken_fraction']}",
        "",
        "## Minimal Broken Examples",
        "",
        markdown_table(top_broken[["class_id", "class_size", "attack_cost", "attack_auc_gns", "nontrivial_pair_count", "alias_pair_fraction", "operators", "representative"]]) if len(top_broken) else "No broken classes found.",
        "",
        "## Honesty Notes",
        "",
        "- This is adversarial search over bounded candidate sequences, not exhaustive graph-edit enumeration.",
        "- The verifier and consequence signatures are unchanged from Experiment 16.",
        "- Same-DAG synchronous attacks and cross-DAG one-sided attacks are both measured.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 17A: adversarial backbone stress test")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-dags", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--exprs-per-dag-depth", type=int, default=80)
    parser.add_argument("--max-analyzed-classes", type=int, default=1200)
    parser.add_argument("--pairs-per-class", type=int, default=2)
    parser.add_argument("--cross-pairs-per-class", type=int, default=2)
    parser.add_argument("--max-attack-budget", type=int, default=4)
    parser.add_argument("--candidate-budget", type=int, default=100)
    parser.add_argument("--beam-width", type=int, default=8)
    parser.add_argument("--baseline-pairs", type=int, default=300)
    parser.add_argument("--max-examples", type=int, default=25)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17A")
    args = parser.parse_args()

    out = ensure(args.outputs)
    t0 = time.perf_counter()
    records = build_records(args.seed, args.num_dags, args.max_depth, args.exprs_per_dag_depth)
    build_sec = time.perf_counter() - t0
    t1 = time.perf_counter()
    attack_df, curve_df, cross_df, op_report, examples = analyze_classes(records, args)
    attack_sec = time.perf_counter() - t1
    t2 = time.perf_counter()
    baselines = baseline_attacks(records, args)
    baseline_sec = time.perf_counter() - t2
    alias_report = {
        "alias_pair_fraction_mean": float(attack_df["alias_pair_fraction"].mean()) if len(attack_df) else 0.0,
        "classes_with_nontrivial_pairs": int((attack_df["nontrivial_pair_count"] > 0).sum()) if len(attack_df) else 0,
        "classes_with_alias_only_pairs": int((attack_df["nontrivial_pair_count"] == 0).sum()) if len(attack_df) else 0,
        "broken_nontrivial_classes": int(((attack_df["broken"] == True) & (attack_df["nontrivial_pair_count"] > 0)).sum()) if len(attack_df) else 0,
    }
    decision = decide(attack_df, cross_df, baselines)

    attack_df.to_csv(out / "attack_cost.csv", index=False)
    curve_df.to_csv(out / "attack_curve.csv", index=False)
    attack_df[attack_df["broken"] == True].to_csv(out / "broken_classes.csv", index=False)
    cross_df.to_csv(out / "cross_dag_attack.csv", index=False)
    write_json(out / "minimal_attack_examples.json", examples)
    write_json(out / "alias_attack_report.json", alias_report)
    write_json(out / "baseline_attack_report.json", baselines)
    write_json(out / "operation_destructiveness.json", op_report)
    write_json(out / "final_decision.json", decision)
    pd.DataFrame([
        {"stage": "build_records", "runtime_sec": build_sec, "items": len(records), "runtime_per_item_sec": build_sec / max(1, len(records))},
        {"stage": "adversarial_attack", "runtime_sec": attack_sec, "items": len(attack_df), "runtime_per_item_sec": attack_sec / max(1, len(attack_df))},
        {"stage": "baselines", "runtime_sec": baseline_sec, "items": args.baseline_pairs, "runtime_per_item_sec": baseline_sec / max(1, args.baseline_pairs)},
    ]).to_csv(out / "complexity_report.csv", index=False)
    plot_outputs(attack_df, curve_df, out)
    write_summary(out / "summary.md", args, decision, attack_df, curve_df, cross_df, baselines, alias_report, op_report)

    print(json.dumps({
        "classification": decision["classification"],
        "num_expressions": len(records),
        "analyzed_classes": decision["evidence"]["analyzed_class_count"],
        "broken_classes": decision["evidence"]["broken_class_count"],
        "surviving_fraction": decision["evidence"]["surviving_fraction"],
        "min_attack_cost": decision["evidence"]["min_attack_cost"],
        "mean_attack_auc_gns": decision["evidence"]["mean_attack_auc_gns"],
        "outputs": str(out),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
