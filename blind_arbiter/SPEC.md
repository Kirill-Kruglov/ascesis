# Blind Arbiter — Specification

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

## Findings (current, after a strict audit — see `results/audit_report.md`)

An earlier draft of this section overstated the result; the strict audit corrected it.

1. C1' and C2' pass, but C1'(b) passes only marginally: geometric's mean high-R (`R >= 2.0`)
   true permanence is `0.511`, just over the `0.50` bar and well inside the seed noise. "The
   substrate is alive" rests on that thin margin. (Note: the gate code currently evaluates
   C1'(b) as `any point >= 0.50` rather than the locked `mean per regime >= 0.50`; the verdict
   coincides here but the implementation must be fixed to the locked predicate.)
2. There is NO sustained boundary. geometric's held-out permanence is non-monotonic and stays
   near coin-flip across mid-to-high `R` (0.600 at R=0.833, 0.500 at 1.2, 0.667 at 2.0, then
   0.433 at 3.33 and 6.5), with wide, overlapping Wilson 95% bands. The first-crossing
   `R* = 0.833` is only where a noisy curve first pokes above 0.5; it does not stay above. So
   "holds true permanence above R*" and "R* is a safety/development trade-off curve" do NOT
   survive and are withdrawn.
3. The signal is fully decoupled where it matters: at R=0.833 the correlation is `0.067` (final)
   / `0.102` (mean). The earlier `corr = 0.203` was a whole-`R` average, not the value at R*,
   and was misleading.
4. Regime ordering does hold: scalar (permanence 0 everywhere, no decoupling, dies by
   concentration) < lexicographic (~0.33-0.47) < geometric (~0.43-0.67). Active balancing helps;
   a floor-first rule on the observed signal does not, plausibly because the observed-signal
   floor is not the true-gene floor under Goodhart. Parity audit found no seed/grid/penalty
   handicap; one open SPEC question is whether the lagged-capture penalty should override
   lexicographic's observed-floor tier.
5. Defending true permanence under Goodhart requires ACTIVE intervention (intervention inside
   the floor exceeds outside). `floor_not_maximized` is therefore a descriptive diagnostic, not
   a gate.

Honest summary: a non-spatial blind active arbiter does NOT reliably hold permanence under
Goodhart. The best regime reaches only coin-flip permanence with the signal decoupled. This is
a weak/negative result for the optimistic "active feeder holds equilibrium above a boundary"
thesis; what survives is the ordering scalar < lexicographic < geometric.

## Caveats (mandatory with any external presentation)

- Non-spatial toy; 30 held-out seeds; wide confidence bands.
- No sustained boundary; the headline boundary claim was withdrawn after audit (see above).
- Active intervention is required; this is not a passive keeper.
- A passive-keeper comparison is a separate future test, not yet run.

## Reproduce

```sh
python3 run.py
```

Outputs in `results/`: raw data, `run_manifest.json` (seeds, R grid, `spec_sha256`), `report.md`,
`validation_report.md`, and SVG plots (permanence-vs-R, corr-over-time, three failure modes).
Field ownership is in `references.md`.
