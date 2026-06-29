# Toward a Theory of Faithful Abstraction

## Status

Working theory.

This document is intentionally separated from the empirical basis.

Everything in this document should be interpreted as a theoretical
construction built upon the experimental observations described in
`01_empirical_basis.md`.

Nothing here should be interpreted as experimentally proven unless explicitly
marked.

---

# 1. Motivation

The empirical program established several observations that are difficult to
explain using the traditional "feature selection" view of abstraction.

Projection blindness (18.1), mechanism interaction (BA1), mechanism
decomposition (BA3), semantic layers (BA4), and structured witness classes
(FA1) together suggest that the primary unit of abstraction is not the
individual variable.

This motivates a different theoretical framework.

---

# 2. Three Levels

The theory distinguishes three different objects.

Level 1

Concrete dynamics.

The complete underlying transition system.

---

Level 2

Semantic information.

Information that distinguishes behaviour relevant to a target property.

Examples:

- spread of local failures;
- remaining total mass;
- delayed response to intervention;
- policy-visible concentration.

---

Level 3

Representation.

Concrete variables, metrics and state encodings.

Examples:

- vectors;
- ratios;
- HHI;
- counters;
- dashboard statistics.

---

[DERIVED]

The experiments suggest that Level 2 is neither identical to the concrete
state nor identical to the implementation variables.

Instead it forms an intermediate semantic layer.

---

# 3. Information Invariants

The central theoretical object becomes the Information Invariant.

Definition (working).

An information invariant is the smallest semantic object that distinguishes
two concrete behaviours relevant to a target property.

It is intentionally independent of implementation.

One invariant may depend upon several variables.

One variable may participate in several invariants.

---

Examples

Variable:

```
zone_welfare[]
```

Possible invariant:

```
count(zone_welfare < threshold)
```

---

Variable:

```
lineage_mass[]
```

Possible invariant:

```
total_mass
```

---

Variable:

```
response history
```

Possible invariant:

```
response_to_aid distinguishability
```

---

[HYPOTHESIS]

Information invariants constitute the natural refinement unit.

---

# 4. Semantic Layers

BA4 motivates a layered ontology.

Layer 1

Dynamics

State evolution.

---

Layer 2

Policy

Decision logic.

---

Layer 3

Observation

Accessible information.

---

Layer 4

Projection

Information explicitly retained by the abstraction.

---

Layer 5

Reporting

Information used only after execution.

---

[DERIVED]

The same variable may appear in multiple layers.

Therefore variables cannot be assigned semantic meaning without context.

The unit of abstraction should therefore not be the variable itself.

---

# 5. Witness

The central empirical object of the FA program is the false-safe witness.

Definition.

A witness is a concrete state whose abstraction predicts SAFE while the
concrete trajectory violates the target property.

---

Witnesses are treated as evidence of missing semantic information.

Not of missing variables.

---

[DERIVED]

FA1 suggests that witnesses form a structured semantic population rather than
isolated implementation errors.

---

# 6. Refinement

Traditional refinement:

```
counterexample

↓

add variables
```

Faithful refinement:

```
counterexample

↓

identify missing information

↓

verify layer eligibility

↓

introduce invariant

↓

repeat
```

---

[HYPOTHESIS]

The second procedure produces more stable abstractions than the first.

---

# 7. Compression versus Discrimination

FA2 introduces an important distinction.

Compression.

How few invariants explain the witness population.

---

Discrimination.

How well those invariants separate witness states from ordinary SAFE states.

---

[DERIVED]

Compression alone is insufficient.

---

[HYPOTHESIS]

Faithful abstraction requires simultaneous optimisation of:

- compression;
- discrimination;
- semantic eligibility;
- structural compatibility.

---

# 8. Layer Eligibility

Not every invariant is admissible.

An invariant is eligible only if it belongs to a layer capable of influencing
the verified property.

Examples of likely eligible invariants:

- spread;
- mass;
- policy-visible concentration;
- compact history summaries.

Examples of likely ineligible invariants:

- reporting ratios;
- dashboard statistics;
- post-hoc metrics.

---

[HYPOTHESIS]

Layer eligibility is a prerequisite for faithful refinement.

---

# 9. Faithfulness

Traditional view.

Two abstract states are equivalent if they share the same representation.

Working FA view.

Two abstract states are equivalent only if they remain indistinguishable
relative to the verified property.

---

Therefore,

faithfulness becomes property-relative rather than representation-relative.

---

# 10. Candidate Principle

Faithful Refinement Principle.

[HYPOTHESIS]

Refinement should add only the smallest layer-eligible semantic information
required to separate the observed witness class.

---

This principle is currently unsupported.

It serves only as the organising hypothesis of the FA program.

---

# 11. Predictions

The theory predicts the following.

[PREDICTION]

Different witness classes should repeatedly require the same information
invariants.

---

[PREDICTION]

History-related witnesses should compress into a much smaller family of
history summaries.

---

[PREDICTION]

Reporting-only metrics should rarely become necessary refinement coordinates.

---

[PREDICTION]

Independent implementations of the same behavioural substrate should produce
similar witness taxonomies.

---

[PREDICTION]

Constructive refinement should fail if discrimination requires high-dimensional
raw state rather than compact semantic invariants.

---

# 12. Immediate Falsifiers

The theory would be substantially weakened if any of the following were shown.

1.

Witness classes become unstable across seeds or implementations.

2.

Minimal information is no more useful than arbitrary variables.

3.

High discrimination requires almost the complete raw state.

4.

Layer discipline provides no measurable benefit.

5.

Witness compression disappears after implementation changes.

---

# 13. Scope

This theory does not claim to explain all abstractions.

It currently concerns only abstractions constructed for behavioural
verification.

Whether the framework generalises beyond this domain remains unknown.

---

# 14. Current Status

The theory is intentionally incomplete.

It should be regarded as the simplest theoretical structure presently capable
of explaining the empirical observations.

Future experiments are expected either to strengthen it or to replace it.
