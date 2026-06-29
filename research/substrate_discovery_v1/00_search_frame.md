# research/Substrate_Discovery_v1/00_search_frame.md

# Substrate Discovery v1 — Search Frame

## Status

Research frame.

This document begins the next phase after the Justitia / Door-1 investigation.

It is not a candidate proposal.

It is a disciplined search frame for identifying future substrate classes.

---

# 1. Goal Anchor

The long-term goal remains:

> Train LLM-like systems in environments where world structure is derived from lawful interaction, not statistically absorbed from human internet text.

The project is not merely searching for a safer benchmark.

It is searching for a substrate capable of supporting derived internal world models.

---

# 2. Why This Phase Exists

The Justitia investigation produced strong negative knowledge.

It did not falsify the long-term goal.

It falsified several natural paths through one candidate substrate.

The next phase should therefore avoid asking:

> How can Justitia be repaired?

Instead it should ask:

> What properties must a substrate have so that derivable world modelling is possible?

---

# 3. Extracted Constraints from Justitia

Future substrate candidates should be evaluated against these constraints.

## C1 — Lawful dynamics

The environment must contain stable generative structure.

If the world has no regularity, nothing meaningful can be derived.

## C2 — Intervention

The learner must be able to act.

Pure passive observation risks reproducing the internet-training problem in another form.

## C3 — Feedback

Actions must produce consequences that constrain future belief.

The substrate must punish false internal models.

## C4 — Non-vacuous safety boundary

If safety requires declaring almost everything unsafe, the substrate is not useful.

## C5 — Layer discipline

Dynamics, observation, control, projection and reporting must be separable.

## C6 — Counterexample decomposability

Failures should decompose into reusable classes.

If every failure is unique, refinement will not scale.

## C7 — Verification or audit tractability

The substrate does not need to be fully decidable, but it must admit some meaningful audit process.

## C8 — Avoid proxy-world collapse

The learner should not merely learn human descriptions of the world.

It should be forced to infer structure from interaction with the substrate.

---

# 4. Search Question

Which classes of environments naturally support:

```text
lawful dynamics
+
intervention
+
feedback
+
derivable structure
+
auditable failure
