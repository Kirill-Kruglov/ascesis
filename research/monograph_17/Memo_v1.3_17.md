# Memo v1.3 — Current State

Status

Analytical checkpoint after Experiment 17A.

This memo supersedes v1.2.

Its purpose is

not

to summarize experiments,

but

to record

what is now known,

what has been rejected,

and

where the remaining uncertainty lives.

---

# 0. Original Goal

The project has never changed its objective.

Goal:

Construct a finite presentation

that generates

an arbitrarily large

internally derivable

training substrate

for reasoning.

Knowledge should be

derived,

not statistically generalized.

Everything else
(Sanskrit,
proof systems,
rewrite systems,
world generators)

is implementation.

---

# 1. What has survived

The following statements are currently accepted.

---

## A

Internet corpora

encode statistical regularities.

This motivates the project.

Status

Accepted.

---

## B

Large state spaces

do not imply

large reasoning spaces.

(WorldCore)

Status

Accepted.

---

## C

Infinite syntax

does not imply

infinite semantics.

(System C)

Status

Accepted.

---

## D

Feature relations

are poor semantic proxies.

Experiment 16.

Status

Accepted.

---

## E

Consequence relations

carry information

that features do not.

Experiment 16.

Status

Accepted.

---

# 2. What has been rejected

---

## Strong H2

Meaning

=

globally forced consequence class.

Experiment 17A rejects

the strong interpretation.

Most consequence classes

break under adversarial attacks.

Status

Rejected.

---

## Universal Backbone

Experiment 17 suggested

all classes were frozen.

Experiment 17A demonstrated

this was caused

by weak perturbation operators.

Status

Rejected.

---

# 3. The important remaining fact

Although

strong H2

was rejected,

not everything disappeared.

Result

108

classes

survived

adversarial attacks.

These surviving classes

are now

the primary object

of study.

The question is no longer

"Does backbone exist?"

The question is

"Why these classes?"

---

# 4. New ambiguity

Experiment 17A introduced

an ambiguity

that did not previously exist.

There are two fundamentally different kinds of perturbation.

---

Type I

Representation-preserving

Examples

alpha-renaming

mediator expansion

path refinement

graph isomorphism

These may preserve

the same underlying theory.

---

Type II

Theory-changing

Examples

merge nodes

reverse causality

delete causal chain

branch swap

These change

the theory itself.

---

Experiment 17A

did not distinguish

between them.

Therefore

its negative result

cannot yet be interpreted uniquely.

---

# 5. Competing explanations

## H2a

Backbone

is weak.

Most consequence classes

are genuinely fragile.

---

## H2b

Backbone

is invariant only

under semantics-preserving transformations.

Experiment 17A

attacked

the theory,

not merely

its representation.

Current evidence

does not distinguish

between H2a

and

H2b.

---

# 6. Current research question

The project

is no longer asking

"What is meaning?"

It asks

"What transformations preserve meaning?"

This is a much more precise question.

---

# 7. Analytical consequences

The project now naturally touches

Model Theory

Universal Algebra

Category Theory

Bisimulation

Graph Isomorphism

Constraint Satisfaction

SAT Backbone

Residual Finiteness

not because these fields are goals,

but because they study

representation-independent invariants.

---

# 8. Immediate next experiment

Experiment 17A.2

must classify

perturbations.

Only then

can Model Backbone (17B)

be interpreted correctly.

---

# 9. Current confidence

Established

★★★★★

feature ≠ consequence

proof algebra matters

representation matters

adversarial testing works

Strongly supported

★★★★☆

consequence carries genuine semantic signal

Open

★★★☆☆

meaning survives semantics-preserving transformations

Weak

★★☆☆☆

meaning = globally forced consequence class

Unknown

★

whether nontrivial backbone exists after perturbation taxonomy.

---

# 10. Principle

Continue searching

for the boundary.

Do not optimize

inside

already rejected hypotheses.

Every experiment

must attempt

to destroy

the current leading hypothesis.

Only hypotheses

that survive repeated falsification

should move forward.
