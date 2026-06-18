# Validation Report: 02 Hedger vs Incomplete

## Measures
Where does geometric-mean optimization apply, and where is it undefined because no valid scalar exists? Links: `field_check.md` nodes 13, 15, and 16; `questions.md` narrowed active spine.

## Artifact Checks

| check | result | interpretation |
|---|---|---|
| finite_values | passed | Bounded additive scores replace the prior 1e17 axis explosion. |
| agent_divergence | passed | Held-out divergences: `[{"environment": "heldout_incommensurable_threshold", "geometric_mean": "extractive_growth", "incomplete_preference": "preserve_threshold", "valid_geometric_mean_available": false}, {"environment": "heldout_incommensurable_sacred_floor", "geometric_mean": "major_gain_violate_floor", "incomplete_preference": "modest_gain_preserve_floor", "valid_geometric_mean_available": false}]`. |
| non_scalarizable_check | passed | Incommensurable envs set `valid_geometric_mean_available=false`; hedger there is undefined, not defeated. |
| scalar_artifact_removed | passed | Corrected geometric hedger should remove the prior scalar-risk win by incomplete preferences. |

## Hedger Not Applicable

["heldout_incommensurable_threshold", "heldout_incommensurable_sacred_floor"]

## Sacred / Protected Values Legitimacy

Manual decision required: if sacred/protected values are accepted as real non-scalarizable structures, the incommensurable branch remains live. If the sacred floor is judged artificial, this test does not support the branch.

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/survival_by_environment.svg`

## Verdict

valid result. Publication-grade status: needs human review of non-scalarizable environment legitimacy before publication; scalar-risk artifact status is `passed`.
