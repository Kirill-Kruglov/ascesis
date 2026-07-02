# CL2.1 — Shuffled-Control Repair / Artifact Isolation Gate

## 0. Verdict

`SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT`

Original shuffled control failure is best explained as an invalid anti-artifact control for the primary rule-family learner, not as proven CL2 success.

## 1. Goal anchor

CL2.1 serves the safe / derivable substrate goal only by repairing the
anti-artifact instrument required before a CL2 learner-probe claim can be
trusted. It does not claim CL2 passed.

## 2. Inputs used

| file | status |
|---|---|
| `experiments/CL/CL2_equal_volume_learner_probe/SPEC.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/dataset_builder.py` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/learners.py` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/run_cl2.py` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/dataset_manifest.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/split_manifest.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/decision.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/domain.py` | PRESENT |
| `playbook_extraction/02_extracted_method.md` | PRESENT |
| `playbook_extraction/03_not_yet_method.md` | PRESENT |
| `playbook_extraction/harness/output_schema.md` | PRESENT |
| `playbook_extraction/harness/failure_conditions.md` | PRESENT |

## 3. CL2 failure being repaired

CL2 halted with `LEARNER-LEAKAGE-FAIL` because the shuffled-target control
exceeded its threshold. CL2.1 diagnoses whether that was leakage, an evaluation
bug, a marginal artifact, or an invalid control for the primary learner's
inductive bias.

## 4. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL2_1_shuffled_control_repair/CL2_1_preregistration.json`

This file was written before diagnostic metrics were computed. Thresholds were
loaded from the preregistration and not changed after seeing diagnostics.

## 5. Evaluation integrity audit

```json
{
  "target_fields_in_features": false,
  "test_target_used_in_fit": false,
  "prediction_compared_to_original_true_target": true,
  "shuffled_control_test_targets_remain_original": true,
  "forbidden_fields_present": false,
  "forbidden_oracle_calls": [],
  "evaluation_mismatch_detected": false
}
```

## 6. Shuffle diagnostics

```json
{
  "original_global_shuffle": {
    "random_exact": 0.0,
    "random_coordinate": 0.6386629566210046,
    "source_holdout_exact": 0.6463414634146342,
    "source_holdout_coordinate": 0.9410569105691057,
    "structural_holdout_exact": 0.0,
    "structural_holdout_coordinate": 0.6778332906311384,
    "max_exact": 0.6463414634146342
  },
  "within_action_shuffle": {
    "random_exact": 1.0,
    "random_coordinate": 1.0,
    "source_holdout_exact": 1.0,
    "source_holdout_coordinate": 1.0,
    "structural_holdout_exact": 1.0,
    "structural_holdout_coordinate": 1.0,
    "max_exact": 1.0
  },
  "within_phase_shuffle": {
    "random_exact": 0.816138698630137,
    "random_coordinate": 0.9693564497716894,
    "source_holdout_exact": 0.23876765083440307,
    "source_holdout_coordinate": 0.8573669947225788,
    "structural_holdout_exact": 1.0,
    "structural_holdout_coordinate": 1.0,
    "max_exact": 1.0
  },
  "cross_action_shuffle": {
    "random_exact": 0.0,
    "random_coordinate": 0.5212970890410958,
    "source_holdout_exact": 0.0,
    "source_holdout_coordinate": 0.679147054628441,
    "structural_holdout_exact": 1.0,
    "structural_holdout_coordinate": 1.0,
    "max_exact": 1.0
  },
  "cross_phase_shuffle": {
    "random_exact": 0.0,
    "random_coordinate": 0.6189711757990868,
    "source_holdout_exact": 0.0,
    "source_holdout_coordinate": 0.685672514619883,
    "structural_holdout_exact": 0.0,
    "structural_holdout_coordinate": 0.6395294218122811,
    "max_exact": 0.0
  }
}
```

## 7. Impossible-target and feature-permutation diagnostics

```json
{
  "independent_impossible_target": {
    "random_exact": 0.0,
    "random_coordinate": 0.8026897831050228,
    "source_holdout_exact": 0.0,
    "source_holdout_coordinate": 0.5359435173299102,
    "structural_holdout_exact": 0.0,
    "structural_holdout_coordinate": 0.6395294218122811,
    "max_exact": 0.0
  },
  "feature_permutation_control": {
    "random_exact": 0.0,
    "random_coordinate": 0.6386629566210046,
    "source_holdout_exact": 0.42854086435601196,
    "source_holdout_coordinate": 0.888995863642847,
    "structural_holdout_exact": 0.0988982833717653,
    "structural_holdout_coordinate": 0.8498163805619608,
    "max_exact": 0.42854086435601196
  }
}
```

## 8. Learner bias ablation

```json
{
  "primary_rule_family_learner": {
    "original_global_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.6463414634146342,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.6463414634146342
    },
    "within_action_shuffle": {
      "random_exact": 1.0,
      "source_holdout_exact": 1.0,
      "structural_holdout_exact": 1.0,
      "max_exact": 1.0
    },
    "within_phase_shuffle": {
      "random_exact": 0.816138698630137,
      "source_holdout_exact": 0.23876765083440307,
      "structural_holdout_exact": 1.0,
      "max_exact": 1.0
    },
    "cross_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 1.0,
      "max_exact": 1.0
    },
    "cross_phase_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "independent_impossible_target": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "feature_permutation_control": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.42854086435601196,
      "structural_holdout_exact": 0.0988982833717653,
      "max_exact": 0.42854086435601196
    }
  },
  "majority_delta_baseline": {
    "original_global_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "within_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "within_phase_shuffle": {
      "random_exact": 0.007491438356164383,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.007491438356164383
    },
    "cross_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "cross_phase_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "independent_impossible_target": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "feature_permutation_control": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    }
  },
  "memorizer_baseline": {
    "original_global_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "within_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "within_phase_shuffle": {
      "random_exact": 0.007491438356164383,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.007491438356164383
    },
    "cross_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "cross_phase_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "independent_impossible_target": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "feature_permutation_control": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    }
  },
  "copy_source_baseline": {
    "original_global_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "within_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "within_phase_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "cross_action_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "cross_phase_shuffle": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "independent_impossible_target": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    },
    "feature_permutation_control": {
      "random_exact": 0.0,
      "source_holdout_exact": 0.0,
      "structural_holdout_exact": 0.0,
      "max_exact": 0.0
    }
  },
  "high_score_concentrated_in_primary": true,
  "primary_high_controls": [
    "cross_action_shuffle",
    "feature_permutation_control",
    "original_global_shuffle",
    "within_action_shuffle",
    "within_phase_shuffle"
  ],
  "baseline_high_controls": [],
  "bias_artifact_supported": true,
  "notes": "High shuffled scores are interpreted only as diagnostic evidence, not as CL2 success."
}
```

## 9. Competing explanations

H1 real leakage: evaluated by forbidden fields/calls and independent impossible
target control.

H2 evaluation bug: evaluated by target-feature separation, fit/test separation,
and original-true-target comparison.

H3 marginal artifact: evaluated by within/cross action and phase shuffles.

H4 strong inductive bias: evaluated by comparing the primary rule-family learner
against majority-delta, memorizer, and copy-source baselines.

## 10. Decision

Decision: `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT`

CL2 rerun allowed: `False`

Downstream representation allowed: `False`

## 11. Replacement control recommendation

`NO_RERUN_ALLOWED`

If a rerun is allowed, it is only a repaired CL2 rerun with the replacement
controls and thresholds stated in `outputs/control_recommendation.md`.

## 12. Bought-by-simplification check

The diagnostics still use the same toy finite ledger and hand-designed learner
family. Repairing a control does not establish learner success. The only
allowed inference is whether CL2's anti-artifact instrument can be made more
trustworthy.

## 13. What was NOT shown

- No claim that CL2 passed.
- No claim that learner transition learning is admissible evidence yet.
- No claim that this is a substrate.
- No claim that world-model content is derived.
- No claim that LLM training is safe.
- No claim that action-ledger safety transfers to other domains.
- No claim that the boundary is learned.
- No claim that the oracle-filtered ledger is available in real domains.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.
- No claim that repairing a control proves the learner result.

## 14. Durable result

CL2.1 produced an instrument verdict plus detailed diagnostics for shuffled
controls, impossible targets, feature permutation, learner bias, and evaluation
integrity. The durable result is the decision in `outputs/decision.json`.
