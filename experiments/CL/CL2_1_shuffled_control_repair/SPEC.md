# CL2.1 - Shuffled-Control Repair / Artifact Isolation Gate

Status: pre-registered repair gate after CL2.

CL2 halted with `LEARNER-LEAKAGE-FAIL` because the shuffled-target control
scored above threshold even though the initial leakage audit found no forbidden
fields or forbidden oracle calls. CL2.1 diagnoses that failure without claiming
CL2 success.

## Goal Anchor

The project goal is to train an LLM / learner so that its world-model is
derived rather than merely generalized from internet-like data. The current
weakened step is safe-boundary learner training. CL2.1 serves that goal only by
repairing the anti-artifact control required before any learner-probe claim can
be trusted.

## Scope

CL2.1 uses the CL2 candidate safe action ledger and the CL2 primary learner.
It does not train an LLM, run representation analysis, run autonomous rollout,
change CL2 thresholds, or claim CL2 passed.

## Diagnostics

- evaluation integrity check;
- original global target shuffle reproduction;
- within-action target shuffle;
- within-phase target shuffle;
- cross-action target shuffle;
- cross-phase target shuffle;
- independent impossible target control;
- feature permutation control;
- learner bias ablation across primary, majority-delta, memorizer, and copy-source learners.

## Outputs

The runner writes:

- `outputs/control_metrics.json`
- `outputs/decision.json`
- `outputs/final_report.md`
- `outputs/shuffle_diagnostics.json`
- `outputs/impossible_target_diagnostics.json`
- `outputs/learner_bias_audit.json`
- `outputs/evaluation_integrity_audit.md`
- `outputs/control_recommendation.md`
