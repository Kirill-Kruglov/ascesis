# Experiment 17E - Latent Metric Geometry

## Decision

Classification: `Multi_axis_supported`

One axis reconstructs the successful metric cluster, but perturbation sensitivity requires additional latent axes.

## Key Numbers

- PC1 F1 explained variance: `0.721998293170383`
- M1/M3/M5 reconstruction R2 with k=1: `0.9844277730935765`
- M1/M3/M5 reconstruction R2 with k=2: `0.9969379194314314`
- PC1 variance explained by controls: `0.6963947274868871`
- Functional-core AUC latent1: `0.9928286045991502`
- Functional-core AUC latent2: `0.9993036655903477`
- Functional-core AUC controls: `0.690433630852173`
- Class-B survival AUC latent1: `0.5023683295671824`
- Class-B survival AUC latent2: `0.7315655186114076`
- Class-B survival AUC latent3: `0.768968364331653`
- Class-B survival AUC controls: `0.6963509721635917`

## Required Correlations

- M1_original_score vs M3_reuse_score: Pearson `0.990069`, Spearman `0.969283`, partial `0.992384`
- M1_original_score vs M5_perturbation_centrality_score: Pearson `0.973812`, Spearman `0.993496`, partial `0.974242`
- M3_reuse_score vs M5_perturbation_centrality_score: Pearson `0.965993`, Spearman `0.973116`, partial `0.963675`
- M1_original_score vs M6_frequency_control_score: Pearson `-0.184517`, Spearman `-0.213151`, partial `nan`
- M3_reuse_score vs M6_frequency_control_score: Pearson `-0.256677`, Spearman `-0.378413`, partial `nan`
- M5_perturbation_centrality_score vs M6_frequency_control_score: Pearson `-0.242043`, Spearman `-0.277169`, partial `nan`
- M4_compression_score vs M6_frequency_control_score: Pearson `0.927056`, Spearman `0.927179`, partial `nan`

## Limitations

- Seed stability requires full 17D-style outputs for seeds 43 and 44.

## Artifacts

- feature_matrix.csv
- correlation_matrix.csv
- partial_correlation_matrix.csv
- pca_f1_summary.json / pca_f2_summary.json / pca_f3_summary.json
- pca_loadings.csv
- factor_analysis_summary.json
- ica_summary.json
- reconstruction_results.csv
- prediction_results.csv
- control_leakage.csv
- seed_stability.json
- latent_components.csv
- latent_axis_interpretation.md
- final_decision.json