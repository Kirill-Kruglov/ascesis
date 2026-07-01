# S4 — Tiny Boundary-Accounting / Replay Implementation

## 0. Verdict

`S4-PASS-TINY-IMPLEMENTATION-AUDIT-OK`

S3 decision was verified at runtime from:

```text
/home/master/llm_projects/ascesis/experiments/S/S3_tiny_implementation_spec_for_boundary_accounting_replay_protocol/S3_decision.json
```

S3 runtime verification passed: `True`.
S4 implements only a tiny boundary-accounting / replay audit engine inside the
S4 output directory.

## 1. Goal anchor

The immutable project goal is to train an LLM / learner so that its world-model
is derived, not merely generalized from internet-like data.

S4 serves that goal only by implementing an audit/replay machine that exposes
provenance, transition traces, Goodhart flags, oracle warnings, and
claim-strength downgrades for finite toy records.

## 2. Inputs used

Required S0/S1/S2/B0/S3/MAP/ledger context files were read as constraints.
Pre-change worktree state was not clean; unrelated untracked files were present.
S4 edited only `experiments/S/S4_tiny_boundary_accounting_replay_implementation/`.

## 3. S3 constraints carried forward

- Boundary-accounting / replay engine only.
- No semantic, meaning, truth, grounding, substrate, learner-evidence, or LLM-safety system.
- Every input field needs provenance.
- Forbidden oracle fields are rejected.
- Status follows T1-T9 fields, not claim or expression names.
- Claim strength is downgraded and forbidden overclaims stay forbidden.

## 4. Implementation summary

Implemented `boundary_replay_engine.py` and `run_s4.py` using Python 3 standard
library only. The engine exposes the required public functions and writes all
required JSON/Markdown outputs.

## 5. Base replay results

| claim | final status | allowed claim strength |
|---|---|---|
| A_liquid_powder | SUSPENDED | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC, EXTERNAL_CONTACT_REQUIRED |
| B_hereditary_infertility | SUSPENDED | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC, EXTERNAL_CONTACT_REQUIRED |
| C_square_circle | KILLED | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC |
| D_everything_true_in_context | DANGEROUS | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC |
| E_x_related_to_y_somehow | FORMED | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC, EXTERNAL_CONTACT_REQUIRED |
| F_translucent_causal_sweetness_field | POETIC | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC, EXTERNAL_CONTACT_REQUIRED |
| G_light_wave_particle_pair | LOCAL | BOUNDARY_ACCOUNTING, TOY_REPLAY_DETERMINISTIC |

## 6. Mutation test results

| mutation | result | final status |
|---|---|---|
| M1 | pass | FORMED |
| M2 | pass | DANGEROUS |
| M3 | pass | FORMED |
| M4 | pass | KILLED |
| M5 | pass | POETIC |
| M6 | pass | FORMED |

## 7. Oracle / provenance rejection results

Oracle rejection tests passed: 2 / 2.
Provenance/init validation tests passed: 2 / 2.

## 8. Static audit results

Static audit passed: `True`.

## 9. Claim-strength downgrade audit

Claim-strength downgrade passed: `True`.
No replay or mutation output allowed `RULE_GENERATED_CONTENT`,
`DERIVATION_EVIDENCE`, or `SUBSTRATE_CLAIM`.

## 10. Pass / fail analysis

S4 passes because the actual upstream S3 decision artifact is verified at runtime, code exists only inside the S4 directory, base cases replay, every field has provenance, missing provenance and forbidden oracle fields are rejected, replay outputs include required audit fields, no lookup behavior is detected, M1-M6 and O1-O4 pass, G1-G5 gate-chain tests pass, static audit passes, and claim-strength downgrades block forbidden overclaims.

## 11. What was NOT shown

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

## 12. Downstream permission

Allowed next work:

```text
S4 postmortem / demo packaging
S5 boundary-accounting demo spec
B1 external-contact route analysis
```

Not allowed: LLM training, substrate claims, derivability claims, semantic
boundary-generator claims, learner-evidence claims, grounding claims, or
world-transfer claims.

## 13. Durable result

S4 shows only that a bounded boundary-accounting / replay audit machine can be
implemented for the finite toy S-records. It makes hidden-oracle, provenance,
lookup, Goodhart, and claim-strength failures visible in audit outputs.
