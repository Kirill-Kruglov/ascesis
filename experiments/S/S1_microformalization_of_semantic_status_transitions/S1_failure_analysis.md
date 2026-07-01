# S1 Failure Analysis

## IC1 — Status Overlap

check:
Can a claim be both `STABLE` and `DANGEROUS`?

result:
Pass. `DANGEROUS` is an active blocker for T5. A claim with active Goodhart or explosion flags cannot be `STABLE`.

remaining risk:
Implementation must enforce single final status plus archived status history.

## IC2 — Grammar Bypass

check:
Can derivation trace alone produce `LOCAL` or `STABLE`?

result:
Pass. T1 grants only `FORMED`; T2 may grant `POETIC`; T4 and T5 require scope, assumptions, consequence obligations, and guard clearance.

remaining risk:
A future toy model must not encode grammar score as a hidden consequence score.

## IC3 — Context Laundering

check:
Can a new scope save any contradiction?

result:
Pass. T4 and T8 require scope lineage, assumptions, consequence delta, and no `CONTEXT_PROLIFERATION_PROXY` flag. Case D is `DANGEROUS`.

remaining risk:
The toy model must define cost/lineage enough to prevent cheap context splitting.

## IC4 — Vacuity

check:
Can a claim with no relation type or consequence become `STABLE`?

result:
Pass. T4 and T5 are blocked without consequence obligations. `VOLUME_PROXY` blocks vacuous claims such as Case E.

remaining risk:
The toy model must make "contrast outcome" non-empty.

## IC5 — Dogmatism

check:
Can all contradictions be killed immediately?

result:
Pass. T3 preserves underdefined/future-meaning claims as `SUSPENDED`, and T8 permits scoped local dualism.

remaining risk:
The toy model must still allow T6 for declared-scope failures such as Euclidean square circle.

## IC6 — Explosion

check:
Can local contradiction imply arbitrary claims?

result:
Pass. Contradiction links produce quarantine, scope split, assumption split, weakening, kill, or danger flag. They do not create arbitrary inference.

remaining risk:
The toy model must not include an unrestricted inference rule from contradictory local claims.

## Decision Vocabulary Failure Modes

`S1-FAIL-AD-HOC-CLASSIFICATION` is avoided because cases replay through T1-T9 and guards.

`S1-FAIL-STATUS-SYSTEM-INCOHERENT` is avoided by single final status, DANGEROUS blocking STABLE, and scoped KILLED.

`S1-FAIL-CONSEQUENCE-OBLIGATION-UNDEFINED` is avoided by defining test, expected outcome, contrast outcome, and failure condition.

`S1-FAIL-CONTRADICTION-CONTAINMENT-UNDEFINED` is avoided by scoped contradiction relation and non-explosive repair outputs.

`S1-FAIL-GOODHART-GUARDS-UNFORMALIZED` is avoided because each guard has trigger, blocked transition, repair, activating case, and danger condition.

`S1-FAIL-GRAMMAR-AS-MEANING` is avoided because derivation trace cannot promote beyond `FORMED`/`POETIC`.

`S1-INCONCLUSIVE` is avoided at the analytic level because the schema is precise enough for a toy-model specification, but not for implementation.
