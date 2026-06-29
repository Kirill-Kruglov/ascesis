# ASCESIS_Research_Methodology_v2.md

## Lines 1–228

```markdown
# ASCESIS Research Methodology
## Version 2.0
### Methodological Foundations of the Experimental Program

---

# Purpose of This Document

This document defines the methodological framework used throughout the ASCESIS research program.

Unlike the Research Ontology, which describes the current epistemic state of the project, this document specifies how knowledge is generated, evaluated, revised, and incorporated into the ontology.

Its purpose is to make every methodological decision explicit and independently auditable.

A reader should be able to determine not only what was concluded, but also why each experiment was designed, why particular alternatives were rejected, and under which conditions every conclusion should be considered invalid.

The methodology intentionally separates observations from interpretation. Every conclusion appearing elsewhere in the project should be reproducible from the evidence chain documented here.

---

# 1. Research Objective

The ASCESIS project investigates whether semantic organization can emerge from purely formal generative systems without relying on statistical language models, external semantic labels, pretrained embeddings, or human annotation.

The project does not attempt to model human language directly.

Instead, it investigates the structural conditions under which internally meaningful organization might become inevitable inside finite formal systems.

Consequently, the project is not organized around prediction accuracy.

Its primary objective is constraint discovery.

---

# 2. Fundamental Research Strategy

The central methodological principle is falsification-first research.

Each experiment is designed primarily as an attempt to invalidate the strongest currently available explanation.

Positive results are considered provisional.

Negative results are considered reductions of the admissible hypothesis space.

This choice reflects the observation that many apparently successful semantic theories can explain positive evidence, whereas comparatively few survive carefully constructed counterexamples.

Accordingly, the project measures progress primarily by the elimination of explanatory alternatives rather than by accumulation of supporting evidence.

---

# 3. Epistemic Model

Throughout the project five epistemic categories are distinguished.

## 3.1 Observation

An observation is a directly measured property of an experiment.

Examples include measured survival fractions, correlation coefficients, PCA reconstruction accuracy, attack costs, or counts of consequence classes.

Observations contain no interpretation.

---

## 3.2 Experimental Constraint

A constraint is an observation that has survived repeated attempts at falsification.

Constraints define the current boundary of admissible explanation.

Constraints are treated as project knowledge until experimentally revised.

---

## 3.3 Interpretation

Interpretations explain observations.

Interpretations remain provisional.

Multiple competing interpretations may coexist.

Interpretations never automatically become constraints.

---

## 3.4 Working Hypothesis

A working hypothesis proposes an explanatory mechanism.

Its primary value is that it produces experimentally distinguishable predictions.

A hypothesis is not retained because it is plausible.

It is retained only while it remains useful for designing stronger falsification experiments.

---

## 3.5 Open Question

An open question represents uncertainty that has survived the current experimental program.

Open questions determine future experiments.

---

# 4. Principle of Traceability

Every nontrivial statement appearing anywhere in the project must be traceable to explicit evidence.

The evidence chain has the following structure.

Statement

↓

Supporting Experiment(s)

↓

Measured Quantities

↓

Computational Artifacts

↓

Inference

↓

Remaining Alternative Explanations

A statement that cannot be traced through this chain must not appear as established knowledge.

Instead it must be labeled either as interpretation or hypothesis.

---

# 5. Evidence Classification

The project distinguishes several evidence classes.

## E — Experimental

Results produced directly by completed experiments.

Examples:

17A.2

17C

17D

17E

17F

---

## C — Computational

Derived numerical results.

Examples include:

correlation matrices,

PCA,

AUC,

reconstruction accuracy,

bootstrap estimates,

attack costs.

Computational evidence supports interpretation but does not replace experimental evidence.

---

## T — Theoretical

Logical derivations or mathematical proofs.

Theoretical results remain valid independently of implementation.

No current ASCESIS result belongs exclusively to this class.

---

## L — Literature

External publications used for comparison.

Literature is never treated as proof of an ASCESIS hypothesis.

Instead it identifies similar structural phenomena and competing explanations.

---

## O — Observation

Raw empirical facts not yet incorporated into explanatory models.

---

## H — Hypothesis

Untested explanatory proposal.

---

# 6. Why Synthetic Substrates

The project deliberately avoids natural language corpora.

Natural language simultaneously contains:

semantic structure,

statistical regularities,

historical artifacts,

human conventions,

and unknown latent variables.

Consequently, positive results obtained from natural language rarely isolate the mechanism responsible for observed behaviour.

Synthetic substrates provide complete control over:

generation process,

perturbation process,

consequence extraction,

and evaluation.

This allows semantic hypotheses to be attacked under controlled conditions.

---

# 7. Why External Knowledge Is Excluded

The project intentionally excludes:

human semantic annotation,

internet knowledge,

knowledge graphs,

pretrained embeddings,

large language models,

reinforcement learning from human feedback,

manual class importance.

The purpose of these exclusions is methodological rather than ideological.

External knowledge introduces explanatory variables that cannot be independently controlled.

Once external semantic information enters the system, it becomes impossible to determine whether observed organization emerged internally or was imported implicitly.

Therefore every completed experiment measures only internally generated structure.

---

# 8. Why Internal Metrics

All metric families are constructed exclusively from quantities derivable inside the investigated substrate.

Typical examples include:

operator reuse,

derivational participation,

graph diversity,

expression depth,

perturbation participation,

intervention effects,

frequency,

compression,

centrality.

The project intentionally avoids metrics requiring external interpretation.

This restriction ensures that every measured quantity is reproducible from the substrate itself.

---

# 9. Why Multiple Independent Metrics

The earliest experiments relied upon relatively small numbers of composite metrics.

Experiment 17D demonstrated that this approach was insufficient.

Different metric constructions produced different classifications.

Consequently, every important latent quantity is now evaluated through multiple independent observable families.

Agreement between independent observables is treated as stronger evidence than success of any individual metric.

Disagreement triggers additional falsification experiments rather than metric selection.

---

# 10. Principle of Metric Independence

Metric families should measure different structural properties whenever possible.

Two metrics that differ only algebraically but encode identical information should not be considered independent evidence.

Whenever high correlation is observed, experiments should determine whether:

the metrics measure one latent variable,

one metric is a trivial transformation of another,

or both depend on a shared hidden factor.

Experiment 17E was introduced specifically to investigate this question.

---

# 11. Perturbation Philosophy

Perturbations are treated as experimental interventions rather than random noise.

Every perturbation family represents an explicit hypothesis concerning which structural changes should preserve semantic identity.

The distinction introduced in Experiment 17A.2 between representation-preserving perturbations and theory-changing perturbations became a permanent methodological principle.

Future perturbation classes must therefore specify which theoretical assumptions they preserve and which they intentionally violate.

```
