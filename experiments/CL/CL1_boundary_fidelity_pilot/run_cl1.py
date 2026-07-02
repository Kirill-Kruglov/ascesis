from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from boundary import candidate_boundary, projection_blind_boundary, trivially_safe_boundary
from domain import ACTIONS, State, all_states, collapse_mechanism, is_collapsed, observe, rollout_outcome


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PREREG_PATH = ROOT / "CL1_preregistration.json"


BoundaryFn = Callable[[State, int], str]


def load_preregistration() -> dict:
    with PREREG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def witness(
    state: State,
    decision: str,
    full_outcome: str,
    mechanism: str,
    coordinate: str,
) -> dict[str, object]:
    return {
        "state": state.as_dict(),
        "observation": observe(state),
        "boundary_decision": decision,
        "full_outcome": full_outcome,
        "collapse_mechanism": mechanism,
        "which_coordinate_or_projection_mattered": coordinate,
    }


def evaluate_boundary(
    states: list[State],
    boundary: BoundaryFn,
    horizon: int,
    collect_witnesses: bool = False,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    safe_labeled = 0
    false_safe = 0
    already_collapsed = 0
    already_collapsed_safe = 0
    full_safe = 0
    false_positive = 0
    admitted_transition_count = 0
    false_safe_witnesses: list[dict[str, object]] = []
    false_positive_witnesses: list[dict[str, object]] = []

    for state in states:
        decision = boundary(state, horizon)
        collapses, mechanism, _, step = rollout_outcome(state, horizon)
        already = is_collapsed(state)

        if decision == "SAFE":
            safe_labeled += 1
            admitted_transition_count += len(ACTIONS)
            if collapses:
                false_safe += 1
                if collect_witnesses and len(false_safe_witnesses) < 25:
                    coordinate = "candidate boundary mismatch"
                    if boundary is projection_blind_boundary:
                        coordinate = "projection omitted failed_zone_count and mass"
                    false_safe_witnesses.append(
                        witness(
                            state,
                            decision,
                            f"collapse_within_horizon_step_{step}",
                            mechanism,
                            coordinate,
                        )
                    )

        if already:
            already_collapsed += 1
            if decision == "SAFE":
                already_collapsed_safe += 1

        if not collapses:
            full_safe += 1
            if decision == "DOOMED":
                false_positive += 1
                if collect_witnesses and len(false_positive_witnesses) < 25:
                    false_positive_witnesses.append(
                        witness(
                            state,
                            decision,
                            "remains_safe_within_horizon",
                            "none",
                            "boundary was conservative for this state",
                        )
                    )

    metrics = {
        "safe_labeled_count": safe_labeled,
        "doomed_labeled_count": len(states) - safe_labeled,
        "false_safe_count": false_safe,
        "already_collapsed_count": already_collapsed,
        "already_collapsed_labeled_safe_count": already_collapsed_safe,
        "full_safe_count": full_safe,
        "false_positive_count": false_positive,
        "admitted_transition_count": admitted_transition_count,
        "false_safe_rate": false_safe / safe_labeled if safe_labeled else 0.0,
        "already_collapsed_labeled_safe_rate": (
            already_collapsed_safe / already_collapsed if already_collapsed else 0.0
        ),
        "false_positive_rate": false_positive / full_safe if full_safe else 0.0,
    }
    return metrics, false_safe_witnesses, false_positive_witnesses


def decide(candidate_metrics: dict[str, object], thresholds: dict[str, object]) -> tuple[str, str, bool]:
    false_safe_rate = float(candidate_metrics["false_safe_rate"])
    already_rate = float(candidate_metrics["already_collapsed_labeled_safe_rate"])
    false_positive_rate = float(candidate_metrics["false_positive_rate"])
    equal_volume_possible = bool(candidate_metrics["equal_volume_possible"])

    if false_safe_rate > float(thresholds["false_safe_rate_max"]) or already_rate > float(
        thresholds["already_collapsed_labeled_safe_rate_max"]
    ):
        return (
            "BOUNDARY-FAILS-FALSE-SAFE",
            "Candidate boundary labels collapse-bound or already-collapsed states SAFE.",
            False,
        )

    if false_positive_rate > float(thresholds["false_positive_rate_max"]) or not equal_volume_possible:
        return (
            "BOUNDARY-CONSERVATIVE-BUT-VACUOUS",
            "Candidate boundary is dangerous-error clean but too conservative or cannot support equal-volume sampling.",
            False,
        )

    return (
        "BOUNDARY-FIDELITY-OK",
        "Candidate boundary satisfies false-safe, purity, non-vacuity, and equal-volume thresholds on the exhaustive state set.",
        True,
    )


def write_layer_audit() -> None:
    text = """# CL1 Layer Audit

| coordinate | roles | boundary use | learner visible | risk if projected away |
|---|---|---|---|---|
| `zones` | DYNAMICS, OBSERVATION, PROJECTION | Candidate boundary uses full zone vector for rollout. | Yes | Omitting failed-zone count can hide spread collapse. |
| `mass` | DYNAMICS, OBSERVATION, PROJECTION | Candidate boundary uses mass for rollout. | Yes | Omitting mass can hide global resource collapse. |
| `phase` | DYNAMICS, OBSERVATION, PROJECTION | Candidate boundary uses phase to know the next lawful exogenous shock. | Yes | Omitting phase can mispredict near-horizon shocks. |
| `collapse_predicate` | AUDIT-ONLY | Used only for ground truth and metric computation. | No | If made learner-visible, it leaks oracle labels. |
| `future_rollout_outcome` | AUDIT-ONLY | Used only for metric computation and candidate boundary's transition-semantics rollout, not as a stored label. | No | Stored labels would turn the boundary into an oracle. |
| `mean_zone_health` | REPORTING, PROJECTION baseline | Used only by projection-blind baseline. | Derivable from observation | As a sole coordinate, it hides spread collapse. |
| `safe_labeled_count` and rates | REPORTING | Not used as boundary evidence. | No | Using post-hoc rates as boundary input would be circular. |

Projected-away coordinates for the candidate: none of the domain's collapse-relevant
state coordinates (`zones`, `mass`, `phase`) are projected away. The candidate still
abstracts away action alternatives by evaluating the pre-registered safety policy only.

Projection-blind baseline projected-away risks: failed-zone spread, mass, and phase.
"""
    (OUTPUTS / "layer_audit.md").write_text(text, encoding="utf-8")


def write_final_report(
    prereg: dict,
    metrics: dict,
    decision: dict,
    candidate_false_safe_witnesses: list[dict[str, object]],
    candidate_false_positive_witnesses: list[dict[str, object]],
) -> None:
    report = f"""# CL1 — Minimal Lawful Domain Boundary-Fidelity Pilot

## 0. Verdict

`{decision["decision"]}`

{decision["reason"]}

## 1. Goal anchor

This pilot serves the safe / derivable substrate goal only as a safety-boundary
precondition test. It asks whether one minimal lawful generated domain can
support a faithful and non-vacuous boundary before any learner training.

## 2. Inputs used

| file | status |
|---|---|
| `playbook_extraction/CL0_closed_ledger_candidate_proposal.md` | METHOD/EVIDENCE |
| `playbook_extraction/CL0_preregistration.json` | METHOD |
| `playbook_extraction/02_extracted_method.md` | METHOD |
| `playbook_extraction/03_not_yet_method.md` | METHOD |
| `playbook_extraction/harness/output_schema.md` | METHOD |
| `playbook_extraction/harness/failure_conditions.md` | METHOD |
| `research/closed_directions_ledger.md` | MISSING |
| `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` | EVIDENCE |
| `research/faithful_abstraction_v1/01_empirical_basis.md` | EVIDENCE |
| `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | EVIDENCE |
| `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md` | EVIDENCE |
| `experiments/BA/BA4_layer_audit/justitia_layer_audit.md` | EVIDENCE |
| `experiments/15_collapse_boundary/outputs_15_2/summary.md` | EVIDENCE |
| `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md` | EVIDENCE |
| `experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json` | EVIDENCE |
| `experiments/JB/18_1_shielded_training/claude_code_task_18_1_shielded_training.md` | EVIDENCE |

## 3. Domain specification

Domain: `{prereg["domain_name"]}`.

State space: {prereg["state_space_description"]}

Transition semantics: {prereg["transition_semantics"]}

Collapse predicate: {prereg["collapse_predicate"]}

Learner-visible observation: {prereg["learner_visible_observation"]}

Horizon: `{prereg["horizon"]}`.

Evaluation set: exhaustive finite state set.

## 4. Layer audit summary

The candidate boundary uses `zones`, `mass`, and `phase` as layer-eligible
DYNAMICS / OBSERVATION / PROJECTION coordinates. Collapse labels and future
outcomes are AUDIT-ONLY. Reporting rates are not boundary evidence. Full table:
`outputs/layer_audit.md`.

## 5. Pre-registration provenance

`CL1_preregistration.json` was written before final metric computation. The
runner reads this file and uses its thresholds unchanged:

```json
{json.dumps(prereg["thresholds"], indent=2)}
```

## 6. Metrics

```json
{json.dumps(metrics, indent=2)}
```

## 7. Controls and baselines

- Candidate boundary: bounded rollout under the safety policy using
  layer-eligible coordinates.
- Projection-blind baseline: uses mean zone health only; omits spread, mass,
  and phase. It is expected to expose 18.1-style projection blindness.
- Trivially-safe baseline: labels all states DOOMED; detects vacuity.
- Unfiltered control: no boundary filtering; used for equal-volume comparison.

## 8. Decision

Decision: `{decision["decision"]}`.

Downstream allowed: `{decision["downstream_allowed"]}`.

The decision follows the exact CL1 rule over false-safe, already-collapsed
purity, false-positive/non-vacuity, and equal-volume conditions.

## 9. Witness analysis

Candidate false-safe witnesses: `{len(candidate_false_safe_witnesses)}`.

Candidate false-positive witnesses recorded: `{len(candidate_false_positive_witnesses)}`.

If witness lists are empty, the corresponding output file contains `[]`. The
projection-blind baseline is reported in `outputs/metrics.json`; it is a control
for instrument sensitivity, not the candidate decision.

## 10. Bought-by-simplification check

The candidate boundary is not allowed to use collapse labels or future outcome
labels as learner-visible inputs. It evaluates the lawful transition rule over
the pre-registered horizon. The projection-blind baseline shows what happens
when spread and mass coordinates are omitted. The trivially-safe baseline shows
that safety alone can be bought by admitting no states, so equal-volume and FPR
are mandatory.

## 11. What was NOT shown

- No claim that this is a substrate.
- No claim that learner world-model content is derived.
- No claim that LLM training is safe.
- No claim that boundary fidelity transfers to other domains.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.
- No claim that a toy domain itself is valuable outside this gate.

## 12. Durable result

The durable result is the boundary decision above. If it passes, the next allowed
step is only a separately pre-registered learner-training gate under equal-volume
controls. If it fails, downstream work halts and witness analysis determines
whether to repair projection/layers, reject the candidate, or redesign ground
truth.
"""
    (OUTPUTS / "final_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUTPUTS.mkdir(exist_ok=True)
    prereg = load_preregistration()
    horizon = int(prereg["horizon"])
    thresholds = prereg["thresholds"]
    min_equal_volume = int(prereg["minimum_equal_volume_transitions"])

    states = list(all_states())
    if not states or horizon <= 0:
        decision = {
            "decision": "INCONCLUSIVE-MISSING-GROUND-TRUTH",
            "reason": "Evaluation set or horizon is unavailable / degenerate.",
            "thresholds_used": thresholds,
            "downstream_allowed": False,
        }
        metrics = {}
        candidate_false_safe_witnesses: list[dict[str, object]] = []
        candidate_false_positive_witnesses: list[dict[str, object]] = []
    else:
        candidate_raw, candidate_false_safe_witnesses, candidate_false_positive_witnesses = evaluate_boundary(
            states, candidate_boundary, horizon, collect_witnesses=True
        )
        blind_raw, blind_false_safe_witnesses, blind_false_positive_witnesses = evaluate_boundary(
            states, projection_blind_boundary, horizon, collect_witnesses=True
        )
        trivial_raw, _, _ = evaluate_boundary(states, trivially_safe_boundary, horizon)

        unfiltered_available = len(states) * len(ACTIONS)
        candidate_equal_volume = (
            int(candidate_raw["admitted_transition_count"]) >= min_equal_volume
            and unfiltered_available >= int(candidate_raw["admitted_transition_count"])
        )
        trivial_equal_volume = (
            int(trivial_raw["admitted_transition_count"]) >= min_equal_volume
            and unfiltered_available >= int(trivial_raw["admitted_transition_count"])
        )

        candidate_metrics = {
            "false_safe_rate": candidate_raw["false_safe_rate"],
            "already_collapsed_labeled_safe_rate": candidate_raw[
                "already_collapsed_labeled_safe_rate"
            ],
            "false_positive_rate": candidate_raw["false_positive_rate"],
            "equal_volume_possible": candidate_equal_volume,
            "safe_labeled_count": candidate_raw["safe_labeled_count"],
            "doomed_labeled_count": candidate_raw["doomed_labeled_count"],
            "admitted_transition_count": candidate_raw["admitted_transition_count"],
        }

        metrics = {
            "domain": {
                "state_count": len(states),
                "action_count": len(ACTIONS),
                "horizon": horizon,
                "minimum_equal_volume_transitions": min_equal_volume,
            },
            "candidate_boundary": candidate_metrics,
            "projection_blind_baseline": {
                "false_safe_rate": blind_raw["false_safe_rate"],
                "already_collapsed_labeled_safe_rate": blind_raw[
                    "already_collapsed_labeled_safe_rate"
                ],
                "false_positive_rate": blind_raw["false_positive_rate"],
                "safe_labeled_count": blind_raw["safe_labeled_count"],
                "doomed_labeled_count": blind_raw["doomed_labeled_count"],
                "false_safe_witness_examples": blind_false_safe_witnesses[:5],
                "false_positive_witness_examples": blind_false_positive_witnesses[:5],
            },
            "trivially_safe_baseline": {
                "false_safe_rate": trivial_raw["false_safe_rate"],
                "already_collapsed_labeled_safe_rate": trivial_raw[
                    "already_collapsed_labeled_safe_rate"
                ],
                "false_positive_rate": trivial_raw["false_positive_rate"],
                "equal_volume_possible": trivial_equal_volume,
                "safe_labeled_count": trivial_raw["safe_labeled_count"],
                "doomed_labeled_count": trivial_raw["doomed_labeled_count"],
                "admitted_transition_count": trivial_raw["admitted_transition_count"],
            },
            "unfiltered_control": {
                "collapse_rate_within_horizon": sum(
                    1 for state in states if rollout_outcome(state, horizon)[0]
                )
                / len(states),
                "available_transition_count": unfiltered_available,
            },
        }

        decision_name, reason, downstream_allowed = decide(candidate_metrics, thresholds)
        decision = {
            "decision": decision_name,
            "reason": reason,
            "thresholds_used": thresholds,
            "downstream_allowed": downstream_allowed,
        }

    (OUTPUTS / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (OUTPUTS / "decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")
    (OUTPUTS / "false_safe_witnesses.json").write_text(
        json.dumps(candidate_false_safe_witnesses, indent=2), encoding="utf-8"
    )
    (OUTPUTS / "false_positive_witnesses.json").write_text(
        json.dumps(candidate_false_positive_witnesses, indent=2), encoding="utf-8"
    )
    write_layer_audit()
    write_final_report(
        prereg,
        metrics,
        decision,
        candidate_false_safe_witnesses,
        candidate_false_positive_witnesses,
    )


if __name__ == "__main__":
    main()

