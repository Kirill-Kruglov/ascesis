# S2 Toy Model Domains

This file defines finite toy domains only. The labels are specification tokens,
not evidence of truth, grounding, substrate, derivability, or learning.

## Status Domain

The final status domain is exactly:

```text
FORMED
POETIC
SUSPENDED
LOCAL
STABLE
KILLED
DANGEROUS
```

## Expression Domain

```text
E = {
  liquid_powder,
  hereditary_infertility,
  square_circle,
  everything_true_in_context,
  x_related_to_y_somehow,
  translucent_causal_sweetness_field,
  light_wave,
  light_particle
}
```

No helper expressions are added. For Case G, `light_wave` and `light_particle`
are linked by a pair relation rather than by adding a new expression.

## Primitive Domain

```text
P = {
  liquid,
  powder,
  infertility,
  inheritance,
  square,
  circle,
  context,
  relation,
  sweetness_field,
  light,
  wave,
  particle,
  true_claim,
  x,
  y
}
```

Primitive membership admits a formation trace only. It does not imply semantic
admissibility beyond `FORMED` or `POETIC`.

## Derivation Trace Domain

```text
D = {
  COMPOSITION,
  PREDICATION,
  META_CLAIM,
  RELATION_CLAIM,
  PSEUDO_TERM,
  MODEL_PAIR
}
```

Trace rules:

| trace | toy condition | maximum status from trace alone |
|---|---|---|
| `COMPOSITION` | expression combines two primitives | `FORMED` |
| `PREDICATION` | one primitive is predicated of another | `FORMED` |
| `META_CLAIM` | expression asserts a rule about claims or contexts | `FORMED` |
| `RELATION_CLAIM` | expression asserts a relation without its tests | `FORMED` |
| `PSEUDO_TERM` | expression introduces a technical-looking term | `FORMED` or `POETIC` |
| `MODEL_PAIR` | two model predicates are paired under possible scope split | `FORMED` |

## Scope Domain

Each scope has finite fields:

```text
scope_id
domain
model
assumptions
allowed_tests
scope_cost
lineage_required
```

| scope_id | domain | model | assumptions | allowed_tests | scope_cost | lineage_required |
|---|---|---|---|---|---:|---|
| `ORDINARY_MATERIAL` | material | default material ontology | `ordinary_liquid_not_powder` | `T_FLOW_GRANULARITY`, `T_PHASE_BEHAVIOR` | 0 | false |
| `FUTURE_MATERIAL_OBJECT_CLASS` | material | explicit new object class | `new_material_class_possible` | `T_FLOW_GRANULARITY`, `T_PHASE_BEHAVIOR` | 2 | true |
| `ORDINARY_REPRODUCTION` | reproduction | unaided reproduction | `absolute_infertility_means_no_reproduction`, `inheritance_requires_lineage` | `T_LINEAGE_MECHANISM`, `T_REPRODUCTION_ROUTE` | 0 | false |
| `GENETIC_PREDISPOSITION` | reproduction | inherited risk mechanism | `inheritance_requires_lineage` | `T_LINEAGE_MECHANISM` | 2 | true |
| `ASSISTED_REPRODUCTION` | reproduction | intervention-mediated lineage | `assisted_reproduction_possible`, `inheritance_requires_lineage` | `T_LINEAGE_MECHANISM`, `T_REPRODUCTION_ROUTE` | 2 | true |
| `EUCLIDEAN_GEOMETRY` | geometry | ordinary Euclidean commitments | `euclidean_square_circle_incompatible` | `T_GEOMETRY_AXIOMS` | 0 | false |
| `METAPHORICAL_LANGUAGE` | language | figurative use | `naming_is_not_meaning` | `T_TERM_OPERATIONAL_ROLE` | 1 | true |
| `NONSTANDARD_GEOMETRY` | geometry | changed formal commitments | `changed_geometry_requires_axioms` | `T_GEOMETRY_AXIOMS` | 3 | true |
| `META_SEMANTIC_RULE` | semantic policy | context creation rule | `contexts_are_not_free_truth_makers` | `T_CONTEXT_COST` | 0 | false |
| `UNCONSTRAINED_RELATION` | relation | unspecified relation | `relation_must_be_typed` | `T_RELATION_DISCRIMINATION` | 0 | false |
| `SPECIFIED_RELATION` | relation | typed relation | `relation_must_be_typed` | `T_RELATION_DISCRIMINATION` | 1 | true |
| `PSEUDO_TECHNICAL_TERM` | term | named pseudo-technical role | `naming_is_not_meaning` | `T_TERM_OPERATIONAL_ROLE` | 0 | false |
| `WAVE_EXPERIMENTAL_SCOPE` | light model | wave setup | `wave_tests_differ_from_particle_tests` | `T_WAVE_INTERFERENCE` | 1 | true |
| `PARTICLE_EXPERIMENTAL_SCOPE` | light model | particle setup | `wave_tests_differ_from_particle_tests` | `T_PARTICLE_DETECTION` | 1 | true |

Scope creation rule:

```text
new non-default scope is admissible only if
  scope_cost > 0
  and lineage_required == true
  and a consequence_delta test is present.
```

## Assumption Domain

```text
A = {
  ordinary_liquid_not_powder,
  new_material_class_possible,
  absolute_infertility_means_no_reproduction,
  inheritance_requires_lineage,
  assisted_reproduction_possible,
  euclidean_square_circle_incompatible,
  changed_geometry_requires_axioms,
  contexts_are_not_free_truth_makers,
  relation_must_be_typed,
  naming_is_not_meaning,
  wave_tests_differ_from_particle_tests,
  no_explosion_from_local_dualism,
  population_is_not_truth
}
```

Assumptions are finite tokens. They are used to check compatibility and rule
preconditions inside the toy model; they are not evidence that the assumption is
true outside the toy model.

## Test Domain

Each test has finite fields:

```text
test_id
scope_allowed
expected_outcomes
contrast_outcomes
failure_condition
```

| test_id | scope_allowed | expected_outcomes | contrast_outcomes | failure_condition |
|---|---|---|---|---|
| `T_FLOW_GRANULARITY` | `ORDINARY_MATERIAL`, `FUTURE_MATERIAL_OBJECT_CLASS` | `DISTINGUISHES_FROM_LIQUID_AND_POWDER` | `COLLAPSES_TO_METAPHOR` | `OPERATIONAL_ROLE_ABSENT` |
| `T_PHASE_BEHAVIOR` | `ORDINARY_MATERIAL`, `FUTURE_MATERIAL_OBJECT_CLASS` | `DISTINGUISHES_FROM_LIQUID_AND_POWDER` | `COLLAPSES_TO_METAPHOR` | `OPERATIONAL_ROLE_ABSENT` |
| `T_LINEAGE_MECHANISM` | `ORDINARY_REPRODUCTION`, `GENETIC_PREDISPOSITION`, `ASSISTED_REPRODUCTION` | `MECHANISM_SPECIFIED` | `MECHANISM_ABSENT` | `MECHANISM_ABSENT` |
| `T_REPRODUCTION_ROUTE` | `ORDINARY_REPRODUCTION`, `ASSISTED_REPRODUCTION` | `ROUTE_SPECIFIED` | `ROUTE_ABSENT` | `ROUTE_ABSENT` |
| `T_GEOMETRY_AXIOMS` | `EUCLIDEAN_GEOMETRY`, `NONSTANDARD_GEOMETRY` | `AXIOMS_COMPATIBLE` | `AXIOMS_INCOMPATIBLE` | `AXIOMS_INCOMPATIBLE` |
| `T_CONTEXT_COST` | `META_SEMANTIC_RULE` | `CONTEXT_COST_PRESENT` | `CONTEXT_COST_ABSENT` | `CONTEXT_COST_ABSENT` |
| `T_RELATION_DISCRIMINATION` | `UNCONSTRAINED_RELATION`, `SPECIFIED_RELATION` | `RELATION_TYPED` | `RELATION_UNSPECIFIED` | `RELATION_UNSPECIFIED` |
| `T_TERM_OPERATIONAL_ROLE` | `PSEUDO_TECHNICAL_TERM`, `METAPHORICAL_LANGUAGE` | `OPERATIONAL_ROLE_PRESENT` | `OPERATIONAL_ROLE_ABSENT` | `OPERATIONAL_ROLE_ABSENT` |
| `T_WAVE_INTERFERENCE` | `WAVE_EXPERIMENTAL_SCOPE` | `WAVE_PATTERN_OBSERVED` | `WAVE_PATTERN_ABSENT` | `WAVE_PATTERN_ABSENT` |
| `T_PARTICLE_DETECTION` | `PARTICLE_EXPERIMENTAL_SCOPE` | `PARTICLE_EVENT_OBSERVED` | `PARTICLE_EVENT_ABSENT` | `PARTICLE_EVENT_ABSENT` |

## Outcome Domain

```text
O = {
  UNTESTED,
  DISTINGUISHES_FROM_LIQUID_AND_POWDER,
  COLLAPSES_TO_METAPHOR,
  MECHANISM_SPECIFIED,
  MECHANISM_ABSENT,
  ROUTE_SPECIFIED,
  ROUTE_ABSENT,
  AXIOMS_COMPATIBLE,
  AXIOMS_INCOMPATIBLE,
  CONTEXT_COST_PRESENT,
  CONTEXT_COST_ABSENT,
  RELATION_TYPED,
  RELATION_UNSPECIFIED,
  OPERATIONAL_ROLE_PRESENT,
  OPERATIONAL_ROLE_ABSENT,
  WAVE_PATTERN_OBSERVED,
  WAVE_PATTERN_ABSENT,
  PARTICLE_EVENT_OBSERVED,
  PARTICLE_EVENT_ABSENT,
  ADVERSARIAL_PARAPHRASE_SURVIVED,
  ADVERSARIAL_PARAPHRASE_FAILED
}
```

An outcome counts as passed for T5 only if it is an expected outcome of a test
in the declared scope and at least one contrast outcome is excluded. `UNTESTED`
cannot promote a claim to `LOCAL` or `STABLE`.

## Anchor Domain

```text
ANCHOR = {
  FORMAL_ANCHOR,
  OPERATIONAL_ANCHOR,
  EXTERNAL_ANCHOR,
  ADVERSARIAL_PARAPHRASE_ANCHOR,
  POPULATION_STABILITY_ANCHOR
}
```

Toy presence conditions:

| anchor | present iff | absent iff |
|---|---|---|
| `FORMAL_ANCHOR` | a finite scope supplies explicit axioms or formal commitments and `T_GEOMETRY_AXIOMS` is declared | no formal test is declared |
| `OPERATIONAL_ANCHOR` | at least one declared test has expected and contrast outcomes | tests are empty or only `UNTESTED` |
| `EXTERNAL_ANCHOR` | a finite external check token is supplied by the case table | no external check token is supplied |
| `ADVERSARIAL_PARAPHRASE_ANCHOR` | outcome includes `ADVERSARIAL_PARAPHRASE_SURVIVED` | outcome includes `ADVERSARIAL_PARAPHRASE_FAILED` or is untested |
| `POPULATION_STABILITY_ANCHOR` | population usage is `STABLE_USAGE` or `CONTESTED_USAGE` and paraphrase is `SURVIVED` | population is popularity-only or paraphrase is missing |

At least one non-population anchor is required before `STABLE`. Population
stability alone is insufficient.

## Population Domain

```text
agents = {A1, A2, A3}
usage_states = {UNUSED, USED_ONCE, STABLE_USAGE, CONTESTED_USAGE}
paraphrase_states = {NOT_TESTED, SURVIVED, FAILED}
minority_states = {PRESERVED, ERASED, NOT_APPLICABLE}
```

Population state object:

```text
PopulationState := {
  agents_subset,
  usage_state,
  paraphrase_state,
  minority_state
}
```

Population rule:

```text
population_state may support T5 only if
  usage_state in {STABLE_USAGE, CONTESTED_USAGE}
  and paraphrase_state == SURVIVED
  and minority_state != ERASED
  and consequence tests and non-population anchors are already present.
```

## Goodhart Flag Domain

Use exactly:

```text
VOLUME_PROXY
COHERENCE_PROXY
CONTRADICTION_MINIMIZATION_PROXY
CONTEXT_PROLIFERATION_PROXY
GRAMMAR_PROXY
POPULATION_PROXY
```

Activation predicates are defined in `S2_goodhart_control_protocol.md`.
