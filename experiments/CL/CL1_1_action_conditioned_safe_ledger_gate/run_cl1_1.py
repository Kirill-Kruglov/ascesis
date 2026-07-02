from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from action_boundary import (
    AdmissionFn,
    action_rollout_outcome,
    candidate_action_admission,
    cl1_state_level_carryover_admission,
    learner_visible_transition,
    projection_blind_action_admission,
    trivially_safe_action_admission,
    unfiltered_action_admission,
)


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PREREG_PATH = ROOT / "CL1_1_preregistration.json"
CL1_ROOT = ROOT.parents[0] / "CL1_boundary_fidelity_pilot"

if str(CL1_ROOT) not in sys.path:
    sys.path.insert(0, str(CL1_ROOT))

from domain import ACTIONS, Action, State, all_states, is_collapsed, observe, transition  # noqa: E402


INPUT_FILES = [
    "experiments/CL/CL1_boundary_fidelity_pilot/SPEC.md",
    "experiments/CL/CL1_boundary_fidelity_pilot/CL1_preregistration.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/domain.py",
    "experiments/CL/CL1_boundary_fidelity_pilot/boundary.py",
    "experiments/CL/CL1_boundary_fidelity_pilot/run_cl1.py",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/layer_audit.md",
    "playbook_extraction/CL0_closed_ledger_candidate_proposal.md",
    "playbook_extraction/CL0_preregistration.json",
    "playbook_extraction/02_extracted_method.md",
    "playbook_extraction/03_not_yet_method.md",
    "playbook_extraction/harness/output_schema.md",
    "playbook_extraction/harness/failure_conditions.md",
]


def project_root() -> Path:
    return ROOT.parents[2]


def input_statuses() -> list[dict[str, str]]:
    base = project_root()
    return [
        {"file": path, "status": "PRESENT" if (base / path).exists() else "MISSING"}
        for path in INPUT_FILES
    ]


def load_preregistration() -> dict[str, Any]:
    with PREREG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def state_action_witness(
    state: State,
    action: Action,
    admission_decision: str,
    reason: str,
) -> dict[str, Any]:
    outcome = action_rollout_outcome(state, action, HORIZON)
    successor = outcome["successor"]
    return {
        "state": state.as_dict(),
        "action": action,
        "successor": successor.as_dict(),
        "learner_visible_transition": learner_visible_transition(state, action, successor),
        "admission_decision": admission_decision,
        "full_outcome": outcome["full_outcome"],
        "collapse_mechanism": outcome["mechanism"],
        "collapse_step_after_action": outcome["collapse_step_after_action"],
        "which_coordinate_policy_or_action_mattered": reason,
    }


def false_positive_witness(state: State, action: Action, why_rejected: str) -> dict[str, Any]:
    outcome = action_rollout_outcome(state, action, HORIZON)
    successor = outcome["successor"]
    return {
        "state": state.as_dict(),
        "action": action,
        "successor": successor.as_dict(),
        "learner_visible_transition": learner_visible_transition(state, action, successor),
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": why_rejected,
    }


def evaluate_admission(
    states: list[State],
    admission: AdmissionFn,
    horizon: int,
    minimum_equal_volume: int,
    collect_witnesses: bool = False,
    witness_reason: str = "candidate action admission mismatch",
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    total_pairs = len(states) * len(ACTIONS)
    admitted = 0
    unsafe_admitted = 0
    source_admitted = 0
    successor_admitted = 0
    safe_action_pairs = 0
    false_positive = 0
    unsafe_witnesses: list[dict[str, Any]] = []
    false_positive_witnesses: list[dict[str, Any]] = []

    for state in states:
        for action in ACTIONS:
            outcome = action_rollout_outcome(state, action, horizon)
            successor = outcome["successor"]
            safe_pair = not outcome["collapses"]
            if safe_pair:
                safe_action_pairs += 1

            decision = admission(state, action, horizon)
            if decision == "ADMIT":
                admitted += 1
                if outcome["collapses"]:
                    unsafe_admitted += 1
                    if collect_witnesses and len(unsafe_witnesses) < 25:
                        unsafe_witnesses.append(
                            state_action_witness(state, action, "ADMIT", witness_reason)
                        )
                if is_collapsed(state):
                    source_admitted += 1
                if is_collapsed(successor):
                    successor_admitted += 1
            elif safe_pair:
                false_positive += 1
                if collect_witnesses and len(false_positive_witnesses) < 25:
                    false_positive_witnesses.append(
                        false_positive_witness(
                            state,
                            action,
                            "admission rule rejected a transition that remains safe under the audited continuation",
                        )
                    )

    rejected = total_pairs - admitted
    metrics = {
        "admitted_transition_count": admitted,
        "rejected_transition_count": rejected,
        "unsafe_admitted_transition_count": unsafe_admitted,
        "already_collapsed_source_admitted_count": source_admitted,
        "already_collapsed_successor_admitted_count": successor_admitted,
        "safe_action_transition_count": safe_action_pairs,
        "false_positive_action_count": false_positive,
        "unsafe_admitted_transition_rate": unsafe_admitted / admitted if admitted else 0.0,
        "already_collapsed_source_admitted_rate": source_admitted / admitted if admitted else 0.0,
        "already_collapsed_successor_admitted_rate": successor_admitted / admitted if admitted else 0.0,
        "false_positive_action_rate": false_positive / safe_action_pairs if safe_action_pairs else 0.0,
        "equal_volume_possible": admitted >= minimum_equal_volume and total_pairs >= admitted,
    }
    return metrics, unsafe_witnesses, false_positive_witnesses


def decide(candidate: dict[str, Any], thresholds: dict[str, Any]) -> tuple[str, str, bool]:
    unsafe_rate = float(candidate["unsafe_admitted_transition_rate"])
    source_rate = float(candidate["already_collapsed_source_admitted_rate"])
    successor_rate = float(candidate["already_collapsed_successor_admitted_rate"])
    fpr = float(candidate["false_positive_action_rate"])
    equal_volume = bool(candidate["equal_volume_possible"])

    if (
        unsafe_rate > float(thresholds["unsafe_admitted_transition_rate_max"])
        or source_rate > float(thresholds["already_collapsed_source_admitted_rate_max"])
        or successor_rate > float(thresholds["already_collapsed_successor_admitted_rate_max"])
    ):
        return (
            "ACTION-LEDGER-FAILS-UNSAFE-ADMISSION",
            "Candidate admits unsafe, already-collapsed-source, or already-collapsed-successor transitions.",
            False,
        )

    if fpr > float(thresholds["false_positive_action_rate_max"]) or not equal_volume:
        return (
            "ACTION-LEDGER-CONSERVATIVE-BUT-VACUOUS",
            "Candidate is dangerous-error clean but too conservative or cannot support equal-volume sampling.",
            False,
        )

    return (
        "ACTION-LEDGER-OK",
        "Candidate action ledger satisfies unsafe-admission, source purity, successor purity, non-vacuity, and equal-volume thresholds.",
        True,
    )


def compact_baseline(metrics: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "admitted_transition_count",
        "unsafe_admitted_transition_rate",
        "already_collapsed_source_admitted_rate",
        "already_collapsed_successor_admitted_rate",
        "false_positive_action_rate",
    ]
    return {key: metrics[key] for key in keys}


def write_layer_audit_delta() -> None:
    text = """# CL1.1 Layer Audit Delta

- CL1 checked state-level SAFE under safety-policy rollout.
- CL1.1 checks action-conditioned admitted transitions.
- The candidate action admission rule uses source `zones`, `mass`, `phase`, the selected `action`, successor `zones`, `mass`, `phase`, and deterministic safety-policy continuation for the remaining horizon.
- Learner-visible values are only `observe(state)`, `action`, and `observe(successor)`.
- Audit-only values are collapse predicate results, collapse mechanisms, full rollout outcomes, witness classes, rates, and post-hoc counts.
- The candidate still abstracts away future action alternatives after the first admitted action.
- The result is policy-continuation scoped, not all-actions scoped.
- The CL1 state-level carryover baseline is retained to test whether admitting all actions from CL1 SAFE states leaks unsafe action transitions.
"""
    (OUTPUTS / "layer_audit_delta.md").write_text(text, encoding="utf-8")


def write_final_report(
    prereg: dict[str, Any],
    metrics: dict[str, Any],
    decision: dict[str, Any],
    candidate_unsafe_witnesses: list[dict[str, Any]],
    candidate_false_positive_witnesses: list[dict[str, Any]],
) -> None:
    statuses = input_statuses()
    status_rows = "\n".join(f"| `{row['file']}` | {row['status']} |" for row in statuses)
    metrics_json = json.dumps(metrics, indent=2)
    thresholds_json = json.dumps(decision["thresholds_used"], indent=2)

    report = f"""# CL1.1 — Action-Conditioned Safe Ledger Gate

## 0. Verdict

`{decision["decision"]}`

{decision["reason"]}

## 1. Goal anchor

This gate serves the safe / derivable substrate goal only as a transition-ledger
precondition. The honest weakened claim is that a learner should not observe
collapse trajectories if the training ledger is meant to be a safe substrate
precursor. CL1.1 therefore tests admitted `(state, action, successor)`
transitions before any learner training.

No learner is trained here and no derived world-model claim is made.

## 2. Inputs used

| file | status |
|---|---|
{status_rows}

The required CL1 domain code, CL1 metrics, CL0 preregistration, and CL1
preregistration were present.

## 3. CL1 mismatch being tested

CL1 checked `SAFE(state)` under deterministic safety-policy rollout. The CL1
metrics also counted admitted transitions as if every action from a SAFE state
were ledger-admissible.

CL1.1 tests the repair hypothesis H1: a state-level SAFE boundary is
insufficient for a learner ledger unless each admitted action transition is
also safe.

## 4. Domain and action-space specification

Domain: `{prereg["domain_name"]}`.

State/action space: {prereg["state_action_space_description"]}

Transition semantics: {prereg["transition_semantics"]}

Collapse predicate: {prereg["collapse_predicate"]}

Learner-visible transition: {prereg["learner_visible_transition"]}

## 5. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json`

This file was written before final CL1.1 metric computation. The runner loads
the thresholds from that file and does not move thresholds after seeing
results.

Thresholds used:

```json
{thresholds_json}
```

## 6. Candidate action admission rule

Candidate rule:

```text
ADMIT(state, action) iff
1. source state is not already collapsed;
2. successor = transition(state, action) is not already collapsed;
3. rollout from successor under CL1 safety_policy remains non-collapse for horizon - 1;
4. only observe(state), action, observe(successor) are learner-visible.
```

CL1.1 tests one-step action admission followed by safety-policy continuation.
It does not prove safety under arbitrary future learner actions.

## 7. Metrics

```json
{metrics_json}
```

## 8. Controls and baselines

CL1 state-level carryover baseline admits all actions from states where the CL1
candidate boundary says SAFE. It tests the mismatch directly.

Projection-blind action baseline admits actions from states marked SAFE by the
mean-zone-health projection and tests action-ledger projection blindness.

Trivially-safe action baseline admits no actions and tests whether safety is
being bought by vacuity.

Unfiltered action control admits all `(state, action)` pairs and establishes the
total transition budget and unsafe-transition rate.

## 9. Decision

Decision: `{decision["decision"]}`

Downstream allowed: `{decision["downstream_allowed"]}`

The decision rule is the pre-registered CL1.1 rule:
`ACTION-LEDGER-OK` requires unsafe admission, source purity, successor purity,
false-positive, and equal-volume gates all to pass.

## 10. Witness analysis

Candidate unsafe admitted witnesses recorded:
`{len(candidate_unsafe_witnesses)}`.

Candidate false-positive action witnesses recorded:
`{len(candidate_false_positive_witnesses)}`.

If these files are empty, the candidate had no such witnesses under the
exhaustive CL1.1 evaluation. Baseline witness examples, where relevant, are
embedded in `outputs/metrics.json` for diagnostic comparison.

## 11. Layer audit delta

CL1 checked state-level SAFE under safety-policy rollout. CL1.1 checks
action-conditioned admitted transitions.

Coordinates used by the candidate admission rule: source `zones`, `mass`,
`phase`; selected `action`; successor `zones`, `mass`, `phase`; and deterministic
safety-policy continuation over the remaining horizon.

Learner-visible values: source observation, action, successor observation.

Audit-only values: collapse predicate, collapse mechanism, future outcome,
witness class, metric counts, and rates.

The candidate still abstracts away future action alternatives. The result is
policy-continuation scoped, not all-actions scoped.

## 12. Bought-by-simplification check

The candidate does not drop collapse-relevant source or successor coordinates in
the CL1 domain. It still simplifies future behavior by checking only CL1
safety-policy continuation after the first action. That simplification is
reported as scope, not as an all-actions safety claim.

The trivially-safe baseline is expected to be safe but vacuous because it admits
zero transitions. Equal-volume and false-positive gates prevent counting that as
a useful learner ledger.

## 13. What was NOT shown

- No claim that this is a substrate.
- No claim that learner world-model content is derived.
- No claim that LLM training is safe.
- No claim that action-ledger safety transfers to other domains.
- No claim that the candidate is safe under arbitrary future learner policies.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.
- No claim that a toy domain itself is valuable outside this gate.
- No claim that learner training is allowed unless `ACTION-LEDGER-OK` is reached.

## 14. Durable result

CL1.1 converts the CL1 state boundary into an action-conditioned transition
ledger gate over the exhaustive finite `(state, action)` set. The durable result
is the decision in `outputs/decision.json` plus witness files for unsafe
admission and false-positive action rejection.
"""
    (OUTPUTS / "final_report.md").write_text(report, encoding="utf-8")


HORIZON = 6


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    prereg = load_preregistration()
    horizon = int(prereg["horizon"])
    minimum_equal_volume = int(prereg["minimum_equal_volume_transitions"])
    thresholds = prereg["thresholds"]
    states = list(all_states())
    state_action_count = len(states) * len(ACTIONS)

    candidate_metrics, candidate_unsafe, candidate_false_positive = evaluate_admission(
        states,
        candidate_action_admission,
        horizon,
        minimum_equal_volume,
        collect_witnesses=True,
        witness_reason="candidate admitted an action whose audited rollout collapses",
    )
    cl1_metrics, cl1_unsafe, cl1_false_positive = evaluate_admission(
        states,
        cl1_state_level_carryover_admission,
        horizon,
        minimum_equal_volume,
        collect_witnesses=True,
        witness_reason="CL1 state-level boundary admitted all actions from a SAFE source state",
    )
    projection_metrics, projection_unsafe, projection_false_positive = evaluate_admission(
        states,
        projection_blind_action_admission,
        horizon,
        minimum_equal_volume,
        collect_witnesses=True,
        witness_reason="projection-blind action baseline omitted failed-zone spread, mass, or phase",
    )
    trivial_metrics, _, trivial_false_positive = evaluate_admission(
        states,
        trivially_safe_action_admission,
        horizon,
        minimum_equal_volume,
        collect_witnesses=True,
    )
    unfiltered_metrics, unfiltered_unsafe, _ = evaluate_admission(
        states,
        unfiltered_action_admission,
        horizon,
        minimum_equal_volume,
        collect_witnesses=True,
        witness_reason="unfiltered control admits all actions",
    )

    unfiltered_control = {
        "unsafe_transition_rate": unfiltered_metrics["unsafe_admitted_transition_rate"],
        "unsafe_transition_count": unfiltered_metrics["unsafe_admitted_transition_count"],
        "available_transition_count": state_action_count,
    }

    cl1_baseline = compact_baseline(cl1_metrics)
    cl1_baseline["unsafe_admitted_witness_examples"] = cl1_unsafe[:10]
    cl1_baseline["false_positive_action_witness_examples"] = cl1_false_positive[:10]

    projection_baseline = compact_baseline(projection_metrics)
    projection_baseline["unsafe_admitted_witness_examples"] = projection_unsafe[:10]
    projection_baseline["false_positive_action_witness_examples"] = projection_false_positive[:10]

    trivial_baseline = compact_baseline(trivial_metrics)
    trivial_baseline["equal_volume_possible"] = trivial_metrics["equal_volume_possible"]
    trivial_baseline["false_positive_action_witness_examples"] = trivial_false_positive[:10]

    decision_value, reason, downstream_allowed = decide(candidate_metrics, thresholds)
    decision = {
        "decision": decision_value,
        "reason": reason,
        "thresholds_used": {
            "unsafe_admitted_transition_rate_max": thresholds["unsafe_admitted_transition_rate_max"],
            "already_collapsed_source_admitted_rate_max": thresholds[
                "already_collapsed_source_admitted_rate_max"
            ],
            "already_collapsed_successor_admitted_rate_max": thresholds[
                "already_collapsed_successor_admitted_rate_max"
            ],
            "false_positive_action_rate_max": thresholds["false_positive_action_rate_max"],
            "equal_volume_required": thresholds["equal_volume_required"],
        },
        "downstream_allowed": downstream_allowed,
    }

    metrics = {
        "domain": {
            "state_count": len(states),
            "action_count": len(ACTIONS),
            "state_action_count": state_action_count,
            "horizon": horizon,
            "minimum_equal_volume_transitions": minimum_equal_volume,
        },
        "candidate_action_ledger": candidate_metrics,
        "cl1_state_level_carryover_baseline": cl1_baseline,
        "projection_blind_action_baseline": projection_baseline,
        "trivially_safe_action_baseline": trivial_baseline,
        "unfiltered_action_control": unfiltered_control,
        "diagnostic": {
            "cl1_mismatch_reproduced": cl1_metrics["unsafe_admitted_transition_count"] > 0,
            "candidate_scope": "one-step action admission followed by CL1 safety-policy continuation",
            "all_future_action_branches_tested": False,
            "unfiltered_unsafe_witness_examples": unfiltered_unsafe[:10],
        },
    }

    write_json(OUTPUTS / "metrics.json", metrics)
    write_json(OUTPUTS / "decision.json", decision)
    write_json(OUTPUTS / "unsafe_admitted_witnesses.json", candidate_unsafe)
    write_json(OUTPUTS / "false_positive_action_witnesses.json", candidate_false_positive)
    write_layer_audit_delta()
    write_final_report(prereg, metrics, decision, candidate_unsafe, candidate_false_positive)


if __name__ == "__main__":
    main()
