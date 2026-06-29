# research/Substrate_Discovery_v1/02_candidate_axes.md

````markdown
# Candidate Space — Evaluation Axes

## Status

Analytical framework.

This document does not evaluate any existing substrate.

It defines the coordinate system in which future substrate candidates
will be compared.

The axes below are extracted from:

- Door-1 investigation
- Justitia experiments
- BA/FA/JB series
- literature survey

The purpose is to reduce subjective judgement during future exploration.

---

# Principle

A substrate should not be judged by novelty.

It should be judged by where it lies inside the candidate space.

Every future candidate should therefore receive coordinates
along the following independent axes.

---

# Axis A

## Source of Structure

Question:

Where does regularity come from?

Possible values:

Human annotations
↓

Recorded trajectories

↓

Simulation rules

↓

Executable programs

↓

Mathematical laws

↓

Physical laws

Interpretation

The further downward,

the less the learner depends on human descriptions.

Preferred direction:

toward lawful executable structure.

---

# Axis B

## Derivability

Question

Can the learner derive internal structure
from interaction?

Scale

0

No derivation.
Pure memorisation.

↓

1

Weak statistical regularities.

↓

2

Predictive patterns.

↓

3

Stable causal mechanisms.

↓

4

Composable laws.

↓

5

General rule system.

Preferred direction:

high.

---

# Axis C

## Intervention

Question

Can the learner change the environment?

Scale

Passive observation

↓

Limited actions

↓

Closed-loop interaction

↓

Rich intervention

↓

Long-horizon manipulation

Preferred direction:

closed-loop interaction.

---

# Axis D

## Feedback Sharpness

Question

How clearly does the environment reject
incorrect world models?

Weak

↓

Delayed

↓

Local

↓

Immediate

↓

Law-constrained

Preferred direction:

clear lawful correction.

---

# Axis E

## Observability

Question

How much of the state is visible?

Fully observable

↓

Partially observable

↓

Hidden latent state

↓

Only consequences visible

Observation

Neither extreme is ideal.

Fully observable
reduces inference.

Completely hidden
creates ambiguity.

Preferred region:

moderate partial observability.

---

# Axis F

## Temporal Dependence

Question

How much of the future depends on trajectory
rather than current state?

State-based

↓

Finite history

↓

Bounded memory

↓

Long history

↓

Entire trajectory

Observation

Justitia suggests excessive trajectory dependence
creates verification problems.

Preferred region:

state
or
bounded history.

---

# Axis G

## Verification Tractability

Question

Can claims about the environment
be externally checked?

None

↓

Empirical only

↓

Simulation replay

↓

Executable proof

↓

Formal proof

Preferred direction:

toward executable verification.

---

# Axis H

## Layer Separation

Question

Can the following layers
be distinguished?

Dynamics

Observation

Control

Projection

Reporting

Scale

Entangled

↓

Mostly separated

↓

Explicitly separated

Preferred direction:

explicit separation.

---

# Axis I

## Counterexample Structure

Question

What do failures look like?

Random

↓

Many unique failures

↓

Small witness families

↓

Reusable witness taxonomy

↓

Minimal counterexamples

Preferred direction:

structured failures.

---

# Axis J

## Safety Boundary

Question

Does the environment admit
a useful safety boundary?

No boundary

↓

Only heuristic

↓

Conservative but vacuous

↓

Useful conservative

↓

Faithful boundary

Preferred direction:

useful conservative
or
faithful.

---

# Axis K

## Open-endedness

Question

Can complexity continue growing?

Finite tasks

↓

Large benchmark

↓

Procedural worlds

↓

Evolutionary worlds

↓

Open-ended dynamics

Observation

Unlimited complexity
is valuable
only if verification remains possible.

---

# Axis L

## Proxy Risk

Question

How easily can the learner succeed
by modelling humans
instead of the world?

Very high

↓

Medium

↓

Low

↓

Almost impossible

Preferred direction:

low.

---

# Candidate Coordinate

Every future substrate
should receive a vector:

```text
S =

(
A,
B,
C,
D,
E,
F,
G,
H,
I,
J,
K,
L
)
```

No single axis determines suitability.

The geometry of the vector matters.

---

# Dominated Candidates

A candidate is dominated
if another candidate
is no worse
on every axis
and strictly better
on at least one.

Dominated candidates
should normally not be pursued.

---

# Expected Regions

## Region 1

Internet-scale language corpora

High proxy

Weak intervention

Weak derivability

Strong scale

Not Door-1.

---

## Region 2

Formal theorem worlds

Excellent verification

Excellent derivability

Weak embodiment

Weak physical grounding.

Promising.

---

## Region 3

Program synthesis worlds

Executable

Interactive

Composable

Strong auditability.

Highly promising.

---

## Region 4

Physics toy worlds

Lawful

Interactive

Excellent derivability

Potentially insufficient richness.

Promising.

---

## Region 5

Artificial life

Rich

Open-ended

Weak verification

Possible Justitia-like path dependence.

Needs caution.

---

## Region 6

Developmental robotics

Excellent interaction

Excellent feedback

Weak verification

High engineering cost.

Research direction.

---

# Search Strategy

Do not optimise one axis.

Instead,

search for Pareto-optimal substrate families.

Candidates lying on the Pareto frontier
should receive detailed investigation.

Dominated candidates
should be discarded early.

---

# Immediate Next Document

03_candidate_landscape.md

The purpose will be
to place known substrate families
inside this coordinate system
and identify
the currently best unexplored regions.

````
