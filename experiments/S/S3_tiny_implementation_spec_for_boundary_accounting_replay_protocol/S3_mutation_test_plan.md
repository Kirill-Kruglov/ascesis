# S3 Mutation Test Plan

The future implementation task must include these mutation tests. The tests are
specified here only; S3 does not run them.

## Test Requirements

Each mutation test must record:

```text
test_id
original_record
mutation
expected_status_change_or_blocker
lookup_failure_detected_if
oracle_failure_detected_if
claim_strength_expected
```

## M1 - Remove extension path from A

Original:

```text
liquid_powder -> SUSPENDED
```

Mutation:

```text
extension_path_count = 0
new_material_class_possible removed
```

Expected:

```text
SUSPENDED should no longer be justified.
T3 blocked.
T6 or FORM/POETIC fallback must be considered from remaining fields.
```

Lookup failure detected if:

```text
expression_id == liquid_powder still forces SUSPENDED.
```

Oracle failure detected if:

```text
runtime says future meaning is possible without extension-path fields.
```

## M2 - Add free context to C

Original:

```text
square_circle under EUCLIDEAN_GEOMETRY -> KILLED
```

Mutation:

```text
new_scope_requested = true
scope_cost = 0
scope_lineage = absent
consequence_delta = false
```

Expected:

```text
CONTEXT_PROLIFERATION_PROXY activates.
DANGEROUS should be considered before any context-rescue LOCAL.
```

Lookup failure detected if:

```text
expression_id == square_circle always forces KILLED and ignores context laundering fields.
```

Oracle failure detected if:

```text
runtime uses "obvious nonsense" rather than finite context/provenance fields.
```

## M3 - Type the relation in E

Original:

```text
X related to Y somehow -> FORMED
```

Mutation:

```text
relation_type = SPECIFIED
candidate_tests include T_RELATION_DISCRIMINATION
candidate_outcomes include RELATION_TYPED
consequence_delta = true
```

Expected:

```text
T4 may become possible if other LOCAL preconditions are satisfied.
VOLUME_PROXY should no longer block solely because relation is unspecified.
```

Lookup failure detected if:

```text
expression_id == x_related_to_y_somehow always forces FORMED.
```

Oracle failure detected if:

```text
runtime asks a human whether the typed relation really means anything.
```

## M4 - Remove scope distinction from G

Original:

```text
wave / particle -> LOCAL dualism
```

Mutation:

```text
same scope and same tests for both claims
```

Expected:

```text
T8 blocked.
Contradiction containment must fail to T6 or T7 depending on finite fields.
```

Lookup failure detected if:

```text
expression_ids light_wave/light_particle always force LOCAL dualism.
```

Oracle failure detected if:

```text
runtime uses outside physics knowledge rather than scope/test fields.
```

## M5 - Add population-only stability to F

Original:

```text
pseudo-term -> POETIC
```

Mutation:

```text
population_state = STABLE_USAGE
anchors = {POPULATION_STABILITY_ANCHOR}
no non-population anchor
no operational role
```

Expected:

```text
POPULATION_PROXY blocks T5.
STABLE forbidden.
allowed claim strength remains FORM_ONLY / BOUNDARY_ACCOUNTING.
```

Lookup failure detected if:

```text
expression_id == translucent_causal_sweetness_field forces POETIC without reporting population proxy.
```

Oracle failure detected if:

```text
population agreement is reported as truth.
```

## M6 - Swap expression names with decisive fields preserved

Mutation:

```text
Use expression_id = square_circle
but fields from Case E relation-unspecified replay.
```

Expected:

```text
Status follows decisive fields, not expression name.
The output should not become KILLED solely from expression_id.
Finite-domain inconsistency warnings may be emitted if primitives/trace/scope
do not match expression_id, but status must not be assigned by expression name.
```

Lookup failure detected if:

```text
expression_id == square_circle forces KILLED despite relation-unspecified fields.
```

Oracle failure detected if:

```text
runtime uses ordinary-language judgement about square circles.
```

## Suite Pass Condition

The mutation suite is sufficient only if it catches:

- direct `claim_id` lookup;
- direct `expression_id` lookup;
- forbidden final-status input;
- runtime human semantic judgement;
- population-as-truth;
- protective-as-truth;
- grammar-as-meaning;
- rule-replay-as-semantic-generation.
