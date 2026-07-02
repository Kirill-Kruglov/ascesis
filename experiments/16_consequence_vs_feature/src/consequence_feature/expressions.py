from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Any

from consequence_feature.dag import CausalDAG


@dataclass(frozen=True)
class Expression:
    expr_id: str
    surface: str
    ast: tuple[Any, ...]
    features: dict[str, Any]
    dag_id: str
    depth: int
    operator: str
    x: str
    y: str
    conditioning: tuple[str, ...] = ()
    interventions: tuple[str, ...] = ()

    def ast_key(self) -> tuple[Any, ...]:
        return self.ast

    def feature_key(self) -> tuple[Any, ...]:
        return (
            self.features["operator_type"],
            tuple(self.features["mentioned_variables"]),
            self.features["num_variables"],
            self.features["has_do"],
            self.features["conditioning_set_size"],
            self.features["surface_template"],
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "expr_id": self.expr_id,
            "surface": self.surface,
            "ast": repr(self.ast),
            "features": self.features,
            "dag_id": self.dag_id,
            "depth": self.depth,
        }


def _features(operator: str, mentioned: tuple[str, ...], has_do: bool, cond_size: int, template: str) -> dict[str, Any]:
    return {
        "operator_type": operator,
        "mentioned_variables": tuple(sorted(mentioned)),
        "num_variables": len(set(mentioned)),
        "has_do": has_do,
        "conditioning_set_size": cond_size,
        "surface_template": template,
    }


def make_expr(dag: CausalDAG, depth: int, operator: str, x: str, y: str, conditioning: tuple[str, ...] = (), interventions: tuple[str, ...] = (), idx: int = 0) -> Expression:
    cond = tuple(sorted(conditioning))
    do_nodes = tuple(sorted(interventions))
    if operator == "Reachable":
        surface = f"Reachable({x}, {y})"
        template = "Reachable(X,Y)"
        has_do = False
    elif operator == "Effect":
        surface = f"Effect({x} -> {y})"
        template = "Effect(X->Y)"
        has_do = False
    elif operator == "Ancestor":
        surface = f"Ancestor({x}, {y})"
        template = "Ancestor(X,Y)"
        has_do = False
    elif operator == "P_obs":
        surface = f"P({y} | {x})"
        template = "P(Y|X)"
        has_do = False
    elif operator == "P_do":
        surface = f"P({y} | do({x}))"
        template = "P(Y|do(X))"
        has_do = True
    elif operator == "P_do_cond":
        z = ", ".join(cond)
        surface = f"P({y} | do({x}), {z})"
        template = "P(Y|do(X),Z)"
        has_do = True
    elif operator == "P_multi_do":
        z = ", ".join(f"do({v})" for v in do_nodes if v != x)
        surface = f"P({y} | do({x}), {z})"
        template = "P(Y|do(X),do(Z))"
        has_do = True
    elif operator == "Independent":
        z = ", ".join(cond)
        surface = f"Independent({x}, {y} | {z})"
        template = "Independent(X,Y|Z)"
        has_do = False
    elif operator == "Blocked":
        z = ", ".join(cond)
        surface = f"Blocked({x}, {y} | {z})"
        template = "Blocked(X,Y|Z)"
        has_do = False
    else:
        raise ValueError(f"unknown operator {operator}")
    mentioned = (x, y) + cond + do_nodes
    ast = (operator, x, y, cond, do_nodes)
    expr_id = f"{dag.dag_id}:d{depth}:{idx:05d}:{operator}"
    return Expression(
        expr_id=expr_id,
        surface=surface,
        ast=ast,
        features=_features(operator, mentioned, has_do, len(cond), template),
        dag_id=dag.dag_id,
        depth=depth,
        operator=operator,
        x=x,
        y=y,
        conditioning=cond,
        interventions=do_nodes,
    )


def expression_candidates_for_depth(dag: CausalDAG, depth: int) -> list[Expression]:
    nodes = list(dag.nodes)
    pairs = [(x, y) for x in nodes for y in nodes if x != y]
    exprs: list[Expression] = []
    idx = 0
    if depth == 1:
        ops = ["Reachable", "Effect", "Ancestor"]
        for op, (x, y) in itertools.product(ops, pairs):
            exprs.append(make_expr(dag, depth, op, x, y, idx=idx)); idx += 1
    elif depth == 2:
        for op, (x, y) in itertools.product(["P_obs", "P_do"], pairs):
            exprs.append(make_expr(dag, depth, op, x, y, interventions=(x,) if op == "P_do" else (), idx=idx)); idx += 1
    elif depth == 3:
        for x, y in pairs:
            for z in nodes:
                if z in (x, y):
                    continue
                for op in ["Independent", "Blocked"]:
                    exprs.append(make_expr(dag, depth, op, x, y, conditioning=(z,), idx=idx)); idx += 1
    elif depth == 4:
        for x, y in pairs:
            for z in nodes:
                if z in (x, y):
                    continue
                exprs.append(make_expr(dag, depth, "P_do_cond", x, y, conditioning=(z,), interventions=(x,), idx=idx)); idx += 1
    elif depth == 5:
        for x, y in pairs:
            for z in nodes:
                if z in (x, y):
                    continue
                exprs.append(make_expr(dag, depth, "P_multi_do", x, y, interventions=(x, z), idx=idx)); idx += 1
    else:
        cond_size = min(2 + max(0, depth - 6), max(1, len(nodes) - 2))
        for x, y in pairs:
            others = [z for z in nodes if z not in (x, y)]
            for cond in itertools.combinations(others, cond_size):
                for op in ["Independent", "Blocked", "P_do_cond"]:
                    interventions = (x,) if op == "P_do_cond" else ()
                    exprs.append(make_expr(dag, depth, op, x, y, conditioning=cond, interventions=interventions, idx=idx)); idx += 1
    return exprs


def generate_expressions(dag: CausalDAG, max_depth: int, rng: random.Random, per_depth_cap: int = 120) -> list[Expression]:
    out: list[Expression] = []
    for depth in range(1, max_depth + 1):
        candidates = expression_candidates_for_depth(dag, depth)
        if len(candidates) > per_depth_cap:
            candidates = rng.sample(candidates, per_depth_cap)
            candidates = sorted(candidates, key=lambda e: e.expr_id)
        out.extend(candidates)
    return out
