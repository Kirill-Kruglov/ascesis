# S3 Oracle Leakage Controls

The future program must emit warnings or blocking errors for oracle leakage and
CL mistake patterns. These controls are part of the specification only.

## Oracle Leakage Warnings

Emit `FORBIDDEN_INPUT_FIELD` and reject the record if any forbidden field
appears:

```text
final_status
expected_final_status
future_meaning_possible
obvious_nonsense
inside_boundary
truth_label
semantic_label
safe_label_as_truth
derived_label
substrate_label
```

Emit `DIRECT_ID_STATUS_LOOKUP` if:

```text
claim_id or expression_id determines status directly.
```

Emit `RUNTIME_HUMAN_JUDGEMENT` if:

```text
the program requests a human to decide what a claim really means during replay.
```

Emit `REAL_WORLD_TRUTH_LOOKUP` if:

```text
the program performs external truth lookup or real-world fact lookup.
```

Emit `SANSKRIT_TRUTH_ORACLE` if:

```text
Sanskrit/Panini/derivational well-formedness is used as truth or semantic success.
```

Emit `POPULATION_AS_TRUTH` if:

```text
population agreement or stable usage is reported as truth or promotes without consequences.
```

Emit `PROTECTIVE_AS_TRUTH` if:

```text
VIABILITY_BOUNDARY or safety/protective rejection is reported as truth.
```

Emit `HUMAN_AUTHORED_AS_DERIVED` if:

```text
HUMAN_AUTHORED_BOUNDARY fields are reported as derived evidence.
```

Emit `TOY_OUTCOME_AS_EXTERNAL_TRUTH` if:

```text
toy outcome token is reported as external truth contact.
```

Emit `RULE_REPLAY_AS_SEMANTIC_GENERATION` if:

```text
RULE_GENERATED_BOUNDARY replay is reported as semantic generation or boundary generation.
```

## CL Mistake Warnings

Emit `PRECONDITION_AS_SUBSTRATE` if:

```text
finite fields, safe ledgers, admission decisions, or test preconditions are reported as substrate evidence.
```

Emit `HAND_AUTHORED_AS_LEARNER_EVIDENCE` if:

```text
human-authored fields are reported as learner evidence.
```

Emit `RULE_PRIOR_AS_LEARNING` if:

```text
rule-family behavior is reported as learning evidence.
```

Emit `VIABILITY_AS_DERIVABILITY` if:

```text
safe/viability boundary is reported as derivability evidence.
```

Emit `REPRESENTATION_WORK_PREMATURE` if:

```text
representation, LLM, substrate, or derivability work is enabled before learner evidence.
```

Emit `TOY_REPLAY_AS_WORLD_TRANSFER` if:

```text
toy replay is reported as transferring to real language or real world without a transfer gate.
```

## Blocking Rule

Any oracle leakage warning or CL mistake warning must block stronger downstream
claims. It may still allow an audit record to be emitted if the schema itself
is valid, but the output must include the warning and downgrade the claim
strength.

## Required Output Integration

The future program must place warnings in:

```text
oracle_leakage_warnings
cl_mistake_warnings
downgrade_reason
runtime_decision
```

Warnings must be visible in normal output, not hidden in logs.
