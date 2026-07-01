# S2 Failure Analysis

## Decision Vocabulary Evaluation

`S2-FAIL-AD-HOC-SEMANTIC-ORACLE`

Result:
Not triggered. Given the finite case fields, replay is deterministic. The
specification does not ask a human what the claim really means during replay.

Residual risk:
The case fields are authored by humans. This is acceptable for S2 only because
S2 is a toy-model specification gate, not a learning-evidence gate.

`S2-FAIL-FINITE-DOMAINS-UNDEFINED`

Result:
Not triggered. Expression, primitive, derivation trace, scope, assumption, test,
outcome, anchor, population, and Goodhart flag domains are finite and explicit.

Residual risk:
The finite domains are small and tailored to the S0 cases. Transfer to broader
language is not shown.

`S2-FAIL-CONSEQUENCE-TESTS-NONOPERATIONAL`

Result:
Not triggered. Each test has allowed scopes, expected outcomes, contrast
outcomes, and a failure condition.

Residual risk:
The tests are toy tokens, not empirical procedures.

`S2-FAIL-ANCHORS-NONOPERATIONAL`

Result:
Not triggered. Anchor presence and absence conditions are defined over toy
fields.

Residual risk:
External anchors are only finite tokens in S2; no external check is performed.

`S2-FAIL-SCOPE-COST-UNDEFINED`

Result:
Not triggered. Scope cost, lineage requirement, and consequence delta are
required for non-default context creation.

Residual risk:
Cost values are ordinal toy costs, not measured costs.

`S2-FAIL-POPULATION-STATE-AS-POPULARITY`

Result:
Not triggered. Population agreement cannot promote to `STABLE` without
adversarial paraphrase survival, consequence tests, contradiction containment,
and non-population anchors.

Residual risk:
Population state is not exercised as a real multi-agent process.

`S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL`

Result:
Not triggered. Each Goodhart flag has an activation predicate over finite toy
fields, blocked transitions, repair condition, activating case, and danger
condition.

Residual risk:
The predicates are sufficient for the seven cases, not for open-ended language.

`S2-FAIL-REPEATS-CL-MISTAKES`

Result:
Not triggered. S2 does not treat a safe ledger as substrate evidence, a
hand-coded prior as learning evidence, or preconditions as derivability
evidence.

Residual risk:
Future work must continue to separate hand-coded toy rules from learner
evidence.

`S2-INCONCLUSIVE`

Result:
Not selected. The toy fields are concrete enough for a later tiny
implementation specification, provided that later work remains bounded by the
finite S2 objects.

`HALT-GOAL-DRIFT`

Result:
Not triggered. S2 did not become a philosophy survey, Sanskrit worship, logic
theory, DSL construction, implementation plan, or framework naming exercise.

## Pass Condition Check

| condition | result |
|---|---|
| S1 pass confirmed | pass |
| all required finite domains defined | pass |
| T1-T9 operationalized over finite fields | pass |
| S0 cases A-G have deterministic replay protocols | pass |
| consequence tests have outcomes and contrast outcomes | pass |
| anchors operationalized for toy use | pass |
| scope cost / lineage prevents free context laundering | pass |
| population state cannot promote by popularity alone | pass |
| Goodhart controls have concrete activation predicates | pass |
| oracle leakage audit detects no hidden semantic oracle | pass |
| CL mistake audit detects no repeated CL failures | pass |
| no forbidden downstream work or claim is made | pass |

## Remaining Limits

- S2 does not show that the toy specification can be implemented correctly.
- S2 does not show that any learner can use the specification.
- S2 does not show grounding, substrate, representation, or derivability.
- S2 does not show transfer from finite S0 cases to real language.
- S2 does not remove the need for later anti-oracle controls if the toy model is implemented.
