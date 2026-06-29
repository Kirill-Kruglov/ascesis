# Post-Reorg Inventory

Generated after reorg passes 1-3. This file does not overwrite the original inventory files.

## Git Status Short

```text
 M README.md
D  blind_arbiter/README.md
D  blind_arbiter/SPEC.md
D  blind_arbiter/camouflage_audit/SPEC.md
D  blind_arbiter/camouflage_audit/results/audit_surface_best_gamma.svg
D  blind_arbiter/camouflage_audit/results/gamma_audit_off.svg
D  blind_arbiter/camouflage_audit/results/raw/per_seed.csv
D  blind_arbiter/camouflage_audit/results/raw/results.json
D  blind_arbiter/camouflage_audit/results/raw/surface.csv
D  blind_arbiter/camouflage_audit/results/report.md
D  blind_arbiter/camouflage_audit/results/run_manifest.json
D  blind_arbiter/camouflage_audit/results/validation_report.md
D  blind_arbiter/camouflage_audit/run.py
D  blind_arbiter/references.md
D  blind_arbiter/results/audit_report.md
D  blind_arbiter/results/corr_sa_over_time.svg
D  blind_arbiter/results/failure_mode_camouflage.svg
D  blind_arbiter/results/failure_mode_collective_hack.svg
D  blind_arbiter/results/failure_mode_collective_punishment.svg
D  blind_arbiter/results/permanence_survival.svg
D  blind_arbiter/results/raw/results.csv
D  blind_arbiter/results/raw/results.json
D  blind_arbiter/results/report.md
D  blind_arbiter/results/run_manifest.json
D  blind_arbiter/results/validation_report.md
D  blind_arbiter/run.py
D  blind_arbiter/strategic_camouflage/SPEC.md
D  blind_arbiter/strategic_camouflage/results/concealment_surface_strong_gamma.svg
D  blind_arbiter/strategic_camouflage/results/gamma_audit_off.svg
D  blind_arbiter/strategic_camouflage/results/permanence_surface_strong_gamma.svg
D  blind_arbiter/strategic_camouflage/results/raw/calibration_per_seed.csv
D  blind_arbiter/strategic_camouflage/results/raw/per_seed.csv
D  blind_arbiter/strategic_camouflage/results/raw/results.json
D  blind_arbiter/strategic_camouflage/results/raw/surface.csv
D  blind_arbiter/strategic_camouflage/results/report.md
D  blind_arbiter/strategic_camouflage/results/run_manifest.json
D  blind_arbiter/strategic_camouflage/results/validation_report.md
D  blind_arbiter/strategic_camouflage/run.py
 M experiments/README.md
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
?? experiments/FA/
?? experiments/INDEX.md
?? experiments/JB/
?? repo_reorg_inventory/
?? research/
```

## Top-Level Tree To Depth 3

`venv/` internals are intentionally collapsed in this tree view.

```text
.
  ascesis_of_learning_grace/
    archive/
      INDEX.md
    dialogs/
      dialog.part_1.md
      dialog.part_10.md
      dialog.part_11.md
      dialog.part_12.md
      dialog.part_13.md
      dialog.part_14.md
      dialog.part_15.md
      dialog.part_16.md
      dialog.part_17.md
      dialog.part_18.md
      dialog.part_19.md
      dialog.part_2.md
      dialog.part_20.md
      dialog.part_21.md
      dialog.part_22.md
      dialog.part_3.md
      dialog.part_4.md
      dialog.part_5.md
      dialog.part_6.md
      dialog.part_7.md
      dialog.part_8.md
      dialog.part_9.md
      field_check.md
      subject_index.md
    field_check.md
    glossary.md
    proposals.md
    questions.md
    references.md
    rejected_branches.md
    status.md
    structure.md
  experiments/
    01_goodhart_bench/
      results/
      README.md
      run.py
      SPEC.md
    02_hedger_vs_incomplete/
      results/
      README.md
      run.py
      SPEC.md
    03_silence_vs_fabrication/
      results/
      tools/
      README.md
      run.py
      SPEC.md
    04_admissible_set_core/
      results/
      README.md
      run.py
      SPEC.md
    05_reflective_stability_of_incompleteness/
      results/
      README.md
      run.py
      SPEC.md
    06_sugarscape_governor/
      results/
      README.md
      run.py
      SPEC.md
    07_empowerment_vs_corrigibility/
      results/
      CODEX_PROMPT.md
      README.md
      run.py
      SPEC.md
    08_blind_consequence_feeder_viability/
      config/
      results/
      results_09/
      results_10/
      results_11/
      results_12/
      README.md
      run.py
      run09.py
      run10.py
      run11.py
      run12.py
      seeds.json
      SPEC_IMPLEMENTED.md
      SPEC_IMPLEMENTED_09.md
      SPEC_IMPLEMENTED_10.md
      SPEC_IMPLEMENTED_11.md
      SPEC_IMPLEMENTED_12.md
    13_evolvable_action_strategies/
      results/
      results_14/
      results_15/
      results_16/
      run.py
      run14.py
      run15.py
      run16.py
      SPEC_EXP16.md
      SPEC_EXP16_1_PATCH.md
      SPEC_IMPLEMENTED.md
      SPEC_IMPLEMENTED_14.md
      SPEC_IMPLEMENTED_15.md
    14_dsl_core/
      venv/
      worldcore/
      EXPERIMENTS.md
      SPEC-v0.4.md
      SPEC-v0.42.md
    15_collapse_boundary/
      outputs/
      outputs_15_0_1/
      outputs_15_1/
      outputs_15_2/
      scripts/
      src/
      tests/
      claude_code_report_15_0_1.md
      claude_code_task_15_0_1_measurement_repair.md
      claude_code_task_15_2_enumeration_to_exhaustion.md
      codex_experiment_task_15_1.md
      pyproject.toml
      README.md
      requirements.txt
      SPEC_v0.1.md
    16_consequence_vs_feature/
      outputs_16/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17_backbone_consequence/
      outputs_17/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17A.2_Semantic_Perturbation_Taxonomy/
      outputs_17A2/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17A_backbone_consequence/
      outputs_17A/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17C_interpretive_closure_test/
      outputs_17C/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17D_closure_metric_robustness/
      outputs_17D/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17E_latent_metric_geometry/
      outputs_17E/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    17F_cross_substrate_latent_geometry/
      outputs_17F/
      scripts/
      src/
      tests/
      GPT_Codex_Spec_Experiment.md
      pyproject.toml
      README.md
      requirements.txt
    BA/
      BA0_boundary_analysis/
      BA1_E1_monotonicity_breakers/
      BA2_E1_semantic_benefit_vs_structural_cost_map/
      BA3_E1_MB5_surrogate_replacement_test/
      BA4_layer_audit/
      INDEX.md
    FA/
      FA1_E1_false_safe_witness_taxonomy/
      FA2_5_E1_candidate_validation/
      FA2_E1_minimal_invariant_compression_test/
      T_C_Monotonicity_of_Faithful_Justitia_Abstraction/
      INDEX.md
    JB/
      18_0_shield_synthesis/
      18_1_shielded_training/
      JB0_E1_standard_cegar_boundary_assessment/
      INDEX.md
    INDEX.md
    README.md
    validation_summary.md
  repo_reorg_inventory/
    artifact_map.csv
    artifact_map.md
    duplicate_and_stale_candidates.md
    git_state.md
    post_reorg_inventory.md
    proposed_target_structure.md
    reorg_pass_1_report.md
    reorg_pass_2_report.md
    reorg_pass_3_report.md
    reorg_plan.md
  research/
    door1_postmortem/
      Door1_Extracted_Knowledge_v1.md
    faithful_abstraction_v1/
      00_program.md
      01_empirical_basis.md
      02_fa_theory.md
      BRIDGE_MAP_18_1_TO_FA2.md
      REVIEW_PACKET.md
    monograph_17/
      ASCESIS_Appendix_A_Research_Ledger_v2.md
      ASCESIS_Experimental_Chronicle_v2.md
      ASCESIS_PROJECT_INDEX_v2.md
      ASCESIS_Research_Methodology_v2.md
      ASCESIS_Research_Ontology_Part_I_—_Foundations_&_Research_Ontology_Version_2.0_Post-17F.md
      ASCESIS_Research_Program_v2.md
      ASCESIS_Scientific_Context_v2.md
      GPT_eval17F.md
      GPT_summary.md
      Memo_v1.3_17.md
    playbook/
      00_monograph_kill_gates.md
      01_playbook_extraction_plan.md
      02_source_artifact_map.md
      README.md
    substrate_discovery_v1/
      00_research_axioms.md
      00_search_frame.md
      01_research_question.md
      02_candidate_axes.md
      03_Computability_of_Environment.md
      04_Derivability.md
      04_triage_framework.md
      05_candidate_triage_matrix.md
      05_Interaction_and_Identifiability.md
      06_Necessary_Properties.md
      07_Search_Strategy.md
      08_Candidate_Evaluation_Framework.md
      09_Open_Problems.md
      2026-06-29_research_session.md
      project_names.md
    README.md
  .gitignore
  CITATION.cff
  CONTRIBUTORS.md
  LICENSE
  README.md
```

## Remaining Untracked Roots

```text
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
experiments/BA
experiments/FA
experiments/INDEX.md
experiments/JB
repo_reorg_inventory
research
```

## Remaining Ignored / Generated Roots Summary

```text
ascesis_of_learning_grace/dialogs/ (ignored research source material)
experiments/14_dsl_core/venv/ (ignored virtualenv internals)
experiments/*/outputs*/ and experiments/*/results*/ (generated evidence artifacts preserved by instruction)
```

## Paths Still Needing Human Decision

- `experiments/14_dsl_core/venv/`: local virtualenv preserved by instruction; decide in a later explicit approval pass.
- `experiments/ascesis_17.zip`: absent in the final state; user reported removing it during pass 3, and this pass did not search for or restore it.
- `repo_reorg_inventory/artifact_map.md` and `repo_reorg_inventory/artifact_map.csv`: stale relative to post-reorg paths; preserve as pre-reorg evidence or regenerate into new filenames.
- `repo_reorg_inventory/git_state.md`: stale snapshot from pre-reorg state; preserve as historical inventory evidence.

## Commit Recommendation

The repo is ready to commit the reorganization work after human review of the staged tracked deletion of `blind_arbiter/` and the large untracked experiment/research roots. Recommended commit shape:

1. Commit reorg pass reports and navigation indexes.
2. Commit removal of extracted `blind_arbiter/` with README updates.
3. Commit or explicitly stage the large untracked experiment/research roots according to project policy.

Do not remove `venv/`, `outputs/`, `results/`, or `raw/` in the commit-prep pass unless separately approved.
