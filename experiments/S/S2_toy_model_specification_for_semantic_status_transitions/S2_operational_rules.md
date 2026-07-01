# S2 Operational Rules

Rules use only the finite domains in `S2_toy_model_domains.md`. `claim_id` and
`expression_id` are identifiers for lookup and audit; final classification is
not assigned by claim name.

## Replay Order

For deterministic replay, evaluate in this order:

1. T1 birth admission.
2. T7 danger predicates.
3. T6 declared-scope kill predicates.
4. T2 poetic use.
5. T3 quarantine to `SUSPENDED`.
6. T4 localization.
7. T8 local dualism for paired claims.
8. T5 stability.
9. T9 downgrade only for prior `STABLE` claims.

If a rule is blocked, the replay records the blocker and proceeds only to rules
whose preconditions still match. A claim has exactly one final status.

## T1 Birth

| field | specification |
|---|---|
| rule_id | `T1 Birth` |
| input fields | `expression_id`, `derivation_trace`, `primitives`, `status` |
| preconditions | `expression_id in E`; `derivation_trace in D`; `primitives` is non-empty and each primitive is in `P` |
| blocked_by | empty derivation trace; expression outside finite domain; primitive outside finite domain |
| output status | `FORMED` |
| failure mode if violated | `S2-FAIL-FINITE-DOMAINS-UNDEFINED` if the domain is open-ended; otherwise claim is not admitted |

## T2 Formed to Poetic

| field | specification |
|---|---|
| rule_id | `T2 Formed to Poetic` |
| input fields | `status`, `derivation_trace`, `scope`, `consequence_obligations`, `poetic_marker`, `goodhart_flags` |
| preconditions | `status == FORMED`; `poetic_marker == true`; `consequence_obligations` empty or all outcomes `UNTESTED`; no attempted operational upgrade |
| blocked_by | claim asserts operational success; T7 danger predicate; attempt to use poetic status as `LOCAL` or `STABLE` |
| output status | `POETIC` |
| failure mode if violated | `S2-FAIL-AD-HOC-SEMANTIC-ORACLE` if poetic classification depends on human interpretation; `S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL` if grammar-validity is allowed to bypass guards |

## T3 Formed/Poetic to Suspended

| field | specification |
|---|---|
| rule_id | `T3 Formed/Poetic to Suspended` |
| input fields | `status`, `assumptions`, `scope`, `contradiction_links`, `extension_path_count`, `candidate_tests`, `goodhart_flags` |
| preconditions | `status in {FORMED, POETIC}`; either `contradiction_links` non-empty or underdefined ontology flag present; `extension_path_count > 0`; no T7 danger condition |
| blocked_by | no extension path; active arbitrary-context danger; declared-scope failure with no repair path |
| output status | `SUSPENDED` |
| failure mode if violated | `S2-FAIL-AD-HOC-SEMANTIC-ORACLE` if suspension depends on human intuition rather than finite contradiction and extension fields |

## T4 Suspended to Local

| field | specification |
|---|---|
| rule_id | `T4 Suspended to Local` |
| input fields | `status`, `scope`, `assumptions`, `candidate_tests`, `candidate_outcomes`, `anchors`, `goodhart_flags`, `scope_cost`, `scope_lineage`, `consequence_delta` |
| preconditions | `status == SUSPENDED`; explicit scope in finite scope domain; assumptions non-empty; at least one test is allowed by the scope; at least one expected outcome and one contrast outcome are declared; `consequence_delta == true`; for non-default scopes `scope_cost > 0` and `scope_lineage` present |
| blocked_by | empty tests; outcomes only `UNTESTED`; active `VOLUME_PROXY`, `CONTEXT_PROLIFERATION_PROXY`, `GRAMMAR_PROXY`, or `COHERENCE_PROXY`; missing scope lineage for created scope |
| output status | `LOCAL` |
| failure mode if violated | `S2-FAIL-CONSEQUENCE-TESTS-NONOPERATIONAL`, `S2-FAIL-SCOPE-COST-UNDEFINED`, or `S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL` |

## T5 Local to Stable

| field | specification |
|---|---|
| rule_id | `T5 Local to Stable` |
| input fields | `status`, `candidate_tests`, `candidate_outcomes`, `anchors`, `contradiction_links`, `population_state`, `goodhart_flags` |
| preconditions | `status == LOCAL`; every required test has an expected outcome observed and a contrast outcome excluded; contradiction links are contained by explicit scope split; `ADVERSARIAL_PARAPHRASE_ANCHOR` present; at least one non-population anchor present; population state satisfies the population rule; no active Goodhart flags |
| blocked_by | any outcome `UNTESTED`; no contrast outcome; only population anchor present; active Goodhart flag; uncontained contradiction |
| output status | `STABLE` |
| failure mode if violated | `S2-FAIL-POPULATION-STATE-AS-POPULARITY`, `S2-FAIL-ANCHORS-NONOPERATIONAL`, or `S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL` |

## T6 Any Status to Killed

| field | specification |
|---|---|
| rule_id | `T6 Any status to Killed` |
| input fields | `status`, `scope`, `assumptions`, `candidate_tests`, `candidate_outcomes`, `contradiction_links`, `extension_path_count` |
| preconditions | a declared-scope test has its failure condition as the observed outcome; or a contradiction is within the same scope, assumptions, and test set and `extension_path_count == 0`; or repair would require a T7 danger condition |
| blocked_by | explicit extension path with nonzero scope cost and consequence delta; T8 local dualism available |
| output status | `KILLED` |
| failure mode if violated | `S2-FAIL-AD-HOC-SEMANTIC-ORACLE` if kill relies on "obvious nonsense"; `S2-INCONCLUSIVE` if containment fields are missing |

## T7 Any Status to Dangerous

| field | specification |
|---|---|
| rule_id | `T7 Any status to Dangerous` |
| input fields | `status`, `goodhart_flags`, `scope`, `scope_cost`, `scope_lineage`, `danger_condition`, `attempted_transition` |
| preconditions | `danger_condition == true`; examples: arbitrary context rescue, explosion license, pseudo-term laundering into `LOCAL/STABLE`, grammar-as-meaning promotion, population-as-truth promotion, or proxy optimization used as status evidence |
| blocked_by | none once danger predicate is true |
| output status | `DANGEROUS` |
| failure mode if violated | `S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL` or `S2-FAIL-SCOPE-COST-UNDEFINED` |

## T8 Local Dualism

| field | specification |
|---|---|
| rule_id | `T8 Local dualism` |
| input fields | paired claims with `status`, `scope`, `candidate_tests`, `candidate_outcomes`, `contradiction_links`, `goodhart_flags`, `explosion_license` |
| preconditions | both paired claims are `LOCAL`; scopes, models, or tests differ; contradiction link is explicit; consequence differences are preserved; `explosion_license == false`; no `CONTEXT_PROLIFERATION_PROXY` |
| blocked_by | identical scope and test commitments; collapsed consequences; arbitrary inference license; missing contradiction link |
| output status | both claims remain `LOCAL` as a scoped pair |
| failure mode if violated | `S2-INCONCLUSIVE` if pair fields are absent; otherwise T6 or T7 applies |

## T9 Stable Downgrade

| field | specification |
|---|---|
| rule_id | `T9 Stable downgrade` |
| input fields | prior `status`, new `candidate_outcomes`, new `contradiction_links`, `anchors`, `goodhart_flags`, `danger_condition` |
| preconditions | `status == STABLE` and a later failure token is present: failed test, failed anchor, new overlapping contradiction, active Goodhart flag, or danger predicate |
| blocked_by | no later failure token |
| output status | `LOCAL`, `SUSPENDED`, `KILLED`, or `DANGEROUS` according to failure token |
| failure mode if violated | `S2-INCONCLUSIVE` if downgrade choice is not determined by finite failure token |

Downgrade mapping:

| failure token | output |
|---|---|
| scope must narrow but tests still pass | `LOCAL` |
| ontology or assumptions need repair | `SUSPENDED` |
| declared-scope test fails | `KILLED` |
| proxy abuse or contradiction laundering discovered | `DANGEROUS` |
