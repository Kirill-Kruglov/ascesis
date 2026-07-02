#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    def tqdm(iterable, **_: object):
        return iterable

from worldcore.baselines import (
    fit_statistical_model,
    labels,
    majority_predictions,
    predict_statistical_model,
)
from worldcore.experiments import ensure_output_dir, save_line_plot, write_csv, write_json
from worldcore.generator import generate_adversarial_pair, generate_task, make_rng
from worldcore.metrics import answer_accuracy, novelty_curve
from worldcore.proof import (
    extract_proof,
    proof_novelty_curve,
    shape_counts,
    structural_vector,
    write_proof,
)
from worldcore.solver import answer_query


TRAIN_FAMILIES = ["entailment", "negation", "unknown", "transitivity", "contradiction"]
OOD_FAMILIES = ["implication+transitivity", "transitivity+negation", "causal+temporal", "belief+fact", "part-of+location"]


def solver_predictions(pairs: list[tuple[object, object]]) -> list[str]:
    return [str(answer_query(world, task.query)[0]) for world, task in pairs]


def build_pairs(seed: int, num_worlds: int, max_train: int, depth_train_max: int, depth_test: list[int]) -> tuple[list[tuple[object, object]], list[tuple[object, object]], list[tuple[object, object]]]:
    rng = make_rng(seed)
    train_pairs = []
    train_pool_size = max(num_worlds, max_train)
    for idx in tqdm(range(train_pool_size), desc="proof train pool"):
        family = TRAIN_FAMILIES[idx % len(TRAIN_FAMILIES)]
        depth = 1 + (idx % depth_train_max)
        train_pairs.append(generate_task(rng, f"train_{idx}", family=family, proof_depth=depth, entity_prefix=f"tr{idx}_"))
    train_tasks = [task for _, task in train_pairs]
    train_task_hashes = {task.canonical_task_hash for task in train_tasks}
    train_world_hashes = {task.canonical_world_hash for task in train_tasks}

    ood_pairs = []
    target = max(150, max_train // 10) * len(depth_test)
    idx = 0
    attempts = 0
    while len(ood_pairs) < target and attempts < target * 80:
        depth = max(4, depth_test[len(ood_pairs) % len(depth_test)])
        family = OOD_FAMILIES[idx % len(OOD_FAMILIES)]
        world, task = generate_task(rng, f"ood_{idx}", family=family, proof_depth=depth, entity_prefix=f"ood{idx}_")
        idx += 1
        attempts += 1
        if task.canonical_task_hash in train_task_hashes or task.canonical_world_hash in train_world_hashes:
            continue
        ood_pairs.append((world, task))

    adversarial_pairs = []
    for adv_idx in range(max(20, max_train // 40)):
        adversarial_pairs.extend(generate_adversarial_pair(rng, f"{adv_idx}", entity_prefix="adv_"))
    return train_pairs, ood_pairs, adversarial_pairs


def materialize_proofs(pairs: list[tuple[object, object]], out_dir: Path, limit_files: int | None = None) -> list[dict[str, object]]:
    proofs = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for idx, (world, task) in enumerate(tqdm(pairs, desc="extract proofs")):
        proof = extract_proof(world, task, proof_id=f"proof_{idx:06d}_{task.task_id}")
        proof["metrics"]["proof_id"] = proof["proof_id"]
        proofs.append(proof)
        if limit_files is None or idx < limit_files:
            write_proof(out_dir / f"{proof['proof_id']}.json", proof)
    return proofs


def metrics_rows(proofs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for proof in proofs:
        row = dict(proof["metrics"])
        row["proof_id"] = proof["proof_id"]
        row["world_id"] = proof["world_id"]
        row["task_id"] = proof["task_id"]
        row["answer"] = proof["answer"]
        row["final_conclusion"] = proof["final_conclusion"] or ""
        rows.append(row)
    return rows


def save_proof_space(path: Path, proofs: list[dict[str, object]]) -> None:
    vectors = [structural_vector(proof) for proof in proofs]
    frame = pd.DataFrame(vectors).fillna(0.0)
    if len(frame) < 2:
        return
    values = StandardScaler().fit_transform(frame.values)
    coords = PCA(n_components=2, random_state=0).fit_transform(values)
    shapes = [str(proof["metrics"]["shape"]) for proof in proofs]
    shape_ids = {shape: idx for idx, shape in enumerate(sorted(set(shapes)))}
    colors = [shape_ids[shape] for shape in shapes]
    plt.figure(figsize=(7, 5))
    plt.scatter(coords[:, 0], coords[:, 1], c=colors, s=8, alpha=0.65, cmap="tab10")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Proof structural space")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def save_novelty_comparison(path: Path, world_rows: list[dict[str, object]], task_rows: list[dict[str, object]], proof_rows: list[dict[str, object]]) -> None:
    plt.figure(figsize=(7, 4))
    plt.plot([r["generated"] for r in world_rows], [r["novelty_rate"] for r in world_rows], label="world novelty")
    plt.plot([r["generated"] for r in task_rows], [r["novelty_rate"] for r in task_rows], label="task novelty")
    plt.plot([r["generated"] for r in proof_rows], [r["proof_novelty"] for r in proof_rows], label="proof novelty")
    plt.xlabel("generated")
    plt.ylabel("novelty")
    plt.title("World vs task vs proof novelty")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def save_proof_saturation(path: Path, proof_rows: list[dict[str, object]]) -> None:
    plt.figure(figsize=(7, 4))
    plt.plot([r["generated"] for r in proof_rows], [r["unique"] for r in proof_rows], label="unique proof graphs")
    plt.xlabel("generated proofs")
    plt.ylabel("unique proof graphs")
    plt.title("Proof saturation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def difficulty_rows(proofs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for proof in proofs:
        metrics = proof["metrics"]
        rows.append(
            {
                "proof_id": proof["proof_id"],
                "task_id": proof["task_id"],
                "reasoning_pattern": metrics["reasoning_pattern"],
                "shape": metrics["shape"],
                "difficulty": metrics["difficulty"],
                "minimal_proof_length": metrics["minimal_proof_length"],
                "width": metrics["width"],
                "branching_factor": metrics["branching_factor"],
                "alternative_proofs": metrics["alternative_proofs"],
                "proof_entropy": metrics["proof_entropy"],
                "reuse": metrics["reuse"],
                "fan_in": metrics["fan_in"],
                "estimated_backtracking_complexity": (1 + float(metrics["alternative_proofs"])) * (1 + float(metrics["fan_in"])) * (1 + float(metrics["depth"])),
            }
        )
    return rows


def correlations(proofs: list[dict[str, object]], ood_pairs: list[tuple[object, object]], train_tasks: list[object], seed: int) -> list[dict[str, object]]:
    if not ood_pairs:
        return []
    ood_tasks = [task for _, task in ood_pairs]
    model = fit_statistical_model(list(train_tasks), seed=seed, kind="forest")
    pred = predict_statistical_model(model, ood_tasks)
    correct = [1.0 if p == y else 0.0 for p, y in zip(pred, labels(ood_tasks))]
    by_task = {proof["task_id"]: proof for proof in proofs}
    rows = []
    metrics = ["difficulty", "length", "depth", "width", "proof_entropy", "alternative_proofs", "fan_in", "reuse"]
    for metric in metrics:
        xs = []
        ys = []
        for idx, task in enumerate(ood_tasks):
            proof = by_task.get(task.task_id)
            if proof is None:
                continue
            xs.append(float(proof["metrics"].get(metric, 0.0)))
            ys.append(correct[idx])
        rows.append({"feature": metric, "target": "OOD_correct", "pearson": pearson(xs, ys), "n": len(xs)})
    shape_groups: dict[str, list[float]] = defaultdict(list)
    for idx, task in enumerate(ood_tasks):
        proof = by_task.get(task.task_id)
        if proof:
            shape_groups[str(proof["metrics"]["shape"])].append(correct[idx])
    for shape, values in sorted(shape_groups.items()):
        rows.append({"feature": f"shape:{shape}", "target": "OOD_accuracy", "pearson": "", "n": len(values), "accuracy": sum(values) / len(values)})
    return rows


def forced_length_audit(seed: int, mins: list[int], train_n: int, test_n: int, attempt_multiplier: int = 8) -> list[dict[str, object]]:
    rows = []
    for min_len in mins:
        rng = make_rng(seed + min_len)
        train_pairs = []
        test_pairs = []
        train_attempts = train_n * attempt_multiplier
        test_attempts = test_n * attempt_multiplier
        for attempts in range(1, train_attempts + 1):
            world, task = generate_task(rng, f"forced_train_{min_len}_{attempts}", family="transitivity", proof_depth=min_len, entity_prefix=f"fltr{min_len}_{attempts}_")
            proof = extract_proof(world, task)
            if int(proof["metrics"]["minimal_proof_length"]) >= min_len:
                train_pairs.append((world, task, proof))
                if len(train_pairs) >= train_n:
                    break
        for attempts in range(1, test_attempts + 1):
            family = OOD_FAMILIES[attempts % len(OOD_FAMILIES)]
            world, task = generate_task(rng, f"forced_test_{min_len}_{attempts}", family=family, proof_depth=max(4, min_len), entity_prefix=f"flte{min_len}_{attempts}_")
            proof = extract_proof(world, task)
            if int(proof["metrics"]["minimal_proof_length"]) >= min_len:
                test_pairs.append((world, task, proof))
                if len(test_pairs) >= test_n:
                    break
        train_tasks = [task for _, task, _ in train_pairs]
        test_tasks = [task for _, task, _ in test_pairs]
        if len(train_tasks) >= 5 and len(test_tasks) >= 5:
            model = fit_statistical_model(train_tasks, seed=seed + min_len, kind="forest")
            graph_pred = predict_statistical_model(model, test_tasks)
            majority_pred = majority_predictions(labels(train_tasks), len(test_tasks))
            solver_pred = [str(answer_query(world, task.query)[0]) for world, task, _ in test_pairs]
            y = labels(test_tasks)
            graph_acc = answer_accuracy(y, graph_pred)
            majority_acc = answer_accuracy(y, majority_pred)
            solver_acc = answer_accuracy(y, solver_pred)
        else:
            graph_acc = majority_acc = solver_acc = 0.0
        all_proofs = [proof for *_, proof in train_pairs + test_pairs]
        rows.append(
            {
                "minimum length": min_len,
                "actual average length": mean([float(proof["metrics"]["minimal_proof_length"]) for proof in all_proofs]),
                "proof diversity": len({proof["metrics"]["canonical_proof_hash"] for proof in all_proofs}) / len(all_proofs) if all_proofs else 0.0,
                "OOD accuracy": graph_acc,
                "graph classifier": graph_acc,
                "solver": solver_acc,
                "majority baseline": majority_acc,
                "accepted_train": len(train_tasks),
                "accepted_test": len(test_tasks),
                "train_candidates": train_attempts,
                "test_candidates": test_attempts,
            }
        )
    return rows


def decision_gate(
    world_novelty: float,
    task_novelty: float,
    proof_novelty: float,
    forced_rows: list[dict[str, object]],
    capacity_world_novelty: float | None = None,
) -> dict[str, object]:
    forced_high = [row for row in forced_rows if row["minimum length"] >= 4]
    forced_diversity = mean([float(row["proof diversity"]) for row in forced_high])
    raw_world_novelty = capacity_world_novelty if capacity_world_novelty is not None else world_novelty
    accepted_long = sum(int(row.get("accepted_train", 0)) + int(row.get("accepted_test", 0)) for row in forced_high)
    if raw_world_novelty < 0.5 and proof_novelty < 0.5:
        outcome = "World poor"
        recommendation = "expand ontology"
    elif raw_world_novelty >= 0.5 and proof_novelty < 0.5 and task_novelty < 0.7:
        outcome = "Task extractor poor"
        recommendation = "rewrite task extraction"
    elif proof_novelty < 0.5 and accepted_long > 0 and forced_diversity < 0.5:
        outcome = "Proof algebra poor"
        recommendation = "consider proof-first architecture"
    else:
        outcome = "Current evidence insufficient"
        recommendation = "collect more diagnostics"
    return {
        "outcome": outcome,
        "recommendation": recommendation,
        "evidence": {
            "capacity_world_novelty": raw_world_novelty,
            "extracted_world_novelty": world_novelty,
            "task_novelty": task_novelty,
            "proof_novelty": proof_novelty,
            "forced_long_proof_diversity": forced_diversity,
            "accepted_long_forced_proofs": accepted_long,
        },
    }


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (den_x * den_y) if den_x and den_y else 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-worlds", type=int, default=5_000)
    parser.add_argument("--train-sizes", nargs="+", type=int, default=[100, 300, 1000])
    parser.add_argument("--depth-train-max", type=int, default=2)
    parser.add_argument("--depth-test", nargs="+", type=int, default=[4, 5])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-proof-files", type=int, default=2_000)
    parser.add_argument("--forced-train", type=int, default=40)
    parser.add_argument("--forced-test", type=int, default=40)
    parser.add_argument("--forced-attempt-multiplier", type=int, default=8)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--capacity-summary", type=Path, default=Path("outputs/capacity_summary.json"))
    args = parser.parse_args()

    out = ensure_output_dir(args.outputs)
    proofs_dir = out / "proofs"
    max_train = max(args.train_sizes)
    train_pairs, ood_pairs, adversarial_pairs = build_pairs(args.seed, args.num_worlds, max_train, args.depth_train_max, [max(4, d) for d in args.depth_test])
    analysis_pairs = train_pairs[:max_train] + ood_pairs + adversarial_pairs
    proofs = materialize_proofs(analysis_pairs, proofs_dir, args.max_proof_files)

    train_tasks = [task for _, task in train_pairs[:max_train]]
    ood_tasks = [task for _, task in ood_pairs]
    world_rows = novelty_curve(train_tasks, "canonical_world_hash", "generated")
    task_rows = novelty_curve(train_tasks, "canonical_task_hash", "generated")
    proof_rows = proof_novelty_curve(proofs)
    shape_rows, shape_summary = shape_counts(proofs)
    metric_rows = metrics_rows(proofs)
    diff_rows = difficulty_rows(proofs)
    corr_rows = correlations(proofs, ood_pairs, train_tasks, args.seed)
    forced_rows = forced_length_audit(args.seed, [2, 4, 6, 8], train_n=args.forced_train, test_n=args.forced_test, attempt_multiplier=args.forced_attempt_multiplier)

    write_csv(out / "proof_metrics.csv", metric_rows)
    write_csv(out / "proof_shape_counts.csv", shape_rows)
    write_csv(out / "proof_novelty_curve.csv", proof_rows)
    write_csv(out / "difficulty_distribution.csv", diff_rows)
    write_csv(out / "correlations.csv", corr_rows)
    write_csv(out / "forced_length_summary.csv", forced_rows)
    save_proof_space(out / "proof_space.png", proofs)
    save_proof_saturation(out / "proof_saturation.png", proof_rows)
    save_novelty_comparison(out / "novelty_comparison.png", world_rows, task_rows, proof_rows)

    capacity_world_novelty = None
    if args.capacity_summary.exists():
        try:
            capacity_world_novelty = float(json.loads(args.capacity_summary.read_text()).get("uniqueness_ratio"))
        except Exception:
            capacity_world_novelty = None
    gate = decision_gate(
        world_novelty=float(world_rows[-1]["novelty_rate"]),
        task_novelty=float(task_rows[-1]["novelty_rate"]),
        proof_novelty=float(proof_rows[-1]["proof_novelty"]),
        forced_rows=forced_rows,
        capacity_world_novelty=capacity_world_novelty,
    )
    gate["proof_shape_summary"] = shape_summary
    gate["generated_proofs"] = len(proofs)
    gate["unique_proof_graphs"] = len({proof["metrics"]["canonical_proof_hash"] for proof in proofs})
    gate["proof_files_written"] = min(len(proofs), args.max_proof_files)
    write_json(out / "decision_gate.json", gate)
    print(json.dumps(gate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
