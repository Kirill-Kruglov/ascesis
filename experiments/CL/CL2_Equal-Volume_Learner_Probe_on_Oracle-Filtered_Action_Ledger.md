# CL2: Equal-Volume Learner Probe on Oracle-Filtered Action Ledger

**To:** Codex
**From:** Kirill / analyst
**Task type:** offline learner-probe after CL1.1
**Status:** transition-structure learnability test, not substrate discovery
**Do not name any framework. Do not open a new research programme.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest weakened form:

> Train an LLM / learner inside a **safe boundary** so the learner does not observe collapse-trajectories; safety comes from domain filtering even if content inside the boundary is still generalized rather than fully derived.

Every step must pass the parallel-reality test:

> “We are doing this to obtain a safe / derivable substrate for LLMs, and this step leads there by…”

If the honest ending is “because transition prediction on a toy domain is interesting,” stop and set verdict to `HALT-GOAL-DRIFT`.

---

## 1. Why CL2 exists

CL1.1 repaired the CL1 state-level boundary into an action-conditioned safe ledger.

CL1.1 showed:

```text
ADMIT(state, action)
```

can be evaluated over the exhaustive `(state, action)` set on `FourZoneMassDomain`.

CL1.1 did **not** show:

* that a learner can learn from the admitted ledger;
* that learned content is derived;
* that the result transfers;
* that LLM training is safe;
* that the safe ledger is a substrate.

Therefore CL2 tests only the next precondition:

> Can a small non-oracle learner trained on the CL1.1 oracle-filtered action ledger learn the lawful transition structure inside the admitted safe domain, under equal-volume controls, without using collapse labels, future outcomes, or the transition oracle at prediction time?

---

## 2. Task objective

Run **CL2 — Equal-Volume Learner Probe on Oracle-Filtered Action Ledger**.

The output must be one of:

1. `LEARNER-PROBE-OK`
2. `LEARNER-MEMORIZATION-TRAP`
3. `LEARNER-LEAKAGE-FAIL`
4. `LEARNER-CONTROL-NO-BETTER`
5. `LEARNER-INCONCLUSIVE-DATA`
6. `HALT-GOAL-DRIFT`

All outcomes are valid. A failed learner probe is useful evidence.

---

## 3. What this task is NOT

Do NOT do any of the following:

* Do not claim substrate discovery.
* Do not claim world-model derivation.
* Do not train an LLM.
* Do not train a large neural network.
* Do not do autonomous policy rollout.
* Do not test arbitrary future learner actions.
* Do not claim safety outside the CL1.1 action-ledger scope.
* Do not use collapse labels, future outcomes, collapse mechanisms, or witness classes as learner inputs.
* Do not let the learner call `transition`, `rollout_outcome`, `action_rollout_outcome`, `is_collapsed`, or the candidate admission oracle at prediction time.
* Do not optimize learner architecture after seeing test results.
* Do not turn this into ML benchmarking.
* Do not introduce a new domain.
* Do not build a general substrate generator, DSL, CEGIS loop, or synthesis framework.
* Do not modify, move, delete, stage, or commit existing project files.

---

## 4. Required input files

Read these files if present:

```text
experiments/CL/CL1_boundary_fidelity_pilot/domain.py
experiments/CL/CL1_boundary_fidelity_pilot/boundary.py
experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json
experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json
experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/SPEC.md
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/run_cl1_1.py
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/final_report.md
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/layer_audit_delta.md
playbook_extraction/CL0_closed_ledger_candidate_proposal.md
playbook_extraction/CL0_preregistration.json
playbook_extraction/02_extracted_method.md
playbook_extraction/03_not_yet_method.md
playbook_extraction/harness/output_schema.md
playbook_extraction/harness/failure_conditions.md
```

If some files are absent, list them as `MISSING`.

Continue only if these are present:

```text
CL1 domain implementation
CL1.1 action admission implementation
CL1.1 metrics
CL1.1 decision
CL0/CL1/CL1.1 pre-registration evidence
```

---

## 5. Allowed output files

Create a new experiment directory only:

```text
experiments/CL/CL2_equal_volume_learner_probe/
```

Inside it, create:

```text
SPEC.md
CL2_preregistration.json
dataset_builder.py
learners.py
run_cl2.py
outputs/dataset_manifest.json
outputs/split_manifest.json
outputs/metrics.json
outputs/decision.json
outputs/final_report.md
outputs/prediction_error_witnesses.json
outputs/memorization_audit.json
outputs/leakage_audit.md
```

Do not edit existing files outside the CL2 directory.

---

## 6. CL2 hypothesis

CL2 tests exactly this hypothesis:

```text
H2:
The CL1.1 oracle-filtered action ledger contains enough lawful transition structure
for a small non-oracle learner to learn transition prediction inside the admitted
safe domain better than memorization/copy baselines, under equal-volume controls.
```

This is not a derivability claim.

It is only a precondition:

```text
safe action ledger
→ non-oracle transition learning possible
→ maybe later test representation / derivation
```

---

## 7. Phase A — Pre-registration before dataset split and training

Before computing final metrics, write:

```text
experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json
```

It must contain:

```json
{
  "gate": "CL2",
  "inherits_from": [
    "playbook_extraction/CL0_preregistration.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/CL1_preregistration.json",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json"
  ],
  "repair_context": "CL1.1 produced an oracle-filtered action ledger. CL2 tests only whether a non-oracle learner can learn transition structure from that ledger under equal-volume controls.",
  "domain_name": "FourZoneMassDomain",
  "ledger_scope": "one-step admitted action plus CL1 safety-policy continuation; not arbitrary future learner actions",
  "random_seed": 20260630,
  "candidate_dataset": "all CL1.1 ADMIT_CANDIDATE transitions",
  "equal_volume_control": "sample equal number of transitions from unfiltered state-action space with same seed",
  "learner_visible_input": "observe(state), action",
  "learner_target": "observe(successor)",
  "forbidden_learner_inputs": [
    "collapse_label",
    "future_outcome",
    "collapse_mechanism",
    "witness_class",
    "candidate_admission_decision",
    "oracle_rollout_result",
    "post_hoc_metric",
    "source_file_lineage_as_feature"
  ],
  "forbidden_prediction_calls": [
    "transition",
    "rollout_outcome",
    "action_rollout_outcome",
    "is_collapsed",
    "collapse_mechanism",
    "candidate_action_admission"
  ],
  "splits": {
    "random_split": "70/15/15 train/validation/test over candidate admitted transitions",
    "source_state_holdout": "hold out a disjoint set of source states from training and evaluate on admitted transitions from those source states",
    "structural_holdout": "hold out at least one pre-registered structural slice from training, such as phase == 3 or a mass band, and evaluate there"
  },
  "primary_learner": "non-oracle transition learner implemented in learners.py; fixed before metrics",
  "baselines": [
    "copy_source_baseline",
    "memorizer_baseline",
    "majority_delta_baseline",
    "shuffled_target_control",
    "equal_volume_unfiltered_control_learner"
  ],
  "metrics": {
    "exact_next_observation_accuracy": "fraction of transitions where all successor coordinates are predicted exactly",
    "coordinate_accuracy": "mean coordinate-wise accuracy over successor observation",
    "random_split_accuracy": "exact accuracy on random held-out candidate transitions",
    "source_state_holdout_accuracy": "exact accuracy on unseen source-state candidate transitions",
    "structural_holdout_accuracy": "exact accuracy on pre-registered structural holdout",
    "memorization_gap": "primary learner structural_holdout_accuracy minus memorizer structural_holdout_accuracy",
    "copy_gap": "primary learner structural_holdout_accuracy minus copy_source_baseline structural_holdout_accuracy",
    "control_gap": "primary learner candidate-test accuracy minus equal-volume unfiltered-control learner accuracy on the same candidate test set",
    "shuffled_target_accuracy": "accuracy of learner trained on shuffled targets"
  },
  "thresholds": {
    "random_split_accuracy_min": 0.95,
    "source_state_holdout_accuracy_min": 0.80,
    "structural_holdout_accuracy_min": 0.75,
    "memorization_gap_min": 0.20,
    "copy_gap_min": 0.30,
    "control_gap_min": -0.10,
    "shuffled_target_accuracy_max": 0.25,
    "leakage_allowed": false
  },
  "decision_vocabulary": [
    "LEARNER-PROBE-OK",
    "LEARNER-MEMORIZATION-TRAP",
    "LEARNER-LEAKAGE-FAIL",
    "LEARNER-CONTROL-NO-BETTER",
    "LEARNER-INCONCLUSIVE-DATA",
    "HALT-GOAL-DRIFT"
  ],
  "downstream_halt_rule": "No representation analysis, derivability claim, autonomous rollout, LLM scaling, or substrate claim unless decision is LEARNER-PROBE-OK."
}
```

The report must attest that this file was written before final dataset split, training, and metric computation.

Do not move thresholds after seeing results.

---

## 8. Dataset construction

Use the CL1 / CL1.1 domain and action admission code.

Build these datasets.

## 8.1 Candidate safe action ledger

```text
D_candidate = all transitions (observe(state), action, observe(successor))
where CL1.1 candidate_action_admission(state, action) == ADMIT
```

The learner-visible row contains only:

```text
source_zones, source_mass, source_phase, action, successor_zones, successor_mass, successor_phase
```

It must not contain:

```text
collapse labels
future outcome
collapse mechanism
admission decision
witness class
safe/unsafe tag
rollout result
```

## 8.2 Equal-volume unfiltered control

Build:

```text
D_unfiltered_equal_volume
```

by sampling the same number of transitions as `D_candidate` from the unfiltered `(state, action)` space using the pre-registered seed.

The control learner is trained on this dataset.

It is evaluated on the same candidate safe test sets as the candidate learner.

Purpose:

> ensure that any learner result is not merely due to dataset size or implementation.

## 8.3 Shuffled-target control

Create a copy of the candidate training set with successor observations shuffled.

Purpose:

> ensure the learner/evaluation pipeline cannot score well without real transition structure.

## 8.4 Baseline datasets

The baselines must use the same candidate splits where applicable.

---

## 9. Required splits

Write:

```text
outputs/split_manifest.json
```

It must include exact counts and selection rules for:

1. random train / validation / test split;
2. source-state holdout split;
3. structural holdout split.

## 9.1 Random split

Randomly split `D_candidate` into:

```text
70% train
15% validation
15% test
```

using the pre-registered seed.

## 9.2 Source-state holdout

Hold out complete source states:

```text
no source state in this test split may appear in training
```

Purpose:

> prevent exact table lookup from masquerading as transition learning.

## 9.3 Structural holdout

Pre-register one structural slice before training.

Acceptable examples:

```text
phase == 3
mass in {2, 3}
one zone at boundary health == 0 but not collapsed
```

Pick exactly one and record it in `CL2_preregistration.json`.

Purpose:

> test whether the learner captures lawful transition regularities rather than memorizing seen local patterns.

If the structural holdout has too few candidate transitions, set verdict to `LEARNER-INCONCLUSIVE-DATA`.

---

## 10. Learners and baselines

Implement:

```text
learners.py
```

with at least these learners.

## 10.1 Primary non-oracle learner

A small learner that maps:

```text
observe(state), action → observe(successor)
```

Allowed:

* arithmetic over learner-visible features;
* fitting rules from training rows;
* decision tables over visible features;
* simple coordinate-wise predictors;
* standard-library Python only.

Forbidden:

* calling `transition`;
* calling `rollout_outcome`;
* calling `action_rollout_outcome`;
* calling collapse predicates;
* using admission labels;
* using future outcomes;
* hardcoding the CL1 domain transition function directly from `domain.py`.

If the learner is hand-designed using visible domain variables, state this honestly. It still counts only as a toy learner probe, not derivation.

## 10.2 Copy-source baseline

Predict:

```text
successor_observation = source_observation
```

Purpose:

> ensure apparent accuracy is not due to most transitions being near-identity.

## 10.3 Memorizer baseline

Memorize exact training mapping:

```text
(source_observation, action) → successor_observation
```

For unseen pairs, fall back to copy-source or majority-delta.

Purpose:

> expose table-lookup success.

## 10.4 Majority-delta baseline

Learn the most common successor delta per action from training rows.

Purpose:

> provide a weak non-oracle statistical baseline.

## 10.5 Shuffled-target control

Train the same primary learner on shuffled targets.

Purpose:

> expose pipeline leakage or evaluation bugs.

## 10.6 Equal-volume unfiltered-control learner

Train the same primary learner on `D_unfiltered_equal_volume`.

Evaluate it on the same candidate safe test sets.

Purpose:

> compare safe-ledger training against same-size unfiltered training.

---

## 11. Metrics

Compute metrics for every learner and split.

## 11.1 Exact next-observation accuracy

```text
exact_next_observation_accuracy =
P(predicted successor observation == true successor observation)
```

This is the primary metric.

## 11.2 Coordinate accuracy

Mean exact coordinate accuracy across:

```text
successor_z0
successor_z1
successor_z2
successor_z3
successor_mass
successor_phase
```

This is diagnostic only, not enough for pass.

## 11.3 Memorization gap

```text
memorization_gap =
primary structural_holdout exact accuracy
-
memorizer structural_holdout exact accuracy
```

Pass requires:

```text
memorization_gap >= 0.20
```

## 11.4 Copy gap

```text
copy_gap =
primary structural_holdout exact accuracy
-
copy_source structural_holdout exact accuracy
```

Pass requires:

```text
copy_gap >= 0.30
```

## 11.5 Control gap

```text
control_gap =
primary candidate-test exact accuracy
-
equal-volume unfiltered-control learner exact accuracy on same candidate test
```

Pass requires:

```text
control_gap >= -0.10
```

This does not require the safe-ledger learner to beat unfiltered. It only requires that safe filtering did not destroy learnability relative to equal-volume unfiltered training.

## 11.6 Shuffled target check

Pass requires:

```text
shuffled_target_accuracy <= 0.25
```

If shuffled targets score high, set verdict to `LEARNER-LEAKAGE-FAIL`.

---

## 12. Decision rule

Use exactly this decision rule.

```text
LEARNER-PROBE-OK
iff
no leakage is detected
AND random_split_accuracy >= 0.95
AND source_state_holdout_accuracy >= 0.80
AND structural_holdout_accuracy >= 0.75
AND memorization_gap >= 0.20
AND copy_gap >= 0.30
AND control_gap >= -0.10
AND shuffled_target_accuracy <= 0.25
```

```text
LEARNER-LEAKAGE-FAIL
iff
learner inputs include forbidden fields
OR learner calls forbidden oracle functions at prediction time
OR shuffled_target_accuracy > 0.25
OR evaluation uses target/successor information as input
```

```text
LEARNER-MEMORIZATION-TRAP
iff
random_split_accuracy passes
AND (
  source_state_holdout_accuracy < 0.80
  OR structural_holdout_accuracy < 0.75
  OR memorization_gap < 0.20
)
```

```text
LEARNER-CONTROL-NO-BETTER
iff
no leakage is detected
AND candidate learner does not satisfy control_gap >= -0.10
```

```text
LEARNER-INCONCLUSIVE-DATA
iff
candidate admitted ledger has fewer than 500 transitions
OR any required holdout has fewer than 100 transitions
OR split construction is degenerate
OR learner implementation cannot run without violating constraints
```

```text
HALT-GOAL-DRIFT
iff
the work becomes about ML benchmarking, learner architecture search, policy optimization, toy-domain exploration, or methodology rather than testing safe-ledger transition learnability as a precondition for the LLM substrate goal
```

If multiple verdicts apply, choose the strongest halt in this order:

```text
HALT-GOAL-DRIFT
LEARNER-LEAKAGE-FAIL
LEARNER-INCONCLUSIVE-DATA
LEARNER-MEMORIZATION-TRAP
LEARNER-CONTROL-NO-BETTER
LEARNER-PROBE-OK
```

---

## 13. Required outputs

## 13.1 `outputs/dataset_manifest.json`

Must contain:

```json
{
  "candidate_transition_count": null,
  "unfiltered_equal_volume_transition_count": null,
  "candidate_features": [],
  "candidate_targets": [],
  "forbidden_fields_present": false,
  "random_seed": null,
  "ledger_scope": "one-step action admission plus safety-policy continuation"
}
```

## 13.2 `outputs/split_manifest.json`

Must contain:

```json
{
  "random_split": {
    "train_count": null,
    "validation_count": null,
    "test_count": null
  },
  "source_state_holdout": {
    "train_count": null,
    "test_count": null,
    "heldout_source_state_count": null
  },
  "structural_holdout": {
    "rule": "...",
    "train_count": null,
    "test_count": null
  }
}
```

## 13.3 `outputs/metrics.json`

Must contain metrics for:

```text
primary_learner
copy_source_baseline
memorizer_baseline
majority_delta_baseline
shuffled_target_control
equal_volume_unfiltered_control_learner
```

For each learner, report:

```json
{
  "random_split_exact_accuracy": null,
  "random_split_coordinate_accuracy": null,
  "source_state_holdout_exact_accuracy": null,
  "source_state_holdout_coordinate_accuracy": null,
  "structural_holdout_exact_accuracy": null,
  "structural_holdout_coordinate_accuracy": null
}
```

Also report:

```json
{
  "memorization_gap": null,
  "copy_gap": null,
  "control_gap": null,
  "shuffled_target_accuracy": null
}
```

## 13.4 `outputs/decision.json`

Must contain:

```json
{
  "decision": "...",
  "reason": "...",
  "thresholds_used": {
    "random_split_accuracy_min": 0.95,
    "source_state_holdout_accuracy_min": 0.80,
    "structural_holdout_accuracy_min": 0.75,
    "memorization_gap_min": 0.20,
    "copy_gap_min": 0.30,
    "control_gap_min": -0.10,
    "shuffled_target_accuracy_max": 0.25,
    "leakage_allowed": false
  },
  "downstream_allowed": false
}
```

Set `downstream_allowed: true` only if decision is `LEARNER-PROBE-OK`.

## 13.5 `outputs/prediction_error_witnesses.json`

Include up to 25 error examples for the primary learner on the structural holdout:

```json
{
  "source_observation": "...",
  "action": "...",
  "true_successor_observation": "...",
  "predicted_successor_observation": "...",
  "split": "structural_holdout",
  "error_type": "..."
}
```

If no errors exist, write `[]`.

## 13.6 `outputs/memorization_audit.json`

Must contain:

```json
{
  "exact_training_pair_overlap_random_test": null,
  "exact_training_pair_overlap_source_state_holdout": null,
  "exact_training_pair_overlap_structural_holdout": null,
  "memorizer_structural_holdout_accuracy": null,
  "primary_structural_holdout_accuracy": null,
  "memorization_gap": null,
  "memorization_trap_detected": null
}
```

## 13.7 `outputs/leakage_audit.md`

Must state:

```text
- learner-visible inputs;
- learner targets;
- forbidden fields checked;
- whether collapse labels appear in features;
- whether future outcomes appear in features;
- whether admission decisions appear in features;
- whether learner code imports or calls forbidden oracle functions;
- whether shuffled-target control passed;
- whether evaluation accidentally uses target values as inputs.
```

## 13.8 Final report

Write:

```text
outputs/final_report.md
```

The report must contain exactly these sections:

```text
# CL2 — Equal-Volume Learner Probe on Oracle-Filtered Action Ledger

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. CL1.1 scope carried forward
## 4. Dataset construction
## 5. Pre-registration provenance
## 6. Learners and baselines
## 7. Splits
## 8. Metrics
## 9. Leakage audit
## 10. Memorization audit
## 11. Equal-volume control comparison
## 12. Decision
## 13. Prediction error witnesses
## 14. Bought-by-simplification check
## 15. What was NOT shown
## 16. Durable result
```

---

## 14. Mandatory “what was NOT shown”

Include this section even if CL2 passes.

State explicitly:

* no claim that this is a substrate;
* no claim that world-model content is derived;
* no claim that LLM training is safe;
* no claim that the learner learned beyond `FourZoneMassDomain`;
* no claim that the learner is safe under autonomous policy rollout;
* no claim that the learner is safe under arbitrary future actions;
* no claim that the action ledger transfers to other domains;
* no claim that the boundary is learned;
* no claim that the oracle-filtered ledger is available in real domains;
* no claim that a general substrate generator exists;
* no claim that the playbook is constructive in general.

---

## 15. Halt-downstream rule

If the decision is not `LEARNER-PROBE-OK`, stop.

Do not run representation analysis.

Do not run autonomous rollout.

Do not train an LLM.

Do not make derivability or substrate claims.

The next step after failure is:

```text
LEARNER-LEAKAGE-FAIL → remove leakage and rerun from pre-registration
LEARNER-MEMORIZATION-TRAP → strengthen split / learner / domain or halt learner path
LEARNER-CONTROL-NO-BETTER → analyze whether safe filtering destroyed learnability
LEARNER-INCONCLUSIVE-DATA → fix dataset/split degeneracy before any learner claim
HALT-GOAL-DRIFT → abandon CL2 path
```

If the decision is `LEARNER-PROBE-OK`, the only allowed next step is a separately pre-registered representation / model-internal structure probe. It must still make no substrate or derivability claim until tested.

---

## 16. Pass/fail bar for the Codex task

The Codex task itself succeeds if it produces a complete CL2 report and a valid decision, even if the learner probe fails.

The task fails if:

* no pre-registration JSON is written before dataset split and metric computation;
* thresholds are changed after seeing results;
* learner features include collapse labels, future outcomes, admission labels, or witness classes;
* learner code calls forbidden oracle functions at prediction time;
* there is no equal-volume unfiltered control;
* there is no shuffled-target control;
* there is no memorizer baseline;
* there is no copy-source baseline;
* there is no source-state holdout;
* there is no structural holdout;
* no leakage audit is written;
* no memorization audit is written;
* no prediction witness file is written;
* `what was NOT shown` is omitted;
* the report claims substrate discovery, derived world-model content, autonomous safety, or LLM safety;
* the work turns into learner architecture search, policy optimization, DSL/CEGIS/meta-synthesis, or toy-domain exploration.

---

## 17. Final instruction

The desired result is not “learner success.”

The desired result is a reliable decision:

> either the oracle-filtered action ledger supports non-oracle transition learning under equal-volume controls,
> or the apparent safe ledger is exposed as too narrow, leaky, memorization-prone, or unlearnable.

Optimize for survival under criticism, not for preserving the CL1.1 positive result.

