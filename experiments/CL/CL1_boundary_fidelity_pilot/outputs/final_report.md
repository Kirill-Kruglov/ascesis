# CL1 — Minimal Lawful Domain Boundary-Fidelity Pilot

## 0. Verdict

`BOUNDARY-FIDELITY-OK`

Candidate boundary satisfies false-safe, purity, non-vacuity, and equal-volume thresholds on the exhaustive state set.

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

Domain: `FourZoneMassDomain`.

State space: Exhaustive finite state set: four zone-health coordinates in {0,1,2,3,4}, global mass in {0,1,2,3,4,5,6}, and phase in {0,1,2,3}. Total states: 5^4 * 7 * 4 = 17500.

Transition semantics: state_t+1 = transition(state_t, action_t, exogenous_t). Exogenous_t is phase-indexed zone shock. AID_i increases zone i and costs mass; CONSERVE restores mass; shock damages the phase zone; failed zones drain mass; phase advances modulo 4.

Collapse predicate: Collapse if at least two zones have health <= 0 (spread mechanism) or if mass <= 0 (mass mechanism). The predicate is audit-only.

Learner-visible observation: zones, mass, phase. No collapse labels, future outcomes, collapse mechanism labels, or reporting-only metrics are learner-visible.

Horizon: `6`.

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
{
  "false_safe_rate_max": 0.05,
  "already_collapsed_labeled_safe_rate_max": 0.0,
  "false_positive_rate_max": 0.2,
  "equal_volume_required": true
}
```

## 6. Metrics

```json
{
  "domain": {
    "state_count": 17500,
    "action_count": 5,
    "horizon": 6,
    "minimum_equal_volume_transitions": 500
  },
  "candidate_boundary": {
    "false_safe_rate": 0.0,
    "already_collapsed_labeled_safe_rate": 0.0,
    "false_positive_rate": 0.0,
    "equal_volume_possible": true,
    "safe_labeled_count": 7835,
    "doomed_labeled_count": 9665,
    "admitted_transition_count": 39175
  },
  "projection_blind_baseline": {
    "false_safe_rate": 0.37257799671592773,
    "already_collapsed_labeled_safe_rate": 0.4167306216423638,
    "false_positive_rate": 0.024633056796426293,
    "safe_labeled_count": 12180,
    "doomed_labeled_count": 5320,
    "false_safe_witness_examples": [
      {
        "state": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 0
        },
        "observation": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 0
        },
        "boundary_decision": "SAFE",
        "full_outcome": "collapse_within_horizon_step_0",
        "collapse_mechanism": "both",
        "which_coordinate_or_projection_mattered": "projection omitted failed_zone_count and mass"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "observation": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "boundary_decision": "SAFE",
        "full_outcome": "collapse_within_horizon_step_0",
        "collapse_mechanism": "both",
        "which_coordinate_or_projection_mattered": "projection omitted failed_zone_count and mass"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "observation": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "boundary_decision": "SAFE",
        "full_outcome": "collapse_within_horizon_step_0",
        "collapse_mechanism": "both",
        "which_coordinate_or_projection_mattered": "projection omitted failed_zone_count and mass"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 3
        },
        "observation": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 3
        },
        "boundary_decision": "SAFE",
        "full_outcome": "collapse_within_horizon_step_0",
        "collapse_mechanism": "both",
        "which_coordinate_or_projection_mattered": "projection omitted failed_zone_count and mass"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 1,
          "phase": 0
        },
        "observation": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 1,
          "phase": 0
        },
        "boundary_decision": "SAFE",
        "full_outcome": "collapse_within_horizon_step_0",
        "collapse_mechanism": "spread",
        "which_coordinate_or_projection_mattered": "projection omitted failed_zone_count and mass"
      }
    ],
    "false_positive_witness_examples": [
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 6,
          "phase": 0
        },
        "observation": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 6,
          "phase": 0
        },
        "boundary_decision": "DOOMED",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "which_coordinate_or_projection_mattered": "boundary was conservative for this state"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 6,
          "phase": 3
        },
        "observation": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 6,
          "phase": 3
        },
        "boundary_decision": "DOOMED",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "which_coordinate_or_projection_mattered": "boundary was conservative for this state"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 5,
          "phase": 2
        },
        "observation": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 5,
          "phase": 2
        },
        "boundary_decision": "DOOMED",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "which_coordinate_or_projection_mattered": "boundary was conservative for this state"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 5,
          "phase": 3
        },
        "observation": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 5,
          "phase": 3
        },
        "boundary_decision": "DOOMED",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "which_coordinate_or_projection_mattered": "boundary was conservative for this state"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 6,
          "phase": 0
        },
        "observation": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 6,
          "phase": 0
        },
        "boundary_decision": "DOOMED",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "which_coordinate_or_projection_mattered": "boundary was conservative for this state"
      }
    ]
  },
  "trivially_safe_baseline": {
    "false_safe_rate": 0.0,
    "already_collapsed_labeled_safe_rate": 0.0,
    "false_positive_rate": 1.0,
    "equal_volume_possible": false,
    "safe_labeled_count": 0,
    "doomed_labeled_count": 17500,
    "admitted_transition_count": 0
  },
  "unfiltered_control": {
    "collapse_rate_within_horizon": 0.5522857142857143,
    "available_transition_count": 87500
  }
}
```

## 7. Controls and baselines

- Candidate boundary: bounded rollout under the safety policy using
  layer-eligible coordinates.
- Projection-blind baseline: uses mean zone health only; omits spread, mass,
  and phase. It is expected to expose 18.1-style projection blindness.
- Trivially-safe baseline: labels all states DOOMED; detects vacuity.
- Unfiltered control: no boundary filtering; used for equal-volume comparison.

## 8. Decision

Decision: `BOUNDARY-FIDELITY-OK`.

Downstream allowed: `True`.

The decision follows the exact CL1 rule over false-safe, already-collapsed
purity, false-positive/non-vacuity, and equal-volume conditions.

## 9. Witness analysis

Candidate false-safe witnesses: `0`.

Candidate false-positive witnesses recorded: `0`.

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
