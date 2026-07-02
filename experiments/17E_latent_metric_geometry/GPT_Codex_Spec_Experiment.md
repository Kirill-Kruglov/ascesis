# Experiment 17E — Latent Metric Geometry

## Project

`17E_latent_metric_geometry`

## Purpose

Experiment 17D showed that closure metrics do not fully agree.

However, the disagreement may not mean that the closure signal is arbitrary. It may mean that the metrics are projections of a smaller latent structure.

This experiment tests whether internal semantic/closure metrics reduce to:

```text id="ym1e8a"
one dominant latent axis
```

or require:

```text id="3zxgd4"
multiple independent latent axes
```

This is a higher-level test of whether “meaning-like” structure in this substrate is intrinsically one-dimensional or multi-dimensional.

---

# Background

17C suggested:

```text id="2c6mij"
consequence invariance alone is insufficient.
```

17D weakened that interpretation:

```text id="loejq3"
closure-active/dead classification depends on metric choice.
```

But 17D also found a strong cluster:

```text id="vw6qy9"
M1_original
M3_reuse
M5_perturbation_centrality
```

These metrics may be measuring the same hidden variable.

This experiment asks:

```text id="zla13n"
Are successful closure metrics independent,
or are they projections of a lower-dimensional latent geometry?
```

---

# Research Question

What is the minimal latent dimensionality of the internal metric space?

---

# Hypotheses

## H5_one_axis

All successful closure-like metrics mostly measure a single latent variable.

Prediction:

```text id="ewz3fl"
PC1 or one latent factor explains most variance among M1/M3/M5 and predicts Class B sensitivity.
```

Interpretation:

```text id="ycz703"
There may be one dominant internal functional-indispensability axis.
```

## H6_multi_axis

Closure-like behavior requires multiple independent latent axes.

Prediction:

```text id="qg7y93"
At least two or more orthogonal factors are required to reconstruct metric behavior and predict perturbation outcomes.
```

Interpretation:

```text id="unl0ry"
No single definition of meaning/closure will be sufficient.
```

## H7_metric_noise

Metric geometry is unstable or dominated by controls/frequency artifacts.

Prediction:

```text id="69og26"
Latent axes are unstable across seeds or mostly explain frequency/class-size artifacts.
```

---

# Inputs

Use outputs from 17D where possible.

Required input tables:

```text id="uzcek3"
metric_scores.csv
metric_active_sets.csv
class_a_by_metric.csv
class_b_by_metric.csv
dead_invariant_recheck.csv
```

If needed, recompute from 17C/17D pipeline.

Use same base generation parameters:

```text id="yk7xuw"
--seed 42
--num-dags 500
--max-depth 6
```

If affordable, repeat for:

```text id="2lbo5k"
--seed 43
--seed 44
```

---

# Feature Matrix

Construct one row per consequence class.

Columns should include all available internal metrics and raw structural descriptors.

Required columns:

```text id="xo7qj6"
M1_original_score
M2_intervention_score
M3_reuse_score
M4_compression_score
M5_perturbation_centrality_score
M6_frequency_control_score
M7_random_matched_score

class_size
dag_diversity
operator_diversity
depth_min
depth_max
expression_depth
frequency
reuse_count
reuse_rate
intervention_role
conditional_role
raw_score
role_score
```

Also include labels only for evaluation, not for fitting:

```text id="ie13hn"
class_a_survives
class_b_survives
class_b_attack_cost
class_b_auc_gns
active_M1
active_M3
active_M5
functional_core_membership
strict_core_membership
```

---

# Preprocessing

1. Remove columns that are constant or nearly constant.
2. Log-transform heavy-tailed count variables:

```text id="k8n9lx"
class_size
dag_diversity
frequency
reuse_count
```

3. Standardize numeric features to zero mean and unit variance.
4. Keep controls (`M6`, `M7`, frequency, class_size) marked separately.

---

# Analyses

## A1 — Correlation Structure

Compute:

```text id="mdcwx1"
Pearson correlation
Spearman correlation
partial correlations controlling for frequency/class_size/dag_diversity
```

Required comparisons:

```text id="e5y1n2"
M1-M3
M1-M5
M3-M5
M1-M6
M3-M6
M5-M6
M4-M6
```

---

## A2 — PCA

Run PCA on:

### Feature Set F1

Only real metrics:

```text id="8tpyl7"
M1, M2, M3, M4, M5
```

### Feature Set F2

Real metrics + controls:

```text id="iv4qv6"
M1, M2, M3, M4, M5, M6, M7
```

### Feature Set F3

All internal descriptors:

```text id="llng0o"
all numeric structural columns
```

Report:

```text id="cmrspp"
explained variance ratio
cumulative variance
loadings
number of components needed for 80%, 90%, 95% variance
```

---

## A3 — Factor Analysis / ICA

Run at least:

```text id="0pcap2"
FactorAnalysis
FastICA
```

for candidate dimensions:

```text id="v4j6xg"
k = 1, 2, 3, 4, 5
```

Report which factor structure is most stable and interpretable.

---

## A4 — Reconstruction Test

Test how many latent dimensions are needed to reconstruct M1/M3/M5.

For k = 1..5:

```text id="16rf6v"
fit latent embedding using all training classes
reconstruct M1, M3, M5
report R2 and MAE
```

Also run reconstruction after removing frequency-like controls.

Question:

```text id="7swuww"
Can M1/M3/M5 be reconstructed from one latent axis?
```

---

## A5 — Predictive Test

Use latent components to predict perturbation behavior.

Targets:

```text id="fp6byc"
class_b_survives
class_b_auc_gns
class_b_attack_cost
functional_core_membership
strict_core_membership
```

Models:

```text id="wisgff"
logistic regression
ridge regression
small decision tree
```

Use cross-validation.

Compare:

```text id="x9jp2b"
1 latent dimension
2 latent dimensions
3 latent dimensions
all raw metrics
controls only
random baseline
```

Report:

```text id="cpd5i7"
AUC
accuracy
F1
R2 where applicable
calibration if available
```

---

## A6 — Stability Across Seeds

If multiple seeds are available:

1. Run the same analysis per seed.
2. Align components by maximum loading similarity.
3. Report component stability.

Required:

```text id="gspnnt"
component_loading_correlation_across_seeds
latent_score_correlation_across_seeds
stable_axis_count
```

---

## A7 — Control Leakage Test

Determine whether the dominant latent axes are just frequency/size artifacts.

For each latent component, regress it against:

```text id="ltjww6"
class_size
frequency
dag_diversity
operator_diversity
depth
M6_frequency_control
M7_random_matched
```

Report:

```text id="2r78hj"
variance explained by controls
residual predictive power after controls
```

If PC1 is mostly explained by frequency/control variables, do not interpret it as functional indispensability.

---

# Decision Logic

## Classification: One_axis_supported

Use if:

```text id="ea0q99"
one component explains most variance among M1/M3/M5
and one component predicts Class B behavior nearly as well as all metrics
and the component is not reducible to frequency/control variables
and the component is stable across seeds
```

Interpretation:

```text id="o5b4ao"
The substrate appears to contain a dominant functional-indispensability axis.
```

---

## Classification: Multi_axis_supported

Use if:

```text id="8bln1r"
two or more components are required
to reconstruct M1/M3/M5
or predict perturbation behavior
and these components are not reducible to controls
```

Interpretation:

```text id="k9zjag"
The substrate does not admit a single scalar closure/meaning measure.
```

---

## Classification: Control_artifact

Use if:

```text id="r1ixu7"
dominant axes are mostly explained by frequency, class size, DAG diversity, or M6/M7 controls
```

Interpretation:

```text id="8ahcbr"
The closure signal is mostly structural prevalence, not functional indispensability.
```

---

## Classification: Metric_noise

Use if:

```text id="os44kj"
latent structure is unstable
or predictive power is close to random
or components do not generalize across seeds
```

---

## Classification: Inconclusive

Use if:

```text id="t9qpb9"
the data partially supports multiple interpretations
without clean separation
```

---

# Required Outputs

Create:

```text id="0hi1cb"
experiments/17E_latent_metric_geometry/outputs_17E/
```

Required files:

```text id="bsl5jk"
feature_matrix.csv
correlation_matrix.csv
partial_correlation_matrix.csv

pca_f1_summary.json
pca_f2_summary.json
pca_f3_summary.json
pca_loadings.csv

factor_analysis_summary.json
ica_summary.json

reconstruction_results.csv
prediction_results.csv
control_leakage.csv

seed_stability.json
latent_components.csv
latent_axis_interpretation.md

final_decision.json
final_report.md
implementation_notes.md
failure_examples.json
```

---

# Required Questions

Answer explicitly:

1. How many latent dimensions are needed to explain M1/M3/M5?

2. Is there one dominant closure-like axis?

3. Is that axis independent of frequency/class-size/DAG-diversity controls?

4. Does the latent axis predict Class B sensitivity?

5. Does adding more axes improve prediction materially?

6. Are axes stable across seeds?

7. Does the result support one-axis, multi-axis, control-artifact, metric-noise, or inconclusive interpretation?

---

# Scientific Interpretation Rules

Do not claim that the latent axis is “meaning.”

Allowed language:

```text id="doyhm7"
functional-indispensability axis
closure-like latent axis
internal metric geometry
latent structural factor
```

Forbidden language:

```text id="tbva0t"
true meaning discovered
semantic essence
proof of real-world semantics
```

---

# Expected Value

This experiment is useful under all outcomes.

If one-axis:

```text id="2fkd9l"
Stop searching for many closure metrics.
Study the dominant latent axis.
```

If multi-axis:

```text id="3ibk9n"
Reject any scalar definition of meaning/closure for this substrate.
```

If control-artifact:

```text id="y34cgv"
Do not build on 17C/17D closure results.
Return to consequence invariance or redesign closure.
```

If metric-noise:

```text id="dvfkip"
The current substrate does not support stable closure analysis.
```

