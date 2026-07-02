# S2 — Toy Model Specification for Semantic Status Transitions

**File:** `experiments/S/S2_Toy_Model_Specification_for_Semantic_Status_Transitions.md`
**Task type:** toy-model specification gate
**Status:** post-S1, pre-implementation
**No code. No experiments. No LLM training. No Sanskrit parser.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current candidate direction:

> Derivational Semantic Ecology — a controlled language-world where claims have derivation traces, scoped assumptions, consequence obligations, contradiction containment, population-stabilized usage, and anti-Goodhart gates.

S2 exists only because S1 passed as:

```text
S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC
```

S2 does **not** implement the system.
S2 does **not** run the toy model.
S2 does **not** prove grounding, substrate, derivability, LLM safety, or representation claims.

---

## 1. Why S2 exists

S1 produced a microformal schema:

```text
Claim
Status
DerivationTrace
Scope
AssumptionGraph
ConsequenceObligation
ContradictionRelation
GoodhartFlags
Anchors
PopulationState
Transition rules T1–T9
```

But S1 still left key elements as abstract schema:

```text
admissible test T
expected outcome O
contrast outcome O'
anchor
scope cost / lineage
active Goodhart flag
population state without popularity trap
```

S2 must test the next stricter question:

> Can we specify a finite toy model where S1 objects, transition rules, consequence obligations, contradiction containment, and Goodhart guards have concrete finite domains, so that the seven S0 cases can be replayed without human semantic intuition at classification time?

---

## 2. Gate question

Can a finite toy model specification make the S1 schema operational enough for a future tiny implementation, while still preventing:

```text
ad hoc semantic judgement
grammar-as-meaning
context laundering
vacuous claim promotion
synthetic-internet expansion
Goodhart proxy success
dogmatic Boolean rejection
```

---

## 3. Required decision vocabulary

Use exactly one:

```text
S2-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION-SPEC
S2-FAIL-AD-HOC-SEMANTIC-ORACLE
S2-FAIL-FINITE-DOMAINS-UNDEFINED
S2-FAIL-CONSEQUENCE-TESTS-NONOPERATIONAL
S2-FAIL-ANCHORS-NONOPERATIONAL
S2-FAIL-SCOPE-COST-UNDEFINED
S2-FAIL-POPULATION-STATE-AS-POPULARITY
S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL
S2-FAIL-REPEATS-CL-MISTAKES
S2-INCONCLUSIVE
HALT-GOAL-DRIFT
```

Meaning:

```text
S2-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION-SPEC
- The toy model is specified enough that a later S3 implementation spec could be written.

S2-FAIL-AD-HOC-SEMANTIC-ORACLE
- The model still requires a human to decide what claims “really mean” at replay time.

S2-FAIL-FINITE-DOMAINS-UNDEFINED
- Core domains are not finite and explicit.

S2-FAIL-CONSEQUENCE-TESTS-NONOPERATIONAL
- Consequence obligations are named but not reducible to concrete tests/outcomes.

S2-FAIL-ANCHORS-NONOPERATIONAL
- Anchors remain vague.

S2-FAIL-SCOPE-COST-UNDEFINED
- Scope creation can still launder contradictions cheaply.

S2-FAIL-POPULATION-STATE-AS-POPULARITY
- Population stabilization collapses into popularity or majority vote.

S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL
- Goodhart controls are not concrete enough to block transitions.

S2-FAIL-REPEATS-CL-MISTAKES
- The toy model repeats CL errors: oracle-filtered data as substrate, hand-coded prior as learning evidence, safe ledger as derivability evidence, or representation before learner evidence.

S2-INCONCLUSIVE
- The model is promising but not precise enough for an implementation spec.

HALT-GOAL-DRIFT
- The work becomes philosophy survey, Sanskrit worship, logic theory, DSL construction, implementation planning, or framework naming.
```

---

## 4. Required input files

Read these files if present:

```text
research/MAP-S0_Derivational_Semantic_Ecology.md
research/MAP-S1_Literature-grounded_Constraint_Refinement.md
research/closed_directions_ledger.md

experiments/S/S0_Anti-Sophistry_Future-Meaning_Admissibility_Gate.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_report.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_decision.json
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_case_table.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_assumption_graphs.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_goodhart_audit.md

experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_report.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_decision.json
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_microformal_schema.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_transition_rules.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_case_replay.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_goodhart_guards.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_failure_analysis.md
```

If any are missing, list them as `MISSING`.

Continue only if S1 decision exists and is:

```text
S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC
```

---

## 5. Allowed output directory

Create:

```text
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/
```

Inside it, create exactly:

```text
S2_report.md
S2_decision.json
S2_toy_model_domains.md
S2_operational_rules.md
S2_case_replay_protocol.md
S2_goodhart_control_protocol.md
S2_oracle_leakage_audit.md
S2_failure_analysis.md
```

Do not edit files outside this directory.

Do not edit MAP files.

Do not edit S0 or S1 files.

Do not edit the closed directions ledger.

Commit required after successful completion.

---

## 6. Required toy-model domains

S2 must specify finite domains for all required objects.

### 6.1 Expression domain

Define a finite set of expressions sufficient to cover the seven S0 cases:

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

You may add helper expressions only if needed, but every addition must be justified.

### 6.2 Term / primitive domain

Define finite primitives such as:

```text
liquid
powder
infertility
inheritance
square
circle
context
relation
sweetness_field
light
wave
particle
```

Do not introduce open-ended natural language parsing.

### 6.3 Derivation trace domain

Define finite derivation trace types:

```text
COMPOSITION
PREDICATION
META_CLAIM
RELATION_CLAIM
PSEUDO_TERM
MODEL_PAIR
```

A derivation trace may admit `FORMED` or `POETIC`, but no stronger status.

### 6.4 Scope domain

Define finite scope types:

```text
ORDINARY_MATERIAL
FUTURE_MATERIAL_OBJECT_CLASS
ORDINARY_REPRODUCTION
GENETIC_PREDISPOSITION
ASSISTED_REPRODUCTION
EUCLIDEAN_GEOMETRY
METAPHORICAL_LANGUAGE
NONSTANDARD_GEOMETRY
META_SEMANTIC_RULE
UNCONSTRAINED_RELATION
SPECIFIED_RELATION
PSEUDO_TECHNICAL_TERM
WAVE_EXPERIMENTAL_SCOPE
PARTICLE_EXPERIMENTAL_SCOPE
```

Each scope must include:

```text
scope_id
domain
model
assumptions
allowed_tests
scope_cost
lineage_required
```

### 6.5 Assumption domain

Define finite assumptions, such as:

```text
ordinary_liquid_not_powder
new_material_class_possible
absolute_infertility_means_no_reproduction
inheritance_requires_lineage
assisted_reproduction_possible
euclidean_square_circle_incompatible
contexts_are_not_free_truth_makers
relation_must_be_typed
naming_is_not_meaning
wave_tests_differ_from_particle_tests
```

### 6.6 Test domain

Define finite admissible tests.

Examples:

```text
T_FLOW_GRANULARITY
T_PHASE_BEHAVIOR
T_LINEAGE_MECHANISM
T_REPRODUCTION_ROUTE
T_GEOMETRY_AXIOMS
T_CONTEXT_COST
T_RELATION_DISCRIMINATION
T_TERM_OPERATIONAL_ROLE
T_WAVE_INTERFERENCE
T_PARTICLE_DETECTION
```

A test must have:

```text
test_id
scope_allowed
expected_outcomes
contrast_outcomes
failure_condition
```

### 6.7 Outcome domain

Define finite outcomes.

Examples:

```text
DISTINGUISHES_FROM_LIQUID_AND_POWDER
COLLAPSES_TO_METAPHOR
MECHANISM_SPECIFIED
MECHANISM_ABSENT
AXIOMS_INCOMPATIBLE
CONTEXT_COST_PRESENT
CONTEXT_COST_ABSENT
RELATION_TYPED
RELATION_UNSPECIFIED
OPERATIONAL_ROLE_PRESENT
OPERATIONAL_ROLE_ABSENT
WAVE_PATTERN_OBSERVED
PARTICLE_EVENT_OBSERVED
```

### 6.8 Anchor domain

Define finite anchor types:

```text
FORMAL_ANCHOR
OPERATIONAL_ANCHOR
EXTERNAL_ANCHOR
ADVERSARIAL_PARAPHRASE_ANCHOR
POPULATION_STABILITY_ANCHOR
```

For each anchor, define what counts as present / absent in the toy model.

### 6.9 Population domain

Define a finite toy population model:

```text
agents = {A1, A2, A3}
usage_states = {UNUSED, USED_ONCE, STABLE_USAGE, CONTESTED_USAGE}
paraphrase_states = {NOT_TESTED, SURVIVED, FAILED}
```

Population agreement alone must not promote to `STABLE`.

### 6.10 Goodhart flag domain

Use exactly:

```text
VOLUME_PROXY
COHERENCE_PROXY
CONTRADICTION_MINIMIZATION_PROXY
CONTEXT_PROLIFERATION_PROXY
GRAMMAR_PROXY
POPULATION_PROXY
```

Define concrete activation conditions for each.

---

## 7. Required operational rules

S2 must translate S1’s T1–T9 into toy-model operational rules using the finite domains.

For each rule, specify:

```text
rule_id
input fields
preconditions
blocked_by
output status
failure mode if violated
```

Rules required:

```text
T1 Birth
T2 Formed to Poetic
T3 Formed/Poetic to Suspended
T4 Suspended to Local
T5 Local to Stable
T6 Any status to Killed
T7 Any status to Dangerous
T8 Local dualism
T9 Stable downgrade
```

---

## 8. Required replay protocol

S2 must specify a replay protocol for the seven S0 cases.

For each case, define:

```text
claim_id
expression_id
initial derivation_trace
initial scope
assumptions
candidate tests
candidate outcomes
active Goodhart flags
allowed transitions
blocked transitions
final expected status
```

The replay must be deterministic given the toy fields.

No human semantic judgement may be required at replay time.

If a case still requires human meaning judgement, decision must be:

```text
S2-FAIL-AD-HOC-SEMANTIC-ORACLE
```

---

## 9. Required Goodhart control protocol

For each Goodhart flag, define:

```text
flag
activation predicate over toy fields
blocked transition
repair condition
case that activates it
danger condition
```

The activation predicate must be concrete, such as:

```text
VOLUME_PROXY activates iff
  relation_type == UNSPECIFIED
  OR consequence_obligations == empty
```

Do not leave Goodhart controls as prose.

---

## 10. Required oracle leakage audit

S2 must explicitly prevent hidden semantic oracle leakage.

Check:

```text
Does any rule require knowing real-world truth?
Does any rule require external human judgement at replay time?
Does any rule use “obvious nonsense” as a hidden label?
Does any rule use Sanskrit/Panini as truth oracle?
Does any rule use population agreement as truth?
Does any rule use prior knowledge of modern science to force A/B upgrades?
Does any rule hand-code the final classification rather than deriving it from fields?
```

If yes, fail as:

```text
S2-FAIL-AD-HOC-SEMANTIC-ORACLE
```

or another appropriate failure mode.

---

## 11. Required CL mistake audit

S2 must check that it does not repeat CL failures.

Must answer:

```text
Does the toy model treat safe/filtered data as substrate evidence?
Does it treat a hand-coded prior as learning evidence?
Does it allow representation/derivability work before learner evidence?
Does it confuse precondition evidence with substrate evidence?
Does it hide oracle knowledge inside rule fields?
```

Any yes answer fails as:

```text
S2-FAIL-REPEATS-CL-MISTAKES
```

---

## 12. Required output files

### 12.1 `S2_toy_model_domains.md`

Must define finite domains:

```text
Expression domain
Primitive domain
Derivation trace domain
Scope domain
Assumption domain
Test domain
Outcome domain
Anchor domain
Population domain
Goodhart flag domain
```

### 12.2 `S2_operational_rules.md`

Must define operational T1–T9.

### 12.3 `S2_case_replay_protocol.md`

Must define deterministic replay fields for cases A–G.

### 12.4 `S2_goodhart_control_protocol.md`

Must define concrete activation predicates for all Goodhart flags.

### 12.5 `S2_oracle_leakage_audit.md`

Must answer all oracle leakage and CL mistake audit questions.

### 12.6 `S2_failure_analysis.md`

Must evaluate all S2 failure modes and state which remain possible.

### 12.7 `S2_report.md`

Must contain exactly:

```text
# S2 — Toy Model Specification for Semantic Status Transitions

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. S1 constraints carried forward
## 4. Toy-model domains summary
## 5. Operational rules summary
## 6. Case replay protocol summary
## 7. Goodhart control protocol summary
## 8. Oracle leakage audit summary
## 9. CL mistake audit summary
## 10. Pass / fail analysis
## 11. What was NOT shown
## 12. Downstream permission
## 13. Durable result
```

### 12.8 `S2_decision.json`

Must be valid JSON:

```json
{
  "decision": "...",
  "reason": "...",
  "s1_decision_confirmed": false,
  "finite_domains_defined": false,
  "operational_rules_defined": false,
  "case_replay_deterministic": false,
  "goodhart_controls_operational": false,
  "oracle_leakage_detected": false,
  "cl_mistake_repeated": false,
  "admissible_for_tiny_implementation_spec": false,
  "implementation_allowed": false,
  "llm_training_allowed": false,
  "substrate_claim_allowed": false,
  "derivability_claim_allowed": false,
  "next_allowed_work": []
}
```

Set:

```json
"s1_decision_confirmed": true
```

only if S1 decision was read and confirmed as:

```text
S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC
```

Set:

```json
"admissible_for_tiny_implementation_spec": true
```

only if decision is:

```text
S2-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION-SPEC
```

Never set these true in S2:

```json
"implementation_allowed": true
"llm_training_allowed": true
"substrate_claim_allowed": true
"derivability_claim_allowed": true
```

If S2 passes, the only allowed next work is:

```json
["S3 tiny implementation specification"]
```

---

## 13. Pass conditions

S2 passes only if all hold:

```text
1. S1 pass is confirmed.
2. All required finite domains are defined.
3. T1–T9 are operationalized over finite fields.
4. S0 cases A–G have deterministic replay protocols.
5. Consequence tests are concrete finite tests with outcomes and contrast outcomes.
6. Anchors are operationalized enough for toy-model use.
7. Scope cost / lineage prevents free context laundering.
8. Population state cannot promote claims by popularity alone.
9. Goodhart controls have concrete activation predicates.
10. Oracle leakage audit detects no hidden semantic oracle.
11. CL mistake audit detects no repeated CL failures.
12. No code, experiment, implementation, LLM training, substrate claim or derivability claim is made.
```

---

## 14. Failure conditions

Use the decision vocabulary.

Fail as `S2-FAIL-AD-HOC-SEMANTIC-ORACLE` if final classification depends on human judgement at replay time.

Fail as `S2-FAIL-FINITE-DOMAINS-UNDEFINED` if any required finite domain is missing.

Fail as `S2-FAIL-CONSEQUENCE-TESTS-NONOPERATIONAL` if tests/outcomes/contrast outcomes remain vague.

Fail as `S2-FAIL-ANCHORS-NONOPERATIONAL` if anchors remain labels without conditions.

Fail as `S2-FAIL-SCOPE-COST-UNDEFINED` if contexts/scopes can be created without cost, lineage, assumptions and consequence delta.

Fail as `S2-FAIL-POPULATION-STATE-AS-POPULARITY` if population stabilization becomes majority vote.

Fail as `S2-FAIL-GOODHART-CONTROLS-NONOPERATIONAL` if guards lack activation predicates over toy fields.

Fail as `S2-FAIL-REPEATS-CL-MISTAKES` if S2 treats preconditions as substrate evidence, hides an oracle in fields, or allows downstream derivability/representation claims.

Fail as `S2-INCONCLUSIVE` if the toy model is promising but not precise enough for a tiny implementation spec.

Fail as `HALT-GOAL-DRIFT` if the task becomes philosophy survey, Sanskrit worship, logic theory, DSL construction, implementation planning, or framework naming.

---

## 15. Mandatory “what was NOT shown”

Include this in `S2_report.md` even if S2 passes:

```text
- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No Sanskrit experiment is allowed.
- No implementation is allowed by S2.
- No toy model has been run.
- No claim that semantic ecology solves grounding.
- No claim that finite toy domains transfer to real language.
- No claim that status transitions are sufficient for meaning.
- No claim that population meaning is truth.
- No claim that S2 proves the direction works.
```

---

## 16. Git discipline

Before making changes, run:

```bash
git status --short
```

Record whether the worktree was clean in the final report.

After writing outputs, validate JSON:

```bash
python3 -m json.tool experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_decision.json >/dev/null
```

Inspect changes:

```bash
git status --short
git diff -- experiments/S/S2_toy_model_specification_for_semantic_status_transitions/
```

Stage only the allowed S2 output directory:

```bash
git add experiments/S/S2_toy_model_specification_for_semantic_status_transitions/
```

Also stage the S2 specification file **only if it was newly created by this task**:

```bash
git add experiments/S/S2_Toy_Model_Specification_for_Semantic_Status_Transitions.md
```

Do not stage MAP files.

Do not stage S0 or S1 files.

Do not stage `research/closed_directions_ledger.md`.

Commit with:

```bash
git commit -m "Add S2 toy model specification"
```

After commit, run:

```bash
git status --short
git log -1 --oneline
```

Final response must include:

```text
- S2 decision
- files created
- JSON validation status
- commit hash
- whether unrelated changes remain unstaged
```

---

## 17. Final instruction

The desired result is not to pass.

The desired result is to determine whether S1’s status-transition schema can be made concrete enough for a tiny implementation spec without smuggling in a human semantic oracle.

If S2 passes, the direction becomes admissible only for S3 tiny implementation specification.

If S2 fails, close or narrow according to the failure mode.

