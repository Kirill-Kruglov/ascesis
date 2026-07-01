# S1 Microformal Schema

## Claim Object

```text
Claim := {
  id,
  expression,
  derivation_trace,
  assumptions,
  scope,
  status,
  consequence_obligations,
  contradiction_links,
  goodhart_flags,
  population_state,
  anchors
}
```

Field constraints:

- `id`: stable identifier for the claim.
- `expression`: surface expression or claim pair.
- `derivation_trace`: source primitives / terms, formation rules, transformations, and lineage.
- `assumptions`: typed assumption set used by the claim.
- `scope`: typed scope object.
- `status`: exactly one final status from the S0 status set.
- `consequence_obligations`: structured tests required before `LOCAL` or `STABLE`.
- `contradiction_links`: scoped links to claims or commitments that conflict under overlapping assumptions/tests.
- `goodhart_flags`: active proxy-failure flags.
- `population_state`: usage/stabilization record; never sufficient by itself.
- `anchors`: formal or external anchors; required for `STABLE`.

## Status Set

Final statuses are exactly:

```text
FORMED
POETIC
SUSPENDED
LOCAL
STABLE
KILLED
DANGEROUS
```

No Boolean truth value is a status. Helper labels such as `vacuous`, `metaphor`,
or `scope_split_required` may appear only as annotations.

## Derivation Trace

```text
DerivationTrace := {
  source_primitives,
  formation_rules,
  transformations,
  lineage
}
```

Constraint:

```text
derivation_trace != empty
```

can admit `FORMED`, and with evocative use can support `POETIC`. It cannot by
itself promote a claim to `LOCAL` or `STABLE`.

## Scope Object

```text
Scope := {
  domain,
  model,
  scale,
  context,
  observer_or_agent,
  intervention_class,
  assumption_set
}
```

A claim without explicit scope cannot become `LOCAL` or `STABLE`.

Context creation is not free. A new scope must add lineage, assumptions, and a
consequence delta. Otherwise `CONTEXT_PROLIFERATION_PROXY` fires.

## Assumption Graph

```text
AssumptionGraph := {
  nodes: assumptions,
  edges: supports | conflicts | refines | scope-splits,
  active_set,
  conflict_boundaries
}
```

Contradiction is evaluated over overlapping active assumption sets, not globally.

## Consequence Obligation

```text
ConsequenceObligation := {
  claim_id,
  scope_id,
  assumptions,
  test,
  expected_outcome,
  contrast_outcome,
  failure_condition
}
```

Structural rule:

```text
if claim C holds under scope S and assumptions A,
then admissible test T should distinguish expected outcome O
from at least one alternative O'.
```

No consequence obligation means no `LOCAL` or `STABLE`.

## Contradiction Relation

```text
Contradiction(C1, C2) iff
  C1 and C2 assert incompatible commitments
  under overlapping scope
  and shared assumptions
  and shared consequence tests.
```

A contradiction produces one or more of:

```text
quarantine
scope split
assumption split
weakening
kill
danger flag
```

It never produces arbitrary explosion.

## Goodhart Flags

```text
VOLUME_PROXY
COHERENCE_PROXY
CONTRADICTION_MINIMIZATION_PROXY
CONTEXT_PROLIFERATION_PROXY
GRAMMAR_PROXY
POPULATION_PROXY
```

A claim with any active Goodhart flag cannot become `STABLE`.

## Anchor Types

```text
formal_anchor
external_anchor
operational_anchor
adversarial_paraphrase_anchor
population_stability_anchor
```

Population stabilization is never sufficient alone.

## Population State

```text
PopulationState := {
  users,
  usage_stability,
  adversarial_paraphrase_survival,
  minority_hypotheses_preserved,
  agreement_without_consequence_flag
}
```

Population agreement can support `STABLE` only when consequence obligations,
contradiction containment, and anchors are also present.
