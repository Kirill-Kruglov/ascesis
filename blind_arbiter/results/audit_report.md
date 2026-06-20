# Blind Arbiter Audit Report

## Boundary Logic Audit

- `curve_data` is aggregated from held-out rows only; train rows are not used for `true_permanence_rate`, `mean_final_corr`, or `r_star`.
- `first_above` sorts by numeric `R` and returns the first held-out curve point with true permanence rate >= 0.50.
- This is a first-crossing rule, not a monotone/sustained-boundary rule. `sustained R*` below is computed separately as the first R after which all higher-R points remain >= 0.50.

## H_boundary With Seed Bands

| regime | R | held-out success | rate | Wilson 95% band | final corr | mean corr | mean time-to-failure |
|---|---:|---:|---:|---:|---:|---:|---:|
| scalar | 0.182 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 4.0 |
| scalar | 0.333 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 4.3 |
| scalar | 0.375 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 5.2 |
| scalar | 0.571 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 6.0 |
| scalar | 0.833 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 6.9 |
| scalar | 1.200 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 7.3 |
| scalar | 2.000 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 8.0 |
| scalar | 3.333 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 8.9 |
| scalar | 6.500 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | 1.000 | 9.2 |
| geometric | 0.182 | 0/30 | 0.000 | [0.000, 0.114] | 0.400 | 0.856 | 26.4 |
| geometric | 0.333 | 0/30 | 0.000 | [0.000, 0.114] | -0.533 | 0.564 | 43.2 |
| geometric | 0.375 | 1/30 | 0.033 | [0.006, 0.167] | -0.867 | 0.002 | 77.0 |
| geometric | 0.571 | 4/30 | 0.133 | [0.053, 0.297] | -0.533 | -0.021 | 110.7 |
| geometric | 0.833 | 18/30 | 0.600 | [0.423, 0.754] | 0.067 | 0.102 | 118.0 |
| geometric | 1.200 | 15/30 | 0.500 | [0.332, 0.668] | -0.200 | 0.056 | 116.9 |
| geometric | 2.000 | 20/30 | 0.667 | [0.488, 0.808] | -0.067 | 0.090 | 114.6 |
| geometric | 3.333 | 13/30 | 0.433 | [0.274, 0.608] | 0.067 | 0.048 | 116.4 |
| geometric | 6.500 | 13/30 | 0.433 | [0.274, 0.608] | 0.200 | 0.127 | 114.3 |
| lexicographic | 0.182 | 0/30 | 0.000 | [0.000, 0.114] | -0.400 | 0.293 | 35.4 |
| lexicographic | 0.333 | 2/30 | 0.067 | [0.018, 0.213] | -0.667 | -0.047 | 69.3 |
| lexicographic | 0.375 | 2/30 | 0.067 | [0.018, 0.213] | 0.000 | -0.050 | 100.2 |
| lexicographic | 0.571 | 2/30 | 0.067 | [0.018, 0.213] | -0.400 | -0.114 | 109.3 |
| lexicographic | 0.833 | 13/30 | 0.433 | [0.274, 0.608] | -0.133 | -0.049 | 109.5 |
| lexicographic | 1.200 | 11/30 | 0.367 | [0.219, 0.545] | -0.067 | -0.173 | 108.2 |
| lexicographic | 2.000 | 14/30 | 0.467 | [0.302, 0.639] | 0.000 | -0.054 | 112.8 |
| lexicographic | 3.333 | 10/30 | 0.333 | [0.192, 0.512] | 0.000 | -0.072 | 115.5 |
| lexicographic | 6.500 | 10/30 | 0.333 | [0.192, 0.512] | -0.133 | -0.055 | 113.0 |

## H_regime Strict Read

| regime | first-crossing R* | sustained R* | interpretation |
|---|---:|---:|---|
| scalar | None | None | never reaches held-out permanence >= 0.50 |
| geometric | 0.833 | None | crosses >= 0.50 once but does not remain above threshold at higher R |
| lexicographic | None | None | never reaches held-out permanence >= 0.50 |

## Headline Audit

- Geometric first-crossing R* survives: `0.833` with true permanence `0.600` (18/30 held-out seeds).
- C1'(b) passes marginally under the locked high-R mean: best high-R mean is `0.511` for `geometric`, margin `0.011`.
- The stronger wording 'holds above R*' does not survive strict reading: sustained R* is `None` because geometric falls to `0.433` at R=3.333 and R=6.500.
- The reported corr `0.203` is the geometric all-R mean of per-run mean corr, not the corr at R*=0.833. At R*=0.833, final corr is `0.067` and mean corr is `0.102`.
- H_regime survives in the first-crossing sense: only geometric has a finite first-crossing R*. It does not survive as a sustained-boundary claim.

## Parity Audit

- Same effort: all regimes use the same seeds, R grid, substrate, action grid, lag/audit observation, and calibration history.
- Same consequence signal: all regimes compute the same direct lagged-capture penalty from `obs.lagged_capture * obs.lagged_alloc`; the arbiter still receives no hidden genes or true shares.
- Scalar and geometric have the same key shape: primary objective minus consequence penalty, then the same distance-to-signal tie-break.
- Lexicographic intentionally has a different key because it is floor-first over observed signal. The consequence penalty is applied inside the floor tier; it cannot override the top-level preference for keeping the observed signal floor nonnegative.
- Verdict: no parity/correctness bug found in scalar/geometric. Lexicographic failure is plausibly a real result of optimizing an observed signal-floor under Goodhart, with one caveat: the SPEC does not fully specify whether the lagged-capture penalty should be allowed to override the observed-floor tier. Under the current floor-first definition, lexicographic is not accidentally handicapped by unequal seeds or missing penalty, but it is semantically stricter than scalar/geometric.

## Fixes Applied In This Audit Pass

- Evaluation fix: C1'(b) now uses the locked per-regime high-R bucket mean instead of the weaker any-single-high-R-point test; predicate text and dynamics were unchanged.
- Report-only fix: C2 mid-R fields were relabeled from misleading `scalar_mid_*` wording to all-regime `mid_bucket_*` wording; C2 predicate was unchanged.
- Report-only fix: first-crossing R* and sustained R* are now reported separately; the locked first-crossing calculation was retained.
- Report-only addition: Wilson seed bands and parity audit are emitted here. No substrate, R grid, regime objective, or locked predicate was changed.
