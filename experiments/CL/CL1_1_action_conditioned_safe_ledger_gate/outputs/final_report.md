# CL1.1 — Action-Conditioned Safe Ledger Gate

## 0. Verdict

`ACTION-LEDGER-OK`

Candidate action ledger satisfies unsafe-admission, source purity, successor purity, non-vacuity, and equal-volume thresholds.

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
| `experiments/CL/CL1_boundary_fidelity_pilot/SPEC.md` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/CL1_preregistration.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/domain.py` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/boundary.py` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/run_cl1.py` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/layer_audit.md` | PRESENT |
| `playbook_extraction/CL0_closed_ledger_candidate_proposal.md` | PRESENT |
| `playbook_extraction/CL0_preregistration.json` | PRESENT |
| `playbook_extraction/02_extracted_method.md` | PRESENT |
| `playbook_extraction/03_not_yet_method.md` | PRESENT |
| `playbook_extraction/harness/output_schema.md` | PRESENT |
| `playbook_extraction/harness/failure_conditions.md` | PRESENT |

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

Domain: `FourZoneMassDomain`.

State/action space: Exhaustive finite pair set: 17500 CL1 states times 5 actions = 87500 (state, action) pairs.

Transition semantics: The CL1 deterministic transition is reused unchanged. AID_i increases zone i and costs mass; CONSERVE restores mass; the phase-indexed exogenous shock damages one zone; failed zones drain mass; phase advances modulo 4.

Collapse predicate: Collapse if at least two zones have health <= 0 (spread mechanism) or if mass <= 0 (mass mechanism). The predicate is audit-only.

Learner-visible transition: observe(state), action, observe(successor). Observations contain zones, mass, and phase only. No collapse labels, future outcomes, mechanisms, witness classes, or reporting-only metrics are learner-visible.

## 5. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json`

This file was written before final CL1.1 metric computation. The runner loads
the thresholds from that file and does not move thresholds after seeing
results.

Thresholds used:

```json
{
  "unsafe_admitted_transition_rate_max": 0.05,
  "already_collapsed_source_admitted_rate_max": 0.0,
  "already_collapsed_successor_admitted_rate_max": 0.0,
  "false_positive_action_rate_max": 0.2,
  "equal_volume_required": true
}
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
{
  "domain": {
    "state_count": 17500,
    "action_count": 5,
    "state_action_count": 87500,
    "horizon": 6,
    "minimum_equal_volume_transitions": 500
  },
  "candidate_action_ledger": {
    "admitted_transition_count": 31142,
    "rejected_transition_count": 56358,
    "unsafe_admitted_transition_count": 0,
    "already_collapsed_source_admitted_count": 0,
    "already_collapsed_successor_admitted_count": 0,
    "safe_action_transition_count": 31142,
    "false_positive_action_count": 0,
    "unsafe_admitted_transition_rate": 0.0,
    "already_collapsed_source_admitted_rate": 0.0,
    "already_collapsed_successor_admitted_rate": 0.0,
    "false_positive_action_rate": 0.0,
    "equal_volume_possible": true
  },
  "cl1_state_level_carryover_baseline": {
    "admitted_transition_count": 39175,
    "unsafe_admitted_transition_rate": 0.2339757498404595,
    "already_collapsed_source_admitted_rate": 0.0,
    "already_collapsed_successor_admitted_rate": 0.12477345245692406,
    "false_positive_action_rate": 0.036381735277117716,
    "unsafe_admitted_witness_examples": [
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
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 5,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 5,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_6",
        "collapse_mechanism": "mass",
        "collapse_step_after_action": 6,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            1
          ],
          "mass": 4,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 3
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              1
            ],
            "mass": 4,
            "phase": 0
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_5",
        "collapse_mechanism": "mass",
        "collapse_step_after_action": 5,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            3,
            1
          ],
          "mass": 4,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 3
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              3,
              1
            ],
            "mass": 4,
            "phase": 0
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_3",
        "collapse_mechanism": "mass",
        "collapse_step_after_action": 3,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 3
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 0
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_3",
        "collapse_mechanism": "mass",
        "collapse_step_after_action": 3,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            2,
            1
          ],
          "mass": 5,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 3
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              1
            ],
            "mass": 5,
            "phase": 0
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_5",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 5,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            1,
            3
          ],
          "mass": 3,
          "phase": 3
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 5,
            "phase": 2
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              1,
              3
            ],
            "mass": 3,
            "phase": 3
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_5",
        "collapse_mechanism": "mass",
        "collapse_step_after_action": 5,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            1,
            4
          ],
          "mass": 3,
          "phase": 3
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 5,
            "phase": 2
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              1,
              4
            ],
            "mass": 3,
            "phase": 3
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_5",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 5,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            1,
            3
          ],
          "mass": 5,
          "phase": 3
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 5,
            "phase": 2
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              1,
              3
            ],
            "mass": 5,
            "phase": 3
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_5",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 5,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            3,
            2
          ],
          "mass": 3,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 5,
            "phase": 3
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              3,
              2
            ],
            "mass": 3,
            "phase": 0
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_3",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 3,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
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
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 3,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 5,
            "phase": 3
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 3,
            "phase": 0
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "collapse_within_horizon_step_3",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 3,
        "which_coordinate_policy_or_action_mattered": "CL1 state-level boundary admitted all actions from a SAFE source state"
      }
    ],
    "false_positive_action_witness_examples": [
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            2
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            3
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              3
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            4
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            4
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              4
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              4
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            1
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              1
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 0
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 5,
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            2
          ],
          "mass": 3,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 5,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              2
            ],
            "mass": 3,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 3,
          "phase": 3
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            2
          ],
          "mass": 1,
          "phase": 0
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 3,
            "phase": 3
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              2
            ],
            "mass": 1,
            "phase": 0
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 0
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            3
          ],
          "mass": 3,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 5,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              3
            ],
            "mass": 3,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 2
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            1,
            3
          ],
          "mass": 4,
          "phase": 3
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 6,
            "phase": 2
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              1,
              3
            ],
            "mass": 4,
            "phase": 3
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      }
    ]
  },
  "projection_blind_action_baseline": {
    "admitted_transition_count": 60900,
    "unsafe_admitted_transition_rate": 0.5008702791461412,
    "already_collapsed_source_admitted_rate": 0.17832512315270935,
    "already_collapsed_successor_admitted_rate": 0.3344499178981938,
    "false_positive_action_rate": 0.0239226767709203,
    "unsafe_admitted_witness_examples": [
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
        "action": "AID_0",
        "successor": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_0",
          "successor_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            1,
            3,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              1,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            0,
            4,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              0,
              4,
              4
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
          "phase": 0
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
        "action": "AID_0",
        "successor": {
          "zones": [
            1,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_0",
          "successor_observation": {
            "zones": [
              1,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            0,
            4,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              0,
              4,
              4
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
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
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            0,
            3,
            4
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              0,
              3,
              4
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "projection-blind action baseline omitted failed-zone spread, mass, or phase"
      }
    ],
    "false_positive_action_witness_examples": [
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            2
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            3
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              3
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            4
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            4
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              4
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              4
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            1
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              1
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 0
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 5,
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            2
          ],
          "mass": 3,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 5,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              2
            ],
            "mass": 3,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_0",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_0",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            3,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              3,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      }
    ]
  },
  "trivially_safe_action_baseline": {
    "admitted_transition_count": 0,
    "unsafe_admitted_transition_rate": 0.0,
    "already_collapsed_source_admitted_rate": 0.0,
    "already_collapsed_successor_admitted_rate": 0.0,
    "false_positive_action_rate": 1.0,
    "equal_volume_possible": false,
    "false_positive_action_witness_examples": [
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            2
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            3
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              3
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            1,
            4
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            2,
            4
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              1,
              4
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              4
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            1
          ],
          "mass": 6,
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              1
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 0
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      },
      {
        "state": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 5,
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            2
          ],
          "mass": 3,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 5,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              2
            ],
            "mass": 3,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_0",
        "successor": {
          "zones": [
            0,
            1,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_0",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            2,
            2,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              2,
              2,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            1,
            3,
            2
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              1,
              3,
              2
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
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
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            1,
            2,
            3
          ],
          "mass": 4,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              1,
              2,
              2
            ],
            "mass": 6,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              1,
              2,
              3
            ],
            "mass": 4,
            "phase": 1
          }
        },
        "admission_decision": "REJECT",
        "full_outcome": "remains_safe_within_horizon",
        "collapse_mechanism": "none",
        "why_rejected": "admission rule rejected a transition that remains safe under the audited continuation"
      }
    ]
  },
  "unfiltered_action_control": {
    "unsafe_transition_rate": 0.6440914285714285,
    "unsafe_transition_count": 56358,
    "available_transition_count": 87500
  },
  "diagnostic": {
    "cl1_mismatch_reproduced": true,
    "candidate_scope": "one-step action admission followed by CL1 safety-policy continuation",
    "all_future_action_branches_tested": false,
    "unfiltered_unsafe_witness_examples": [
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 0
        },
        "action": "AID_0",
        "successor": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_0",
          "successor_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 0
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            1,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              1,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 0
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            0,
            1,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              0,
              1,
              0
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 0
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            0,
            0,
            1
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              0,
              0,
              1
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 0
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 0
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "action": "AID_0",
        "successor": {
          "zones": [
            1,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_0",
          "successor_observation": {
            "zones": [
              1,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "action": "AID_1",
        "successor": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_1",
          "successor_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "action": "AID_2",
        "successor": {
          "zones": [
            0,
            0,
            1,
            0
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_2",
          "successor_observation": {
            "zones": [
              0,
              0,
              1,
              0
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "action": "AID_3",
        "successor": {
          "zones": [
            0,
            0,
            0,
            1
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "AID_3",
          "successor_observation": {
            "zones": [
              0,
              0,
              0,
              1
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      },
      {
        "state": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 1
        },
        "action": "CONSERVE",
        "successor": {
          "zones": [
            0,
            0,
            0,
            0
          ],
          "mass": 0,
          "phase": 2
        },
        "learner_visible_transition": {
          "source_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 1
          },
          "action": "CONSERVE",
          "successor_observation": {
            "zones": [
              0,
              0,
              0,
              0
            ],
            "mass": 0,
            "phase": 2
          }
        },
        "admission_decision": "ADMIT",
        "full_outcome": "source_already_collapsed_step_0",
        "collapse_mechanism": "both",
        "collapse_step_after_action": 0,
        "which_coordinate_policy_or_action_mattered": "unfiltered control admits all actions"
      }
    ]
  }
}
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

Decision: `ACTION-LEDGER-OK`

Downstream allowed: `True`

The decision rule is the pre-registered CL1.1 rule:
`ACTION-LEDGER-OK` requires unsafe admission, source purity, successor purity,
false-positive, and equal-volume gates all to pass.

## 10. Witness analysis

Candidate unsafe admitted witnesses recorded:
`0`.

Candidate false-positive action witnesses recorded:
`0`.

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
