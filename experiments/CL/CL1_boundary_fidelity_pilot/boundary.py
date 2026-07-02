from __future__ import annotations

from domain import State, collapse_relevant_coordinates, rollout_outcome


def candidate_boundary(state: State, horizon: int) -> str:
    collapses, _, _, _ = rollout_outcome(state, horizon)
    return "DOOMED" if collapses else "SAFE"


def projection_blind_boundary(state: State, horizon: int) -> str:
    del horizon
    coords = collapse_relevant_coordinates(state)
    mean_zone_health = float(coords["mean_zone_health"])
    # Deliberately projection-blind: ignores failed-zone spread, mass and phase.
    return "SAFE" if mean_zone_health > 1.5 else "DOOMED"


def trivially_safe_boundary(state: State, horizon: int) -> str:
    del state, horizon
    return "DOOMED"

