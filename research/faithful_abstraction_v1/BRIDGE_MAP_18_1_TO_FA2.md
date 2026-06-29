# Bridge Map
## From 18.1 to Faithful Abstraction

## Status

Research trajectory.

This document does not introduce new hypotheses.

Its purpose is to reconstruct the actual decision process that transformed
the project from the 18-series into the Faithful Abstraction program.

Every transition must be justified by an empirical result.

Every branch records:

- question,
- experiment,
- result,
- decision,
- surviving hypothesis.

This document should allow an independent researcher to replay the reasoning
without relying on historical conversation.

---

# Original Objective

The original project objective (meme v1.1–v1.4) remained unchanged throughout
this sequence.

The objective was **not**:

> to develop a general theory of abstraction.

The objective was:

> to construct an analytically understandable and safety-faithful substrate
> suitable for future LLM training.

Justitia was developed as one candidate substrate.

Therefore every intermediate investigation must ultimately justify its value
relative to this objective.

This constraint is called the Goal Anchor.

---

# Stage 0

## Question

Can a compact analytical shield abstraction faithfully separate SAFE from
future collapse?

Experiment:

18.1

---

## Result

[FACT]

The predefined kill-gate failed.

Projection produced false-safe states.

More importantly,

many projected SAFE states already belonged to the concrete collapse basin.

---

## Surviving interpretation

Projection blindness exists.

---

## Eliminated interpretation

The current abstraction is already faithful.

---

## Goal relevance

High.

Without faithful abstraction,

the original project objective cannot be achieved.

---

# Stage 1

## Question

Why did the projection fail?

Possible explanations:

A.

One dominant monotonicity-breaking mechanism.

B.

Interaction of several mechanisms.

C.

Projection-level error.

---

Experiment

BA1

---

## Result

[FACT]

No clean single-mechanism ablation repaired fidelity.

Only MB4 appeared dominant,

but MB4 destroyed the original semantics.

---

## Decision

Reject explanation A.

Keep B and C.

---

# Stage 2

## Question

Perhaps complexity itself is required for semantic fidelity?

Experiment

BA2

---

## Result

[FACT]

Benefit and structural cost were poorly aligned.

Some expensive mechanisms contributed little observable fidelity.

---

## Decision

Reject

"all complexity is necessary."

---

# Stage 3

## Question

Can poor mechanisms simply be replaced?

Experiment

BA3

---

## Result

[FACT]

MB5 split into multiple functional components.

Transition behaviour and reporting behaviour separated.

---

## Decision

Mechanism taxonomy is too coarse.

Mechanisms are not necessarily atomic.

---

# Stage 4

## Question

Why did MB5 appear non-atomic?

Experiment

BA4

---

## Result

[FACT]

Static audit revealed semantic layer mixing.

Some variables simultaneously played:

- dynamics roles,
- policy roles,
- projection roles,
- reporting roles.

---

## Decision

Mechanism replacement alone is insufficient.

Layer discipline becomes necessary.

---

## Surviving hypothesis

Projection may fail because semantically different information was merged.

---

# Stage 5

## Research Pivot

At this point,

the project changed the immediate research question.

Old question:

How do we repair this abstraction?

↓

New question:

What information must every faithful abstraction preserve?

Important:

This is **not** a change of project goal.

It is a temporary change of research object motivated by the previous failures.

Goal Anchor remains unchanged.

---

# Stage 6

## Question

Do false-safe witnesses exhibit semantic structure?

Experiment

FA1

---

## Result

[FACT]

5839 false-safe witnesses.

History/control-related classes dominated.

Forward dynamics formed another large class.

Unknown/mixed remained small.

---

## Decision

Witness population is structured.

Refinement should be guided by witness classes rather than arbitrary feature
selection.

---

## Surviving hypothesis

Missing information may be more useful than missing raw variables.

Status:

Hypothesis.

Not yet established.

---

# Stage 7

## Question

Can witness classes be explained using a compact family of candidate
information invariants?

Experiment

FA2

---

## Result

[FACT]

Compact invariant families explain almost all witness classes.

However,

only false-safe witnesses were analysed.

No ordinary SAFE states were included.

---

## Decision

Compression demonstrated.

Discrimination NOT demonstrated.

---

## Critical consequence

The following claim is unsupported:

"Compact refinement exists."

Only the weaker claim survives:

"Compact witness compression exists."

---

# Current Position

The project currently stands here.

```
Original Goal

↓

Need faithful abstraction

↓

18.1

↓

Projection blindness

↓

BA

↓

Mechanism-level explanations weakened

↓

Layer discipline introduced

↓

FA1

↓

Witness structure

↓

FA2

↓

Compression observed

↓

???

Discrimination
```

The next transition has not yet been justified.

---

# Existing Kill-Gates

The project has accumulated several successful kill-gates.

## KG-1

18.1

Question:

Does the abstraction remain faithful?

Result:

No.

Program continued.

---

## KG-2

BA1

Question:

Is one mechanism responsible?

Result:

No.

---

## KG-3

BA2

Question:

Is complexity automatically justified?

Result:

No.

---

## KG-4

BA3

Question:

Is MB5 an atomic mechanism?

Result:

No.

---

## KG-5

BA4

Question:

Can reporting variables be treated as transition mechanisms?

Result:

No.

---

## KG-6

FA2

Question:

Has constructive refinement already been demonstrated?

Result:

No.

Compression ≠ discrimination.

---

# Future Kill-Gates

These kill-gates are mandatory before the FA program can claim success.

---

## FA2.5

Question

Do compact invariants discriminate false-safe from ordinary SAFE?

Required data

False-safe

+

True SAFE

Metrics

Precision

Recall

ROC

False-positive rate

Possible outcomes

PASS

Compact discrimination exists.

FAIL

Witness compression was insufficient.

---

## FA3

Question

Is H_FA1 genuinely different from standard CEGAR refinement?

Required comparison

Variable refinement

vs

Predicate refinement

vs

Information-invariant refinement

If no measurable distinction exists,

H_FA1 should be rejected or reformulated.

---

## FA4

Question

Does witness taxonomy generalise beyond Justitia?

Candidate substrates

Alternative collapse environments.

Possible outcomes

Transfer

↓

supports abstraction-level interpretation.

Failure

↓

supports Justitia-specific interpretation.

---

# Exit Criteria

The Faithful Abstraction program exists only because it serves the Goal Anchor.

Therefore the FA program must terminate if any of the following become true.

1.

FA2.5 demonstrates poor discrimination.

2.

Standard CEGAR fully explains all observations.

3.

Witness taxonomy fails to transfer.

4.

Layer discipline provides no measurable benefit.

5.

No path from FA back to the original project objective can be articulated.

---

# Final Position

The Faithful Abstraction program should not be interpreted as a replacement
for the original project.

It is a constrained exploratory branch.

Its sole justification is the possibility that understanding faithful
abstraction construction is a necessary intermediate step toward building an
analytically understandable and safety-faithful substrate.

If future experiments fail to support that proposition,

the FA program should be closed.
