#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from pathlib import Path

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from worldcore.experiments import ensure_output_dir, save_line_plot, write_csv, write_json
from worldcore.metrics import answer_accuracy


def make_example(rng: random.Random, depth: int, idx: int) -> dict[str, object]:
    symbols = [f"C{idx}_{i}" for i in range(depth + 2)]
    facts = [(symbols[i], symbols[i + 1]) for i in range(depth)]
    positive = rng.random() > 0.25
    query = (symbols[0], symbols[depth] if positive else symbols[-1])
    for _ in range(rng.randint(0, 3)):
        facts.append((f"D{idx}_{rng.randint(0, 9)}", f"D{idx}_{rng.randint(10, 19)}"))
    return {"facts": facts, "query": query, "answer": "true" if positive else "unknown", "depth": depth}


def features(example: dict[str, object]) -> dict[str, float]:
    facts = example["facts"]
    query = example["query"]
    starts = {left for left, _ in facts}
    ends = {right for _, right in facts}
    return {
        "num_rules": len(facts),
        "depth_hint": example["depth"],
        "query_start_seen": float(query[0] in starts),
        "query_end_seen": float(query[1] in ends),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-examples", type=int, default=20_000)
    parser.add_argument("--max-proof-depth", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rng = random.Random(args.seed)
    examples = [make_example(rng, 1 + idx % args.max_proof_depth, idx) for idx in range(args.num_examples)]
    split = int(len(examples) * 0.7)
    train = examples[:split]
    test = examples[split:]
    model = Pipeline([("vec", DictVectorizer()), ("clf", LogisticRegression(max_iter=400, random_state=args.seed))])
    model.fit([features(ex) for ex in train], [ex["answer"] for ex in train])
    predictions = model.predict([features(ex) for ex in test])

    rows = []
    for depth in range(1, args.max_proof_depth + 1):
        depth_examples = [ex for ex in test if ex["depth"] == depth]
        depth_pred = model.predict([features(ex) for ex in depth_examples])
        rows.append(
            {
                "proof_depth": depth,
                "accuracy": answer_accuracy([ex["answer"] for ex in depth_examples], list(depth_pred)),
                "count": len(depth_examples),
            }
        )
    summary = {
        "seed": args.seed,
        "num_examples": args.num_examples,
        "overall_accuracy": answer_accuracy([ex["answer"] for ex in test], list(predictions)),
        "passes_sanity": answer_accuracy([ex["answer"] for ex in test], list(predictions)) >= 0.8,
    }
    out = ensure_output_dir(args.outputs)
    write_json(out / "fld_sanity_summary.json", summary)
    write_csv(out / "fld_accuracy_by_depth.csv", rows)
    save_line_plot(out / "fld_accuracy_by_depth.png", rows, "proof_depth", ["accuracy"], "FLD sanity accuracy by depth")


if __name__ == "__main__":
    main()
