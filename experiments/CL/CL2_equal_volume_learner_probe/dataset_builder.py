from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Any


CL_ROOT = Path(__file__).resolve().parents[1]
CL1_ROOT = CL_ROOT / "CL1_boundary_fidelity_pilot"
CL1_1_ROOT = CL_ROOT / "CL1_1_action_conditioned_safe_ledger_gate"
for path in (CL1_ROOT, CL1_1_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from action_boundary import candidate_action_admission  # noqa: E402
from domain import ACTIONS, Action, State, all_states, observe, transition  # noqa: E402


Row = dict[str, Any]


def row_from_transition(state: State, action: Action) -> Row:
    successor = transition(state, action)
    source = observe(state)
    target = observe(successor)
    return {
        "source_zones": list(source["zones"]),
        "source_mass": source["mass"],
        "source_phase": source["phase"],
        "action": action,
        "successor_zones": list(target["zones"]),
        "successor_mass": target["mass"],
        "successor_phase": target["phase"],
    }


def build_candidate_rows(horizon: int) -> list[Row]:
    rows: list[Row] = []
    for state in all_states():
        for action in ACTIONS:
            if candidate_action_admission(state, action, horizon) == "ADMIT":
                rows.append(row_from_transition(state, action))
    return rows


def build_unfiltered_equal_volume_rows(count: int, seed: int) -> list[Row]:
    all_rows = [row_from_transition(state, action) for state in all_states() for action in ACTIONS]
    rng = random.Random(seed)
    rng.shuffle(all_rows)
    return all_rows[:count]


def forbidden_fields_present(rows: list[Row]) -> bool:
    forbidden = {
        "collapse_label",
        "future_outcome",
        "collapse_mechanism",
        "witness_class",
        "candidate_admission_decision",
        "oracle_rollout_result",
        "post_hoc_metric",
        "source_file_lineage_as_feature",
        "safe",
        "unsafe",
        "admission_decision",
    }
    for row in rows:
        if forbidden.intersection(row):
            return True
    return False


def source_key(row: Row) -> tuple[tuple[int, ...], int, int]:
    return (tuple(row["source_zones"]), int(row["source_mass"]), int(row["source_phase"]))


def feature_key(row: Row) -> tuple[tuple[int, ...], int, int, str]:
    return (
        tuple(row["source_zones"]),
        int(row["source_mass"]),
        int(row["source_phase"]),
        str(row["action"]),
    )


def target_observation(row: Row) -> dict[str, Any]:
    return {
        "zones": list(row["successor_zones"]),
        "mass": int(row["successor_mass"]),
        "phase": int(row["successor_phase"]),
    }


def source_observation(row: Row) -> dict[str, Any]:
    return {
        "zones": list(row["source_zones"]),
        "mass": int(row["source_mass"]),
        "phase": int(row["source_phase"]),
    }


def random_split(rows: list[Row], seed: int) -> dict[str, list[Row]]:
    shuffled = list(rows)
    random.Random(seed).shuffle(shuffled)
    train_end = int(len(shuffled) * 0.70)
    validation_end = train_end + int(len(shuffled) * 0.15)
    return {
        "train": shuffled[:train_end],
        "validation": shuffled[train_end:validation_end],
        "test": shuffled[validation_end:],
    }


def source_state_holdout_split(rows: list[Row], seed: int, test_fraction: float = 0.15) -> dict[str, list[Row]]:
    by_source: dict[tuple[tuple[int, ...], int, int], list[Row]] = {}
    for row in rows:
        by_source.setdefault(source_key(row), []).append(row)

    keys = list(by_source)
    random.Random(seed + 1).shuffle(keys)
    target_test_count = max(100, int(len(rows) * test_fraction))
    heldout: set[tuple[tuple[int, ...], int, int]] = set()
    test_count = 0
    for key in keys:
        heldout.add(key)
        test_count += len(by_source[key])
        if test_count >= target_test_count:
            break

    train = [row for row in rows if source_key(row) not in heldout]
    test = [row for row in rows if source_key(row) in heldout]
    return {"train": train, "test": test}


def structural_holdout_split(rows: list[Row]) -> dict[str, list[Row]]:
    train = [row for row in rows if int(row["source_phase"]) != 3]
    test = [row for row in rows if int(row["source_phase"]) == 3]
    return {"train": train, "test": test}


def shuffled_targets(rows: list[Row], seed: int) -> list[Row]:
    shuffled = [dict(row) for row in rows]
    targets = [
        (list(row["successor_zones"]), int(row["successor_mass"]), int(row["successor_phase"]))
        for row in rows
    ]
    random.Random(seed + 2).shuffle(targets)
    for row, target in zip(shuffled, targets):
        row["successor_zones"] = target[0]
        row["successor_mass"] = target[1]
        row["successor_phase"] = target[2]
    return shuffled
