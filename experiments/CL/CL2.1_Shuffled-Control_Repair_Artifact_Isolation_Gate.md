# Codex Task — CL2.1: Shuffled-Control Repair / Artifact Isolation Gate

**To:** Codex
**From:** Kirill / analyst
**Task type:** repair-gate after CL2
**Status:** anti-leakage / anti-artifact control repair
**Do not name any framework. Do not open a new research programme.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest weakened form:

> Train an LLM / learner inside a **safe boundary** so the learner does not observe collapse-trajectories; safety comes from domain filtering even if content inside the boundary is still generalized rather than fully derived.

Every step must pass the parallel-reality test:

> “We are doing this to obtain a safe / derivable substrate for LLMs, and this step leads there by…”

If the honest ending is “because shuffled controls, toy-domain ML, or learner diagnostics are interesting,” stop and set verdict to `HALT-GOAL-DRIFT`.

---

## 1. Why CL2.1 exists

CL2 tested whether a small non-oracle learner could learn transition structure from the CL1.1 oracle-filtered action ledger under equal-volume controls.

CL2 result:

```text
LEARNER-LEAKAGE-FAIL
```

The primary learner passed the accuracy / holdout gates, but the shuffled-target control scored too high:

```text
shuffled_target_accuracy = 0.6463414634146342
pre-registered threshold <= 0.25
```

The leakage audit did not find forbidden learner fields or forbidden oracle calls.

Therefore CL2.1 must not attempt to claim learner success.

CL2.1 must answer a narrower question:

> Was the CL2 shuffled-target failure caused by real leakage, by an evaluation bug, by marginal-distribution artifacts, or by a strong hand-designed rule-family inductive bias that makes the original shuffled-target control invalid for this setting?

---

## 2. Task objective

Run **CL2.1 — Shuffled-Control Repair / Artifact Isolation Gate**.

Your job is to diagnose and repair the anti-leakage / anti-artifact controls used in CL2.

The output must be one of:

1. `CONTROL-REPAIRED-CL2-RERUN-ALLOWED`
2. `REAL-LEAKAGE-DETECTED`
3. `EVALUATION-BUG-DETECTED`
4. `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT`
5. `INCONCLUSIVE-CONTROL-FAILURE`
6. `HALT-GOAL-DRIFT`

All six outcomes are valid.

A negative / inconclusive result is useful if it prevents false constructive claims.

---

## 3. What this task is NOT

Do NOT do any of the following:

* Do not claim CL2 learner success.
* Do not rerun CL2 with relaxed thresholds.
* Do not move the CL2 shuffled-target threshold.
* Do not claim substrate discovery.
* Do not claim world-model derivation.
* Do not train an LLM.
* Do not run representation analysis.
* Do not run autonomous rollout.
* Do not introduce a new domain.
* Do not optimize learner architecture for score.
* Do not turn this into ML benchmarking.
* Do not build a general methodology of controls.
* Do not build a DSL, CEGIS loop, synthesis framework, or substrate generator.
* Do not modify, move, delete, stage, or commit existing project files.

---

## 4. Required input files

Read these files if present:

```text
experiments/CL/CL2_equal_volume_learner_probe/SPEC.md
experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json
experiments/CL/CL2_equal_volume_learner_probe/dataset_builder.py
experiments/CL/CL2_equal_volume_learner_probe/learners.py
experiments/CL/CL2_equal_volume_learner_probe/run_cl2.py
experiments/CL/CL2_equal_volume_learner_probe/outputs/dataset_manifest.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/split_manifest.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/metrics.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/decision.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/final_report.md
experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json
experiments/CL/CL1_boundary_fidelity_pilot/domain.py
playbook_extraction/02_extracted_method.md
playbook_extraction/03_not_yet_method.md
playbook_extraction/harness/output_schema.md
playbook_extraction/harness/failure_conditions.md
```

If some files are absent, list them as `MISSING`.

Continue only if these are present:

```text
CL2 dataset builder
CL2 learners
CL2 runner
CL2 metrics
CL2 leakage audit
CL2 decision
CL1 / CL1.1 domain and ledger code
```

---

## 5. Allowed output files

Create a new experiment directory only:

```text
experiments/CL/CL2_1_shuffled_control_repair/
```

Inside it, create:

```text
SPEC.md
CL2_1_preregistration.json
control_diagnostics.py
run_cl2_1.py
outputs/control_metrics.json
outputs/decision.json
outputs/final_report.md
outputs/shuffle_diagnostics.json
outputs/impossible_target_diagnostics.json
outputs/learner_bias_audit.json
outputs/evaluation_integrity_audit.md
outputs/control_recommendation.md
```

Do not edit existing files outside the CL2.1 directory.

---

## 6. CL2.1 hypotheses

CL2.1 tests four competing explanations.

```text
H1_REAL_LEAKAGE:
The CL2 learner or evaluation pipeline had access to forbidden information, despite the first audit not finding it.
```

```text
H2_EVALUATION_BUG:
The shuffled-target score was high because evaluation accidentally compared against shuffled targets, reused training targets, or otherwise evaluated the wrong object.
```

```text
H3_MARGINAL_ARTIFACT:
The shuffled targets retained enough marginal / bucket structure that exact successor prediction remained high for reasons unrelated to lawful transition learning.
```

```text
H4_STRONG_INDUCTIVE_BIAS:
The rule-family learner has such a strong prior over the true transition family that the original shuffled-target control is invalid; it can recover true-ish transition rules from features and domain-shaped target marginals even when pairwise source-target alignment is broken.
```

The task must decide which explanation is best supported.

---

## 7. Phase A — Pre-registration before diagnostics

Before running diagnostics, write:

```text
experiments/CL/CL2_1_shuffled_control_repair/CL2_1_preregistration.json
```

It must contain:

```json
{
  "gate": "CL2.1",
  "inherits_from": [
    "experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/decision.json"
  ],
  "repair_reason": "CL2 halted because shuffled-target control scored above the pre-registered maximum despite no forbidden fields or forbidden oracle calls being found.",
  "domain_name": "FourZoneMassDomain",
  "dataset_scope": "CL2 candidate safe action ledger only; one-step action admission plus safety-policy continuation",
  "random_seed": 20260630,
  "diagnostics": [
    "evaluation_integrity_check",
    "global_target_shuffle",
    "within_action_target_shuffle",
    "within_phase_target_shuffle",
    "cross_action_target_shuffle",
    "cross_phase_target_shuffle",
    "independent_impossible_target_control",
    "feature_permutation_control",
    "learner_bias_ablation"
  ],
  "primary_question": "Can we distinguish true leakage/evaluation failure from an invalid shuffled-target control caused by bias or marginal artifacts?",
  "thresholds": {
    "global_shuffle_exact_accuracy_max": 0.25,
    "within_action_shuffle_exact_accuracy_max": 0.25,
    "within_phase_shuffle_exact_accuracy_max": 0.25,
    "cross_action_shuffle_exact_accuracy_max": 0.25,
    "cross_phase_shuffle_exact_accuracy_max": 0.25,
    "independent_impossible_target_exact_accuracy_max": 0.10,
    "feature_permutation_exact_accuracy_max": 0.25,
    "evaluation_mismatch_allowed": false,
    "forbidden_field_allowed": false,
    "forbidden_oracle_call_allowed": false
  },
  "decision_vocabulary": [
    "CONTROL-REPAIRED-CL2-RERUN-ALLOWED",
    "REAL-LEAKAGE-DETECTED",
    "EVALUATION-BUG-DETECTED",
    "SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT",
    "INCONCLUSIVE-CONTROL-FAILURE",
    "HALT-GOAL-DRIFT"
  ],
  "downstream_halt_rule": "No CL2 rerun, representation analysis, derivability claim, autonomous rollout, LLM scaling, or substrate claim unless decision is CONTROL-REPAIRED-CL2-RERUN-ALLOWED."
}
```

The report must attest that this file was written before diagnostic metrics were computed.

Do not change thresholds after seeing diagnostics.

---

## 8. Required diagnostics

Use the same CL2 candidate rows, splits, and primary learner unless a diagnostic explicitly says otherwise.

The learner must still not call forbidden oracle functions at prediction time.

---

### 8.1 Evaluation integrity check

Verify the following:

```text
1. Test features do not contain target fields.
2. Train features do not contain target fields.
3. Prediction is computed before target comparison.
4. Exact accuracy compares prediction to the original true test target.
5. Shuffled-control training targets are shuffled only in the training set.
6. Shuffled-control test targets remain true original targets.
7. No test target is used during fit.
8. No forbidden oracle function is imported or called in learners.py.
9. No forbidden fields exist in dataset rows.
```

If any violation is found, verdict must be:

```text
EVALUATION-BUG-DETECTED
```

or

```text
REAL-LEAKAGE-DETECTED
```

depending on the violation.

---

### 8.2 Original global shuffle reproduction

Reproduce the CL2 shuffled-target control exactly.

Purpose:

> confirm that the high shuffled score is reproducible.

Output:

```text
global_shuffle_exact_accuracy by split
global_shuffle_coordinate_accuracy by split
```

---

### 8.3 Within-action target shuffle

Shuffle targets only within each action bucket.

Purpose:

> test whether action-conditioned target marginals explain the high score.

If within-action shuffle remains high, the control may be preserving too much action-level structure.

---

### 8.4 Within-phase target shuffle

Shuffle targets only within each source phase bucket.

Purpose:

> test whether phase-conditioned target marginals explain the high score.

If within-phase shuffle remains high, phase structure may dominate the learner.

---

### 8.5 Cross-action target shuffle

Shuffle targets across incompatible action buckets.

Implementation:

```text
AID_0 targets should be assigned to non-AID_0 rows where possible.
AID_1 targets should be assigned to non-AID_1 rows where possible.
...
CONSERVE targets should be assigned to non-CONSERVE rows where possible.
```

Purpose:

> destroy action-target compatibility.

If cross-action shuffle still scores high, suspect evaluation bug, leakage, or overly deterministic target marginals.

---

### 8.6 Cross-phase target shuffle

Shuffle targets across incompatible phase buckets.

Implementation:

```text
source_phase p targets should be assigned to rows with source_phase != p where possible.
```

Purpose:

> destroy phase-target compatibility.

If cross-phase shuffle still scores high, suspect evaluation bug, leakage, or target marginal dominance.

---

### 8.7 Independent impossible target control

Replace training targets with independently sampled valid-looking targets.

Targets must be valid observations but not generated by the transition rule.

Example:

```text
successor_zones sampled uniformly from observed zone range
successor_mass sampled uniformly from observed mass range
successor_phase sampled uniformly from observed phase range
```

Use fixed pre-registered seed.

Purpose:

> if the learner still scores high, there is evaluation leakage or an evaluation bug.

Pass condition:

```text
independent_impossible_target_exact_accuracy <= 0.10
```

---

### 8.8 Feature permutation control

Permute source features while keeping true targets fixed in training.

Examples:

```text
permute source_zones across rows
permute source_mass across rows
permute source_phase across rows
permute action across rows
```

Purpose:

> test whether the learner can score well without correct source-target pairing.

Pass condition:

```text
feature_permutation_exact_accuracy <= 0.25
```

---

### 8.9 Learner bias ablation

Run the same diagnostics for at least these learners:

```text
primary_rule_family_learner
majority_delta_baseline
memorizer_baseline
copy_source_baseline
```

Optionally add a deliberately weaker coordinate-majority learner if simple to implement.

Purpose:

> identify whether the high shuffled score is specific to the rule-family learner or appears across learners.

If only the rule-family learner scores high on marginal-preserving shuffles, but impossible-target and cross-bucket controls fail low, classify as:

```text
SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT
```

not as proven real leakage.

---

## 9. Required metrics

Write:

```text
outputs/control_metrics.json
```

It must contain:

```json
{
  "evaluation_integrity": {
    "target_fields_in_features": null,
    "test_target_used_in_fit": null,
    "prediction_compared_to_original_true_target": null,
    "forbidden_fields_present": null,
    "forbidden_oracle_calls": [],
    "evaluation_mismatch_detected": null
  },
  "original_global_shuffle": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "within_action_shuffle": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "within_phase_shuffle": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "cross_action_shuffle": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "cross_phase_shuffle": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "independent_impossible_target": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "feature_permutation_control": {
    "primary": {
      "random_exact": null,
      "source_holdout_exact": null,
      "structural_holdout_exact": null,
      "max_exact": null
    }
  },
  "learner_bias_ablation": {
    "majority_delta_baseline": {},
    "memorizer_baseline": {},
    "copy_source_baseline": {}
  }
}
```

For every control and learner, report both exact and coordinate accuracy.

Use `max_exact` across required splits as the gate value.

---

## 10. Decision rule

Use exactly this decision rule.

```text
EVALUATION-BUG-DETECTED
iff
evaluation_integrity.evaluation_mismatch_detected == true
OR prediction is compared to shuffled test target instead of original true target
OR target fields are included in features
OR test target is used during fit
```

```text
REAL-LEAKAGE-DETECTED
iff
forbidden fields are present
OR forbidden oracle calls are imported/called in learner prediction
OR independent_impossible_target max_exact > 0.10
```

```text
SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT
iff
no evaluation bug is detected
AND no real leakage is detected
AND original_global_shuffle max_exact > 0.25
AND (
  cross_action_shuffle max_exact <= 0.25
  OR cross_phase_shuffle max_exact <= 0.25
  OR independent_impossible_target max_exact <= 0.10
)
AND high shuffled score is concentrated in primary_rule_family_learner rather than all baselines
```

```text
CONTROL-REPAIRED-CL2-RERUN-ALLOWED
iff
no evaluation bug is detected
AND no real leakage is detected
AND at least one repaired negative control is identified whose max_exact is below threshold:
  - cross_action_shuffle max_exact <= 0.25
  - cross_phase_shuffle max_exact <= 0.25
  - independent_impossible_target max_exact <= 0.10
  - feature_permutation_control max_exact <= 0.25
AND the report specifies a replacement CL2 shuffled-control rule to use in a future CL2 rerun
```

```text
INCONCLUSIVE-CONTROL-FAILURE
iff
no evaluation bug is detected
AND no real leakage is detected
AND all repaired controls remain high
OR diagnostics disagree in a way that does not support a replacement control
```

```text
HALT-GOAL-DRIFT
iff
the work becomes about general control methodology, learner benchmarking, toy-domain analysis, or architecture tuning rather than repairing the CL2 anti-artifact gate for the safe-ledger learner probe
```

If multiple verdicts apply, choose the strongest halt in this order:

```text
HALT-GOAL-DRIFT
EVALUATION-BUG-DETECTED
REAL-LEAKAGE-DETECTED
INCONCLUSIVE-CONTROL-FAILURE
SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT
CONTROL-REPAIRED-CL2-RERUN-ALLOWED
```

Important:

`CONTROL-REPAIRED-CL2-RERUN-ALLOWED` does not mean CL2 passed.

It only means a repaired CL2 rerun is allowed with a stronger pre-registered control.

---

## 11. Required outputs

### 11.1 `outputs/shuffle_diagnostics.json`

Must contain detailed split-level metrics for:

```text
original_global_shuffle
within_action_shuffle
within_phase_shuffle
cross_action_shuffle
cross_phase_shuffle
```

For each:

```json
{
  "random_exact": null,
  "random_coordinate": null,
  "source_holdout_exact": null,
  "source_holdout_coordinate": null,
  "structural_holdout_exact": null,
  "structural_holdout_coordinate": null,
  "max_exact": null
}
```

---

### 11.2 `outputs/impossible_target_diagnostics.json`

Must contain:

```json
{
  "independent_impossible_target": {
    "random_exact": null,
    "source_holdout_exact": null,
    "structural_holdout_exact": null,
    "max_exact": null
  },
  "feature_permutation_control": {
    "random_exact": null,
    "source_holdout_exact": null,
    "structural_holdout_exact": null,
    "max_exact": null
  }
}
```

---

### 11.3 `outputs/learner_bias_audit.json`

Must contain per-learner diagnostics for:

```text
primary_rule_family_learner
majority_delta_baseline
memorizer_baseline
copy_source_baseline
```

For each learner, report max exact accuracy under:

```text
original_global_shuffle
within_action_shuffle
within_phase_shuffle
cross_action_shuffle
cross_phase_shuffle
independent_impossible_target
feature_permutation_control
```

Also include:

```json
{
  "high_score_concentrated_in_primary": null,
  "bias_artifact_supported": null,
  "notes": "..."
}
```

---

### 11.4 `outputs/evaluation_integrity_audit.md`

Must state:

```text
- whether target fields appear in learner features;
- whether test targets are used in fit;
- whether shuffled-control test targets remain original true targets;
- whether prediction is compared against original true test targets;
- whether forbidden fields exist in rows;
- whether forbidden oracle calls are imported or called;
- whether independent impossible targets scored below threshold;
- whether any evaluation mismatch was found.
```

---

### 11.5 `outputs/control_recommendation.md`

Must specify one of:

```text
NO_RERUN_ALLOWED
RERUN_CL2_WITH_CROSS_ACTION_SHUFFLE
RERUN_CL2_WITH_CROSS_PHASE_SHUFFLE
RERUN_CL2_WITH_INDEPENDENT_IMPOSSIBLE_TARGET
RERUN_CL2_WITH_FEATURE_PERMUTATION_CONTROL
RERUN_CL2_WITH_MULTIPLE_REPAIRED_CONTROLS
```

If a rerun is recommended, state the replacement pre-registered threshold.

Do not recommend rerun if real leakage or evaluation bug is detected.

---

### 11.6 `outputs/decision.json`

Must contain:

```json
{
  "decision": "...",
  "reason": "...",
  "thresholds_used": {
    "global_shuffle_exact_accuracy_max": 0.25,
    "within_action_shuffle_exact_accuracy_max": 0.25,
    "within_phase_shuffle_exact_accuracy_max": 0.25,
    "cross_action_shuffle_exact_accuracy_max": 0.25,
    "cross_phase_shuffle_exact_accuracy_max": 0.25,
    "independent_impossible_target_exact_accuracy_max": 0.10,
    "feature_permutation_exact_accuracy_max": 0.25,
    "evaluation_mismatch_allowed": false,
    "forbidden_field_allowed": false,
    "forbidden_oracle_call_allowed": false
  },
  "cl2_rerun_allowed": false,
  "downstream_representation_allowed": false
}
```

Set `cl2_rerun_allowed: true` only if decision is `CONTROL-REPAIRED-CL2-RERUN-ALLOWED`.

Never set `downstream_representation_allowed: true` in CL2.1.

---

### 11.7 Final report

Write:

```text
outputs/final_report.md
```

The report must contain exactly these sections:

```text
# CL2.1 — Shuffled-Control Repair / Artifact Isolation Gate

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. CL2 failure being repaired
## 4. Pre-registration provenance
## 5. Evaluation integrity audit
## 6. Shuffle diagnostics
## 7. Impossible-target and feature-permutation diagnostics
## 8. Learner bias ablation
## 9. Competing explanations
## 10. Decision
## 11. Replacement control recommendation
## 12. Bought-by-simplification check
## 13. What was NOT shown
## 14. Durable result
```

---

## 12. Mandatory “what was NOT shown”

Include this section regardless of verdict.

State explicitly:

* no claim that CL2 passed;
* no claim that learner transition learning is admissible evidence yet;
* no claim that this is a substrate;
* no claim that world-model content is derived;
* no claim that LLM training is safe;
* no claim that action-ledger safety transfers to other domains;
* no claim that the boundary is learned;
* no claim that the oracle-filtered ledger is available in real domains;
* no claim that a general substrate generator exists;
* no claim that the playbook is constructive in general;
* no claim that repairing a control proves the learner result.

---

## 13. Halt-downstream rule

CL2.1 may only allow a CL2 rerun with repaired controls.

CL2.1 may not allow:

```text
representation analysis
derivability claims
autonomous rollout
LLM training
substrate claims
```

If verdict is not `CONTROL-REPAIRED-CL2-RERUN-ALLOWED`, stop.

If verdict is `CONTROL-REPAIRED-CL2-RERUN-ALLOWED`, the next allowed step is:

```text
CL2.2 or CL2-rerun with repaired pre-registered controls
```

not CL3.

---

## 14. Pass/fail bar for the Codex task

The Codex task itself succeeds if it produces a complete CL2.1 report and a valid decision, even if no rerun is allowed.

The task fails if:

* no pre-registration JSON is written before diagnostics;
* thresholds are changed after seeing diagnostics;
* original CL2 shuffled failure is not reproduced;
* no evaluation integrity audit is written;
* no impossible-target control is run;
* no cross-action or cross-phase shuffle is run;
* no feature-permutation control is run;
* no learner-bias ablation is run;
* no control recommendation is written;
* real leakage is ignored;
* an evaluation bug is ignored;
* `what was NOT shown` is omitted;
* the report claims CL2 passed;
* the report allows representation / derivability work;
* the work turns into general ML benchmarking, control methodology, toy-domain exploration, DSL/CEGIS/meta-synthesis, or substrate-generation theory.

---

## 15. Final instruction

The desired result is not “repair success.”

The desired result is an honest instrument verdict:

> either the CL2 control failure is explained and a stronger rerun control is pre-registered,
> or CL2 remains halted because its anti-artifact instrument is not trustworthy.

Optimize for survival under criticism, not for recovering the CL2 positive-looking learner scores.

