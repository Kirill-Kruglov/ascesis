from __future__ import annotations

from collections import defaultdict
from typing import Any

INTERVENTION_OPS = {"P_do", "P_do_cond", "P_multi_do", "Effect"}
CONDITIONAL_OPS = {"Independent", "Blocked", "P_do_cond"}


def _norm(value: float, max_value: float) -> float:
    return value / max_value if max_value > 0 else 0.0


def group_records(records: list[dict[str, Any]]) -> dict[Any, list[dict[str, Any]]]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        groups[rec["consequence_key"]].append(rec)
    return groups


def class_feature_table(records: list[dict[str, Any]]) -> dict[Any, dict[str, Any]]:
    groups = group_records(records)
    max_size = max((len(v) for v in groups.values()), default=1)
    max_dag_div = max((len({r["dag_id"] for r in v}) for v in groups.values()), default=1)
    max_depth = max((int(r["depth"]) for r in records), default=1)
    table: dict[Any, dict[str, Any]] = {}
    for key, items in groups.items():
        ops = {r["operator"] for r in items}
        dag_ids = {r["dag_id"] for r in items}
        depths = {int(r["depth"]) for r in items}
        intervention_role = sum(1 for r in items if r["operator"] in INTERVENTION_OPS) / len(items)
        conditional_role = sum(1 for r in items if r["operator"] in CONDITIONAL_OPS) / len(items)
        freq = _norm(len(items), max_size)
        dag_div = _norm(len(dag_ids), max_dag_div)
        depth_score = _norm(max(depths), max_depth)
        op_div = min(1.0, len(ops) / 3.0)
        role_score = max(intervention_role, conditional_role)
        # Internal interpreter score: only derivable structural/role quantities.
        raw_score = 0.30 * freq + 0.25 * dag_div + 0.20 * op_div + 0.15 * depth_score + 0.10 * role_score
        table[key] = {
            "class_size": len(items),
            "operator_diversity": len(ops),
            "dag_diversity": len(dag_ids),
            "depth_min": min(depths),
            "depth_max": max(depths),
            "intervention_role": intervention_role,
            "conditional_role": conditional_role,
            "role_score": role_score,
            "raw_score": raw_score,
            "operators": ";".join(sorted(ops)),
            "representative": " || ".join(sorted({r["surface"] for r in items})[:3]),
        }
    return table


def compute_closure_state(records: list[dict[str, Any]], iterations: int = 4, strong_quantile: float = 0.60) -> dict[str, Any]:
    table = class_feature_table(records)
    if not table:
        return {"scores": {}, "active_keys": set(), "dead_keys": set(), "threshold": 1.0, "metrics": {}}
    scores = {key: row["raw_score"] for key, row in table.items()}
    # Closed loop: scores are repeatedly updated by internally active neighbors sharing operators/depth roles.
    for _ in range(iterations):
        op_mass: dict[str, float] = defaultdict(float)
        depth_mass: dict[int, float] = defaultdict(float)
        for key, row in table.items():
            score = scores[key]
            for op in row["operators"].split(";"):
                if op:
                    op_mass[op] += score
            depth_mass[int(row["depth_max"])] += score
        max_op = max(op_mass.values(), default=1.0)
        max_depth = max(depth_mass.values(), default=1.0)
        next_scores = {}
        for key, row in table.items():
            ops = [op for op in row["operators"].split(";") if op]
            reuse = sum(op_mass[op] for op in ops) / max(1, len(ops)) / max_op if ops else 0.0
            depth_reuse = depth_mass[int(row["depth_max"])] / max_depth
            next_scores[key] = 0.55 * row["raw_score"] + 0.30 * reuse + 0.15 * depth_reuse
        scores = next_scores
    ordered = sorted(scores.values())
    idx = min(len(ordered) - 1, max(0, int(len(ordered) * strong_quantile)))
    threshold = ordered[idx]
    active = {key for key, score in scores.items() if score >= threshold}
    dead = set(scores) - active
    loop_reuse_rate = sum(1 for k, row in table.items() if row["operator_diversity"] > 1 or row["dag_diversity"] > 1) / len(table)
    metrics = {
        "num_classes": len(table),
        "closure_participation_rate": len(active) / len(table),
        "mean_interpreter_score": sum(scores.values()) / len(scores),
        "semantic_survival_fraction": len(active) / len(table),
        "dead_consequence_fraction": len(dead) / len(table),
        "loop_reuse_rate": loop_reuse_rate,
        "threshold": threshold,
    }
    return {"scores": scores, "features": table, "active_keys": active, "dead_keys": dead, "threshold": threshold, "metrics": metrics}
