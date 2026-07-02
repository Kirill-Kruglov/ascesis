# KG_SPEC — Programme Gate Specification

**Status:** Draft

**Scope:** Research Programme Infrastructure

**Applies to:** All future Programme Gates (KG-*).

---

# Purpose

A Programme Gate (KG) is a formal evaluation stage applied to the research programme itself.

Unlike experimental kill-gates, which evaluate hypotheses about the external world, Programme Gates evaluate the structure, assumptions and scientific legitimacy of the research programme.

A Programme Gate exists to answer a single question:

> **Should the programme continue in its current form?**

A Programme Gate never exists to improve writing.

It exists to determine whether a component of the programme survives independent criticism.

---

# Why Programme Gates Exist

Experience from Door 1 demonstrated that research programmes can drift long before individual experiments fail.

Negative empirical results are insufficient if the programme silently changes its concepts, assumptions or objectives.

Programme Gates therefore apply the same falsification discipline to the programme itself.

---

# Objects of Evaluation

Programme Gates may evaluate:

- research goals;
- central concepts;
- assumptions;
- bridges between research stages;
- evidence transfer;
- operational definitions;
- interaction with prior literature;
- methodological procedures.

Programme Gates do **not** evaluate prose quality.

---

# General Lifecycle

```
Programme

↓

Programme Gate Specification

↓

KG-N

↓

Decision

↓

(if needed)

Programme Revision (PR)

↓

Next Gate
```

Every Programme Gate produces a decision.

Only Programme Revisions may modify the programme.

---

# Inputs

Every KG must explicitly declare its inputs.

Typical inputs include:

- current programme documents;
- previous Programme Revisions;
- previous KG decisions;
- empirical evidence;
- external reviews;
- relevant literature.

Implicit inputs are forbidden.

---

# Outputs

Every KG produces exactly one structured output.

Required sections:

- Scope
- Question
- Evidence
- Competing hypotheses
- Analysis
- Decision
- Consequences

No programme edits occur inside a KG.

---

# Allowed Decisions

Every Programme Gate must end with one of the following decisions.

## Continue

The evaluated component survives.

No Programme Revision required.

---

## Continue After Revision

The component survives only after explicit programme modification.

A Programme Revision becomes mandatory.

---

## Pause

Current evidence is insufficient.

Research is frozen until missing evidence is obtained.

---

## Reject

The evaluated component fails.

The programme must either:

- remove the component,

or

- replace it through an explicit Programme Revision.

---

# Burden of Proof

The burden always lies on the programme.

External criticism does not need to prove the programme false.

The programme must demonstrate why the criticised component survives.

This follows Popperian asymmetry:

Failure requires only one successful falsification.

Survival requires surviving every available criticism.

---

# Programme Revisions

Programme Gates never modify programme documents.

Programme Revisions (PR) are the only mechanism by which the programme changes.

The separation is intentional.

KG answers:

> Should something change?

PR answers:

> What exactly changes?

---

# Relationship to Experimental Kill-Gates

Experimental Kill-Gates evaluate scientific hypotheses.

Programme Gates evaluate the research programme.

They operate at different epistemic levels.

```
Experiment

↓

Experimental Kill-Gate

↓

Knowledge


Research Programme

↓

Programme Gate

↓

Programme Revision
```

The two mechanisms complement one another.

---

# Evidence Rules

Evidence does not automatically transfer.

Every transfer requires an explicit bridge.

Examples:

Door 1

↓

Door1 Extracted Knowledge

↓

Substrate Discovery

↓

KG1

Without an explicit bridge, evidence remains local.

---

# External Review

External reviewers have no privileged authority.

Their role is to generate high-quality falsification attempts.

Examples:

- Claude
- future human reviewers
- published criticism
- replication failures

External criticism becomes evidence,

not truth.

---

# Dependencies

Programme Gates may depend on earlier Programme Gates.

Dependencies must form an acyclic graph.

No gate may depend upon itself.

Future KG pipeline documentation defines these dependencies explicitly.

---

# Completion Criteria

A Programme Gate is complete only if:

- scope is explicit;
- evidence is identified;
- competing explanations are considered;
- a decision is made;
- consequences are documented;
- future dependencies are updated.

---

# Failure Modes

Programme Gates are themselves subject to future review.

Typical failure modes include:

- ritualization;
- bureaucratic documentation;
- overfitting to one research programme;
- inability to reject weak concepts;
- excessive dependence on one reviewer;
- silent goal drift.

The existence of Programme Gates does not guarantee scientific quality.

They are tools,

not proofs.

---

# Design Principles

Programme Gates should be:

- minimal;
- explicit;
- falsifiable;
- historically traceable;
- independent of any individual LLM;
- reproducible by another research team.

---

# Relationship to the Playbook

The Playbook specifies research procedure.

Programme Gates specify programme governance.

The two are intentionally separated.

A future Playbook may reuse Programme Gates,

but Programme Gates are not tied to any particular implementation.

---

# Versioning

Programme Gates evolve through explicit revisions.

Changes to this specification require:

- external review;
- explicit rationale;
- version increment.

Silent modification is prohibited.

---

# Exit Condition

The Programme Gate framework succeeds only if it eventually makes itself unnecessary.

If a research programme reaches stable scientific maturity,

future Programme Gates should become increasingly rare.

A framework that requires perpetual self-governance has likely become bureaucracy rather than science.

---

# Final Principle

A Programme Gate is successful

not when it preserves the programme,

but when it increases confidence that the surviving programme is closer to reality than the programme that entered the gate.

If rejection is the correct outcome,

rejection is success.

---

**Status**

Draft.

To be instantiated first by:

**KG1 — Goal Anchor Identity Gate.**
