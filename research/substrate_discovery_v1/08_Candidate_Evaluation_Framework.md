# research/Substrate_Discovery_v1/08_Candidate_Evaluation_Framework.md

```markdown
# Candidate Evaluation Framework

## Status

Methodological framework.

This document defines how future substrate classes
will be evaluated.

The framework intentionally avoids ranking
individual implementations.

Instead,

it evaluates substrate families
according to the analytical requirements
developed in previous chapters.

---

# Motivation

Historically,

candidate environments
were evaluated independently.

This made comparison difficult.

The present framework introduces
a common evaluation procedure.

Every future substrate
should be analysed
using the same criteria.

---

# Principle

The objective
is not to identify
the best candidate.

The objective
is to progressively eliminate
entire classes
that fail
necessary analytical requirements.

---

# Evaluation Levels

Evaluation proceeds
from abstract
to concrete.

Level A

Computational Class

↓

Level B

Necessary Properties

↓

Level C

Interaction Geometry

↓

Level D

Expected Information Gain

↓

Level E

Implementation Feasibility

↓

Level F

Experimental Priority

---

# Stage A

Computational Classification

Question

Which computational family
does this candidate belong to?

Examples

- deterministic dynamics

- lawful stochastic dynamics

- executable programs

- theorem proving

- hybrid systems

- evolutionary systems

- multi-agent systems

Purpose

Locate the candidate
within the computational landscape.

---

# Stage B

Necessary Property Projection

Evaluate

Lawful Structure

Intervention

Counterfactual Richness

Compositionality

Auditability

Model Advantage

Lawful Stochasticity

Explorable Complexity

Stable Intervention Semantics

Proxy Resistance

Progressive Discoverability

Information Gain

The objective
is not precise scoring.

The objective
is identifying
obvious weaknesses.

---

# Stage C

Interaction Geometry

Questions

Can the learner

intervene?

observe consequences?

repeat experiments?

construct counterfactuals?

accumulate reusable knowledge?

Interaction
is evaluated independently
of computational complexity.

---

# Stage D

Expected Information Gain

Estimate

What would be learned
if this candidate fails?

Possible outcomes

New theorem.

New boundary.

New constraint.

New benchmark.

New methodology.

Search-space reduction.

Candidates
with low transferable knowledge
receive lower priority.

---

# Stage E

Implementation Feasibility

Estimate

Implementation cost.

Experimental complexity.

Required engineering.

Required computational resources.

Availability
of existing simulators.

Analytical understanding.

Expensive implementation
without analytical value
receives low priority.

---

# Stage F

Experimental Priority

Combine

Analytical importance.

Expected information gain.

Implementation cost.

Candidate maturity.

Literature coverage.

Result

Priority

High

Medium

Low

Deferred

---

# Candidate Comparison

Comparison
should never rely solely upon

performance.

Instead,

compare

analytical properties,

expected information gain,

and

transferability.

Performance
is considered
only after
analytical survival.

---

# Candidate Elimination

Candidates
may be rejected

before implementation

if

analytical contradictions
are sufficient.

Such rejection
is considered
a successful outcome.

---

# Living Evaluation

The framework
is intentionally dynamic.

Discovery
of new necessary properties

changes

future evaluations.

Candidate scores
are therefore

expected to evolve.

This behaviour
is desirable.

---

# Relation to Previous Programmes

Justitia

evaluated
one implementation.

The present framework

evaluates

families.

This distinction
greatly increases
knowledge transfer.

---

# Research Ledger

Every completed evaluation
should generate

Candidate Summary

↓

Analytical Assessment

↓

Open Questions

↓

Kill-Gates

↓

Decision

↓

Expected Future Value

The decision
must always
be reproducible.

---

# Candidate Kill-Gates

CF-1

Does the candidate
violate
a known necessary property?

↓

Reject.

---

CF-2

Does the candidate
offer
little transferable knowledge?

↓

Lower priority.

---

CF-3

Can another candidate
answer
the same analytical question
more cheaply?

↓

Postpone.

---

CF-4

Does implementation
precede analytical understanding?

↓

Stop.

Return
to analysis.

---

CF-5

Has the evaluation
become implementation-driven
rather than question-driven?

↓

Return
to the Goal Anchor.

---

# Summary

The Candidate Evaluation Framework
transforms substrate selection

from

engineering preference

into

analytical comparison.

Future candidates
should no longer compete
through intuition,

but

through
their ability
to survive
a common analytical procedure.
```
