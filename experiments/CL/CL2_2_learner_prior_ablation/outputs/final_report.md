# CL2.2 — Learner-Prior Ablation / Data-Dependence Gate

## 0. Verdict

`NO-GENERIC-LEARNER-SIGNAL`

No leakage or artifact persisted, but the evidence-eligible generic learner failed a required positive accuracy threshold.

## 1. Goal anchor

CL2.2 serves the safe / derivable substrate goal only by testing whether learner
performance depends on safe-ledger data after removing the CL2 rule-family prior.
It does not claim substrate discovery or derivability.

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
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/SPEC.md` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/CL2_1_preregistration.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/control_diagnostics.py` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/run_cl2_1.py` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/control_metrics.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/decision.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/learner_bias_audit.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/evaluation_integrity_audit.md` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/control_recommendation.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/domain.py` | PRESENT |
| `playbook_extraction/02_extracted_method.md` | PRESENT |
| `playbook_extraction/03_not_yet_method.md` | PRESENT |
| `playbook_extraction/harness/output_schema.md` | PRESENT |
| `playbook_extraction/harness/failure_conditions.md` | PRESENT |

## 3. CL2.1 durable constraint carried forward

CL2.1 found `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT`; the CL2 rule-family learner
is diagnostic-only and cannot support a positive CL2.2 verdict.

## 4. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL2_2_learner_prior_ablation/CL2_2_preregistration.json`

This file was written before CL2.2 dataset construction, training, diagnostics,
and metric computation.

## 5. Dataset and splits

Dataset manifest:

```json
{
  "candidate_transition_count": 31142,
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

Split manifest:

```json
{
  "source_state_holdout": {
    "train_count": 26468,
    "test_count": 4674,
    "exact_source_overlap": 0.0
  },
  "structural_holdout": {
    "rule": "source_phase == 3",
    "train_count": 23336,
    "test_count": 7806
  },
  "cross_phase_holdout": {
    "rule": "train on source_phase != 3; evaluate source_phase == 3",
    "train_count": 23336,
    "test_count": 7806
  }
}
```

## 6. Evidence-eligible learner

The evidence-eligible learner is `GenericSubsetBackoffLearner`. It learns
generic majority target-coordinate tables over visible feature subsets and backs
off to smaller subsets. It does not encode the exact transition family.

## 7. Prior diagnostic learner

The CL2 `RuleFamilyTransitionLearner` is run as `PRIOR-DIAGNOSTIC-ONLY`. Its
metrics cannot support `DATA-DEPENDENT-LEARNING-OK`.

## 8. Learning curve diagnostics

```json
{
  "generic_learner": {
    "zero_fit": {
      "source_holdout_exact": 0.0,
      "source_holdout_coordinate": 0.09620596205962059,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.22081304979075925,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.22081304979075925
    },
    "1_percent": {
      "source_holdout_exact": 0.0017115960633290544,
      "source_holdout_coordinate": 0.43802595920696047,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.2702835425740883,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.27256811000085407
    },
    "5_percent": {
      "source_holdout_exact": 0.004278990158322636,
      "source_holdout_coordinate": 0.4738981600342319,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.3152062516013323,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.3109787343069434
    },
    "20_percent": {
      "source_holdout_exact": 0.0068463842533162175,
      "source_holdout_coordinate": 0.5009627727856226,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.395529080194722,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.3968528482363993
    },
    "100_percent": {
      "source_holdout_exact": 0.0038510911424903724,
      "source_holdout_coordinate": 0.5343032377692198,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.5305534204458109,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.5305534204458109
    }
  },
  "prior_diagnostic_rule_family": {
    "zero_fit": {
      "source_holdout_exact": 0.02139495079161318,
      "source_holdout_coordinate": 0.6467337041791471,
      "structural_holdout_exact": 0.02024084037919549,
      "structural_holdout_coordinate": 0.6466179861644888,
      "cross_phase_exact": 0.02024084037919549,
      "cross_phase_coordinate": 0.6466179861644888
    },
    "100_percent": {
      "source_holdout_exact": 1.0,
      "source_holdout_coordinate": 1.0,
      "structural_holdout_exact": 1.0,
      "structural_holdout_coordinate": 1.0,
      "cross_phase_exact": 1.0,
      "cross_phase_coordinate": 1.0
    }
  },
  "data_gain": 0.0,
  "tiny_to_full_gain": 0.0
}
```

## 9. Corrupted-target controls

```json
{
  "generic_learner_corrupted_controls": {
    "independent_impossible_target": {
      "source_holdout_exact": 0.0002139495079161318,
      "source_holdout_coordinate": 0.20114819569248324,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.21052182082159024,
      "cross_phase_exact": 0.00012810658467845247,
      "cross_phase_coordinate": 0.19617388333760355,
      "max_exact": 0.0002139495079161318
    },
    "cross_phase_target_shuffle": {
      "source_holdout_exact": 0.0002139495079161318,
      "source_holdout_coordinate": 0.24668378262729995,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.19122042873003672,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.1843240242548467,
      "max_exact": 0.0002139495079161318
    },
    "feature_permutation_control": {
      "source_holdout_exact": 0.0002139495079161318,
      "source_holdout_coordinate": 0.22347026101839965,
      "structural_holdout_exact": 0.0,
      "structural_holdout_coordinate": 0.18541293022461355,
      "cross_phase_exact": 0.0,
      "cross_phase_coordinate": 0.18323511828507985,
      "max_exact": 0.0002139495079161318
    }
  },
  "best_corrupted_target_accuracy": 0.0002139495079161318,
  "corruption_drop": 0.0,
  "leakage_detected": false
}
```

## 10. Prior ablation comparison

```json
{
  "generic_learner_full_data": {
    "source_holdout_exact": 0.0038510911424903724,
    "structural_holdout_exact": 0.0,
    "cross_phase_exact": 0.0
  },
  "rule_family_prior_diagnostic": {
    "source_holdout_exact": 1.0,
    "structural_holdout_exact": 1.0,
    "cross_phase_exact": 1.0
  },
  "prior_advantage": {
    "source_holdout": 0.9961489088575096,
    "structural_holdout": 1.0,
    "cross_phase": 1.0
  },
  "interpretation": "Rule-family learner is diagnostic-only; positive evidence must come from the generic learner."
}
```

## 11. Leakage and evaluation audit

```json
{
  "forbidden_imports": [],
  "forbidden_calls": [],
  "encodes_exact_transition_family": false,
  "exact_family_term_hits": {
    "aid_mechanics": false,
    "phase_indexed_shock": false,
    "failed_zone_mass_drain": false,
    "conserve_restores_mass": false,
    "max_update_rules": false
  }
}
```

## 12. Decision

Decision: `NO-GENERIC-LEARNER-SIGNAL`

Downstream allowed: `False`

Representation probe allowed: `False`

## 13. Error witnesses

Structural-holdout error witnesses recorded: `25`.

## 14. Bought-by-simplification check

The generic learner is intentionally weak and table-based. A negative result
does not prove the ledger is unlearnable by every possible generic learner. It
only prevents using the prior-confounded CL2 learner as evidence.

## 15. What was NOT shown

- No claim that this is a substrate.
- No claim that world-model content is derived.
- No claim that LLM training is safe.
- No claim that learner performance transfers beyond `FourZoneMassDomain`.
- No claim that the learner is safe under autonomous policy rollout.
- No claim that the learner is safe under arbitrary future actions.
- No claim that the action ledger transfers to other domains.
- No claim that the boundary is learned.
- No claim that the oracle-filtered ledger is available in real domains.
- No claim that data-dependence proves derivability.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.

## 16. Durable result

CL2.2 produced a data-dependence verdict, prior audit, corrupted-control
diagnostics, and durable constraint. The durable decision is recorded in
`outputs/decision.json`.
