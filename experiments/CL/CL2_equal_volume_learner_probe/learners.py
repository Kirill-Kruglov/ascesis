from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Protocol


Row = dict[str, Any]
Prediction = dict[str, Any]


def _target(row: Row) -> Prediction:
    return {
        "zones": list(row["successor_zones"]),
        "mass": int(row["successor_mass"]),
        "phase": int(row["successor_phase"]),
    }


def _source(row: Row) -> Prediction:
    return {
        "zones": list(row["source_zones"]),
        "mass": int(row["source_mass"]),
        "phase": int(row["source_phase"]),
    }


def _feature_key(row: Row) -> tuple[tuple[int, ...], int, int, str]:
    return (
        tuple(row["source_zones"]),
        int(row["source_mass"]),
        int(row["source_phase"]),
        str(row["action"]),
    )


def _target_key(row: Row) -> tuple[tuple[int, ...], int, int]:
    return (tuple(row["successor_zones"]), int(row["successor_mass"]), int(row["successor_phase"]))


class Learner(Protocol):
    def fit(self, rows: list[Row]) -> None:
        ...

    def predict(self, row: Row) -> Prediction:
        ...


class CopySourceBaseline:
    def fit(self, rows: list[Row]) -> None:
        del rows

    def predict(self, row: Row) -> Prediction:
        return _source(row)


class MajorityDeltaBaseline:
    def __init__(self) -> None:
        self.delta_by_action: dict[str, tuple[tuple[int, ...], int, int]] = {}
        self.global_delta: tuple[tuple[int, ...], int, int] = ((0, 0, 0, 0), 0, 0)

    def fit(self, rows: list[Row]) -> None:
        by_action: dict[str, Counter[tuple[tuple[int, ...], int, int]]] = defaultdict(Counter)
        global_counter: Counter[tuple[tuple[int, ...], int, int]] = Counter()
        for row in rows:
            source_zones = list(row["source_zones"])
            successor_zones = list(row["successor_zones"])
            delta = (
                tuple(successor_zones[i] - source_zones[i] for i in range(len(source_zones))),
                int(row["successor_mass"]) - int(row["source_mass"]),
                int(row["successor_phase"]) - int(row["source_phase"]),
            )
            by_action[str(row["action"])][delta] += 1
            global_counter[delta] += 1
        self.global_delta = global_counter.most_common(1)[0][0] if global_counter else self.global_delta
        self.delta_by_action = {
            action: counter.most_common(1)[0][0] for action, counter in by_action.items()
        }

    def predict(self, row: Row) -> Prediction:
        delta = self.delta_by_action.get(str(row["action"]), self.global_delta)
        source_zones = list(row["source_zones"])
        zones = [source_zones[i] + delta[0][i] for i in range(len(source_zones))]
        return {
            "zones": zones,
            "mass": int(row["source_mass"]) + delta[1],
            "phase": int(row["source_phase"]) + delta[2],
        }


class MemorizerBaseline:
    def __init__(self) -> None:
        self.table: dict[tuple[tuple[int, ...], int, int, str], Prediction] = {}
        self.fallback = MajorityDeltaBaseline()

    def fit(self, rows: list[Row]) -> None:
        self.table = {_feature_key(row): _target(row) for row in rows}
        self.fallback.fit(rows)

    def predict(self, row: Row) -> Prediction:
        prediction = self.table.get(_feature_key(row))
        if prediction is not None:
            return {"zones": list(prediction["zones"]), "mass": prediction["mass"], "phase": prediction["phase"]}
        return self.fallback.predict(row)


class RuleFamilyTransitionLearner:
    """Fits a small visible-variable transition-rule family from rows.

    The learner is intentionally simple and fixed. It searches parameters inside
    a generic action/shock/drain update family using only source observations,
    action names, and successor observations from training rows. Prediction does
    not call any domain, rollout, collapse, or admission oracle.
    """

    def __init__(self) -> None:
        self.zone_count = 4
        self.max_zone = 4
        self.max_mass = 6
        self.params = {
            "aid_zone_delta": 0,
            "aid_mass_delta": 0,
            "conserve_mass_delta": 0,
            "shock_delta": 0,
            "failed_zone_mass_cost": 0,
            "phase_offset": 1,
        }

    def fit(self, rows: list[Row]) -> None:
        if not rows:
            return
        self.zone_count = len(rows[0]["source_zones"])
        self.max_zone = max(
            max(max(row["source_zones"]), max(row["successor_zones"])) for row in rows
        )
        self.max_mass = max(
            max(int(row["source_mass"]), int(row["successor_mass"])) for row in rows
        )

        best_score: tuple[int, int] | None = None
        best_params: dict[str, int] | None = None
        for aid_zone_delta in (0, 1):
            for aid_mass_delta in (-1, 0):
                for conserve_mass_delta in (0, 1):
                    for shock_delta in (0, 1):
                        for failed_zone_mass_cost in (0, 1):
                            for phase_offset in range(self.zone_count):
                                params = {
                                    "aid_zone_delta": aid_zone_delta,
                                    "aid_mass_delta": aid_mass_delta,
                                    "conserve_mass_delta": conserve_mass_delta,
                                    "shock_delta": shock_delta,
                                    "failed_zone_mass_cost": failed_zone_mass_cost,
                                    "phase_offset": phase_offset,
                                }
                                exact_errors = 0
                                coordinate_errors = 0
                                for row in rows:
                                    prediction = self._predict_with_params(row, params)
                                    target = _target(row)
                                    if prediction != target:
                                        exact_errors += 1
                                    coordinate_errors += _coordinate_error_count(prediction, target)
                                score = (exact_errors, coordinate_errors)
                                if best_score is None or score < best_score:
                                    best_score = score
                                    best_params = params
        if best_params is not None:
            self.params = best_params

    def predict(self, row: Row) -> Prediction:
        return self._predict_with_params(row, self.params)

    def _predict_with_params(self, row: Row, params: dict[str, int]) -> Prediction:
        zones = list(row["source_zones"])
        mass = int(row["source_mass"])
        phase = int(row["source_phase"])
        action = str(row["action"])

        if action == "CONSERVE":
            mass = min(self.max_mass, mass + params["conserve_mass_delta"])
        elif action.startswith("AID_"):
            try:
                idx = int(action.split("_", 1)[1])
            except ValueError:
                idx = 0
            if 0 <= idx < len(zones):
                zones[idx] = min(self.max_zone, zones[idx] + params["aid_zone_delta"])
            mass += params["aid_mass_delta"]

        if 0 <= phase < len(zones):
            zones[phase] = max(0, zones[phase] - params["shock_delta"])

        failed_count = sum(1 for value in zones if value <= 0)
        mass -= failed_count * params["failed_zone_mass_cost"]
        mass = max(0, min(self.max_mass, mass))
        next_phase = (phase + params["phase_offset"]) % self.zone_count

        return {"zones": zones, "mass": mass, "phase": next_phase}


def _coordinate_error_count(prediction: Prediction, target: Prediction) -> int:
    errors = 0
    for idx, value in enumerate(target["zones"]):
        if prediction["zones"][idx] != value:
            errors += 1
    if prediction["mass"] != target["mass"]:
        errors += 1
    if prediction["phase"] != target["phase"]:
        errors += 1
    return errors
