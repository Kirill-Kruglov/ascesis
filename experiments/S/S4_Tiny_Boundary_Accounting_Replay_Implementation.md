# S4 — Tiny Boundary-Accounting / Replay Implementation

**File:** `experiments/S/S4_Tiny_Boundary_Accounting_Replay_Implementation.md`
**Task type:** bounded tiny implementation task
**Status:** post-S3, code allowed only inside S4 output directory
**Allowed:** small Python implementation, JSON fixtures, audit outputs, tests
**Forbidden:** LLM training, experiments beyond specified tiny replay/mutation tests, Sanskrit parser, semantic generator, substrate/derivability claims

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest S-branch status after B0/S3:

> We do not have a semantic boundary generator. We have a bounded specification for a boundary-accounting / replay audit engine over finite, human-authored toy fields.

S4 exists only because S3 passed as:

```text
S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION
```

S4 may implement only:

```text
boundary accounting
deterministic replay
provenance validation
oracle-field rejection
Goodhart flag activation
claim-strength downgrades
mutation tests
audit output
```

S4 must not implement or claim:

```text
semantic engine
meaning generator
boundary generator
truth detector
grounding system
substrate prototype
learner evidence
LLM safety
derivability
```

---

## 1. Why S4 exists

S3 produced a contract for a future tiny program.

S4 now implements that tiny program, but only as an audit/replay machine.

The core question:

> Can a small implementation replay S2-style finite records through T1–T9, expose boundary-source provenance, reject oracle leaks, downgrade claim strength, and pass mutation tests that would catch direct lookup or hidden semantic-oracle behavior?

---

## 2. Required decision vocabulary

Use exactly one:

```text
S4-PASS-TINY-IMPLEMENTATION-AUDIT-OK
S4-FAIL-LOOKUP-BEHAVIOR
S4-FAIL-PROVENANCE-VALIDATION
S4-FAIL-ORACLE-FIELD-REJECTION
S4-FAIL-MUTATION-SUITE
S4-FAIL-CLAIM-STRENGTH-DOWNGRADE
S4-FAIL-BOUNDARY-GENERATOR-OVERCLAIM
S4-FAIL-CL-MISTAKE-REPEATED
S4-INCONCLUSIVE
HALT-GOAL-DRIFT
```

Meanings:

```text
S4-PASS-TINY-IMPLEMENTATION-AUDIT-OK
- The tiny implementation satisfies S3’s audit/replay contract.

S4-FAIL-LOOKUP-BEHAVIOR
- claim_id or expression_id determines status directly.

S4-FAIL-PROVENANCE-VALIDATION
- records without provenance are accepted.

S4-FAIL-ORACLE-FIELD-REJECTION
- forbidden semantic/truth/final-status fields are accepted.

S4-FAIL-MUTATION-SUITE
- required mutation tests are missing or fail.

S4-FAIL-CLAIM-STRENGTH-DOWNGRADE
- stronger claims are allowed or downgrade output is missing.

S4-FAIL-BOUNDARY-GENERATOR-OVERCLAIM
- implementation or report describes the engine as generating meaning/boundary/truth.

S4-FAIL-CL-MISTAKE-REPEATED
- implementation treats preconditions, authored fields, or rule replay as substrate/derivability/learner evidence.

S4-INCONCLUSIVE
- partial implementation exists but cannot support a pass.

HALT-GOAL-DRIFT
- work turns into general framework, learner, Sanskrit work, LLM work, philosophical essay, or unbounded implementation.
```

---

## 3. Required input files

Read these files if present:

```text
research/MAP-S0_Derivational_Semantic_Ecology.md
research/MAP-S1_Literature-grounded_Constraint_Refinement.md
research/closed_directions_ledger.md

experiments/S/S0_Anti-Sophistry_Future-Meaning_Admissibility_Gate.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_decision.json
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_report.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_case_table.md
experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_goodhart_audit.md

experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_decision.json
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_microformal_schema.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_transition_rules.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_case_replay.md
experiments/S/S1_microformalization_of_semantic_status_transitions/S1_goodhart_guards.md

experiments/S/S2_Toy_Model_Specification_for_Semantic_Status_Transitions.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_decision.json
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_toy_model_domains.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_operational_rules.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_case_replay_protocol.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_goodhart_control_protocol.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_oracle_leakage_audit.md

experiments/B/B0_Boundary-Origin_Claim-Strength_Ledger.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_decision.json
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_report.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_boundary_source_ledger.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_claim_strength_table.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_s2_reinterpretation.md

experiments/S/S3_Tiny_Implementation_Spec_for_Boundary_Accounting_Replay_Protocol.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_decision.json
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_report.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_program_contract.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_input_schema.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_output_schema.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_replay_algorithm_spec.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_mutation_test_plan.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_oracle_leakage_controls.md
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_failure_analysis.md
```

If files are missing, list them as `MISSING`.

Continue only if S3 decision exists and is:

```text
S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION
```

---

## 4. Allowed output directory

Create:

```text
experiments/S/S4_tiny_boundary_accounting_replay_implementation/
```

Inside it, create exactly these top-level files/directories:

```text
README.md
S4_report.md
S4_decision.json
boundary_replay_engine.py
run_s4.py
data/cases.json
data/mutations.json
outputs/replay_results.json
outputs/mutation_results.json
outputs/oracle_rejection_results.json
outputs/provenance_validation_results.json
outputs/claim_strength_audit.json
outputs/static_audit.json
outputs/final_audit_summary.md
```

You may create `data/` and `outputs/` directories inside the S4 directory.

Do not modify files outside the S4 output directory.

Do not edit MAP files.

Do not edit S0/S1/S2/S3/B0 files.

Do not edit `research/closed_directions_ledger.md`.

Commit required after successful completion.

---

## 5. Implementation constraints

Use:

```text
Python 3
standard library only
no external dependencies
no network
no model calls
no LLM calls
no Sanskrit parser
no machine learning
```

The implementation must be small and auditable.

Forbidden:

```text
direct dictionary mapping claim_id -> final_status
direct dictionary mapping expression_id -> final_status
input field final_status
input field expected_final_status
input field future_meaning_possible
input field obvious_nonsense
input field inside_boundary
input field truth_label
input field semantic_label
input field safe_label_as_truth
input field derived_label
input field substrate_label
runtime human judgement
real-world fact lookup
Sanskrit/Panini truth oracle
population agreement as truth
protective boundary as truth
human-authored fields as derived evidence
toy outcome token as external truth contact
rule replay as semantic generation
```

---

## 6. Required engine behavior

Implement `boundary_replay_engine.py`.

It must expose at least these functions:

```python
load_json(path: str) -> dict | list
validate_record(record: dict) -> list[dict]
replay_record(record: dict) -> dict
compute_goodhart_flags(record: dict) -> list[str]
compute_claim_strength(record: dict, replay: dict) -> dict
run_mutation_tests(cases: list[dict], mutations: list[dict]) -> dict
run_static_audit(source_paths: list[str]) -> dict
```

Function names may be extended, but these must exist.

### 6.1 Required statuses

Use exactly:

```text
FORMED
POETIC
SUSPENDED
LOCAL
STABLE
KILLED
DANGEROUS
```

### 6.2 Required boundary sources

Use exactly:

```text
FORM_BOUNDARY
CONSEQUENCE_BOUNDARY
VIABILITY_BOUNDARY
RULE_GENERATED_BOUNDARY
HUMAN_AUTHORED_BOUNDARY
POPULATION_BOUNDARY
UNKNOWN_OR_MIXED_BOUNDARY
```

### 6.3 Required claim-strength levels

Use exactly:

```text
FORM_ONLY
BOUNDARY_ACCOUNTING
TOY_REPLAY_DETERMINISTIC
TOY_CONSEQUENCE_PROTOCOL
VIABILITY_SHIELD
EXTERNAL_CONTACT_REQUIRED
RULE_GENERATED_CONTENT
DERIVATION_EVIDENCE
SUBSTRATE_CLAIM
```

In S4, the engine must never place these in `allowed_claim_strength`:

```text
RULE_GENERATED_CONTENT
DERIVATION_EVIDENCE
SUBSTRATE_CLAIM
```

They must appear in `forbidden_overclaims`.

---

## 7. Required input schema enforcement

Every case record in `data/cases.json` must contain:

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

The engine must reject a record if:

```text
any required field is absent
any field has no boundary_source_by_field entry
any field has no field_provenance entry
any boundary source is outside allowed taxonomy
boundary_source_by_field and field_provenance disagree materially
initial_status is not UNINITIALIZED
any forbidden oracle field appears
```

Rejected records must appear in:

```text
outputs/oracle_rejection_results.json
outputs/provenance_validation_results.json
```

---

## 8. Required case records

`data/cases.json` must include at least the seven S0 cases:

```text
A_liquid_powder
B_hereditary_infertility
C_square_circle
D_everything_true_in_context
E_x_related_to_y_somehow
F_translucent_causal_sweetness_field
G_light_wave_particle_pair
```

Each record must be built from finite S2-style fields.

Important:

```text
Do not include final_status.
Do not include expected_final_status.
Do not include hidden labels like future_meaning_possible or obvious_nonsense.
```

The engine may produce the expected statuses by rules, but the inputs must not contain them.

---

## 9. Required replay algorithm

`replay_record(record)` must apply this fixed order:

```text
1. Validate record schema.
2. Reject forbidden oracle fields.
3. Validate finite domain membership where implemented.
4. Validate provenance for every field.
5. Initialize status only through T1.
6. Apply T7 danger predicates.
7. Apply T6 declared-scope kill predicates.
8. Apply T2 poetic rule.
9. Apply T3 suspension rule.
10. Apply T4 localization rule.
11. Apply T8 local dualism rule.
12. Apply T5 stability rule.
13. Apply T9 downgrade rule only if prior STABLE exists.
14. Compute active Goodhart flags.
15. Compute boundary-source provenance summary.
16. Compute allowed claim strength.
17. Emit audit record.
```

Every replay result must include:

```text
claim_id
expression_id
final_status
transition_trace
blocked_transitions
active_goodhart_flags
boundary_sources_used
dominant_boundary_source
allowed_claim_strength
forbidden_overclaims
downgrade_reason
oracle_leakage_warnings
cl_mistake_warnings
runtime_decision
```

For every transition attempt, `transition_trace` must include:

```text
rule_id
preconditions_checked
fields_consulted
boundary_sources_consulted
status_before
status_after
blocked_by
warning_ids
```

---

## 10. Required operational rule behavior

Implement minimal T1–T9 behavior sufficient for S4.

### T1 — Birth

If:

```text
expression_id present
derivation_trace non-empty
primitives non-empty
initial_status == UNINITIALIZED
```

then status may become `FORMED`.

### T7 — Dangerous

If:

```text
danger_condition == true
or CONTEXT_PROLIFERATION_PROXY active
or GRAMMAR_PROXY used to promote beyond POETIC
or POPULATION_PROXY used to promote to truth/STABLE without consequence/anchor
or protective boundary reported as truth
```

then status becomes `DANGEROUS`, and `T5` must be blocked.

### T6 — Killed

If:

```text
declared_scope_failure == true
or candidate_outcomes contains AXIOMS_INCOMPATIBLE under EUCLIDEAN_GEOMETRY
or same_scope_contradiction_without_repair == true
```

then status may become `KILLED`, unless T7 has already set `DANGEROUS`.

### T2 — Poetic

If:

```text
status == FORMED
and derivation_trace contains PSEUDO_TERM or poetic_marker == true
and no operational upgrade preconditions hold
```

then status may become `POETIC`.

### T3 — Suspended

If:

```text
status in {FORMED, POETIC}
and contradiction_or_underdefined_ontology == true
and extension_path_count > 0
and danger_condition == false
```

then status may become `SUSPENDED`.

### T4 — Local

If:

```text
status == SUSPENDED
and scope explicit
and assumptions non-empty
and candidate_tests non-empty
and candidate_outcomes include expected and contrast outcomes
and consequence_delta == true
and scope_cost > 0 for created/non-default scope
and scope_lineage present for created/non-default scope
and no blocking Goodhart flag active
```

then status may become `LOCAL`.

### T8 — Local dualism

If:

```text
paired_claims == true
and both sides have distinct scopes/tests
and contradiction_links explicit
and consequence differences preserved
and no explosion flag
```

then pair may remain `LOCAL`.

### T5 — Stable

If:

```text
status == LOCAL
and all required toy tests have expected outcomes and contrast outcomes
and contradiction contained
and adversarial paraphrase survived
and at least one non-population anchor exists
and population conditions pass
and no Goodhart flag active
```

then status may become `STABLE`.

S4 may have no STABLE happy-path case. That is acceptable.

### T9 — Stable downgrade

If:

```text
prior status is STABLE
and later finite failure token appears
```

downgrade according to failure token.

---

## 11. Required Goodhart flags

Implement recomputation of at least:

```text
VOLUME_PROXY
COHERENCE_PROXY
CONTRADICTION_MINIMIZATION_PROXY
CONTEXT_PROLIFERATION_PROXY
GRAMMAR_PROXY
POPULATION_PROXY
```

Minimum activation rules:

```text
VOLUME_PROXY:
  relation_type == UNSPECIFIED
  or consequence_obligations empty
  or attempted_progress_metric in {claim_count, term_count, relation_count}

COHERENCE_PROXY:
  coherence_score == HIGH
  and (candidate_tests empty or anchors empty or all outcomes UNTESTED)

CONTRADICTION_MINIMIZATION_PROXY:
  contradiction_links non-empty
  and attempted_transition == T6
  and (extension_path_count > 0 or local_dualism_available == true)

CONTEXT_PROLIFERATION_PROXY:
  new_scope_requested == true
  and (scope_cost == 0 or scope_lineage absent or consequence_delta == false or assumptions empty)

GRAMMAR_PROXY:
  derivation_trace non-empty
  and attempted_transition in {T4, T5}
  and (candidate_tests empty or OPERATIONAL_ROLE_ABSENT in candidate_outcomes)

POPULATION_PROXY:
  population_state.usage_state == STABLE_USAGE
  and (population_state.paraphrase_state != SURVIVED
       or anchors subset only POPULATION_STABILITY_ANCHOR
       or candidate_tests empty)
```

---

## 12. Required mutation tests

Create `data/mutations.json` and implement M1–M6.

Each mutation test must include:

```text
test_id
source_case_id
mutation_description
field_changes
expected_behavior
lookup_failure_condition
oracle_failure_condition
```

Required tests:

### M1 — Remove extension path from A

Mutation:

```text
source_case_id = A_liquid_powder
extension_path_count = 0
remove new_material_class_possible from assumptions
```

Expected:

```text
SUSPENDED should no longer be justified.
T3 blocked.
```

Failure if:

```text
expression_id == liquid_powder still forces SUSPENDED.
```

### M2 — Add free context to C

Mutation:

```text
source_case_id = C_square_circle
new_scope_requested = true
scope_cost = 0
scope_lineage = absent
consequence_delta = false
```

Expected:

```text
CONTEXT_PROLIFERATION_PROXY active.
DANGEROUS considered before any context-rescue LOCAL.
```

Failure if:

```text
square_circle always forces KILLED and ignores context laundering fields.
```

### M3 — Type relation in E

Mutation:

```text
source_case_id = E_x_related_to_y_somehow
relation_type = SPECIFIED
candidate_tests include T_RELATION_DISCRIMINATION
candidate_outcomes include RELATION_TYPED and contrast outcome
consequence_delta = true
```

Expected:

```text
VOLUME_PROXY no longer blocks solely due to unspecified relation.
T4 may become possible if other LOCAL preconditions satisfy.
```

Failure if:

```text
expression_id always forces FORMED.
```

### M4 — Remove scope distinction from G

Mutation:

```text
source_case_id = G_light_wave_particle_pair
same scope and same tests for both sides
```

Expected:

```text
T8 blocked.
Local dualism should fail.
```

Failure if:

```text
light_wave/light_particle always force LOCAL dualism.
```

### M5 — Add population-only stability to F

Mutation:

```text
source_case_id = F_translucent_causal_sweetness_field
population_state.usage_state = STABLE_USAGE
anchors = {POPULATION_STABILITY_ANCHOR}
no non-population anchor
no operational role
```

Expected:

```text
POPULATION_PROXY active.
T5 blocked.
STABLE forbidden.
```

Failure if:

```text
population agreement is treated as truth.
```

### M6 — Swap expression names with decisive fields preserved

Mutation:

```text
source_case_id = E_x_related_to_y_somehow
expression_id = square_circle
keep E relation-unspecified fields
```

Expected:

```text
Status follows fields, not expression name.
Output must not become KILLED solely from expression_id.
May emit finite-domain consistency warning.
```

Failure if:

```text
expression_id == square_circle forces KILLED.
```

Mutation results must be written to:

```text
outputs/mutation_results.json
```

---

## 13. Required oracle/provenance negative tests

In addition to M1–M6, S4 must test at least these rejection cases:

### O1 — Forbidden final status field

Add:

```text
final_status = STABLE
```

Expected:

```text
record rejected
oracle_leakage_warning includes FORBIDDEN_INPUT_FIELD
```

### O2 — Missing provenance

Remove `field_provenance` for one decisive field.

Expected:

```text
record rejected
runtime_decision = REJECT_PROVENANCE_MISSING
```

### O3 — Truth label field

Add:

```text
truth_label = true
```

Expected:

```text
record rejected
oracle_leakage_warning includes FORBIDDEN_INPUT_FIELD
```

### O4 — Initial status bypass

Set:

```text
initial_status = STABLE
```

Expected:

```text
record rejected or blocked
T1-only initialization preserved
```

Write results to:

```text
outputs/oracle_rejection_results.json
outputs/provenance_validation_results.json
```

---

## 14. Required static audit

`run_static_audit` must inspect S4 source files for forbidden patterns.

Minimum checks:

```text
"final_status_by_claim"
"status_by_claim"
"final_status_by_expression"
"status_by_expression"
"expected_final_status"
"future_meaning_possible"
"obvious_nonsense"
"truth_label"
"semantic_label"
"substrate_label"
```

The static audit should be simple string scanning. It must avoid false-positive failure from documented forbidden field lists if possible by limiting checks to executable code files, especially `boundary_replay_engine.py` and `run_s4.py`.

Write:

```text
outputs/static_audit.json
```

---

## 15. Required run script

Implement `run_s4.py`.

It must:

```text
load data/cases.json
replay all valid cases
run mutation tests M1–M6
run oracle/provenance negative tests O1–O4
run static audit
write all outputs
write S4_decision.json
write S4_report.md or ensure it is updated after run
print compact summary
exit nonzero if pass conditions fail
```

---

## 16. Required outputs

### 16.1 `outputs/replay_results.json`

Must include one result per base case with full audit output.

### 16.2 `outputs/mutation_results.json`

Must include M1–M6 with pass/fail and reasons.

### 16.3 `outputs/oracle_rejection_results.json`

Must include O1/O3 and any forbidden-field rejection tests.

### 16.4 `outputs/provenance_validation_results.json`

Must include O2/O4 and provenance/init validation results.

### 16.5 `outputs/claim_strength_audit.json`

Must summarize allowed strengths and forbidden overclaims for all base cases and mutations.

### 16.6 `outputs/static_audit.json`

Must show forbidden lookup/static pattern results.

### 16.7 `outputs/final_audit_summary.md`

Must summarize:

```text
base replay count
mutation pass count
oracle rejection pass count
provenance validation pass count
static audit result
claim-strength downgrade result
overall audit result
```

### 16.8 `S4_report.md`

Must contain exactly:

```text
# S4 — Tiny Boundary-Accounting / Replay Implementation

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. S3 constraints carried forward
## 4. Implementation summary
## 5. Base replay results
## 6. Mutation test results
## 7. Oracle / provenance rejection results
## 8. Static audit results
## 9. Claim-strength downgrade audit
## 10. Pass / fail analysis
## 11. What was NOT shown
## 12. Downstream permission
## 13. Durable result
```

### 16.9 `S4_decision.json`

Must be valid JSON:

```json
{
  "decision": "...",
  "reason": "...",
  "s3_decision_confirmed": false,
  "implementation_completed": false,
  "base_replay_completed": false,
  "mutation_tests_passed": false,
  "oracle_field_rejection_passed": false,
  "provenance_validation_passed": false,
  "static_audit_passed": false,
  "claim_strength_downgrade_passed": false,
  "lookup_behavior_detected": false,
  "oracle_leakage_detected": false,
  "boundary_generator_overclaim_detected": false,
  "cl_mistake_repeated": false,
  "admissible_for_postmortem_or_next_gate": false,
  "llm_training_allowed": false,
  "substrate_claim_allowed": false,
  "derivability_claim_allowed": false,
  "semantic_boundary_generator_claim_allowed": false,
  "next_allowed_work": []
}
```

Set `implementation_completed: true` only if code exists and run succeeded.

Set `mutation_tests_passed: true` only if all M1–M6 pass.

Set `oracle_field_rejection_passed: true` only if O1/O3 pass.

Set `provenance_validation_passed: true` only if O2/O4 pass.

Set `static_audit_passed: true` only if no forbidden executable-code patterns are found.

Never set:

```json
"llm_training_allowed": true
"substrate_claim_allowed": true
"derivability_claim_allowed": true
"semantic_boundary_generator_claim_allowed": true
```

If S4 passes, allowed next work is one of:

```text
S4 postmortem / demo packaging
S5 boundary-accounting demo spec
B1 external-contact route analysis
```

Do not allow LLM/model/substrate work.

---

## 17. Pass conditions

S4 passes only if all hold:

```text
1. S3 pass is confirmed.
2. Code exists only inside S4 output directory.
3. Program is boundary-accounting / replay engine only.
4. Base cases A–G replay without forbidden input fields.
5. Every input field has provenance.
6. Missing provenance is rejected.
7. Forbidden oracle fields are rejected.
8. Replay output includes transition trace, blockers, boundary sources, allowed claim strength, forbidden overclaims, and warnings.
9. No claim_id/expression_id lookup behavior is detected.
10. M1–M6 mutation tests pass.
11. O1–O4 rejection tests pass.
12. Static audit passes.
13. Claim-strength downgrade never allows RULE_GENERATED_CONTENT, DERIVATION_EVIDENCE, or SUBSTRATE_CLAIM.
14. No boundary-generator, meaning-generator, grounding, substrate, derivability, LLM-safety, learner-evidence, or world-transfer claim is made.
```

---

## 18. Failure conditions

Fail as `S4-FAIL-LOOKUP-BEHAVIOR` if mutation tests or static audit detect ID/expression lookup.

Fail as `S4-FAIL-PROVENANCE-VALIDATION` if records without provenance are accepted.

Fail as `S4-FAIL-ORACLE-FIELD-REJECTION` if forbidden fields are accepted.

Fail as `S4-FAIL-MUTATION-SUITE` if any required mutation test fails or is absent.

Fail as `S4-FAIL-CLAIM-STRENGTH-DOWNGRADE` if forbidden overclaim levels are allowed.

Fail as `S4-FAIL-BOUNDARY-GENERATOR-OVERCLAIM` if reports or code comments claim meaning/boundary generation.

Fail as `S4-FAIL-CL-MISTAKE-REPEATED` if preconditions/authored fields/replay are treated as substrate, derivability, learner evidence, or world transfer.

Fail as `S4-INCONCLUSIVE` if implementation is partial or outputs are incomplete.

Fail as `HALT-GOAL-DRIFT` if task expands beyond tiny audit/replay implementation.

---

## 19. Mandatory “what was NOT shown”

Include in `S4_report.md`:

```text
- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No semantic boundary generator was implemented.
- No meaning generator was implemented.
- No claim that S2/S3/S4 generates semantic boundary.
- No claim that protective boundary is truth.
- No claim that grammar boundary is semantic.
- No claim that human-authored boundary is derived.
- No claim that toy replay transfers to real language.
- No claim that boundary accounting is meaning.
- No claim that passing mutation tests proves the direction works.
```

---

## 20. Required commands

From repository root, after creating the files:

```bash
python3 experiments/S/S4_tiny_boundary_accounting_replay_implementation/run_s4.py
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/S4_decision.json >/dev/null
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/outputs/replay_results.json >/dev/null
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/outputs/mutation_results.json >/dev/null
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/outputs/oracle_rejection_results.json >/dev/null
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/outputs/provenance_validation_results.json >/dev/null
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/outputs/claim_strength_audit.json >/dev/null
python3 -m json.tool experiments/S/S4_tiny_boundary_accounting_replay_implementation/outputs/static_audit.json >/dev/null
```

---

## 21. Git discipline

Before making changes, run:

```bash
git status --short
```

Record whether the worktree was clean in the final report.

After writing and running outputs:

```bash
git status --short
git diff -- experiments/S/S4_tiny_boundary_accounting_replay_implementation/
```

Stage only the allowed S4 output directory:

```bash
git add experiments/S/S4_tiny_boundary_accounting_replay_implementation/
```

Also stage the S4 spec file only if it was newly created in this task:

```bash
git add experiments/S/S4_Tiny_Boundary_Accounting_Replay_Implementation.md
```

Do not stage MAP files.

Do not stage S0/S1/S2/S3/B0 files.

Do not stage `research/closed_directions_ledger.md`.

Commit with:

```bash
git commit -m "Add S4 boundary accounting replay implementation"
```

After commit:

```bash
git status --short
git log -1 --oneline
```

Final response must include:

```text
- S4 decision
- files created
- commands run
- JSON validation status
- commit hash
- whether unrelated changes remain unstaged
```

---

## 22. Final instruction

The desired result is not “a meaning engine”.

The desired result is a tiny audit/replay implementation that makes hidden oracles, lookup behavior, missing provenance, Goodhart overclaiming, and claim-strength inflation visible.

If S4 passes, it proves only:

> a bounded boundary-accounting / replay machine can be implemented for the toy S-records.

It does not prove meaning, grounding, derivability, substrate, or LLM safety.

