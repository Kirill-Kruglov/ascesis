# S3 Failure Analysis

## S3-FAIL-LOOKUP-TABLE-RISK

Result:
Not triggered.

Reason:
The spec bans `claim_id -> final_status` and `expression_id -> final_status`
maps, rejects final-status input fields, requires status to arise from T1-T9
preconditions, and defines M1-M6 mutation tests that detect lookup behavior.

Residual risk:
Actual S4 code must make the absence of lookup maps inspectable.

## S3-FAIL-PROVENANCE-MISSING

Result:
Not triggered.

Reason:
Every required input field must have `boundary_source_by_field` and
`field_provenance`; missing or invalid provenance rejects the record.

Residual risk:
Provenance can be present but low quality. S4 must expose provenance content in
audit output.

## S3-FAIL-MUTATION-TESTS-INSUFFICIENT

Result:
Not triggered.

Reason:
M1-M6 test extension-path, context laundering, relation typing, local dualism,
population-only stability, and expression-name swaps. These catch direct lookup
and oracle behavior.

Residual risk:
The suite is minimal and tailored to S0 cases; later broader suites may be
needed.

## S3-FAIL-BOUNDARY-GENERATOR-OVERCLAIM

Result:
Not triggered.

Reason:
The program is specified only as a boundary-accounting / replay engine and is
forbidden from reporting itself as a semantic or boundary generator.

Residual risk:
User-facing summaries after implementation must preserve this wording.

## S3-FAIL-CLAIM-STRENGTH-DOWNGRADE-MISSING

Result:
Not triggered.

Reason:
The output schema requires `allowed_claim_strength`, `forbidden_overclaims`,
and `downgrade_reason`; downgrade logic caps every source class.

Residual risk:
Actual code must make downgrade logic deterministic and tested.

## S3-FAIL-ORACLE-LEAKAGE-RISK

Result:
Not triggered.

Reason:
Forbidden input fields, runtime human judgement, real-world truth lookup,
Sanskrit truth oracle, population-as-truth, protective-as-truth,
human-authored-as-derived, toy-outcome-as-external-truth, and
rule-replay-as-semantic-generation all have warnings or blocking errors.

Residual risk:
Hidden defaults in S4 could reintroduce oracle labels if not audited.

## S3-FAIL-REPEATS-CL-MISTAKES

Result:
Not triggered.

Reason:
The spec warns against preconditions as substrate, hand-authored fields as
learner evidence, rule priors as learning, viability as derivability,
premature representation/LLM work, and toy replay as world transfer.

Residual risk:
Future branches must still supply learner evidence before representation or
derivability work.

## S3-INCONCLUSIVE

Result:
Not selected.

Reason:
The spec is precise enough for a later tiny implementation task because it
defines program contract, schemas, fixed replay order, anti-lookup controls,
mutation tests, warnings, and downgrade logic.

## HALT-GOAL-DRIFT

Result:
Not triggered.

Reason:
S3 did not implement code, run tests, perform experiments, write a philosophy
essay, name a framework, run Sanskrit work, train a learner, or make downstream
claims.

## Pass Condition Check

| condition | result |
|---|---|
| B0 pass confirmed | pass |
| Program specified only as boundary-accounting / replay engine | pass |
| Input schema requires provenance for every field | pass |
| Forbidden oracle fields rejected | pass |
| Output schema includes required audit fields | pass |
| Replay algorithm uses T1-T9 fixed order | pass |
| claim_id / expression_id cannot determine status directly | pass |
| M1-M6 mutation tests defined | pass |
| Oracle leakage controls explicit | pass |
| CL mistake controls explicit | pass |
| Claim-strength downgrade logic explicit | pass |
| No implementation, experiment, training, or downstream claim | pass |
