# Safe Reorganization Pass 1 Report

Date: 2026-06-29

Scope: safe reorganization based on `repo_reorg_inventory/`.

No experiment outputs, raw result folders, caches, venvs, or `blind_arbiter/` were pruned or moved.

## 1. Commands / Actions Performed

Created target directories:

```sh
mkdir -p research
mkdir -p research/monograph_17
mkdir -p research/faithful_abstraction_v1
mkdir -p research/substrate_discovery_v1
mkdir -p research/door1_postmortem
mkdir -p experiments/BA
mkdir -p experiments/FA
mkdir -p experiments/JB
```

All moved source paths were untracked, so `mv` was used. No tracked source path in this pass required `git mv`.

After each move, the destination path was checked with `test -e`.

## 2. Moved Paths

### Research Docs

- `experiments/Door1_Extracted_Knowledge_v1.md` -> `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md`
- `experiments/BRIDGE_MAP_18_1_TO_FA2.md` -> `research/faithful_abstraction_v1/BRIDGE_MAP_18_1_TO_FA2.md`
- `experiments/Memo_v1.3 _17.md` -> `research/monograph_17/Memo_v1.3_17.md`
- `experiments/monograph_17/*` -> `research/monograph_17/`
- `experiments/monography_FA/*` -> `research/faithful_abstraction_v1/`
- `experiments/Substrate_Discovery_v1/*` -> `research/substrate_discovery_v1/`

### Justitia Boundary

- `experiments/18_0_shield_synthesis/` -> `experiments/JB/18_0_shield_synthesis/`
- `experiments/18_1_shielded_training/` -> `experiments/JB/18_1_shielded_training/`
- `experiments/JB0_E1_standard_cegar_boundary_assessment/` -> `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/`
- `experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment/JB0.E1_Standard_CEGAR_Boundary_Assessment.md` -> `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/SPEC_original.md`

### Boundary Analysis

- `experiments/BA0_boundary_analysis/` -> `experiments/BA/BA0_boundary_analysis/`
- `experiments/BA1_E1_monotonicity_breakers/` -> `experiments/BA/BA1_E1_monotonicity_breakers/`
- `experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/` -> `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/`
- `experiments/BA3_E1_MB5_surrogate_replacement_test/` -> `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/`
- `experiments/BA4_layer_audit/` -> `experiments/BA/BA4_layer_audit/`
- `experiments/BA1.E1_monotonicity_breaker_ablation_map/BA1.E1_monotonicity_breaker_ablation_map.md` -> `experiments/BA/BA1_E1_monotonicity_breakers/SPEC_original.md`
- `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/BA2.E1_Semantic_benefit_vs_structural_cost_map.md` -> `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/SPEC_original.md`
- `experiments/BA3.E1_MB5_Surrogate_Replacement_Test/BA3.E1_MB5_Surrogate_Replacement_Test.md` -> `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/SPEC_original.md`
- `experiments/BA4.0_Layered_Abstraction_Discipline/BA4.0_Layered_Abstraction_Discipline.md` -> `experiments/BA/BA4_layer_audit/SPEC_original.md`

### Faithful Abstraction

- `experiments/FA1_E1_false_safe_witness_taxonomy/` -> `experiments/FA/FA1_E1_false_safe_witness_taxonomy/`
- `experiments/FA2_E1_minimal_invariant_compression_test/` -> `experiments/FA/FA2_E1_minimal_invariant_compression_test/`
- `experiments/FA2_5_E1_candidate_validation/` -> `experiments/FA/FA2_5_E1_candidate_validation/`
- `experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction/` -> `experiments/FA/T_C_Monotonicity_of_Faithful_Justitia_Abstraction/`
- `experiments/FA1.E1_False-Safe_Witness_Taxonomy/FA1.E1_False-Safe_Witness_Taxonomy.md` -> `experiments/FA/FA1_E1_false_safe_witness_taxonomy/SPEC_original.md`
- `experiments/FA2.E1_Minimal_Invariant_Compression_Test/FA2.E1_Minimal_Invariant_Compression_Test.md` -> `experiments/FA/FA2_E1_minimal_invariant_compression_test/SPEC_original.md`
- `experiments/FA2.5.E1_Faithful_Candidate_Validation/FA2.5.E1_Faithful_Candidate_Validation.md` -> `experiments/FA/FA2_5_E1_candidate_validation/SPEC_original.md`

## 3. Skipped Paths

- `blind_arbiter/` was left untouched as required.
- `ascesis_of_learning_grace/` was left untouched as required.
- `experiments/01_goodhart_bench/` through `experiments/17F_cross_substrate_latent_geometry/` were left untouched, except for explicit BA/FA/JB moves listed above.
- `experiments/14_dsl_core/` was left untouched as required.
- `experiments/ascesis_17.zip` was left untouched as required.
- `venv/`, `.pytest_cache/`, `__pycache__/`, `raw/`, `outputs/`, and `results/` were not pruned.
- `README.md` and `experiments/README.md` were not edited; `rg` found no obvious references in those two files to the moved paths.

## 4. Duplicate Handling

`experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/` was compared with `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/` using recursive `diff -qr`.

Result: the dotted outputs are identical to canonical outputs.

Action: the dotted `outputs/` directory was preserved in place and not deleted. The dotted BA2 directory remains non-empty only because it contains duplicate outputs.

## 5. Empty Directories Removed

Only empty directories left after moving their markdown contents were removed:

- `experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment`
- `experiments/BA1.E1_monotonicity_breaker_ablation_map`
- `experiments/BA3.E1_MB5_Surrogate_Replacement_Test`
- `experiments/BA4.0_Layered_Abstraction_Discipline`
- `experiments/FA1.E1_False-Safe_Witness_Taxonomy`
- `experiments/FA2.E1_Minimal_Invariant_Compression_Test`
- `experiments/FA2.5.E1_Faithful_Candidate_Validation`
- `experiments/monograph_17`
- `experiments/monography_FA`
- `experiments/Substrate_Discovery_v1`

No content-bearing file was deleted.

## 6. Files That Need Human Review

- `experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs/`: duplicate output tree preserved in place; human should decide whether to archive, keep, or remove in a later pass.
- `experiments/ascesis_17.zip`: untouched binary archive; human should confirm whether it duplicates repository content before any later archive/delete action.
- `repo_reorg_inventory/artifact_map.*`: now partially stale because paths were moved after inventory generation; consider regenerating inventory in a later pass.
- `research/faithful_abstraction_v1/`: contains both FA monograph docs and `BRIDGE_MAP_18_1_TO_FA2.md`; this is reasonable, but final naming should be human-approved.

## 7. Git Status After Reorg

```text
?? experiments/14_dsl_core/
?? experiments/15_collapse_boundary/
?? experiments/16_consequence_vs_feature/
?? experiments/17A.2_Semantic_Perturbation_Taxonomy/
?? experiments/17A_backbone_consequence/
?? experiments/17C_interpretive_closure_test/
?? experiments/17D_closure_metric_robustness/
?? experiments/17E_latent_metric_geometry/
?? experiments/17F_cross_substrate_latent_geometry/
?? experiments/17_backbone_consequence/
?? experiments/BA/
?? experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/
?? experiments/FA/
?? experiments/JB/
?? experiments/ascesis_17.zip
?? repo_reorg_inventory/
?? research/
```

## 8. Recommended Next Pass

1. Review and commit this safe reorganization pass.
2. Decide whether to archive or keep the duplicate BA2 dotted `outputs/` tree.
3. Regenerate `repo_reorg_inventory/artifact_map.*` after the new layout is accepted.
4. Consider updating `.gitignore` for `venv/`, `.pytest_cache/`, local assistant state, and generated bytecode only after deciding what should be committed first.
5. In a separate confirmed pass, consider moving `blind_arbiter/` to `packages/blind_arbiter/` and updating README links together.

Safe reorganization pass complete; no content-bearing files were deleted.
