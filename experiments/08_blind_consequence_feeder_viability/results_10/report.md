# Experiment 10 Report: Minimal Enforcement

Final verdict: **D. Result invalid due to failed validation.**

## Validation Checks

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

## Required Questions

1. What killed Experiment 09 policies? Capture under T1/T2/FIXED_MI_DELAY; Experiment 10 keeps this as the target failure mode.
2. Minimal enforcement threshold: none found under the viability criterion.
3. Threshold dependence: reported in raw summary across R, adversarial strength, and catastrophe worlds; no causal claim beyond this toy sweep.
4. Diversity: `consequence_plus_diversity` tests enforcement plus non-adversarial diversity; raw metrics distinguish non-adversarial and adversarial diversity.
5. Response-to-aid: included as comparator and as part of `consequence_plus_diversity`.
6. Viable region breadth: `0` non-trivial enforcement-viable cells out of `94` enforcement cells. Raw viability-only cells remain in `raw/summary.csv` and are not counted for A if they have no capture-world enforcement events/cost.
7. Most controlling assumption: delayed neighbor consequence is treated as reliable enough to trigger zone-level enforcement; if that signal is adversarially controlled, the mechanism should fail.
8. Current calibration failure: enforcement fires and costs resources, but no capture-relevant world gets capture below 1.0; pure-catastrophe raw viability is a control result, not an enforcement kernel.

## Best Enforcement Cells

| nontrivial viable | raw viable | world | policy | C | p | permanence | capture | strict zero capture | collapse | irrev frac | welfare | diversity | cost | false positive | events |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | PURE_CATASTROPHE | consequence_plus_diversity | 0.2 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.520 | 0.000 | 0.000 | 0.0 |
| 0 | 1 | PURE_CATASTROPHE | consequence_plus_diversity | 0.45 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.520 | 0.000 | 0.000 | 0.0 |
| 0 | 1 | PURE_CATASTROPHE | consequence_plus_diversity | 0.7 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.520 | 0.000 | 0.000 | 0.0 |
| 0 | 1 | PURE_CATASTROPHE | consequence_plus_diversity | 0.45 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.516 | 0.000 | 0.000 | 0.0 |
| 0 | 1 | PURE_CATASTROPHE | consequence_plus_diversity | 0.45 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.520 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_penalty | 0.2 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_penalty | 0.45 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_penalty | 0.7 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_quarantine | 0.2 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_quarantine | 0.45 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_quarantine | 0.7 | 0.0 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |
| 0 | 0 | PURE_CATASTROPHE | neighbor_audit_penalty | 0.2 | 0.35 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.440 | 0.000 | 0.000 | 0.0 |

## Capture-Relevant Enforcement Cells

These rows exclude pure-catastrophe controls. The validation failure is that all capture-relevant enforcement rows retain `capture=1.0`.

| world | policy | C | p | duration | R | adv | severity | migration | permanence | capture | welfare | diversity | cost | events |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| MIXED_CAPTURE_CATASTROPHE | neighbor_quarantine | 0.45 | 0.0 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.756 | 0.550 | 0.022 | 30.7 |
| MIXED_CAPTURE_CATASTROPHE | neighbor_audit_penalty | 0.45 | 0.1 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.755 | 0.554 | 0.022 | 1.8 |
| MIXED_CAPTURE_CATASTROPHE | neighbor_audit_penalty | 0.45 | 0.1 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.755 | 0.554 | 0.025 | 1.8 |
| MIXED_CAPTURE_CATASTROPHE | neighbor_audit_penalty | 0.45 | 0.1 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.755 | 0.554 | 0.027 | 1.8 |
| PURE_CAPTURE | neighbor_audit_penalty | 0.45 | 0.1 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.354 | 0.595 | 0.049 | 6.5 |
| MIXED_CAPTURE_CATASTROPHE | neighbor_audit_penalty | 0.2 | 0.35 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.755 | 0.554 | 0.053 | 6.7 |
| SCAVENGER_CATASTROPHE | neighbor_audit_penalty | 0.2 | 0.35 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.753 | 0.555 | 0.054 | 6.9 |
| PURE_CAPTURE | neighbor_audit_penalty | 0.45 | 0.1 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.354 | 0.595 | 0.057 | 6.5 |
| SCAVENGER_CATASTROPHE | neighbor_quarantine | 0.2 | 0.0 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.753 | 0.545 | 0.058 | 58.2 |
| SCAVENGER_CATASTROPHE | neighbor_quarantine | 0.45 | 0.0 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.753 | 0.545 | 0.064 | 58.2 |
| MIXED_CAPTURE_CATASTROPHE | neighbor_quarantine | 0.2 | 0.0 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.754 | 0.543 | 0.065 | 64.9 |
| PURE_CAPTURE | neighbor_audit_penalty | 0.45 | 0.1 | 4 | 3.50 | 0.70 | 0.55 | 0.22/0.08 | 0.000 | 1.000 | 0.354 | 0.595 | 0.066 | 6.5 |
