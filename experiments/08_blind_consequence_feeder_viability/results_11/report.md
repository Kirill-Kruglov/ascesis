# Experiment 11 Report: Action-Channel Containment

Final verdict: **D. Result invalid due to failed validation.**

## Validation Checks

| check | result |
|---|---:|
| hidden_type_absent_from_observation | `True` |
| controls_fire_only_from_delayed_consequence | `True` |
| controls_have_cost | `True` |
| feature_proxy_fails_T1 | `True` |
| always_cut_fails_T2 | `True` |
| always_aid_fails_T2 | `True` |
| monoculture_fails_T3 | `True` |
| action_containment_fires | `True` |
| not_all_zones_starved | `True` |
| pure_catastrophe_test_present | `True` |
| capture_not_one_for_all_action_containment | `False` |

## Required Analyses

1. Did any action-channel lever reduce capture? See channel ranking below; reduction is computed relative to Experiment 10 zone penalties in the same substrate family.
2. Strongest channel: `action_containment_anti_concentration` in `MIXED_CAPTURE_CATASTROPHE` with capture `1.000` and reduction `0.000` versus zone penalties.
3. Minimal viable containment threshold: none found under the action-containment viability criterion.
4. Starvation check: welfare/collapse/irreversible failures are reported in raw summary and Best Action Cells; viability rejects starvation-only wins.
5. Catastrophe preservation: pure-catastrophe rows track `false_containment_rate` and are excluded from capture-kernel evidence.
6. Diversity complement: combined containment plus diversity is compared directly with combined containment and diversity-only rows.
7. R visibility: delay sweep rows for `combined_action_containment` are in raw summary; no causal claim beyond this toy sweep.
8. Viable region breadth: `0` action-containment viable cells out of `131` action-containment cells.

## Channel Ranking

| policy | best world | capture | reduction vs zone penalty | permanence | welfare | collapse | cost | false containment | events | HHI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| action_containment_anti_concentration | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.775 | 0.000 | 0.011 | 0.069 | 16.9 | 0.138 |
| action_containment_influence_throttle | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.772 | 0.000 | 0.013 | 0.059 | 17.1 | 0.144 |
| action_containment_extraction_cap | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.772 | 0.000 | 0.017 | 0.060 | 17.2 | 0.144 |
| action_containment_aid_escrow | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.772 | 0.000 | 0.022 | 0.071 | 21.0 | 0.147 |
| action_containment_migration_friction | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.772 | 0.000 | 0.137 | 0.059 | 17.1 | 0.144 |
| action_containment_replication_throttle | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.772 | 0.000 | 0.186 | 0.059 | 17.1 | 0.144 |
| combined_action_containment_plus_response_to_aid | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.773 | 0.000 | 0.273 | 0.068 | 17.9 | 0.144 |
| combined_action_containment | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.773 | 0.000 | 0.275 | 0.059 | 17.0 | 0.144 |
| combined_action_containment_plus_diversity | MIXED_CAPTURE_CATASTROPHE | 1.000 | 0.000 | 0.000 | 0.773 | 0.000 | 0.276 | 0.059 | 17.0 | 0.144 |

## Best Action Cells

| action viable | raw viable | world | policy | C | duration | permanence | capture | strict zero capture | collapse | irrev frac | welfare | diversity | cost | false containment | events | escrowed | intercepted |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | PURE_CATASTROPHE | combined_action_containment_plus_diversity | 0.25 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.532 | 0.243 | 0.089 | 14.0 | 0.00 | 64.90 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment_plus_diversity | 0.7 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.529 | 0.467 | 0.089 | 14.0 | 0.00 | 63.37 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment | 0.7 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.429 | 0.465 | 0.089 | 14.0 | 0.00 | 63.57 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment_plus_response_to_aid | 0.7 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.429 | 0.464 | 0.088 | 13.9 | 0.00 | 63.44 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment_plus_diversity | 0.45 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.532 | 0.363 | 0.089 | 14.0 | 0.00 | 64.13 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment | 0.45 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.427 | 0.362 | 0.089 | 14.0 | 0.00 | 64.33 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment_plus_response_to_aid | 0.45 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.427 | 0.360 | 0.088 | 13.9 | 0.00 | 64.23 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment | 0.45 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.431 | 0.359 | 0.089 | 14.0 | 0.00 | 64.31 |
| 0 | 0 | PURE_CATASTROPHE | action_containment_replication_throttle | 0.7 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.427 | 0.343 | 0.089 | 14.0 | 0.00 | 66.55 |
| 0 | 0 | PURE_CATASTROPHE | action_containment_migration_friction | 0.7 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.423 | 0.266 | 0.089 | 14.0 | 0.00 | 66.30 |
| 0 | 0 | PURE_CATASTROPHE | action_containment_replication_throttle | 0.45 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.426 | 0.254 | 0.089 | 14.0 | 0.00 | 66.46 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment | 0.45 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.422 | 0.243 | 0.044 | 7.8 | 0.00 | 65.16 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment | 0.25 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.425 | 0.242 | 0.089 | 14.0 | 0.00 | 65.11 |
| 0 | 0 | PURE_CATASTROPHE | combined_action_containment_plus_response_to_aid | 0.25 | 4 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.426 | 0.241 | 0.088 | 13.9 | 0.00 | 65.05 |

## Capture-Relevant Action Cells

These rows exclude pure-catastrophe controls. The validation failure is that all capture-relevant action-containment rows retain `capture=1.0`.

| world | policy | C | R | adv | severity | permanence | capture | welfare | diversity | cost | false containment | events | pressure before | pressure after |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MIXED_CAPTURE_CATASTROPHE | action_containment_anti_concentration | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.775 | 0.530 | 0.011 | 0.069 | 16.9 | 2.029 | 2.031 |
| SCAVENGER_CATASTROPHE | action_containment_anti_concentration | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.774 | 0.530 | 0.011 | 0.059 | 17.6 | 2.156 | 2.157 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_influence_throttle | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.772 | 0.533 | 0.013 | 0.059 | 17.1 | 2.035 | 2.037 |
| SCAVENGER_CATASTROPHE | action_containment_influence_throttle | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.757 | 0.535 | 0.014 | 0.060 | 17.8 | 2.165 | 2.166 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_anti_concentration | 0.45 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.775 | 0.530 | 0.015 | 0.069 | 16.9 | 2.029 | 2.031 |
| SCAVENGER_CATASTROPHE | action_containment_anti_concentration | 0.45 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.774 | 0.530 | 0.015 | 0.059 | 17.6 | 2.156 | 2.157 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_influence_throttle | 0.45 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.772 | 0.532 | 0.017 | 0.059 | 17.1 | 2.035 | 2.037 |
| SCAVENGER_CATASTROPHE | action_containment_influence_throttle | 0.45 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.757 | 0.535 | 0.017 | 0.060 | 17.8 | 2.165 | 2.166 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_extraction_cap | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.772 | 0.533 | 0.017 | 0.060 | 17.2 | 2.036 | 2.037 |
| SCAVENGER_CATASTROPHE | action_containment_extraction_cap | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.756 | 0.537 | 0.018 | 0.063 | 18.3 | 2.166 | 2.167 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_anti_concentration | 0.7 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.775 | 0.530 | 0.019 | 0.069 | 16.9 | 2.029 | 2.031 |
| SCAVENGER_CATASTROPHE | action_containment_anti_concentration | 0.7 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.774 | 0.530 | 0.020 | 0.059 | 17.6 | 2.156 | 2.157 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_influence_throttle | 0.7 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.772 | 0.532 | 0.021 | 0.059 | 17.1 | 2.035 | 2.037 |
| MIXED_CAPTURE_CATASTROPHE | action_containment_aid_escrow | 0.25 | 3.50 | 0.70 | 0.55 | 0.000 | 1.000 | 0.772 | 0.533 | 0.022 | 0.071 | 21.0 | 2.033 | 2.035 |
