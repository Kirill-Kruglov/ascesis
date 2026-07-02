# CL2.2 - Learner-Prior Ablation / Data-Dependence Gate

Status: pre-registered data-dependence repair gate after CL2.1.

CL2.1 found that the CL2 primary rule-family learner was confounded by strong
transition-family prior. CL2.2 tests whether transition-prediction performance
can be shown to depend on safe-ledger data when that prior is ablated.

## Goal Anchor

The project goal is to train an LLM / learner so that its world-model is
derived rather than merely generalized from internet-like data. The current
weakened step is safe-boundary learner training. CL2.2 serves that goal only by
testing whether a learner's transition prediction depends on safe-ledger data
rather than an inadmissible hand-coded transition prior.

## Scope

CL2.2 uses the CL2 candidate safe action ledger:

```text
one-step action admission plus CL1 safety-policy continuation
```

It does not claim CL2 passed, does not run representation analysis, does not
train an LLM, and does not claim substrate discovery or derivability.

## Evidence-Eligible Learner

The evidence-eligible learner is a generic table/backoff learner over visible
feature subsets. It learns target-coordinate values from rows. It does not
encode the exact CL1 transition family and does not call oracle functions.

## Diagnostics

- zero-fit diagnostic;
- 1%, 5%, 20%, and 100% data learning curve;
- source-state, structural, and cross-phase holdouts;
- corrupted-target controls;
- prior diagnostic using the CL2 rule-family learner, labeled diagnostic-only;
- leakage and prior audit.

## Outputs

The runner writes:

- `outputs/dataset_manifest.json`
- `outputs/learning_curve_metrics.json`
- `outputs/control_metrics.json`
- `outputs/prior_ablation_metrics.json`
- `outputs/decision.json`
- `outputs/final_report.md`
- `outputs/data_dependence_audit.json`
- `outputs/prior_audit.md`
- `outputs/error_witnesses.json`
- `outputs/durable_constraint.md`
