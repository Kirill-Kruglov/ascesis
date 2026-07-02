from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, Literal, TypedDict


CL1_ROOT = Path(__file__).resolve().parents[1] / "CL1_boundary_fidelity_pilot"
if str(CL1_ROOT) not in sys.path:
    sys.path.insert(0, str(CL1_ROOT))

from boundary import candidate_boundary, projection_blind_boundary  # noqa: E402
from domain import (  # noqa: E402
    Action,
    Mechanism,
    State,
    collapse_mechanism,
    is_collapsed,
    observe,
    safety_policy,
    transition,
)


Admission = Literal["ADMIT", "REJECT"]


class ActionOutcome(TypedDict):
    successor: State
    collapses: bool
    mechanism: Mechanism
    collapse_step_after_action: int | None
    full_outcome: str


def action_rollout_outcome(state: State, action: Action, horizon: int) -> ActionOutcome:
    """Audit-only full outcome for first action plus safety-policy continuation."""

    successor = transition(state, action)

    if is_collapsed(state):
        mechanism = collapse_mechanism(state)
        return {
            "successor": successor,
            "collapses": True,
            "mechanism": mechanism,
            "collapse_step_after_action": 0,
            "full_outcome": "source_already_collapsed_step_0",
        }

    if is_collapsed(successor):
        mechanism = collapse_mechanism(successor)
        return {
            "successor": successor,
            "collapses": True,
            "mechanism": mechanism,
            "collapse_step_after_action": 1,
            "full_outcome": "successor_collapsed_step_1",
        }

    current = successor
    for step in range(2, horizon + 1):
        current = transition(current, safety_policy(current))
        if is_collapsed(current):
            mechanism = collapse_mechanism(current)
            return {
                "successor": successor,
                "collapses": True,
                "mechanism": mechanism,
                "collapse_step_after_action": step,
                "full_outcome": f"collapse_within_horizon_step_{step}",
            }

    return {
        "successor": successor,
        "collapses": False,
        "mechanism": "none",
        "collapse_step_after_action": None,
        "full_outcome": "remains_safe_within_horizon",
    }


def learner_visible_transition(state: State, action: Action, successor: State) -> dict[str, object]:
    return {
        "source_observation": observe(state),
        "action": action,
        "successor_observation": observe(successor),
    }


def candidate_action_admission(state: State, action: Action, horizon: int) -> Admission:
    outcome = action_rollout_outcome(state, action, horizon)
    return "REJECT" if outcome["collapses"] else "ADMIT"


def cl1_state_level_carryover_admission(state: State, action: Action, horizon: int) -> Admission:
    del action
    return "ADMIT" if candidate_boundary(state, horizon) == "SAFE" else "REJECT"


def projection_blind_action_admission(state: State, action: Action, horizon: int) -> Admission:
    del action
    return "ADMIT" if projection_blind_boundary(state, horizon) == "SAFE" else "REJECT"


def trivially_safe_action_admission(state: State, action: Action, horizon: int) -> Admission:
    del state, action, horizon
    return "REJECT"


def unfiltered_action_admission(state: State, action: Action, horizon: int) -> Admission:
    del state, action, horizon
    return "ADMIT"


AdmissionFn = Callable[[State, Action, int], Admission]
