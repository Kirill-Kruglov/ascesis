# 08 Blind Type-B Arbiter (Non-Spatial Population Game) SPEC

Status: pre-registered. Committed before any run. Priority is the validity of the test,
not the result. A clean negative (no boundary appears, or no regime difference) is a
success of the test and publishes. Do not retune to rescue a hypothesis.

This is the cheapest-first slice of the blind-arbiter environment: a non-spatial population
game, no spatial grid, no multi-agent RL. If the `R`-boundary does not appear even here, the
idea is refuted cheaply; if it does, a spatial / MARL version can follow.

## Question

Can a type-blind arbiter (it controls only resource dispensing and a lag, reacts to the
realized consequence of past dispensing, and never classifies agent types) hold permanence
of a population under optimization pressure and signal-behavior decoupling (Goodhart)? Where
is the boundary in `R = horizon_harm / horizon_observation`, and do different arbiter payout
rules move it?

Links: `structure.md` bridge 2 (resource-time safety) and the telos bridges; `field_check.md`
nodes 15, 16, 22, 27. Field grounding to add to `field_check.md` before publication:
replicator permanence (Hofbauer & Sigmund), ESS / Hawk-Dove (Maynard Smith), indirect
reciprocity (Nowak & Sigmund 2005), mechanism design under hidden types (Myerson;
Holmstrom moral hazard), Stackelberg / automated mechanism design.

## Model (non-spatial)

- `G` groups (default `G = 2`), shares `x_g(t)` on the simplex (`sum_g x_g = 1`).
- Each group has a hidden aggressiveness `a_g in [0,1]` (the behavior gene: propensity to
  capture when given resource; invisible to the arbiter) and an observable signal
  `s_g in [0,1]` with `s_g(0) = clip(a_g + noise)`.
- Each step the arbiter allocates a unit resource budget across groups as `r_g` (`sum r_g = 1`)
  using only observed information: the realized consequence of dispensing from `lag` steps ago
  plus a stochastic audit; never `a_g`.
- Realized consequence: a group given resource captures with intensity increasing in
  `a_g * r_g`; capture transfers share from the others at `capture_rate`; otherwise
  coexistence. The arbiter sees the consequence only after `lag` steps.
- Share update is replicator-style: a group grows with usable resource and shrinks under
  others' capture; renormalize to the simplex; a group below `survival_threshold` goes
  extinct (absorbing).
- Signal mutation (the Goodhart engine, emergent): `s_g` drifts toward whatever signal value
  has recently attracted more resource, decoupling `s_g` from `a_g` over time. This is not a
  penalty term; it is selection on the signal.

## R axis (definition fixed here)

`R := horizon_harm / horizon_observation`, where `horizon_harm` is the number of steps for an
unchecked capture to become irreversible (push a group below survival) and
`horizon_observation = lag + audit_period`. So:

- `R > 1`: harm becomes irreversible slower than the arbiter observes -> the arbiter can in
  principle react in time.
- `R < 1`: harm is irreversible before it is observed -> no blind mechanism can hold
  permanence.

Note: this fixes an inconsistency in the source environment description, where the ratio was
written with the opposite orientation to its own prose. The content is unchanged: a blind
arbiter cannot hold permanence when capture is faster than observation.

Sweep `R` (by varying `capture_rate` and `lag`) and build the permanence-survival curve.

## Arbiter regimes (one interface, swappable payout rules)

All regimes use only post-lag observed consequences plus the stochastic audit, never `a_g`.

- `scalar`: dispenses to maximize a single scalar of observed shares (control; expected to be
  hacked as signal decouples).
- `geometric`: dispenses to maximize the geometric mean of observed shares (bet-hedging;
  expected strong here -- this is its home field, so it is a home-field check, not a favorite).
- `lexicographic`: permanence-floor first (keep `prod_g x_g > eps`); inside the floor it does
  not optimize shares.

## Permanence and failure

- Permanence := `prod_g x_g > eps_permanence` (interior of the simplex). This is a floor, not a
  maximized objective: the arbiter intervenes near the collapse boundary and does not equalize
  shares inside the floor.
- Failure (either one): extinction (any `x_g < survival_threshold`) or capture (any
  `x_g > 1 - eps`). Both count as arbiter failure.

## Hypotheses

Calibration (near-definitional, reported but not claimed as findings):
- C1: at `R << 1`, permanence fails for all regimes. If not, the harm/observation mechanic is
  broken.
- C2: the `scalar` arbiter is hacked -- `corr(s, a)` falls and permanence degrades. If not, the
  Goodhart engine is broken.
- C3: `geometric` is comparatively strong on this home field. A home-field check, not a win.

Real content (pre-registered):
- H_boundary: there is a critical `R*` such that permanence holds for `R > R*` on held-out
  seeds. Measure `R*` and whether it sits at `~1` or strictly above 1 (a margin forced by the
  stochastic audit and lag). Report the sharpness of the transition.
- H_regime: `lexicographic` (floor-first) holds permanence down to a lower `R*` than `scalar`;
  compare to `geometric`. A null result (no regime moves `R*`) is publishable.

## Failure modes the stand must surface (required outputs, not optional)

1. camouflage faster than the window (`R < 1`): the floor is broken; show signal-gene
   decoupling and permanence loss.
2. collective hack: a coordinated group rewrites the effective payout / captures the feeder as
   an institution; blindness does not save it.
3. collective punishment of the innocent: consequence-based reaction penalizes low-aggression
   members inside a group (model within-group heterogeneity of `a`).

## Metrics

- permanence (binary) per seed; permanence-survival curve vs `R` (median and IQR bands).
- `corr(s_g, a_g)` over time (direct Goodhart indicator).
- time-to-capture and time-to-extinction vs `lag`.
- share trajectories on the simplex.

## Environment split

- Train seeds and held-out seeds (as in the Sugarscape protocol). Tune only on train; report
  the curve and regime comparison on held-out seeds.

## Artifact / discipline checks

1. blind_arbiter: the arbiter's input never includes `a_g`; only post-lag observed consequences
   and the stochastic audit. (Static check on the call signature plus a runtime assertion.)
2. emergent_goodhart: signal-gene decoupling arises from the dispensing dynamics and signal
   mutation, with no hand-coded penalty.
3. floor_not_maximized: inside the permanence floor the arbiter does not equalize shares
   (intervention magnitude near zero while `prod x_g > eps`).
4. symmetric_comparison: all regimes run on identical seeds and the same `R` grid, with no
   tie-break favoring any regime; `improvement_iterations` per regime logged.
5. finite_values and reproducibility: fixed seeds, one command, all numbers finite.
6. calibration_gate: C1 and C2 hold (R<<1 fails for all; scalar is hackable), else the stand is
   not yet measuring the question.

## Win / interpretation criterion

- The deliverable is the permanence-survival curve vs `R` with `R*` located, plus the three
  failure-mode plots. H_regime is supported if a regime shifts `R*` on held-out seeds by a
  pre-registered margin; otherwise report the null. The headline `R<1` failure is calibration,
  not a finding.

## Implementation notes

Pure Python plus numpy; matplotlib only for plots; no heavy dependencies (match experiments
01-06). One command from this directory, fixed seeds, outputs in the same layout as the other
experiments. Functional forms above have pre-registered defaults; any change is logged in the
run manifest and kept symmetric across regimes.
