from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Any


CL_ROOT = Path(__file__).resolve().parents[1]
CL2_ROOT = CL_ROOT / "CL2_equal_volume_learner_probe"
for path in (CL2_ROOT,):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from dataset_builder import (  # noqa: E402
    build_candidate_rows,
    forbidden_fields_present,
    source_key,
    source_state_holdout_split,
    structural_holdout_split,
)


Row = dict[str, Any]


def copy_rows(rows: list[Row]) -> list[Row]:
    return [
        dict(row, source_zones=list(row["source_zones"]), successor_zones=list(row["successor_zones"]))
        for row in rows
    ]


def build_rows() -> list[Row]:
    return build_candidate_rows(horizon=6)


def build_required_splits(rows: list[Row], seed: int) -> dict[str, dict[str, list[Row]]]:
    source = source_state_holdout_split(rows, seed)
    structural = structural_holdout_split(rows)
    cross_phase = structural_holdout_split(rows)
    return {
        "source": source,
        "structural": structural,
        "cross_phase": cross_phase,
    }


def sample_fraction(rows: list[Row], fraction: float, seed: int) -> list[Row]:
    if fraction >= 1.0:
        return list(rows)
    count = max(1, int(len(rows) * fraction))
    output = list(rows)
    random.Random(seed).shuffle(output)
    return output[:count]


def independent_impossible_targets(rows: list[Row], seed: int) -> list[Row]:
    rng = random.Random(seed + 101)
    output = copy_rows(rows)
    observed_zone_values = sorted({value for row in rows for value in row["source_zones"] + row["successor_zones"]})
    observed_mass_values = sorted({int(row["source_mass"]) for row in rows} | {int(row["successor_mass"]) for row in rows})
    observed_phase_values = sorted({int(row["source_phase"]) for row in rows} | {int(row["successor_phase"]) for row in rows})
    for row in output:
        row["successor_zones"] = [rng.choice(observed_zone_values) for _ in row["source_zones"]]
        row["successor_mass"] = rng.choice(observed_mass_values)
        row["successor_phase"] = rng.choice(observed_phase_values)
    return output


def cross_phase_target_shuffle(rows: list[Row], seed: int) -> list[Row]:
    output = copy_rows(rows)
    rng = random.Random(seed + 202)
    targets_by_phase: dict[int, list[tuple[list[int], int, int]]] = {}
    for row in rows:
        phase = int(row["source_phase"])
        targets_by_phase.setdefault(phase, []).append(
            (list(row["successor_zones"]), int(row["successor_mass"]), int(row["successor_phase"]))
        )
    for targets in targets_by_phase.values():
        rng.shuffle(targets)
    for row in output:
        phase = int(row["source_phase"])
        other_phases = [candidate for candidate in targets_by_phase if candidate != phase and targets_by_phase[candidate]]
        if not other_phases:
            other_phases = [candidate for candidate in targets_by_phase if targets_by_phase[candidate]]
        chosen = rng.choice(other_phases)
        target = targets_by_phase[chosen].pop()
        row["successor_zones"] = list(target[0])
        row["successor_mass"] = target[1]
        row["successor_phase"] = target[2]
    return output


def feature_permutation_control(rows: list[Row], seed: int) -> list[Row]:
    rng = random.Random(seed + 303)
    output = copy_rows(rows)
    zones = [list(row["source_zones"]) for row in rows]
    masses = [int(row["source_mass"]) for row in rows]
    phases = [int(row["source_phase"]) for row in rows]
    actions = [row["action"] for row in rows]
    rng.shuffle(zones)
    rng.shuffle(masses)
    rng.shuffle(phases)
    rng.shuffle(actions)
    for idx, row in enumerate(output):
        row["source_zones"] = list(zones[idx])
        row["source_mass"] = masses[idx]
        row["source_phase"] = phases[idx]
        row["action"] = actions[idx]
    return output


def exact_source_overlap(train: list[Row], test: list[Row]) -> float:
    if not test:
        return 0.0
    train_sources = {source_key(row) for row in train}
    return sum(1 for row in test if source_key(row) in train_sources) / len(test)
