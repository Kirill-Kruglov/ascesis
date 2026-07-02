#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict, deque
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, r2_score

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    def tqdm(iterable, **_: object):
        return iterable

from worldcore.experiments import ensure_output_dir, write_csv, write_json
from worldcore.generator import generate_task, make_rng
from worldcore.proof import closure_audit, extract_proof, proof_opportunities_for_world


FAMILIES = [
    "entailment",
    "negation",
    "unknown",
    "transitivity",
    "contradiction",
    "implication+transitivity",
    "transitivity+negation",
    "causal+temporal",
    "belief+fact",
    "part-of+location",
]
OOD_FAMILIES = ["implication+transitivity", "transitivity+negation", "causal+temporal", "belief+fact", "part-of+location"]
FEATURES = ["difficulty", "minimal_proof_length", "width", "branching_factor", "alternative_proofs", "proof_entropy", "reuse", "fan_in"]


def build_selected_pairs(seed: int, num_worlds: int) -> list[tuple[object, object]]:
    rng = make_rng(seed)
    pairs = []
    for idx in tqdm(range(num_worlds), desc="sample worlds"):
        family = FAMILIES[idx % len(FAMILIES)]
        depth = 1 + (idx % 5)
        if family in OOD_FAMILIES:
            depth = max(4, depth)
        pairs.append(generate_task(rng, f"audit_{idx}", family=family, proof_depth=depth, entity_prefix=f"aud{idx}_"))
    return pairs


def write_closure_files(closures: list[dict[str, object]], closure_dir: Path, max_files: int) -> None:
    closure_dir.mkdir(parents=True, exist_ok=True)
    limit = len(closures) if max_files < 0 else min(max_files, len(closures))
    for idx, closure in enumerate(closures[:limit]):
        (closure_dir / f"world_{idx:05d}.json").write_text(json.dumps(closure, indent=2, sort_keys=True), encoding="utf-8")


def closure_statistics(closures: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "world_id": c["world_id"],
            "initial_fact_count": c["initial_fact_count"],
            "derived_fact_count": c["derived_fact_count"],
            "closure_size": c["closure_size"],
            "closure_expansion_ratio": c["closure_expansion_ratio"],
            "rule_application_count": len(c["rule_applications"]),
        }
        for c in closures
    ]


def opportunity_summary(world_ids: list[str], opportunities_by_world: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows = []
    for world_id in world_ids:
        ops = opportunities_by_world.get(world_id, [])
        shapes = Counter(str(op["proof_shape"]) for op in ops)
        goals = defaultdict(int)
        for op in ops:
            goals[str(op["goal_fact"])] += 1
        rows.append(
            {
                "world_id": world_id,
                "proof_opportunities": len(ops),
                "distinct_proof_DAGs": len({op["canonical_proof_hash"] for op in ops}),
                "distinct_proof_shapes": len(shapes),
                "average_alternatives_per_goal": mean(list(goals.values())),
                "proof_entropy": entropy(shapes),
                "largest_shape_fraction": max((v / len(ops) for v in shapes.values()), default=0.0),
            }
        )
    return rows


def selected_proof_rows(pairs: list[tuple[object, object]]) -> list[dict[str, object]]:
    rows = []
    for world, task in pairs:
        proof = extract_proof(world, task)
        metrics = proof["metrics"]
        rows.append(
            {
                "world_id": world.world_id,
                "task_id": task.task_id,
                "reasoning_pattern": task.reasoning_pattern,
                "answer": str(task.answer),
                "selected_proof_hash": metrics["canonical_proof_hash"],
                "selected_shape": metrics["shape"],
                "selected_length": metrics["minimal_proof_length"],
                "selected_family": family_from_pattern(task.reasoning_pattern),
                "proof_exists": int(int(metrics["minimal_proof_length"]) > 0),
                "difficulty": metrics["difficulty"],
                "minimal_proof_length": metrics["minimal_proof_length"],
                "width": metrics["width"],
                "branching_factor": metrics["branching_factor"],
                "alternative_proofs": metrics["alternative_proofs"],
                "proof_entropy": metrics["proof_entropy"],
                "reuse": metrics["reuse"],
                "fan_in": metrics["fan_in"],
                "shape": metrics["shape"],
            }
        )
    return rows


def extractor_coverage(selected_rows: list[dict[str, object]], opportunities_by_world: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows = []
    for selected in selected_rows:
        world_id = str(selected["world_id"])
        ops = opportunities_by_world.get(world_id, [])
        selected_hash = str(selected["selected_proof_hash"])
        selected_shape = str(selected["selected_shape"])
        selected_length = str(selected["selected_length"])
        selected_family = str(selected["selected_family"])
        available_hashes = {str(op["canonical_proof_hash"]) for op in ops}
        selected_hits = int(selected_hash in available_hashes)
        rows.append(
            {
                "world_id": world_id,
                "task_id": selected["task_id"],
                "scope": "overall",
                "bucket": "all",
                "available_proofs": len(ops),
                "available_unique_proofs": len(available_hashes),
                "selected_proofs": selected_hits,
                "coverage": selected_hits / max(1, len(ops)),
            }
        )
        for scope, bucket_key, selected_bucket in [
            ("shape", "proof_shape", selected_shape),
            ("length", "proof_length", selected_length),
            ("reasoning_family", "reasoning_family", selected_family),
        ]:
            subset = [op for op in ops if str(op[bucket_key]) == selected_bucket]
            subset_hashes = {str(op["canonical_proof_hash"]) for op in subset}
            rows.append(
                {
                    "world_id": world_id,
                    "task_id": selected["task_id"],
                    "scope": scope,
                    "bucket": selected_bucket,
                    "available_proofs": len(subset),
                    "available_unique_proofs": len(subset_hashes),
                    "selected_proofs": int(selected_hash in subset_hashes),
                    "coverage": int(selected_hash in subset_hashes) / max(1, len(subset)),
                }
            )
    return rows


def closure_graph_metrics(closures: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for c in closures:
        facts = set(c["closure_facts"])
        adj: dict[str, set[str]] = defaultdict(set)
        alt_paths = Counter()
        for app in c["rule_applications"]:
            conclusion = str(app["conclusion"])
            alt_paths[conclusion] += 1
            for premise in app["premises"]:
                adj[str(premise)].add(conclusion)
        reachable_pairs, lengths = all_reachable_pairs(adj)
        components = connected_components(facts, adj)
        branch_vals = [len(v) for v in adj.values()]
        rows.append(
            {
                "world_id": c["world_id"],
                "fact_nodes": len(facts),
                "derivation_edges": sum(len(v) for v in adj.values()),
                "reachable_pairs": reachable_pairs,
                "connected_components": components,
                "min_path_length": min(lengths) if lengths else 0,
                "avg_path_length": mean(lengths),
                "max_path_length": max(lengths) if lengths else 0,
                "alternative_paths": sum(max(0, v - 1) for v in alt_paths.values()),
                "average_branching": mean(branch_vals),
            }
        )
    return rows


def closure_proof_novelty(opportunities: list[dict[str, object]]) -> list[dict[str, object]]:
    seen = set()
    rows = []
    for idx, op in enumerate(opportunities, start=1):
        h = str(op["canonical_proof_hash"])
        before = len(seen)
        seen.add(h)
        rows.append({"generated": idx, "new": int(len(seen) > before), "unique": len(seen), "closure_proof_novelty": len(seen) / idx})
    return rows


def difficulty_audit(opportunities: list[dict[str, object]], selected_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    # Audit the selected-task difficulty oracle, because this is where proof/no-proof collapse can occur.
    feature_rows = []
    for row in selected_rows:
        feature_rows.append(
            {
                "difficulty": float(row["difficulty"]),
                "minimal_proof_length": float(row["minimal_proof_length"]),
                "width": float(row["width"]),
                "branching_factor": float(row["branching_factor"]),
                "alternative_proofs": float(row["alternative_proofs"]),
                "proof_entropy": float(row["proof_entropy"]),
                "reuse": float(row["reuse"]),
                "fan_in": float(row["fan_in"]),
                "shape": str(row["shape"]),
                "proof_exists": int(row["proof_exists"]),
            }
        )
    if not feature_rows:
        return [], {"status": "Difficulty Oracle collapsed", "accuracy": 0.0, "r2": 0.0, "n": 0}
    shape_ids = {shape: idx for idx, shape in enumerate(sorted({row["shape"] for row in feature_rows}))}
    rows = []
    for feature in FEATURES:
        vals = [float(row[feature]) for row in feature_rows]
        rows.append(
            {
                "feature": feature,
                "kind": "distribution",
                "mean": mean(vals),
                "variance": variance(vals),
                "min": min(vals),
                "max": max(vals),
                "correlation_with_proof_exists": pearson(vals, [float(row["proof_exists"]) for row in feature_rows]),
                "correlation_with_shape": pearson(vals, [float(shape_ids[row["shape"]]) for row in feature_rows]),
            }
        )
    for i, left in enumerate(FEATURES):
        for right in FEATURES[i + 1 :]:
            rows.append(
                {
                    "feature": f"{left}__{right}",
                    "kind": "mutual_correlation",
                    "mean": "",
                    "variance": "",
                    "min": "",
                    "max": "",
                    "correlation_with_proof_exists": "",
                    "correlation_with_shape": pearson([float(row[left]) for row in feature_rows], [float(row[right]) for row in feature_rows]),
                }
            )
    X = [[float(row["difficulty"])] for row in feature_rows]
    y = [int(row["proof_exists"]) for row in feature_rows]
    if len(set(y)) < 2:
        accuracy = 1.0
        pseudo_r2 = 1.0
    else:
        model = LogisticRegression(random_state=0).fit(X, y)
        pred = model.predict(X)
        accuracy = float(accuracy_score(y, pred))
        pseudo_r2 = float(r2_score(y, pred))
    collapse = accuracy >= 0.95 or pseudo_r2 >= 0.9
    return rows, {
        "status": "Difficulty Oracle collapsed" if collapse else "Difficulty Oracle not collapsed",
        "accuracy": accuracy,
        "r2": pseudo_r2,
        "n": len(feature_rows),
        "proof_exists_rate": sum(y) / len(y),
    }

def forced_rejection_report(seed: int, mins: list[int], attempts_per_split: int) -> list[dict[str, object]]:
    rows = []
    for min_len in mins:
        rng = make_rng(seed + 1000 + min_len)
        for split in ["train", "test"]:
            for attempt in range(1, attempts_per_split + 1):
                if split == "train":
                    family = "transitivity"
                else:
                    family = OOD_FAMILIES[attempt % len(OOD_FAMILIES)]
                try:
                    world, task = generate_task(rng, f"forced_reject_{split}_{min_len}_{attempt}", family=family, proof_depth=max(min_len, 4 if split == "test" else 1), entity_prefix=f"fr{split}{min_len}_{attempt}_")
                    proof = extract_proof(world, task)
                    actual = int(proof["metrics"]["minimal_proof_length"])
                    if actual >= min_len:
                        reason = "accepted"
                    elif actual == 0:
                        reason = "proof absent"
                    else:
                        reason = "insufficient depth"
                except Exception as exc:  # pragma: no cover - diagnostic output
                    actual = -1
                    reason = f"proof extraction failed:{type(exc).__name__}"
                rows.append(
                    {
                        "minimum_length": min_len,
                        "split": split,
                        "candidate": attempt,
                        "family": family,
                        "actual_length": actual,
                        "rejection_reason": reason,
                    }
                )
    return rows


def diversity_explanation(selected_rows: list[dict[str, object]], opportunities: list[dict[str, object]], forced_rows: list[dict[str, object]], diff_status: dict[str, object]) -> dict[str, object]:
    selected_hashes = {str(row["selected_proof_hash"]) for row in selected_rows}
    opportunity_hashes = {str(op["canonical_proof_hash"]) for op in opportunities}
    selected_novelty = len(selected_hashes) / max(1, len(selected_rows))
    closure_novelty = len(opportunity_hashes) / max(1, len(opportunities))
    forced_accepted = [row for row in forced_rows if row["rejection_reason"] == "accepted"]
    reasons = []
    if closure_novelty > selected_novelty * 2:
        reasons.append("closure richer")
    if forced_accepted and len({row["actual_length"] for row in forced_accepted}) > 1:
        reasons.append("proof length")
    if diff_status["status"] == "Difficulty Oracle collapsed":
        reasons.append("measurement bug")
    if len(opportunity_hashes) <= 20:
        reasons.append("canonicalization artifact")
    if not reasons:
        reasons.append("unknown")
    return {
        "selected_proof_novelty": selected_novelty,
        "closure_proof_novelty": closure_novelty,
        "forced_accepted_count": len(forced_accepted),
        "explanations": reasons,
        "primary_explanation": reasons[0],
    }


def reasoning_family_audit(opportunities: list[dict[str, object]], coverage_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    coverage_by_family = defaultdict(list)
    for row in coverage_rows:
        if row["scope"] == "reasoning_family":
            coverage_by_family[str(row["bucket"])].append(float(row["coverage"]))
    by = defaultdict(list)
    for op in opportunities:
        by[str(op["reasoning_family"])].append(op)
    families = ["transitivity", "implication", "belief", "causal", "part-of", "negation", "mixed"]
    rows = []
    for family in families:
        ops = by.get(family, [])
        rows.append(
            {
                "reasoning_family": family,
                "closure_size": len({op["goal_fact"] for op in ops}),
                "proof_opportunities": len(ops),
                "proof_diversity": len({op["canonical_proof_hash"] for op in ops}) / max(1, len(ops)),
                "extractor_coverage": mean(coverage_by_family.get(family, [])),
            }
        )
    return rows


def sampling_simulation(opportunities: list[dict[str, object]], sample_size: int, seed: int, trials: int = 30) -> list[dict[str, object]]:
    if not opportunities:
        return []
    strategies = {
        "uniform": lambda op, counts: 1.0,
        "length weighted": lambda op, counts: 1.0 + float(op["proof_length"]),
        "entropy weighted": lambda op, counts: 1.0 + math.log2(1.0 + counts[str(op["proof_shape"])]),
        "shape weighted": lambda op, counts: 1.0 / counts[str(op["proof_shape"])],
        "rare proof weighted": lambda op, counts: 1.0 / counts[str(op["canonical_proof_hash"])],
        "random": lambda op, counts: 1.0,
    }
    rng = random.Random(seed)
    rows = []
    shape_counts = Counter(str(op["proof_shape"]) for op in opportunities)
    hash_counts = Counter(str(op["canonical_proof_hash"]) for op in opportunities)
    for name, weight_fn in strategies.items():
        counts = hash_counts if name == "rare proof weighted" else shape_counts
        weights = [max(1e-9, weight_fn(op, counts)) for op in opportunities]
        diversities = []
        shape_diversities = []
        for _ in range(trials):
            sample = rng.choices(opportunities, weights=weights, k=min(sample_size, len(opportunities)))
            diversities.append(len({op["canonical_proof_hash"] for op in sample}) / max(1, len(sample)))
            shape_diversities.append(len({op["proof_shape"] for op in sample}) / max(1, len(sample)))
        rows.append(
            {
                "strategy": name,
                "sample_size": min(sample_size, len(opportunities)),
                "expected_proof_diversity": mean(diversities),
                "expected_shape_diversity": mean(shape_diversities),
                "trials": trials,
            }
        )
    return rows


def decision_H2(closure_rows: list[dict[str, object]], summary_rows: list[dict[str, object]], coverage_rows: list[dict[str, object]]) -> dict[str, object]:
    avg_expansion = mean([float(row["closure_expansion_ratio"]) for row in closure_rows])
    avg_ops = mean([float(row["proof_opportunities"]) for row in summary_rows])
    avg_distinct = mean([float(row["distinct_proof_DAGs"]) for row in summary_rows])
    overall_coverage = mean([float(row["coverage"]) for row in coverage_rows if row["scope"] == "overall"])
    if avg_ops >= 3 and avg_distinct >= 2 and overall_coverage < 0.5:
        outcome = "Closure rich -> Extractor poor"
        diversity_loss = "Task extraction"
        recommendation = "rewrite extractor"
    elif avg_ops < 2 and overall_coverage >= 0.5:
        outcome = "Closure poor -> Extractor reasonable"
        diversity_loss = "Closure"
        recommendation = "rewrite generator"
    elif avg_ops >= 1 and overall_coverage < 0.8:
        outcome = "Mixed"
        diversity_loss = "Closure and task extraction"
        recommendation = "collect targeted diagnostics before architectural changes"
    else:
        outcome = "Unknown"
        diversity_loss = "Instrumentation"
        recommendation = "improve instrumentation"
    return {
        "outcome": outcome,
        "diversity_disappears_at": diversity_loss,
        "recommendation": recommendation,
        "evidence": {
            "avg_closure_expansion_ratio": avg_expansion,
            "avg_proof_opportunities_per_world": avg_ops,
            "avg_distinct_proof_DAGs_per_world": avg_distinct,
            "avg_extractor_coverage": overall_coverage,
        },
    }


def family_from_pattern(pattern: str) -> str:
    if "transitivity" in pattern:
        return "transitivity"
    if "belief" in pattern:
        return "belief"
    if "causal" in pattern:
        return "causal"
    if "part" in pattern:
        return "part-of"
    if "negation" in pattern or "contradiction" in pattern:
        return "negation"
    if "implication" in pattern or "entailment" in pattern:
        return "implication"
    if "mixed" in pattern:
        return "mixed"
    return "mixed"


def all_reachable_pairs(adj: dict[str, set[str]]) -> tuple[int, list[int]]:
    total = 0
    lengths = []
    for start in adj:
        queue = deque([(start, 0)])
        seen = {start}
        while queue:
            node, dist = queue.popleft()
            for nxt in adj.get(node, set()):
                if nxt not in seen:
                    seen.add(nxt)
                    total += 1
                    lengths.append(dist + 1)
                    queue.append((nxt, dist + 1))
    return total, lengths


def connected_components(nodes: set[str], adj: dict[str, set[str]]) -> int:
    undirected = defaultdict(set)
    for src, dsts in adj.items():
        for dst in dsts:
            undirected[src].add(dst)
            undirected[dst].add(src)
    seen = set()
    count = 0
    for node in nodes:
        if node in seen:
            continue
        count += 1
        stack = [node]
        seen.add(node)
        while stack:
            cur = stack.pop()
            for nxt in undirected.get(cur, set()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return count


def entropy(counter: Counter) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    value = 0.0
    for count in counter.values():
        p = count / total
        if p:
            value -= p * math.log2(p)
    return value


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def variance(values: list[float]) -> float:
    if not values:
        return 0.0
    m = mean(values)
    return sum((value - m) ** 2 for value in values) / len(values)


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    return numerator / (den_x * den_y) if den_x and den_y else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-worlds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-closure-files", type=int, default=-1)
    parser.add_argument("--forced-attempts", type=int, default=80)
    parser.add_argument("--sampling-trials", type=int, default=30)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    out = ensure_output_dir(args.outputs)
    pairs = build_selected_pairs(args.seed, args.num_worlds)
    closures = []
    all_ops = []
    opportunities_by_world: dict[str, list[dict[str, object]]] = {}
    for world, _task in tqdm(pairs, desc="closure/opportunity audit"):
        closure = closure_audit(world)
        closures.append(closure)
        ops = proof_opportunities_for_world(world)
        opportunities_by_world[world.world_id] = ops
        all_ops.extend(ops)

    write_closure_files(closures, out / "closure", args.max_closure_files)
    closure_rows = closure_statistics(closures)
    selected_rows = selected_proof_rows(pairs)
    summary_rows = opportunity_summary([world.world_id for world, _ in pairs], opportunities_by_world)
    coverage_rows = extractor_coverage(selected_rows, opportunities_by_world)
    graph_rows = closure_graph_metrics(closures)
    novelty_rows = closure_proof_novelty(all_ops)
    diff_rows, diff_status = difficulty_audit(all_ops, selected_rows)
    forced_rows = forced_rejection_report(args.seed, [2, 4, 6, 8], args.forced_attempts)
    explanation = diversity_explanation(selected_rows, all_ops, forced_rows, diff_status)
    family_rows = reasoning_family_audit(all_ops, coverage_rows)
    sampling_rows = sampling_simulation(all_ops, sample_size=len(selected_rows), seed=args.seed, trials=args.sampling_trials)
    decision = decision_H2(closure_rows, summary_rows, coverage_rows)
    decision["difficulty_oracle"] = diff_status
    decision["diversity_explanation"] = explanation

    write_csv(out / "closure_statistics.csv", closure_rows)
    write_csv(out / "proof_opportunities.csv", all_ops)
    write_csv(out / "proof_opportunity_summary.csv", summary_rows)
    write_csv(out / "extractor_coverage.csv", coverage_rows)
    write_csv(out / "closure_graph_metrics.csv", graph_rows)
    write_csv(out / "closure_proof_novelty.csv", novelty_rows)
    write_csv(out / "difficulty_audit.csv", diff_rows)
    write_csv(out / "forced_rejection_report.csv", forced_rows)
    write_json(out / "diversity_explanation.json", explanation)
    write_csv(out / "reasoning_family_audit.csv", family_rows)
    write_csv(out / "sampling_simulation.csv", sampling_rows)
    write_json(out / "decision_H2.json", decision)
    print(json.dumps(decision, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
