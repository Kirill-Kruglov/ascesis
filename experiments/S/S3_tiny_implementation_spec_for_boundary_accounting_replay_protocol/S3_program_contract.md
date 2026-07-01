# S3 Program Contract

This is a specification for a future tiny program only. It does not implement
code and does not permit code in S3.

## Program Type

The future program may be specified only as:

```text
boundary-accounting / replay engine
```

The future program must not be described or reported as:

```text
semantic engine
meaning generator
boundary generator
truth detector
grounding system
substrate prototype
```

## Contract

Input:

```text
finite S2-style case records with explicit field provenance
```

Process:

```text
validate finite domains;
reject forbidden oracle fields;
validate boundary-source provenance for every field;
apply T1-T9 in fixed replay order;
activate Goodhart flags;
record blocked transitions;
classify boundary sources;
compute allowed claim strength;
run mutation tests;
emit audit outputs.
```

Output:

```text
final status;
transition trace;
blocked transitions;
active Goodhart flags;
boundary-source provenance summary;
claim-strength downgrade;
oracle-leakage warnings;
CL-mistake warnings;
mutation-test results.
```

## Non-Goals

The future program must not:

- infer real-world truth;
- request human judgement at runtime;
- treat Sanskrit/Panini as a truth oracle;
- treat population agreement as truth;
- treat protective boundary as truth;
- treat human-authored fields as derived;
- treat toy outcome tokens as external truth contact;
- treat deterministic rule replay as semantic generation;
- produce substrate, derivability, grounding, representation, LLM-safety, or learner-evidence claims.

## Runtime Decision Types

The program may emit only audit decisions such as:

```text
ACCEPT_REPLAY_AUDIT
REJECT_SCHEMA_ERROR
REJECT_FORBIDDEN_ORACLE_FIELD
REJECT_PROVENANCE_MISSING
REJECT_FINITE_DOMAIN_ERROR
WARN_ORACLE_LEAKAGE
WARN_CL_MISTAKE
```

These runtime decisions are audit outcomes, not semantic truth values.
