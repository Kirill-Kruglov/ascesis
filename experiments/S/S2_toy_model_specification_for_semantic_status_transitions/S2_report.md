# S2 — Toy Model Specification for Semantic Status Transitions

## 0. Verdict

`S2-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION-SPEC`

S1 decision was confirmed as `S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC`.
S2 specifies finite toy domains, operational T1-T9 rules, deterministic replay
protocols for cases A-G, concrete Goodhart activation predicates, and oracle /
CL mistake audits.

This admits only `S3 tiny implementation specification`. S2 does not admit
implementation, experiments, model training, Sanskrit experiments,
representation probes, substrate claims, derivability claims, grounding claims,
or LLM-safety claims.

## 1. Goal anchor

The immutable project goal is to train an LLM / learner so that its world-model
is derived, not merely generalized from internet-like data.

S2 serves that goal only by asking whether S1's status-transition schema can be
made finite and replayable without a hidden human semantic oracle. It does not
claim that the direction works.

## 2. Inputs used

| file | role | status |
|---|---|---|
| `experiments/S/S2_Toy_Model_Specification_for_Semantic_Status_Transitions.md` | Primary S2 specification | PRESENT |
| `research/MAP-S0_Derivational_Semantic_Ecology.md` | Constraint context | PRESENT |
| `research/MAP-S1_Literature-grounded_Constraint_Refinement.md` | Constraint context | PRESENT |
| `research/closed_directions_ledger.md` | Closed CL constraints | PRESENT |
| `experiments/S/S0_Anti-Sophistry_Future-Meaning_Admissibility_Gate.md` | S0 task | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_report.md` | S0 report | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_decision.json` | S0 decision | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_case_table.md` | S0 cases | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_assumption_graphs.md` | S0 assumption graphs | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_goodhart_audit.md` | S0 guards | PRESENT |
| `experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md` | S1 task | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_report.md` | S1 report | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_decision.json` | S1 decision | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_microformal_schema.md` | S1 schema | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_transition_rules.md` | S1 rules | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_case_replay.md` | S1 replay | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_goodhart_guards.md` | S1 guards | PRESENT |
| `experiments/S/S1_microformalization_of_semantic_status_transitions/S1_failure_analysis.md` | S1 failure analysis | PRESENT |

Pre-change worktree state:
not clean. Existing untracked unrelated files and directories were present,
including S0/S1/S2 task specs, CL materials, MAP files, ledger, and other
experiment trees. S2 changed only the allowed output directory.

## 3. S1 constraints carried forward

1. The status set is exactly `FORMED`, `POETIC`, `SUSPENDED`, `LOCAL`, `STABLE`, `KILLED`, `DANGEROUS`.
2. Derivation trace cannot promote beyond `FORMED` or `POETIC`.
3. Stronger statuses require scope, assumptions, consequence obligations, contradiction accounting, and guards.
4. Context creation requires cost, lineage, assumption split, and consequence delta.
5. Population stabilization is not truth and cannot promote alone.
6. Local contradiction is non-explosive and must preserve consequence differences.
7. CL constraints remain active: no substrate, derivability, representation, or learner-evidence claim is allowed.

## 4. Toy-model domains summary

`S2_toy_model_domains.md` defines finite domains for:

- expression;
- primitive;
- derivation trace;
- scope;
- assumption;
- test;
- outcome;
- anchor;
- population;
- Goodhart flags.

The expression domain covers exactly the S0 replay expressions:
`liquid_powder`, `hereditary_infertility`, `square_circle`,
`everything_true_in_context`, `x_related_to_y_somehow`,
`translucent_causal_sweetness_field`, `light_wave`, and `light_particle`.

Tests have allowed scopes, expected outcomes, contrast outcomes, and failure
conditions. Anchors have presence and absence conditions. Population state is
finite and cannot promote claims by popularity alone.

## 5. Operational rules summary

`S2_operational_rules.md` operationalizes:

- T1 Birth;
- T2 Formed to Poetic;
- T3 Formed/Poetic to Suspended;
- T4 Suspended to Local;
- T5 Local to Stable;
- T6 Any status to Killed;
- T7 Any status to Dangerous;
- T8 Local dualism;
- T9 Stable downgrade.

Each rule specifies input fields, preconditions, blockers, output status, and
failure mode if violated. Replay order is fixed so that the same finite fields
produce the same status.

## 6. Case replay protocol summary

`S2_case_replay_protocol.md` defines deterministic fields for all seven cases:

| case | final expected status | decisive toy fields |
|---|---|---|
| A | `SUSPENDED` | contradiction plus extension path, untested consequences |
| B | `SUSPENDED` | scoped contradiction plus possible mechanism paths, untested consequences |
| C | `KILLED` | Euclidean scope, `AXIOMS_INCOMPATIBLE`, no extension path |
| D | `DANGEROUS` | context cost absent and context proliferation danger |
| E | `FORMED` | relation unspecified and volume proxy blocking upgrade |
| F | `POETIC` | pseudo-term, poetic marker, absent operational role |
| G | `LOCAL` | distinct experimental scopes and consequence tests |

No case requires external semantic judgement at replay time once the toy fields
are supplied.

## 7. Goodhart control protocol summary

`S2_goodhart_control_protocol.md` gives concrete activation predicates for:

- `VOLUME_PROXY`;
- `COHERENCE_PROXY`;
- `CONTRADICTION_MINIMIZATION_PROXY`;
- `CONTEXT_PROLIFERATION_PROXY`;
- `GRAMMAR_PROXY`;
- `POPULATION_PROXY`.

Each predicate is stated over finite fields such as relation type, consequence
obligations, candidate outcomes, attempted transition, scope cost, scope
lineage, anchors, and population state.

## 8. Oracle leakage audit summary

`S2_oracle_leakage_audit.md` answers all required oracle questions. No rule
requires real-world truth, external human judgement at replay time, an "obvious
nonsense" label, Sanskrit/Panini as truth oracle, population agreement as truth,
modern-science knowledge to force A/B upgrades, or direct claim-name-to-status
assignment.

The residual risk is explicit: humans authored the finite fields. S2 treats
that as the inspected toy input, not as learned evidence.

## 9. CL mistake audit summary

The CL audit detects no repeated CL mistake. S2 does not treat safe or filtered
data as substrate evidence, does not treat hand-coded priors as learning
evidence, does not allow representation or derivability work, does not confuse
preconditions with substrate evidence, and does not hide a replay-time oracle in
rule fields.

## 10. Pass / fail analysis

S2 passes because:

1. S1 pass is confirmed.
2. All required finite domains are defined.
3. T1-T9 are operationalized over finite fields.
4. S0 cases A-G have deterministic replay protocols.
5. Consequence tests have concrete expected outcomes, contrast outcomes, and failure conditions.
6. Anchors have toy presence and absence conditions.
7. Scope cost and lineage block free context laundering.
8. Population state cannot promote claims by popularity alone.
9. Goodhart controls have concrete activation predicates.
10. Oracle leakage audit detects no hidden replay-time semantic oracle.
11. CL mistake audit detects no repeated CL failures.
12. No code, experiment, implementation, model training, substrate claim, or derivability claim is made.

## 11. What was NOT shown

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

## 12. Downstream permission

Allowed next work:

```text
S3 tiny implementation specification
```

Not allowed:

- implementation;
- code;
- experiments;
- model training;
- Sanskrit experiment;
- representation probe;
- substrate claim;
- derivability claim;
- grounding claim;
- LLM-safety claim.

## 13. Durable result

S2 makes S1's schema concrete enough for a later tiny implementation
specification by defining finite domains, operational transition rules, replay
fields, Goodhart predicates, and audit checks. The durable result is only
admissibility for S3 specification, not evidence that the direction works.
