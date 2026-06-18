# 02 Hedger vs Incomplete Report

SPEC hash: `f7877449121e26ddbe43eeb0170994c37fb71727acd05d33236135f3ddd32abe`

| environment | split | kind | agent | valid GM? | action | survival | score | violations | incomparable |
|---|---|---|---|---:|---|---:|---:|---:|---:|
| train_scalar_stationary | train | scalarizable | arithmetic_mean | true | axis_b | 0.00 | 55.10 | 0.00 | 0.00 |
| train_scalar_stationary | train | scalarizable | geometric_mean | true | balanced | 1.00 | 62.97 | 0.00 | 0.00 |
| train_scalar_stationary | train | scalarizable | incomplete_preference | true | balanced | 1.00 | 62.97 | 0.00 | 1.00 |
| train_scalar_shift | train | scalarizable | arithmetic_mean | true | lottery | 1.00 | 65.35 | 0.00 | 0.00 |
| train_scalar_shift | train | scalarizable | geometric_mean | true | early_a_late_b | 1.00 | 64.18 | 0.00 | 0.00 |
| train_scalar_shift | train | scalarizable | incomplete_preference | true | balanced | 1.00 | 62.39 | 0.00 | 1.00 |
| heldout_scalar_risk | heldout | scalarizable | arithmetic_mean | true | axis_b | 0.00 | 54.11 | 0.00 | 0.00 |
| heldout_scalar_risk | heldout | scalarizable | geometric_mean | true | balanced | 1.00 | 62.74 | 0.00 | 0.00 |
| heldout_scalar_risk | heldout | scalarizable | incomplete_preference | true | balanced | 1.00 | 62.74 | 0.00 | 1.00 |
| heldout_scalar_shift | heldout | scalarizable | arithmetic_mean | true | specialist | 1.00 | 64.65 | 0.00 | 0.00 |
| heldout_scalar_shift | heldout | scalarizable | geometric_mean | true | balanced | 1.00 | 62.06 | 0.00 | 0.00 |
| heldout_scalar_shift | heldout | scalarizable | incomplete_preference | true | balanced | 1.00 | 62.06 | 0.00 | 1.00 |
| heldout_incommensurable_threshold | heldout | incommensurable | arithmetic_mean | false | extractive_growth | 0.00 | 85.09 | 60.00 | 0.00 |
| heldout_incommensurable_threshold | heldout | incommensurable | geometric_mean | false | extractive_growth | 0.00 | 85.09 | 60.00 | 0.00 |
| heldout_incommensurable_threshold | heldout | incommensurable | incomplete_preference | false | preserve_threshold | 1.00 | 64.75 | 0.00 | 1.00 |
| heldout_incommensurable_sacred_floor | heldout | incommensurable | arithmetic_mean | false | major_gain_violate_floor | 0.00 | 92.92 | 60.00 | 0.00 |
| heldout_incommensurable_sacred_floor | heldout | incommensurable | geometric_mean | false | major_gain_violate_floor | 0.00 | 92.92 | 60.00 | 0.00 |
| heldout_incommensurable_sacred_floor | heldout | incommensurable | incomplete_preference | false | modest_gain_preserve_floor | 1.00 | 63.58 | 0.00 | 1.00 |

## Held-out Strict Wins Where Geometric Mean Is Valid

[]

## Hedger Not Applicable

["heldout_incommensurable_threshold", "heldout_incommensurable_sacred_floor"]

These are not wins over hedging. They are cases where the scalar hedger is undefined because the environment declares no valid common currency.

## Sacred / Protected Values Legitimacy

The `heldout_incommensurable_sacred_floor` environment is intended as a toy protected-value threshold: some violations are not tradeable for more of another good. This is grounded in Tetlock/Fiske work on taboo trade-offs and protected or sacred values. If that literature is accepted as a legitimate non-scalarizable structure, this branch remains live; if the toy floor is judged artificial, the result is an artifact.

## Artifact Checks

- finite_values: `passed`
- agent_divergence: `passed`
- non_scalarizable_check: `passed`
- scalar_artifact_removed: `passed`
- heldout_divergences: `[{"environment": "heldout_incommensurable_threshold", "geometric_mean": "extractive_growth", "incomplete_preference": "preserve_threshold", "valid_geometric_mean_available": false}, {"environment": "heldout_incommensurable_sacred_floor", "geometric_mean": "major_gain_violate_floor", "incomplete_preference": "modest_gain_preserve_floor", "valid_geometric_mean_available": false}]`
