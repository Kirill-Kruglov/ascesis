# Faithful Abstraction Program v1.0

## Status

Working research program.

This document defines the scope, motivation and research discipline of the
Faithful Abstraction (FA) program.

It is not itself evidence.

All empirical claims referenced here are established in the accompanying
empirical basis document.

---

# 1. Background

The original objective of the project (meme v1.1–v1.4) was to understand whether
a compact analytical abstraction could faithfully distinguish safe from
collapsing trajectories in the Justitia environment.

Initially this question was investigated through closure metrics (17-series),
latent metric geometry, and cross-substrate comparison.

Later, the project shifted toward formal verification and WSTS-inspired
abstractions.

Experiment 18.1 demonstrated that the first apparently successful abstraction
was not faithful.

This became the turning point of the project.

---

# 2. Transition from BA to FA

Boundary Analysis (BA0–BA4) systematically investigated possible explanations
for the failure observed in 18.1.

The following explanations were examined.

- A single dominant monotonicity breaker.
- Structural complexity as the price of semantic fidelity.
- Removal of "bad" mechanisms.
- Mechanism-level replacement.
- Layer confusion.

Each hypothesis was either rejected or substantially refined.

The result was a change of research object.

The project is no longer centred on Justitia itself.

Instead, Justitia is treated as an experimental substrate for studying the
construction of faithful abstractions.

---

# 3. New Research Object

The primary object of study is now:

> Faithful Abstraction Construction.

This object is intentionally more general than Justitia.

The long-term question becomes:

> Which information must be preserved so that an abstraction remains faithful
> with respect to a target behavioural property?

The project therefore moves one level upward.

Instead of asking:

> Can this particular abstraction be verified?

it asks:

> How should faithful abstractions be constructed in the first place?

---

# 4. Empirical Origin

The Faithful Abstraction program was not proposed a priori.

It emerged from a sequence of negative experimental results.

[FACT]

The following observations motivated the transition.

• Experiment 18.1 demonstrated projection blindness.

• BA1 failed to identify a single dominant monotonicity-breaking mechanism.

• BA2 showed that structural cost and semantic benefit are not aligned.

• BA3 demonstrated that MB5 is not an atomic mechanism.

• BA4 showed that multiple semantic layers had been unintentionally merged.

These observations collectively motivate a different research direction.

---

# 5. Central Working Hypothesis

The current working hypothesis is:

## H_FA1

Faithful abstraction refinement should be driven by minimal missing semantic
information rather than minimal missing variables.

This hypothesis is not yet proven.

It defines the central direction of the FA program.

---

# 6. Conceptual Shift

Earlier stages implicitly assumed:

Concrete State

↓

Variables

↓

Projection

↓

Verification

The FA program instead assumes:

Concrete Dynamics

↓

Semantic Layers

↓

Information Invariants

↓

Projection

↓

Verification

The difference is fundamental.

Variables are implementation artefacts.

Information invariants are semantic objects.

---

# 7. Research Discipline

Every future FA experiment follows the same sequence.

Concrete execution

↓

False-safe witness extraction

↓

Missing information analysis

↓

Layer eligibility check

↓

Candidate refinement

↓

Kill-gate

↓

Repeat

This order is mandatory.

No refinement may be accepted before passing the layer audit and kill-gate.

---

# 8. Current Status

The FA program is exploratory.

No constructive faithful abstraction has yet been produced.

However, the project now possesses:

• an empirical witness taxonomy,

• a layer discipline,

• a refinement discipline,

• an explicit falsification strategy.

These constitute the initial foundation of the research program.

---

# 9. Reading Order

Readers are encouraged to continue with:

01_empirical_basis.md

followed by

02_fa_theory.md

before reading any speculative hypotheses.
