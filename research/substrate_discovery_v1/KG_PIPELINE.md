# KG_PIPELINE — Programme Gate Pipeline

**Status:** Draft

**Depends on:**
- KG_SPEC.md
- PR1_programme_revision.md

---

# Purpose

This document defines the dependency structure of the Programme Gates.

Unlike a checklist, Programme Gates form a directed acyclic graph (DAG).

Each gate exists because an earlier gate leaves a question unresolved.

The purpose of the pipeline is to ensure that research proceeds only after
its prerequisites have survived independent scrutiny.

---

# Pipeline Overview

```
                 External Review
                        │
                        ▼
                     KG0 Review
                        │
                        ▼
             PR1 Programme Revision
                        │
                        ▼
        KG1 Goal Anchor Identity Gate
                        │
                        ▼
        KG2 Derivability Reduction Gate
                        │
                        ▼
   KG3 Internal Model Operationalization
             │                     │
             │                     ▼
             │          KG5 Necessity Audit
             │
             ▼
 KG4 Proxy-World Demonstration Gate
             │
             ▼
 KG6 Prior-Art Reduction Gate
             │
             ▼
 Candidate Substrate Evaluation
             │
             ▼
 Experimental Programme
```

---

# KG0

## Purpose

Evaluate external criticism.

## Inputs

- External review
- Existing programme

## Outputs

- Accepted criticisms
- Rejected criticisms
- Programme Freeze

## Decision

Already completed.

---

# PR1

## Purpose

Apply explicit programme patch.

## Inputs

- KG0

## Outputs

- Revised programme

## Decision

Already completed.

---

# KG1

## Name

Goal Anchor Identity Gate

---

## Question

Does the current Substrate Discovery programme still address
the original research objective?

---

## Required Evidence

- Goal formulation
- Bridge documents
- Door1 extracted knowledge
- Explicit necessity argument

---

## Failure

If the bridge cannot be established,

Substrate Discovery becomes an independent programme,

rather than the continuation of the original one.

---

## Success

The bridge is explicitly demonstrated.

---

# KG2

## Name

Derivability Reduction Gate

---

## Question

Can "Derivability" be reduced to existing theory?

---

## Competing Explanations

- Active Learning
- System Identification
- Model-Based RL
- Predictive Processing
- Computational Mechanics
- Algorithmic Statistics
- CEGAR
- Others

---

## Failure

No measurable distinction exists.

---

## Success

A measurable distinction survives reduction.

---

# KG3

## Name

Internal Model Operationalization Gate

---

## Question

Can an internal model be measured independently
of linguistic behaviour?

---

## Required Output

Operational definition.

Observable quantities.

Candidate measurements.

---

## Failure

Internal Model remains intuitive only.

---

## Success

Independent operationalization exists.

---

# KG4

## Name

Proxy-World Demonstration Gate

---

## Question

Can a minimal computational environment demonstrate
the central claims of the programme?

---

## Required Output

Small toy environment.

Observable learning.

Derivable structure.

Independent replication.

---

## Failure

No measurable demonstration exists.

---

## Success

The toy world exhibits the expected behaviour.

---

# KG5

## Name

Necessity Audit

---

## Question

Which proposed properties are actually necessary?

---

## Input

Candidate property list.

---

## Output

Each property classified as:

- Necessary
- Desideratum
- Incidental
- Rejected

---

## Dependency

Requires KG3.

---

# KG6

## Name

Prior-Art Reduction Gate

---

## Question

After all previous gates,

what remains genuinely novel?

---

## Failure

Everything reduces to prior literature.

---

## Success

Residual explanatory contribution remains.

---

# Dependency Rules

Dependencies are mandatory.

A gate may not begin until every upstream dependency
has completed.

The dependency graph must remain acyclic.

---

# Programme State Machine

```
Draft

↓

External Review

↓

KG Review

↓

Programme Revision

↓

Gate

↓

Revision

↓

Next Gate

↓

Candidate Evaluation

↓

Experimental Programme
```

---

# Evidence Flow

Evidence always flows downward.

```
Experiment

↓

Knowledge Extraction

↓

Programme

↓

Programme Gate

↓

Programme Revision

↓

Next Gate
```

No evidence may skip intermediate stages.

---

# Exit Criteria

The pipeline terminates when one of the following occurs.

## A

The programme survives all gates.

Research proceeds to substrate construction.

---

## B

One gate rejects the programme.

Research terminates.

---

## C

The programme splits.

A descendant programme is created.

The relationship between parent and child
must be explicitly documented.

---

# Meta Principle

Programme Gates exist to make continuation
more difficult than abandonment.

A research programme should continue only when
surviving criticism is harder than generating new ideas.

---

# Current Status

| Gate | Status |
|-------|--------|
| KG0 | Complete |
| PR1 | Complete |
| KG1 | Pending |
| KG2 | Pending |
| KG3 | Pending |
| KG4 | Pending |
| KG5 | Pending |
| KG6 | Pending |

---

# Next Gate

**KG1 — Goal Anchor Identity Gate**
