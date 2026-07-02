from __future__ import annotations

import math
from collections import Counter

from worldcore.types import Task, WorldState


def novelty_rate(hashes: list[str]) -> float:
    return uniqueness_ratio(hashes)


def uniqueness_ratio(hashes: list[str]) -> float:
    if not hashes:
        return 0.0
    return len(set(hashes)) / len(hashes)


def collision_fraction(hashes: list[str]) -> float:
    return 1.0 - uniqueness_ratio(hashes) if hashes else 0.0


def collision_rate(hashes: list[str]) -> float:
    # Backward-compatible alias for old callers. Prefer uniqueness_ratio and collision_fraction.
    return collision_fraction(hashes)


def saturation_curve(hashes: list[str], checkpoints: list[int]) -> list[dict[str, float]]:
    rows = []
    for n in checkpoints:
        prefix = hashes[:n]
        rows.append(
            {
                "samples": n,
                "unique": len(set(prefix)),
                "uniqueness_ratio": uniqueness_ratio(prefix),
                "collision_fraction": collision_fraction(prefix),
                "novelty_rate": novelty_rate(prefix),
            }
        )
    return rows


def novelty_curve(tasks: list[Task], hash_attr: str, x_name: str = "generated") -> list[dict[str, float]]:
    seen: set[str] = set()
    rows = []
    for idx, task in enumerate(tasks, start=1):
        value = str(getattr(task, hash_attr))
        before = len(seen)
        seen.add(value)
        rows.append(
            {
                x_name: idx,
                "new": int(len(seen) > before),
                "unique": len(seen),
                "novelty_rate": len(seen) / idx,
            }
        )
    return rows


def answer_accuracy(y_true: list[object], y_pred: list[object]) -> float:
    if not y_true:
        return 0.0
    return sum(left == right for left, right in zip(y_true, y_pred)) / len(y_true)


def label_distribution(tasks: list[Task]) -> dict[str, float]:
    counts = Counter(str(task.answer) for task in tasks)
    total = sum(counts.values())
    entropy = 0.0
    for count in counts.values():
        probability = count / total if total else 0.0
        if probability:
            entropy -= probability * math.log2(probability)
    payload: dict[str, float] = {"true": float(counts.get("True", 0)), "false": float(counts.get("False", 0)), "unknown": float(counts.get("unknown", 0))}
    payload["total"] = float(total)
    payload["entropy"] = entropy
    payload["max_entropy"] = math.log2(3)
    payload["normalized_entropy"] = entropy / math.log2(3) if total else 0.0
    return payload


def complexity_row(task: Task) -> dict[str, object]:
    return {
        "task_id": task.task_id,
        "canonical_task_hash": task.canonical_task_hash,
        "reasoning_pattern": task.reasoning_pattern,
        "answer": str(task.answer),
        "reasoning_depth": task.proof_depth,
        "number_of_distractors": task.num_distractors,
        "number_of_supporting_facts": task.num_supporting_facts,
        "number_of_irrelevant_facts": task.num_irrelevant_facts,
        "number_of_predicates": task.num_predicates,
        "number_of_entities": task.num_entities,
        "number_of_inference_rules_used": task.num_inference_rules_used,
    }


def split_validation(train_tasks: list[Task], test_tasks: list[Task], train_worlds: list[WorldState], test_worlds: list[WorldState]) -> dict[str, object]:
    train_world_hashes = {task.canonical_world_hash for task in train_tasks}
    test_world_hashes = {task.canonical_world_hash for task in test_tasks}
    train_task_hashes = {task.canonical_task_hash for task in train_tasks}
    test_task_hashes = {task.canonical_task_hash for task in test_tasks}
    train_names = {entity.id for world in train_worlds for entity in world.entities}
    test_names = {entity.id for world in test_worlds for entity in world.entities}
    train_templates = {task.reasoning_pattern for task in train_tasks}
    test_templates = {task.reasoning_pattern for task in test_tasks}
    return {
        "shared_world_hashes": len(train_world_hashes & test_world_hashes),
        "shared_task_hashes": len(train_task_hashes & test_task_hashes),
        "shared_entity_names": len(train_names & test_names),
        "shared_templates": len(train_templates & test_templates),
        "train_templates": sorted(train_templates),
        "test_templates": sorted(test_templates),
        "train_max_depth": max((task.proof_depth for task in train_tasks), default=0),
        "test_min_depth": min((task.proof_depth for task in test_tasks), default=0),
    }


def world_feature_counts(world: WorldState) -> dict[str, float]:
    counts = Counter(fact.predicate for fact in world.facts)
    counts["num_entities"] = len(world.entities)
    counts["num_facts"] = len(world.facts)
    for entity in world.entities:
        counts[f"type:{entity.type}"] += 1
    return dict(counts)


def task_feature_counts(task: Task) -> dict[str, float]:
    counts = Counter(f"fact:{fact.predicate}" for fact in task.facts)
    counts[f"query:{task.query.predicate}"] += 1
    counts[f"pattern:{task.reasoning_pattern}"] += 1
    counts["num_facts"] = len(task.facts)
    counts["query_arity"] = len(task.query.args)
    counts["proof_depth"] = task.proof_depth
    counts["num_predicates"] = task.num_predicates
    counts["num_entities"] = task.num_entities
    counts["num_rules"] = task.num_inference_rules_used
    counts["num_distractors"] = task.num_distractors
    return dict(counts)
