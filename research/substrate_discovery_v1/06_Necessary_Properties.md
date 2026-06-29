# research/Substrate_Discovery_v1/06_Necessary_Properties.md

```markdown
# Necessary Properties

## Status

Analytical framework.

This chapter proposes candidate necessary properties
that a computational environment may require
in order to induce internal-model construction.

No property presented here is considered established.

Each remains subject to analytical
and computational falsification.

---

# Motivation

Previous chapters introduced

- computable environments,
- derivability,
- interaction.

The next question naturally follows.

Which properties of an environment
could make internal-model construction
the rational strategy?

Rather than searching directly
for successful substrates,

the present programme searches
for necessary properties.

This shifts the search
from implementations
towards constraints.

---

# Methodological Principle

Necessary properties
are considerably more valuable
than successful examples.

A successful example
may represent only one solution.

A necessary property
constrains the entire search space.

Therefore,

the programme prioritises
identification of necessary properties
over construction
of individual environments.

---

# Candidate Property P1

Lawful Computational Structure

Description

The environment must possess
stable computational regularities
that persist across interaction.

Without lawful structure,

generalisation becomes impossible.

Status

High confidence.

Supported by existing theory.

Still requires formal review.

---

# Candidate Property P2

Intervention Sensitivity

Description

Actions performed by the learner
must reveal information
not obtainable
through passive observation alone.

Otherwise,

interaction contributes
no additional computational value.

Status

Medium confidence.

Derived from Chapter 5.

---

# Candidate Property P3

Counterfactual Richness

Description

Different actions
must generate meaningfully different futures.

Otherwise,

internal models
provide little advantage.

Status

Working hypothesis.

---

# Candidate Property P4

Auditability

Description

The learner
must be capable
of identifying
why outcomes occur.

Auditability
does not require
complete interpretability.

It requires
persistent computational causes
that can be investigated.

Status

Working hypothesis.

---

# Candidate Property P5

Compositionality

Description

Previously discovered mechanisms
should remain reusable
in new situations.

Without compositionality,

knowledge becomes
trajectory-specific.

Status

Working hypothesis.

---

# Candidate Property P6

Model Advantage

Description

Learners possessing
better internal models

should systematically outperform

learners relying only on memorisation
or statistical lookup.

This property directly connects
environment design
to the Goal Anchor.

Status

Critical hypothesis.

---

# Candidate Property P7

Lawful Stochasticity

Description

Randomness
should arise
from stable computational processes
rather than arbitrary perturbation.

The learner
should derive distributions,
not individual outcomes.

Status

Open question.

---

# Candidate Property P8

Explorable Complexity

Description

The environment
must contain
non-trivial computational structure,

yet remain sufficiently constrained
to permit progressive discovery.

Both extremes
appear undesirable.

Pure simplicity
provides little learning opportunity.

Unbounded complexity
may prevent derivation.

Status

Working hypothesis.

---

# Candidate Property P9

Stable Intervention Semantics

Description

Actions
should possess
persistent computational meaning.

The same intervention
should not arbitrarily change
its consequences.

Otherwise,

internal models
cannot accumulate.

Status

Working hypothesis.

---

# Candidate Property P10

No Dominant Proxy Strategy

Description

Successful behaviour
should not be achievable
primarily through

lookup,

memorisation,

surface heuristics,

or shortcut policies.

Otherwise,

internal-model construction
ceases to be rational.

Status

Critical hypothesis.

---

# Candidate Property P11

Progressive Discoverability

Description

The learner
should encounter
computational structure
incrementally.

Discovery
should neither be trivial
nor impossible.

Status

Open question.

---

# Candidate Property P12

Information Gain through Interaction

Description

Interaction
should consistently reduce
uncertainty
about computational structure.

If interaction
produces no additional information,

the environment
cannot support derivation.

Status

Working hypothesis.

---

# Property Dependencies

Some properties
appear related.

Lawful Structure

↓

Counterfactual Richness

↓

Model Advantage

↓

Internal Models

Other relationships
remain unknown.

Constructing
a dependency graph
is future work.

---

# Candidate Kill-Gates

NP-1

Can successful internal models emerge
without lawful structure?

If YES,

P1 weakens.

---

NP-2

Can memorisation
match model-based behaviour?

If YES,

P6 weakens.

---

NP-3

Can arbitrary stochasticity
produce equally effective learning?

If YES,

P7 weakens.

---

NP-4

Can proxy strategies
dominate
despite all previous properties?

If YES,

P10 becomes insufficient.

---

NP-5

Can a successful substrate
lack compositionality?

If YES,

P5 weakens.

---

# Research Consequence

Notice the change
relative to the Justitia programme.

Previously

the search asked

"Does this substrate work?"

Now

the search asks

"Which necessary properties
does this substrate satisfy?"

This inversion
greatly increases
the amount of transferable knowledge.

Even unsuccessful substrates
contribute information
about the property space.

---

# Relation to Future Candidate Search

Future substrate classes

should no longer be evaluated
as isolated proposals.

Instead,

each candidate
should first be projected
onto the present property space.

Candidate comparison
then becomes analytical
rather than intuitive.

This principle
will guide
the remainder
of the programme.

---

# Summary

This chapter intentionally avoids
identifying the correct substrate.

Instead,

it proposes
that progress
should be measured
by discovering
necessary properties
shared by all successful substrates.

If correct,

this approach transforms

substrate search

into

constraint discovery.
```
