from __future__ import annotations

from typing import Any

from consequence_feature.dag import CausalDAG
from consequence_feature.expressions import Expression


def _bucket_count(value: int) -> str:
    if value <= 0:
        return "0"
    if value == 1:
        return "1"
    if value <= 3:
        return "2-3"
    return "4+"


def _pair_signature(dag: CausalDAG, x: str, y: str, intervened: tuple[str, ...] = (), conditioned: tuple[str, ...] = ()) -> dict[str, Any]:
    graph = dag.remove_incoming(set(intervened)) if intervened else dag
    cond = set(conditioned)
    directed_paths = graph.directed_path_count(x, y)
    return {
        "kind": "pair_consequence",
        "x": x,
        "y": y,
        "intervened": tuple(sorted(intervened)),
        "conditioned": tuple(sorted(conditioned)),
        "reachable": graph.reachable(x, y),
        "ancestor": x in graph.ancestors(y),
        "direct_edge": graph.has_edge(x, y),
        "directed_path_bucket": _bucket_count(directed_paths),
        "d_separated": graph.d_separated(x, y, cond),
        "common_ancestor": bool((graph.ancestors(x) & graph.ancestors(y)) - cond),
    }


def consequence_signature(dag: CausalDAG, expr: Expression) -> dict[str, Any]:
    op = expr.operator
    x, y = expr.x, expr.y
    if op in {"Reachable", "Effect", "Ancestor", "P_do"}:
        intervened = (x,) if op == "P_do" else ()
        return _pair_signature(dag, x, y, intervened=intervened)
    if op == "P_obs":
        sig = _pair_signature(dag, x, y)
        sig["observationally_connected"] = not dag.d_separated(x, y, set())
        return sig
    if op == "P_do_cond":
        return _pair_signature(dag, x, y, intervened=(x,), conditioned=expr.conditioning)
    if op == "P_multi_do":
        return _pair_signature(dag, x, y, intervened=expr.interventions)
    if op in {"Independent", "Blocked"}:
        cond = set(expr.conditioning)
        return {
            "kind": "conditional_consequence",
            "x": x,
            "y": y,
            "conditioned": tuple(sorted(cond)),
            "d_separated": dag.d_separated(x, y, cond),
            "blocked": dag.d_separated(x, y, cond),
            "reachable_x_to_y": dag.reachable(x, y),
            "reachable_y_to_x": dag.reachable(y, x),
            "conditioning_ancestors_x": tuple(sorted(set(expr.conditioning) & dag.ancestors(x))),
            "conditioning_ancestors_y": tuple(sorted(set(expr.conditioning) & dag.ancestors(y))),
        }
    raise ValueError(f"unknown operator {op}")


def freeze_signature(sig: dict[str, Any]) -> tuple[Any, ...]:
    frozen = []
    for key in sorted(sig):
        value = sig[key]
        if isinstance(value, list):
            value = tuple(value)
        elif isinstance(value, set):
            value = tuple(sorted(value))
        frozen.append((key, value))
    return tuple(frozen)
