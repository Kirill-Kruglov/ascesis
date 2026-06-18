# Validation Report: 01 Goodhart Bench

## Measures
Calibration: proxy optimization should improve proxy reward while degrading true reward under pressure. Links: `field_check.md` node 11.

## Artifact Checks

| check | result | interpretation |
|---|---|---|
| Goodhart curve separation | passed | Agent true-reward curves are not identical. |
| quantilizer achieves non-trivial proxy gain while avoiding trap | passed | Quantilizer proxy gain over random must be positive, and its trap rate must stay below proxy-maximizer; otherwise it is either random or not avoiding the trap. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/true_reward_vs_pressure.svg`

## Verdict

valid result.
