# Git State

Snapshot was collected before writing `repo_reorg_inventory/`; the inventory directory itself is therefore not part of the pre-existing artifact classification.

## Git Summary

- tracked files: 255
- untracked files/directories from `git status --short`: 37
- untracked files from `git ls-files --others --exclude-standard`: 8604
- ignored files from `git ls-files --ignored --others --exclude-standard`: 18259
- modified tracked paths: 0

## `git status --short`

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
?? experiments/18_0_shield_synthesis/
?? experiments/18_1_shielded_training/
?? experiments/BA0_boundary_analysis/
?? experiments/BA1.E1_monotonicity_breaker_ablation_map/
?? experiments/BA1_E1_monotonicity_breakers/
?? experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/
?? experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/
?? experiments/BA3.E1_MB5_Surrogate_Replacement_Test/
?? experiments/BA3_E1_MB5_surrogate_replacement_test/
?? experiments/BA4.0_Layered_Abstraction_Discipline/
?? experiments/BA4_layer_audit/
?? experiments/BRIDGE_MAP_18_1_TO_FA2.md
?? experiments/Door1_Extracted_Knowledge_v1.md
?? experiments/FA1.E1_False-Safe_Witness_Taxonomy/
?? experiments/FA1_E1_false_safe_witness_taxonomy/
?? experiments/FA2.5.E1_Faithful_Candidate_Validation/
?? experiments/FA2.E1_Minimal_Invariant_Compression_Test/
?? experiments/FA2_5_E1_candidate_validation/
?? experiments/FA2_E1_minimal_invariant_compression_test/
?? experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment/
?? experiments/JB0_E1_standard_cegar_boundary_assessment/
?? "experiments/Memo_v1.3 _17.md"
?? experiments/Substrate_Discovery_v1/
?? experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction/
?? experiments/ascesis_17.zip
?? experiments/monograph_17/
?? experiments/monography_FA/
```

## `git status --short --ignored` summary

Full ignored output is very large because of `venv` and cache trees. Key status lines are summarized here.

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
?? experiments/18_0_shield_synthesis/
?? experiments/18_1_shielded_training/
?? experiments/BA0_boundary_analysis/
?? experiments/BA1.E1_monotonicity_breaker_ablation_map/
?? experiments/BA1_E1_monotonicity_breakers/
?? experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/
?? experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/
?? experiments/BA3.E1_MB5_Surrogate_Replacement_Test/
?? experiments/BA3_E1_MB5_surrogate_replacement_test/
?? experiments/BA4.0_Layered_Abstraction_Discipline/
?? experiments/BA4_layer_audit/
?? experiments/BRIDGE_MAP_18_1_TO_FA2.md
?? experiments/Door1_Extracted_Knowledge_v1.md
?? experiments/FA1.E1_False-Safe_Witness_Taxonomy/
?? experiments/FA1_E1_false_safe_witness_taxonomy/
?? experiments/FA2.5.E1_Faithful_Candidate_Validation/
?? experiments/FA2.E1_Minimal_Invariant_Compression_Test/
?? experiments/FA2_5_E1_candidate_validation/
?? experiments/FA2_E1_minimal_invariant_compression_test/
?? experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment/
?? experiments/JB0_E1_standard_cegar_boundary_assessment/
?? "experiments/Memo_v1.3 _17.md"
?? experiments/Substrate_Discovery_v1/
?? experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction/
?? experiments/ascesis_17.zip
?? experiments/monograph_17/
?? experiments/monography_FA/
!! .claude/
!! ascesis_of_learning_grace/dialogs/
!! blind_arbiter/__pycache__/
!! blind_arbiter/camouflage_audit/__pycache__/
!! experiments/01_goodhart_bench/__pycache__/
!! experiments/02_hedger_vs_incomplete/__pycache__/
!! experiments/03_silence_vs_fabrication/__pycache__/
!! experiments/03_silence_vs_fabrication/tools/__pycache__/
!! experiments/04_admissible_set_core/__pycache__/
!! experiments/05_reflective_stability_of_incompleteness/__pycache__/
!! experiments/06_sugarscape_governor/__pycache__/
!! experiments/07_empowerment_vs_corrigibility/__pycache__/
!! experiments/14_dsl_core/.pytest_cache/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/PIL/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/_code/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/_io/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/_py/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/assertion/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/config/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/_pytest/mark/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/contourpy/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/contourpy/util/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/cycler/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/dateutil/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/dateutil/parser/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/dateutil/zoneinfo/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/cffLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/colorLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/config/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/cu2qu/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/designspaceLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/diff/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/encodings/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/feaLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/merge/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/misc/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/misc/filesystem/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/misc/plistlib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/mtiLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/otlLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/otlLib/optimize/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/pens/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/qu2cu/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/subset/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/svgLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/svgLib/path/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/t1Lib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/ttLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/ttLib/tables/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/ufoLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/unicodedata/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/varLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/varLib/avar/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/varLib/instancer/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/fontTools/voltLib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/iniconfig/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/externals/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/externals/cloudpickle/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/externals/loky/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/externals/loky/backend/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/test/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/joblib/test/data/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/kiwisolver/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/_api/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/axes/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/backends/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/backends/qt_editor/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/projections/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/sphinxext/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/style/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/testing/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/testing/jpl_units/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/matplotlib/tri/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/mpl_toolkits/axes_grid1/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/mpl_toolkits/axes_grid1/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/mpl_toolkits/axisartist/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/mpl_toolkits/axisartist/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/mpl_toolkits/mplot3d/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/mpl_toolkits/mplot3d/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_arrow/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_compliant/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_dask/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_duckdb/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_ibis/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_interchange/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_pandas_like/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_polars/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_spark_like/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/_sql/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/stable/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/stable/v1/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/stable/v2/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/testing/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/narwhals/testing/asserts/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/approximation/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/approximation/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/assortativity/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/assortativity/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/bipartite/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/centrality/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/centrality/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/coloring/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/coloring/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/community/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/community/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/components/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/components/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/connectivity/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/connectivity/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/flow/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/flow/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/isomorphism/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/isomorphism/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/link_analysis/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/link_analysis/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/minors/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/minors/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/operators/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/operators/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/shortest_paths/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/shortest_paths/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/traversal/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/traversal/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/tree/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/algorithms/tree/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/classes/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/classes/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/drawing/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/drawing/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/generators/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/generators/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/linalg/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/linalg/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/readwrite/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/readwrite/json_graph/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/readwrite/json_graph/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/readwrite/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/utils/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/networkx/utils/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_core/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_core/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_core/tests/examples/cython/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_core/tests/examples/limited_api/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_pyinstaller/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_pyinstaller/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_typing/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/_utils/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/char/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/core/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/ctypeslib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/doc/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/f2py/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/f2py/_backends/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/f2py/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/fft/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/fft/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/lib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/lib/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/linalg/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/linalg/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/ma/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/ma/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/matrixlib/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/matrixlib/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/polynomial/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/polynomial/tests/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/random/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/random/_examples/cffi/__pycache__/
!! experiments/14_dsl_core/venv/lib/python3.12/site-packages/numpy/random/_examples/numba/__pycache__/
... truncated in report; 554 additional ignored/cache lines
```

## `git ls-files`

```text
.gitignore
CITATION.cff
CONTRIBUTORS.md
LICENSE
README.md
ascesis_of_learning_grace/archive/INDEX.md
ascesis_of_learning_grace/field_check.md
ascesis_of_learning_grace/glossary.md
ascesis_of_learning_grace/proposals.md
ascesis_of_learning_grace/questions.md
ascesis_of_learning_grace/references.md
ascesis_of_learning_grace/rejected_branches.md
ascesis_of_learning_grace/status.md
ascesis_of_learning_grace/structure.md
blind_arbiter/README.md
blind_arbiter/SPEC.md
blind_arbiter/camouflage_audit/SPEC.md
blind_arbiter/camouflage_audit/results/audit_surface_best_gamma.svg
blind_arbiter/camouflage_audit/results/gamma_audit_off.svg
blind_arbiter/camouflage_audit/results/raw/per_seed.csv
blind_arbiter/camouflage_audit/results/raw/results.json
blind_arbiter/camouflage_audit/results/raw/surface.csv
blind_arbiter/camouflage_audit/results/report.md
blind_arbiter/camouflage_audit/results/run_manifest.json
blind_arbiter/camouflage_audit/results/validation_report.md
blind_arbiter/camouflage_audit/run.py
blind_arbiter/references.md
blind_arbiter/results/audit_report.md
blind_arbiter/results/corr_sa_over_time.svg
blind_arbiter/results/failure_mode_camouflage.svg
blind_arbiter/results/failure_mode_collective_hack.svg
blind_arbiter/results/failure_mode_collective_punishment.svg
blind_arbiter/results/permanence_survival.svg
blind_arbiter/results/raw/results.csv
blind_arbiter/results/raw/results.json
blind_arbiter/results/report.md
blind_arbiter/results/run_manifest.json
blind_arbiter/results/validation_report.md
blind_arbiter/run.py
blind_arbiter/strategic_camouflage/SPEC.md
blind_arbiter/strategic_camouflage/results/concealment_surface_strong_gamma.svg
blind_arbiter/strategic_camouflage/results/gamma_audit_off.svg
blind_arbiter/strategic_camouflage/results/permanence_surface_strong_gamma.svg
blind_arbiter/strategic_camouflage/results/raw/calibration_per_seed.csv
blind_arbiter/strategic_camouflage/results/raw/per_seed.csv
blind_arbiter/strategic_camouflage/results/raw/results.json
blind_arbiter/strategic_camouflage/results/raw/surface.csv
blind_arbiter/strategic_camouflage/results/report.md
blind_arbiter/strategic_camouflage/results/run_manifest.json
blind_arbiter/strategic_camouflage/results/validation_report.md
blind_arbiter/strategic_camouflage/run.py
experiments/01_goodhart_bench/README.md
experiments/01_goodhart_bench/SPEC.md
experiments/01_goodhart_bench/results/raw/results.csv
experiments/01_goodhart_bench/results/raw/results.json
experiments/01_goodhart_bench/results/report.md
experiments/01_goodhart_bench/results/run_manifest.json
experiments/01_goodhart_bench/results/true_reward_vs_pressure.svg
experiments/01_goodhart_bench/results/validation_report.md
experiments/01_goodhart_bench/run.py
experiments/02_hedger_vs_incomplete/README.md
experiments/02_hedger_vs_incomplete/SPEC.md
experiments/02_hedger_vs_incomplete/results/raw/results.csv
experiments/02_hedger_vs_incomplete/results/raw/results.json
experiments/02_hedger_vs_incomplete/results/report.md
experiments/02_hedger_vs_incomplete/results/run_manifest.json
experiments/02_hedger_vs_incomplete/results/survival_by_environment.svg
experiments/02_hedger_vs_incomplete/results/validation_report.md
experiments/02_hedger_vs_incomplete/run.py
experiments/03_silence_vs_fabrication/README.md
experiments/03_silence_vs_fabrication/SPEC.md
experiments/03_silence_vs_fabrication/results/fabrication_rates.svg
experiments/03_silence_vs_fabrication/results/model_selection/selection_report.md
experiments/03_silence_vs_fabrication/results/model_selection/selection_rows.csv
experiments/03_silence_vs_fabrication/results/model_selection/selection_summary.csv
experiments/03_silence_vs_fabrication/results/model_selection/selection_summary.json
experiments/03_silence_vs_fabrication/results/raw/results.csv
experiments/03_silence_vs_fabrication/results/raw/results.json
experiments/03_silence_vs_fabrication/results/report.md
experiments/03_silence_vs_fabrication/results/run_manifest.json
experiments/03_silence_vs_fabrication/results/validation_report.md
experiments/03_silence_vs_fabrication/run.py
experiments/03_silence_vs_fabrication/tools/llama_server_backend.py
experiments/03_silence_vs_fabrication/tools/reclassify_existing.py
experiments/03_silence_vs_fabrication/tools/select_llama_model.py
experiments/04_admissible_set_core/README.md
experiments/04_admissible_set_core/SPEC.md
experiments/04_admissible_set_core/results/admissible_set_size.svg
experiments/04_admissible_set_core/results/raw/results.csv
experiments/04_admissible_set_core/results/raw/results.json
experiments/04_admissible_set_core/results/report.md
experiments/04_admissible_set_core/results/run_manifest.json
experiments/04_admissible_set_core/results/validation_report.md
experiments/04_admissible_set_core/run.py
experiments/05_reflective_stability_of_incompleteness/README.md
experiments/05_reflective_stability_of_incompleteness/SPEC.md
experiments/05_reflective_stability_of_incompleteness/results/partial_stability_heatmap.svg
experiments/05_reflective_stability_of_incompleteness/results/raw/results.csv
experiments/05_reflective_stability_of_incompleteness/results/raw/results.json
experiments/05_reflective_stability_of_incompleteness/results/report.md
experiments/05_reflective_stability_of_incompleteness/results/run_manifest.json
experiments/05_reflective_stability_of_incompleteness/results/validation_report.md
experiments/05_reflective_stability_of_incompleteness/run.py
experiments/06_sugarscape_governor/README.md
experiments/06_sugarscape_governor/SPEC.md
experiments/06_sugarscape_governor/results/population_survival.svg
experiments/06_sugarscape_governor/results/raw/population_by_step.csv
experiments/06_sugarscape_governor/results/raw/results.csv
experiments/06_sugarscape_governor/results/raw/results.json
experiments/06_sugarscape_governor/results/report.md
experiments/06_sugarscape_governor/results/run_manifest.json
experiments/06_sugarscape_governor/results/validation_report.md
experiments/06_sugarscape_governor/run.py
experiments/07_empowerment_vs_corrigibility/CODEX_PROMPT.md
experiments/07_empowerment_vs_corrigibility/README.md
experiments/07_empowerment_vs_corrigibility/SPEC.md
experiments/07_empowerment_vs_corrigibility/results/empowerment_vs_corrigibility.svg
experiments/07_empowerment_vs_corrigibility/results/raw/results.csv
experiments/07_empowerment_vs_corrigibility/results/raw/results.json
experiments/07_empowerment_vs_corrigibility/results/report.md
experiments/07_empowerment_vs_corrigibility/results/run_manifest.json
experiments/07_empowerment_vs_corrigibility/results/validation_report.md
experiments/07_empowerment_vs_corrigibility/run.py
experiments/08_blind_consequence_feeder_viability/README.md
experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED.md
experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_09.md
experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_10.md
experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_11.md
experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_12.md
experiments/08_blind_consequence_feeder_viability/config/default_config.json
experiments/08_blind_consequence_feeder_viability/results/MI_vs_permanence.svg
experiments/08_blind_consequence_feeder_viability/results/collapse_probability_vs_R.svg
experiments/08_blind_consequence_feeder_viability/results/delay_vs_permanence_fixed_MI.svg
experiments/08_blind_consequence_feeder_viability/results/diversity_floor_vs_shock_survival.svg
experiments/08_blind_consequence_feeder_viability/results/heatmap_adversarial_strength_delay.svg
experiments/08_blind_consequence_feeder_viability/results/heatmap_catastrophe_severity_policy.svg
experiments/08_blind_consequence_feeder_viability/results/permanence_vs_R.svg
experiments/08_blind_consequence_feeder_viability/results/raw/runs.csv
experiments/08_blind_consequence_feeder_viability/results/raw/summary.csv
experiments/08_blind_consequence_feeder_viability/results/raw/viability_cells.csv
experiments/08_blind_consequence_feeder_viability/results/report.md
experiments/08_blind_consequence_feeder_viability/results/run_manifest.json
experiments/08_blind_consequence_feeder_viability/results/scavenger_exploitation_vs_aid_policy.svg
experiments/08_blind_consequence_feeder_viability/results/validation_report.md
experiments/08_blind_consequence_feeder_viability/results/viability_kernel_map.svg
experiments/08_blind_consequence_feeder_viability/results_09/consequence_vs_feature_permanence.svg
experiments/08_blind_consequence_feeder_viability/results_09/diversity_floor_vs_shock_survival.svg
experiments/08_blind_consequence_feeder_viability/results_09/fixed_MI_delay_R_plot.svg
experiments/08_blind_consequence_feeder_viability/results_09/irreversible_failures_vs_R.svg
experiments/08_blind_consequence_feeder_viability/results_09/neighbor_vs_self_consequence_performance.svg
experiments/08_blind_consequence_feeder_viability/results_09/raw/runs.csv
experiments/08_blind_consequence_feeder_viability/results_09/raw/summary.csv
experiments/08_blind_consequence_feeder_viability/results_09/report.md
experiments/08_blind_consequence_feeder_viability/results_09/run_manifest.json
experiments/08_blind_consequence_feeder_viability/results_09/trivial_policy_survival_T1_proxy_trap.svg
experiments/08_blind_consequence_feeder_viability/results_09/trivial_policy_survival_T2_sag_ambiguity_trap.svg
experiments/08_blind_consequence_feeder_viability/results_09/trivial_policy_survival_T3_monoculture_trap.svg
experiments/08_blind_consequence_feeder_viability/results_09/validation_report.md
experiments/08_blind_consequence_feeder_viability/results_10/capture_by_enforcement.svg
experiments/08_blind_consequence_feeder_viability/results_10/cost_share_by_policy.svg
experiments/08_blind_consequence_feeder_viability/results_10/false_positive_pure_catastrophe.svg
experiments/08_blind_consequence_feeder_viability/results_10/raw/runs.csv
experiments/08_blind_consequence_feeder_viability/results_10/raw/summary.csv
experiments/08_blind_consequence_feeder_viability/results_10/raw/viable_cells.csv
experiments/08_blind_consequence_feeder_viability/results_10/report.md
experiments/08_blind_consequence_feeder_viability/results_10/run_manifest.json
experiments/08_blind_consequence_feeder_viability/results_10/validation_report.md
experiments/08_blind_consequence_feeder_viability/results_10/viability_by_enforcement.svg
experiments/08_blind_consequence_feeder_viability/results_11/capture_by_action_channel.svg
experiments/08_blind_consequence_feeder_viability/results_11/cost_by_action_channel.svg
experiments/08_blind_consequence_feeder_viability/results_11/raw/channel_ranking.csv
experiments/08_blind_consequence_feeder_viability/results_11/raw/runs.csv
experiments/08_blind_consequence_feeder_viability/results_11/raw/summary.csv
experiments/08_blind_consequence_feeder_viability/results_11/raw/viable_cells.csv
experiments/08_blind_consequence_feeder_viability/results_11/report.md
experiments/08_blind_consequence_feeder_viability/results_11/resource_hhi_by_action_channel.svg
experiments/08_blind_consequence_feeder_viability/results_11/run_manifest.json
experiments/08_blind_consequence_feeder_viability/results_11/validation_report.md
experiments/08_blind_consequence_feeder_viability/results_12/capture_by_intervention.svg
experiments/08_blind_consequence_feeder_viability/results_12/delta_capture_by_intervention.svg
experiments/08_blind_consequence_feeder_viability/results_12/hawk_population_by_intervention.svg
experiments/08_blind_consequence_feeder_viability/results_12/raw/runs.csv
experiments/08_blind_consequence_feeder_viability/results_12/raw/summary.csv
experiments/08_blind_consequence_feeder_viability/results_12/report.md
experiments/08_blind_consequence_feeder_viability/results_12/run_manifest.json
experiments/08_blind_consequence_feeder_viability/results_12/validation_report.md
experiments/08_blind_consequence_feeder_viability/run.py
experiments/08_blind_consequence_feeder_viability/run09.py
experiments/08_blind_consequence_feeder_viability/run10.py
experiments/08_blind_consequence_feeder_viability/run11.py
experiments/08_blind_consequence_feeder_viability/run12.py
experiments/08_blind_consequence_feeder_viability/seeds.json
experiments/13_evolvable_action_strategies/SPEC_EXP16.md
experiments/13_evolvable_action_strategies/SPEC_EXP16_1_PATCH.md
experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED.md
experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_14.md
experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_15.md
experiments/13_evolvable_action_strategies/results/audit_delta_exploit_mass.svg
experiments/13_evolvable_action_strategies/results/raw/runs.csv
experiments/13_evolvable_action_strategies/results/raw/summary.csv
experiments/13_evolvable_action_strategies/results/raw/viable_cells.csv
experiments/13_evolvable_action_strategies/results/report.md
experiments/13_evolvable_action_strategies/results/run_manifest.json
experiments/13_evolvable_action_strategies/results/validation_report.md
experiments/13_evolvable_action_strategies/results/w2_capture_by_policy.svg
experiments/13_evolvable_action_strategies/results/w2_exploit_mass_by_policy.svg
experiments/13_evolvable_action_strategies/results_14/perturbation_pass_rate.svg
experiments/13_evolvable_action_strategies/results_14/raw/cell_classification.csv
experiments/13_evolvable_action_strategies/results_14/raw/runs.csv
experiments/13_evolvable_action_strategies/results_14/raw/seed_robustness.csv
experiments/13_evolvable_action_strategies/results_14/raw/summary.csv
experiments/13_evolvable_action_strategies/results_14/raw/w2_boundary_viable.csv
experiments/13_evolvable_action_strategies/results_14/report.md
experiments/13_evolvable_action_strategies/results_14/run_manifest.json
experiments/13_evolvable_action_strategies/results_14/seed_permanence_ci_lower.svg
experiments/13_evolvable_action_strategies/results_14/validation_report.md
experiments/13_evolvable_action_strategies/results_14/w6_action_ablation_permanence.svg
experiments/13_evolvable_action_strategies/results_15/best_permanence_by_family.svg
experiments/13_evolvable_action_strategies/results_15/classification_best_capture.svg
experiments/13_evolvable_action_strategies/results_15/part_a_best_permanence.svg
experiments/13_evolvable_action_strategies/results_15/raw/runs.csv
experiments/13_evolvable_action_strategies/results_15/raw/summary.csv
experiments/13_evolvable_action_strategies/results_15/raw/world_classification.csv
experiments/13_evolvable_action_strategies/results_15/report.md
experiments/13_evolvable_action_strategies/results_15/run_manifest.json
experiments/13_evolvable_action_strategies/results_15/validation_report.md
experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_action_channel_cost_scale_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_adversarial_gaps.svg
experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_adversarial_pressure_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W3_catastrophe_ambiguity_mutation_rate_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_action_channel_cost_scale_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_adversarial_gaps.svg
experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_adversarial_pressure_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W4_scavenger_catastrophe_mutation_rate_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_action_channel_cost_scale_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_adversarial_gaps.svg
experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_adversarial_pressure_permanence.svg
experiments/13_evolvable_action_strategies/results_16/W6_mutation_corridor_mutation_rate_permanence.svg
experiments/13_evolvable_action_strategies/results_16/boundary_atlas.md
experiments/13_evolvable_action_strategies/results_16/boundary_summary.svg
experiments/13_evolvable_action_strategies/results_16/raw/boundary.csv
experiments/13_evolvable_action_strategies/results_16/raw/cg_ablation.csv
experiments/13_evolvable_action_strategies/results_16/raw/decoupling.csv
experiments/13_evolvable_action_strategies/results_16/raw/marginal.csv
experiments/13_evolvable_action_strategies/results_16/raw/runs.csv
experiments/13_evolvable_action_strategies/results_16/raw/sensitivity.csv
experiments/13_evolvable_action_strategies/results_16/raw/summary.csv
experiments/13_evolvable_action_strategies/results_16/run_manifest.json
experiments/13_evolvable_action_strategies/results_16/sensitivity_report.md
experiments/13_evolvable_action_strategies/run.py
experiments/13_evolvable_action_strategies/run14.py
experiments/13_evolvable_action_strategies/run15.py
experiments/13_evolvable_action_strategies/run16.py
experiments/README.md
experiments/validation_summary.md
```

## `git ls-files --others --exclude-standard` top-level summary

```text
"experiments/monograph_17
experiments/14_dsl_core
experiments/15_collapse_boundary
experiments/16_consequence_vs_feature
experiments/17A.2_Semantic_Perturbation_Taxonomy
experiments/17A_backbone_consequence
experiments/17C_interpretive_closure_test
experiments/17D_closure_metric_robustness
experiments/17E_latent_metric_geometry
experiments/17F_cross_substrate_latent_geometry
experiments/17_backbone_consequence
experiments/18_0_shield_synthesis
experiments/18_1_shielded_training
experiments/BA0_boundary_analysis
experiments/BA1.E1_monotonicity_breaker_ablation_map
experiments/BA1_E1_monotonicity_breakers
experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map
experiments/BA2_E1_semantic_benefit_vs_structural_cost_map
experiments/BA3.E1_MB5_Surrogate_Replacement_Test
experiments/BA3_E1_MB5_surrogate_replacement_test
experiments/BA4.0_Layered_Abstraction_Discipline
experiments/BA4_layer_audit
experiments/BRIDGE_MAP_18_1_TO_FA2.md
experiments/Door1_Extracted_Knowledge_v1.md
experiments/FA1.E1_False-Safe_Witness_Taxonomy
experiments/FA1_E1_false_safe_witness_taxonomy
experiments/FA2.5.E1_Faithful_Candidate_Validation
experiments/FA2.E1_Minimal_Invariant_Compression_Test
experiments/FA2_5_E1_candidate_validation
experiments/FA2_E1_minimal_invariant_compression_test
experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment
experiments/JB0_E1_standard_cegar_boundary_assessment
experiments/Memo_v1.3 _17.md
experiments/Substrate_Discovery_v1
experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction
experiments/ascesis_17.zip
experiments/monograph_17
experiments/monography_FA
```

## `find . -maxdepth 3 -type f | sort`

```text
./.claude/scheduled_tasks.lock
./.claude/settings.local.json
./.gitignore
./CITATION.cff
./CONTRIBUTORS.md
./LICENSE
./README.md
./ascesis_of_learning_grace/archive/INDEX.md
./ascesis_of_learning_grace/dialogs/dialog.part_1.md
./ascesis_of_learning_grace/dialogs/dialog.part_10.md
./ascesis_of_learning_grace/dialogs/dialog.part_11.md
./ascesis_of_learning_grace/dialogs/dialog.part_12.md
./ascesis_of_learning_grace/dialogs/dialog.part_13.md
./ascesis_of_learning_grace/dialogs/dialog.part_14.md
./ascesis_of_learning_grace/dialogs/dialog.part_15.md
./ascesis_of_learning_grace/dialogs/dialog.part_16.md
./ascesis_of_learning_grace/dialogs/dialog.part_17.md
./ascesis_of_learning_grace/dialogs/dialog.part_18.md
./ascesis_of_learning_grace/dialogs/dialog.part_19.md
./ascesis_of_learning_grace/dialogs/dialog.part_2.md
./ascesis_of_learning_grace/dialogs/dialog.part_20.md
./ascesis_of_learning_grace/dialogs/dialog.part_21.md
./ascesis_of_learning_grace/dialogs/dialog.part_22.md
./ascesis_of_learning_grace/dialogs/dialog.part_3.md
./ascesis_of_learning_grace/dialogs/dialog.part_4.md
./ascesis_of_learning_grace/dialogs/dialog.part_5.md
./ascesis_of_learning_grace/dialogs/dialog.part_6.md
./ascesis_of_learning_grace/dialogs/dialog.part_7.md
./ascesis_of_learning_grace/dialogs/dialog.part_8.md
./ascesis_of_learning_grace/dialogs/dialog.part_9.md
./ascesis_of_learning_grace/dialogs/field_check.md
./ascesis_of_learning_grace/dialogs/subject_index.md
./ascesis_of_learning_grace/field_check.md
./ascesis_of_learning_grace/glossary.md
./ascesis_of_learning_grace/proposals.md
./ascesis_of_learning_grace/questions.md
./ascesis_of_learning_grace/references.md
./ascesis_of_learning_grace/rejected_branches.md
./ascesis_of_learning_grace/status.md
./ascesis_of_learning_grace/structure.md
./blind_arbiter/README.md
./blind_arbiter/SPEC.md
./blind_arbiter/__pycache__/run.cpython-312.pyc
./blind_arbiter/camouflage_audit/SPEC.md
./blind_arbiter/camouflage_audit/run.py
./blind_arbiter/references.md
./blind_arbiter/results/audit_report.md
./blind_arbiter/results/corr_sa_over_time.svg
./blind_arbiter/results/failure_mode_camouflage.svg
./blind_arbiter/results/failure_mode_collective_hack.svg
./blind_arbiter/results/failure_mode_collective_punishment.svg
./blind_arbiter/results/permanence_survival.svg
./blind_arbiter/results/report.md
./blind_arbiter/results/run_manifest.json
./blind_arbiter/results/validation_report.md
./blind_arbiter/run.py
./blind_arbiter/strategic_camouflage/SPEC.md
./blind_arbiter/strategic_camouflage/run.py
./experiments/01_goodhart_bench/README.md
./experiments/01_goodhart_bench/SPEC.md
./experiments/01_goodhart_bench/run.py
./experiments/02_hedger_vs_incomplete/README.md
./experiments/02_hedger_vs_incomplete/SPEC.md
./experiments/02_hedger_vs_incomplete/run.py
./experiments/03_silence_vs_fabrication/README.md
./experiments/03_silence_vs_fabrication/SPEC.md
./experiments/03_silence_vs_fabrication/run.py
./experiments/04_admissible_set_core/README.md
./experiments/04_admissible_set_core/SPEC.md
./experiments/04_admissible_set_core/run.py
./experiments/05_reflective_stability_of_incompleteness/README.md
./experiments/05_reflective_stability_of_incompleteness/SPEC.md
./experiments/05_reflective_stability_of_incompleteness/run.py
./experiments/06_sugarscape_governor/README.md
./experiments/06_sugarscape_governor/SPEC.md
./experiments/06_sugarscape_governor/run.py
./experiments/07_empowerment_vs_corrigibility/CODEX_PROMPT.md
./experiments/07_empowerment_vs_corrigibility/README.md
./experiments/07_empowerment_vs_corrigibility/SPEC.md
./experiments/07_empowerment_vs_corrigibility/run.py
./experiments/08_blind_consequence_feeder_viability/README.md
./experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED.md
./experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_09.md
./experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_10.md
./experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_11.md
./experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_12.md
./experiments/08_blind_consequence_feeder_viability/run.py
./experiments/08_blind_consequence_feeder_viability/run09.py
./experiments/08_blind_consequence_feeder_viability/run10.py
./experiments/08_blind_consequence_feeder_viability/run11.py
./experiments/08_blind_consequence_feeder_viability/run12.py
./experiments/08_blind_consequence_feeder_viability/seeds.json
./experiments/13_evolvable_action_strategies/SPEC_EXP16.md
./experiments/13_evolvable_action_strategies/SPEC_EXP16_1_PATCH.md
./experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED.md
./experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_14.md
./experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED_15.md
./experiments/13_evolvable_action_strategies/run.py
./experiments/13_evolvable_action_strategies/run14.py
./experiments/13_evolvable_action_strategies/run15.py
./experiments/13_evolvable_action_strategies/run16.py
./experiments/14_dsl_core/EXPERIMENTS.md
./experiments/14_dsl_core/SPEC-v0.4.md
./experiments/14_dsl_core/SPEC-v0.42.md
./experiments/15_collapse_boundary/README.md
./experiments/15_collapse_boundary/SPEC_v0.1.md
./experiments/15_collapse_boundary/claude_code_report_15_0_1.md
./experiments/15_collapse_boundary/claude_code_task_15_0_1_measurement_repair.md
./experiments/15_collapse_boundary/claude_code_task_15_2_enumeration_to_exhaustion.md
./experiments/15_collapse_boundary/codex_experiment_task_15_1.md
./experiments/15_collapse_boundary/pyproject.toml
./experiments/15_collapse_boundary/requirements.txt
./experiments/16_consequence_vs_feature/GPT_Codex_Spec_Experiment.md
./experiments/16_consequence_vs_feature/README.md
./experiments/16_consequence_vs_feature/pyproject.toml
./experiments/16_consequence_vs_feature/requirements.txt
./experiments/17A.2_Semantic_Perturbation_Taxonomy/GPT_Codex_Spec_Experiment.md
./experiments/17A.2_Semantic_Perturbation_Taxonomy/README.md
./experiments/17A.2_Semantic_Perturbation_Taxonomy/pyproject.toml
./experiments/17A.2_Semantic_Perturbation_Taxonomy/requirements.txt
./experiments/17A_backbone_consequence/GPT_Codex_Spec_Experiment.md
./experiments/17A_backbone_consequence/README.md
./experiments/17A_backbone_consequence/pyproject.toml
./experiments/17A_backbone_consequence/requirements.txt
./experiments/17C_interpretive_closure_test/GPT_Codex_Spec_Experiment.md
./experiments/17C_interpretive_closure_test/README.md
./experiments/17C_interpretive_closure_test/pyproject.toml
./experiments/17C_interpretive_closure_test/requirements.txt
./experiments/17D_closure_metric_robustness/GPT_Codex_Spec_Experiment.md
./experiments/17D_closure_metric_robustness/README.md
./experiments/17D_closure_metric_robustness/pyproject.toml
./experiments/17D_closure_metric_robustness/requirements.txt
./experiments/17E_latent_metric_geometry/GPT_Codex_Spec_Experiment.md
./experiments/17E_latent_metric_geometry/README.md
./experiments/17E_latent_metric_geometry/pyproject.toml
./experiments/17E_latent_metric_geometry/requirements.txt
./experiments/17F_cross_substrate_latent_geometry/GPT_Codex_Spec_Experiment.md
./experiments/17F_cross_substrate_latent_geometry/README.md
./experiments/17F_cross_substrate_latent_geometry/pyproject.toml
./experiments/17F_cross_substrate_latent_geometry/requirements.txt
./experiments/17_backbone_consequence/GPT_Codex_Spec_Experiment.md
./experiments/17_backbone_consequence/README.md
./experiments/17_backbone_consequence/pyproject.toml
./experiments/17_backbone_consequence/requirements.txt
./experiments/18_0_shield_synthesis/README.md
./experiments/18_0_shield_synthesis/claude_code_task_18_0_shield_synthesis.md
./experiments/18_1_shielded_training/README.md
./experiments/18_1_shielded_training/claude_code_task_18_1_shielded_training.md
./experiments/BA0_boundary_analysis/transition_semantics_report.md
./experiments/BA1.E1_monotonicity_breaker_ablation_map/BA1.E1_monotonicity_breaker_ablation_map.md
./experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/BA2.E1_Semantic_benefit_vs_structural_cost_map.md
./experiments/BA3.E1_MB5_Surrogate_Replacement_Test/BA3.E1_MB5_Surrogate_Replacement_Test.md
./experiments/BA4.0_Layered_Abstraction_Discipline/BA4.0_Layered_Abstraction_Discipline.md
./experiments/BA4_layer_audit/function_audit.csv
./experiments/BA4_layer_audit/justitia_layer_audit.md
./experiments/BA4_layer_audit/layer_audit.csv
./experiments/BRIDGE_MAP_18_1_TO_FA2.md
./experiments/Door1_Extracted_Knowledge_v1.md
./experiments/FA1.E1_False-Safe_Witness_Taxonomy/FA1.E1_False-Safe_Witness_Taxonomy.md
./experiments/FA2.5.E1_Faithful_Candidate_Validation/FA2.5.E1_Faithful_Candidate_Validation.md
./experiments/FA2.E1_Minimal_Invariant_Compression_Test/FA2.E1_Minimal_Invariant_Compression_Test.md
./experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment/JB0.E1_Standard_CEGAR_Boundary_Assessment.md
./experiments/Memo_v1.3 _17.md
./experiments/README.md
./experiments/Substrate_Discovery_v1/00_research_axioms.md
./experiments/Substrate_Discovery_v1/00_search_frame.md
./experiments/Substrate_Discovery_v1/01_research_question.md
./experiments/Substrate_Discovery_v1/02_candidate_axes.md
./experiments/Substrate_Discovery_v1/03_Computability_of_Environment.md
./experiments/Substrate_Discovery_v1/04_Derivability.md
./experiments/Substrate_Discovery_v1/04_triage_framework.md
./experiments/Substrate_Discovery_v1/05_Interaction_and_Identifiability.md
./experiments/Substrate_Discovery_v1/05_candidate_triage_matrix.md
./experiments/Substrate_Discovery_v1/06_Necessary_Properties.md
./experiments/Substrate_Discovery_v1/07_Search_Strategy.md
./experiments/Substrate_Discovery_v1/08_Candidate_Evaluation_Framework.md
./experiments/Substrate_Discovery_v1/09_Open_Problems.md
./experiments/Substrate_Discovery_v1/2026-06-29_research_session.md
./experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction/T-C_Monotonicity_of_Faithful_Justitia_Abstraction.md
./experiments/ascesis_17.zip
./experiments/monograph_17/ASCESIS_Appendix_A_Research_Ledger_v2.md
./experiments/monograph_17/ASCESIS_Experimental_Chronicle_v2.md
./experiments/monograph_17/ASCESIS_PROJECT_INDEX_v2.md
./experiments/monograph_17/ASCESIS_Research_Methodology_v2.md
./experiments/monograph_17/ASCESIS_Research_Ontology_Part_I_—_Foundations_&_Research_Ontology_Version_2.0_Post-17F.md
./experiments/monograph_17/ASCESIS_Research_Program_v2.md
./experiments/monograph_17/ASCESIS_Scientific_Context_v2.md
./experiments/monograph_17/GPT_eval17F.md
./experiments/monograph_17/GPT_summary.md
./experiments/monography_FA/00_program.md
./experiments/monography_FA/01_empirical_basis.md
./experiments/monography_FA/02_fa_theory.md
./experiments/monography_FA/REVIEW_PACKET.md
./experiments/validation_summary.md
```

## `find . -maxdepth 3 -type d | sort`

```text
.
./.claude
./ascesis_of_learning_grace
./ascesis_of_learning_grace/archive
./ascesis_of_learning_grace/dialogs
./blind_arbiter
./blind_arbiter/__pycache__
./blind_arbiter/camouflage_audit
./blind_arbiter/camouflage_audit/__pycache__
./blind_arbiter/camouflage_audit/results
./blind_arbiter/results
./blind_arbiter/results/raw
./blind_arbiter/strategic_camouflage
./blind_arbiter/strategic_camouflage/results
./experiments
./experiments/01_goodhart_bench
./experiments/01_goodhart_bench/__pycache__
./experiments/01_goodhart_bench/results
./experiments/02_hedger_vs_incomplete
./experiments/02_hedger_vs_incomplete/__pycache__
./experiments/02_hedger_vs_incomplete/results
./experiments/03_silence_vs_fabrication
./experiments/03_silence_vs_fabrication/__pycache__
./experiments/03_silence_vs_fabrication/results
./experiments/03_silence_vs_fabrication/tools
./experiments/04_admissible_set_core
./experiments/04_admissible_set_core/__pycache__
./experiments/04_admissible_set_core/results
./experiments/05_reflective_stability_of_incompleteness
./experiments/05_reflective_stability_of_incompleteness/__pycache__
./experiments/05_reflective_stability_of_incompleteness/results
./experiments/06_sugarscape_governor
./experiments/06_sugarscape_governor/__pycache__
./experiments/06_sugarscape_governor/results
./experiments/07_empowerment_vs_corrigibility
./experiments/07_empowerment_vs_corrigibility/__pycache__
./experiments/07_empowerment_vs_corrigibility/results
./experiments/08_blind_consequence_feeder_viability
./experiments/08_blind_consequence_feeder_viability/config
./experiments/08_blind_consequence_feeder_viability/results
./experiments/08_blind_consequence_feeder_viability/results_09
./experiments/08_blind_consequence_feeder_viability/results_10
./experiments/08_blind_consequence_feeder_viability/results_11
./experiments/08_blind_consequence_feeder_viability/results_12
./experiments/13_evolvable_action_strategies
./experiments/13_evolvable_action_strategies/results
./experiments/13_evolvable_action_strategies/results_14
./experiments/13_evolvable_action_strategies/results_15
./experiments/13_evolvable_action_strategies/results_16
./experiments/14_dsl_core
./experiments/14_dsl_core/.pytest_cache
./experiments/14_dsl_core/venv
./experiments/14_dsl_core/worldcore
./experiments/15_collapse_boundary
./experiments/15_collapse_boundary/.pytest_cache
./experiments/15_collapse_boundary/outputs
./experiments/15_collapse_boundary/outputs_15_0_1
./experiments/15_collapse_boundary/outputs_15_1
./experiments/15_collapse_boundary/outputs_15_2
./experiments/15_collapse_boundary/scripts
./experiments/15_collapse_boundary/src
./experiments/15_collapse_boundary/tests
./experiments/16_consequence_vs_feature
./experiments/16_consequence_vs_feature/.pytest_cache
./experiments/16_consequence_vs_feature/outputs_16
./experiments/16_consequence_vs_feature/scripts
./experiments/16_consequence_vs_feature/src
./experiments/16_consequence_vs_feature/tests
./experiments/17A.2_Semantic_Perturbation_Taxonomy
./experiments/17A.2_Semantic_Perturbation_Taxonomy/.pytest_cache
./experiments/17A.2_Semantic_Perturbation_Taxonomy/outputs_17A2
./experiments/17A.2_Semantic_Perturbation_Taxonomy/scripts
./experiments/17A.2_Semantic_Perturbation_Taxonomy/src
./experiments/17A.2_Semantic_Perturbation_Taxonomy/tests
./experiments/17A_backbone_consequence
./experiments/17A_backbone_consequence/.pytest_cache
./experiments/17A_backbone_consequence/outputs_17A
./experiments/17A_backbone_consequence/scripts
./experiments/17A_backbone_consequence/src
./experiments/17A_backbone_consequence/tests
./experiments/17C_interpretive_closure_test
./experiments/17C_interpretive_closure_test/.pytest_cache
./experiments/17C_interpretive_closure_test/outputs_17C
./experiments/17C_interpretive_closure_test/scripts
./experiments/17C_interpretive_closure_test/src
./experiments/17C_interpretive_closure_test/tests
./experiments/17D_closure_metric_robustness
./experiments/17D_closure_metric_robustness/.pytest_cache
./experiments/17D_closure_metric_robustness/outputs_17D
./experiments/17D_closure_metric_robustness/scripts
./experiments/17D_closure_metric_robustness/src
./experiments/17D_closure_metric_robustness/tests
./experiments/17E_latent_metric_geometry
./experiments/17E_latent_metric_geometry/.pytest_cache
./experiments/17E_latent_metric_geometry/outputs_17E
./experiments/17E_latent_metric_geometry/scripts
./experiments/17E_latent_metric_geometry/src
./experiments/17E_latent_metric_geometry/tests
./experiments/17F_cross_substrate_latent_geometry
./experiments/17F_cross_substrate_latent_geometry/.pytest_cache
./experiments/17F_cross_substrate_latent_geometry/outputs_17F
./experiments/17F_cross_substrate_latent_geometry/scripts
./experiments/17F_cross_substrate_latent_geometry/src
./experiments/17F_cross_substrate_latent_geometry/tests
./experiments/17_backbone_consequence
./experiments/17_backbone_consequence/.pytest_cache
./experiments/17_backbone_consequence/outputs_17
./experiments/17_backbone_consequence/scripts
./experiments/17_backbone_consequence/src
./experiments/17_backbone_consequence/tests
./experiments/18_0_shield_synthesis
./experiments/18_0_shield_synthesis/.pytest_cache
./experiments/18_0_shield_synthesis/outputs_18_0
./experiments/18_0_shield_synthesis/scripts
./experiments/18_0_shield_synthesis/src
./experiments/18_0_shield_synthesis/tests
./experiments/18_1_shielded_training
./experiments/18_1_shielded_training/.pytest_cache
./experiments/18_1_shielded_training/outputs_18_1
./experiments/18_1_shielded_training/scripts
./experiments/18_1_shielded_training/src
./experiments/18_1_shielded_training/tests
./experiments/BA0_boundary_analysis
./experiments/BA1.E1_monotonicity_breaker_ablation_map
./experiments/BA1_E1_monotonicity_breakers
./experiments/BA1_E1_monotonicity_breakers/outputs
./experiments/BA1_E1_monotonicity_breakers/scripts
./experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map
./experiments/BA2.E1_Semantic_benefit_vs_structural_cost_map/outputs
./experiments/BA2_E1_semantic_benefit_vs_structural_cost_map
./experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs
./experiments/BA2_E1_semantic_benefit_vs_structural_cost_map/scripts
./experiments/BA3.E1_MB5_Surrogate_Replacement_Test
./experiments/BA3_E1_MB5_surrogate_replacement_test
./experiments/BA3_E1_MB5_surrogate_replacement_test/outputs
./experiments/BA3_E1_MB5_surrogate_replacement_test/scripts
./experiments/BA4.0_Layered_Abstraction_Discipline
./experiments/BA4_layer_audit
./experiments/FA1.E1_False-Safe_Witness_Taxonomy
./experiments/FA1_E1_false_safe_witness_taxonomy
./experiments/FA1_E1_false_safe_witness_taxonomy/outputs
./experiments/FA1_E1_false_safe_witness_taxonomy/scripts
./experiments/FA2.5.E1_Faithful_Candidate_Validation
./experiments/FA2.E1_Minimal_Invariant_Compression_Test
./experiments/FA2_5_E1_candidate_validation
./experiments/FA2_5_E1_candidate_validation/outputs
./experiments/FA2_5_E1_candidate_validation/scripts
./experiments/FA2_E1_minimal_invariant_compression_test
./experiments/FA2_E1_minimal_invariant_compression_test/outputs
./experiments/FA2_E1_minimal_invariant_compression_test/scripts
./experiments/JB0.E1_Standard_CEGAR_Boundary_Assessment
./experiments/JB0_E1_standard_cegar_boundary_assessment
./experiments/JB0_E1_standard_cegar_boundary_assessment/outputs
./experiments/JB0_E1_standard_cegar_boundary_assessment/scripts
./experiments/Substrate_Discovery_v1
./experiments/T-C_Monotonicity_of_Faithful_Justitia_Abstraction
./experiments/monograph_17
./experiments/monography_FA
```
