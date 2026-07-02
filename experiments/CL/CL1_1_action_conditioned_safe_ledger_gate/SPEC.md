# CL1.1 - Action-Conditioned Safe Ledger Gate

Status: pre-registered executable repair gate.

This experiment repairs the CL1 state-level boundary into an action-conditioned
transition ledger check. CL1 showed that `SAFE(state)` can be faithful under the
declared safety-policy rollout, but learner ledgers contain transitions:

```text
observation(state), action, observation(successor)
```

CL1.1 therefore evaluates every `(state, action)` pair in the CL1
`FourZoneMassDomain`.

## Goal Anchor

The project goal is to train an LLM / learner so that its world-model is
derived rather than merely generalized from internet-like data. The current
weakened step is a safe transition-ledger precondition: before any learner
training, admitted transition data must exclude collapse trajectories under the
declared boundary semantics.

This experiment serves that goal only by testing whether the CL1 boundary can
be repaired into a safe action-conditioned ledger. It does not train a learner,
does not claim derivation, and does not claim substrate discovery.

## Domain

Domain name: `FourZoneMassDomain`.

The experiment imports the CL1 domain implementation unchanged:

```text
experiments/CL/CL1_boundary_fidelity_pilot/domain.py
```

Full state:

```text
State(zones=(z0,z1,z2,z3), mass=m, phase=p)
```

Action space:

```text
AID_0, AID_1, AID_2, AID_3, CONSERVE
```

Collapse predicate:

- `spread`: at least two zones have health `<= 0`;
- `mass`: mass is `<= 0`;
- `both`: both clauses hold.

Learner-visible transition:

```text
observe(state), action, observe(successor)
```

Collapse labels, future outcomes, mechanisms, and witness classes are audit-only.

## Candidate Admission Rule

`ADMIT_CANDIDATE(state, action)` is true iff:

1. the source state is not already collapsed;
2. `transition(state, action)` is not already collapsed;
3. rollout from the successor under the CL1 deterministic safety policy remains
   non-collapse for `horizon - 1`;
4. the learner-visible transition contains only source observation, action, and
   successor observation;
5. no collapse label, future outcome label, witness class, or reporting-only
   metric is learner-visible.

CL1.1 tests one-step action admission followed by safety-policy continuation.
It does not prove safety under arbitrary future learner actions.

## Baselines

- CL1 state-level carryover: admit every action from states where the CL1
  candidate boundary says `SAFE`.
- Projection-blind action baseline: admit every action from states where the
  CL1 projection-blind boundary says `SAFE`.
- Trivially-safe action baseline: admit no actions.
- Unfiltered action control: admit all `(state, action)` pairs.

## Thresholds

- `unsafe_admitted_transition_rate <= 0.05`
- `already_collapsed_source_admitted_rate == 0`
- `already_collapsed_successor_admitted_rate == 0`
- `false_positive_action_rate <= 0.20`
- `equal_volume_possible == true`

Minimum equal-volume transition budget: `500`.

## Outputs

The runner writes:

- `outputs/metrics.json`
- `outputs/decision.json`
- `outputs/final_report.md`
- `outputs/unsafe_admitted_witnesses.json`
- `outputs/false_positive_action_witnesses.json`
- `outputs/layer_audit_delta.md`
