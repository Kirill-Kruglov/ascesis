#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    def tqdm(iterable, **_: object):
        return iterable

from worldcore.baselines import (
    fit_statistical_model,
    labels,
    majority_predictions,
    memorization_analysis,
    memorization_predictions,
    predict_statistical_model,
    random_predictions,
)
from worldcore.experiments import ensure_output_dir, save_line_plot, write_csv, write_json
from worldcore.generator import generate_adversarial_pair, generate_task, make_rng
from worldcore.metrics import (
    answer_accuracy,
    complexity_row,
    label_distribution,
    novelty_curve,
    split_validation,
)
from worldcore.solver import answer_query


TRAIN_FAMILIES = ["entailment", "negation", "unknown", "transitivity", "contradiction"]
OOD_FAMILIES = ["implication+transitivity", "transitivity+negation", "causal+temporal", "belief+fact", "part-of+location"]


def solver_predictions(pairs: list[tuple[object, object]]) -> list[str]:
    predictions = []
    for world, task in pairs:
        answer, _ = answer_query(world, task.query)
        predictions.append(str(answer))
    return predictions


def _build_train_pool(rng, size: int, depth_train_max: int) -> list[tuple[object, object]]:
    pairs = []
    for idx in tqdm(range(size), desc="train canonical pool"):
        family = TRAIN_FAMILIES[idx % len(TRAIN_FAMILIES)]
        depth = 1 + (idx % depth_train_max)
        pairs.append(generate_task(rng, f"train_{idx}", family=family, proof_depth=depth, entity_prefix=f"tr{idx}_"))
    return pairs


def _build_ood_pool(rng, train_tasks, train_worlds, depths: list[int], per_depth: int) -> list[tuple[object, object]]:
    train_task_hashes = {task.canonical_task_hash for task in train_tasks}
    train_world_hashes = {task.canonical_world_hash for task in train_tasks}
    pairs = []
    idx = 0
    attempts = 0
    target = per_depth * len(depths)
    while len(pairs) < target and attempts < target * 80:
        depth = depths[len(pairs) % len(depths)]
        family = OOD_FAMILIES[idx % len(OOD_FAMILIES)]
        world, task = generate_task(rng, f"ood_{idx}", family=family, proof_depth=max(4, depth), entity_prefix=f"ood{idx}_")
        attempts += 1
        idx += 1
        if task.canonical_task_hash in train_task_hashes or task.canonical_world_hash in train_world_hashes:
            continue
        pairs.append((world, task))
    return pairs


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _failure_mode(split_report: dict[str, object], entropy: float, novelty: float, final_row: dict[str, float]) -> tuple[str, list[str]]:
    reasons = []
    if split_report["shared_world_hashes"] or split_report["shared_task_hashes"] or split_report["shared_entity_names"]:
        reasons.append("OOD leakage")
    if entropy < 0.5:
        reasons.append("label imbalance")
    if novelty < 0.5:
        reasons.append("finite generator")
    if final_row.get("memorization", 0.0) >= final_row.get("graph_classifier", 0.0) and final_row.get("memorization", 0.0) > 0.8:
        reasons.append("template memorization")
    if final_row.get("avg depth", 0.0) < 3.0 or final_row.get("avg rules", 0.0) < 1.0:
        reasons.append("too-simple reasoning")
    if final_row.get("solver", 0.0) < 0.95:
        reasons.append("solver mismatch")
    return (reasons[0] if reasons else "healthy", reasons)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-worlds", type=int, default=5_000)
    parser.add_argument("--train-sizes", nargs="+", type=int, default=[100, 300, 1000])
    parser.add_argument("--depth-train-max", type=int, default=2)
    parser.add_argument("--depth-test", nargs="+", type=int, default=[4, 5])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rng = make_rng(args.seed)
    out = ensure_output_dir(args.outputs)
    max_train = max(args.train_sizes)
    train_pool_size = max(args.num_worlds, max_train)
    depth_test = [max(4, depth) for depth in args.depth_test]

    train_pairs = _build_train_pool(rng, train_pool_size, args.depth_train_max)
    train_worlds = [world for world, _ in train_pairs]
    train_tasks = [task for _, task in train_pairs]
    ood_pairs = _build_ood_pool(rng, train_tasks, train_worlds, depth_test, max(150, max_train // 10))
    adversarial_pairs = []
    for adv_idx in range(max(20, max_train // 40)):
        left, right = generate_adversarial_pair(rng, f"{adv_idx}", entity_prefix="adv_")
        adversarial_pairs.extend([left, right])
    ood_worlds = [world for world, _ in ood_pairs]
    ood_tasks = [task for _, task in ood_pairs]
    adversarial_tasks = [task for _, task in adversarial_pairs]

    split_report = split_validation(train_tasks[:max_train], ood_tasks, train_worlds[:max_train], ood_worlds)
    all_tasks = train_tasks[:max_train] + ood_tasks + adversarial_tasks
    label_report = label_distribution(all_tasks)
    complexity_rows = [complexity_row(task) for task in all_tasks]

    world_novelty_rows = novelty_curve(train_tasks[:max_train], "canonical_world_hash", "generated")
    task_novelty_rows = novelty_curve(train_tasks[:max_train], "canonical_task_hash", "generated")

    learn_rows = []
    summary_rows = []
    memorization_curve = []
    solver_curve = []
    ood_curve = []
    previous_accuracy: float | None = None
    y_ood = labels(ood_tasks)

    for n in args.train_sizes:
        subset = train_tasks[:n]
        train_y = labels(subset)
        model = fit_statistical_model(subset, seed=args.seed, kind="forest")
        graph_pred = predict_statistical_model(model, ood_tasks)
        memo_pred = memorization_predictions(subset, ood_tasks)
        majority_pred = majority_predictions(train_y, len(ood_tasks))
        random_pred = random_predictions(train_y, len(ood_tasks), args.seed + n)
        solver_pred = solver_predictions(ood_pairs)

        graph_acc = answer_accuracy(y_ood, graph_pred)
        row = {
            "train_size": n,
            "world_novelty": len({task.canonical_world_hash for task in subset}) / n,
            "task_novelty": len({task.canonical_task_hash for task in subset}) / n,
            "solver": answer_accuracy(y_ood, solver_pred),
            "memorization": answer_accuracy(y_ood, memo_pred),
            "majority": answer_accuracy(y_ood, majority_pred),
            "random": answer_accuracy(y_ood, random_pred),
            "graph_classifier": graph_acc,
            "OOD": graph_acc,
            "entropy": label_report["normalized_entropy"],
            "avg depth": _mean([float(task.proof_depth) for task in ood_tasks]),
            "avg distractors": _mean([float(task.num_distractors) for task in ood_tasks]),
            "avg rules": _mean([float(task.num_inference_rules_used) for task in ood_tasks]),
        }
        delta = 0.0 if previous_accuracy is None else graph_acc - previous_accuracy
        previous_accuracy = graph_acc
        learn_rows.append({"train_size": n, "ood_unseen_accuracy": graph_acc, "delta_accuracy": delta})
        summary_rows.append(row)
        memorization_curve.append({"train_size": n, "accuracy": row["memorization"]})
        solver_curve.append({"train_size": n, "accuracy": row["solver"]})
        ood_curve.append({"train_size": n, "accuracy": graph_acc})

    final_memo = memorization_analysis(train_tasks[:max_train], ood_tasks)
    adversarial_accuracy = answer_accuracy(labels(adversarial_tasks), solver_predictions(adversarial_pairs))

    failure_mode, reasons = _failure_mode(split_report, float(label_report["normalized_entropy"]), task_novelty_rows[-1]["novelty_rate"], summary_rows[-1])
    kolmogorov = {
        "world_novelty_curve": world_novelty_rows,
        "task_novelty_curve": task_novelty_rows,
        "ood_curve": ood_curve,
        "memorization_curve": memorization_curve,
        "solver_curve": solver_curve,
        "suspected_failure_mode": failure_mode,
        "warnings": reasons,
    }
    summary = {
        "seed": args.seed,
        "num_worlds_requested": args.num_worlds,
        "num_train_generated": len(train_tasks),
        "max_train_size_used": max_train,
        "num_ood": len(ood_tasks),
        "adversarial_accuracy": adversarial_accuracy,
        "suspected_failure_mode": failure_mode,
        "warnings": reasons,
        "final": summary_rows[-1],
    }

    write_json(out / "openendedness_summary.json", summary)
    write_json(out / "ood_split_validation.json", split_report)
    write_json(out / "memorization_analysis.json", final_memo)
    write_json(out / "label_distribution.json", label_report)
    write_json(out / "kolmogorov_report.json", kolmogorov)
    write_csv(out / "world_novelty_curve.csv", world_novelty_rows)
    write_csv(out / "task_novelty_curve.csv", task_novelty_rows)
    write_csv(out / "novelty_curve.csv", [{"generated": row["generated"], "world_novelty": world_novelty_rows[idx]["novelty_rate"], "task_novelty": row["novelty_rate"]} for idx, row in enumerate(task_novelty_rows)])
    write_csv(out / "learnability_curve.csv", learn_rows)
    write_csv(out / "complexity_distribution.csv", complexity_rows)
    write_csv(out / "experiment_summary.csv", summary_rows)
    save_line_plot(out / "novelty_vs_learnability.png", [{"train_size": row["train_size"], "task_novelty": row["task_novelty"], "OOD": row["OOD"]} for row in summary_rows], "train_size", ["task_novelty", "OOD"], "Novelty vs OOD transfer")
    save_line_plot(out / "ood_depth_accuracy.png", summary_rows, "train_size", ["OOD", "memorization", "majority", "random", "solver"], "OOD baselines")

    if reasons:
        print("WARNING")
        print("Current experiment cannot falsify hypothesis.")
        print("Reason:")
        for reason in reasons:
            print(f"- {reason}")


if __name__ == "__main__":
    main()
