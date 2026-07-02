# CL1 — Minimal Lawful Domain Boundary-Fidelity Pilot

Status: pre-registered executable pilot.

This experiment instantiates the CL0 candidate in the weakest admissible form:
a generated lawful domain with a safety boundary that is tested for fidelity and
non-vacuity before any learner training.

It does not claim a substrate has been found. It does not train an LLM. It does
not test world-model derivation.

## Goal Anchor

The project goal is to train an LLM / learner so that its world-model is
derived rather than generalized from internet-like data. The current weakened
step is safer domain filtering: a learner should not observe collapse
trajectories unless a boundary has first been shown faithful and non-vacuous.

CL1 serves that goal by testing whether one minimal lawful domain can implement
the CL0 boundary-fidelity protocol without repeating the known failures:
projection blindness, conservative vacuity, compression without discrimination,
or layer confusion.

## Domain

Domain name: `FourZoneMassDomain`.

Full state:

```text
State(zones=(z0,z1,z2,z3), mass=m, phase=p)
```

where each zone health is in `[0, 4]`, mass is in `[0, 6]`, and phase is in
`[0, 3]`.

Action space:

```text
AID_0, AID_1, AID_2, AID_3, CONSERVE
```

Transition:

```text
state_t+1 = transition(state_t, action_t, exogenous_t)
```

The exogenous term is deterministic and lawful: phase `p` shocks zone `p`.
Actions and shocks update zone health and mass by fixed rules in `domain.py`.

Collapse predicate:

- `spread`: at least two zones have health `<= 0`;
- `mass`: mass is `<= 0`;
- `both`: both clauses hold.

Learner-visible observation:

```text
zones, mass, phase
```

Collapse labels and future outcomes are audit-only and are not learner-visible.

## Boundary Variants

Candidate boundary:

Bounded forward rollout under the deterministic safety policy using
layer-eligible coordinates `zones`, `mass`, and `phase`. SAFE means no collapse
within the pre-registered horizon.

Projection-blind baseline:

A deliberately weak baseline that uses mean zone health only and omits
failed-zone spread and mass. It is intended to reproduce 18.1-style projection
blindness.

Trivially-safe baseline:

Classifies every state as DOOMED.

Unfiltered control:

No boundary filtering.

## Pre-registered Gate

Thresholds are inherited from CL0:

- `false_safe_rate <= 0.05`;
- `already_collapsed_labeled_safe_rate == 0`;
- `false_positive_rate <= 0.20`;
- equal-volume shielded/control sampling required.

Decision rule is exactly the CL1 task specification.

## Outputs

The runner writes:

- `outputs/metrics.json`
- `outputs/decision.json`
- `outputs/final_report.md`
- `outputs/false_safe_witnesses.json`
- `outputs/false_positive_witnesses.json`
- `outputs/layer_audit.md`

