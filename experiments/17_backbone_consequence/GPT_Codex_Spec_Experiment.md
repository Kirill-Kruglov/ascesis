# Experiment 17 — Backbone Consequence

Project:

17_backbone_consequence

Status:

Door 1 analytical validation.

No LLMs.

No Sanskrit.

No new world generators.

Reuse Experiment 16 wherever possible.

---

# Objective

Experiment 16 established

feature ≠ consequence

AST ≠ consequence

and

consequence equivalence is derivable.

Experiment 17 tests the stronger hypothesis.

H2

Meaning

≠

consequence class

Meaning

=

globally forced consequence class.

Operational hypothesis

A consequence-equivalence relation is meaningful only if it survives
admissible perturbations of the generating theory.

---

# Research Question

Given

φ ≡ ψ

under the verifier,

how stable is this equivalence
under small perturbations
of the underlying causal theory?

---

# Guiding Principle

We are NOT measuring

number of equivalence classes.

We are measuring

necessity.

---

# Base System

Reuse the causal DAG generator
from Experiment 16.

Reuse the verifier unchanged.

Reuse all consequence signatures.

No semantic redesign.

---

# Perturbation Model

Implement admissible perturbations.

Minimum set:

P1

remove one edge

P2

add one edge
without creating cycles

P3

reverse one edge

P4

rename one internal variable
(alpha-equivalent control)

P5

replace one mediator node
with equivalent chain

Optional:

P6

edge probability perturbation
before DAG generation

---

# Perturbation Budget

Define

k

=

number of perturbation operations.

Evaluate

k ∈

0
1
2
3
4

---

# Backbone Definition

For every consequence-equivalent pair

(φ, ψ)

compute

Persistence(k)

=

fraction of admissible perturbations
of size k
for which

φ ≡ ψ

still holds.

---

# Global Necessity Score

Define

GNS

Global Necessity Score

for every equivalence class.

Example

GNS

=

weighted average

Persistence(1)

Persistence(2)

Persistence(3)

Persistence(4)

Codex may choose another monotone definition,
but must justify it.

---

# Frozen Consequence Classes

Define

Frozen

if

Persistence(k)

>

0.95

for every tested k.

Define

Weak

if

Persistence(1)

already drops below

0.5

Thresholds configurable.

---

# Required Outputs

For every consequence class report

class id

class size

GNS

Persistence curve

representative expressions

---

# Stability Spectrum

Produce histogram

number of classes

vs

Global Necessity Score.

Question:

Are there

many weak classes

few frozen classes

or

continuous spectrum?

---

# Collapse Test

Question

Do high-GNS classes
collapse into one giant trivial class?

If yes

H2 weakens.

If no

H2 strengthens.

---

# Diversity Test

Question

Are frozen classes
still structurally diverse?

Measure

expression depth

operator diversity

DAG diversity

inside each frozen class.

---

# Local vs Global

Measure

minimum perturbation

required

to destroy

equivalence.

If

single edge

breaks equivalence

class is local.

If

multiple coordinated perturbations

required

class is global.

---

# Backbone Coverage

Compute

fraction of all consequence classes
that are frozen.

Outputs

coverage

weighted coverage

coverage by depth

coverage by DAG size

---

# Random Baseline

Construct

random partitions

having

same class-size distribution.

Repeat perturbation analysis.

Expectation

random partitions
should have very low persistence.

---

# Feature Baseline

Repeat

Persistence analysis

using

feature equivalence.

Question

Does consequence relation
produce significantly more
high-GNS classes
than feature relation?

---

# AST Baseline

Repeat

Persistence

for AST identity.

Expectation

Persistence

≈

1

only for alpha-renaming.

Otherwise

low.

---

# Complexity Analysis

Measure

runtime

per perturbation

runtime

per class

runtime

vs DAG size

Estimate

whether

Global Necessity

appears tractable
for toy systems.

---

# Plots

Required

Persistence curves

GNS histogram

Coverage by depth

Coverage by DAG size

Frozen vs Weak scatter

Perturbation sensitivity matrix

---

# Decision Logic

Label

H2_supported

if

there exists

nontrivial

high-GNS

classes

that

remain diverse

and

are significantly stronger
than feature baseline.

---

Label

H2_not_supported

if

all consequence classes

are

fragile.

---

Label

Trivial_backbone

if

only

trivial tautological classes

survive.

---

Label

Instrumentation_failure

if

perturbation engine
cannot preserve verifier correctness.

---

# Required Summary

Answer explicitly.

1

Do frozen consequence classes exist?

2

Are they nontrivial?

3

How many?

4

Are they more stable than feature classes?

5

Are they more stable than AST identity?

6

Does stability correlate
with expression depth?

7

Does stability correlate
with consequence class size?

8

Should Global Necessity
replace

class cardinality

as the project's primary invariant?

---

# Kill Conditions

Kill H2 immediately if

all classes

become fragile
after one perturbation.

Kill Door 1 if

only trivial equivalences
remain frozen.

---

# README

Explain

why

Experiment 17

does NOT search
for better generators.

It validates

whether

Global Necessity

is a meaningful mathematical object.

---

# Expected Commands

pytest

python scripts/run_backbone_consequence.py \
    --seed 42 \
    --num-dags 500 \
    --max-depth 6

Large run

python scripts/run_backbone_consequence.py \
    --seed 42 \
    --num-dags 2000 \
    --max-depth 8
