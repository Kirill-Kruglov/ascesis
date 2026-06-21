# Experiment 16 Sensitivity Report

Final verdict: **BD: one AC implementation alone reproduces C_full.**

## Validation Checks

| check | result |
|---|---:|
| feeder_observation_excludes_strategy_parameters | `True` |
| derived_exploitative_label_not_in_policy | `True` |
| fixed_hidden_types_absent | `True` |
| mutation_and_selection_occur | `True` |
| feature_proxy_fails_W1 | `True` |
| monoculture_fails_W5 | `True` |
| exploitative_strategies_rise_under_no_control | `True` |
| part_a_does_not_use_delayed_consequence | `True` |
| part_b_does_not_use_fixed_caps | `True` |
| ac_cg_strictly_dominates_singles_in_robust_worlds | `True` |
| boundary_exists_for_each_axis | `True` |
| decoupling_identifies_load_bearing_ac | `True` |
| smoke_mode | `False` |

## Threshold Stability

| world | AC+CG fraction | Type None fraction | stable |
|---|---:|---:|---:|
| W6_mutation_corridor | 1.000 | 0.000 | `True` |
| W3_catastrophe_ambiguity | 1.000 | 0.000 | `True` |
| W4_scavenger_catastrophe | 1.000 | 0.000 | `True` |
| W2_pure_capture | 0.000 | 1.000 | `False` |
| W5_monoculture_shock | 0.000 | 1.000 | `False` |

## Decoupling

| world | axis | point | variant | permanence | robust | capture | welfare |
|---|---|---|---|---:|---:|---:|---:|
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=0.60 | C_caps_only | 1.000 | `True` | 0.336 | 0.968 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=0.60 | C_dyn_only | 1.000 | `True` | 0.318 | 0.964 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=0.60 | C_full | 1.000 | `True` | 0.319 | 0.958 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=0.80 | C_caps_only | 0.875 | `True` | 0.457 | 0.946 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=0.80 | C_dyn_only | 0.975 | `True` | 0.406 | 0.966 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=0.80 | C_full | 0.963 | `True` | 0.409 | 0.962 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.00 | C_caps_only | 0.188 | `False` | 0.537 | 0.926 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.00 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.00 | C_full | 0.863 | `True` | 0.447 | 0.945 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.20 | C_caps_only | 0.125 | `False` | 0.631 | 0.909 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.20 | C_dyn_only | 0.425 | `False` | 0.524 | 0.943 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.20 | C_full | 0.350 | `False` | 0.530 | 0.936 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.40 | C_caps_only | 0.487 | `False` | 0.659 | 0.816 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.40 | C_dyn_only | 0.175 | `False` | 0.549 | 0.950 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.40 | C_full | 0.113 | `False` | 0.568 | 0.949 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.60 | C_caps_only | 0.512 | `False` | 0.683 | 0.782 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.60 | C_dyn_only | 0.125 | `False` | 0.561 | 0.954 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.60 | C_full | 0.125 | `False` | 0.563 | 0.950 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.80 | C_caps_only | 0.512 | `False` | 0.671 | 0.788 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.80 | C_dyn_only | 0.163 | `False` | 0.563 | 0.952 |
| W3_catastrophe_ambiguity | adversarial_pressure | adversarial_pressure=1.80 | C_full | 0.087 | `False` | 0.560 | 0.951 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.45 | C_caps_only | 0.312 | `False` | 0.525 | 0.911 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.45 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.45 | C_full | 0.900 | `True` | 0.452 | 0.938 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.62 | C_caps_only | 0.237 | `False` | 0.526 | 0.906 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.62 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.62 | C_full | 0.912 | `True` | 0.443 | 0.937 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.82 | C_caps_only | 0.450 | `False` | 0.513 | 0.904 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.82 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.12;strength=0.82 | C_full | 0.938 | `True` | 0.443 | 0.933 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.45 | C_caps_only | 0.163 | `False` | 0.540 | 0.923 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.45 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.45 | C_full | 0.838 | `True` | 0.457 | 0.941 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.62 | C_caps_only | 0.188 | `False` | 0.537 | 0.926 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.62 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.62 | C_full | 0.863 | `True` | 0.447 | 0.945 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.82 | C_caps_only | 0.200 | `False` | 0.533 | 0.925 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.82 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.18;strength=0.82 | C_full | 0.812 | `True` | 0.452 | 0.942 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.45 | C_caps_only | 0.150 | `False` | 0.539 | 0.925 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.45 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.45 | C_full | 0.887 | `True` | 0.448 | 0.947 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.62 | C_caps_only | 0.113 | `False` | 0.536 | 0.929 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.62 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.62 | C_full | 0.875 | `True` | 0.450 | 0.946 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.82 | C_caps_only | 0.212 | `False` | 0.533 | 0.928 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.82 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.24;strength=0.82 | C_full | 0.900 | `True` | 0.454 | 0.944 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.45 | C_caps_only | 0.150 | `False` | 0.539 | 0.929 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.45 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.45 | C_full | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.62 | C_caps_only | 0.150 | `False` | 0.539 | 0.928 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.62 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.62 | C_full | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.82 | C_caps_only | 0.163 | `False` | 0.539 | 0.929 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.82 | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | cap_tightness | share=0.32;strength=0.82 | C_full | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | default | default | C_caps_only | 0.188 | `False` | 0.537 | 0.926 |
| W3_catastrophe_ambiguity | default | default | C_dyn_only | 0.887 | `True` | 0.448 | 0.950 |
| W3_catastrophe_ambiguity | default | default | C_full | 0.863 | `True` | 0.447 | 0.945 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=0.60 | C_caps_only | 1.000 | `True` | 0.337 | 0.975 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=0.60 | C_dyn_only | 1.000 | `True` | 0.331 | 0.956 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=0.60 | C_full | 1.000 | `True` | 0.329 | 0.957 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=0.80 | C_caps_only | 1.000 | `True` | 0.373 | 0.961 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=0.80 | C_dyn_only | 1.000 | `True` | 0.361 | 0.966 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=0.80 | C_full | 1.000 | `True` | 0.361 | 0.965 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.00 | C_caps_only | 0.050 | `False` | 0.552 | 0.923 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.00 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.00 | C_full | 0.713 | `True` | 0.488 | 0.967 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.20 | C_caps_only | 0.000 | `False` | 0.640 | 0.886 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.20 | C_dyn_only | 0.487 | `False` | 0.510 | 0.960 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.20 | C_full | 0.438 | `False` | 0.510 | 0.960 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.40 | C_caps_only | 0.000 | `False` | 0.701 | 0.888 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.40 | C_dyn_only | 0.312 | `False` | 0.521 | 0.960 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.40 | C_full | 0.200 | `False` | 0.534 | 0.948 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.60 | C_caps_only | 0.000 | `False` | 0.680 | 0.891 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.60 | C_dyn_only | 0.175 | `False` | 0.549 | 0.950 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.60 | C_full | 0.188 | `False` | 0.541 | 0.950 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.80 | C_caps_only | 0.000 | `False` | 0.626 | 0.889 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.80 | C_dyn_only | 0.175 | `False` | 0.558 | 0.948 |
| W4_scavenger_catastrophe | adversarial_pressure | adversarial_pressure=1.80 | C_full | 0.200 | `False` | 0.552 | 0.942 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.45 | C_caps_only | 0.075 | `False` | 0.544 | 0.915 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.45 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.45 | C_full | 0.750 | `True` | 0.484 | 0.970 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.62 | C_caps_only | 0.062 | `False` | 0.538 | 0.911 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.62 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.62 | C_full | 0.750 | `True` | 0.484 | 0.968 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.82 | C_caps_only | 0.050 | `False` | 0.536 | 0.901 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.82 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.12;strength=0.82 | C_full | 0.688 | `True` | 0.488 | 0.968 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.45 | C_caps_only | 0.013 | `False` | 0.560 | 0.924 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.45 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.45 | C_full | 0.700 | `True` | 0.487 | 0.969 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.62 | C_caps_only | 0.050 | `False` | 0.552 | 0.923 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.62 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.62 | C_full | 0.713 | `True` | 0.488 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.82 | C_caps_only | 0.062 | `False` | 0.543 | 0.922 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.82 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.18;strength=0.82 | C_full | 0.588 | `False` | 0.492 | 0.968 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.45 | C_caps_only | 0.013 | `False` | 0.561 | 0.926 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.45 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.45 | C_full | 0.625 | `True` | 0.490 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.62 | C_caps_only | 0.025 | `False` | 0.559 | 0.924 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.62 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.62 | C_full | 0.637 | `True` | 0.489 | 0.969 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.82 | C_caps_only | 0.037 | `False` | 0.557 | 0.924 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.82 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.24;strength=0.82 | C_full | 0.600 | `False` | 0.493 | 0.969 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.45 | C_caps_only | 0.013 | `False` | 0.562 | 0.925 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.45 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.45 | C_full | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.62 | C_caps_only | 0.013 | `False` | 0.562 | 0.925 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.62 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.62 | C_full | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.82 | C_caps_only | 0.013 | `False` | 0.562 | 0.925 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.82 | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | cap_tightness | share=0.32;strength=0.82 | C_full | 0.637 | `True` | 0.490 | 0.967 |
| W4_scavenger_catastrophe | default | default | C_caps_only | 0.050 | `False` | 0.552 | 0.923 |
| W4_scavenger_catastrophe | default | default | C_dyn_only | 0.637 | `True` | 0.489 | 0.967 |
| W4_scavenger_catastrophe | default | default | C_full | 0.713 | `True` | 0.488 | 0.967 |
