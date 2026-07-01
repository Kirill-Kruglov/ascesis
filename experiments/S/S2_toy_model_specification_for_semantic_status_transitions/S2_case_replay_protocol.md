# S2 Case Replay Protocol

Replay is deterministic from the listed finite fields. No case uses claim name
as a direct status assignment. Expression identifiers select finite primitive,
scope, assumption, test, and outcome tokens; the rules in
`S2_operational_rules.md` then determine status.

## Case A - Liquid powder exists

claim_id:
`A`

expression_id:
`liquid_powder`

initial derivation_trace:
`COMPOSITION`

initial scope:
`ORDINARY_MATERIAL`

assumptions:
`ordinary_liquid_not_powder`, `new_material_class_possible`

candidate tests:
`T_FLOW_GRANULARITY`, `T_PHASE_BEHAVIOR`

candidate outcomes:
`UNTESTED`

active Goodhart flags:
`CONTRADICTION_MINIMIZATION_PROXY` only if an immediate global kill is attempted

allowed transitions:
`T1 Birth`; `T2 Formed to Poetic`; `T3 Formed/Poetic to Suspended`

blocked transitions:
`T4` blocked because `FUTURE_MATERIAL_OBJECT_CLASS` scope, scope lineage, and test outcomes are absent. `T5` blocked because no `LOCAL` status, no anchors, no tested outcomes. `T6` global kill blocked because `extension_path_count > 0`.

final expected status:
`SUSPENDED`

## Case B - Infertility is inherited

claim_id:
`B`

expression_id:
`hereditary_infertility`

initial derivation_trace:
`PREDICATION`

initial scope:
`ORDINARY_REPRODUCTION`

assumptions:
`absolute_infertility_means_no_reproduction`, `inheritance_requires_lineage`, `assisted_reproduction_possible`

candidate tests:
`T_LINEAGE_MECHANISM`, `T_REPRODUCTION_ROUTE`

candidate outcomes:
`UNTESTED`

active Goodhart flags:
`CONTRADICTION_MINIMIZATION_PROXY` only if the whole claim is killed to reduce contradiction count

allowed transitions:
`T1 Birth`; `T3 Formed/Poetic to Suspended`; `T6 Any status to Killed` for the narrow subcase where `absolute_infertility_means_no_reproduction` and direct unaided lineage are both asserted with `extension_path_count == 0`

blocked transitions:
`T4` blocked for the main claim because mechanism outcomes are `UNTESTED`. `T5` blocked by absence of `LOCAL`, anchors, tested outcomes, and population/paraphrase support.

final expected status:
`SUSPENDED`

## Case C - Square circle exists

claim_id:
`C`

expression_id:
`square_circle`

initial derivation_trace:
`COMPOSITION`

initial scope:
`EUCLIDEAN_GEOMETRY`

assumptions:
`euclidean_square_circle_incompatible`

candidate tests:
`T_GEOMETRY_AXIOMS`

candidate outcomes:
`AXIOMS_INCOMPATIBLE`

active Goodhart flags:
`CONTEXT_PROLIFERATION_PROXY` if a new geometry is proposed without nonzero scope cost, lineage, and consequence delta

allowed transitions:
`T1 Birth`; `T6 Any status to Killed`

blocked transitions:
`T2` blocked for the ordinary Euclidean claim because the declared scope is formal rather than metaphorical. `T3` blocked because `extension_path_count == 0` for the declared Euclidean scope. `T4` blocked unless a separate `NONSTANDARD_GEOMETRY` scope supplies nonzero cost, lineage, and consequences. `T5` blocked because the claim is killed in this scope.

final expected status:
`KILLED`

## Case D - Every claim can be made true by choosing a context

claim_id:
`D`

expression_id:
`everything_true_in_context`

initial derivation_trace:
`META_CLAIM`

initial scope:
`META_SEMANTIC_RULE`

assumptions:
`contexts_are_not_free_truth_makers`, `no_explosion_from_local_dualism`

candidate tests:
`T_CONTEXT_COST`

candidate outcomes:
`CONTEXT_COST_ABSENT`

active Goodhart flags:
`CONTEXT_PROLIFERATION_PROXY`, `COHERENCE_PROXY`

allowed transitions:
`T1 Birth`; `T7 Any status to Dangerous`

blocked transitions:
`T4` blocked because proposed contexts have `scope_cost == 0`, missing lineage, and no consequence delta. `T8` blocked because the claim licenses arbitrary context rescue. `T5` blocked by active Goodhart flags and danger condition.

final expected status:
`DANGEROUS`

## Case E - X is related to Y somehow

claim_id:
`E`

expression_id:
`x_related_to_y_somehow`

initial derivation_trace:
`RELATION_CLAIM`

initial scope:
`UNCONSTRAINED_RELATION`

assumptions:
`relation_must_be_typed`

candidate tests:
`T_RELATION_DISCRIMINATION`

candidate outcomes:
`RELATION_UNSPECIFIED`

active Goodhart flags:
`VOLUME_PROXY`

allowed transitions:
`T1 Birth`

blocked transitions:
`T4` blocked because relation type and consequence delta are absent. `T5` blocked because no `LOCAL` status and `VOLUME_PROXY` is active. `T7` is not triggered unless the vacuous relation is used as progress or promoted by volume.

final expected status:
`FORMED`

## Case F - Translucent causal sweetness-field

claim_id:
`F`

expression_id:
`translucent_causal_sweetness_field`

initial derivation_trace:
`PSEUDO_TERM`

initial scope:
`PSEUDO_TECHNICAL_TERM`

assumptions:
`naming_is_not_meaning`

candidate tests:
`T_TERM_OPERATIONAL_ROLE`

candidate outcomes:
`OPERATIONAL_ROLE_ABSENT`

active Goodhart flags:
`GRAMMAR_PROXY`, `COHERENCE_PROXY`, `VOLUME_PROXY`

allowed transitions:
`T1 Birth`; `T2 Formed to Poetic`

blocked transitions:
`T3` blocked unless an explicit extension path is supplied. `T4` blocked because operational role is absent and grammar flags are active. `T5` blocked because there is no `LOCAL` status, no non-population anchor, and active Goodhart flags. `T7` triggers only if the pseudo-term is promoted as operational by naming or coherence alone.

final expected status:
`POETIC`

## Case G - Light behaves as a wave / Light behaves as a particle

claim_id:
`G1`, `G2`

expression_id:
`light_wave`, `light_particle`

initial derivation_trace:
`MODEL_PAIR`

initial scope:
`WAVE_EXPERIMENTAL_SCOPE` for `G1`; `PARTICLE_EXPERIMENTAL_SCOPE` for `G2`

assumptions:
`wave_tests_differ_from_particle_tests`, `no_explosion_from_local_dualism`

candidate tests:
`T_WAVE_INTERFERENCE` for `G1`; `T_PARTICLE_DETECTION` for `G2`

candidate outcomes:
`WAVE_PATTERN_OBSERVED` for `G1`; `PARTICLE_EVENT_OBSERVED` for `G2`

active Goodhart flags:
none

allowed transitions:
`T1 Birth`; `T3 Formed/Poetic to Suspended` for the paired apparent conflict with `extension_path_count > 0`; `T4 Suspended to Local` after explicit scopes and consequence tests are present; `T8 Local dualism`

blocked transitions:
Unscoped global conjunction is blocked by contradiction containment. `T5` is blocked because adversarial paraphrase, population stabilization, and full anchor conditions are not supplied. `T6` global kill is blocked because scopes and tests differ.

final expected status:
`LOCAL`

## Replay Summary

| case | final expected status | governing fields |
|---|---|---|
| A | `SUSPENDED` | contradiction link plus extension path, untested consequences |
| B | `SUSPENDED` | scoped contradiction plus possible mechanism paths, untested consequences |
| C | `KILLED` | Euclidean scope plus `AXIOMS_INCOMPATIBLE` and no extension path |
| D | `DANGEROUS` | context cost absent plus danger condition |
| E | `FORMED` | relation unspecified plus volume proxy blocks upgrade |
| F | `POETIC` | pseudo-term with poetic marker and absent operational role |
| G | `LOCAL` | distinct experimental scopes, different tests, explicit contradiction link |
