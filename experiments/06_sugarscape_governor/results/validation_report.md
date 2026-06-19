# Validation Report: 06 Sugarscape Governor

## Measures
Whether a corrected geometric hedger remains sufficient, or whether incomplete preference helps near an emergent reproduction floor in a Sugarscape-style ecology. Links: `experiments/02_hedger_vs_incomplete`, `questions.md` narrowed active spine.

## Artifact Checks

| check | result | interpretation |
|---|---|---|
| emergent floor from population dynamics | passed | No explicit floor penalty is present in governor objectives; demographic floor is computed after the run. |
| hedger correctly implemented | passed | Scalar probe choice: `balanced`. |
| seed noise visible | passed | Held-out distributions and survival bands are reported. |
| A/B identical environments | passed | Same seeds are replayed for each governor. |
| governor actions diverge | passed | Modal held-out allocation divergences: `[{"step": 50, "modal_allocations": {"arithmetic_mean": 0.8, "geometric_mean": 0.65, "incomplete_preference": 0.8}}, {"step": 90, "modal_allocations": {"arithmetic_mean": 0.5, "geometric_mean": 0.65, "incomplete_preference": 0.5}}]`. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`, `results/raw/population_by_step.csv`
- Human-readable: `results/report.md`, `results/population_survival.svg`

## Verdict

negative_or_inconclusive. Publication-grade status requires human review of the Sugarscape source choice and scarcity parameters.
