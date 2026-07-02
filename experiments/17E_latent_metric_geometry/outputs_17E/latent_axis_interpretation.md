# Experiment 17E - Latent Axis Interpretation

Classification: `Multi_axis_supported`

One axis reconstructs the successful metric cluster, but perturbation sensitivity requires additional latent axes.

## Required Questions

1. Latent dimensions for M1/M3/M5: k=1 gives mean reconstruction R2 `0.984428`; k=2 gives `0.996938`.
2. One dominant closure-like axis: PC1 over real metrics explains `0.721998` variance.
3. Independence from controls: controls explain `0.696395` of PC1.
4. Class B sensitivity: latent1 AUC `0.5023683295671824`; latent2 AUC `0.7315655186114076`; latent3 AUC `0.768968364331653`.
5. More axes: latent2/3 materially improve Class-B prediction over latent1; functional-core latent2 AUC `0.9993036655903477` vs latent1 AUC `0.9928286045991502`.
6. Seed stability: not tested; only seed 42 full 17D outputs are available.
7. Interpretation: `Multi_axis_supported`.

## PCA Summary

- F1 real metrics PC1 variance: 0.721998293170383
- F2 real+controls PC1 variance: 0.5307946047687934
- F3 all internal PC1 variance: 0.40556781469768727

The experiment does not claim true meaning or semantic essence. It tests only latent structural factors in this toy substrate.