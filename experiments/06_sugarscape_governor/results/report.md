# 06 Sugarscape Governor Report

SPEC hash: `63fedf2b5a99f8a5f1b4ec3bd75548372ba27b20e6739080cf2d69b59903acc2`

## Distribution Summary

| split | governor | median collapse | q25 | q75 | shock survival | mean Gini | median final pop |
|---|---|---:|---:|---:|---:|---:|---:|
| train | arithmetic_mean | 116.0 | 104.5 | 120.0 | 0.00 | 0.237 | 0.0 |
| train | geometric_mean | 163.0 | 122.2 | 180.0 | 0.60 | 0.265 | 5.0 |
| train | incomplete_preference | 121.5 | 110.0 | 135.8 | 0.27 | 0.236 | 0.0 |
| heldout | arithmetic_mean | 106.0 | 96.5 | 119.5 | 0.03 | 0.240 | 0.0 |
| heldout | geometric_mean | 180.0 | 127.2 | 180.0 | 0.63 | 0.263 | 9.0 |
| heldout | incomplete_preference | 119.0 | 102.2 | 128.8 | 0.20 | 0.244 | 0.0 |

## Held-Out A/B Result

- incomplete median collapse: `119.0`
- hedger median collapse: `180.0`
- incomplete > hedger pairwise win rate: `0.23`
- pairwise ties: `2`
- result by pre-registered criterion: `negative_or_inconclusive`

## Artifact Checks

| check | result | interpretation |
|---|---|---|
| emergent_floor_not_penalty | passed | No governor reward contains population-threshold penalty; floor is estimated post hoc from demographic recovery. |
| hedger_scalar_probe | passed | Geometric hedger chooses `balanced` in a scalar risk sanity probe. |
| seed_distribution_reported | passed | Reports median, q25, q75, and pairwise held-out seeds. |
| ab_identity | passed | Same train/held-out seeds and environment parameters are used for all governors. |
| allocation_divergence | passed | Held-out modal allocation divergences: `[{"step": 50, "modal_allocations": {"arithmetic_mean": 0.8, "geometric_mean": 0.65, "incomplete_preference": 0.8}}, {"step": 90, "modal_allocations": {"arithmetic_mean": 0.5, "geometric_mean": 0.65, "incomplete_preference": 0.5}}]`. |

## Source Note

The ecological rules are Sugarscape-style rather than a new toy world: sugar landscape, growback, metabolism, vision movement, aging, reproduction, and Gini wealth. The governor layer is the added experimental intervention.

## Outputs

- Raw summary: `results/raw/results.json`, `results/raw/results.csv`
- Population-by-step raw data: `results/raw/population_by_step.csv`
- Plot: `results/population_survival.svg`
