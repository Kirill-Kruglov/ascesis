# S1 — Microformalization of Semantic Status Transitions

## 0. Verdict

`S1-PASS-ADMISSIBLE-FOR-TOY-MODEL-SPEC`

S0 decision was confirmed as `S0-PASS-ADMISSIBLE-FOR-MICROFORMALIZATION`.
S1 expresses the S0 distinctions as a minimal microformal status-transition
system with explicit claim fields, statuses, consequence obligations, scoped
contradiction relation, Goodhart guards, transition rules, case replay, and
incoherence checks.

This admits only `S2 toy model specification`. It does not admit implementation,
experiments, model training, Sanskrit experiments, representation probes,
substrate claims, derivability claims, grounding claims, or LLM-safety claims.

## 1. Goal anchor

The immutable project goal is to train an LLM / learner so that its world-model
is derived, not merely generalized from internet-like data.

S1 serves that goal only by asking whether S0's anti-sophistry distinctions can
be made rule-like enough for a future toy-model specification. If the
distinctions remained ad hoc, the semantic ecology direction would risk becoming
coherent synthetic text or grammar-valid sophistry.

## 2. Inputs used

| file | role | status |
|---|---|---|
| `experiments/S/S1_Microformalization_of_Semantic_Status_Transitions.md` | Primary S1 specification | PRESENT |
| `research/MAP-S0_Derivational_Semantic_Ecology.md` | Constraint context | PRESENT |
| `research/MAP-S1_Literature-grounded_Constraint_Refinement.md` | Constraint context | PRESENT |
| `research/closed_directions_ledger.md` | Closed CL constraints | PRESENT |
| `experiments/S/S0_Anti-Sophistry_Future-Meaning_Admissibility_Gate.md` | S0 task | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_report.md` | Prior gate result | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_decision.json` | S0 decision | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_case_table.md` | S0 cases | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_assumption_graphs.md` | S0 assumption graphs | PRESENT |
| `experiments/S/S0_anti_sophistry_future_meaning_admissibility_gate/S0_goodhart_audit.md` | S0 guards | PRESENT |

MAP files, S0 files, and `research/closed_directions_ledger.md` were read only.

## 3. S0 constraints carried forward

1. Statuses are non-Boolean and exactly `FORMED`, `POETIC`, `SUSPENDED`, `LOCAL`, `STABLE`, `KILLED`, `DANGEROUS`.
2. Derivation trace / grammar can admit at most `FORMED` or `POETIC`.
3. Scope, assumptions, consequence obligations, contradiction links, population state, and anchors are required before strong statuses.
4. Contexts cannot be free contradiction-rescue devices.
5. Population agreement is not truth.
6. No single proxy can promote a claim to `STABLE`.
7. CL closure constraints remain active: no substrate, derivability, or learner-evidence claims are allowed from these gates.

## 4. Microformal schema summary

`S1_microformal_schema.md` defines:

- `Claim` object with all required fields;
- exact S0 status set;
- `DerivationTrace`;
- typed `Scope`;
- `AssumptionGraph`;
- structural `ConsequenceObligation`;
- scoped non-explosive `Contradiction` relation;
- Goodhart flags;
- anchor types;
- population state.

The core schema constraint is:

```text
if claim C holds under scope S and assumptions A,
then admissible test T should distinguish expected outcome O
from at least one alternative O'.
```

## 5. Transition rule summary

`S1_transition_rules.md` defines T1-T9:

- T1 Birth;
- T2 Formed to Poetic;
- T3 Formed/Poetic to Suspended;
- T4 Suspended to Local;
- T5 Local to Stable;
- T6 Any status to Killed;
- T7 Any status to Dangerous;
- T8 Local dualism;
- T9 Stable downgrade.

The decisive blockers are: no derivation-only upgrade beyond `POETIC`, no
`LOCAL` without scope and consequences, no `STABLE` with active Goodhart flags,
and no local contradiction explosion.

## 6. Case replay summary

`S1_case_replay.md` replays all seven S0 cases through T1-T9:

| case | final S1 classification | governing rules |
|---|---|---|
| A | `SUSPENDED` with possible `POETIC` use | T1, T2, T3; T4/T5 blocked |
| B | `SUSPENDED`; literal unaided subclaim `KILLED`; scoped mechanisms possible `LOCAL` | T3, T4, T6 |
| C | `KILLED` under Euclidean scope; `POETIC`/scoped `LOCAL` alternatives only | T2, T4, T6 |
| D | `DANGEROUS` | T7, context guard |
| E | `FORMED` with vacuity annotation | T1, volume guard |
| F | `FORMED`/`POETIC` | T1, T2, grammar guard |
| G | scoped `LOCAL` dualism | T4, T8 |

The replay is rule-based rather than ad hoc.

## 7. Goodhart guard summary

`S1_goodhart_guards.md` formalizes:

- `VOLUME_PROXY`;
- `COHERENCE_PROXY`;
- `CONTRADICTION_MINIMIZATION_PROXY`;
- `CONTEXT_PROLIFERATION_PROXY`;
- `GRAMMAR_PROXY`;
- `POPULATION_PROXY`.

Each guard has a trigger condition, blocked transition, repair condition, S0
activating case, and kill/danger condition.

## 8. Incoherence checks

`S1_failure_analysis.md` checks:

- `IC1` Status overlap: pass, `DANGEROUS` blocks `STABLE`.
- `IC2` Grammar bypass: pass, derivation trace cannot produce `LOCAL`/`STABLE`.
- `IC3` Context laundering: pass, contexts need cost, lineage, assumptions, consequence delta.
- `IC4` Vacuity: pass, no consequence means no `STABLE`.
- `IC5` Dogmatism: pass, `SUSPENDED` and `LOCAL` remain available.
- `IC6` Explosion: pass, local contradiction cannot imply arbitrary claims.

## 9. Pass / fail analysis

S1 passes because:

1. S0 pass is confirmed.
2. The claim object includes all required fields.
3. The status set is exactly the S0 status set.
4. Derivation trace cannot promote beyond `FORMED`/`POETIC` by itself.
5. Consequence obligation is defined structurally.
6. Contradiction relation is scoped and non-explosive.
7. Goodhart guards are rule-level, not slogans.
8. Transitions T1-T9 are explicit.
9. Cases A-G replay correctly through rules.
10. Incoherence checks IC1-IC6 pass.
11. No implementation, code, experiment, LLM training, substrate claim, or derivability claim is made.

## 10. What was NOT shown

- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No Sanskrit experiment is allowed.
- No implementation is allowed.
- No toy model has been specified yet.
- No claim that semantic ecology solves grounding.
- No claim that status transitions are sufficient for meaning.
- No claim that contradiction containment is enough.
- No claim that population meaning is truth.
- No claim that S1 proves the direction works.

## 11. Downstream permission

Allowed next work:

```text
S2 toy model specification
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
- LLM-safety claim.

## 12. Durable result

S1 turns S0's analytic distinctions into a minimal rule-level schema suitable
for a future toy-model specification. The durable result is not that the
semantic ecology works. The durable result is that the next admissible step can
specify a toy model whose objects, transitions, guards, and failure modes are
already constrained.
