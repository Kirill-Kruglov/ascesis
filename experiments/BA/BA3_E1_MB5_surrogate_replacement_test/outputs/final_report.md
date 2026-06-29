# BA3.E1 MB5 Surrogate Replacement Test

**Decision:** `MB5_functionally_split`.
**Successful transition surrogates:** `[]`.
**Successful subfamily replacements:** `['S4b_reporting_ratios', 'S4c_projection_resource_hhi', 'S4d_capture_components']`.
**Best false-safe surrogate:** `S4a_policy_visible_concentration` = `0.31171889150516213`.
**Best benefit/cost surrogate:** `S4b_reporting_ratios` = `1.9415341783280828`.
**Best transition benefit/cost surrogate:** `S4a_policy_visible_concentration` = `1.0452775637545912`.

## Summary

| run | false-safe | pure blindness | future collapse | witnesses | cost | benefit | ratio | validity |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| baseline | 0.3525 | 0.1314 | 0.5532 | 2650 | 0.6454 | 1.0000 | 1.5494 | valid |
| MB5_removal | 0.3738 | 0.0738 | 0.5919 | 5731 | 0.8607 | 0.9859 | 1.1455 | valid |
| S1_absolute_deficit | 0.5650 | 0.0795 | 0.7086 | 4964 | 0.8631 | 0.8806 | 1.0202 | valid |
| S2_threshold_boolean | 0.3823 | 0.0883 | 0.5941 | 6338 | 0.9833 | 0.9830 | 0.9997 | valid |
| S3_conservative_upper_bound | 0.3702 | 0.0974 | 0.5691 | 5836 | 0.9570 | 0.9889 | 1.0333 | valid |
| S4a_policy_visible_concentration | 0.3117 | 0.0888 | 0.5250 | 5652 | 0.9502 | 0.9933 | 1.0453 | valid |
| S4b_reporting_ratios | 0.3525 | 0.1314 | 0.5532 | 2764 | 0.5151 | 1.0000 | 1.9415 | valid |
| S4c_projection_resource_hhi | 0.3525 | 0.1314 | 0.5532 | 2753 | 0.5286 | 1.0000 | 1.8918 | valid |
| S4d_capture_components | 0.3525 | 0.1314 | 0.5532 | 3081 | 0.5932 | 1.0000 | 1.6858 | valid |

## Required Questions

1. Can MB5 be replaced by any valid surrogate? Full transition-level replacement: `False`; subfamily replacement: `True`.
2. Best false-safe behavior: `S4a_policy_visible_concentration`.
3. Best benefit/cost ratio: `S4b_reporting_ratios` overall; `S4a_policy_visible_concentration` among transition-level surrogates.
4. Surrogates reducing witness count: `[]`.
5. Collapse distribution preservation is reported in `semantic_validity.csv`; severe shifts are excluded from success.
6. MB5 status: `MB5_functionally_split`.
7. Most suspicious subfamily: projection/reporting `resource_hhi` if it changes little while retaining structural cost.
8. Indispensable subfamily: any S4 variant whose replacement worsens false-safe materially; see `surrogate_comparison.csv`.
9. Strongest counterexample against H1: `S1_absolute_deficit`.
10. Strongest counterexample against H0: `S4b_reporting_ratios`.

## Interpretation

A transition-level surrogate is counted as successful only if it is semantically valid, matches or improves baseline false-safe within the materiality band, does not materially increase pure blindness, and reduces structural cost or monotonicity witnesses. Reporting/projection-only variants are counted only as subfamily replacements, not as full MB5 replacements.
