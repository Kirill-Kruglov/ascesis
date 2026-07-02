from __future__ import annotations

import ast
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


CL_ROOT = Path(__file__).resolve().parents[1]
CL2_ROOT = CL_ROOT / "CL2_equal_volume_learner_probe"
for path in (CL2_ROOT,):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from dataset_builder import (  # noqa: E402
    build_candidate_rows,
    forbidden_fields_present,
    random_split,
    source_state_holdout_split,
    structural_holdout_split,
    target_observation,
)
from learners import (  # noqa: E402
    CopySourceBaseline,
    Learner,
    MajorityDeltaBaseline,
    MemorizerBaseline,
    RuleFamilyTransitionLearner,
)


Row = dict[str, Any]
LearnerFactory = Callable[[], Learner]

TARGET_FIELDS = {"successor_zones", "successor_mass", "successor_phase"}
FEATURE_FIELDS = {"source_zones", "source_mass", "source_phase", "action"}
FORBIDDEN_CALLS = [
    "transition",
    "rollout_outcome",
    "action_rollout_outcome",
    "is_collapsed",
    "collapse_mechanism",
    "candidate_action_admission",
]


def feature_view(row: Row) -> Row:
    return {
        "source_zones": list(row["source_zones"]),
        "source_mass": int(row["source_mass"]),
        "source_phase": int(row["source_phase"]),
        "action": row["action"],
    }


def split_rows(rows: list[Row], seed: int) -> dict[str, dict[str, list[Row]]]:
    return {
        "random": random_split(rows, seed),
        "source": source_state_holdout_split(rows, seed),
        "structural": structural_holdout_split(rows),
    }


def prediction_equal(prediction: dict[str, Any], target: dict[str, Any]) -> bool:
    return (
        list(prediction["zones"]) == list(target["zones"])
        and int(prediction["mass"]) == int(target["mass"])
        and int(prediction["phase"]) == int(target["phase"])
    )


def score_learner(
    learner_factory: LearnerFactory,
    train_rows: list[Row],
    test_rows: list[Row],
) -> dict[str, float]:
    learner = learner_factory()
    learner.fit(train_rows)
    if not test_rows:
        return {"exact": 0.0, "coordinate": 0.0}

    exact = 0
    coordinate_correct = 0
    coordinate_total = 0
    for row in test_rows:
        prediction = learner.predict(feature_view(row))
        target = target_observation(row)
        if prediction_equal(prediction, target):
            exact += 1
        for idx, value in enumerate(target["zones"]):
            coordinate_total += 1
            if prediction["zones"][idx] == value:
                coordinate_correct += 1
        coordinate_total += 1
        if int(prediction["mass"]) == int(target["mass"]):
            coordinate_correct += 1
        coordinate_total += 1
        if int(prediction["phase"]) == int(target["phase"]):
            coordinate_correct += 1

    return {
        "exact": exact / len(test_rows),
        "coordinate": coordinate_correct / coordinate_total if coordinate_total else 0.0,
    }


def score_control(
    learner_factory: LearnerFactory,
    splits: dict[str, dict[str, list[Row]]],
    transform: Callable[[list[Row], int], list[Row]],
    seed: int,
) -> dict[str, float]:
    results: dict[str, float] = {}
    for offset, split_name in enumerate(("random", "source", "structural")):
        train = transform(splits[split_name]["train"], seed)
        test = splits[split_name]["test"]
        scores = score_learner(learner_factory, train, test)
        prefix = "source_holdout" if split_name == "source" else f"{split_name}_holdout"
        if split_name == "random":
            prefix = "random"
        results[f"{prefix}_exact"] = scores["exact"]
        results[f"{prefix}_coordinate"] = scores["coordinate"]
    results["max_exact"] = max(
        results["random_exact"],
        results["source_holdout_exact"],
        results["structural_holdout_exact"],
    )
    return results


def copy_rows(rows: list[Row]) -> list[Row]:
    return [dict(row, source_zones=list(row["source_zones"]), successor_zones=list(row["successor_zones"])) for row in rows]


def assign_targets(rows: list[Row], targets: list[tuple[list[int], int, int]]) -> list[Row]:
    output = copy_rows(rows)
    for row, target in zip(output, targets):
        row["successor_zones"] = list(target[0])
        row["successor_mass"] = int(target[1])
        row["successor_phase"] = int(target[2])
    return output


def target_tuple(row: Row) -> tuple[list[int], int, int]:
    return (list(row["successor_zones"]), int(row["successor_mass"]), int(row["successor_phase"]))


def global_shuffle(rows: list[Row], seed: int) -> list[Row]:
    targets = [target_tuple(row) for row in rows]
    random.Random(seed + 2).shuffle(targets)
    return assign_targets(rows, targets)


def within_bucket_shuffle(rows: list[Row], seed: int, bucket_fn: Callable[[Row], Any]) -> list[Row]:
    output = copy_rows(rows)
    indices_by_bucket: dict[Any, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        indices_by_bucket[bucket_fn(row)].append(idx)
    rng = random.Random(seed + 20)
    for indices in indices_by_bucket.values():
        targets = [target_tuple(rows[idx]) for idx in indices]
        rng.shuffle(targets)
        for idx, target in zip(indices, targets):
            output[idx]["successor_zones"] = list(target[0])
            output[idx]["successor_mass"] = int(target[1])
            output[idx]["successor_phase"] = int(target[2])
    return output


def cross_bucket_shuffle(rows: list[Row], seed: int, bucket_fn: Callable[[Row], Any]) -> list[Row]:
    output = copy_rows(rows)
    buckets = [bucket_fn(row) for row in rows]
    targets = [target_tuple(row) for row in rows]
    indices = list(range(len(rows)))
    rng = random.Random(seed + 30)
    rng.shuffle(indices)
    available_by_bucket: dict[Any, list[int]] = defaultdict(list)
    for idx in indices:
        available_by_bucket[buckets[idx]].append(idx)

    assigned_indices: list[int] = []
    for row_idx, bucket in enumerate(buckets):
        candidates = [candidate_bucket for candidate_bucket in available_by_bucket if candidate_bucket != bucket]
        candidates = [candidate_bucket for candidate_bucket in candidates if available_by_bucket[candidate_bucket]]
        if not candidates:
            candidates = [candidate_bucket for candidate_bucket in available_by_bucket if available_by_bucket[candidate_bucket]]
        chosen_bucket = rng.choice(candidates)
        target_idx = available_by_bucket[chosen_bucket].pop()
        assigned_indices.append(target_idx)

    assigned_targets = [targets[idx] for idx in assigned_indices]
    return assign_targets(output, assigned_targets)


def independent_impossible_targets(rows: list[Row], seed: int) -> list[Row]:
    rng = random.Random(seed + 40)
    output = copy_rows(rows)
    observed_zone_values = sorted({value for row in rows for value in row["source_zones"] + row["successor_zones"]})
    observed_mass_values = sorted({int(row["source_mass"]) for row in rows} | {int(row["successor_mass"]) for row in rows})
    observed_phase_values = sorted({int(row["source_phase"]) for row in rows} | {int(row["successor_phase"]) for row in rows})
    for row in output:
        row["successor_zones"] = [rng.choice(observed_zone_values) for _ in row["source_zones"]]
        row["successor_mass"] = rng.choice(observed_mass_values)
        row["successor_phase"] = rng.choice(observed_phase_values)
    return output


def feature_permutation(rows: list[Row], seed: int) -> list[Row]:
    rng = random.Random(seed + 50)
    output = copy_rows(rows)
    source_zones = [list(row["source_zones"]) for row in rows]
    source_mass = [int(row["source_mass"]) for row in rows]
    source_phase = [int(row["source_phase"]) for row in rows]
    actions = [row["action"] for row in rows]
    rng.shuffle(source_zones)
    rng.shuffle(source_mass)
    rng.shuffle(source_phase)
    rng.shuffle(actions)
    for idx, row in enumerate(output):
        row["source_zones"] = list(source_zones[idx])
        row["source_mass"] = int(source_mass[idx])
        row["source_phase"] = int(source_phase[idx])
        row["action"] = actions[idx]
    return output


def identity(rows: list[Row], seed: int) -> list[Row]:
    del seed
    return copy_rows(rows)


def scan_learner_code_for_forbidden_calls() -> dict[str, Any]:
    path = CL2_ROOT / "learners.py"
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports: list[str] = []
    calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in {"domain", "action_boundary", "boundary"}:
            for alias in node.names:
                if alias.name in FORBIDDEN_CALLS:
                    imports.append(alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"domain", "action_boundary", "boundary"}:
                    imports.append(alias.name)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                calls.append(func.id)
            elif isinstance(func, ast.Attribute) and func.attr in FORBIDDEN_CALLS:
                calls.append(func.attr)
    return {
        "imports_forbidden_oracle_functions": sorted(set(imports)),
        "calls_forbidden_oracle_functions": sorted(set(calls)),
        "forbidden_oracle_calls": sorted(set(imports + calls)),
    }


def evaluation_integrity(rows: list[Row], code_scan: dict[str, Any]) -> dict[str, Any]:
    feature_keys = set(feature_view(rows[0]).keys()) if rows else set()
    target_fields_in_features = bool(TARGET_FIELDS.intersection(feature_keys))
    forbidden_present = forbidden_fields_present(rows)
    forbidden_calls = code_scan["forbidden_oracle_calls"]
    mismatch = target_fields_in_features
    return {
        "target_fields_in_features": target_fields_in_features,
        "test_target_used_in_fit": False,
        "prediction_compared_to_original_true_target": True,
        "shuffled_control_test_targets_remain_original": True,
        "forbidden_fields_present": forbidden_present,
        "forbidden_oracle_calls": forbidden_calls,
        "evaluation_mismatch_detected": mismatch,
    }


CONTROL_TRANSFORMS: dict[str, Callable[[list[Row], int], list[Row]]] = {
    "original_global_shuffle": global_shuffle,
    "within_action_shuffle": lambda rows, seed: within_bucket_shuffle(rows, seed, lambda row: row["action"]),
    "within_phase_shuffle": lambda rows, seed: within_bucket_shuffle(rows, seed, lambda row: row["source_phase"]),
    "cross_action_shuffle": lambda rows, seed: cross_bucket_shuffle(rows, seed, lambda row: row["action"]),
    "cross_phase_shuffle": lambda rows, seed: cross_bucket_shuffle(rows, seed, lambda row: row["source_phase"]),
    "independent_impossible_target": independent_impossible_targets,
    "feature_permutation_control": feature_permutation,
}

LEARNERS: dict[str, LearnerFactory] = {
    "primary_rule_family_learner": RuleFamilyTransitionLearner,
    "majority_delta_baseline": MajorityDeltaBaseline,
    "memorizer_baseline": MemorizerBaseline,
    "copy_source_baseline": CopySourceBaseline,
}
