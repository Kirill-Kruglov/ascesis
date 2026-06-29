# Boundary Analysis Index

| item | path | main report | final decision / assessment | result |
|---|---|---|---|---|
| BA0 transition semantics report | `experiments/BA/BA0_boundary_analysis/` | `experiments/BA/BA0_boundary_analysis/transition_semantics_report.md` | none found | Static transition-semantics extraction from Justitia; no new simulations. |
| BA1 monotonicity breakers | `experiments/BA/BA1_E1_monotonicity_breakers/` | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/final_report.md` | `experiments/BA/BA1_E1_monotonicity_breakers/outputs/final_decision.json` | `Case C / H2_supported`; clean single-mechanism ablations did not materially reduce false-safe error. |
| BA2 semantic benefit vs structural cost | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/` | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/final_report.md` | `experiments/BA/BA2_E1_semantic_benefit_vs_structural_cost_map/outputs/hypothesis_assessment.json` | `H_BA2_rejected`; at least one clean mechanism has high structural cost and low semantic benefit. |
| BA3 MB5 surrogate replacement | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/` | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/final_report.md` | `experiments/BA/BA3_E1_MB5_surrogate_replacement_test/outputs/hypothesis_assessment.json` | `MB5_functionally_split`; no full successful transition surrogate, but subfamily replacements exist. |
| BA4 layer audit | `experiments/BA/BA4_layer_audit/` | `experiments/BA/BA4_layer_audit/justitia_layer_audit.md` | `experiments/BA/BA4_layer_audit/SPEC_original.md` | `Layer_audit_complete`; separates dynamics, policy/control, observation, projection, and reporting layers. |
