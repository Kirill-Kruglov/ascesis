# S3 — Tiny Implementation Spec for Boundary-Accounting / Replay Protocol

**File:** `experiments/S/S3_Tiny_Implementation_Spec_for_Boundary_Accounting_Replay_Protocol.md`
**Task type:** tiny implementation specification gate
**Status:** post-B0, pre-code
**No implementation. No code. No experiments. No LLM training.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest S-branch status after B0:

> S2 is not a boundary generator. S2 is a finite boundary-accounting / toy replay protocol over human-authored fields, toy consequence tokens, viability guards, and deterministic rules.

S3 exists only because B0 passed as:

```text id="5kbs04"
B0-PASS-BOUNDARY-SOURCES-SEPARATED
```

S3 may specify a tiny implementation **only** for:

```text id="m3gqh7"
boundary accounting
+
deterministic replay protocol
+
provenance audit
+
claim-strength downgrade audit
```

S3 must not specify a semantic boundary generator.

---

## 1. Why S3 exists

S2 provided finite toy domains and deterministic replay protocols.

B0 then downgraded S2:

```text id="bi7z99"
S2 is a boundary-accounting / toy replay protocol, not a boundary generator.
```

The next safe step is not “implement meaning”.

The next safe step is:

> specify a tiny program that takes explicitly supplied finite fields, applies T1–T9, and outputs status, blocked transitions, boundary-source provenance, Goodhart flags, and allowed claim strength.

S3 must make it impossible to hide a semantic oracle inside implementation defaults.

---

## 2. Gate question

Can we write a tiny implementation specification for the S2 replay/accounting protocol such that:

```text id="gsjdnf"
1. no claim_id / expression_id direct lookup determines final status;
2. every input field has provenance;
3. every output status has a transition trace;
4. every boundary source is reported;
5. every claim-strength overclaim is downgraded;
6. mutation tests expose hidden oracle / lookup behavior;
7. implementation remains strictly an audit/replay engine, not a semantic boundary generator?
```

---

## 3. Required decision vocabulary

Use exactly one:

```text id="h4d9jy"
S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION
S3-FAIL-LOOKUP-TABLE-RISK
S3-FAIL-PROVENANCE-MISSING
S3-FAIL-MUTATION-TESTS-INSUFFICIENT
S3-FAIL-BOUNDARY-GENERATOR-OVERCLAIM
S3-FAIL-CLAIM-STRENGTH-DOWNGRADE-MISSING
S3-FAIL-ORACLE-LEAKAGE-RISK
S3-FAIL-REPEATS-CL-MISTAKES
S3-INCONCLUSIVE
HALT-GOAL-DRIFT
```

Meaning:

```text id="mgyw7l"
S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION
- The implementation spec is precise and bounded enough that actual code may be written later.

S3-FAIL-LOOKUP-TABLE-RISK
- The spec allows direct mapping from claim_id/expression_id to final status.

S3-FAIL-PROVENANCE-MISSING
- Inputs/outputs do not require boundary-source provenance.

S3-FAIL-MUTATION-TESTS-INSUFFICIENT
- The spec lacks mutation tests to detect hidden oracle or lookup behavior.

S3-FAIL-BOUNDARY-GENERATOR-OVERCLAIM
- The spec describes the program as generating meaning/boundary rather than accounting/replay.

S3-FAIL-CLAIM-STRENGTH-DOWNGRADE-MISSING
- Outputs omit allowed claim strength and forbidden overclaims.

S3-FAIL-ORACLE-LEAKAGE-RISK
- The spec allows hidden semantic labels, real-world truth lookup, Sanskrit/Panini as truth oracle, or human judgement at runtime.

S3-FAIL-REPEATS-CL-MISTAKES
- The spec treats preconditions, hand-coded fields, or rule priors as substrate / derivability / learner evidence.

S3-INCONCLUSIVE
- The spec is promising but not enough for code.

HALT-GOAL-DRIFT
- Work becomes implementation, philosophy essay, framework naming, Sanskrit worship, learner work, or S-branch overclaiming.
```

---

## 4. Required input files

Read these files if present:

```text id="tmrxdb"
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

experiments/S/S2_Toy_Model_Specification_for_Semantic_Status_Transitions.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_report.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_decision.json
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_toy_model_domains.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_operational_rules.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_case_replay_protocol.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_goodhart_control_protocol.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_oracle_leakage_audit.md
experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_failure_analysis.md

experiments/B/B0_Boundary-Origin_Claim-Strength_Ledger.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_report.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_decision.json
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_boundary_source_ledger.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_claim_strength_table.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_trilemma_map.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_s2_reinterpretation.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_failure_analysis.md
```

If any are missing, list them as `MISSING`.

Continue only if B0 decision exists and is:

```text id="q3o9m7"
B0-PASS-BOUNDARY-SOURCES-SEPARATED
```

---

## 5. Allowed output directory

Create:

```text id="sn6pjx"
experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/
```

Inside it, create exactly:

```text id="hydvpg"
S3_report.md
S3_decision.json
S3_program_contract.md
S3_input_schema.md
S3_output_schema.md
S3_replay_algorithm_spec.md
S3_mutation_test_plan.md
S3_oracle_leakage_controls.md
S3_failure_analysis.md
```

Do not edit files outside this directory.

Do not edit MAP files.

Do not edit S0/S1/S2/B0 files.

Do not edit the closed directions ledger.

Commit required after successful completion.

---

## 6. Required program contract

S3 must specify a tiny future program with this contract:

```text id="6oj8ah"
Input:
  finite S2-style case records with explicit field provenance.

Process:
  validate finite domains;
  apply T1–T9 in fixed replay order;
  activate Goodhart flags;
  record blocked transitions;
  classify boundary sources;
  compute allowed claim strength;
  run mutation tests;
  emit audit outputs.

Output:
  status;
  transition trace;
  blocked transitions;
  active Goodhart flags;
  boundary-source provenance;
  claim-strength downgrade;
  oracle-leakage warnings;
  CL-mistake warnings.
```

The program must be described as:

```text id="lu7ghr"
boundary-accounting / replay engine
```

It must not be described as:

```text id="gjes4a"
semantic engine
meaning generator
boundary generator
truth detector
grounding system
substrate prototype
```

---

## 7. Required input schema

S3 must define an input schema for future implementation.

Minimum required fields:

```text id="tk2tx3"
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

### 7.1 Boundary-source provenance required

Every field must carry one of:

```text id="kp8adg"
FORM_BOUNDARY
CONSEQUENCE_BOUNDARY
VIABILITY_BOUNDARY
RULE_GENERATED_BOUNDARY
HUMAN_AUTHORED_BOUNDARY
POPULATION_BOUNDARY
UNKNOWN_OR_MIXED_BOUNDARY
```

If any input field lacks provenance, the future program must reject the record or emit a blocking audit error.

### 7.2 Forbidden input fields

The future program must reject any record containing fields like:

```text id="2jh7ya"
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

Presence of any such field is an oracle leakage failure.

---

## 8. Required output schema

S3 must define output schema:

```text id="pyi49l"
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
mutation_test_results
runtime_decision
```

Allowed claim strength must be selected from B0 levels:

```text id="2f6qzu"
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

The future program must never output:

```text id="gp2v1o"
RULE_GENERATED_CONTENT
DERIVATION_EVIDENCE
SUBSTRATE_CLAIM
```

unless explicitly configured in a future non-S3 gate. In S3 they are forbidden overclaims.

---

## 9. Required replay algorithm spec

S3 must specify deterministic algorithm steps:

```text id="y7ksxg"
1. Validate record schema.
2. Reject forbidden oracle fields.
3. Validate finite domain membership.
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

Important:

```text id="a6k17a"
claim_id and expression_id may be used only for lookup of finite fields,
not direct final status assignment.
```

---

## 10. Required anti-lookup controls

S3 must specify how future implementation prevents direct lookup.

Required controls:

```text id="8a5nve"
1. No dictionary mapping claim_id -> final_status.
2. No dictionary mapping expression_id -> final_status.
3. No field named final_status / expected_final_status in input.
4. Replay must produce status only from rule preconditions.
5. Mutation tests must change fields while keeping expression_id constant and verify status changes.
6. Mutation tests must swap expression_id while preserving decisive fields and verify status follows fields, not expression name.
```

If the future implementation cannot satisfy these, S3 must fail.

---

## 11. Required mutation test plan

S3 must specify mutation tests sufficient to detect lookup / oracle behavior.

At minimum include:

### M1 — Remove extension path from A

Original:

```text id="7k5r9q"
liquid_powder → SUSPENDED
```

Mutation:

```text id="h5p672"
extension_path_count = 0
new_material_class_possible removed
```

Expected:

```text id="8raazn"
SUSPENDED should no longer be justified.
T3 blocked; T6 or FORM/POETIC fallback must be considered.
```

### M2 — Add free context to C

Original:

```text id="sh67ha"
square_circle under EUCLIDEAN_GEOMETRY → KILLED
```

Mutation:

```text id="b8d0yd"
new_scope_requested = true
scope_cost = 0
scope_lineage = absent
consequence_delta = false
```

Expected:

```text id="2jd2k7"
CONTEXT_PROLIFERATION_PROXY / DANGEROUS should activate.
```

### M3 — Type the relation in E

Original:

```text id="ooji88"
X related to Y somehow → FORMED
```

Mutation:

```text id="x21vws"
relation_type = SPECIFIED
candidate_tests include T_RELATION_DISCRIMINATION
candidate_outcomes include RELATION_TYPED
consequence_delta = true
```

Expected:

```text id="98ls3v"
T4 may become possible if other fields satisfy LOCAL preconditions.
```

### M4 — Remove scope distinction from G

Original:

```text id="1lgmrt"
wave / particle → LOCAL dualism
```

Mutation:

```text id="r0nwnp"
same scope and same tests for both claims
```

Expected:

```text id="5hgqyd"
T8 blocked; contradiction containment must fail to T6 or T7.
```

### M5 — Add population-only stability to F

Original:

```text id="pjn3xq"
pseudo-term → POETIC
```

Mutation:

```text id="oktvzr"
population_state = STABLE_USAGE
anchors = {POPULATION_STABILITY_ANCHOR}
no non-population anchor
no operational role
```

Expected:

```text id="iat9pw"
POPULATION_PROXY blocks T5; STABLE forbidden.
```

### M6 — Swap expression names with decisive fields preserved

Mutation:

```text id="fh8e74"
Use expression_id = square_circle
but fields from Case E relation-unspecified replay.
```

Expected:

```text id="i9x7ha"
Status follows fields, not expression name.
```

If mutation tests are absent or weak, S3 must fail as:

```text id="k477n5"
S3-FAIL-MUTATION-TESTS-INSUFFICIENT
```

---

## 12. Required oracle leakage controls

S3 must define runtime checks for forbidden oracle leakage.

The future program must emit `oracle_leakage_warnings` if:

```text id="e0nim9"
forbidden input fields appear;
claim_id or expression_id determines status directly;
human judgement is requested at runtime;
real-world truth lookup is performed;
Sanskrit/Panini is used as truth oracle;
population agreement is used as truth;
protective / viability boundary is reported as truth;
human-authored field is reported as derived;
toy outcome token is reported as external truth contact;
rule-generated replay is reported as semantic generation.
```

---

## 13. Required CL mistake controls

S3 must define warnings for CL mistakes:

```text id="89nyll"
precondition treated as substrate evidence;
hand-authored fields treated as learner evidence;
rule prior treated as learning evidence;
safe/viability boundary treated as derivability;
representation/LLM work allowed before learner evidence;
toy replay treated as world transfer.
```

Any such warning must block downstream claims.

---

## 14. Required claim-strength downgrade logic

S3 must specify downgrade logic:

```text id="nk0tmm"
If dominant boundary source is FORM_BOUNDARY:
  allowed <= FORM_ONLY.

If dominant source includes HUMAN_AUTHORED_BOUNDARY:
  allowed <= BOUNDARY_ACCOUNTING or TOY_REPLAY_DETERMINISTIC.

If source includes CONSEQUENCE_BOUNDARY only as toy tokens:
  allowed <= TOY_CONSEQUENCE_PROTOCOL.

If source is VIABILITY_BOUNDARY:
  allowed <= VIABILITY_SHIELD with caveat.

If external contact is required but absent:
  allowed includes EXTERNAL_CONTACT_REQUIRED, not DERIVATION_EVIDENCE.

If RULE_GENERATED_BOUNDARY processes supplied fields:
  allowed <= TOY_REPLAY_DETERMINISTIC.

In S3, forbidden overclaims always include:
  RULE_GENERATED_CONTENT
  DERIVATION_EVIDENCE
  SUBSTRATE_CLAIM
```

---

## 15. Required outputs

### 15.1 `S3_program_contract.md`

Must define the future program as boundary-accounting / replay engine only.

### 15.2 `S3_input_schema.md`

Must define required and forbidden input fields.

### 15.3 `S3_output_schema.md`

Must define output fields and claim-strength downgrade requirements.

### 15.4 `S3_replay_algorithm_spec.md`

Must define deterministic replay algorithm and anti-lookup rule.

### 15.5 `S3_mutation_test_plan.md`

Must define M1–M6.

### 15.6 `S3_oracle_leakage_controls.md`

Must define oracle leakage and CL mistake warnings.

### 15.7 `S3_failure_analysis.md`

Must evaluate all S3 failure modes.

### 15.8 `S3_report.md`

Must contain exactly:

```text id="jp9q5k"
# S3 — Tiny Implementation Spec for Boundary-Accounting / Replay Protocol

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. B0 constraints carried forward
## 4. Program contract summary
## 5. Input schema summary
## 6. Output schema summary
## 7. Replay algorithm summary
## 8. Anti-lookup and mutation-test summary
## 9. Oracle leakage control summary
## 10. Claim-strength downgrade summary
## 11. Pass / fail analysis
## 12. What was NOT shown
## 13. Downstream permission
## 14. Durable result
```

### 15.9 `S3_decision.json`

Must be valid JSON:

```json id="zqv6kr"
{
  "decision": "...",
  "reason": "...",
  "b0_decision_confirmed": false,
  "s3_specifies_boundary_accounting_only": false,
  "input_schema_defined": false,
  "output_schema_defined": false,
  "anti_lookup_controls_defined": false,
  "mutation_tests_defined": false,
  "provenance_required_for_all_fields": false,
  "claim_strength_downgrade_defined": false,
  "oracle_leakage_controls_defined": false,
  "cl_mistake_controls_defined": false,
  "admissible_for_tiny_implementation": false,
  "implementation_allowed_by_s3": false,
  "llm_training_allowed": false,
  "substrate_claim_allowed": false,
  "derivability_claim_allowed": false,
  "next_allowed_work": []
}
```

Set:

```json id="gjm1zs"
"b0_decision_confirmed": true
```

only if B0 decision was read and confirmed as:

```text id="iajbao"
B0-PASS-BOUNDARY-SOURCES-SEPARATED
```

Set:

```json id="o37m94"
"admissible_for_tiny_implementation": true
```

only if decision is:

```text id="pce3ic"
S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION
```

Important distinction:

```text id="gnlprj"
admissible_for_tiny_implementation may be true;
implementation_allowed_by_s3 must remain false.
```

S3 is a spec gate. Actual implementation requires a later explicit user decision.

Never set:

```json id="b2g23j"
"implementation_allowed_by_s3": true
"llm_training_allowed": true
"substrate_claim_allowed": true
"derivability_claim_allowed": true
```

If S3 passes, the only allowed next work is:

```json id="u7r2kf"
["S4 tiny implementation task"]
```

---

## 16. Pass conditions

S3 passes only if all hold:

```text id="dn1alw"
1. B0 pass is confirmed.
2. Program is specified only as boundary-accounting / replay engine.
3. Input schema requires provenance for every field.
4. Forbidden oracle fields are rejected.
5. Output schema includes status, transition trace, blocked transitions, boundary sources, allowed claim strength, forbidden overclaims, and warnings.
6. Replay algorithm uses T1–T9 and fixed order.
7. claim_id / expression_id cannot determine final status directly.
8. Mutation tests M1–M6 are defined and strong enough to catch lookup/oracle behavior.
9. Oracle leakage controls are explicit.
10. CL mistake controls are explicit.
11. Claim-strength downgrade logic is explicit.
12. No implementation, code, experiment, model training, substrate claim, derivability claim, grounding claim, or LLM-safety claim is made.
```

---

## 17. Failure conditions

Fail as `S3-FAIL-LOOKUP-TABLE-RISK` if direct ID-to-status mapping is allowed or not tested.

Fail as `S3-FAIL-PROVENANCE-MISSING` if provenance is not required for all fields.

Fail as `S3-FAIL-MUTATION-TESTS-INSUFFICIENT` if mutation tests are absent, weak, or do not distinguish field-driven replay from lookup.

Fail as `S3-FAIL-BOUNDARY-GENERATOR-OVERCLAIM` if the future program is described as generating semantic boundaries.

Fail as `S3-FAIL-CLAIM-STRENGTH-DOWNGRADE-MISSING` if output omits allowed strength / forbidden overclaims.

Fail as `S3-FAIL-ORACLE-LEAKAGE-RISK` if forbidden fields, real-world lookup, Sanskrit truth oracle, population-as-truth, protective-as-truth, or human-authored-as-derived are allowed.

Fail as `S3-FAIL-REPEATS-CL-MISTAKES` if S3 treats hand-authored fields, rule priors, or preconditions as substrate / derivability / learner evidence.

Fail as `S3-INCONCLUSIVE` if the spec is close but not enough for bounded code.

Fail as `HALT-GOAL-DRIFT` if the task becomes implementation, framework naming, philosophy essay, Sanskrit worship, learner work, or S-branch overclaiming.

---

## 18. Mandatory “what was NOT shown”

Include in `S3_report.md`:

```text id="f5rn2q"
- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No implementation is performed by S3.
- No claim that S2 or S3 generates semantic boundary.
- No claim that protective boundary is truth.
- No claim that grammar boundary is semantic.
- No claim that human-authored boundary is derived.
- No claim that toy replay transfers to real language.
- No claim that boundary accounting is meaning.
- No claim that tiny implementation, if later built, would prove the direction.
```

---

## 19. Git discipline

Before making changes, run:

```bash id="ttkyq2"
git status --short
```

Record whether the worktree was clean in the final report.

After writing outputs, validate JSON:

```bash id="momw9l"
python3 -m json.tool experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_decision.json >/dev/null
```

Inspect changes:

```bash id="qqlilj"
git status --short
git diff -- experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/
```

Stage only the allowed S3 output directory:

```bash id="8rye7h"
git add experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/
```

Also stage the S3 spec file only if it was newly created in this task:

```bash id="kl6zeh"
git add experiments/S/S3_Tiny_Implementation_Spec_for_Boundary_Accounting_Replay_Protocol.md
```

Do not stage MAP files.

Do not stage S0/S1/S2/B0 files.

Do not stage `research/closed_directions_ledger.md`.

Commit with:

```bash id="vdcv3z"
git commit -m "Add S3 boundary accounting implementation spec"
```

After commit, run:

```bash id="wzsbnr"
git status --short
git log -1 --oneline
```

Final response must include:

```text id="e4xyuy"
- S3 decision
- files created
- JSON validation status
- commit hash
- whether unrelated changes remain unstaged
```

---

## 20. Final instruction

The desired result is not to unlock implementation at any cost.

The desired result is a safe implementation specification for an audit machine:

> It should make boundary provenance, replay traces, Goodhart guards, oracle warnings, and claim-strength downgrades impossible to hide.

If S3 passes, implementation may be considered later only as S4 tiny implementation task.

If S3 fails, narrow or close according to failure mode.

