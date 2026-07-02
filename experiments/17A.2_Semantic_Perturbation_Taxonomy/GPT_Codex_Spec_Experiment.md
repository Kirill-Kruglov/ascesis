# Experiment 17A.2 — Semantic Perturbation Taxonomy

Project

17A2_semantic_taxonomy

Purpose

Resolve the ambiguity introduced by Experiment 17A.

Experiment 17A mixed

representation-preserving

and

theory-changing

perturbations.

This experiment separates them.

No new generators.

No verifier redesign.

Reuse Experiment 17A.

---

# Research Question

Does consequence backbone survive

semantics-preserving

transformations

while failing

only

under theory-changing transformations?

---

# Principle

We are NOT measuring

robustness.

We are measuring

what counts

as

"the same theory."

---

# Step 1

For every perturbation operator

classify it.

---

Class A

Representation preserving.

Candidate examples

alpha renaming

mediator expansion

path refinement

graph isomorphism

edge subdivision

equivalent proof refactoring

---

Class B

Theory changing.

Candidate examples

merge nodes

reverse causality

delete causal path

swap branches

replace implication

add independent cause

remove dependency

---

Codex

must justify

every classification.

---

# Step 2

Repeat Experiment 17A

using

only

Class A.

Report

Persistence

Attack Cost

AUC GNS

---

# Step 3

Repeat

using

only

Class B.

---

# Step 4

Compare.

Main question

Does backbone disappear

already

under Class A?

or

only

under Class B?

---

# Representation Audit

For every

Class A

operator

verify

that

semantic verifier

produces

equivalent world behaviour.

Reject

operators

that fail this audit.

---

# Outputs

taxonomy.csv

operator_classification.md

representation_only_summary.json

theory_change_summary.json

comparison.md

---

# Required Questions

1

Which perturbations

preserve representation?

2

Which perturbations

change the theory?

3

How many classes survive

Class A only?

4

How many survive

Class B only?

5

Does Experiment 17A remain valid

after this separation?

6

Should Global Necessity

be defined

relative to

representation-preserving transformations?

---

# Decision Logic

Classification

Representation_invariant

if

backbone survives

Class A

but not

Class B.

---

Classification

Weak_backbone

if

backbone fails

already

under Class A.

---

Classification

Taxonomy_failure

if

operators

cannot be cleanly separated.

---

# Kill Conditions

Reject

representation-invariant meaning

if

Class A

alone

destroys

most consequence classes.

---

# README

Explain

why

Experiment 17A

could not distinguish

representation

from

theory.

Experiment 17A.2

exists

solely

to resolve

that ambiguity.
