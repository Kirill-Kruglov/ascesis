# CL-PM0 — CL Branch Postmortem

## 0. Verdict

`CL-BRANCH-CLOSED`

The CL branch produced a non-vacuous oracle-filtered action-safe ledger on one
toy lawful domain, but failed to produce admissible evidence of generic
non-oracle transition learning. Therefore no representation, derivability,
substrate, or LLM-safety downstream work is allowed from this branch.

## 1. Goal anchor

The project goal is to train an LLM / learner so that its world-model is
derived, not merely generalized from internet-like data.

The current honest weakened form is to train a learner inside a safe boundary so
the learner does not observe collapse trajectories. The CL branch tested
preconditions for that weakened form. It did not deliver the main goal.

## 2. Inputs used

| file | status |
|---|---|
| `playbook_extraction/CL0_closed_ledger_candidate_proposal.md` | PRESENT |
| `playbook_extraction/CL0_preregistration.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/SPEC.md` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL1_boundary_fidelity_pilot/outputs/layer_audit.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/SPEC.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/layer_audit_delta.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/SPEC.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/metrics.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/decision.json` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md` | PRESENT |
| `experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/SPEC.md` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/control_metrics.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/decision.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/learner_bias_audit.json` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/evaluation_integrity_audit.md` | PRESENT |
| `experiments/CL/CL2_1_shuffled_control_repair/outputs/control_recommendation.md` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/SPEC.md` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/learning_curve_metrics.json` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/control_metrics.json` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/prior_ablation_metrics.json` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/decision.json` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/final_report.md` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/data_dependence_audit.json` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/prior_audit.md` | PRESENT |
| `experiments/CL/CL2_2_learner_prior_ablation/outputs/durable_constraint.md` | PRESENT |
| `research/closed_directions_ledger.md` | MISSING before PM0; CREATED by PM0 |
| `playbook_extraction/02_extracted_method.md` | PRESENT |
| `playbook_extraction/03_not_yet_method.md` | PRESENT |
| `playbook_extraction/harness/output_schema.md` | PRESENT |
| `playbook_extraction/harness/failure_conditions.md` | PRESENT |

## 3. Timeline of CL gates

| gate | question | decision | useful result | halt / limitation |
| ---- | -------- | -------- | ------------- | ----------------- |
| CL0 | Is there a minimal candidate family after closed directions? | `PASS-CANDIDATE` | Proposed a layer-audited safe-transition ledger as a weakened boundary candidate. | Candidate only; not substrate or derivability evidence. |
| CL1 | Can a state-level boundary be faithful and non-vacuous on `FourZoneMassDomain`? | `BOUNDARY-FIDELITY-OK` | Candidate state boundary had false-safe rate `0.0`, false-positive rate `0.0`, equal-volume possible. | State-level SAFE did not yet define a learner transition ledger. |
| CL1.1 | Can state safety be repaired into action-conditioned ledger admission? | `ACTION-LEDGER-OK` | Candidate action ledger admitted `31142` transitions with unsafe admitted rate `0.0`. | Scope is oracle-filtered one-step action plus safety-policy continuation, not substrate evidence. |
| CL2 | Can a learner learn transition structure from the safe ledger under equal volume? | `LEARNER-LEAKAGE-FAIL` | Primary learner passed accuracy gates, exposing a tempting false positive. | Shuffled-target accuracy `0.6463414634146342` exceeded threshold `0.25`. |
| CL2.1 | Was the shuffled failure leakage, evaluation bug, or bias artifact? | `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT` | No direct leakage/evaluation bug found; rule-family learner prior identified as confound. | CL2 rerun and representation work not allowed. |
| CL2.2 | Does performance depend on data after prior ablation? | `NO-GENERIC-LEARNER-SIGNAL` | Generic learner controls stayed low and no leakage/artifact persisted. | Generic full-data structural accuracy `0.0`; no evidence-bearing learner signal. |

## 4. What survived

1. Boundary-first discipline survived: boundary and ledger gates halted learner claims before downstream representation work.
2. State-level safety was shown insufficient for learner ledgers: CL1 state-level carryover admitted unsafe actions at rate `0.2339757498404595`.
3. An action-conditioned oracle ledger exists on `FourZoneMassDomain`: CL1.1 admitted `31142` action transitions with unsafe admitted rate `0.0`.
4. Projection-blind, state-level, and trivially-safe baselines were useful controls.
5. The CL kill-gate chain prevented false learner evidence from being promoted.
6. The CL branch produced durable constraints for future substrate search.

## 5. What failed

1. CL1 state-level SAFE did not imply safe action ledger.
2. CL2 learner result was not admissible because shuffled-target control failed.
3. CL2.1 showed the primary rule-family learner was confounded by transition-family prior.
4. CL2.2 showed no evidence-bearing generic learner signal on the current safe ledger.
5. The current CL learner path cannot proceed to representation / derivability.

## 6. What was killed

| killed direction | evidence | failure mode | durable constraint |
| ---------------- | -------- | ------------ | ------------------ |
| K1 - State-level SAFE as learner-ledger admission | CL1.1 state-level carryover baseline | `SAFE(state)` plus all actions leaked unsafe transitions. | Future learner ledgers must be action-conditioned or transition-conditioned. |
| K2 - Oracle-filtered action ledger as substrate evidence | CL1.1 `ACTION-LEDGER-OK`; CL2.2 halt | Action-safe ledger exists but does not show substrate, derivability, learned boundary, or transfer. | Safe ledger is only a precondition, not substrate evidence. |
| K3 - Rule-family learner as evidence of learning-from-ledger | CL2 high learner scores; CL2.1 `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT` | `RuleFamilyTransitionLearner` solved the task while carrying transition-family prior. | Learners that encode the domain transition family are diagnostic-only. |
| K4 - Original global shuffled-target control as sufficient anti-leakage gate | CL2 shuffled-target accuracy `0.6463414634146342`; CL2.1 diagnostics | Global shuffle failed high under primary rule-family learner; control was invalid against this prior. | Future learner probes need controls that distinguish data-dependence from prior-dependence. |
| K5 - Current CL safe ledger as evidence-bearing for generic transition learning | CL2.2 `NO-GENERIC-LEARNER-SIGNAL` | Generic learner showed no full-data exact transition signal under required holdouts. | Current safe ledger/domain/learner interface is not admissible evidence for learned transition structure. |

## 7. What remains open

- Whether a different lawful domain can produce a safe ledger that is evidence-bearing for generic learners.
- Whether a different learner class, without exact transition-family prior, can show data-dependent learning under stricter controls.
- Whether the problem is the domain, the ledger interface, the learner class, or the weakened project formulation.
- Whether future analytic work can derive a candidate direction from accumulated impossibility constraints.

Forbidden as next moves: tune learners until success, run representation analysis anyway, scale to LLM, or claim boundary safety transfers.

## 8. Fundamental constraints extracted

1. Boundary fidelity must precede learner claims.
2. State safety is weaker than transition/action safety.
3. Safe filtering is not derivability.
4. Oracle-filtered data is not a learned boundary.
5. Learner success is not evidence if bought by transition-family prior.
6. Generic learner failure blocks representation/derivability work.
7. Negative controls must be designed against the learner's inductive bias, not only against field leakage.
8. Toy-domain success cannot transfer without a separate transfer gate.
9. A safe ledger must become evidence-bearing before model-internal claims are allowed.

## 9. Bought-by-simplification analysis

`FourZoneMassDomain` simplified away real-world open-endedness, high-dimensional
state, ambiguous observations, stochasticity, and non-toy intervention structure.

The oracle action ledger bought safety by using full transition knowledge and
audit-only collapse predicates. That is acceptable as a safety precondition but
blocks any claim that the boundary was learned or available in realistic domains.

The rule-family learner bought performance by encoding a transition-family prior.
CL2.1 showed this made the original shuffled-target control invalid and made the
learner diagnostic-only.

The generic learner lost the transition-family prior and then failed to produce
full-data exact learning signal under source-state and structural holdouts.

Acceptable simplifications: toy domain, oracle collapse audit, finite exhaustive
ledger, and pre-registered gates as precondition tests.

Blocking simplifications: oracle-filtered ledger as substrate evidence, encoded
transition law as learner evidence, and toy-domain success as transfer evidence.

## 10. Parallel-reality check

We did CL0-CL2.2 to obtain a safe / derivable substrate for LLMs, and this branch
led there by showing that a safe action ledger is possible on a toy lawful
domain, but also showing that this is insufficient for learner-derived
world-model evidence unless the ledger supports generic, data-dependent
learning. Therefore the branch constrains future substrate search rather than
providing a substrate.

## 11. What was NOT shown

- No substrate was found.
- No derived world-model was shown.
- No LLM safety was shown.
- No learned boundary was shown.
- No transfer beyond `FourZoneMassDomain` was shown.
- No autonomous learner safety was shown.
- No arbitrary future action safety was shown.
- No generic transition-learning evidence was shown.
- No representation probe is allowed.
- No derivability claim is allowed.
- No general substrate generator exists.
- No general constructive playbook was shown.

## 12. Closed-direction ledger update summary

The ledger section `## CL branch: safe action ledger without generic learner signal`
was written to `experiments/CL/CL_PM0_postmortem/CL_PM0_closed_direction_entries.md`
and created in `research/closed_directions_ledger.md`.

The central ledger did not exist before PM0, so PM0 created it with the required
CL branch section.

## 13. Next analytic work allowed

Allowed:

1. postmortem review;
2. closed-direction ledger review;
3. analytic constraint-map work.

Not allowed from this branch:

1. representation analysis;
2. derivability claims;
3. autonomous rollout;
4. LLM training;
5. substrate claims;
6. learner tuning until success.

## 14. Final durable result

The CL branch is closed as a substrate / derivability / learner-evidence path.
It is retained as boundary precondition evidence, action-ledger precondition
evidence, and negative constraints for future analytic substrate search.
