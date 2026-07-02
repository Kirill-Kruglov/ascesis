# Experiment 17E - Latent Metric Geometry

This experiment analyzes the metric space produced by experiment 17D.

Default input:

```bash
python3 scripts/run_latent_metric_geometry.py
```

The default path reads:

```text
../17D_closure_metric_robustness/outputs_17D
```

Outputs are written to:

```text
outputs_17E/
```
Optional per-class perturbation labels can be generated with:

```bash
python3 scripts/generate_attack_labels.py
python3 scripts/run_latent_metric_geometry.py --attack-labels outputs_17E/attack_labels.csv
```

That optional pass reruns the 17A.2 perturbation analyzer and may take substantially longer than the default latent-geometry analysis.
