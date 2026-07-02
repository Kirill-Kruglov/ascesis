from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class CausalDAG:
    dag_id: str
    nodes: tuple[str, ...]
    directed_edges: tuple[tuple[str, str], ...]
    edge_probability: float
    seed: int

    def parents(self, node: str) -> set[str]:
        return {a for a, b in self.directed_edges if b == node}

    def children(self, node: str) -> set[str]:
        return {b for a, b in self.directed_edges if a == node}

    def has_edge(self, a: str, b: str) -> bool:
        return (a, b) in self.directed_edges

    def remove_incoming(self, intervened: set[str]) -> "CausalDAG":
        edges = tuple((a, b) for a, b in self.directed_edges if b not in intervened)
        suffix = "do_" + "_".join(sorted(intervened)) if intervened else "obs"
        return CausalDAG(f"{self.dag_id}:{suffix}", self.nodes, edges, self.edge_probability, self.seed)

    def ancestors(self, node: str) -> set[str]:
        out: set[str] = set()
        frontier = list(self.parents(node))
        while frontier:
            cur = frontier.pop()
            if cur in out:
                continue
            out.add(cur)
            frontier.extend(self.parents(cur) - out)
        return out

    def descendants(self, node: str) -> set[str]:
        out: set[str] = set()
        frontier = list(self.children(node))
        while frontier:
            cur = frontier.pop()
            if cur in out:
                continue
            out.add(cur)
            frontier.extend(self.children(cur) - out)
        return out

    def reachable(self, source: str, target: str) -> bool:
        return target in self.descendants(source)

    def skeleton_neighbors(self, node: str) -> set[str]:
        return self.parents(node) | self.children(node)

    def directed_path_count(self, source: str, target: str, limit: int = 8) -> int:
        count = 0
        stack = [(source, {source})]
        while stack and count < limit:
            cur, seen = stack.pop()
            for child in self.children(cur):
                if child == target:
                    count += 1
                elif child not in seen:
                    stack.append((child, seen | {child}))
        return count

    def all_simple_skeleton_paths(self, source: str, target: str, max_paths: int = 2048) -> list[tuple[str, ...]]:
        if source == target:
            return [(source,)]
        paths: list[tuple[str, ...]] = []
        stack = [(source, (source,))]
        while stack and len(paths) < max_paths:
            cur, path = stack.pop()
            for nxt in sorted(self.skeleton_neighbors(cur)):
                if nxt in path:
                    continue
                next_path = path + (nxt,)
                if nxt == target:
                    paths.append(next_path)
                else:
                    stack.append((nxt, next_path))
        return paths

    def is_collider_on_path(self, left: str, mid: str, right: str) -> bool:
        return self.has_edge(left, mid) and self.has_edge(right, mid)

    def path_active(self, path: tuple[str, ...], conditioned: set[str]) -> bool:
        if len(path) <= 2:
            return True
        conditioned_or_desc = set(conditioned)
        for z in conditioned:
            conditioned_or_desc |= self.descendants(z)
        for i in range(1, len(path) - 1):
            left, mid, right = path[i - 1], path[i], path[i + 1]
            collider = self.is_collider_on_path(left, mid, right)
            if collider:
                if mid not in conditioned_or_desc:
                    return False
            elif mid in conditioned:
                return False
        return True

    def d_separated(self, x: str, y: str, conditioned: set[str]) -> bool:
        if x == y:
            return False
        for path in self.all_simple_skeleton_paths(x, y):
            if self.path_active(path, conditioned):
                return False
        return True


def generate_dag(dag_id: str, node_count: int, edge_probability: float, rng: random.Random, seed: int) -> CausalDAG:
    nodes = tuple(f"N{i}" for i in range(node_count))
    order = list(nodes)
    rng.shuffle(order)
    edges: list[tuple[str, str]] = []
    for a, b in combinations(order, 2):
        if rng.random() < edge_probability:
            edges.append((a, b))
    edges = sorted(edges, key=lambda e: (nodes.index(e[0]), nodes.index(e[1])))
    return CausalDAG(dag_id, nodes, tuple(edges), edge_probability, seed)


def generate_dag_grid(seed: int, num_dags: int, node_sizes: tuple[int, ...] = (4, 6, 8, 10), edge_probabilities: tuple[float, ...] = (0.15, 0.25, 0.35)) -> list[CausalDAG]:
    rng = random.Random(seed)
    cells = [(n, p) for n in node_sizes for p in edge_probabilities]
    per_cell = max(1, (num_dags + len(cells) - 1) // len(cells))
    dags: list[CausalDAG] = []
    for node_count, p in cells:
        for idx in range(per_cell):
            if len(dags) >= num_dags:
                break
            dag_seed = rng.randint(0, 2**31 - 1)
            dag_rng = random.Random(dag_seed)
            dag_id = f"dag_n{node_count}_p{str(p).replace('.', '')}_{idx:04d}"
            dags.append(generate_dag(dag_id, node_count, p, dag_rng, dag_seed))
    return dags
