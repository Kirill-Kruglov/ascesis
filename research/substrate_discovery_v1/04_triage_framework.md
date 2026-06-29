# research/Substrate_Discovery_v1/04_triage_framework.md

# Substrate Triage Framework

## Status

Analytical framework.

This document defines a staged falsification procedure for future substrate
candidates.

It does not propose a substrate.

Its purpose is to avoid repeating the Justitia pattern:

1. choose a rich candidate;
2. build experiments around it;
3. discover late that a necessary property fails.

The new procedure attempts to eliminate unsuitable candidate classes as early
and cheaply as possible.

---

# 1. Goal Anchor

The long-term objective remains:

> Train LLM-like systems in environments where world-structure is derived from
> lawful interaction rather than statistically absorbed from human text.

Therefore a substrate candidate is not judged by novelty, richness or elegance.

It is judged by whether it can plausibly support derived internal world models.

---

# 2. Core Principle

The triage procedure is destructive.

It is designed to reject candidates.

A candidate that survives triage is not accepted.

It merely becomes worth deeper investigation.

---

# 3. Triage Levels

## Level 0 — Paper Triage

No computation.

Question:

Can this class of environments even satisfy the Goal Anchor?

Reject immediately if:

- no lawful structure exists;
- no intervention is possible;
- feedback is absent;
- success can be achieved by modelling labels or human descriptions rather than the world.

---

## Level 1 — Necessary Property Test

Analytical.

Question:

Does the candidate satisfy the minimal necessary properties?

Required properties:

1. lawful or lawfully stochastic dynamics;
2. intervention;
3. feedback;
4. counterfactual distinguishability;
5. non-vacuous success/failure boundary;
6. auditability;
7. layer separability.

Failure of any property is grounds for rejection or downgrade.

---

## Level 2 — Boundary Test

Analytical or minimal computational.

Question:

What is the first likely wall?

Possible walls:

- trajectory dependence;
- state explosion;
- weak feedback;
- unverifiable emergence;
- proxy-world collapse;
- vacuous safety;
- lack of counterexamples;
- partial observability without recoverable latent structure.

The goal is to identify the most likely fundamental failure before building a
full prototype.

---

## Level 3 — Minimal Prototype

Smallest possible implementation.

Question:

Does the predicted wall appear immediately?

The prototype should be designed to falsify the candidate class, not to
demonstrate success.

---

## Level 4 — Full Candidate Program

Only candidates that survive Levels 0–3 may receive full experimental
investment.

---

# 4. Decision Tree

```text
START
  |
  v
Lawful or lawfully stochastic?
  |-- NO  -> Reject
  |
  v
Intervention possible?
  |-- NO  -> Reject
  |
  v
Feedback constrains belief?
  |-- NO  -> Reject
  |
  v
Counterfactuals distinguishable?
  |-- NO  -> Reject
  |
  v
Boundary non-vacuous?
  |-- NO  -> Reject or downgrade
  |
  v
Audit possible?
  |-- NO  -> High risk / prototype only
  |
  v
Layer separation possible?
  |-- NO  -> High risk
  |
  v
Minimal prototype
