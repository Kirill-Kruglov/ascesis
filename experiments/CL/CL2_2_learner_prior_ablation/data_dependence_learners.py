from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


Row = dict[str, Any]
Prediction = dict[str, Any]


TARGET_NAMES = ["z0", "z1", "z2", "z3", "mass", "phase"]


def source_observation(row: Row) -> Prediction:
    return {
        "zones": list(row["source_zones"]),
        "mass": int(row["source_mass"]),
        "phase": int(row["source_phase"]),
    }


def target_observation(row: Row) -> Prediction:
    return {
        "zones": list(row["successor_zones"]),
        "mass": int(row["successor_mass"]),
        "phase": int(row["successor_phase"]),
    }


def target_values(row: Row) -> dict[str, int]:
    zones = list(row["successor_zones"])
    return {
        "z0": int(zones[0]),
        "z1": int(zones[1]),
        "z2": int(zones[2]),
        "z3": int(zones[3]),
        "mass": int(row["successor_mass"]),
        "phase": int(row["successor_phase"]),
    }


class GenericSubsetBackoffLearner:
    """Generic evidence-eligible learner over visible feature subsets.

    It stores majority target-coordinate values for generic feature subsets and
    backs off to smaller subsets. It does not encode action mechanics, phase
    shocks, failed-zone drain, conserve behavior, max bounds, or any oracle.
    """

    def __init__(self) -> None:
        self.tables: dict[str, dict[tuple[Any, ...], dict[str, int]]] = {}
        self.global_target: dict[str, int] = {
            "z0": 0,
            "z1": 0,
            "z2": 0,
            "z3": 0,
            "mass": 0,
            "phase": 0,
        }

    def fit(self, rows: list[Row]) -> None:
        if not rows:
            return
        global_counters = {name: Counter() for name in TARGET_NAMES}
        subset_counters: dict[str, dict[tuple[Any, ...], dict[str, Counter[int]]]] = {}
        subset_names = [
            "full",
            "source_tuple",
            "zones_action",
            "mass_phase_action",
            "action_phase",
            "action_mass",
            "phase",
            "action",
        ]
        for name in subset_names:
            subset_counters[name] = defaultdict(lambda: {target: Counter() for target in TARGET_NAMES})

        for row in rows:
            targets = target_values(row)
            for target_name, value in targets.items():
                global_counters[target_name][value] += 1
            for subset_name in subset_names:
                key = self._key(row, subset_name)
                for target_name, value in targets.items():
                    subset_counters[subset_name][key][target_name][value] += 1

        self.global_target = {
            name: counter.most_common(1)[0][0] for name, counter in global_counters.items()
        }
        self.tables = {}
        for subset_name, keyed in subset_counters.items():
            self.tables[subset_name] = {}
            for key, counters in keyed.items():
                self.tables[subset_name][key] = {
                    target_name: counters[target_name].most_common(1)[0][0]
                    for target_name in TARGET_NAMES
                }

    def predict(self, row: Row) -> Prediction:
        values: dict[str, int] = {}
        for target_name in TARGET_NAMES:
            values[target_name] = self._predict_target(row, target_name)
        return {
            "zones": [values["z0"], values["z1"], values["z2"], values["z3"]],
            "mass": values["mass"],
            "phase": values["phase"],
        }

    def _predict_target(self, row: Row, target_name: str) -> int:
        for subset_name in (
            "full",
            "source_tuple",
            "zones_action",
            "mass_phase_action",
            "action_phase",
            "action_mass",
            "phase",
            "action",
        ):
            table = self.tables.get(subset_name, {})
            key = self._key(row, subset_name)
            if key in table:
                return table[key][target_name]
        return self.global_target[target_name]

    def _key(self, row: Row, subset_name: str) -> tuple[Any, ...]:
        zones = tuple(row["source_zones"])
        mass = int(row["source_mass"])
        phase = int(row["source_phase"])
        action = str(row["action"])
        if subset_name == "full":
            return zones + (mass, phase, action)
        if subset_name == "source_tuple":
            return zones + (mass, phase)
        if subset_name == "zones_action":
            return zones + (action,)
        if subset_name == "mass_phase_action":
            return (mass, phase, action)
        if subset_name == "action_phase":
            return (action, phase)
        if subset_name == "action_mass":
            return (action, mass)
        if subset_name == "phase":
            return (phase,)
        if subset_name == "action":
            return (action,)
        return ()


class ZeroFitGenericLearner(GenericSubsetBackoffLearner):
    def fit(self, rows: list[Row]) -> None:
        del rows
        self.tables = {}
        self.global_target = {"z0": 0, "z1": 0, "z2": 0, "z3": 0, "mass": 0, "phase": 0}
