# Blind Type-B Arbiter — Specification

A focused, self-contained working package extracted from the `ascesis_of_learning_grace`
research trail. The full trial-and-error history (predicate locks, a mis-aimed predicate, a
harm-dynamics bug, the demotion of an artifact check) lives in the git commit history; this
file is the clean current spec.

## Question

Can an active, type-blind arbiter hold the permanence of a population that contains an
adversarial fraction, under hard optimization pressure that decouples observable signals from
true behaviour (Goodhart / reward hacking)? Where does the boundary in
`R = horizon_harm / horizon_observation` sit, and which payout rule moves it?

The intuition: an AGI/ASI modelled as an active "feeder" for a population (including agents
that actively search for and exploit reward hacking under evolution), which keeps the
population in equilibrium without classifying agents, reacting only to the realized
consequences of its past dispensing after a lag.

## Model (non-spatial)

- `G` groups (default 2), shares `x_g` on the simplex.
- Each group has a hidden aggressiveness `a_g` (the behaviour gene: propensity to capture
  when fed; invisible to the arbiter) and an observable `signal s_g` (`s_g(0) ~ a_g + noise`).
- Each step the arbiter allocates a unit resource budget `r_g` using only the lagged,
  stochastically-audited consequence of past dispensing and the observable signal — never
  `a_g` or the true shares.
- Capture: a fed group captures with intensity rising in `capture_rate * a_g * r_g`, transfers
  share from the others; shares update replicator-style; a group below `survival_threshold`
  goes extinct.
- Signal mutation (the emergent Goodhart engine): `s_g` drifts toward whatever signal recently
  attracted resource, decoupling from `a_g` over time. Not a penalty term.

## Two spaces (the load-bearing design choice)

- The permanence metric is computed over `behaviour_gene` (the true types): has a real
  predator captured, has a real non-predator gone extinct. This is the floor we defend; the
  arbiter is blind to it.
- Every arbiter objective is computed over `signal` (the observable). This separation is what
  gives `R` a lever (the only bridge from signal to truth is lagged observation) and prevents
  the arbiter from optimizing the metric directly.

## R axis

`R = horizon_harm / horizon_observation`, harm-irreversibility time over observation time
(`lag + audit_period`). `R > 1`: harm is slower than observation, the arbiter can react.
`R < 1`: harm is irreversible before it is observed, no blind mechanism can hold permanence.

## Permanence and failure

- Permanence := `min_g (true x_g) > permanence_eps` held every step. A floor, not a maximized
  objective.
- Failure: extinction (a group below survival) or capture (a group monopolizes).

## Arbiter regimes (one interface, signal-only)

`scalar` (maximize a scalar of observed shares; control), `geometric` (geometric mean of
observed shares), `lexicographic` (observed floor first). All apply a direct lagged-capture
penalty: if feeding a group produced an observed capture, shift resource away from it.

## Locked calibration predicates (existence-of-phenomenon checks)

- `C1' := (a)` for every regime, mean true permanence at `R <= 0.40` (held-out) `< 0.10`,
  AND `(b)` for at least one regime, mean true permanence at `R >= 2.0` `>= 0.50` (so a
  boundary exists).
- `C2' :=` for at least one regime in `0.80 <= R <= 1.50`, mean true permanence `< 0.50` AND
  final `corr(s_g, a_g) < 0.70` (Goodhart-driven failure is present somewhere).

These are immutable existence checks; if unreachable after honest substrate work, that is a
result. The locked hypotheses (boundary location and regime comparison) are read only on a
substrate that passes C1' and C2'.

## Accepted findings (current)

1. The substrate passes C1' and C2' on held-out seeds. It is alive.
2. The active blind arbiter (geometric) holds true-gene permanence above `R* = 0.833` while its
   signal has decoupled from the gene to `corr = 0.203`. The observable is nearly useless, yet
   the arbiter defends the true floor — through lagged-consequence reaction, not signal
   reading. This is the core, non-tautological result.
3. `scalar` (dies by concentration, no decoupling) and `lexicographic` find no boundary.
4. Defending true permanence under Goodhart requires ACTIVE intervention: intervention inside
   the floor exceeds intervention outside it. Passive floor-keeping is insufficient.
   Consequently `floor_not_maximized` is a descriptive diagnostic here, not a pass/fail gate.

## Caveats (mandatory with any external presentation)

- Non-spatial toy; a single regime (`geometric`) achieves a boundary.
- Active intervention is required; this is not a passive keeper.
- The boundary is probabilistic, not deterministic: at/above `R*`, permanence holds on roughly
  0.60-0.67 of held-out seeds, not all. (This is literally the ">= 51% under a safety
  trade-off" regime, not "always works".)
- A passive-keeper comparison is a separate future test, not yet run.

## Reproduce

```sh
python3 run.py
```

Outputs in `results/`: raw data, `run_manifest.json` (seeds, R grid, `spec_sha256`), `report.md`,
`validation_report.md`, and SVG plots (permanence-vs-R, corr-over-time, three failure modes).
Field ownership is in `references.md`.
