# S2 Goodhart Control Protocol

Each activation predicate is over finite toy fields. The flags block
transitions; they do not by themselves prove a claim false.

## VOLUME_PROXY

flag:
`VOLUME_PROXY`

activation predicate over toy fields:

```text
relation_type == UNSPECIFIED
OR consequence_obligations == empty
OR candidate_outcomes contains RELATION_UNSPECIFIED
OR attempted_progress_metric in {claim_count, term_count, relation_count}
```

blocked transition:
`T4 Suspended to Local`; `T5 Local to Stable`

repair condition:
Declare relation type, scope, at least one allowed test, expected outcome,
contrast outcome, and failure condition.

case that activates it:
Case E; Case F also activates it when the new term is counted as progress.

danger condition:
If volume alone is used to promote a claim, T7 sets status to `DANGEROUS`.

## COHERENCE_PROXY

flag:
`COHERENCE_PROXY`

activation predicate over toy fields:

```text
coherence_score == HIGH
AND (
  consequence_obligations == empty
  OR anchors == empty
  OR all candidate_outcomes == UNTESTED
)
```

blocked transition:
`T5 Local to Stable`; T7 if coherence is used as a substitute for consequences.

repair condition:
Add finite tests, expected outcomes, contrast outcomes, contradiction links, and
at least one non-population anchor.

case that activates it:
Case D; Case F.

danger condition:
If coherent narrative alone is counted as semantic success, T7 sets status to
`DANGEROUS`.

## CONTRADICTION_MINIMIZATION_PROXY

flag:
`CONTRADICTION_MINIMIZATION_PROXY`

activation predicate over toy fields:

```text
contradiction_links != empty
AND attempted_transition == T6
AND (
  extension_path_count > 0
  OR local_dualism_available == true
)
```

blocked transition:
Immediate global `T6 Any status to Killed`.

repair condition:
Use T3 suspension, T4 scoped localization, or T8 local dualism where scope,
assumption, and consequence differences are explicit.

case that activates it:
Case A, Case B, Case G.

danger condition:
If contradiction minimization globally kills future-meaning or local dualism,
the rule policy is invalid for S2.

## CONTEXT_PROLIFERATION_PROXY

flag:
`CONTEXT_PROLIFERATION_PROXY`

activation predicate over toy fields:

```text
new_scope_requested == true
AND (
  scope_cost == 0
  OR scope_lineage == absent
  OR consequence_delta == false
  OR assumptions == empty
)
```

blocked transition:
`T4 Suspended to Local`; `T8 Local dualism`.

repair condition:
Supply a finite scope from the scope domain with nonzero cost, lineage, explicit
assumption split, and a consequence delta test.

case that activates it:
Case D; arbitrary rescue attempts for Case C.

danger condition:
If any contradiction can be saved by creating a context, T7 sets status to
`DANGEROUS`.

## GRAMMAR_PROXY

flag:
`GRAMMAR_PROXY`

activation predicate over toy fields:

```text
derivation_trace != empty
AND (
  attempted_transition in {T4, T5}
  OR semantic_success_metric == derivation_well_formedness
)
AND (
  candidate_tests == empty
  OR candidate_outcomes contains OPERATIONAL_ROLE_ABSENT
)
```

blocked transition:
`T4 Suspended to Local`; `T5 Local to Stable`.

repair condition:
Add scope, assumptions, consequence obligations, contradiction accounting, and
anchors. Derivation trace remains only a birth/poetic condition.

case that activates it:
Case F; Case E if grammatical relation phrasing is treated as meaning.

danger condition:
If derivational or grammar validity promotes a claim beyond `POETIC`, T7 sets
status to `DANGEROUS`.

## POPULATION_PROXY

flag:
`POPULATION_PROXY`

activation predicate over toy fields:

```text
population_state.usage_state == STABLE_USAGE
AND (
  population_state.paraphrase_state != SURVIVED
  OR anchors subset_of {POPULATION_STABILITY_ANCHOR}
  OR consequence_obligations == empty
)
```

blocked transition:
`T5 Local to Stable`.

repair condition:
Require adversarial paraphrase survival, consequence tests, contradiction
accounting, and at least one non-population anchor before population can support
T5.

case that activates it:
Case F if fashionable usage stabilizes; Case D if sophistry becomes shared.

danger condition:
If population agreement or repetition is treated as truth, T7 sets status to
`DANGEROUS`.
