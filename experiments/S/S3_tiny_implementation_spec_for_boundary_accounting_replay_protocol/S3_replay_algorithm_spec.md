# S3 Replay Algorithm Spec

This is a deterministic algorithm specification for a future tiny
boundary-accounting / replay engine. It is not code.

## Fixed Replay Steps

The future program must execute these steps in order:

1. Validate record schema.
2. Reject forbidden oracle fields.
3. Validate finite domain membership.
4. Validate provenance for every field.
5. Initialize status only through T1.
6. Apply T7 danger predicates.
7. Apply T6 declared-scope kill predicates.
8. Apply T2 poetic rule.
9. Apply T3 suspension rule.
10. Apply T4 localization rule.
11. Apply T8 local dualism rule.
12. Apply T5 stability rule.
13. Apply T9 downgrade rule only if prior `STABLE` exists.
14. Compute active Goodhart flags.
15. Compute boundary-source provenance summary.
16. Compute allowed claim strength.
17. Emit audit record.

## Rule Application Requirements

T1 Birth:

```text
status may become FORMED only if expression_id, derivation_trace, and
primitives are finite-domain members.
```

T7 Dangerous:

```text
if danger_condition == true or Goodhart predicates imply laundering /
proxy abuse, status becomes DANGEROUS and T5 is blocked.
```

T6 Killed:

```text
if declared-scope failure condition is observed, or same-scope contradiction
has no repair path, status becomes KILLED.
```

T2 Poetic:

```text
if status == FORMED, poetic marker / pseudo-term condition is present, and no
operational upgrade is attempted, status may become POETIC.
```

T3 Suspended:

```text
if status in {FORMED, POETIC}, contradiction/underdefined ontology is present,
extension_path_count > 0, and no danger condition is active, status may become
SUSPENDED.
```

T4 Local:

```text
if status == SUSPENDED, scope and assumptions are explicit, candidate tests
and contrast outcomes are present, consequence_delta == true, created scopes
have cost and lineage, and blocking Goodhart flags are absent, status may
become LOCAL.
```

T8 Local dualism:

```text
if paired claims are LOCAL, scopes/tests differ, contradiction links are
explicit, consequence differences are preserved, and explosion is blocked,
the pair may remain LOCAL.
```

T5 Stable:

```text
if status == LOCAL, all required toy tests have expected outcomes and contrast
outcomes, contradiction is contained, adversarial paraphrase survives,
non-population anchor exists, population conditions pass, and no Goodhart flag
is active, status may become STABLE.
```

T9 Stable downgrade:

```text
if a prior STABLE exists and later finite failure tokens appear, downgrade
according to the specified failure token.
```

## Anti-Lookup Controls

The future program must enforce:

1. No dictionary mapping `claim_id -> final_status`.
2. No dictionary mapping `expression_id -> final_status`.
3. No `final_status` or `expected_final_status` in input.
4. Replay produces status only from rule preconditions and finite fields.
5. Mutation tests change fields while keeping `expression_id` constant and verify status changes.
6. Mutation tests swap `expression_id` while preserving decisive fields and verify status follows fields, not expression name.

## Trace Requirements

For every transition attempt, the trace must include:

```text
rule_id
preconditions_checked
fields_consulted
boundary_sources_consulted
status_before
status_after
blocked_by
warning_ids
```

## Lookup Failure Condition

If any output status can be reproduced by a direct `claim_id` or
`expression_id` lookup without consulting decisive fields, the implementation
would fail S3 as:

```text
S3-FAIL-LOOKUP-TABLE-RISK
```
