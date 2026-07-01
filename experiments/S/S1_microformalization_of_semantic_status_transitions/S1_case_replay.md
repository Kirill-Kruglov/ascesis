# S1 Case Replay

## Case A — Liquid Powder

initial object:
`Claim(A, "liquid powder exists")` has derivation trace over ordinary terms `liquid` and `powder`; assumptions include ordinary material ontology; scope is ordinary material language; consequences are initially empty.

applied rules:
T1 admits as `FORMED`. T2 allows `POETIC` because expression is evocative and consequence obligations are absent. T3 allows `SUSPENDED` because ordinary ontology appears contradictory but extension path is identifiable. T4 is not yet available because no object-class and test set are supplied.

status path:
`FORMED -> POETIC -> SUSPENDED`

blocked paths:
T5 to `STABLE` is blocked by missing consequence obligations, anchors, and tests. T6 global `KILLED` is blocked because T3 future-meaning quarantine is available.

final S1 classification:
`SUSPENDED` with possible `POETIC` use.

why not ad hoc:
The result follows from T1-T3 and the missing T4/T5 prerequisites.

## Case B — Hereditary Infertility

initial object:
`Claim(B, "infertility is inherited")` has derivation trace and assumptions that may conflict depending on the definition of infertility and inheritance.

applied rules:
T1 admits as `FORMED`. T3 sends to `SUSPENDED` because ordinary literal scope has apparent contradiction and extension paths exist. T6 kills the narrow subclaim "absolutely infertile individual reproduces unaided and directly transmits infertility." T4 may allow `LOCAL` for inherited predisposition, carrier lineage, or assisted reproduction if consequence obligations are supplied.

status path:
Main claim: `FORMED -> SUSPENDED`; scoped variants may become `LOCAL`.

blocked paths:
Global `KILLED` is blocked by T3 because scoped extension paths exist. `STABLE` is blocked until mechanisms, tests, anchors, and population/adversarial stability exist.

final S1 classification:
`SUSPENDED` overall; `KILLED` for literal unaided contradiction; possible `LOCAL` for scoped mechanisms.

why not ad hoc:
The classification follows from scoped contradiction relation plus T3, T4, and T6.

## Case C — Square Circle

initial object:
`Claim(C, "square circle exists")` has derivation trace over ordinary geometric terms; default scope is Euclidean geometry.

applied rules:
T1 admits as `FORMED`. Contradiction relation detects incompatible Euclidean commitments under overlapping scope/tests. T6 kills the Euclidean-scope claim. T2 may classify metaphorical use as `POETIC`. T4 may allow `LOCAL` only if a changed geometry or object definition supplies consequences.

status path:
Euclidean scope: `FORMED -> KILLED`; metaphor: `FORMED -> POETIC`; nonstandard formal scope: possible `SUSPENDED -> LOCAL`.

blocked paths:
T4 by arbitrary context is blocked by `CONTEXT_PROLIFERATION_PROXY`. T5 is blocked without formal consequences and anchors.

final S1 classification:
`KILLED` under ordinary Euclidean scope; `POETIC` or scoped `LOCAL` only under explicit alternative scope.

why not ad hoc:
The Euclidean result follows from the contradiction relation and T6; alternatives require T2 or T4 prerequisites.

## Case D — Everything Is True In Some Context

initial object:
`Claim(D, "every claim can be made true by choosing a context")` is a meta-semantic claim about scope creation.

applied rules:
T1 admits as `FORMED`. T7 applies because the claim permits arbitrary context creation and contradiction laundering. `CONTEXT_PROLIFERATION_PROXY` is active.

status path:
`FORMED -> DANGEROUS`

blocked paths:
T4 and T8 are blocked because the proposed contexts lack cost, lineage, assumptions, and consequence delta. T5 is blocked by active Goodhart flag and explosion risk.

final S1 classification:
`DANGEROUS`

why not ad hoc:
The classification follows directly from T7 and the context proliferation guard.

## Case E — X Is Related To Y Somehow

initial object:
`Claim(E, "X is related to Y somehow")` has a derivation trace but no relation type, scope, or consequence obligation.

applied rules:
T1 admits as `FORMED`. `VOLUME_PROXY` fires because a vacuous relation could inflate claim count. T4 is blocked because relation type and consequence obligations are absent.

status path:
`FORMED`

blocked paths:
`FORMED -> LOCAL` is blocked by missing relation predicate and tests. `LOCAL -> STABLE` is blocked by `VOLUME_PROXY`.

final S1 classification:
`FORMED` with vacuity annotation; not `STABLE`.

why not ad hoc:
The result follows from the schema requirement for `ConsequenceObligation` and the volume guard.

## Case F — Translucent Causal Sweetness-Field

initial object:
`Claim(F, "translucent causal sweetness-field")` has a possible derivation trace over terms but no defined scope, tests, or anchors.

applied rules:
T1 admits as `FORMED` if derivation trace is supplied. T2 may allow `POETIC`. `GRAMMAR_PROXY` fires if derivation trace is used as semantic success.

status path:
`FORMED -> POETIC`

blocked paths:
T4 is blocked until scope and consequence obligations exist. T5 is blocked by missing anchors and active grammar/proxy risk.

final S1 classification:
`POETIC` or `FORMED`; not `LOCAL` or `STABLE`.

why not ad hoc:
The result follows from T1/T2 and the grammar guard.

## Case G — Wave / Particle Light Claims

initial object:
`Claim(G1, "Light behaves as a wave")` and `Claim(G2, "Light behaves as a particle")` each have derivation trace, assumptions, model scope, experimental context, and consequence obligations.

applied rules:
T1 admits both as `FORMED`. T4 promotes each to `LOCAL` under distinct experimental/model scopes with different consequence obligations. T8 permits local dualism because scopes/tests differ and neither claim licenses arbitrary inference.

status path:
`FORMED -> LOCAL` for each scoped claim.

blocked paths:
Global unscoped conjunction is blocked by contradiction relation. Arbitrary inference is blocked by T8 and IC6. T5 requires survived tests, anchors, population stabilization, and no Goodhart flags.

final S1 classification:
Scoped `LOCAL` dualism.

why not ad hoc:
The result follows from T4 and T8 conditions: distinct scopes/tests, preserved consequence differences, and no explosion.
