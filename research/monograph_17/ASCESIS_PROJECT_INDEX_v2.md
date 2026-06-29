# ASCESIS_PROJECT_INDEX_v2.md

```markdown
# ASCESIS Project Index
## Complete Research Reference for Independent Scientific Audit
### Version 2.0

---

# Purpose

This document is intended to be the **entry point** for an independent reviewer (Claude Opus, human reviewer, or another research group).

It is **not** a summary.

It is an index into the complete research program.

A reviewer should be able to reconstruct every important scientific conclusion directly from this document together with the repository.

The guiding principle is:

> Every nontrivial statement must be traceable to experiments, computations, artifacts or literature.

---

# Repository Structure

```

memo/

```
memo_v1.1.md
memo_v1.3.md
```

ontology/

```
Research_Ontology_v2.md
Research_Methodology_v2.md
Experimental_Chronicle_v2.md
Scientific_Context_v2.md
Research_Program_v2.md
Appendix_A_Research_Ledger_v2.md
```

experiments/

```
17A.2_Semantic_Perturbation_Taxonomy/

17C_interpretive_closure_test/

17D_closure_metric_robustness/

17E_latent_metric_geometry/

17F_cross_substrate_latent_geometry/
```

```

---

# Reading Order

The recommended review order is:

1. memo_v1.1
2. memo_v1.3
3. Research_Methodology_v2
4. Experimental_Chronicle_v2
5. Research_Ontology_v2
6. Scientific_Context_v2
7. Research_Program_v2
8. Research_Ledger_v2

The methodology should be read before the experiments.

Otherwise many design decisions become difficult to evaluate.

---

# Global Research Goal

The project investigates one question.

Can semantic organization emerge inside finite formal systems without using:

- natural language,
- pretrained models,
- embeddings,
- external ontologies,
- human semantic labels,
- internet knowledge,
- RLHF,
- manually assigned meaning?

Equivalently,

is there a formally identifiable internal organization that deserves semantic interpretation?

The project intentionally does **not** attempt to construct such a theory directly.

Instead it attempts to reduce the admissible space of explanations by repeated falsification.

---

# Methodological Principles

The project follows several permanent methodological rules.

## MP-1

Synthetic substrates only.

Reason:

Natural language mixes semantics with uncontrolled statistical structure.

---

## MP-2

Internal observables only.

Every measured quantity must be computable entirely from the investigated substrate.

---

## MP-3

Falsification first.

Experiments are designed primarily to eliminate explanations.

---

## MP-4

Perturbation-based evaluation.

Meaning is investigated through structural perturbation rather than prediction accuracy.

---

## MP-5

Conservative ontology revision.

Observations do not automatically become ontology entries.

Only experimentally surviving constraints enter the ontology.

---

# Experimental Timeline

The completed experimental series is:

```

17A

↓

17A.2

↓

17C

↓

17D

↓

17E

↓

17F

```

Only experiments beginning with 17A.2 are considered part of the current ontology.

Earlier experiments provide historical context.

---

# Experiment 17A.2

Title

Semantic Perturbation Taxonomy

Directory

```

experiments/17A.2_Semantic_Perturbation_Taxonomy/

```

Outputs

```

experiments/17A.2_Semantic_Perturbation_Taxonomy/outputs_17A2/

```

Primary question

Do all perturbations belong to one semantic class?

Competing explanations

H2

vs

H2-relative

Important outputs

```

representation_only_summary.json

theory_change_summary.json

taxonomy.csv

operator_classification.md

comparison.md

audit_failure_examples.json

representation_only_attack.csv

theory_change_attack.csv

final_decision.json

```

Main observations

Representation-preserving perturbations preserve consequence classes.

Theory-changing perturbations do not.

Main ontology update

Representation-relative invariance becomes mandatory.

---

# Experiment 17C

Title

Interpretive Closure

Directory

```

experiments/17C_interpretive_closure_test/

```

Outputs

```

experiments/17C_interpretive_closure_test/outputs_17C/

```

Question

Is consequence invariance sufficient?

Competing explanations

H2-relative

vs

H3

Important outputs

```

open_summary.json

weak_closure_summary.json

strong_closure_summary.json

closure_metrics.csv

closure_dead_classes.csv

closure_active_classes.csv

class_a_comparison.json

class_b_comparison.json

failure_examples.json

h2_vs_h3_decision.json

```

Main observations

Closure-active subset exists.

Closure-dead invariant classes also exist.

Main limitation

Single closure metric.

---

# Experiment 17D

Title

Closure Metric Robustness

Directory

```

experiments/17D_closure_metric_robustness/

```

Outputs

```

experiments/17D_closure_metric_robustness/outputs_17D/

```

Question

Is closure robust to metric replacement?

Metric families

M1

original

M2

intervention

M3

reuse

M4

compression

M5

perturbation centrality

M6

frequency control

M7

matched random control

Important outputs

```

metric_agreement_matrix.csv

metric_correlation_matrix.csv

functional_core.csv

strict_core.csv

dead_recheck.csv

control_comparison.csv

summary.json

final_decision.json

```

Main observations

M1/M3/M5 form a stable cluster.

Compression aligns with frequency control.

Most closure-dead classes disappear under metric replacement.

Ontology update

Closure score removed as ontology object.

Stable metric family retained.

---

# Experiment 17E

Title

Latent Metric Geometry

Directory

```

experiments/17E_latent_metric_geometry/

```

Outputs

```

experiments/17E_latent_metric_geometry/outputs_17E/

```

Question

What latent structure generates M1/M3/M5?

Analyses

PCA

Correlation

Latent reconstruction

Perturbation prediction

Functional core prediction

Control leakage

Important outputs

```

principal_components.csv

component_loadings.csv

metric_correlations.csv

explained_variance.json

reconstruction_results.json

attack_prediction_auc.json

functional_core_prediction.json

control_leakage.json

attack_labels.csv

summary.json

final_decision.json

```

Main observations

One latent component reconstructs M1/M3/M5.

One latent component fails to predict perturbation survival.

Additional latent dimensions are required.

Ontology update

Dominant latent direction established.

Single scalar semantic observable rejected.

---

# Experiment 17F

Title

Cross-Substrate Latent Geometry

Directory

```

experiments/17F_cross_substrate_latent_geometry/

```

Outputs

```

experiments/17F_cross_substrate_latent_geometry/outputs_17F/

```

Substrates

S1

causal DAG

S2

directed graph

S3

term rewriting

S4

finite automata

Important outputs

```

cross_substrate_summary.csv

metric_geometry.csv

prediction_results.csv

local_classifications.json

substrate_comparison.md

summary.json

final_decision.json

```

Main observations

Only causal DAG reproduces the complete 17E pattern.

Cross-substrate universality is therefore unsupported.

Ontology update

Local constraints separated from universal constraints.

---

# Current Ontology

Established constraints

SC-01

Admissible perturbation classes.

Evidence

17A.2

---

SC-02

Representation-relative invariance.

Evidence

17A.2

17C

17D

17E

17F

---

SC-03

Closure is not uniquely measurable.

Evidence

17D

---

SC-04

Stable internal metric family exists.

Evidence

17D

17E

---

SC-05

Dominant latent metric direction exists.

Evidence

17E

(local)

---

SC-06

Perturbation behaviour is multi-axis.

Evidence

17E

(local)

---

SC-07

Cross-substrate universality unsupported.

Evidence

17F

---

SC-08

Current experiments cannot distinguish

DAG architecture

from

intervention structure.

Evidence

17F

---

# Active Explanations

The project currently considers four principal explanations.

CE-1

DAG architecture.

---

CE-2

Intervention algebra.

---

CE-3

Consequence algebra.

---

CE-4

Observable selection.

No other explanation currently explains all completed experiments better than these four.

---

# Rejected Explanations

RX-01

Meaning survives arbitrary perturbation.

Rejected

17A.2

---

RX-02

Consequence invariance is sufficient.

Rejected

17C

---

RX-03

Closure uniquely identifies semantics.

Rejected

17D

---

RX-04

One scalar explains perturbation behaviour.

Rejected

17E

---

RX-05

17E immediately generalizes.

Rejected

17F

---

# External Scientific Context

The project compared its observations with mature scientific disciplines.

Systems biology

Relevant topics

robustness

functional participation

sloppy models

---

Evolutionary biology

Relevant topics

neutral networks

robustness

evolvability

---

Causal inference

Relevant topics

intervention

invariance

OOD generalization

---

Information theory

Relevant topics

semantic information

compression

PID

---

Statistical physics

Relevant topics

order parameters

renormalization

sloppy manifolds

---

Network science

Relevant topics

centrality

role discovery

structural equivalence

---

Formal methods

Relevant topics

semantic preservation

compiler correctness

abstract interpretation

---

# What Claude Should Verify

The review should focus primarily on falsification rather than agreement.

The following questions are considered the highest priority.

---

## Methodology

Does any experiment contain methodological leakage?

Were any conclusions stronger than the supporting evidence?

Are any perturbation classes incorrectly defined?

Were decision criteria specified before execution?

---

## Computation

Do the reported conclusions follow from the stored JSON and CSV outputs?

Can every ontology entry be reproduced from the preserved artifacts?

Are there missing controls?

Are there hidden statistical assumptions?

---

## Interpretation

Does any ontology constraint overstate what the experiments demonstrate?

Are there alternative explanations not considered?

Can any rejected hypothesis still explain all observations?

---

## External Literature

Are there known experimental results contradicting the ontology?

Are there mature theories explaining the observed latent geometry?

Are there domains omitted from Scientific_Context_v2?

---

## Future Program

Which remaining hypothesis should be attacked first?

Which experiment provides the greatest expected reduction of explanatory uncertainty?

Is the current research tree missing an important branch?

---

# Expected Review Output

The preferred review format is:

1.

Confirmed constraints.

2.

Weak constraints requiring revision.

3.

Overstated conclusions.

4.

Missing alternative explanations.

5.

Missing literature.

6.

Missing experiments.

7.

Recommended ontology revisions.

8.

Recommended methodological revisions.

9.

Recommended changes to future research program.

The objective of the review is not agreement.

The objective is to maximize the probability of finding errors before additional experiments are performed.

---
```
