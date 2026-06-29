# Duplicate And Stale Candidates

No action was taken. These are candidates for a later pass only.

## Duplicate / Merge Candidates

| candidate A | candidate B / target | reason |
|---|---|---|
| `experiments/BA1.E1_monotonicity_breaker_ablation_map` | `experiments/BA1_E1_monotonicity_breakers` | Spec-only dotted directory vs implementation/output underscore directory. |
| `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map` | `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map` | Both contain outputs; underscore also has runner. Compare hashes/contents before merging. |
| `experiments/BA3.E1_MB5_Surrogate_Replacement_Test` | `experiments/BA3_E1_MB5_surrogate_replacement_test` | Spec-only dotted directory vs implementation/output underscore directory. |
| `experiments/FA1.E1_False-Safe_Witness_Taxonomy` | `experiments/FA1_E1_false_safe_witness_taxonomy` | Spec-only dotted directory vs implementation/output underscore directory. |
| `experiments/FA2.E1_Minimal_Invariant_Compression_Test` | `experiments/FA2_E1_minimal_invariant_compression_test` | Spec-only dotted directory vs implementation/output underscore directory. |
| `experiments/FA2.5.E1_Faithful_Candidate_Validation` | `experiments/FA2_5_E1_candidate_validation` | Spec-only dotted directory vs implementation/output underscore directory. |
| `experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment` | `experiments/JB0_E1_standard_cegar_boundary_assessment` | Spec-only dotted directory vs implementation/output underscore directory. |
| `experiments/monography_FA` | `research/faithful_abstraction_v1` | `monography` appears to be a typo/temporary location for FA monograph docs. |
| `experiments/monograph_17` | `research/monograph_17` | Monograph/review packet currently under experiments. |

## Generated / Stale Candidates

| path pattern | status | reason |
|---|---|---|
| `experiments/14_dsl_core/venv` | delete_candidate | local virtualenv; very large and reproducible from requirements/pyproject context |
| `**/__pycache__` | delete_candidate | Python bytecode cache, ignored by `.gitignore` |
| `**/.pytest_cache` | delete_candidate | pytest cache, reproducible and not evidence |
| `experiments/ascesis_17.zip` | delete_candidate or archive_candidate | binary archive likely duplicates monograph/experiment files; confirm before deletion |
| `experiments/*/outputs* and experiments/*/results* raw folders` | archive_candidate | preserve final reports/manifests as evidence; raw bulk can move to archive if reproducible |
| `experiments/14_dsl_core/worldcore/outputs/proofs` | archive_candidate | large generated proof dump; preserve sampled/final metrics in active tree, archive bulk if reproducible |
| `.claude/` | delete_candidate or keep local ignored | local assistant settings/lock; should not be committed |

## Evidence Outputs To Preserve

- Preserve `final_report.md`, `summary.md`, `final_decision.json`, `hypothesis_assessment.json`, `run_manifest.json`, and key CSV/PNG/SVG figures for experiments that support conclusions in monographs or bridge maps.
- Raw exhaustive outputs and proof dumps should be preserved only if they are expensive to regenerate or directly cited; otherwise move to `archive/old_outputs/` in a later approved pass.
- Do not treat old tracked `01-08` results as stale merely because they are old; README/status explicitly use them as the historical calibration trail.
