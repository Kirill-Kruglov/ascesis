# research/Substrate_Discovery_v1/05_candidate_triage_matrix.md

```markdown
# Candidate Triage Matrix

## Status

Analytical synthesis.

This document combines:

- extracted knowledge from the Justitia investigation;
- literature survey;
- candidate axes;
- triage framework.

Its purpose is not to rank ideas.

Its purpose is to estimate where the next unit of research effort
should be invested.

Priority is determined by:

> Expected information gain per unit research effort.

---

# Triage Dimensions

Every candidate class is evaluated along six dimensions.

## K1

Analytical falsifiability

Can a major hypothesis about this class
be attacked without implementation?

High / Medium / Low

---

## K2

Minimal prototype cost

How expensive is the smallest meaningful implementation?

Low / Medium / High

---

## K3

Verification quality

Can failures be externally checked?

Low / Medium / High

---

## K4

Expected transfer to Door-1

If successful,

how directly would this class support
the original Goal Anchor?

Low / Medium / High

---

## K5

Risk of proxy-world collapse

Can the learner succeed
by modelling descriptions
instead of the environment?

Low / Medium / High

Lower is better.

---

## K6

Expected information gain

If the class fails,

how much will we learn?

Low / Medium / High

---

# Matrix

| Candidate Class | K1 | K2 | K3 | K4 | K5 | K6 | Preliminary Priority |
|-----------------|----|----|----|----|----|----|----------------------|
| Program synthesis worlds | High | Low | High | High | Low | High | Immediate |
| Formal proof worlds | High | Low | Very High | Medium | Very Low | Medium | Immediate |
| Physics executable toy worlds | Medium | Medium | High | High | Low | High | High |
| Causal intervention worlds | Medium | Medium | Medium | High | Medium | High | High |
| Artificial life | Low | High | Low | Medium | Medium | Medium | Deferred |
| Developmental robotics | Low | Very High | Low | High | Low | Medium | Deferred |
| Active inference frameworks | High | Low | Medium | Medium | Medium | Medium | Research only |

---

# Candidate Notes

## Program synthesis worlds

Advantages

- executable laws;
- intervention;
- exact feedback;
- compositionality;
- external verification.

Main unknown

Can executable programs become genuine environments
rather than isolated tasks?

Cheapest kill-gate

Construct a tiny self-contained executable world
whose laws are programs.

Determine whether an agent derives reusable world structure
or merely memorises program syntax.

Expected cost

Low.

Information gain

Very high.

---

## Formal proof worlds

Advantages

- strongest auditability;
- explicit derivation;
- no ambiguity.

Main unknown

Does theorem proving produce
world models
or only proof strategies?

Cheapest kill-gate

Construct intervention tasks
inside a proof environment.

If behaviour remains purely symbolic,
Door-1 relevance decreases.

---

## Physics toy worlds

Advantages

- lawful;
- causal;
- intervention;
- compact.

Main unknown

Can richness emerge
without losing verification?

Cheapest kill-gate

Measure whether compositional physical rules
produce reusable abstractions
beyond simple prediction.

---

## Causal intervention worlds

Advantages

- close to Goal Anchor;
- counterfactuals are native.

Main unknown

Do current causal benchmarks
capture environments
or merely annotated datasets?

Cheapest kill-gate

Replace labels
with generated interventions.

Measure whether causal structure
must still be inferred.

---

## Artificial life

Advantages

- emergence;
- open-endedness.

Known warning

Justitia belongs near this region.

Expected wall

trajectory dependence

verification

semantic drift

Priority

Low until a convincing analytical distinction
from Justitia exists.

---

## Developmental robotics

Advantages

excellent interaction.

Expected wall

engineering complexity.

Recommendation

Search for abstract formal analogues
before physical implementations.

---

## Active inference

Treat as

framework

rather than

candidate substrate.

Question

Can active inference
generate substrate design principles?

---

# Pareto Frontier

Current provisional frontier:

1.

Program synthesis worlds

2.

Physics executable worlds

3.

Causal executable worlds

These classes simultaneously score:

- high auditability;
- strong intervention;
- lawful dynamics;
- manageable prototype cost.

---

# Dominated Regions

The following appear currently dominated.

Pure internet-text environments.

Reason

High proxy-world risk.

---

Large unconstrained ALife.

Reason

Lower verification
than executable worlds,
with similar emergence.

---

Full robotics.

Reason

Much higher implementation cost
than executable simulators.

---

# Immediate Research Queue

Priority 1

Program synthesis worlds.

Reason

Maximum expected information gain
per unit effort.

---

Priority 2

Executable physics worlds.

Reason

Strong causal grounding.

---

Priority 3

Executable causal environments.

Reason

Natural intervention structure.

---

# First Kill-Gates

Instead of building large systems,
perform the following sequence.

G1

Can a program-generated world
produce reusable world models?

↓

G2

Can a physics-rule world
remain auditable
while increasing complexity?

↓

G3

Can causal intervention worlds
avoid collapsing
into labelled datasets?

Only if a class survives
its own kill-gate
should a full research programme begin.

---

# Final Observation

The Justitia investigation changed
the optimisation target.

The objective is no longer

"find an interesting environment."

The objective is

"find the environment class
with the highest expected scientific information gain
under disciplined falsification."

This document should be treated
as the current research roadmap,
not as a ranking of ideas.
```
