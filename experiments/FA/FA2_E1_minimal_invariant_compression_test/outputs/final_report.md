# FA2.E1 Minimal Invariant Compression Test

Diagnostic-only analysis over FA1.E1 false-safe witnesses. No new Justitia simulations were run.

## Decision

Classification: **Case E — Inconclusive**.
Interpretation: Compact non-oracle witness coverage is high, but FA1 witness-only data cannot estimate proxy precision or false positives.
H_FA1.1 assessment: `partially_supported_but_precision_unproven`.

## Input

- FA1 false-safe witnesses: `5839`.
- FA1 classes: `{'control_blind': 0, 'forward_dynamics_blind': 1364, 'history_blind': 1932, 'layer_confusion_blind': 0, 'mass_blind': 400, 'mean_blind': 0, 'policy_visible_concentration_blind': 1115, 'spread_blind': 724, 'unknown_or_mixed': 304}`.

## Ordered Refinement Coverage

| set | description | coverage count | coverage fraction | newly covered | coordinates | oracle |
|---|---|---:|---:|---:|---:|---|
| R0 | current 18.0 abstraction only | 0 | 0.000000 | 0 | 0 | no |
| R1 | R0 + I1 omitted collapse clauses | 1124 | 0.192499 | 1124 | 2 | no |
| R2 | R1 + I2 policy-visible concentration | 2528 | 0.432951 | 1404 | 3 | no |
| R3 | R2 + I3 compact history/delayed consequence | 4475 | 0.766398 | 1947 | 5 | no |
| R4-oracle | R3 + I4 oracle temporal reachability | 5839 | 1.000000 | 1364 | 6 | yes |
| R4-proxy | R3 + I4 non-oracle current minimum-zone-welfare proxy | 5829 | 0.998287 | 1354 | 6 | no |
| R5 | R4-proxy + best compact mixed resolver | 5829 | 0.998287 | 0 | 6 | no |

## Required Questions

1. Omitted collapse clauses alone cover `1124` witnesses (`0.192499`).
2. Adding policy-visible concentration raises coverage to `2528` (`0.432951`).
3. Adding compact history summaries raises coverage to `4475` (`0.766398`).
4. Non-oracle proxy coverage reaches `0.998287`, but precision cannot be measured from witness-only input.
5. Highest marginal coverage: `I3` with `1947` newly covered witnesses.
6. Highest marginal compression ratio: `I2` with `1404.000` witnesses per coordinate; cumulative R4-proxy compression is `971.500` witnesses per coordinate.
7. Fraction unresolved after R4-proxy: `0.001713`.
8. I1 is low WSTS risk; I2 is medium; I3 is high monotonicity risk; I4-oracle is high circularity risk; I4-proxy is medium WSTS risk due empirical calibration.
9. FA2 supports compact witness coverage, but not a fully constructive faithful refinement because proxy precision is unmeasured.
10. Strongest counterexample: The selected non-oracle temporal proxy is a broad min_zone_welfare threshold learned from false-safe witnesses only; without non-false-safe SAFE states, coverage may be non-discriminative.

## Temporal Analysis

- Oracle temporal invariant covers `4715` current-not-collapsed false-safe witnesses (`0.807501` of all witnesses).
- Steps to collapse: min `1`, median `18`, mean `20.562`, max `99`.
- Selected non-oracle proxy: `min_zone_welfare <= 0.96`, covering `1354` of `1364` R3 residual witnesses.

No safety claim is made. This experiment measures compression of missing information only.
