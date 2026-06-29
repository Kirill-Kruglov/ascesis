# BA4.0 — Layered Abstraction Discipline

## Purpose

BA4.0 formalizes a discipline that became necessary after BA3.E1.

BA3.E1 showed that MB5 is not a single mechanism. Some MB5 subfamilies affect transition behavior, while others affect reporting, projection, or diagnostics only. Treating all of them as one mechanism produced a category error.

The purpose of this document is to prevent future abstraction errors caused by mixing model layers.

---

# 1. Core Lesson

A variable must not enter a shield or WSTS abstraction merely because it is measurable.

It may enter only if it belongs to the layer relevant to the property being verified.

The key distinction is:

```text
transition-relevant variable
≠
observation variable
≠
projection variable
≠
reporting variable
```

BA3.E1 demonstrated that some ratio/concentration observables can be replaced without changing fidelity, while policy-visible concentration cannot be treated the same way.

---

# 2. Layer Taxonomy

## L1 — Dynamics Layer

Variables and rules that directly change the future state of the environment.

Examples:

* welfare component updates;
* lineage growth;
* mutation;
* migration;
* extraction;
* aid interception;
* neighbor harm;
* mass change.

A variable in this layer may affect collapse causally.

---

## L2 — Policy / Control Layer

Variables used to choose interventions, aid allocation, containment, or audit response.

Examples:

* policy score;
* bad consequence trigger;
* resource allocation;
* containment timer;
* audit activation;
* policy-visible concentration.

This layer may not define collapse directly, but it changes future trajectories.

---

## L3 — Observation Layer

Variables available to the policy as observations of the environment.

Examples:

* delayed observation;
* response_to_aid;
* neighbor_delta;
* sag;
* observed resource concentration.

Observation variables matter only if some transition or policy reads them.

---

## L4 — Projection / Abstraction Layer

Variables used by the shield abstraction.

Examples:

* mean welfare deficit;
* concentration counter;
* resource_hhi if used by the 18.0 projection;
* any counter used by WSTS encoding.

A projection variable must be justified by fidelity to the concrete collapse boundary.

---

## L5 — Reporting / Diagnostic Layer

Variables used only for output, analysis, dashboards, or final metrics.

Examples:

* capture index when not read by policy;
* reporting ratios;
* final summary HHI;
* visualization-only fields.

Reporting variables must not be used as evidence that the shield abstraction is faithful unless they also affect L1–L4.

---

# 3. Layer Rule

For every variable or metric, record:

```text
name
source function
layer membership
read by transition? yes/no
read by policy? yes/no
read by shield projection? yes/no
used only for reporting? yes/no
```

A variable may belong to multiple layers, but this must be explicit.

If a variable is L5-only, it must not justify a safety or WSTS claim.

---

# 4. BA3.E1 Reinterpretation

The previous category MB5 must be split.

## MB5a — Policy-visible concentration

Layer:

```text
L2 / L3
```

Status:

Transition-relevant.

BA3.E1 found that S4a improved false-safe but increased witness count. Therefore it is not removable overhead. It is a transition-relevant trade-off point.

---

## MB5b — Reporting ratios

Layer:

```text
L5
```

Status:

Replaceable for current safety analysis.

S4b preserved fidelity while reducing proxy cost. This does not prove MB5 is unnecessary. It proves that reporting ratios should not be counted as transition mechanisms.

---

## MB5c — Projection-visible resource_hhi

Layer:

```text
L4
```

Status:

Currently weak or inert under the 18.0 doomed-set behavior.

S4c preserved fidelity. This suggests that current projection-visible resource_hhi is not carrying decisive shield information in the present abstraction.

---

## MB5d — Capture/reporting components

Layer:

```text
L5, unless policy reads them
```

Status:

Replaceable as diagnostics.

S4d preserved fidelity but should not be treated as transition-level replacement.

---

# 5. New Methodological Constraint

Any future abstraction must pass a layer audit before fidelity testing.

The order must be:

```text
Layer audit
↓
Projection definition
↓
Fidelity kill-gate
↓
Only then: shield synthesis or repair
```

Skipping the layer audit risks repeating the 18.0 error in a subtler form.

---

# 6. Abstraction Eligibility Rules

A variable is eligible for WSTS/shield abstraction only if at least one condition holds:

1. It directly participates in collapse definition.
2. It causally influences future collapse through transitions.
3. It is read by policy/control and changes future trajectories.
4. It is needed for a conservative over-approximation with documented loss.

A variable is not eligible if:

1. It is reporting-only.
2. It changes only final dashboards.
3. It is used only for interpretive analysis after the run.
4. Removing or replacing it leaves transition behavior and collapse fidelity unchanged.

---

# 7. Critical Consequence

The project should no longer ask:

```text
Is mechanism M necessary?
```

without first asking:

```text
At which layer is M necessary?
```

A mechanism may be unnecessary at the reporting layer but necessary at the policy layer.

This is exactly what BA3.E1 showed for MB5.

---

# 8. Updated Research Question

The previous question was:

```text
Can Justitia be represented as a faithful WSTS abstraction?
```

The refined question is:

```text
Which layers of Justitia must be preserved for a faithful safety abstraction,
and which layers are representational or diagnostic overhead?
```

This question is narrower and better aligned with the project goal.

---

# 9. Next Required Artifact

Before the next computational experiment, produce:

```text
justitia_layer_audit.md
```

Required contents:

* all state variables;
* all derived metrics;
* all policy inputs;
* all projection inputs;
* all reporting metrics;
* layer assignment;
* whether each item affects transition behavior;
* whether each item affects collapse;
* whether each item is eligible for abstraction.

---

# 10. Critical Review of BA4.0

BA4.0 is useful, but it has risks.

## Risk 1 — Layer boundaries may be fuzzy

Some variables move between layers depending on policy.

For example, a metric can be reporting-only in one configuration and policy-visible in another.

Therefore layer assignment must be conditional, not absolute.

---

## Risk 2 — “Reporting-only” does not mean scientifically irrelevant

Reporting variables may reveal real structure.

They simply must not be used as direct safety evidence unless linked to transition or projection behavior.

---

## Risk 3 — Layer discipline may become bureaucracy

The goal is not to classify everything forever.

The goal is to prevent abstraction errors.

Layer audit should remain lightweight and tied to falsification.

---

## Risk 4 — Projection layer may hide old mistakes

Even after layer audit, projection fidelity must still be killed-gated.

A correctly layered projection can still be too coarse.

---

# 11. Current Best Interpretation

BA4.0 does not solve the WSTS problem.

It identifies a prior error class:

```text
layer confusion
```

The project now knows that at least some apparent structural cost came from mixing transition mechanisms with reporting/projection observables.

Therefore the next disciplined step is not shield repair.

It is a layer audit followed by a CEGAR-like abstraction refinement plan.

---

# 12. One-Sentence Summary

BA4.0 says: before asking whether an abstraction is monotone, first determine which model layer each variable belongs to; otherwise reporting, projection, policy, and dynamics will be mixed into one false mechanism.
