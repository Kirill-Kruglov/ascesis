# Proposed Target Structure

This structure is proposed, not applied. It follows the current evidence better than a flat `experiments/` tree: executable harnesses stay under `experiments/`, research syntheses move under `research/`, and extracted packages move under `packages/`.

```text
ascesis/
  README.md
  LICENSE
  CONTRIBUTORS.md
  CITATION.cff

  research/
    ascesis_of_learning_grace/
    monograph_17/
    faithful_abstraction_v1/
    substrate_discovery_v1/
    door1_postmortem/

  packages/
    blind_arbiter/

  experiments/
    01_goodhart_bench/
    02_hedger_vs_incomplete/
    03_silence_vs_fabrication/
    04_admissible_set_core/
    05_reflective_stability_of_incompleteness/
    06_sugarscape_governor/
    07_empowerment_vs_corrigibility/
    08_blind_consequence_feeder_viability/
    13_evolvable_action_strategies/
    14_dsl_core/
    15_collapse_boundary/
    16_consequence_vs_feature/
    17_backbone_consequence/
    17A_backbone_consequence/
    17A2_semantic_perturbation_taxonomy/
    17C_interpretive_closure_test/
    17D_closure_metric_robustness/
    17E_latent_metric_geometry/
    17F_cross_substrate_latent_geometry/

    JB/
      18_0_shield_synthesis/
      18_1_shielded_training/
      JB0_E1_standard_cegar_boundary_assessment/

    BA/
      BA0_boundary_analysis/
      BA1_E1_monotonicity_breakers/
      BA2_E1_semantic_benefit_vs_structural_cost_map/
      BA3_E1_MB5_surrogate_replacement_test/
      BA4_layer_audit/

    FA/
      FA1_E1_false_safe_witness_taxonomy/
      FA2_E1_minimal_invariant_compression_test/
      FA2_5_E1_candidate_validation/
      T_C_monotonicity_of_faithful_justitia_abstraction/

  archive/
    deprecated_specs/
    old_outputs/
    binary_snapshots/
```

## Rationale

- `research/` should hold monographs, research programs, synthesis docs, and Substrate Discovery docs. Several of those files already self-identify with `research/...` headings.
- `experiments/` should hold executable experiment harnesses and their minimal evidence outputs.
- `packages/blind_arbiter/` matches the top-level README statement that blind arbiter is an extracted focused package rather than a sandbox experiment.
- `BA`, `FA`, and `JB` subtrees reduce namespace collisions between dotted spec directories and underscore implementation directories.
- `archive/old_outputs/` is for bulky reproducible raw outputs, not for reports that are cited as evidence.
