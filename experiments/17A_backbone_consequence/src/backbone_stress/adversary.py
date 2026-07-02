from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from consequence_feature.dag import CausalDAG


@dataclass(frozen=True)
class AttackDAG:
    dag: CausalDAG
    operations: tuple[str, ...]


def has_cycle(nodes: tuple[str, ...], edges: set[tuple[str, str]]) -> bool:
    if any(a == b for a, b in edges):
        return True
    children = {n: set() for n in nodes}
    for a, b in edges:
        children.setdefault(a, set()).add(b)
        children.setdefault(b, set())
    temp: set[str] = set()
    perm: set[str] = set()

    def visit(node: str) -> bool:
        if node in perm:
            return False
        if node in temp:
            return True
        temp.add(node)
        for child in children.get(node, ()):
            if visit(child):
                return True
        temp.remove(node)
        perm.add(node)
        return False

    return any(visit(n) for n in nodes if n not in perm)


def make_dag(base: CausalDAG, nodes: tuple[str, ...], edges: set[tuple[str, str]], suffix: str) -> CausalDAG | None:
    next_edges = set(edges)
    if has_cycle(nodes, next_edges):
        return None
    return CausalDAG(f"{base.dag_id}|{suffix}", nodes, tuple(sorted(next_edges)), base.edge_probability, base.seed)


def descendants(dag: CausalDAG, source: str) -> set[str]:
    return dag.descendants(source)


def simple_directed_paths(dag: CausalDAG, source: str, target: str, max_paths: int = 32) -> list[tuple[str, ...]]:
    paths: list[tuple[str, ...]] = []
    stack = [(source, (source,))]
    while stack and len(paths) < max_paths:
        node, path = stack.pop()
        for child in sorted(dag.children(node)):
            if child == target:
                paths.append(path + (child,))
            elif child not in path:
                stack.append((child, path + (child,)))
    return paths


def _protected_ok(nodes: tuple[str, ...], protected: set[str]) -> bool:
    return protected.issubset(set(nodes))


def adversarial_candidates(dag: CausalDAG, protected: set[str] | None = None, limit_per_family: int = 48) -> list[AttackDAG]:
    protected = protected or set()
    nodes = tuple(dag.nodes)
    edges = set(dag.directed_edges)
    out: list[AttackDAG] = []

    def add_candidate(op: str, new_nodes: tuple[str, ...], new_edges: set[tuple[str, str]], suffix: str) -> None:
        if not _protected_ok(new_nodes, protected):
            return
        new = make_dag(dag, new_nodes, new_edges, suffix)
        if new is not None:
            out.append(AttackDAG(new, (op,)))

    # P1 remove edge.
    for a, b in sorted(edges)[:limit_per_family]:
        add_candidate("P1_remove_edge", nodes, edges - {(a, b)}, f"p1_rm_{a}_{b}")

    # P2 add edge without cycles.
    added = 0
    for a in nodes:
        for b in nodes:
            if a == b or (a, b) in edges:
                continue
            add_candidate("P2_add_edge", nodes, edges | {(a, b)}, f"p2_add_{a}_{b}")
            added += 1
            if added >= limit_per_family:
                break
        if added >= limit_per_family:
            break

    # P3 reverse edge.
    for a, b in sorted(edges)[:limit_per_family]:
        add_candidate("P3_reverse_edge", nodes, (edges - {(a, b)}) | {(b, a)}, f"p3_rev_{a}_{b}")

    # P4 alpha rename internal variable.
    for n in nodes[:limit_per_family]:
        if n in protected:
            continue
        renamed = f"{n}_alpha"
        node_map = {x: (renamed if x == n else x) for x in nodes}
        new_nodes = tuple(node_map[x] for x in nodes)
        new_edges = {(node_map[a], node_map[b]) for a, b in edges}
        add_candidate("P4_alpha_rename", new_nodes, new_edges, f"p4_alpha_{n}")

    # P5 split one edge through a mediator.
    for a, b in sorted(edges)[:limit_per_family]:
        m = f"M_{a}_{b}"
        idx = 0
        while m in nodes:
            idx += 1
            m = f"M_{a}_{b}_{idx}"
        add_candidate("P5_split_mediator", tuple(list(nodes) + [m]), (edges - {(a, b)}) | {(a, m), (m, b)}, f"p5_split_{a}_{b}")

    # P6 delete complete causal path.
    count = 0
    for a, b in combinations(nodes, 2):
        for source, target in ((a, b), (b, a)):
            for path in simple_directed_paths(dag, source, target, max_paths=4):
                if len(path) < 3:
                    continue
                path_edges = set(zip(path, path[1:]))
                add_candidate("P6_delete_path", nodes, edges - path_edges, f"p6_delpath_{source}_{target}_{count}")
                count += 1
                if count >= limit_per_family:
                    break
            if count >= limit_per_family:
                break
        if count >= limit_per_family:
            break

    # P7 replace A->B->C with A->D->C.
    count = 0
    for a, b in sorted(edges):
        if b in protected:
            continue
        for c in sorted(dag.children(b)):
            if (b, c) not in edges:
                continue
            d = f"D_{a}_{b}_{c}"
            idx = 0
            while d in nodes:
                idx += 1
                d = f"D_{a}_{b}_{c}_{idx}"
            new_edges = (edges - {(a, b), (b, c)}) | {(a, d), (d, c)}
            add_candidate("P7_replace_chain", tuple(list(nodes) + [d]), new_edges, f"p7_chain_{a}_{b}_{c}")
            count += 1
            if count >= limit_per_family:
                break
        if count >= limit_per_family:
            break

    # P8 merge two internal nodes.
    count = 0
    internal = [n for n in nodes if n not in protected]
    for u, v in combinations(internal, 2):
        merged = f"J_{u}_{v}"
        idx = 0
        while merged in nodes:
            idx += 1
            merged = f"J_{u}_{v}_{idx}"
        node_map = {n: (merged if n in {u, v} else n) for n in nodes}
        new_nodes = tuple(dict.fromkeys(node_map[n] for n in nodes))
        new_edges = {(node_map[a], node_map[b]) for a, b in edges if node_map[a] != node_map[b]}
        add_candidate("P8_merge_internal_nodes", new_nodes, new_edges, f"p8_merge_{u}_{v}")
        count += 1
        if count >= limit_per_family:
            break

    # P9 split one internal node into two mediators.
    for n in internal[:limit_per_family]:
        n_in, n_out = f"{n}_in", f"{n}_out"
        if n_in in nodes or n_out in nodes:
            continue
        new_nodes = tuple([x for x in nodes if x != n] + [n_in, n_out])
        new_edges: set[tuple[str, str]] = set()
        for a, b in edges:
            if b == n:
                new_edges.add((a, n_in))
            elif a == n:
                new_edges.add((n_out, b))
            else:
                new_edges.add((a, b))
        new_edges.add((n_in, n_out))
        add_candidate("P9_split_node", new_nodes, new_edges, f"p9_splitnode_{n}")

    # P10 replace local subgraph around internal node by equal interface with different internal structure.
    for n in internal[:limit_per_family]:
        parents = sorted(dag.parents(n))
        children = sorted(dag.children(n))
        if not parents or not children:
            continue
        r1, r2 = f"R1_{n}", f"R2_{n}"
        if r1 in nodes or r2 in nodes:
            continue
        new_nodes = tuple([x for x in nodes if x != n] + [r1, r2])
        new_edges = {(a, b) for a, b in edges if a != n and b != n}
        for p in parents:
            new_edges.add((p, r1))
        new_edges.add((r1, r2))
        for c in children:
            new_edges.add((r2, c))
        add_candidate("P10_replace_subgraph", new_nodes, new_edges, f"p10_subgraph_{n}")

    # P11 swap independent causal branches: swap child sets of two non-adjacent internal nodes.
    count = 0
    for u, v in combinations(internal, 2):
        if dag.reachable(u, v) or dag.reachable(v, u) or dag.has_edge(u, v) or dag.has_edge(v, u):
            continue
        cu, cv = dag.children(u), dag.children(v)
        if not cu or not cv:
            continue
        new_edges = set(edges)
        for c in cu:
            new_edges.discard((u, c)); new_edges.add((v, c))
        for c in cv:
            new_edges.discard((v, c)); new_edges.add((u, c))
        add_candidate("P11_swap_branches", nodes, new_edges, f"p11_swap_{u}_{v}")
        count += 1
        if count >= limit_per_family:
            break

    # P12 replace implication with alternative derivation: if direct edge and mediated path coexist, remove direct edge; otherwise add a mediator alternative.
    count = 0
    for a, b in sorted(edges):
        paths = [p for p in simple_directed_paths(dag, a, b, max_paths=8) if len(p) > 2]
        if paths:
            add_candidate("P12_alternative_derivation", nodes, edges - {(a, b)}, f"p12_drop_direct_{a}_{b}")
        else:
            alt = f"ALT_{a}_{b}"
            idx = 0
            while alt in nodes:
                idx += 1
                alt = f"ALT_{a}_{b}_{idx}"
            add_candidate("P12_alternative_derivation", tuple(list(nodes) + [alt]), edges | {(a, alt), (alt, b)}, f"p12_add_alt_{a}_{b}")
        count += 1
        if count >= limit_per_family:
            break

    unique: dict[tuple[tuple[str, ...], tuple[tuple[str, str], ...]], AttackDAG] = {}
    for item in out:
        key = (item.dag.nodes, item.dag.directed_edges)
        unique.setdefault(key, item)
    return sorted(unique.values(), key=lambda x: (x.operations, x.dag.dag_id))
