# S3 Input Schema

The future program accepts finite S2-style records only. Every field must carry
boundary-source provenance from the exact allowed taxonomy.

## Allowed Boundary Sources

```text
FORM_BOUNDARY
CONSEQUENCE_BOUNDARY
VIABILITY_BOUNDARY
RULE_GENERATED_BOUNDARY
HUMAN_AUTHORED_BOUNDARY
POPULATION_BOUNDARY
UNKNOWN_OR_MIXED_BOUNDARY
```

## Required Record Shape

Every input record must contain:

```text
claim_id
expression_id
primitives
derivation_trace
initial_status
scope
assumptions
candidate_tests
candidate_outcomes
anchors
population_state
contradiction_links
extension_path_count
scope_cost
scope_lineage
consequence_delta
goodhart_flags_initial
attempted_transition
danger_condition
boundary_source_by_field
field_provenance
```

## Field Requirements

| field | required value shape | provenance requirement | notes |
|---|---|---|---|
| `claim_id` | finite identifier | `HUMAN_AUTHORED_BOUNDARY` or `UNKNOWN_OR_MIXED_BOUNDARY` | audit identifier only; never status lookup key |
| `expression_id` | finite S2 expression token | `FORM_BOUNDARY` plus provenance of assignment | may select finite expression fields; never final status |
| `primitives` | finite list from S2 primitive domain | `FORM_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | supports T1 only |
| `derivation_trace` | finite S2 trace token | `FORM_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | cannot promote beyond form/poetic by itself |
| `initial_status` | `UNINITIALIZED` only | `RULE_GENERATED_BOUNDARY` | future program must initialize through T1 |
| `scope` | finite S2 scope object | `HUMAN_AUTHORED_BOUNDARY`; possible `CONSEQUENCE_BOUNDARY` | scope origin must be explicit |
| `assumptions` | finite assumption tokens | `HUMAN_AUTHORED_BOUNDARY` | not truth evidence |
| `candidate_tests` | finite test tokens | `CONSEQUENCE_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | toy tests only unless later gate says otherwise |
| `candidate_outcomes` | finite outcome tokens | `CONSEQUENCE_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | toy outcomes only |
| `anchors` | finite anchor tokens | `CONSEQUENCE_BOUNDARY`, `POPULATION_BOUNDARY`, or `HUMAN_AUTHORED_BOUNDARY` | external contact token is not real contact by default |
| `population_state` | finite population object | `POPULATION_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | cannot imply truth |
| `contradiction_links` | finite links | `HUMAN_AUTHORED_BOUNDARY` / `CONSEQUENCE_BOUNDARY` | must identify scope/test overlap |
| `extension_path_count` | non-negative integer | `HUMAN_AUTHORED_BOUNDARY` | not future-meaning evidence by itself |
| `scope_cost` | finite integer / ordinal | `HUMAN_AUTHORED_BOUNDARY` / `VIABILITY_BOUNDARY` | blocks free context laundering |
| `scope_lineage` | present/absent finite token | `HUMAN_AUTHORED_BOUNDARY` | required for created scopes |
| `consequence_delta` | boolean | `CONSEQUENCE_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | required for non-free scope creation |
| `goodhart_flags_initial` | finite flag set | `VIABILITY_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | recomputed flags must also be reported |
| `attempted_transition` | finite transition token | `RULE_GENERATED_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | used for guard activation |
| `danger_condition` | boolean / finite reason tokens | `VIABILITY_BOUNDARY` / `HUMAN_AUTHORED_BOUNDARY` | triggers T7 when true |
| `boundary_source_by_field` | map field -> allowed source set | each source from allowed taxonomy | must cover every input field |
| `field_provenance` | map field -> provenance record | not empty for every field | includes source, author/origin token, and audit note |

## Provenance Rule

The future program must reject a record if:

```text
any required field is absent;
any field has no boundary_source_by_field entry;
any boundary source is outside the allowed taxonomy;
any field_provenance entry is empty;
boundary_source_by_field and field_provenance disagree;
initial_status is anything except UNINITIALIZED.
```

## Forbidden Input Fields

The future program must reject any record containing:

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

Any forbidden field is an oracle leakage warning and a blocking schema error.

## Anti-Lookup Input Rule

`claim_id` and `expression_id` may identify the record and select finite
domain tokens. They must never directly determine `final_status`,
`allowed_claim_strength`, or `dominant_boundary_source`.
