from __future__ import annotations

import random
from collections import defaultdict
from typing import Any

INTERVENTION_OPS = {"P_do", "P_do_cond", "P_multi_do", "Effect"}
CONDITIONAL_OPS = {"Independent", "Blocked", "P_do_cond"}


def group_records(records: list[dict[str, Any]]) -> dict[Any, list[dict[str, Any]]]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        groups[rec["consequence_key"]].append(rec)
    return groups


def class_features(records: list[dict[str, Any]]) -> dict[Any, dict[str, Any]]:
    groups = group_records(records)
    max_size = max((len(v) for v in groups.values()), default=1)
    max_dag = max((len({r["dag_id"] for r in v}) for v in groups.values()), default=1)
    max_depth = max((int(r["depth"]) for r in records), default=1)
    table = {}
    for key, items in groups.items():
        ops = {r["operator"] for r in items}
        dags = {r["dag_id"] for r in items}
        depths = {int(r["depth"]) for r in items}
        intervention = sum(1 for r in items if r["operator"] in INTERVENTION_OPS) / len(items)
        conditional = sum(1 for r in items if r["operator"] in CONDITIONAL_OPS) / len(items)
        freq = len(items) / max_size
        dag_div = len(dags) / max_dag
        op_div = min(1.0, len(ops) / 3.0)
        depth_score = max(depths) / max_depth
        complexity = 1.0 + max(depths) + len(ops)
        signature_len = len(repr(key))
        table[key] = {
            "class_size": len(items),
            "freq": freq,
            "dag_diversity": len(dags),
            "dag_div_score": dag_div,
            "operator_diversity": len(ops),
            "op_div_score": op_div,
            "depth_min": min(depths),
            "depth_max": max(depths),
            "depth_score": depth_score,
            "intervention_score": intervention,
            "conditional_score": conditional,
            "role_score": max(intervention, conditional),
            "complexity": complexity,
            "signature_len": signature_len,
            "operators": ";".join(sorted(ops)),
            "representative": " || ".join(sorted({r["surface"] for r in items})[:3]),
        }
    return table


def original_score(row: dict[str, Any]) -> float:
    return 0.30 * row["freq"] + 0.25 * row["dag_div_score"] + 0.20 * row["op_div_score"] + 0.15 * row["depth_score"] + 0.10 * row["role_score"]


def reuse_scores(table: dict[Any, dict[str, Any]], base: dict[Any, float] | None = None, iterations: int = 4) -> dict[Any, float]:
    scores = dict(base) if base else {k: 1.0 for k in table}
    for _ in range(iterations):
        op_mass = defaultdict(float)
        depth_mass = defaultdict(float)
        for key, row in table.items():
            for op in row["operators"].split(";"):
                if op:
                    op_mass[op] += scores[key]
            depth_mass[row["depth_max"]] += scores[key]
        max_op = max(op_mass.values(), default=1.0)
        max_depth = max(depth_mass.values(), default=1.0)
        nxt = {}
        for key, row in table.items():
            ops = [op for op in row["operators"].split(";") if op]
            op_reuse = sum(op_mass[o] for o in ops) / max(1, len(ops)) / max_op if ops else 0.0
            depth_reuse = depth_mass[row["depth_max"]] / max_depth
            nxt[key] = 0.7 * op_reuse + 0.3 * depth_reuse
        scores = nxt
    return scores


def compute_metric_scores(records: list[dict[str, Any]], seed: int = 42) -> tuple[dict[Any, dict[str, Any]], dict[str, dict[Any, float]]]:
    table = class_features(records)
    m1_base = {k: original_score(v) for k, v in table.items()}
    m1_reuse = reuse_scores(table, m1_base)
    m1 = {k: 0.55 * m1_base[k] + 0.45 * m1_reuse[k] for k in table}
    m2 = {k: v["intervention_score"] for k, v in table.items()}
    m3 = reuse_scores(table)
    m4 = {k: (v["class_size"] * (0.5 + v["dag_div_score"])) / max(1.0, v["complexity"] + 0.01 * v["signature_len"]) for k, v in table.items()}
    # Internal centrality proxy: high role, high reuse, low redundancy/complexity.
    m5 = {k: 0.45 * m3[k] + 0.30 * table[k]["role_score"] + 0.25 * (table[k]["op_div_score"] / max(1.0, table[k]["complexity"] / 4.0)) for k in table}
    m6 = {k: 0.55 * v["freq"] + 0.45 * v["dag_div_score"] for k, v in table.items()}
    rng = random.Random(seed)
    keys = list(table)
    vals = list(m1.values())
    rng.shuffle(vals)
    m7 = {k: vals[i] for i, k in enumerate(keys)}
    return table, {"M1_original": m1, "M2_intervention": m2, "M3_reuse": m3, "M4_compression": m4, "M5_perturbation_centrality": m5, "M6_frequency_control": m6, "M7_random_matched": m7}


def select_top_fraction(scores: dict[Any, float], fraction: float) -> set[Any]:
    if not scores:
        return set()
    n = max(1, int(round(len(scores) * fraction)))
    return {k for k, _ in sorted(scores.items(), key=lambda kv: (kv[1], repr(kv[0])), reverse=True)[:n]}
