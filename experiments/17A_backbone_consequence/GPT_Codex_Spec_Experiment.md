# Experiment 17A.1 — Adversarial Backbone Stress Test

Project

17A1_backbone_stress

Status

Critical falsification experiment.

Purpose

Attempt to falsify the result of Experiment 17.

Experiment 17 found

GNS = 1.0

for every analyzed consequence class.

This experiment assumes

that result is suspicious

until it survives adversarial testing.

The burden of proof is now on H2.

---

# Research Question

Are frozen consequence classes

intrinsically stable,

or

did Experiment 17 use perturbations
that were too weak?

---

# Principle

Experiment 17 sampled perturbations.

Experiment 17A.1

searches

for perturbations
that maximally destroy
consequence equivalence.

This is no longer random robustness.

It is adversarial robustness.

---

# Reuse

Reuse

Experiment 17

without modification whenever possible.

Reuse

generator

verifier

consequence signatures

class extraction

analysis pipeline.

---

# Important Rule

DO NOT strengthen
the verifier.

DO NOT redesign
the consequence relation.

The only object allowed to become stronger

is

the perturbation engine.

---

# Perturbation Families

Retain

P1
remove edge

P2
add edge

P3
reverse edge

P4
alpha rename

P5
mediator replacement

and add

---

P6

delete complete causal path

---

P7

replace causal chain

A→B→C

with

A→D→C

---

P8

merge two internal nodes

---

P9

split one node
into two mediators

---

P10

replace one subgraph
by another

with equal input/output interface

but different internal structure

---

P11

swap independent causal branches

---

P12

replace one implication
with alternative derivation

when possible.

---

# Coordinated Perturbations

Experiment 17

used

k

local perturbations.

Now search

coordinated perturbations.

Example

remove

three edges

that together
maximize verifier disagreement.

---

# Adversarial Search

Implement

greedy search.

For each consequence class

find

the perturbation sequence

that minimizes

Persistence.

Not random.

Optimization.

---

# Beam Search

Optional

beam width

8

16

32

Compare.

---

# Search Budget

Per class

maximum

100

candidate perturbation sequences.

Configurable.

---

# Early Exit

If

Persistence

reaches

0

stop searching.

Record

minimal successful attack.

---

# Attack Cost

For every broken class

report

minimum perturbation cost

required
to destroy equivalence.

Call this

Attack Cost.

---

# New Metric

Replace

binary frozen

with

Attack Curve.

Persistence

vs

attack budget.

---

# Global Necessity

Redefine

temporarily

as

area

under

Attack Curve.

Report both

old GNS

new GNS.

---

# Diversity

Measure

whether

high attack cost

correlates with

depth

operator diversity

DAG diversity

class size

---

# Alias Audit

Repeat

Experiment 17 alias audit.

Ensure

attacks

are not simply

breaking aliases.

---

# Cross-DAG Attack

New.

Take

equivalent expressions

from different DAGs.

Attempt

cross-theory attacks.

Question

Does stability survive

across independently generated theories?

---

# Verifier Audit

Important.

If

an attack

changes verifier output

because verifier itself
became inconsistent,

discard.

Only valid attacks count.

---

# Baselines

Repeat attacks for

feature classes

AST identity

random partitions.

---

Expectation

attack cost

consequence

>

AST

>

feature

>

random.

---

# Outputs

attack_cost.csv

attack_curve.csv

broken_classes.csv

minimal_attack_examples.json

cross_dag_attack.csv

alias_attack_report.json

summary.md

final_decision.json

---

# Plots

Attack curves

Attack-cost histogram

Persistence vs attack budget

Attack cost vs depth

Attack cost vs DAG diversity

Attack cost vs operator diversity

---

# Required Questions

1

Can any frozen class
be broken?

---

2

If yes

what is

minimum attack cost?

---

3

How many classes
remain frozen
under adversarial search?

---

4

Does a spectrum emerge?

---

5

Is GNS still constant?

---

6

Which perturbation family
is most destructive?

---

7

Do attacks mostly break

aliases

or

genuinely semantic classes?

---

8

Do cross-DAG attacks
behave differently?

---

# Decision Logic

Classification

Backbone_survives

if

>95%

of classes

remain frozen

under adversarial search.

---

Classification

Backbone_spectrum

if

wide attack-cost distribution emerges.

This is considered

a stronger scientific result

than GNS=1.

---

Classification

Weak_backbone

if

most classes
fail
under small attack cost.

---

Classification

Verifier_artifact

if

attacks mainly expose
implementation assumptions
rather than semantic failures.

---

# Kill Conditions

Kill H2

if

most consequence classes

fail

after low-cost adversarial attacks.

---

Reject Experiment 17

if

the previous GNS=1
was caused mainly
by weak perturbation operators.

---

# README

Explain clearly

why this experiment exists.

It is not

an improvement.

It is an attempt

to falsify

Experiment 17.

A successful falsification

is considered

a positive scientific outcome.

---

# Commands

pytest

python scripts/run_backbone_stress.py \
    --seed 42 \
    --num-dags 500 \
    --max-depth 6

Large

python scripts/run_backbone_stress.py \
    --seed 42 \
    --num-dags 2000 \
    --max-depth 8
