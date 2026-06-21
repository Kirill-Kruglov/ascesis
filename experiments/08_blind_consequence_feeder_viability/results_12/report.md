# Experiment 12 Report: Causal Audit of Capture Dynamics

Final verdict: **C. Capture is controllable only by hidden-type oracle interventions.**

## Validation Checks

| check | result |
|---|---:|
| oracle_kill_hawks_reduces_capture | `True` |
| oracle_kill_hawks_below_0_20 | `True` |
| oracle_freeze_reduces_hawk_growth | `True` |
| type_blind_interventions_fire | `True` |
| intervention_costs_recorded | `True` |
| collateral_damage_recorded | `True` |
| capture_metric_varies_across_interventions | `True` |
| no_hidden_type_in_type_blind_observation | `True` |
| oracle_interventions_explicitly_labeled_non_blind | `True` |

## Required Questions

1. Is capture dynamically reachable at all? Yes by oracle: mean capture falls from `1.000` to `0.000` under `oracle_kill_hawks`.
2. Does hawk reproduction drive capture? Partly: oracle freeze lowers hawk reproduction from `494.53` to `0.00`, but does not generally clear the final capture threshold.
3. Does aid interception drive capture? In this substrate, removing interceptable aid in bad zones does not change capture probability; see zero delta rows and raw `aid_interception_volume`.
4. Does migration drive capture? Blocking outgoing migration from bad zones does not change capture probability in the tested worlds.
5. Does resource concentration drive capture? Resource caps and global density caps reduce some population/concentration metrics but do not change binary capture.
6. Does neighbor edge damage drive capture? Edge cuts reduce/record neighbor damage but do not change binary capture.
7. Largest type-blind delta-capture: `0.000`. No type-blind intervention produced a nonzero capture reduction under the tested ladder.
8. Was the largest delta real or starvation? There is no nonzero type-blind delta to interpret; oracle success is direct hidden-type removal, not starvation.
9. Does the current substrate provide enough non-type causal levers? Under this ladder, no: capture is reachable only through hidden-type oracle probes.
10. Before Experiment 13: change the substrate causal interface or capture threshold mechanics before adding another feeder policy.

## Oracle Probes

| world | intervention | capture | delta capture | hawk pop | delta hawk | adv share | welfare | collapse | events | oracle kill | oracle freeze |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FIXED_MI_DELAY | oracle_freeze_hawk_reproduction | 0.960 | -0.040 | 49.49 | -464.92 | 0.146 | 0.737 | 0.000 | 810.0 | 0.00 | 171.75 |
| FIXED_MI_DELAY | oracle_kill_hawks | 0.000 | -1.000 | 0.00 | -514.41 | 0.000 | 1.000 | 0.000 | 1620.0 | 56.59 | 0.00 |
| MIXED_CAPTURE_CATASTROPHE | oracle_freeze_hawk_reproduction | 1.000 | 0.000 | 59.65 | -452.02 | 0.182 | 0.741 | 0.000 | 810.0 | 0.00 | 212.53 |
| MIXED_CAPTURE_CATASTROPHE | oracle_kill_hawks | 0.000 | -1.000 | 0.00 | -511.68 | 0.000 | 1.000 | 0.000 | 1620.0 | 67.60 | 0.00 |
| PURE_CAPTURE | oracle_freeze_hawk_reproduction | 1.000 | 0.000 | 77.55 | -608.36 | 0.315 | 0.001 | 1.000 | 810.0 | 0.00 | 161.42 |
| PURE_CAPTURE | oracle_kill_hawks | 0.000 | -1.000 | 0.00 | -685.91 | 0.000 | 1.000 | 0.000 | 1620.0 | 85.62 | 0.00 |
| SCAVENGER_CATASTROPHE | oracle_freeze_hawk_reproduction | 1.000 | 0.000 | 59.66 | -452.00 | 0.225 | 0.738 | 0.000 | 810.0 | 0.00 | 209.87 |
| SCAVENGER_CATASTROPHE | oracle_kill_hawks | 0.000 | -1.000 | 0.00 | -511.66 | 0.000 | 1.000 | 0.000 | 1620.0 | 88.60 | 0.00 |

## Type-Blind Intervention Ranking

| world | intervention | capture | delta capture | adv share | hawk pop | dove pop | welfare | collapse | irrev frac | cost | collateral | events | aid intercepted | HHI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MIXED_CAPTURE_CATASTROPHE | combined_type_blind_maximal | 1.000 | 0.000 | 0.259 | 90.97 | 244.63 | 0.958 | 0.000 | 0.222 | 0.956 | 137.58 | 309.0 | 48.26 | 0.111 |
| MIXED_CAPTURE_CATASTROPHE | combined_type_blind_maximal | 1.000 | 0.000 | 0.252 | 82.58 | 230.20 | 0.845 | 0.000 | 0.222 | 0.820 | 138.65 | 397.5 | 52.64 | 0.111 |
| SCAVENGER_CATASTROPHE | combined_type_blind_maximal | 1.000 | 0.000 | 0.286 | 81.24 | 220.91 | 0.841 | 0.000 | 0.222 | 0.832 | 148.02 | 448.3 | 58.19 | 0.111 |
| PURE_CAPTURE | type_blind_no_interceptable_aid_bad_zones | 1.000 | 0.000 | 0.692 | 552.16 | 225.45 | 0.772 | 0.000 | 0.333 | 0.399 | 0.00 | 198.0 | 51.44 | 0.179 |
| PURE_CAPTURE | type_blind_no_interceptable_aid_bad_zones | 1.000 | 0.000 | 0.687 | 537.11 | 224.18 | 0.768 | 0.000 | 0.333 | 0.404 | 0.00 | 142.0 | 51.10 | 0.178 |
| MIXED_CAPTURE_CATASTROPHE | type_blind_edge_cut_bad_zones | 1.000 | 0.000 | 0.642 | 511.47 | 259.36 | 0.766 | 0.000 | 0.222 | 0.104 | 37.32 | 97.6 | 62.46 | 0.220 |
| MIXED_CAPTURE_CATASTROPHE | combined_type_blind_maximal | 1.000 | 0.000 | 0.269 | 92.55 | 235.91 | 0.765 | 0.000 | 0.222 | 0.688 | 175.53 | 352.3 | 53.09 | 0.112 |
| PURE_CAPTURE | type_blind_no_interceptable_aid_bad_zones | 1.000 | 0.000 | 0.711 | 578.00 | 215.26 | 0.764 | 0.000 | 0.333 | 0.454 | 0.00 | 273.6 | 49.06 | 0.188 |
| SCAVENGER_CATASTROPHE | type_blind_edge_cut_bad_zones | 1.000 | 0.000 | 0.651 | 511.49 | 259.88 | 0.764 | 0.000 | 0.222 | 0.085 | 13.06 | 82.0 | 68.73 | 0.217 |
| MIXED_CAPTURE_CATASTROPHE | combined_type_blind_maximal | 1.000 | 0.000 | 0.262 | 91.75 | 242.48 | 0.763 | 0.000 | 0.222 | 0.723 | 144.77 | 350.3 | 54.21 | 0.112 |
| MIXED_CAPTURE_CATASTROPHE | type_blind_resource_cap_bad_zones | 1.000 | 0.000 | 0.605 | 511.55 | 306.36 | 0.763 | 0.000 | 0.222 | 0.022 | 12.36 | 18.8 | 64.51 | 0.202 |
| MIXED_CAPTURE_CATASTROPHE | type_blind_resource_cap_bad_zones | 1.000 | 0.000 | 0.606 | 511.51 | 305.47 | 0.763 | 0.000 | 0.222 | 0.042 | 15.30 | 22.4 | 63.05 | 0.203 |
| MIXED_CAPTURE_CATASTROPHE | type_blind_resource_cap_bad_zones | 1.000 | 0.000 | 0.605 | 511.50 | 305.94 | 0.763 | 0.000 | 0.222 | 0.053 | 14.93 | 24.3 | 62.30 | 0.202 |
| MIXED_CAPTURE_CATASTROPHE | type_blind_resource_cap_bad_zones | 1.000 | 0.000 | 0.605 | 511.47 | 306.66 | 0.763 | 0.000 | 0.222 | 0.064 | 15.01 | 25.8 | 61.47 | 0.202 |
