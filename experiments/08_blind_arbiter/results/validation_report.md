# Validation Report: 08 Blind Type-B Arbiter

| check | result | interpretation |
|---|---|---|
| blind_arbiter | passed | The arbiter interface never receives hidden behavior_gene or true_x; runtime assertion present in `decide()`. |
| emergent_goodhart | passed | Signal mutation is driven by allocation history and lag/audit feedback, not by a hand-coded penalty. |
| floor_not_maximized | failed | Intervention magnitude inside the permanence floor is lower than outside it. |
| symmetric_comparison | passed | All regimes use the same seeds and the same R grid. |
| finite_values | passed | All reported numbers are finite. |
| calibration_gate | failed | C1'=False, C2'=True. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/permanence_survival.svg`, `results/corr_sa_over_time.svg`, `results/failure_mode_camouflage.svg`, `results/failure_mode_collective_hack.svg`, `results/failure_mode_collective_punishment.svg`

## Verdict

calibration failure: Amendment 2 gate did not close; not valid for H_boundary/H_regime.
unreachable predicate: C1'(b); no high-R regime reached mean true permanence >= 0.50, best observed high-R permanence was 0.100 (geometric).
