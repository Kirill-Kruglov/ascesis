# research/Door1_Extracted_Knowledge_v1.md

```markdown
# Door 1 — Extracted Knowledge

## Status

Research synthesis.

This document is not a project report.

It is an extraction of durable knowledge obtained during the Justitia
investigation.

The purpose is not to evaluate Justitia.

The purpose is to identify which observations should constrain every future
Door-1 substrate candidate.

Each statement is explicitly classified as:

- FACT
- INFERENCE
- HYPOTHESIS

Only FACT and directly supported INFERENCE are intended to survive even if
Justitia is later abandoned.

---

# 1. Original Goal

The long-term objective has remained unchanged.

To construct an environment in which an LLM acquires an internal world model
through interaction with a lawful substrate rather than through statistical
generalisation over human-produced internet text.

Justitia was one candidate substrate.

The experiments below evaluate properties of that candidate.

---

# 2. Durable Experimental Results

## Result 1

### Projection blindness is a real failure mode.

FACT.

Experiment:

18.1

Evidence:

Projection merged states that were behaviourally different with respect to
future collapse.

Conclusion:

A compact abstraction may appear analytically correct while failing to preserve
the target behavioural property.

This is a general warning, not a Justitia-specific observation.

---

## Result 2

### Single-mechanism explanations are insufficient.

FACT.

BA1.

No clean monotonicity-breaking mechanism explained the observed failure.

Conclusion:

Behaviourally important errors may arise from interactions rather than
individual mechanisms.

---

## Result 3

### Structural complexity is not automatically justified.

FACT.

BA2.

Large structural cost may produce little semantic benefit.

Conclusion:

Complexity itself is not evidence of fidelity.

---

## Result 4

### Semantic layers matter.

FACT.

BA4.

Variables participating in transition dynamics, policy, observation and
reporting should not automatically be treated as equivalent.

Conclusion:

Safety-relevant abstractions require explicit layer discipline.

This lesson is expected to transfer beyond Justitia.

---

## Result 5

### False-safe witnesses possess reproducible structure.

FACT.

FA1.

Witnesses were not randomly distributed.

Most belonged to a small number of recurring classes.

Interpretation:

Failure analysis should begin with witness populations rather than isolated
counterexamples.

---

## Result 6

### Compression is weaker than discrimination.

FACT.

FA2 + FA2.5.

Compact descriptions of witness populations exist.

However,

those descriptions failed to produce a discriminative abstraction candidate.

Conclusion:

Compression alone should never be interpreted as constructive progress.

---

## Result 7

### Standard CEGAR produced a conservative but practically vacuous boundary.

FACT.

JB0.

False-safe decreased substantially.

False-positive rate became too large for practical usefulness.

Conclusion:

Conservative correctness alone is insufficient.

Practical usefulness must remain an explicit optimisation objective.

---

# 3. What Has Been Closed

The following research directions have now been experimentally closed for
Justitia.

Closed:

A.

Compact faithful abstraction superior to standard history refinement.

Reason:

FA2.5.

---

B.

Immediate standard CEGAR path toward a useful analytical boundary.

Reason:

JB0.

---

These are negative results.

Negative results reduce future search space.

---

# 4. What Has NOT Been Closed

The following statements remain unknown.

Unknown:

Whether another abstraction family exists.

Whether another verification framework is more appropriate.

Whether Justitia fails only because of path dependence.

Whether another substrate could satisfy the original Door-1 objective.

Whether the Door-1 objective itself is achievable.

These remain legitimate research questions.

---

# 5. Emerging Design Constraints

Future substrate candidates should be evaluated against the following checklist.

Candidate properties.

□ Behaviourally faithful abstraction appears possible.

□ Safety boundary is not purely trajectory-dependent.

□ Useful conservative boundaries do not become vacuous.

□ Layer discipline is naturally expressible.

□ Counterexamples admit meaningful decomposition.

□ Verification cost grows controllably.

This checklist is empirical.

It was not assumed before the Justitia investigation.

---

# 6. Important Distinction

The experiments falsified several implementation paths.

They did NOT falsify the original objective.

Failure of one candidate substrate should not be interpreted as failure of the
research programme.

The programme concerns environments capable of supporting derived world models.

Justitia was only one attempt.

---

# 7. New Starting Point

The next stage should begin from these extracted constraints rather than from
the internal structure of Justitia.

Future exploration should therefore ask:

Which kinds of environments naturally satisfy these constraints?

rather than

How can Justitia be repaired?

This marks the end of the current investigation and the beginning of a new
search space.
```
