# Experiment 10 Validation Report

| check | result |
|---|---:|
| hidden_type_absent_from_observation | `True` |
| enforcement_has_cost | `True` |
| delayed_consequence_required | `True` |
| feature_proxy_fails_T1 | `True` |
| always_cut_fails_T2 | `True` |
| always_aid_fails_T2 | `True` |
| monoculture_fails_T3 | `True` |
| not_starving_all_zones | `True` |
| capture_not_one_for_all_enforcement | `False` |
| pure_catastrophe_false_positive_test_run | `True` |

Calibration note: `capture_not_one_for_all_enforcement` is evaluated only on capture-relevant worlds (`PURE_CAPTURE`, `MIXED_CAPTURE_CATASTROPHE`, `SCAVENGER_CATASTROPHE`).

Final verdict: **D. Result invalid due to failed validation.**
