# Codex Specification v0.4
## Project: WorldCore — Open-ended DSL Verification Framework

**Status:** Required revision after first experimental run.

The first implementation successfully demonstrated:

- the framework executes end-to-end;
- the symbolic solver works;
- the capacity bound does not immediately collapse.

However, the current experiments are **not yet capable of falsifying the central hypothesis**, because several metrics are too weak or incorrectly defined.

The goal of this revision is **not to improve scores**, but to make the framework capable of disproving the hypothesis.

---

# Guiding Principle

The objective is **not** to produce a generator that scores well.

The objective is to build a framework that is capable of proving that the generator is *dead* if it really is.

Every metric should therefore be adversarial.

---

# Current Problems

The previous experiment produced:

- perfect solver accuracy
- perfect OOD accuracy
- perfect memorization baseline
- no Kolmogorov trap

This combination is suspicious.

Most likely explanations:

1. memorization baseline is leaking
2. OOD split is not truly OOD
3. task templates repeat
4. novelty metric is too weak
5. reasoning depth is too shallow

This revision addresses those issues.

---

# Revision Overview

The following work items are REQUIRED.

---

# 1. Rename incorrect metrics

Current metric:

```json
collision_rate
```

is misleading.

Replace with

```text
uniqueness_ratio =
unique_canonical_worlds / sampled_worlds
```

and

```text
collision_fraction =
1 - uniqueness_ratio
```

Report both.

---

# 2. True canonical novelty

Currently novelty is insufficient.

Implement TWO independent novelty metrics.

## World novelty

```text
new canonical world hashes
--------------------------
generated worlds
```

## Task novelty

```text
new canonical task hashes
-------------------------
generated tasks
```

Both curves must be exported as CSV.

---

# 3. Canonical OOD split

Current split appears to leak.

OOD MUST satisfy ALL conditions.

---

## Condition A

No canonical task hash may exist in both train and test.

---

## Condition B

No canonical world hash may exist in both train and test.

---

## Condition C

Entity identifiers must be regenerated.

Names cannot overlap.

---

## Condition D

Training:

```
proof depth <= 2
```

Testing:

```
proof depth >= 4
```

---

## Condition E

Training and test must differ in reasoning templates whenever possible.

For example:

train:

```
transitivity
```

test:

```
transitivity + implication
```

or

```
negation + transitivity
```

---

Generate a report

```
ood_split_validation.json
```

containing

```json
{
  "shared_world_hashes": ...,
  "shared_task_hashes": ...,
  "shared_entity_names": ...,
  "shared_templates": ...
}
```

All should ideally be zero.

---

# 4. Memorization baseline redesign

Current memorization baseline reaches 100%.

This should almost never happen.

Replace current implementation.

New memorization baseline:

The predictor may ONLY access

```
canonical_task_hash
```

observed during training.

If hash unseen

↓

predict majority label.

No graph features.

No inference.

No entity names.

No predicates.

Nothing else.

Goal:

Estimate pure template memorization.

Export

```
memorization_analysis.json
```

including

```
seen hashes

unseen hashes

accuracy on seen

accuracy on unseen
```

---

# 5. Label entropy

Measure whether dataset itself is trivial.

Export

```
label_distribution.json
```

Example

```json
{
  "true": ...,
  "false": ...,
  "unknown": ...
}
```

Also compute

```
label entropy
```

If entropy is low

↓

dataset is suspicious.

---

# 6. Task complexity metrics

Each generated task must contain

```
reasoning depth

number of distractors

number of supporting facts

number of irrelevant facts

number of predicates

number of entities

number of inference rules used
```

Produce

```
complexity_distribution.csv
```

---

# 7. Hard adversarial pairs

Generate adversarial pairs.

Example

World A

```
A before B

B before C

?
A before C

TRUE
```

World B

```
A before B

B before C

NOT B before C

?
A before C

FALSE
```

Graphs should differ minimally.

Answers must differ.

Measure

```
adversarial accuracy
```

---

# 8. Mixed reasoning

Current reasoning is too shallow.

Add combinations:

```
transitivity

+

negation
```

```
implication

+

transitivity
```

```
causal

+

temporal
```

```
belief

+

fact
```

```
part-of

+

location
```

etc.

Each task should record

```
reasoning_pattern
```

Example

```
transitivity

transitivity+negation

belief+implication

mixed3
```

---

# 9. Learnability metric redesign

Current learnability definition is insufficient.

Define

```
Learnability(N)
```

as

performance improvement on

UNSEEN

canonical tasks

at

OOD depth.

Compute

```
Δ accuracy

between

N

and

2N
```

Plot

```
learnability curve
```

not just accuracy.

---

# 10. Kolmogorov diagnostics redesign

Current diagnostic is boolean.

Replace with full report.

Include

```
novelty

↓

OOD transfer

↓

memorization

↓

solver
```

Output

```
kolmogorov_report.json
```

with

```json
{
  "world_novelty_curve": ...,
  "task_novelty_curve": ...,
  "ood_curve": ...,
  "memorization_curve": ...,
  "solver_curve": ...,
  "suspected_failure_mode": ...
}
```

Possible failure modes:

```
template memorization

finite generator

solver mismatch

label imbalance

OOD leakage

healthy
```

---

# 11. Positive control

Symbolic solver remains required.

Additionally implement

```
Random predictor

Majority predictor

Hash memorizer

Graph-feature classifier
```

Show all together.

---

# 12. Capacity diagnostics

Current capacity estimate is too coarse.

Add

```
observed novelty vs samples

canonical collisions

expected saturation estimate
```

Produce

```
capacity_diagnostics.png
```

---

# 13. Experimental dashboard

Produce one summary table

```
experiment_summary.csv
```

Columns:

```
train_size

world_novelty

task_novelty

solver

memorization

majority

random

graph classifier

OOD

entropy

avg depth

avg distractors

avg rules

failure mode
```

---

# 14. Stop conditions

Framework should explicitly detect

## A

Template memorization.

## B

Finite generator saturation.

## C

OOD leakage.

## D

Label collapse.

## E

Too-simple reasoning.

If detected

↓

print

```
WARNING

Current experiment cannot falsify hypothesis.

Reason:
...
```

---

# 15. Required output artifacts

After execution the project must produce

```
capacity_summary.json

capacity_diagnostics.png

novelty_curve.csv

task_novelty_curve.csv

world_novelty_curve.csv

learnability_curve.csv

ood_split_validation.json

memorization_analysis.json

label_distribution.json

complexity_distribution.csv

kolmogorov_report.json

experiment_summary.csv
```

---

# 16. Success Criteria

This revision is successful **not** if scores improve.

It is successful if the framework becomes capable of distinguishing between:

- genuine compositional learning

and

- template memorization.

Only after this distinction is reliable should the project proceed toward:

1. environment generation (POET-like branch), or
2. Sanskrit verifier experiments.
