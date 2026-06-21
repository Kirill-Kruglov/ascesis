# Experiment 09 Report: Break Trivial Policies

Final verdict: **B. Trivial policies broken; no consequence-neighbor policy survives.**

## Validation Checks

| check | result |
|---|---:|
| t_irrev_used_in_dynamics | `True` |
| irreversible_failures_possible | `True` |
| last_aid_updates_nonzero | `True` |
| neighbor_metrics_use_neighbors | `True` |
| feature_proxy_trap_active | `True` |
| sag_ambiguity_trap_active | `True` |
| monoculture_trap_active | `True` |
| fixed_mi_target_achieved | `True` |
| trivial_policy_break_test_passed | `True` |
| consequence_neighbor_policy_survives | `False` |

## World Outcomes

| world | policy | permanence | collapse | capture | irrev failures | R | MI |
|---|---|---:|---:|---:|---:|---:|---:|
| FIXED_MI_DELAY | local_global_neighbor | 0.000 | 0.000 | 1.000 | 2.00 | 8.00 | 0.129 |
| FIXED_MI_DELAY | local_global_neighbor | 0.000 | 0.000 | 1.000 | 2.00 | 4.00 | 0.129 |
| FIXED_MI_DELAY | local_global_neighbor | 0.000 | 0.000 | 1.000 | 2.00 | 2.00 | 0.108 |
| FIXED_MI_DELAY | local_global_neighbor | 0.000 | 0.000 | 1.000 | 2.00 | 1.14 | 0.149 |
| FIXED_MI_DELAY | local_global_neighbor | 0.000 | 0.000 | 1.000 | 2.00 | 0.80 | 0.129 |
| FIXED_MI_DELAY | neighbor_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 8.00 | 0.128 |
| FIXED_MI_DELAY | neighbor_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 4.00 | 0.128 |
| FIXED_MI_DELAY | neighbor_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 2.00 | 0.107 |
| FIXED_MI_DELAY | neighbor_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 1.14 | 0.145 |
| FIXED_MI_DELAY | neighbor_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 0.80 | 0.124 |
| FIXED_MI_DELAY | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 2.00 | 8.00 | 0.130 |
| FIXED_MI_DELAY | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 2.00 | 4.00 | 0.130 |
| FIXED_MI_DELAY | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 2.00 | 2.00 | 0.109 |
| FIXED_MI_DELAY | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 2.00 | 1.14 | 0.150 |
| FIXED_MI_DELAY | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 2.00 | 0.80 | 0.130 |
| T1_proxy_trap | always_aid_sagging | 0.000 | 0.700 | 1.000 | 6.80 | 3.50 | 0.866 |
| T1_proxy_trap | always_cut_sagging | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.868 |
| T1_proxy_trap | diversity_all_types | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.865 |
| T1_proxy_trap | diversity_non_adversarial_only | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.863 |
| T1_proxy_trap | feature_proxy | 0.000 | 1.000 | 1.000 | 7.67 | 3.50 | 0.864 |
| T1_proxy_trap | local_global_neighbor | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.865 |
| T1_proxy_trap | monoculture_optimizer | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.861 |
| T1_proxy_trap | neighbor_consequence | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.856 |
| T1_proxy_trap | no_diversity_floor | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.857 |
| T1_proxy_trap | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.862 |
| T1_proxy_trap | self_consequence | 0.000 | 0.000 | 1.000 | 3.00 | 3.50 | 0.870 |
| T2_sag_ambiguity_trap | always_aid_sagging | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.614 |
| T2_sag_ambiguity_trap | always_cut_sagging | 0.000 | 1.000 | 1.000 | 4.00 | 3.50 | 0.911 |
| T2_sag_ambiguity_trap | diversity_all_types | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.621 |
| T2_sag_ambiguity_trap | diversity_non_adversarial_only | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.621 |
| T2_sag_ambiguity_trap | feature_proxy | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.620 |
| T2_sag_ambiguity_trap | local_global_neighbor | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.621 |
| T2_sag_ambiguity_trap | monoculture_optimizer | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.622 |
| T2_sag_ambiguity_trap | neighbor_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.623 |
| T2_sag_ambiguity_trap | no_diversity_floor | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.621 |
| T2_sag_ambiguity_trap | response_to_neighbor_aid | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.618 |
| T2_sag_ambiguity_trap | self_consequence | 0.000 | 0.000 | 1.000 | 2.00 | 3.50 | 0.620 |
| T3_monoculture_trap | always_aid_sagging | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | always_cut_sagging | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | diversity_all_types | 0.967 | 0.033 | 0.000 | 0.30 | 3.50 | 0.000 |
| T3_monoculture_trap | diversity_non_adversarial_only | 1.000 | 0.000 | 0.000 | 0.00 | 3.50 | 0.000 |
| T3_monoculture_trap | feature_proxy | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | local_global_neighbor | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | monoculture_optimizer | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | neighbor_consequence | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | no_diversity_floor | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | response_to_neighbor_aid | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |
| T3_monoculture_trap | self_consequence | 0.000 | 1.000 | 0.000 | 5.00 | 3.50 | 0.000 |

## Interpretation

Experiment 09 is a semantics repair pass, not a larger simulator. The key question is whether the toy substrate now breaks the policies that made experiment 08 fragile.

If the verdict is A, the trivial comparators failed in their target traps and at least one neighbor-consequence policy survived. If B, trivial policies were broken but the consequence-neighbor construction still failed. If C or D, the substrate is still not suitable for reading the intended question.
