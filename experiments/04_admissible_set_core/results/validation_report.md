# Validation Report: 04 Admissible Set Core

## Measures
Can a bottom-up governor maintain a nonempty admissible set without scalar aggregation? Links: `field_check.md` nodes 12-14.

## Artifact Checks

| check | result | interpretation |
|---|---|---|
| collapse under clustered preferences | passed | Compares IID dispersed preferences to clustered structured disagreement. |
| cross-cutting cleavages | passed | Adds independent cleavage dimensions; mean empty rate 0.000 vs clustered 0.000 for N>=16,width>=0.45. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/admissible_set_size.svg`

## Verdict

valid result if interpreted as profile-dependent; clustered and cross-cutting profiles are included to avoid worst-case-only pessimism.
