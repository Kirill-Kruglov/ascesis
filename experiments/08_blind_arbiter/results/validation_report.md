# Validation Report: 08 Blind Type-B Arbiter

| check | result | interpretation |
|---|---|---|
| blind_arbiter | passed | The arbiter interface never receives hidden a_g; runtime assertion present in `decide()`. |
| emergent_goodhart | passed | Signal mutation is driven by allocation history and noise, not a penalty term. |
| floor_not_maximized | passed | Intervention magnitude inside the permanence floor is lower than outside it. |
| symmetric_comparison | passed | All regimes use the same seeds and the same R grid. |
| finite_values | passed | All reported numbers are finite. |
| calibration_gate | failed | C1=False, C2=False. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/permanence_survival.svg`, `results/corr_sa_over_time.svg`, `results/failure_mode_camouflage.svg`, `results/failure_mode_collective_hack.svg`, `results/failure_mode_collective_punishment.svg`

## Verdict

calibration gate failed; stand not yet measuring the question.
