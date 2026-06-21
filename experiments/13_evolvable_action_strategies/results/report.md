# Experiment 13 Report: Evolvable Action Strategies

Final verdict: **A. Evolvable-strategy substrate exposes type-blind causal levers and a non-trivial viability kernel exists.**
Causal audit: **A. Type-blind levers reduce exploitative strategy mass.**

## Validation Checks

| check | result |
|---|---:|
| feeder_observation_excludes_strategy_parameters | `True` |
| fixed_hidden_types_absent | `True` |
| derived_exploitative_label_not_in_policy | `True` |
| feature_proxy_fails_W1 | `True` |
| monoculture_fails_W5 | `True` |
| exploitative_strategies_rise_under_no_control | `True` |
| oracle_not_required_to_change_capture | `True` |
| action_containment_changes_exploitation_payoff | `True` |
| capture_metric_is_composite | `True` |
| mutation_and_selection_occur | `True` |
| oracle_audit_changes_exploitation | `True` |
| audit_baseline_exploitation_present | `True` |

## Required Interpretation

- Best type-blind audit delta exploitative mass: `-0.433`.
- Best oracle audit delta exploitative mass: `-0.692`.
- Viable governance cells: `3`.
- Capture is composite, not a binary hidden-type threshold; component columns are in `raw/summary.csv`.
- Derived labels are used only for metrics and diversity buckets; they are not policy observations.

## Audit Ranking

| world | intervention | capture | delta capture | exploit mass | delta exploit mass | welfare | collapse | cost | events | MI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| W4_scavenger_catastrophe | oracle_suppress_exploit_strategy_params | 0.276 | -0.446 | 0.000 | -0.692 | 0.435 | 0.160 | 0.000 | 4.0 | 0.000 |
| W2_pure_capture | oracle_suppress_exploit_strategy_params | 0.272 | -0.439 | 0.000 | -0.664 | 0.471 | 0.040 | 0.000 | 3.0 | 0.001 |
| W6_mutation_corridor | oracle_suppress_exploit_strategy_params | 0.273 | -0.422 | 0.000 | -0.621 | 0.375 | 0.280 | 0.000 | 3.0 | 0.000 |
| W6_mutation_corridor | combined_type_blind_containment | 0.434 | -0.261 | 0.187 | -0.433 | 0.933 | 0.000 | 0.005 | 188.2 | 0.042 |
| W4_scavenger_catastrophe | combined_type_blind_containment | 0.520 | -0.202 | 0.291 | -0.400 | 0.877 | 0.000 | 0.007 | 194.6 | 0.022 |
| W2_pure_capture | combined_type_blind_containment | 0.559 | -0.151 | 0.400 | -0.264 | 0.821 | 0.000 | 0.008 | 237.3 | 0.026 |
| W4_scavenger_catastrophe | type_blind_extraction_cap | 0.716 | -0.006 | 0.660 | -0.032 | 0.174 | 1.000 | 0.006 | 246.8 | 0.001 |
| W6_mutation_corridor | audit_no_intervention | 0.695 | 0.000 | 0.621 | 0.000 | 0.016 | 1.000 | 0.000 | 0.0 | 0.017 |
| W2_pure_capture | audit_no_intervention | 0.710 | 0.000 | 0.664 | 0.000 | 0.014 | 1.000 | 0.000 | 0.0 | 0.001 |
| W4_scavenger_catastrophe | audit_no_intervention | 0.722 | 0.000 | 0.692 | 0.000 | 0.122 | 1.000 | 0.000 | 0.0 | 0.001 |
| W4_scavenger_catastrophe | type_blind_aid_escrow | 0.727 | 0.004 | 0.693 | 0.001 | 0.168 | 1.000 | 0.010 | 256.7 | 0.001 |
| W4_scavenger_catastrophe | type_blind_migration_friction | 0.726 | 0.004 | 0.694 | 0.003 | 0.164 | 1.000 | 0.006 | 217.0 | 0.001 |
| W2_pure_capture | type_blind_extraction_cap | 0.716 | 0.006 | 0.669 | 0.005 | 0.057 | 1.000 | 0.009 | 362.3 | 0.004 |
| W2_pure_capture | type_blind_migration_friction | 0.728 | 0.018 | 0.671 | 0.007 | 0.047 | 1.000 | 0.009 | 339.0 | 0.008 |

## Best Governance Cells

| viable | world | policy | permanence | collapse | capture | strict zero | exploit mass | coop mass | welfare | min welfare | response diversity | cost | false containment | MI |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | W6_mutation_corridor | action_channel_containment | 1.000 | 0.000 | 0.420 | 0.000 | 0.186 | 0.814 | 0.959 | 0.890 | 0.969 | 0.008 | 0.000 | 0.018 |
| 1 | W6_mutation_corridor | consequence_plus_diversity | 1.000 | 0.000 | 0.432 | 0.000 | 0.193 | 0.807 | 0.953 | 0.899 | 0.964 | 0.008 | 0.000 | 0.018 |
| 1 | W1_proxy_goodhart | consequence_plus_diversity | 0.600 | 0.000 | 0.497 | 0.000 | 0.287 | 0.713 | 0.961 | 0.896 | 0.928 | 0.014 | 0.000 | 0.016 |
| 0 | W3_catastrophe_ambiguity | action_channel_containment | 0.840 | 0.000 | 0.456 | 0.000 | 0.105 | 0.895 | 0.944 | 0.818 | 0.936 | 0.014 | 0.753 | 0.011 |
| 0 | W3_catastrophe_ambiguity | consequence_plus_diversity | 0.840 | 0.000 | 0.461 | 0.000 | 0.114 | 0.886 | 0.949 | 0.834 | 0.944 | 0.014 | 0.895 | 0.011 |
| 0 | W4_scavenger_catastrophe | action_channel_containment | 0.760 | 0.000 | 0.492 | 0.000 | 0.251 | 0.749 | 0.943 | 0.814 | 0.992 | 0.009 | 1.276 | 0.011 |
| 0 | W4_scavenger_catastrophe | action_channel_containment | 0.560 | 0.000 | 0.501 | 0.000 | 0.247 | 0.753 | 0.965 | 0.885 | 0.966 | 0.010 | 0.767 | 0.010 |
| 0 | W4_scavenger_catastrophe | action_channel_containment | 0.520 | 0.000 | 0.501 | 0.000 | 0.236 | 0.764 | 0.977 | 0.910 | 0.961 | 0.011 | 0.504 | 0.006 |
| 0 | W1_proxy_goodhart | action_channel_containment | 0.400 | 0.000 | 0.505 | 0.000 | 0.262 | 0.738 | 0.953 | 0.849 | 0.911 | 0.015 | 0.000 | 0.017 |
| 0 | W4_scavenger_catastrophe | consequence_plus_diversity | 0.400 | 0.000 | 0.512 | 0.000 | 0.273 | 0.727 | 0.962 | 0.896 | 0.970 | 0.010 | 0.746 | 0.008 |
| 0 | W2_pure_capture | action_channel_containment | 0.240 | 0.000 | 0.542 | 0.000 | 0.303 | 0.697 | 0.936 | 0.769 | 0.802 | 0.022 | 0.000 | 0.018 |
| 0 | W2_pure_capture | consequence_plus_diversity | 0.200 | 0.000 | 0.537 | 0.000 | 0.368 | 0.632 | 0.956 | 0.893 | 0.907 | 0.015 | 0.000 | 0.008 |
| 0 | W2_pure_capture | consequence_plus_diversity | 0.160 | 0.000 | 0.542 | 0.000 | 0.378 | 0.622 | 0.952 | 0.887 | 0.918 | 0.015 | 0.000 | 0.012 |
| 0 | W2_pure_capture | action_channel_containment | 0.120 | 0.000 | 0.544 | 0.000 | 0.368 | 0.632 | 0.946 | 0.838 | 0.927 | 0.014 | 0.000 | 0.013 |
