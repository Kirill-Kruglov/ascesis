# Experiment 17F - Cross-Substrate Comparison

Global classification: `DAG_artifact`

Only the causal-DAG substrate reproduced the 17E multi-axis pattern.

| substrate | classes | Class A survive | Class B survive | M135 R2 k=1 | AUC latent1 | AUC latent2 | AUC latent3 | controls AUC | local |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S1_causal_dag | 29934 | 1.0000 | 0.1283 | 0.9844 | 0.5193 | 0.6576 | 0.7645 | 0.7521 | multi_axis |
| S2_directed_graph | 607 | 1.0000 | 0.5272 | 0.9471 | 0.5643 | 0.6227 | 0.6186 | 0.5700 | metric_noise |
| S3_term_rewrite | 422 | 1.0000 | 0.3555 | 0.9336 | 0.6556 | 0.6458 | 0.6355 | 0.6058 | one_axis |
| S4_finite_automata | 359 | 1.0000 | 0.5181 | 0.9442 | 0.5068 | 0.5560 | 0.5713 | 0.5347 | control_artifact |

## Required Questions

1. Does the 17E pattern reproduce outside causal DAGs? See non-causal rows classified as `multi_axis`.
2. Is causal/interventional structure required? It is not required if any non-causal substrate is `multi_axis`.
3. Do non-causal finite systems show similar geometry? See S2/S3/S4 local decisions.
4. Are M1/M3/M5 clustered? See `m135_reconstruction_r2_k1`.
5. Is one axis enough to reconstruct metrics? Usually yes when R2 is high.
6. Is one axis enough to predict perturbation survival? Compare latent1 vs latent2/latent3 AUC.
7. Are controls sufficient? Compare controls AUC and local control-artifact decisions.
8. Best supported global hypothesis: `DAG_artifact`.

No claim is made that meaning or universal semantic geometry has been proven.