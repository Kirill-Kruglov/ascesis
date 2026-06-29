# research/Substrate_Discovery_v1/05_Interaction_and_Identifiability.md

```markdown id="ltm2fv"
# Interaction and Identifiability

## Status

Foundational analytical document.

This chapter investigates why interaction appears to be
a necessary component of the Door-1 objective.

The central claim is intentionally weak.

It does not claim that interaction is always sufficient.

It investigates whether interaction is necessary.

---

# Motivation

The previous chapter introduced derivability.

An immediate question follows.

Can derivability arise
from passive observation alone?

Or

does lawful interaction
provide information
that observations alone cannot reveal?

---

# Passive Observation

Suppose

a learner receives
an unlimited stream
of observations.

The learner may discover

statistical regularities,

prediction rules,

compression,

latent variables.

However,

certain computational hypotheses
remain observationally indistinguishable.

The learner has no mechanism
for separating them.

---

# Intervention

Suppose instead

the learner may perturb
the environment.

Actions now become experiments.

Different computational hypotheses
may produce identical observations,

yet predict different consequences
of intervention.

Interaction therefore reveals
previously hidden computational structure.

---

# Observation

Interaction changes
not only the information received,

but the space
of distinguishable hypotheses.

Status

Observation.

Supported qualitatively
by causal reasoning,

control,

and reinforcement learning.

Needs formal treatment.

---

# Working Definition 5.1

Interaction

is any computational process
through which the learner
changes future observations
by acting upon
the environment.

The definition includes

physical actions,

symbolic actions,

program execution,

proof construction,

experimental perturbation,

policy selection.

Status

Working definition.

---

# Identifiability

Two computational environments
may produce

identical observation streams.

Yet differ
under intervention.

Therefore,

observational equivalence

does not imply

computational equivalence.

This distinction appears fundamental.

---

# Consequence

Passive datasets
may contain
insufficient information
to identify
the computational process
that generated them.

Additional interaction
may be required.

The Goal Anchor
therefore naturally favours
interactive environments.

---

# Counterfactual Structure

Interaction
implicitly generates
counterfactual information.

Instead of asking

"What happened?"

the learner begins asking

"What would happen
if another action
had been chosen?"

Counterfactual structure
appears essential
for discovering computational laws.

---

# Relation to Existing Theory

The present viewpoint
appears related to

causal inference,

active experimentation,

optimal experimental design,

reinforcement learning,

control theory,

system identification.

However,

the current programme
uses these fields
primarily as sources
of analytical tools,

not as complete solutions.

---

# Why Justitia Failed to End the Programme

One possible interpretation
of the Justitia investigation
would be

"The environment was unsuitable."

The present programme
adopts a different interpretation.

The investigation
revealed new constraints
on the interaction
required for successful derivation.

Negative knowledge
therefore becomes
part of the substrate search.

---

# Interaction Geometry

Interaction itself
appears to possess structure.

Possible dimensions include

frequency,

reversibility,

cost,

latency,

locality,

compositionality,

observability.

These dimensions
remain almost unexplored.

Future work
should investigate them directly.

---

# Candidate Hypothesis

Different interaction regimes

may induce

qualitatively different
internal models,

even within
the same environment.

Status

Working hypothesis.

---

# Candidate Failure Modes

Interaction may become

too weak,

too expensive,

too noisy,

too delayed,

or

too unconstrained.

Any of these
may destroy derivability.

Future experiments
should investigate
these limits.

---

# Candidate Kill-Gates

IG-1

Can passive observation
alone
produce
equally rich internal models?

If YES,

interaction
may not be necessary.

---

IG-2

Can intervention
fail to distinguish
computational hypotheses?

If YES,

interaction
is insufficient.

---

IG-3

Can interaction
be replaced
entirely
by richer observations?

If YES,

interaction
is not fundamental.

---

IG-4

Does increasing interaction
always improve derivability?

If NO,

interaction possesses
its own geometry
rather than acting
as a simple quantity.

---

# Connection to the Goal Anchor

The Goal Anchor
does not require

more interaction.

It requires

interaction
that reveals
lawful computational structure.

This distinction
should guide
future substrate design.

---

# Summary

Interaction
should not be viewed
merely
as an engineering feature
of reinforcement learning.

Instead,

interaction appears
to determine

which computational hypotheses
are distinguishable
by the learner.

If this observation survives
future analytical review,

interaction geometry
may become
one of the central objects
of the entire programme.
```
