# Experiment 17D — Closure Metric Robustness / Functional Indispensability

## Project

`17D_closure_metric_robustness`

## Purpose

Test whether the result of Experiment 17C is a real substrate property or an artifact of the chosen closure score.

17C showed that consequence-invariant classes and closure-active classes do not coincide.

But it remains unclear whether closure measures:

```text
semantic closure
```

or merely:

```text
a scoring artifact
```

or a deeper property:

```text
functional indispensability
```

This experiment attempts to falsify the 17C interpretation.

---

# Core Question

Does the “active semantic subset” remain stable when the closure score is replaced by independently defined internal metrics?

---

# Hypotheses

## H3-metric-artifact

17C result is mostly caused by the specific closure score formula.

Prediction:

```text
Different internal scoring formulas select very different active classes.
Low overlap between active subsets.
Different Class B survival behavior.
```

## H4-functional-indispensability

17C detected a deeper internally grounded property.

Prediction:

```text
Different internal metrics converge on a similar active subset.
Active classes remain Class-A invariant.
Active classes remain sharply sensitive to Class-B theory changes.
```

## Null

No stable active subset exists beyond raw consequence invariance.

---

# Inputs

Reuse outputs and code from 17C.

Do not change:

```text
DAG generator
consequence verifier
Class A / Class B taxonomy
perturbation operators
base run parameters
```

Use:

```text
--seed 42
--num-dags 500
--max-depth 6
```

If affordable, also run:

```text
--seed 43
--seed 44
```

---

# Metric Families

Implement at least five independent internal closure metrics.

All metrics must use only internally derivable quantities.

Forbidden:

```text
external labels
human semantic categories
LLM judgments
embeddings
internet data
manual whitelists
```

---

## M1 — Original 17C Closure Score

Reuse the original 17C interpreter score.

This is the baseline.

---

## M2 — Intervention-Only Score

Use only causal/intervention role.

Example components:

```text
P(Y | do(X))
P(Y | do(X), Z)
Effect(X -> Y)
```

Do not use frequency, DAG diversity, operator diversity, or depth.

Purpose:

```text
Test whether active classes are selected by causal role alone.
```

---

## M3 — Reuse-Only Score

Use only iterative reuse across derivation channels.

A class is active if it participates repeatedly in future derivations.

Do not use intervention labels or consequence type.

Purpose:

```text
Test whether closure is really recurrence / self-maintenance.
```

---

## M4 — Minimality / Compression Score

Prefer classes that explain many consequences with low representational complexity.

Possible definition:

```text
score = downstream_coverage / description_complexity
```

where complexity may include:

```text
expression depth
number of operators
signature length
```

Purpose:

```text
Test whether closure is actually compression or explanatory leverage.
```

---

## M5 — Perturbation-Centrality Score

A class is active if removing or perturbing it changes many downstream consequence signatures.

Use internal ablation only.

Do not use Class B attack results directly as input.

Purpose:

```text
Test whether closure is functional indispensability.
```

---

## M6 — Anti-Frequency Control

Select classes using high frequency / high DAG diversity only.

This is a negative control.

Purpose:

```text
If this behaves like semantic closure, then the experiment is likely detecting generic popularity, not meaning.
```

---

## M7 — Random Matched Control

Randomly select classes matched to the active subset by:

```text
class_size
depth
operator_count
DAG diversity bucket
```

Purpose:

```text
Estimate how much separation is expected by chance.
```

---

# Procedure

For each metric M1–M7:

1. Compute score for all consequence classes.
2. Select active subset using a fixed percentile threshold matching M1 active fraction.
3. Run Class A perturbation attack.
4. Run Class B perturbation attack.
5. Record survival metrics.
6. Compare selected active subsets.

---

# Required Metrics

For each metric:

```text
total_classes
active_classes
active_fraction
mean_score
score_distribution
Class_A_surviving_fraction
Class_B_surviving_fraction
mean_auc_gns_Class_A
mean_auc_gns_Class_B
mean_attack_cost_broken
```

---

# Overlap Analysis

Compute pairwise overlap between active subsets:

```text
Jaccard similarity
overlap coefficient
rank correlation of scores
top-k overlap
```

Compare all real metrics against random matched control.

Required table:

```text
metric_i
metric_j
jaccard
overlap_coefficient
spearman_rank_correlation
```

---

# Stability Criterion

A stable functional core exists if:

```text
M1, M2, M3, M4, M5
show significantly higher overlap with each other
than with M6 or M7
```

and if they produce similar perturbation behavior:

```text
Class A survival ≈ 1.0
Class B survival sharply lower than open baseline
```

---

# Main Comparisons

## Test 1 — Metric Dependence

Question:

```text
Does changing the closure metric change the active subset?
```

If yes:

```text
17C may be metric-dependent.
```

If no:

```text
17C likely detected a real substrate property.
```

---

## Test 2 — Functional Core

Question:

```text
Is there an intersection of active classes selected by multiple independent metrics?
```

Define:

```text
functional_core = classes selected by at least 3 of M1–M5
strict_core = classes selected by at least 4 of M1–M5
```

Report size and perturbation behavior of both.

---

## Test 3 — Negative Control

Question:

```text
Do frequency-only or random-matched controls reproduce the 17C effect?
```

If yes:

```text
closure effect is not trustworthy.
```

If no:

```text
closure effect is not reducible to popularity or sampling bias.
```

---

## Test 4 — Dead Invariant Recheck

Take the 743 closure-dead Class-A-invariant classes from 17C.

For each metric, report:

```text
how many become active
how many remain dead
mean score under each metric
```

If many become active under alternative metrics, then 17C “deadness” was metric-specific.

If most remain dead, then H2-rel is more seriously weakened.

---

# Decision Logic

## Classification: Metric_artifact

Use if:

```text
active subsets differ strongly across metrics
and overlap is close to random matched control
and Class B behavior varies widely
```

Interpretation:

```text
17C does not establish a stable closure-active subset.
```

---

## Classification: Functional_core_supported

Use if:

```text
independent internal metrics converge on a common active core
and this core preserves Class A invariance
and shows distinct Class B sensitivity
and controls fail to reproduce the effect
```

Interpretation:

```text
17C likely detected functional indispensability, not merely a scoring artifact.
```

---

## Classification: Frequency_artifact

Use if:

```text
anti-frequency or frequency-only controls reproduce the same behavior
```

Interpretation:

```text
closure score mostly tracks generic prevalence / DAG diversity.
```

---

## Classification: Inconclusive

Use if:

```text
metrics disagree
but controls are also unstable
or sample size is too small
or threshold choice dominates the result
```

---

# Kill Conditions

Reject strong interpretation of 17C if:

```text
M1 is not reproduced by M2–M5
or
random matched control performs similarly
or
active subset depends mainly on threshold
or
frequency-only control explains the result
```

Reject H2-rel sufficiency more strongly if:

```text
most 17C closure-dead invariant classes remain inactive
under independent metrics
```

Support H4 if:

```text
a stable functional core appears
across independent internal metrics
and survives negative controls
```

---

# Required Outputs

Create:

```text
experiments/17D_closure_metric_robustness/outputs_17D/
```

Required files:

```text
metric_scores.csv
metric_active_sets.csv
metric_summaries.json
pairwise_overlap.csv
rank_correlations.csv

functional_core.csv
strict_core.csv
functional_core_summary.json

dead_invariant_recheck.csv
control_comparison.json
class_a_by_metric.csv
class_b_by_metric.csv

failure_examples.json
final_decision.json
final_report.md
implementation_notes.md
```

---

# Required Questions

Answer explicitly:

1. Does the 17C active subset survive replacement of the closure metric?

2. Do independent internal metrics converge on a common active core?

3. Are 17C closure-dead invariant classes still dead under alternative metrics?

4. Can frequency-only or random-matched controls reproduce the same effect?

5. Is the observed closure effect better described as:

   * semantic closure,
   * functional indispensability,
   * frequency artifact,
   * metric artifact,
   * or inconclusive?

6. What is the strongest counterexample against 17C?

7. What is the strongest evidence for a stable functional core?

---

# Reporting Rules

Do not claim “meaning” has been found.

Use cautious language:

```text
functional core
closure-active subset
internally indispensable classes
metric-stable classes
```

Avoid:

```text
true semantic meaning
real-world semantics
biological semantic closure proven
```

---

# Scientific Interpretation

If `Functional_core_supported`:

```text
The project has found evidence for an internally stable functional core:
a subset of consequence classes selected by multiple independent internal criteria.
This weakens raw H2-rel and suggests that consequence invariance must be supplemented by functional indispensability.
```

If `Metric_artifact`:

```text
17C was useful as a falsification attempt, but its closure result does not yet identify a stable substrate property.
The project should not build on H3 until a metric-independent core is found.
```

If `Frequency_artifact`:

```text
Closure was mostly measuring prevalence or generic structural spread.
The hypothesis must be reformulated.
```

---

# Expected Value

This experiment is valuable even if it destroys 17C.

Possible useful outcomes:

```text
17C survives as a real signal.
17C collapses as metric artifact.
A smaller functional core is found.
H2-rel is restored.
H4 replaces H3.
A new hidden assumption is exposed.
```

