# BA1.E1 Monotonicity Breaker Ablation Map

**Decision:** `Case C / H2_supported`.
**Top valid single mechanism:** `none_clean_ablation`.
**Dominance ratio:** `0.000`.
**Apparent invalid dominant mechanism:** `MB4` (CI=1.000).

## Summary Table

| run | false_safe | false_unsafe | pure_blindness | accept | future_collapse | witnesses | semantic_validity |
|---|---:|---:|---:|---:|---:|---:|---|
| baseline | 0.3525 | 0.0000 | 0.1314 | 0.6901 | 0.5532 | 2650 | baseline |
| MB1 | 0.7297 | 0.0000 | 0.0877 | 0.4778 | 0.8708 | 2488 | comparable_enough_for_diagnostic |
| MB2 | 0.3779 | 0.0000 | 0.2040 | 0.6959 | 0.5671 | 2722 | comparable_enough_for_diagnostic |
| MB3 | 0.7476 | 0.0000 | 0.0873 | 0.4787 | 0.8792 | 2532 | comparable_enough_for_diagnostic |
| MB4 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0 | severe_semantic_shift |
| MB5 | 0.3738 | 0.0006 | 0.0738 | 0.6513 | 0.5919 | 5731 | comparable_enough_for_diagnostic |

## Contribution Index

| mechanism | ablated false_safe | CI | semantic_validity |
|---|---:|---:|---|
| MB1 | 0.7297 | -1.0698 | comparable_enough_for_diagnostic |
| MB2 | 0.3779 | -0.0719 | comparable_enough_for_diagnostic |
| MB3 | 0.7476 | -1.1205 | comparable_enough_for_diagnostic |
| MB4 | 0.0000 | 1.0000 | severe_semantic_shift |
| MB5 | 0.3738 | -0.0603 | comparable_enough_for_diagnostic |

## Required Questions

1. Does one mechanism dominate? No; DR=0.000.
2. Largest measured contributor: `none_clean_ablation`.
3. Semantically indispensable mechanisms: any ablation marked `severe_semantic_shift`; see `contribution_index.csv`.
4. Implementation artifacts: MB2/MB3 coupling in `choose_alloc`; MB5 measurement-vs-policy split.
5. Removable without material semantic change: ablations marked `comparable_enough_for_diagnostic` only.
6. Taxonomy: useful but should be revised into submechanisms; see `mechanism_revision.md`.
7. Primary failure mode: `the only apparently dominant ablation is a severe semantic shift; clean single-mechanism ablations do not materially reduce false-safe error`.
8. Strongest counterexample: worse deficit-ordered states can remain shield-SAFE because the unchanged 18.0 shield tracks mean-welfare deficit and omits spread, mass, and forward dynamics.

## Interpretation

This experiment does not repair the abstraction. It maps whether removing one structural mechanism at a time explains the dangerous false-safe error of the existing 18.0/18.1 shield. Negative or weak CI values mean that removing the mechanism did not reduce the original false-safe failure on this diagnostic grid.
A CI from an ablation marked `severe_semantic_shift` is not counted as evidence for H0; it means the mechanism is semantically indispensable under this implementation.
