# Validation Report: Blind Arbiter

| check | result | interpretation |
|---|---|---|
| blind_arbiter | passed | The arbiter interface never receives hidden behavior_gene or true_x; runtime assertion present in `decide()`. |
| emergent_goodhart | passed | Signal mutation is driven by allocation history and lag/audit feedback, not by a hand-coded penalty. |
| floor_intervention (descriptive) | measured | Mean intervention inside floor=0.740, outside floor=0.488. Inside>=outside (yes) is the expected signature of active defense under Goodhart (SPEC Amendment 3); not a gate. |
| symmetric_comparison | passed | All regimes use the same seeds and the same R grid. |
| finite_values | passed | All reported numbers are finite. |
| calibration_gate | passed | C1'=True, C2'=True. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/audit_report.md`, `results/permanence_survival.svg`, `results/corr_sa_over_time.svg`, `results/failure_mode_camouflage.svg`, `results/failure_mode_collective_hack.svg`, `results/failure_mode_collective_punishment.svg`

## Verdict

valid result; boundary readable. Active defense of the floor is the studied regime (floor_not_maximized is descriptive, not a gate; see SPEC Amendment 3).
C1'/C2' passed; locked boundary and regime evaluation may proceed.
