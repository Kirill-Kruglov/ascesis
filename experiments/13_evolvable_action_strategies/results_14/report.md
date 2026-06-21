# Experiment 14 Report: Robustness and Ablation

Final verdict: **A. At least one Experiment 13 kernel is robust.**

## Validation Checks

| check | result |
|---|---:|
| feeder_observation_excludes_strategy_parameters | `True` |
| derived_exploitative_label_not_in_policy | `True` |
| fixed_hidden_types_absent | `True` |
| mutation_and_selection_occur | `True` |
| exploitative_strategies_rise_under_no_control_baseline | `True` |
| feature_proxy_fails_W1 | `True` |
| monoculture_fails_W5 | `True` |
| full_policy_reproduces_at_least_one_exp13_viable_cell | `True` |
| ablation_code_preserves_base_full_dynamics | `True` |
| no_fixed_mi_claim_without_band | `True` |

## Required Questions

1. Experiment 13 viable cells reproduced: `3` of `3` under original seeds.
2. Seed robustness pass: `2` of `3` cells.
3. Viable regions are classified below; perturbation pass rate is the local-contiguity proxy.
4. Load-bearing components are shown by ablation deltas in `raw/summary.csv`; the report table lists the top ablation rows.
5. Diversity is evaluated via no-diversity ablations and response diversity metrics.
6. Action-channel containment robustness is evaluated by capture/exploit mass under perturbations and ablations.
7. W2 pure-capture boundary: `C. broad viable region under stronger containment` with `19` non-trivial viable boundary cells.
8. R sweep MI band: `0.004` to `0.032`; fixed-MI claim is not made.
9. Kernel classification by cell is below.
10. Next falsifiable test: rerun the robust cell in a richer graph with adversarially shifted delayed-consequence MI and unchanged pre-registration thresholds.

## Cell Classification

| cell | class | seed permanence | perm CI lo | collapse CI hi | perturb pass rate |
|---|---|---:|---:|---:|---:|
| W6_action_channel_containment | Robust | 1.000 | 0.963 | 0.037 | 0.929 |
| W6_consequence_plus_diversity | Robust | 1.000 | 0.963 | 0.037 | 0.929 |
| W1_consequence_plus_diversity | Seed artifact | 0.540 | 0.443 | 0.037 | 0.429 |

## Seed Robustness Metrics

| cell | n | permanence | perm lo | perm hi | collapse | collapse hi | capture | exploit mass | welfare | response diversity | pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| W6_action_channel_containment | 100 | 1.000 | 0.963 | 1.000 | 0.000 | 0.037 | 0.427 | 0.190 | 0.959 | 0.967 | 1 |
| W6_consequence_plus_diversity | 100 | 1.000 | 0.963 | 1.000 | 0.000 | 0.037 | 0.426 | 0.194 | 0.955 | 0.965 | 1 |
| W1_consequence_plus_diversity | 100 | 0.540 | 0.443 | 0.634 | 0.000 | 0.037 | 0.500 | 0.294 | 0.955 | 0.913 | 0 |

## Ablation Snapshot

| cell | ablation | permanence | capture | exploit mass | welfare | cost |
|---|---|---:|---:|---:|---:|---:|
| W1_consequence_plus_diversity | no_neighbor_consequence | 0.760 | 0.474 | 0.258 | 0.948 | 0.014 |
| W1_consequence_plus_diversity | random_allocation | 0.640 | 0.484 | 0.252 | 0.973 | 0.014 |
| W1_consequence_plus_diversity | no_migration_friction | 0.600 | 0.499 | 0.286 | 0.955 | 0.012 |
| W1_consequence_plus_diversity | no_response_to_aid | 0.560 | 0.491 | 0.285 | 0.958 | 0.014 |
| W1_consequence_plus_diversity | full | 0.480 | 0.506 | 0.298 | 0.955 | 0.016 |
| W1_consequence_plus_diversity | no_diversity_support | 0.480 | 0.513 | 0.278 | 0.945 | 0.015 |
| W1_consequence_plus_diversity | no_replication_throttle | 0.360 | 0.594 | 0.430 | 0.691 | 0.029 |
| W1_consequence_plus_diversity | no_aid_escrow | 0.320 | 0.516 | 0.320 | 0.951 | 0.014 |
| W1_consequence_plus_diversity | feature_proxy_only | 0.240 | 0.533 | 0.367 | 0.922 | 0.015 |
| W1_consequence_plus_diversity | no_containment | 0.000 | 0.668 | 0.633 | 0.006 | 0.000 |
| W1_consequence_plus_diversity | no_anti_concentration | 0.000 | 0.681 | 0.602 | 0.920 | 0.016 |
| W6_action_channel_containment | full | 1.000 | 0.425 | 0.181 | 0.956 | 0.009 |
| W6_action_channel_containment | no_diversity_support | 1.000 | 0.425 | 0.181 | 0.956 | 0.009 |
| W6_action_channel_containment | no_response_to_aid | 1.000 | 0.425 | 0.194 | 0.960 | 0.008 |
| W6_action_channel_containment | no_replication_throttle | 1.000 | 0.311 | 0.067 | 0.856 | 0.022 |
| W6_action_channel_containment | no_neighbor_consequence | 1.000 | 0.421 | 0.190 | 0.947 | 0.008 |
| W6_action_channel_containment | feature_proxy_only | 1.000 | 0.433 | 0.267 | 0.894 | 0.009 |
| W6_action_channel_containment | random_allocation | 1.000 | 0.369 | 0.107 | 0.977 | 0.007 |
| W6_action_channel_containment | no_aid_escrow | 0.960 | 0.441 | 0.227 | 0.953 | 0.008 |
| W6_action_channel_containment | no_migration_friction | 0.960 | 0.423 | 0.191 | 0.954 | 0.008 |
| W6_action_channel_containment | no_containment | 0.000 | 0.680 | 0.615 | 0.014 | 0.000 |
| W6_action_channel_containment | no_anti_concentration | 0.000 | 0.604 | 0.481 | 0.927 | 0.012 |
| W6_consequence_plus_diversity | full | 1.000 | 0.433 | 0.204 | 0.954 | 0.008 |
| W6_consequence_plus_diversity | no_diversity_support | 1.000 | 0.433 | 0.202 | 0.955 | 0.008 |
| W6_consequence_plus_diversity | no_response_to_aid | 1.000 | 0.425 | 0.194 | 0.960 | 0.008 |
| W6_consequence_plus_diversity | no_aid_escrow | 1.000 | 0.439 | 0.230 | 0.958 | 0.009 |
| W6_consequence_plus_diversity | no_migration_friction | 1.000 | 0.425 | 0.195 | 0.957 | 0.008 |
| W6_consequence_plus_diversity | no_neighbor_consequence | 1.000 | 0.421 | 0.190 | 0.947 | 0.008 |
