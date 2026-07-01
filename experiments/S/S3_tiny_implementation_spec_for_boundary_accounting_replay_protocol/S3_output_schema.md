# S3 Output Schema

The future program must emit an audit record for each replay. Output status is
an audit result of T1-T9 over finite fields, not a truth label.

## Required Output Fields

```text
claim_id
expression_id
final_status
transition_trace
blocked_transitions
active_goodhart_flags
boundary_sources_used
dominant_boundary_source
allowed_claim_strength
forbidden_overclaims
downgrade_reason
oracle_leakage_warnings
cl_mistake_warnings
mutation_test_results
runtime_decision
```

## Output Field Specification

| field | required content |
|---|---|
| `claim_id` | copied identifier from input |
| `expression_id` | copied expression token from input |
| `final_status` | one of `FORMED`, `POETIC`, `SUSPENDED`, `LOCAL`, `STABLE`, `KILLED`, `DANGEROUS`; produced only by transition trace |
| `transition_trace` | ordered list of attempted T1-T9 rules, precondition results, status changes, and reasons |
| `blocked_transitions` | list of blocked rule IDs and finite blocker fields |
| `active_goodhart_flags` | recomputed flags plus initial flags, with predicate reason |
| `boundary_sources_used` | set of boundary sources actually consulted in rule decisions |
| `dominant_boundary_source` | conservative dominant source: `HUMAN_AUTHORED_BOUNDARY` dominates when decisive fields are authored |
| `allowed_claim_strength` | one or more allowed B0 strength levels after downgrade |
| `forbidden_overclaims` | always includes `RULE_GENERATED_CONTENT`, `DERIVATION_EVIDENCE`, `SUBSTRATE_CLAIM` in S3 |
| `downgrade_reason` | explanation of why stronger claim levels are blocked |
| `oracle_leakage_warnings` | warning list from oracle controls |
| `cl_mistake_warnings` | warning list from CL mistake controls |
| `mutation_test_results` | pass/fail/warn results for M1-M6 when mutation suite is run |
| `runtime_decision` | audit decision such as accept/reject/warn |

## Claim-Strength Levels

Allowed output values are from:

```text
FORM_ONLY
BOUNDARY_ACCOUNTING
TOY_REPLAY_DETERMINISTIC
TOY_CONSEQUENCE_PROTOCOL
VIABILITY_SHIELD
EXTERNAL_CONTACT_REQUIRED
RULE_GENERATED_CONTENT
DERIVATION_EVIDENCE
SUBSTRATE_CLAIM
```

In S3, the future program must never place these in `allowed_claim_strength`:

```text
RULE_GENERATED_CONTENT
DERIVATION_EVIDENCE
SUBSTRATE_CLAIM
```

They must appear in `forbidden_overclaims` unless a later non-S3 gate explicitly
changes the claim-strength policy.

## Downgrade Logic

The future program must apply these caps:

```text
If dominant boundary source is FORM_BOUNDARY:
  allowed <= FORM_ONLY.

If source includes HUMAN_AUTHORED_BOUNDARY:
  allowed <= BOUNDARY_ACCOUNTING or TOY_REPLAY_DETERMINISTIC.

If source includes CONSEQUENCE_BOUNDARY only as toy tokens:
  allowed <= TOY_CONSEQUENCE_PROTOCOL.

If source is VIABILITY_BOUNDARY:
  allowed <= VIABILITY_SHIELD with caveat.

If external contact is required but absent:
  allowed includes EXTERNAL_CONTACT_REQUIRED, not DERIVATION_EVIDENCE.

If RULE_GENERATED_BOUNDARY processes supplied fields:
  allowed <= TOY_REPLAY_DETERMINISTIC.
```

If multiple sources are used, the output must choose the most conservative cap
and record the downgrade reason.

## Warning-to-Decision Rule

The future program must set:

```text
runtime_decision = REJECT_FORBIDDEN_ORACLE_FIELD
```

when forbidden input fields are present.

It must set:

```text
runtime_decision = WARN_ORACLE_LEAKAGE
```

when a non-blocking oracle leakage risk is detected.

It must set:

```text
runtime_decision = WARN_CL_MISTAKE
```

when a CL mistake warning is present.
