#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXP16_SRC = ROOT.parents[0] / "16_consequence_vs_feature" / "src"
EXP17A_SRC = ROOT.parents[0] / "17A_backbone_consequence" / "src"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(EXP16_SRC))
sys.path.insert(0, str(EXP17A_SRC))

from backbone_stress.adversary import AttackDAG, adversarial_candidates  # noqa: E402
from consequence_feature.dag import CausalDAG, generate_dag_grid  # noqa: E402
from consequence_feature.expressions import Expression, generate_expressions  # noqa: E402
from consequence_feature.verifier import consequence_signature, freeze_signature  # noqa: E402
from semantic_taxonomy.taxonomy import OPERATOR_TAXONOMY  # noqa: E402

K_VALUES = [0, 1, 2, 3, 4]
ALL_OPS = tuple(OPERATOR_TAXONOMY.keys())


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def stable_id(value: Any) -> str:
    import hashlib
    return hashlib.sha1(repr(value).encode("utf-8")).hexdigest()[:16]


def mentioned(expr: Expression) -> set[str]:
    return {expr.x, expr.y, *expr.conditioning, *expr.interventions}


def equivalent(a_dag: CausalDAG, a_expr: Expression, b_dag: CausalDAG, b_expr: Expression) -> bool | None:
    try:
        return freeze_signature(consequence_signature(a_dag, a_expr)) == freeze_signature(consequence_signature(b_dag, b_expr))
    except Exception:
        return None


def build_records(seed: int, num_dags: int, max_depth: int, per_depth_cap: int) -> list[dict[str, Any]]:
    records = []
    dags = generate_dag_grid(seed=seed, num_dags=num_dags)
    for idx, dag in enumerate(dags, start=1):
        rng = random.Random(seed + idx * 104729)
        for expr in generate_expressions(dag, max_depth=max_depth, rng=rng, per_depth_cap=per_depth_cap):
            sig = freeze_signature(consequence_signature(dag, expr))
            records.append({
                "expr": expr,
                "dag": dag,
                "dag_id": dag.dag_id,
                "dag_size": len(dag.nodes),
                "depth": expr.depth,
                "operator": expr.operator,
                "feature_key": expr.feature_key(),
                "consequence_key": sig,
                "surface": expr.surface,
            })
    return records


def is_alias_pair(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ea, eb = a["expr"], b["expr"]
    return ea.x == eb.x and ea.y == eb.y and ea.conditioning == eb.conditioning and ea.interventions == eb.interventions and ea.operator != eb.operator


def pair_score(a: dict[str, Any], b: dict[str, Any]) -> tuple[int, int, int, str]:
    ea, eb = a["expr"], b["expr"]
    return (int(not is_alias_pair(a, b)), int(ea.operator != eb.operator), int(ea.depth != eb.depth), ea.surface + "|" + eb.surface)


def same_dag_pairs(group: list[dict[str, Any]], max_pairs: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_dag = defaultdict(list)
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
    return [p for _, p in candidates[:max_pairs]]


def cross_dag_pairs(group: list[dict[str, Any]], max_pairs: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_dag = defaultdict(list)
    for rec in group:
        by_dag[rec["dag_id"]].append(rec)
    dag_ids = sorted(by_dag)
    out = []
    for i in range(len(dag_ids)):
        for j in range(i + 1, len(dag_ids)):
            left = sorted(by_dag[dag_ids[i]], key=lambda r: (r["operator"], r["surface"]))[:8]
            right = sorted(by_dag[dag_ids[j]], key=lambda r: (r["operator"], r["surface"]))[:8]
            best = max(((pair_score(a, b), (a, b)) for a in left for b in right), key=lambda x: x[0], default=None)
            if best:
                out.append(best)
            if len(out) >= max_pairs:
                break
        if len(out) >= max_pairs:
            break
    out.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in out[:max_pairs]]


def audit_operator(records: list[dict[str, Any]], operator: str, sample_size: int, seed: int) -> dict[str, Any]:
    rng = random.Random(seed + stable_int(operator))
    sample = rng.sample(records, min(sample_size, len(records)))
    tested = 0
    preserved = 0
    changed = 0
    examples = []
    for rec in sample:
        expr = rec["expr"]
        original = rec["consequence_key"]
        candidates = [c for c in adversarial_candidates(rec["dag"], protected=mentioned(expr), limit_per_family=8) if c.operations[0] == operator]
        for cand in candidates[:2]:
            tested += 1
            try:
                next_sig = freeze_signature(consequence_signature(cand.dag, expr))
            except Exception:
                changed += 1
                continue
            if next_sig == original:
                preserved += 1
            else:
                changed += 1
                if len(examples) < 3:
                    examples.append({"surface": expr.surface, "dag_id": rec["dag_id"], "operator": operator})
        if tested >= sample_size:
            break
    base = OPERATOR_TAXONOMY[operator]
    if base["final_class"] == "A":
        final = "A" if changed == 0 else "B"
    elif base["final_class"] == "audit_required":
        final = "A" if tested > 0 and changed == 0 else "B"
    else:
        final = "B"
    return {
        "operator": operator,
        "candidate_class": base["candidate_class"],
        "initial_class": base["final_class"],
        "final_class": final,
        "audit_tested": tested,
        "audit_preserved": preserved,
        "audit_changed": changed,
        "audit_success_rate": preserved / tested if tested else None,
        "justification": base["reason"],
        "failure_examples": examples,
    }


def stable_int(value: str) -> int:
    import hashlib
    return int(hashlib.sha1(value.encode("utf-8")).hexdigest()[:8], 16)


def filtered_candidates(dag: CausalDAG, protected: set[str], allowed_ops: set[str], candidate_budget: int) -> list[AttackDAG]:
    out = [c for c in adversarial_candidates(dag, protected=protected, limit_per_family=max(4, candidate_budget // 12)) if c.operations[0] in allowed_ops]
    return out[:candidate_budget]


def attack_pair_filtered(pair: tuple[dict[str, Any], dict[str, Any]], allowed_ops: set[str], args, mode: str) -> dict[str, Any]:
    a, b = pair
    a_expr, b_expr = a["expr"], b["expr"]
    if mode == "same_sync":
        if a["dag_id"] != b["dag_id"]:
            return {"valid": False, "broken": False, "cost": None}
        states = [AttackDAG(a["dag"], tuple())]
        other = None
        protected = mentioned(a_expr) | mentioned(b_expr)
    elif mode == "left_only":
        states = [AttackDAG(a["dag"], tuple())]
        other = b["dag"]
        protected = mentioned(a_expr)
    else:
        states = [AttackDAG(b["dag"], tuple())]
        other = a["dag"]
        protected = mentioned(b_expr)
    if equivalent(a["dag"], a_expr, b["dag"], b_expr) is not True:
        return {"valid": False, "broken": False, "cost": None}
    seen = {(states[0].dag.nodes, states[0].dag.directed_edges)}
    tested = 0
    for cost in range(1, args.max_attack_budget + 1):
        candidates = []
        for state in states:
            for cand in filtered_candidates(state.dag, protected, allowed_ops, args.candidate_budget):
                key = (cand.dag.nodes, cand.dag.directed_edges)
                if key in seen:
                    continue
                seen.add(key)
                candidates.append(AttackDAG(cand.dag, state.operations + cand.operations))
        if not candidates:
            break
        next_states = []
        for cand in candidates[: args.candidate_budget]:
            tested += 1
            if mode == "same_sync":
                eq = equivalent(cand.dag, a_expr, cand.dag, b_expr)
            elif mode == "left_only":
                eq = equivalent(cand.dag, a_expr, other, b_expr)  # type: ignore[arg-type]
            else:
                eq = equivalent(other, a_expr, cand.dag, b_expr)  # type: ignore[arg-type]
            if eq is False:
                return {"valid": True, "broken": True, "cost": cost, "operations": list(cand.operations), "tested": tested}
            if eq is True:
                next_states.append(cand)
        states = next_states[: args.beam_width]
        if not states:
            break
    return {"valid": True, "broken": False, "cost": None, "operations": [], "tested": tested}


def analyze(records: list[dict[str, Any]], allowed_ops: set[str], args, label: str) -> tuple[dict[str, Any], pd.DataFrame]:
    groups = defaultdict(list)
    for rec in records:
        groups[rec["consequence_key"]].append(rec)
    items = sorted(groups.items(), key=lambda kv: (-len(kv[1]), stable_id(kv[0])))
    rows = []
    analyzed = 0
    for key, group in items:
        if analyzed >= args.max_analyzed_classes:
            break
        pairs = same_dag_pairs(group, args.pairs_per_class) + cross_dag_pairs(group, args.cross_pairs_per_class)
        if not pairs:
            continue
        analyzed += 1
        valid = []
        for pair in pairs:
            if pair[0]["dag_id"] == pair[1]["dag_id"]:
                res = attack_pair_filtered(pair, allowed_ops, args, "same_sync")
            else:
                left = attack_pair_filtered(pair, allowed_ops, args, "left_only")
                right = attack_pair_filtered(pair, allowed_ops, args, "right_only")
                res = left if (left.get("broken") or not right.get("broken")) else right
            if res.get("valid"):
                valid.append(res)
        broken = [r for r in valid if r.get("broken")]
        costs = [int(r["cost"]) for r in broken if r.get("cost") is not None]
        persistence = {}
        for k in K_VALUES:
            if k == 0:
                persistence[k] = 1.0
            elif valid:
                persistence[k] = sum(1 for r in valid if not (r.get("broken") and r.get("cost") is not None and int(r["cost"]) <= k)) / len(valid)
            else:
                persistence[k] = None
        vals = [persistence[k] for k in (1, 2, 3, 4) if persistence[k] is not None]
        auc = sum(vals) / len(vals) if vals else None
        ops = sorted({r["operator"] for r in group})
        rows.append({
            "class_id": stable_id(key),
            "label": label,
            "class_size": len(group),
            "valid_pair_count": len(valid),
            "broken": bool(broken),
            "attack_cost": min(costs) if costs else None,
            "auc_gns": auc,
            "persistence_k1": persistence[1],
            "persistence_k2": persistence[2],
            "persistence_k3": persistence[3],
            "persistence_k4": persistence[4],
            "operator_diversity": len(ops),
            "depth_max": max(int(r["depth"]) for r in group),
            "dag_diversity": len({r["dag_id"] for r in group}),
            "representative": " || ".join(sorted({r["surface"] for r in group})[:3]),
        })
    df = pd.DataFrame(rows)
    summary = summarize_attack_df(df, label, allowed_ops)
    return summary, df


def summarize_attack_df(df: pd.DataFrame, label: str, allowed_ops: set[str]) -> dict[str, Any]:
    n = len(df)
    broken = int(df["broken"].sum()) if n else 0
    costs = [int(v) for v in df["attack_cost"].dropna()] if n else []
    return {
        "label": label,
        "allowed_ops": sorted(allowed_ops),
        "analyzed_class_count": n,
        "broken_class_count": broken,
        "surviving_class_count": n - broken,
        "surviving_fraction": (n - broken) / n if n else 0.0,
        "min_attack_cost": min(costs) if costs else None,
        "mean_attack_cost_broken": sum(costs) / len(costs) if costs else None,
        "mean_auc_gns": float(df["auc_gns"].dropna().mean()) if n else None,
    }


def write_operator_md(path: Path, taxonomy: list[dict[str, Any]]) -> None:
    lines = ["# Operator Classification", "", "| operator | candidate | final | audit tested | changed | justification |", "|---|---:|---:|---:|---:|---|"]
    for row in taxonomy:
        lines.append(f"| {row['operator']} | {row['candidate_class']} | {row['final_class']} | {row['audit_tested']} | {row['audit_changed']} | {row['justification']} |")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_comparison(path: Path, rep: dict[str, Any], theory: dict[str, Any], decision: dict[str, Any]) -> None:
    lines = [
        "# Experiment 17A.2 Comparison", "",
        f"Decision: `{decision['classification']}`", "",
        "## Representation-only", "",
        f"- surviving classes: {rep['surviving_class_count']} / {rep['analyzed_class_count']}",
        f"- broken classes: {rep['broken_class_count']}",
        f"- mean AUC GNS: {rep['mean_auc_gns']}", "",
        "## Theory-changing", "",
        f"- surviving classes: {theory['surviving_class_count']} / {theory['analyzed_class_count']}",
        f"- broken classes: {theory['broken_class_count']}",
        f"- min attack cost: {theory['min_attack_cost']}",
        f"- mean AUC GNS: {theory['mean_auc_gns']}", "",
        "## Interpretation", "",
        decision["interpretation"],
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def decide(rep: dict[str, Any], theory: dict[str, Any], taxonomy: list[dict[str, Any]]) -> dict[str, Any]:
    if not any(r["final_class"] == "A" for r in taxonomy):
        return {"classification": "Taxonomy_failure", "interpretation": "No operator passed representation-preserving audit."}
    if rep["surviving_fraction"] < 0.5:
        return {"classification": "Weak_backbone", "interpretation": "Backbone fails already under representation-preserving transformations."}
    if rep["surviving_fraction"] > 0.95 and theory["surviving_fraction"] < 0.5:
        return {"classification": "Representation_invariant", "interpretation": "Backbone survives representation-preserving edits but fails under theory-changing edits."}
    return {"classification": "Taxonomy_failure", "interpretation": "Class A/B separation produced mixed or ambiguous outcomes."}


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 17A.2 semantic perturbation taxonomy")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-dags", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--exprs-per-dag-depth", type=int, default=80)
    parser.add_argument("--max-analyzed-classes", type=int, default=1200)
    parser.add_argument("--pairs-per-class", type=int, default=2)
    parser.add_argument("--cross-pairs-per-class", type=int, default=2)
    parser.add_argument("--max-attack-budget", type=int, default=4)
    parser.add_argument("--candidate-budget", type=int, default=80)
    parser.add_argument("--beam-width", type=int, default=8)
    parser.add_argument("--audit-samples", type=int, default=400)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17A2")
    args = parser.parse_args()

    out = ensure(args.outputs)
    t0 = time.perf_counter()
    records = build_records(args.seed, args.num_dags, args.max_depth, args.exprs_per_dag_depth)
    taxonomy = [audit_operator(records, op, args.audit_samples, args.seed) for op in ALL_OPS]
    class_a = {r["operator"] for r in taxonomy if r["final_class"] == "A"}
    class_b = set(ALL_OPS) - class_a
    rep_summary, rep_df = analyze(records, class_a, args, "representation_only")
    theory_summary, theory_df = analyze(records, class_b, args, "theory_change")
    decision = decide(rep_summary, theory_summary, taxonomy)
    elapsed = time.perf_counter() - t0

    pd.DataFrame(taxonomy).drop(columns=["failure_examples"]).to_csv(out / "taxonomy.csv", index=False)
    write_operator_md(out / "operator_classification.md", taxonomy)
    write_json(out / "representation_only_summary.json", rep_summary)
    write_json(out / "theory_change_summary.json", theory_summary)
    write_json(out / "final_decision.json", {**decision, "representation_only": rep_summary, "theory_change": theory_summary, "runtime_sec": elapsed})
    rep_df.to_csv(out / "representation_only_attack.csv", index=False)
    theory_df.to_csv(out / "theory_change_attack.csv", index=False)
    write_comparison(out / "comparison.md", rep_summary, theory_summary, decision)
    write_json(out / "audit_failure_examples.json", {r["operator"]: r["failure_examples"] for r in taxonomy if r["failure_examples"]})

    print(json.dumps({
        "classification": decision["classification"],
        "class_A_ops": sorted(class_a),
        "class_B_ops": sorted(class_b),
        "representation_surviving_fraction": rep_summary["surviving_fraction"],
        "theory_surviving_fraction": theory_summary["surviving_fraction"],
        "outputs": str(out),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
