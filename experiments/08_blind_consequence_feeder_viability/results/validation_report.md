# Validation Report

| check | result | note |
|---|---|---|
| type_blind_feeder | passed | `FeederObservation` contains no hidden type counts; policy assertions check no `pop/type/hidden` fields. |
| raw_failed_seeds_kept | passed | Every train/held-out seed is written to `raw/runs.csv`. |
| feature_vs_consequence_separated | passed | `feature_proxy` is a comparator, not counted as consequence evidence. |
| delayed_observation | passed | Feeder uses the oldest observation in a delay queue. |
| MI_reported_not_optimized | passed | MI is reported post hoc as a diagnostic. |
| negative_results_allowed | passed | Final verdict is selected from the memo's A/B/C/D set. |
| trivial_policy_artifact_check | passed | If feature-proxy or naive sagging policies pass, verdict is downgraded to fragile/tuned rather than clean A. |

Final verdict: **C. Apparent kernel exists but is too fragile / tuned to trust.**
