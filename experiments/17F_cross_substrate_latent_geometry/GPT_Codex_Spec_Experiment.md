# Experiment 17F — Cross-Substrate Latent Geometry Falsification

## Project

`17F_cross_substrate_latent_geometry`

## Purpose

Experiment 17E found that the current causal-DAG substrate has a multi-axis latent metric geometry:

```text id="8fmefw"
one latent axis reconstructs successful internal-function metrics,
but perturbation sensitivity requires additional latent axes.
```

This is a strong result, but it may still be an artifact of:

```text id="0y0sh9"
DAG architecture
causal verifier design
chosen observable metrics
or perturbation taxonomy
```

Experiment 17F attempts to falsify the generality of the 17E result by repeating the latent-geometry analysis across multiple independent substrates.

The goal is not to prove semantic geometry.

The goal is to determine whether the multi-axis structure is:

```text id="e5l064"
DAG-specific
causality-specific
generic to finite generative systems
or metric artifact
```

---

# Core Research Question

Does the 17E pattern survive substrate replacement?

Specifically:

```text id="sn9bx2"
Can one latent axis reconstruct internal-function metrics,
while perturbation sensitivity requires additional independent axes,
across multiple substrates?
```

---

# Background

17A.2 showed:

```text id="en5l82"
representation-preserving perturbations preserve consequence backbone;
theory-changing perturbations destroy most classes.
```

17C suggested that consequence invariance alone may not be sufficient.

17D showed that closure metrics are not fully robust, but a cluster of metrics exists.

17E showed:

```text id="wp3tuu"
M1/M3/M5 collapse to one latent axis,
but Class-B survival requires multiple axes.
```

17F attacks the next hidden assumption:

```text id="w96t8d"
the latent geometry belongs to the substrate,
not to the DAG/verifier implementation.
```

---

# Hypotheses

## H_DAG_artifact

The multi-axis geometry is an artifact of causal-DAG structure.

Prediction:

```text id="0zwuxk"
The 17E pattern appears only in the causal-DAG substrate.
Other substrates do not show the same separation between metric reconstruction and perturbation prediction.
```

## H_causality_required

The multi-axis geometry requires causal/interventional structure.

Prediction:

```text id="0pwroi"
Causal DAGs show the 17E pattern.
Non-causal substrates show weaker or absent perturbation-axis separation.
```

## H_finite_generator_generic

The multi-axis geometry is generic to finite generative systems with nontrivial consequence equivalence.

Prediction:

```text id="0sfa4r"
Multiple substrates show the same pattern,
even without causal semantics.
```

## H_metric_artifact

The effect is caused by the chosen observable metrics.

Prediction:

```text id="fdztn7"
Changing substrate changes the metric geometry unpredictably;
dominant axes do not align with comparable internal roles;
controls explain most of the signal.
```

---

# Substrates

Implement at least four substrates.

## S1 — Causal DAG Substrate

Reuse the existing 17A.2/17E causal DAG substrate.

This is the baseline.

Consequences include:

```text id="vnwxxe"
Reachable
Ancestor
Blocked
Independent
Effect
P_obs
P_do
P_cond_do
```

Class A and Class B perturbations reuse the 17A.2 taxonomy.

---

## S2 — Non-Causal Directed Graph Substrate

Use directed graphs with graph-theoretic consequences only.

No causal/interventional semantics.

Allowed consequences:

```text id="1suohc"
Reachable(X,Y)
PathLengthBucket(X,Y)
InDegreeBucket(X)
OutDegreeBucket(X)
SharedSuccessor(X,Y)
SharedPredecessor(X,Y)
CycleParticipation(X)
CutVertexLikeRole(X)
```

Representation-preserving perturbations:

```text id="ei83xm"
node renaming
subdivide edge preserving reachability
replace internal path by equivalent path
```

Theory-changing perturbations:

```text id="wdiaik"
add edge
remove edge
reverse edge
merge nodes
delete path
swap branches
```

Purpose:

```text id="dfjfkk"
Test whether causal semantics are required,
or graph consequence structure alone is enough.
```

---

## S3 — Term Rewriting Substrate

Construct a finite rewrite system.

Generate terms up to bounded depth.

Consequences are normal-form or derivability relations.

Allowed consequences:

```text id="zt2ng1"
NormalForm(t) = n
Derives(t,u)
EquivalentNF(t,u)
RewriteDistanceBucket(t,u)
CriticalPairParticipation(t)
ConfluenceWitness(t)
```

Representation-preserving perturbations:

```text id="4eqti3"
alpha rename variables
refactor equivalent rewrite path
replace term by provably same normal form
```

Theory-changing perturbations:

```text id="6h6t3l"
add rewrite rule
remove rewrite rule
reverse rewrite rule
change rule RHS
merge symbols
split symbol with non-equivalent behavior
```

Purpose:

```text id="8hqfgl"
Test whether latent geometry appears in symbolic derivation without graph causality.
```

---

## S4 — Finite Automata Substrate

Generate deterministic finite automata over a small alphabet.

Consequences are language-behavioral.

Allowed consequences:

```text id="3i1amw"
Accepts(w)
Rejects(w)
EquivalentState(q1,q2)
ReachableState(q)
MinimalStateClass(q)
TransitionEffect(q,a,q')
DistinguishingWordBucket(q1,q2)
```

Representation-preserving perturbations:

```text id="wp9o14"
state renaming
minimization-preserving refactor
split equivalent state with identical future behavior
```

Theory-changing perturbations:

```text id="s3mmrn"
flip accepting state
change transition
delete transition
add transition
merge distinguishable states
alter alphabet mapping
```

Purpose:

```text id="f4a6xu"
Test whether latent geometry appears in formal behavioral systems.
```

---

## Optional S5 — Reaction Network Substrate

If affordable, implement a small chemical reaction network substrate.

Consequences:

```text id="6r6vbe"
ReachableSpecies
StoichiometricConservation
CatalyticRole
ReactionPathExists
SteadyStateBucket
DependencyOfSpecies
```

Representation-preserving perturbations:

```text id="rjpz10"
rename species
split intermediate preserving net reaction
replace equivalent reaction pathway
```

Theory-changing perturbations:

```text id="p08ddh"
add reaction
remove reaction
reverse reaction
change stoichiometry
merge species
remove catalyst
```

Purpose:

```text id="3i5hmo"
Test a biology-like substrate closer to systems biology.
```

---

# General Requirements

For each substrate, implement:

1. finite generator;
2. consequence extractor;
3. consequence class construction;
4. representation-preserving perturbation family;
5. theory-changing perturbation family;
6. internal metric panel;
7. latent geometry analysis.

Do not use:

```text id="w0xfbj"
LLM labels
external semantic judgments
embeddings
internet data
human-written class importance
manual cherry-picking
```

---

# Internal Metric Panel

For each substrate, define comparable metric families.

Metrics need not be identical in form, but must be analogous in role.

## M1 — Original / composite functional score

Combination of reuse, role participation, diversity, and depth.

## M2 — Intervention / action-effect score

For causal DAGs:

```text id="r4s9zg"
intervention role
```

For non-causal substrates, use closest analogue:

```text id="6snubs"
effect of local operation on downstream consequences
```

## M3 — Reuse score

How often a class participates in downstream derivations or consequence generation.

## M4 — Compression / minimality score

How much downstream structure is explained per unit description complexity.

## M5 — Perturbation centrality score

How many downstream consequence signatures change when this class is ablated or perturbed.

Do not use final Class-B survival labels directly in M5.

## M6 — Frequency control

High frequency / prevalence / class size / occurrence count.

## M7 — Random matched control

Random class selection matched by:

```text id="pbpujm"
class size
depth
frequency bucket
operator/type distribution where possible
```

---

# Perturbation Analysis

For each substrate:

Run Class A attacks:

```text id="avwfrk"
representation-preserving perturbations
```

Run Class B attacks:

```text id="zlx50u"
theory-changing perturbations
```

Report:

```text id="hzpr7n"
Class_A_survival_fraction
Class_B_survival_fraction
Class_B_attack_cost
Class_B_auc_gns
```

---

# Latent Geometry Analysis

Repeat the 17E analysis independently for each substrate.

## A1 — Correlation Analysis

Compute:

```text id="f3cm33"
Pearson correlations
Spearman correlations
partial correlations controlling for frequency/class_size/depth
```

Required comparisons:

```text id="yp3l2m"
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

### F1 — Real Metrics

```text id="q8povs"
M1, M2, M3, M4, M5
```

### F2 — Real Metrics + Controls

```text id="tbdhow"
M1, M2, M3, M4, M5, M6, M7
```

### F3 — All Internal Descriptors

All numeric internal descriptors available for that substrate.

Report:

```text id="alqrfe"
explained variance ratio
cumulative variance
loadings
components needed for 80%, 90%, 95%
```

---

## A3 — Reconstruction Test

For k = 1..5 latent dimensions:

```text id="zej1s1"
reconstruct M1/M3/M5
report mean R2
report individual R2
```

Question:

```text id="wc9tdj"
Does one axis reconstruct the successful metric cluster?
```

---

## A4 — Perturbation Prediction Test

For k = 1..5 latent dimensions:

Predict:

```text id="pwaapq"
Class_B_survives
Class_B_auc_gns
Class_B_attack_cost
```

Compare:

```text id="zozzbn"
latent_1
latent_2
latent_3
all_raw_metrics
controls_only
random_baseline
```

Report:

```text id="f3kp86"
AUC
F1
accuracy
R2 where applicable
```

Question:

```text id="kfivrz"
Does perturbation sensitivity require more axes than metric reconstruction?
```

---

## A5 — Control Leakage

For each substrate:

Regress dominant latent axes against controls:

```text id="nv32uy"
frequency
class_size
depth
DAG/graph/state/term diversity
M6
M7
```

Report:

```text id="o0bku2"
variance explained by controls
residual predictive power
```

---

## A6 — Cross-Substrate Pattern Test

For each substrate, classify local result:

```text id="pn2zzl"
one_axis
multi_axis
control_artifact
metric_noise
no_structure
```

Then compare.

Required summary table:

```text id="n6a4hi"
substrate
class_count
class_a_survival
class_b_survival
m135_reconstruction_r2_k1
class_b_auc_latent1
class_b_auc_latent2
class_b_auc_latent3
controls_auc
local_classification
```

---

# Decision Logic

## Classification: DAG_artifact

Use if:

```text id="fjv4f5"
S1 shows multi-axis geometry,
but S2/S3/S4 do not show comparable structure.
```

Interpretation:

```text id="4s1lcp"
17E is likely specific to causal-DAG implementation.
```

---

## Classification: Causality_required

Use if:

```text id="l47fss"
causal DAG substrate shows the pattern,
graph/term/automata substrates do not,
or only causal/intervention-like substrates show it.
```

Interpretation:

```text id="vjz0vh"
causal/interventional structure may be required for semantic-like latent geometry.
```

---

## Classification: Finite_generator_generic

Use if:

```text id="1mm72c"
S1/S2/S3/S4 all show the 17E pattern:
one axis reconstructs M1/M3/M5,
but perturbation prediction requires additional axes,
and controls do not explain the result.
```

Interpretation:

```text id="ort5yl"
multi-axis latent geometry may be generic to finite derivational substrates.
```

---

## Classification: Metric_artifact

Use if:

```text id="ply3z5"
metric geometry changes unpredictably across substrates,
controls explain most axes,
or M1/M3/M5 do not form a stable cluster in most substrates.
```

Interpretation:

```text id="qj00vh"
17E likely reflects metric design rather than substrate structure.
```

---

## Classification: Mixed

Use if:

```text id="unwdlk"
some substrates show the pattern,
others do not,
with a systematic explanation but not enough to decide generality.
```

Examples:

```text id="dqiy06"
causal + automata yes, rewriting no
DAG + graph yes, automata no
only substrates with nontrivial equivalence classes yes
```

---

## Classification: Inconclusive

Use if:

```text id="zocify"
sample sizes too small
perturbation classes not comparable
consequence classes collapse
or implementation differences dominate results
```

---

# Kill Conditions

Reject general semantic-geometry interpretation if:

```text id="2wzx47"
only S1 reproduces the 17E pattern
```

Reject causality-required interpretation if:

```text id="qccqlh"
non-causal substrates reproduce the same pattern robustly
```

Reject finite-generator-generic interpretation if:

```text id="mf5qbf"
at least two nontrivial finite substrates fail to show the pattern
```

Reject metric-level interpretation if:

```text id="9sutf0"
controls reproduce the same structure across substrates
```

---

# Minimum Run Parameters

For each substrate:

```text id="p9bs1z"
--seed 42
--num-objects 500
--max-depth 6
```

Use equivalent parameters where needed:

```text id="codgzo"
DAGs: num_dags
graphs: num_graphs
rewrite systems: num_terms / num_systems
automata: num_automata
reaction networks: num_networks
```

If affordable:

```text id="dcr238"
--seed 43
--seed 44
```

---

# Required Outputs

Create:

```text id="91m24y"
experiments/17F_cross_substrate_latent_geometry/outputs_17F/
```

For each substrate:

```text id="6hxxcz"
<substrate>_feature_matrix.csv
<substrate>_metric_scores.csv
<substrate>_attack_labels.csv
<substrate>_correlation_matrix.csv
<substrate>_partial_correlations.csv
<substrate>_pca_summary.json
<substrate>_pca_loadings.csv
<substrate>_reconstruction_results.csv
<substrate>_prediction_results.csv
<substrate>_control_leakage.csv
<substrate>_local_decision.json
<substrate>_failure_examples.json
```

Global outputs:

```text id="s0n7gg"
cross_substrate_summary.csv
cross_substrate_decision.json
substrate_comparison.md
final_decision.json
final_report.md
implementation_notes.md
```

---

# Required Questions

Answer explicitly:

1. Does the 17E pattern reproduce outside causal DAGs?

2. Is causal/interventional structure required?

3. Do non-causal finite derivational systems show similar multi-axis geometry?

4. Are M1/M3/M5 clustered in each substrate?

5. Is one latent axis enough to reconstruct internal-function metrics?

6. Is one latent axis enough to predict theory-changing perturbation survival?

7. Are controls sufficient to explain the observed axes?

8. Which hypothesis is best supported:

   * DAG_artifact
   * Causality_required
   * Finite_generator_generic
   * Metric_artifact
   * Mixed
   * Inconclusive

---

# Reporting Rules

Do not claim:

```text id="mrpvwa"
meaning discovered
semantic geometry proven
universal law established
```

Allowed claims:

```text id="zaxcv0"
pattern reproduced
pattern failed under substrate replacement
causality appears necessary
finite-generator effect supported
metric artifact suspected
```

Separate clearly:

```text id="n79u95"
what was measured
what was inferred
what remains open
```

---

# Scientific Interpretation

If `DAG_artifact`:

```text id="o3kmbp"
The project should not generalize 17E beyond causal-DAG substrate.
Next work should inspect which DAG features generate the geometry.
```

If `Causality_required`:

```text id="px8dfa"
The project should treat interventional structure as a necessary ingredient for semantic-like geometry.
```

If `Finite_generator_generic`:

```text id="321u4r"
The project has found a candidate general constraint:
finite derivational substrates with nontrivial consequence equivalence produce multi-axis latent geometry.
```

If `Metric_artifact`:

```text id="a934l1"
The current metric panel is not reliable enough to support semantic interpretation.
Return to observability design.
```

If `Mixed`:

```text id="c2ecmt"
Identify the shared property of substrates that reproduce the effect.
This shared property becomes the next target for falsification.
```

---

# Expected Value

The experiment is valuable under all outcomes.

Possible useful results:

```text id="pihnve"
17E collapses as DAG artifact.
Causality becomes a necessary condition.
A generic finite-generator constraint emerges.
Metric design is exposed as the true driver.
A mixed pattern identifies the next hidden variable.
```

The goal is to reduce the hypothesis space, not to confirm the preferred interpretation.

