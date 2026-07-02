from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from consequence_feature.dag import CausalDAG


@dataclass(frozen=True)
class PerturbedDAG:
    dag: CausalDAG
    operations: tuple[str, ...]


def has_cycle(nodes: tuple[str, ...], edges: Iterable[tuple[str, str]]) -> bool:
    children = {n: set() for n in nodes}
    for a, b in edges:
        if a == b:
            return True
        children.setdefault(a, set()).add(b)
        children.setdefault(b, set())
    temp: set[str] = set()
    perm: set[str] = set()

    def visit(n: str) -> bool:
        if n in perm:
            return False
        if n in temp:
            return True
        temp.add(n)
        for c in children.get(n, ()):
            if visit(c):
                return True
        temp.remove(n)
        perm.add(n)
        return False

    return any(visit(n) for n in nodes if n not in perm)


def is_acyclic(dag: CausalDAG) -> bool:
    return not has_cycle(dag.nodes, dag.directed_edges)


def _make(dag: CausalDAG, edges: Iterable[tuple[str, str]], suffix: str, nodes: tuple[str, ...] | None = None) -> CausalDAG | None:
    next_nodes = nodes or dag.nodes
    next_edges = tuple(sorted(set(edges)))
    if has_cycle(next_nodes, next_edges):
        return None
    return CausalDAG(f"{dag.dag_id}|{suffix}", next_nodes, next_edges, dag.edge_probability, dag.seed)


def one_step_perturbations(dag: CausalDAG, protected: set[str] | None = None, limit: int = 128) -> list[PerturbedDAG]:
    protected = protected or set()
    out: list[PerturbedDAG] = []
    nodes = tuple(dag.nodes)
    edges = set(dag.directed_edges)

    # P1: remove one edge.
    for edge in sorted(edges):
        new = _make(dag, edges - {edge}, f"rm_{edge[0]}_{edge[1]}")
        if new is not None:
            out.append(PerturbedDAG(new, ("P1_remove_edge",)))

    # P2: add one edge without cycles.
    for a in nodes:
        for b in nodes:
            if a == b or (a, b) in edges:
                continue
            new = _make(dag, edges | {(a, b)}, f"add_{a}_{b}")
            if new is not None:
                out.append(PerturbedDAG(new, ("P2_add_edge",)))

    # P3: reverse one edge if acyclic.
    for a, b in sorted(edges):
        new_edges = (edges - {(a, b)}) | {(b, a)}
        new = _make(dag, new_edges, f"rev_{a}_{b}")
        if new is not None:
            out.append(PerturbedDAG(new, ("P3_reverse_edge",)))

    # P4: alpha-rename one internal variable not mentioned by the expression pair.
    for n in nodes:
        if n in protected:
            continue
        renamed = f"{n}_alpha"
        if renamed in nodes:
            continue
        node_map = {x: (renamed if x == n else x) for x in nodes}
        next_nodes = tuple(node_map[x] for x in nodes)
        next_edges = tuple((node_map[a], node_map[b]) for a, b in edges)
        new = _make(dag, next_edges, f"alpha_{n}", nodes=next_nodes)
        if new is not None:
            out.append(PerturbedDAG(new, ("P4_alpha_rename",)))

    # P5: replace one edge with an equivalent mediator chain A -> M -> B.
    for a, b in sorted(edges):
        m = f"M_{a}_{b}"
        suffix = 0
        while m in nodes:
            suffix += 1
            m = f"M_{a}_{b}_{suffix}"
        next_nodes = tuple(list(nodes) + [m])
        next_edges = (edges - {(a, b)}) | {(a, m), (m, b)}
        new = _make(dag, next_edges, f"split_{a}_{b}", nodes=next_nodes)
        if new is not None:
            out.append(PerturbedDAG(new, ("P5_split_mediator",)))

    out = sorted(out, key=lambda p: (p.operations, p.dag.dag_id, p.dag.directed_edges, p.dag.nodes))
    return out[:limit]


def perturbation_samples(dag: CausalDAG, k: int, protected: set[str] | None, rng: random.Random, samples: int) -> list[PerturbedDAG]:
    if k == 0:
        return [PerturbedDAG(dag, ("P0_identity",))]
    frontier = [PerturbedDAG(dag, tuple())]
    seen = {(dag.nodes, dag.directed_edges)}
    for _ in range(k):
        next_frontier: list[PerturbedDAG] = []
        for item in frontier:
            candidates = one_step_perturbations(item.dag, protected=protected, limit=96)
            if len(candidates) > samples:
                candidates = rng.sample(candidates, samples)
            for cand in candidates:
                key = (cand.dag.nodes, cand.dag.directed_edges)
                if key in seen:
                    continue
                seen.add(key)
                next_frontier.append(PerturbedDAG(cand.dag, item.operations + cand.operations))
        if not next_frontier:
            return []
        if len(next_frontier) > samples:
            next_frontier = rng.sample(next_frontier, samples)
        frontier = next_frontier
    return frontier[:samples]
