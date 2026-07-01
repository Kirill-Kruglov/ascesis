# S3 — Tiny Implementation Spec for Boundary-Accounting / Replay Protocol

## 0. Verdict

`S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION`

B0 decision was confirmed as `B0-PASS-BOUNDARY-SOURCES-SEPARATED`.
S3 specifies only a future tiny boundary-accounting / replay engine. It does
not implement code and does not permit implementation in S3.

The admissible future program is an audit machine: it accepts finite records
with provenance, rejects forbidden oracle fields, replays T1-T9, reports
transition traces and blockers, computes Goodhart flags, reports boundary
sources, downgrades claim strength, and emits oracle / CL warnings.

## 1. Goal anchor

The immutable project goal is to train an LLM / learner so that its world-model
is derived, not merely generalized from internet-like data.

S3 serves that goal only by specifying how a future tiny program could preserve
boundary provenance and prevent overclaiming. S3 does not show derivation,
substrate, grounding, representation, LLM safety, or learner evidence.

## 2. Inputs used

| file | role | status |
|---|---|---|
| `experiments/S/S3_Tiny_Implementation_Spec_for_Boundary_Accounting_Replay_Protocol.md` | Primary S3 specification | PRESENT |
| `research/MAP-S0_Derivational_Semantic_Ecology.md` | Constraint context | PRESENT |
| `research/MAP-S1_Literature-grounded_Constraint_Refinement.md` | Constraint context | PRESENT |
| `research/closed_directions_ledger.md` | CL closure constraints | PRESENT |
| `experiments/S/S0_Anti-Sophistry_Future-Meaning_Admissibility_Gate.md` | S0 task | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_report.md` | S0 result | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_decision.json` | S0 decision | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_case_table.md` | S0 cases | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_assumption_graphs.md` | S0 assumptions | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_goodhart_audit.md` | S0 guards | PRESENT |
| `experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md` | S1 task | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_report.md` | S1 result | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_decision.json` | S1 decision | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_microformal_schema.md` | S1 schema | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_transition_rules.md` | S1 rules | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_case_replay.md` | S1 replay | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_goodhart_guards.md` | S1 guards | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_failure_analysis.md` | S1 failure analysis | PRESENT |
| `experiments/S/S2_Toy_Model_Specification_for_Semantic_Status_Transitions.md` | S2 task | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_report.md` | S2 result | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_decision.json` | S2 decision | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_toy_model_domains.md` | S2 domains | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_operational_rules.md` | S2 rules | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_case_replay_protocol.md` | S2 replay | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_goodhart_control_protocol.md` | S2 guards | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_oracle_leakage_audit.md` | S2 oracle / CL audit | PRESENT |
| `experiments/S/S2_toy_model_specification_for_semantic_status_transitions/S2_failure_analysis.md` | S2 failure analysis | PRESENT |
| `experiments/B/B0_Boundary-Origin_Claim-Strength_Ledger.md` | B0 task | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_report.md` | B0 result | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_decision.json` | B0 decision | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_boundary_source_ledger.md` | B0 source ledger | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_claim_strength_table.md` | B0 claim strengths | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_trilemma_map.md` | B0 trilemma | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_s2_reinterpretation.md` | B0 S2 reinterpretation | PRESENT |
| `experiments/B/B0_boundary_origin_claim_strength_ledger/B0_failure_analysis.md` | B0 failure analysis | PRESENT |

Pre-change worktree state:
not clean. Existing untracked unrelated files and directories were present,
including S0/S1/S2/S3 task specs, B0 task spec, CL materials, MAP files,
ledger, and other experiment trees. S3 changed only the allowed output
directory.

## 3. B0 constraints carried forward

1. S2 is boundary accounting / toy replay, not a boundary generator.
2. Human-authored fields are not derived evidence.
3. Protective / viability boundaries are not truth.
4. Grammar / derivation boundaries are not semantic boundaries.
5. Rule replay is not meaningful without consequence pressure.
6. Toy boundaries do not transfer to real language without a transfer gate.
7. S3 may be only a tiny implementation spec for accounting / replay.

## 4. Program contract summary

`S3_program_contract.md` defines the future program only as a
boundary-accounting / replay engine.

It may validate finite domains, reject oracle fields, validate provenance,
apply T1-T9, activate Goodhart flags, record blockers, classify boundary
sources, compute claim strength, run mutation tests, and emit audit outputs.

It must not be described as a semantic engine, meaning generator, boundary
generator, truth detector, grounding system, or substrate prototype.

## 5. Input schema summary

`S3_input_schema.md` defines all required fields:

```text
claim_id, expression_id, primitives, derivation_trace, initial_status, scope,
assumptions, candidate_tests, candidate_outcomes, anchors, population_state,
contradiction_links, extension_path_count, scope_cost, scope_lineage,
consequence_delta, goodhart_flags_initial, attempted_transition,
danger_condition, boundary_source_by_field, field_provenance
```

Every field must carry provenance from the B0 taxonomy. Forbidden oracle fields
such as `final_status`, `expected_final_status`, `truth_label`,
`semantic_label`, `derived_label`, and `substrate_label` must be rejected.

## 6. Output schema summary

`S3_output_schema.md` requires:

```text
claim_id, expression_id, final_status, transition_trace, blocked_transitions,
active_goodhart_flags, boundary_sources_used, dominant_boundary_source,
allowed_claim_strength, forbidden_overclaims, downgrade_reason,
oracle_leakage_warnings, cl_mistake_warnings, mutation_test_results,
runtime_decision
```

Outputs must include status, transition trace, blockers, boundary sources,
allowed strength, forbidden overclaims, and warnings.

## 7. Replay algorithm summary

`S3_replay_algorithm_spec.md` specifies fixed replay order:

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
13. Apply T9 downgrade rule only if prior `STABLE` exists.
14. Compute active Goodhart flags.
15. Compute boundary-source provenance summary.
16. Compute allowed claim strength.
17. Emit audit record.

## 8. Anti-lookup and mutation-test summary

The spec bans `claim_id -> final_status` and `expression_id -> final_status`
lookup maps. It also rejects any input status labels that would turn replay
into oracle copying.

`S3_mutation_test_plan.md` defines:

- M1 remove extension path from A;
- M2 add free context to C;
- M3 type the relation in E;
- M4 remove scope distinction from G;
- M5 add population-only stability to F;
- M6 swap expression names with decisive fields preserved.

These tests force status to follow fields and rules rather than claim name or
expression name.

## 9. Oracle leakage control summary

`S3_oracle_leakage_controls.md` defines warnings for forbidden input fields,
direct ID lookup, runtime human judgement, real-world truth lookup,
Sanskrit/Panini truth oracle, population-as-truth, protective-as-truth,
human-authored-as-derived, toy-outcome-as-external-truth, and
rule-replay-as-semantic-generation.

It also defines CL mistake warnings for preconditions as substrate,
hand-authored fields as learner evidence, rule priors as learning, viability as
derivability, premature representation/LLM work, and toy replay as world
transfer.

## 10. Claim-strength downgrade summary

Allowed strengths are capped:

- `FORM_BOUNDARY` allows at most `FORM_ONLY`.
- `HUMAN_AUTHORED_BOUNDARY` allows at most `BOUNDARY_ACCOUNTING` or `TOY_REPLAY_DETERMINISTIC`.
- Toy `CONSEQUENCE_BOUNDARY` allows at most `TOY_CONSEQUENCE_PROTOCOL`.
- `VIABILITY_BOUNDARY` allows at most caveated `VIABILITY_SHIELD`.
- Absent external contact reports `EXTERNAL_CONTACT_REQUIRED`, not derivation evidence.
- Rule processing over supplied fields allows at most `TOY_REPLAY_DETERMINISTIC`.

In S3, `RULE_GENERATED_CONTENT`, `DERIVATION_EVIDENCE`, and
`SUBSTRATE_CLAIM` are always forbidden overclaims.

## 11. Pass / fail analysis

S3 passes because:

1. B0 pass is confirmed.
2. Program is specified only as boundary-accounting / replay engine.
3. Input schema requires provenance for every field.
4. Forbidden oracle fields are rejected.
5. Output schema includes status, transition trace, blocked transitions, boundary sources, allowed claim strength, forbidden overclaims, and warnings.
6. Replay algorithm uses T1-T9 and fixed order.
7. `claim_id` / `expression_id` cannot determine final status directly.
8. Mutation tests M1-M6 are defined and strong enough to catch lookup/oracle behavior.
9. Oracle leakage controls are explicit.
10. CL mistake controls are explicit.
11. Claim-strength downgrade logic is explicit.
12. No implementation, code, experiment, model training, substrate claim, derivability claim, grounding claim, or LLM-safety claim is made.

## 12. What was NOT shown

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

## 13. Downstream permission

Allowed next work:

```text
S4 tiny implementation task
```

Not allowed by S3:

- implementation in this gate;
- experiments;
- model training;
- Sanskrit experiment;
- substrate claim;
- derivability claim;
- grounding claim;
- representation claim;
- LLM-safety claim;
- semantic / boundary generator claim.

## 14. Durable result

S3 turns B0's boundary-origin discipline into a precise future implementation
spec. The durable result is not a working program and not evidence of meaning.
It is a bounded contract for a later audit/replay machine where provenance,
transition traces, Goodhart flags, oracle warnings, CL warnings, and
claim-strength downgrades are required output.
