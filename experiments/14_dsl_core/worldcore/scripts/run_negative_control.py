#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from collections import deque
from pathlib import Path

from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from worldcore.experiments import ensure_output_dir, save_line_plot, write_csv, write_json
from worldcore.metrics import answer_accuracy


TASKS = ("reachability", "shortest_bucket", "ancestor", "disconnected", "cycle")


def graph_example(rng: random.Random, n: int, task: str) -> dict[str, object]:
    edges = set()
    for left in range(n):
        for right in range(n):
            if left != right and rng.random() < min(0.25, 2.0 / n):
                edges.add((left, right))
    src, dst = rng.randrange(n), rng.randrange(n)
    reachable, dist = bfs(n, edges, src, dst)
    has_cycle = any(bfs(n, edges, node, node, allow_zero=False)[0] for node in range(n))
    if task == "reachability":
        answer = str(reachable)
    elif task == "shortest_bucket":
        answer = "none" if not reachable else ("short" if dist <= 2 else "long")
    elif task == "ancestor":
        answer = str(reachable and src < dst)
    elif task == "disconnected":
        answer = str(not reachable)
    else:
        answer = str(has_cycle)
    return {"n": n, "edges": sorted(edges), "src": src, "dst": dst, "task": task, "answer": answer}


def bfs(n: int, edges: set[tuple[int, int]], src: int, dst: int, allow_zero: bool = True) -> tuple[bool, int]:
    graph = {node: [] for node in range(n)}
    for left, right in edges:
        graph[left].append(right)
    queue: deque[tuple[int, int]] = deque([(src, 0)])
    seen = {src}
    while queue:
        node, depth = queue.popleft()
        if node == dst and (allow_zero or depth > 0):
            return True, depth
        for nxt in graph[node]:
            if nxt not in seen or (nxt == dst and not allow_zero):
                seen.add(nxt)
                queue.append((nxt, depth + 1))
    return False, -1


def features(example: dict[str, object]) -> dict[str, float]:
    edges = example["edges"]
    n = example["n"]
    out_degree = sum(1 for left, _ in edges if left == example["src"])
    in_degree = sum(1 for _, right in edges if right == example["dst"])
    return {
        "n": n,
        "edge_count": len(edges),
        "density": len(edges) / max(1, n * (n - 1)),
        "src_out_degree": out_degree,
        "dst_in_degree": in_degree,
        f"task:{example['task']}": 1.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-examples", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rng = random.Random(args.seed)
    train = [graph_example(rng, rng.randint(5, 8), TASKS[idx % len(TASKS)]) for idx in range(args.num_examples)]
    ood = [graph_example(rng, rng.randint(14, 24), TASKS[idx % len(TASKS)]) for idx in range(max(1_000, args.num_examples // 4))]
    model = Pipeline([("vec", DictVectorizer()), ("clf", RandomForestClassifier(n_estimators=80, max_depth=7, random_state=args.seed))])
    model.fit([features(ex) for ex in train], [ex["answer"] for ex in train])

    rows = []
    for task in TASKS:
        subset = [ex for ex in ood if ex["task"] == task]
        pred = model.predict([features(ex) for ex in subset])
        rows.append({"task": task, "ood_accuracy": answer_accuracy([ex["answer"] for ex in subset], list(pred)), "count": len(subset)})
    summary = {
        "seed": args.seed,
        "num_examples": args.num_examples,
        "mean_ood_accuracy": sum(row["ood_accuracy"] for row in rows) / len(rows),
        "exposes_failure_mode": any(row["ood_accuracy"] < 0.7 for row in rows),
    }

    out = ensure_output_dir(args.outputs)
    write_json(out / "negative_control_summary.json", summary)
    write_csv(out / "negative_control_ood.csv", rows)
    save_line_plot(out / "negative_control_ood.png", rows, "task", ["ood_accuracy"], "Negative control OOD accuracy")


if __name__ == "__main__":
    main()
