# CL2 — Equal-Volume Learner Probe on Oracle-Filtered Action Ledger

## 0. Verdict

`LEARNER-LEAKAGE-FAIL`

Leakage was detected or shuffled-target control scored above the pre-registered maximum.

## 1. Goal anchor

CL2 serves the safe / derivable substrate goal only as a learner-probe
precondition. It asks whether the CL1.1 safe action ledger still contains
learnable transition structure under equal-volume controls. It does not claim
that world-model content is derived.

## 2. Inputs used

| file | status |
|---|---|
| `experiments/CL/CL1_boundary_fidelity_pilot/domain.py` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/boundary.py` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/SPEC.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/run_cl1_1.py` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/layer_audit_delta.md` | PRESENT |
| `playbook_extraction/CL0_closed_ledger_candidate_proposal.md` | PRESENT |
| `playbook_extraction/CL0_preregistration.json` | PRESENT |
| `playbook_extraction/02_extracted_method.md` | PRESENT |
| `playbook_extraction/03_not_yet_method.md` | PRESENT |
| `playbook_extraction/harness/output_schema.md` | PRESENT |
| `playbook_extraction/harness/failure_conditions.md` | PRESENT |

## 3. CL1.1 scope carried forward

Ledger scope: one-step admitted action plus CL1 safety-policy continuation; not arbitrary future learner actions.

The CL1.1 decision was required to be `ACTION-LEDGER-OK` before CL2 could run.
CL2 keeps the one-step action admission plus safety-policy continuation scope
and does not test arbitrary future learner actions.

## 4. Dataset construction

Candidate dataset: all CL1.1 ADMIT_CANDIDATE transitions.

Equal-volume control: sample equal number of transitions from unfiltered state-action space with same seed.

Dataset manifest:

```json
{
  "candidate_transition_count": 31142,
  "unfiltered_equal_volume_transition_count": 31142,
  "candidate_features": [
    "source_zones",
    "source_mass",
    "source_phase",
    "action"
  ],
  "candidate_targets": [
    "successor_zones",
    "successor_mass",
    "successor_phase"
  ],
  "forbidden_fields_present": false,
  "random_seed": 20260630,
  "ledger_scope": "one-step action admission plus safety-policy continuation"
}
```

## 5. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json`

This file was written before final dataset split, learner training, and metric
computation. Structural holdout was pre-registered as
`source_phase == 3`.

## 6. Learners and baselines

Primary learner: Fixed non-oracle rule-family transition learner in learners.py; it fits visible transition parameters from rows before metrics and does not call forbidden oracle functions at prediction time.

Baselines: copy-source, memorizer, majority-delta, shuffled-target control, and
equal-volume unfiltered-control learner.

The primary learner is hand-designed around visible domain variables and fits a
small parameterized rule family from training rows. This is a toy learner probe,
not a derivability claim.

## 7. Splits

```json
{
  "random_split": {
    "train_count": 21799,
    "validation_count": 4671,
    "test_count": 4672
  },
  "source_state_holdout": {
    "train_count": 26468,
    "test_count": 4674,
    "heldout_source_state_count": 1307
  },
  "structural_holdout": {
    "rule": "source_phase == 3",
    "train_count": 23336,
    "test_count": 7806
  }
}
```

## 8. Metrics

```json
{
  "primary_learner": {
    "random_split_exact_accuracy": 1.0,
    "random_split_coordinate_accuracy": 1.0,
    "source_state_holdout_exact_accuracy": 1.0,
    "source_state_holdout_coordinate_accuracy": 1.0,
    "structural_holdout_exact_accuracy": 1.0,
    "structural_holdout_coordinate_accuracy": 1.0
  },
  "copy_source_baseline": {
    "random_split_exact_accuracy": 0.0,
    "random_split_coordinate_accuracy": 0.4792736872146119,
    "source_state_holdout_exact_accuracy": 0.0,
    "source_state_holdout_coordinate_accuracy": 0.48006703751248037,
    "structural_holdout_exact_accuracy": 0.0,
    "structural_holdout_coordinate_accuracy": 0.4799513194978222
  },
  "memorizer_baseline": {
    "random_split_exact_accuracy": 0.1292808219178082,
    "random_split_coordinate_accuracy": 0.60238299086758,
    "source_state_holdout_exact_accuracy": 0.12216516902011125,
    "source_state_holdout_coordinate_accuracy": 0.6384253316217373,
    "structural_holdout_exact_accuracy": 0.0,
    "structural_holdout_coordinate_accuracy": 0.44926979246733284
  },
  "majority_delta_baseline": {
    "random_split_exact_accuracy": 0.1292808219178082,
    "random_split_coordinate_accuracy": 0.60238299086758,
    "source_state_holdout_exact_accuracy": 0.12216516902011125,
    "source_state_holdout_coordinate_accuracy": 0.6384253316217373,
    "structural_holdout_exact_accuracy": 0.0,
    "structural_holdout_coordinate_accuracy": 0.44926979246733284
  },
  "shuffled_target_control": {
    "random_split_exact_accuracy": 0.0,
    "random_split_coordinate_accuracy": 0.6386629566210046,
    "source_state_holdout_exact_accuracy": 0.6463414634146342,
    "source_state_holdout_coordinate_accuracy": 0.9410569105691057,
    "structural_holdout_exact_accuracy": 0.0,
    "structural_holdout_coordinate_accuracy": 0.6778332906311384
  },
  "equal_volume_unfiltered_control_learner": {
    "random_split_exact_accuracy": 1.0,
    "random_split_coordinate_accuracy": 1.0,
    "source_state_holdout_exact_accuracy": 1.0,
    "source_state_holdout_coordinate_accuracy": 1.0,
    "structural_holdout_exact_accuracy": 1.0,
    "structural_holdout_coordinate_accuracy": 1.0
  },
  "memorization_gap": 1.0,
  "copy_gap": 1.0,
  "control_gap": 0.0,
  "shuffled_target_accuracy": 0.6463414634146342
}
```

## 9. Leakage audit

Forbidden learner fields present: `False`.

Learner-code scan:

```json
{
  "imports_forbidden_oracle_functions": [],
  "calls_forbidden_oracle_functions": [],
  "regex_call_hits": [],
  "leakage_detected": false
}
```

Shuffled-target accuracy: `0.6463414634146342`.

## 10. Memorization audit

```json
{
  "exact_training_pair_overlap_random_test": 0.0,
  "exact_training_pair_overlap_source_state_holdout": 0.0,
  "exact_training_pair_overlap_structural_holdout": 0.0,
  "memorizer_structural_holdout_accuracy": 0.0,
  "primary_structural_holdout_accuracy": 1.0,
  "memorization_gap": 1.0,
  "memorization_trap_detected": false
}
```

## 11. Equal-volume control comparison

Control gap:

```text
primary random-test exact accuracy - equal-volume unfiltered-control learner random-test exact accuracy
= 0.0
```

The control learner is trained on the same number of unfiltered transitions and
evaluated on the same candidate safe test sets.

## 12. Decision

Decision: `LEARNER-LEAKAGE-FAIL`

Downstream allowed: `False`

Thresholds used:

```json
{
  "random_split_accuracy_min": 0.95,
  "source_state_holdout_accuracy_min": 0.8,
  "structural_holdout_accuracy_min": 0.75,
  "memorization_gap_min": 0.2,
  "copy_gap_min": 0.3,
  "control_gap_min": -0.1,
  "shuffled_target_accuracy_max": 0.25,
  "leakage_allowed": false
}
```

## 13. Prediction error witnesses

Primary structural-holdout error witnesses recorded: `0`.

If the file is empty, the primary learner made no exact successor errors on the
structural holdout under this probe.

## 14. Bought-by-simplification check

The learner is small and hand-designed around visible variables from a toy
domain. This is a simplification. The safeguards are source-state holdout,
structural holdout, memorizer baseline, copy-source baseline, shuffled-target
control, and equal-volume unfiltered control.

The result is therefore only evidence about transition learnability inside this
oracle-filtered ledger.

## 15. What was NOT shown

- No claim that this is a substrate.
- No claim that world-model content is derived.
- No claim that LLM training is safe.
- No claim that the learner learned beyond `FourZoneMassDomain`.
- No claim that the learner is safe under autonomous policy rollout.
- No claim that the learner is safe under arbitrary future actions.
- No claim that the action ledger transfers to other domains.
- No claim that the boundary is learned.
- No claim that the oracle-filtered ledger is available in real domains.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.

## 16. Durable result

CL2 produced an equal-volume learner-probe decision over the CL1.1
oracle-filtered action ledger. The durable outputs are the dataset manifest,
split manifest, metrics, leakage audit, memorization audit, prediction witnesses,
and decision file in `outputs/`.
