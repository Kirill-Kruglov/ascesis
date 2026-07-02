from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal


Action = Literal["AID_0", "AID_1", "AID_2", "AID_3", "CONSERVE"]
Mechanism = Literal["none", "spread", "mass", "both"]

ACTIONS: tuple[Action, ...] = ("AID_0", "AID_1", "AID_2", "AID_3", "CONSERVE")
ZONE_COUNT = 4
MAX_ZONE = 4
MAX_MASS = 6


@dataclass(frozen=True, order=True)
class State:
    zones: tuple[int, int, int, int]
    mass: int
    phase: int

    def as_dict(self) -> dict[str, object]:
        return {"zones": list(self.zones), "mass": self.mass, "phase": self.phase}


def all_states() -> Iterable[State]:
    for z0 in range(MAX_ZONE + 1):
        for z1 in range(MAX_ZONE + 1):
            for z2 in range(MAX_ZONE + 1):
                for z3 in range(MAX_ZONE + 1):
                    for mass in range(MAX_MASS + 1):
                        for phase in range(ZONE_COUNT):
                            yield State((z0, z1, z2, z3), mass, phase)


def observe(state: State) -> dict[str, object]:
    """Learner-visible observation; no collapse labels or future outcomes."""

    return state.as_dict()


def collapse_mechanism(state: State) -> Mechanism:
    spread = sum(1 for z in state.zones if z <= 0) >= 2
    mass = state.mass <= 0
    if spread and mass:
        return "both"
    if spread:
        return "spread"
    if mass:
        return "mass"
    return "none"


def is_collapsed(state: State) -> bool:
    return collapse_mechanism(state) != "none"


def transition(state: State, action: Action) -> State:
    zones = list(state.zones)
    mass = state.mass

    if action == "CONSERVE":
        mass = min(MAX_MASS, mass + 1)
    else:
        idx = int(action[-1])
        zones[idx] = min(MAX_ZONE, zones[idx] + 1)
        mass -= 1

    shock_idx = state.phase
    zones[shock_idx] = max(0, zones[shock_idx] - 1)

    failed_count = sum(1 for z in zones if z <= 0)
    if failed_count:
        mass -= failed_count

    mass = max(0, min(MAX_MASS, mass))
    next_phase = (state.phase + 1) % ZONE_COUNT
    return State(tuple(zones), mass, next_phase)  # type: ignore[arg-type]


def safety_policy(state: State) -> Action:
    if state.mass <= 1:
        return "CONSERVE"
    weakest = min(range(ZONE_COUNT), key=lambda idx: (state.zones[idx], idx))
    if state.zones[weakest] <= 2:
        return f"AID_{weakest}"  # type: ignore[return-value]
    return "CONSERVE"


def rollout_outcome(state: State, horizon: int) -> tuple[bool, Mechanism, State, int]:
    current = state
    if is_collapsed(current):
        return True, collapse_mechanism(current), current, 0

    for step in range(1, horizon + 1):
        current = transition(current, safety_policy(current))
        if is_collapsed(current):
            return True, collapse_mechanism(current), current, step

    return False, "none", current, horizon


def collapse_relevant_coordinates(state: State) -> dict[str, object]:
    failed_zones = sum(1 for z in state.zones if z <= 0)
    return {
        "failed_zone_count": failed_zones,
        "mass": state.mass,
        "mean_zone_health": sum(state.zones) / ZONE_COUNT,
        "phase": state.phase,
    }

