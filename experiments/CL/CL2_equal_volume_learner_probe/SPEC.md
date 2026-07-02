# CL2 - Equal-Volume Learner Probe on Oracle-Filtered Action Ledger

Status: pre-registered offline learner probe.

CL2 tests whether the CL1.1 oracle-filtered action ledger contains enough
transition structure for a small non-oracle learner to predict successor
observations under equal-volume controls.

This is not substrate discovery, not world-model derivation, and not LLM
training. It is only a learnability precondition after CL1.1.

## Goal Anchor

The project goal is to train an LLM / learner so that its world-model is
derived rather than merely generalized from internet-like data. The current
weakened step is safer learner training inside a safe boundary. CL2 serves that
goal only by testing whether the safe action ledger still supports transition
learning after oracle filtering.

## Scope Carried From CL1.1

The ledger scope remains:

```text
one-step action admission plus CL1 safety-policy continuation
```

CL2 does not test arbitrary future learner actions and does not run autonomous
policy rollout.

## Dataset

Candidate dataset:

```text
all CL1.1 ADMIT_CANDIDATE transitions
```

Learner-visible input:

```text
observe(state), action
```

Target:

```text
observe(successor)
```

Forbidden learner fields:

- collapse labels;
- future outcomes;
- collapse mechanisms;
- witness classes;
- candidate admission decisions;
- oracle rollout results;
- post-hoc metrics;
- source file lineage as feature.

## Splits

- random split: 70/15/15;
- source-state holdout: complete source states held out from training;
- structural holdout: `source_phase == 3`.

## Learners

- primary fixed rule-family learner trained only from visible rows;
- copy-source baseline;
- memorizer baseline;
- majority-delta baseline;
- shuffled-target control;
- equal-volume unfiltered-control learner.

The primary learner is hand-designed around visible transition variables and
fits a small parameterized transition-rule family from training rows. It does
not call oracle transition, collapse, rollout, or admission functions at
prediction time.

## Outputs

The runner writes:

- `outputs/dataset_manifest.json`
- `outputs/split_manifest.json`
- `outputs/metrics.json`
- `outputs/decision.json`
- `outputs/final_report.md`
- `outputs/prediction_error_witnesses.json`
- `outputs/memorization_audit.json`
- `outputs/leakage_audit.md`
