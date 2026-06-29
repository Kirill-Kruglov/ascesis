# research/Substrate_Discovery_v1/07_Search_Strategy.md

```markdown
# Search Strategy

## Status

Methodological document.

This chapter defines the search procedure
for the Substrate Discovery programme.

Unlike previous chapters,
it proposes no theoretical concepts.

Its purpose is to organise
future exploration.

---

# Motivation

Historically,
the project began
by searching directly
for candidate environments.

The Justitia investigation demonstrated
that this approach
is expensive
and difficult to generalise.

The present programme therefore
reverses the search order.

Instead of

Candidate

↓

Evaluation

the programme adopts

Necessary Properties

↓

Candidate Classes

↓

Candidate Environments

↓

Implementations

↓

Experiments

This inversion
is the principal methodological change
introduced by Substrate Discovery.

---

# Principle

The search should maximise

knowledge gained,

not

candidate survival.

Rejecting a candidate
is considered progress
if the rejection
eliminates
an entire region
of the search space.

---

# Search Levels

The programme distinguishes
five analytical levels.

Level 0

Goal Anchor.

Why the programme exists.

---

Level 1

Necessary properties.

Constraints
shared by all
successful substrates.

---

Level 2

Classes of computable environments.

Families
rather than implementations.

---

Level 3

Concrete substrate candidates.

Examples include

physics,

program execution,

proof worlds,

robotics,

multi-agent systems.

---

Level 4

Implementations.

Specific environments.

Specific simulators.

Specific algorithms.

---

Level 5

Experiments.

Concrete computational tests.

---

# Rule

Movement
should normally occur

downward.

Goal

↓

Properties

↓

Classes

↓

Candidates

↓

Implementations

↓

Experiments

Reverse movement
requires explicit justification.

---

# Candidate Pipeline

Every future substrate
passes through
the same sequence.

Step 1

Identify computational class.

---

Step 2

Project
onto
necessary-property space.

---

Step 3

Attempt analytical falsification.

---

Step 4

Review relevant literature.

---

Step 5

Estimate expected information gain.

---

Step 6

Only then

construct implementation.

---

Step 7

Run computational experiments.

---

Step 8

Update
the property map.

---

# Expected Information Gain

Candidate selection
should maximise

expected reduction
of uncertainty.

Not

probability
of success.

A candidate
that can eliminate
an entire hypothesis
is preferable
to one
that merely confirms
existing intuition.

---

# Research Geometry

The programme
is viewed
as movement
through
a search space.

Each experiment
changes

the shape
of the remaining space.

Therefore

negative results

are geometric operations.

They remove regions.

They do not represent failure.

---

# Candidate Ranking

Future candidates
should be ranked
according to

Analytical tractability.

↓

Expected information gain.

↓

Experimental cost.

↓

Implementation complexity.

↓

Novelty.

Novelty alone
is never sufficient.

---

# Research Assets

Every completed investigation
should produce
at least one
of the following assets.

A new theorem.

A new analytical constraint.

A new property.

A rejected hypothesis.

A reduced search region.

A validated benchmark.

An improved methodology.

Otherwise,

the investigation
should be reconsidered.

---

# Decision Ledger

Major programme decisions
should be recorded explicitly.

Examples include

Closing Justitia.

Starting Substrate Discovery.

Rejecting H_FA1.

Accepting a new analytical framework.

The objective
is reproducibility
of reasoning.

---

# Failure Modes

The search procedure
should continuously monitor

candidate attachment,

concept drift,

premature formalisation,

implementation bias,

confirmation bias,

proxy optimisation.

Each represents
a recurring failure mode
observed
during long research programmes.

---

# Programme Kill-Gates

SG-1

Has the Goal Anchor changed?

If YES,

stop
and justify.

---

SG-2

Is a new concept
strictly necessary?

If NO,

reuse existing theory.

---

SG-3

Can the question
be answered analytically?

If YES,

postpone implementation.

---

SG-4

Does a candidate
introduce
new transferable knowledge?

If NO,

deprioritise.

---

SG-5

Has the search become
candidate-centred
rather than
property-centred?

If YES,

return
to Level 1.

---

# Summary

The Substrate Discovery programme
is fundamentally

a search procedure.

Its objective
is not

to defend favourite environments,

but

to progressively reduce
the space
of plausible substrate classes

until either

a surviving family emerges,

or

the Goal Anchor
is shown
to be unattainable
under the assumed constraints.

Both outcomes
represent scientific progress.
```
