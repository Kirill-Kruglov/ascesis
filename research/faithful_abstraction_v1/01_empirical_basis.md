# Empirical Basis of the Faithful Abstraction Program

## Status

Evidence document.

This document contains only empirical results and the minimal inferences that
follow directly from them.

Theoretical interpretation is intentionally postponed until
`02_fa_theory.md`.

---

# 1. Purpose

The Faithful Abstraction (FA) program did not originate from a theoretical
proposal.

It emerged from a sequence of experiments whose original goal was entirely
different.

The purpose of this document is to reconstruct that sequence and establish
exactly which statements are supported by experimental evidence.

Every major conclusion is labelled as one of:

- [FACT]
- [INFERENCE]

Hypotheses are intentionally excluded from this document.

---

# 2. Origin: Experiment 18.1

Relevant directory:

```

experiments/18.1\_\*

```

## Question

Can the current shield abstraction distinguish SAFE from future collapse?

---

## Result

[FACT]

Experiment 18.1 failed its predefined kill-gate.

The decisive observation was not simply an elevated false-safe rate.

The decisive observation was that many states classified as SAFE by the
projection were already inside the concrete collapse basin.

The projection therefore merged semantically distinct concrete states.

---

## Interpretation

[INFERENCE]

The observed failure is best described as projection blindness.

The abstraction omitted information required to distinguish collapse-relevant
states.

---

## Consequence

Experiment 18.1 shifted the research focus.

The problem was no longer:

> "Can the shield be repaired?"

The problem became:

> "What information must every faithful abstraction preserve?"

---

# 3. Boundary Analysis

Boundary Analysis was introduced specifically to answer the previous question.

---

# 3.1 BA1

Relevant directory:

```

experiments/BA1\_E1\_monotonicity\_breakers/

```

## Question

Is there a single monotonicity-breaking mechanism responsible for the observed
failure?

---

## Result

[FACT]

Classification:

```

Case C
H2_supported

```

No clean single-mechanism ablation substantially reduced false-safe.

The only apparently dominant intervention (MB4) produced a severe semantic
shift by effectively removing collapse itself.

Therefore MB4 could not be interpreted as a successful refinement.

---

## Consequence

[INFERENCE]

The observed failure cannot be attributed to a single dominant mechanism.

The explanation must involve either interactions or abstraction-level effects.

---

# 3.2 BA2

Relevant directory:

```

experiments/BA2.E1\_Semantic\_benefit\_vs\_structural\_cost\_map/

```

## Question

Is structural complexity justified by semantic benefit?

---

## Result

[FACT]

High structural cost does not imply high semantic benefit.

MB5 exhibited the poorest benefit/cost ratio.

MB2 also showed low benefit relative to structural complexity.

---

## Consequence

[INFERENCE]

Not all complexity contributes equally to fidelity.

Some mechanisms became candidates for replacement.

---

# 3.3 BA3

Relevant directory:

```

experiments/BA3\_E1\_MB5\_surrogate\_replacement\_test/

```

## Question

Can MB5 be replaced by simpler surrogates?

---

## Result

[FACT]

Classification:

```

MB5_functionally_split

```

Full transition-level replacement failed.

However, several reporting/projection subfamilies could be replaced without
observable loss of behavioural fidelity.

---

## Consequence

[INFERENCE]

MB5 is not an atomic mechanism.

It contains multiple semantically different components.

Transition-visible behaviour and reporting behaviour must therefore be
distinguished.

---

# 3.4 BA4

Relevant directory:

```

experiments/BA4\_layer\_audit/

```

## Question

Why did MB5 appear non-atomic?

---

## Result

[FACT]

Static layer audit completed successfully.

Important observations include:

- `resource_hhi` appears in multiple semantic roles.
- reporting ratios do not necessarily influence transition dynamics.
- capture_index should not be treated as safety evidence.
- reporting metrics and transition variables had previously been grouped
  together.

---

## Consequence

[INFERENCE]

The project had unintentionally mixed multiple semantic layers.

Layer confusion became an experimentally supported explanation.

---

# 4. Transition to Faithful Abstraction

Boundary Analysis did not produce a repaired abstraction.

Instead, it established a methodological discipline.

The object of study therefore changed.

Justitia became an experimental substrate.

Faithful abstraction construction became the primary research target.

---

# 5. FA1

Relevant directory:

```

experiments/FA1\_E1\_false\_safe\_witness\_taxonomy/

```

## Question

Can false-safe witnesses be classified according to missing semantic
information?

---

## Result

[FACT]

Classification:

```

Case C

History_control_dominant

```

Total false-safe witnesses:

```

5839

```

Witness decomposition:

```

history_blind                     1932
forward_dynamics_blind            1364
policy_visible_concentration      1115
spread_blind                       724
mass_blind                         400
unknown_or_mixed                   304

```

Current-collapse witnesses:

```

1124

```

Forward-dynamics witnesses:

```

4715

```

---

## Consequence

[FACT]

False-safe witnesses are highly structured.

The majority belong to a small number of recurring semantic classes.

---

## Consequence

[INFERENCE]

The witness space is not arbitrary.

It admits a compact semantic taxonomy.

---

# 6. FA2

Relevant directory:

```

experiments/FA2\_E1\_minimal\_invariant\_compression\_test/

```

## Question

Can witness classes be explained by a compact family of semantic invariants?

---

## Result

[FACT]

Coverage progression:

```

R1

19.25%

```

R3

```

76.64%

```

R4-proxy

```

99.83%

```

Oracle

```

100%

```

---

## Important observation

[FACT]

The non-oracle proxy achieved almost complete witness coverage.

However,

the experiment intentionally refused to interpret this as constructive success.

The reason is that only false-safe witnesses were analysed.

True SAFE states were absent.

Precision therefore could not be estimated.

---

## Consequence

[INFERENCE]

Witness coverage alone is insufficient.

Candidate invariants must also discriminate false-safe states from ordinary
SAFE states.

---

# 7. Empirical Summary

The following statements are now experimentally established.

[FACT]

Projection blindness exists.

[FACT]

No dominant monotonicity-breaking mechanism has been identified.

[FACT]

MB5 is functionally split.

[FACT]

Semantic layers exist and can become unintentionally merged.

[FACT]

False-safe witnesses exhibit strong semantic structure.

[FACT]

Compact witness compression is possible.

[FACT]

Constructive refinement remains unproven because discriminative power has not
yet been measured.

---

# 8. What Has NOT Been Demonstrated

The following statements remain unsupported.

No experiment has demonstrated that:

- a faithful abstraction has been constructed;

- minimal semantic information is always sufficient;

- compact refinement always exists;

- history summaries are compatible with WSTS;

- witness compression implies good classification performance.

These questions remain open.

---

# 9. Empirical Conclusions

The experimental program has not yet produced a faithful abstraction.

However, it has transformed the problem.

The project no longer asks:

> Which variables should be added?

Instead, the experimentally supported question becomes:

> Which minimal semantic information distinguishes concrete states that are
> merged by the current abstraction?

This question constitutes the empirical foundation of the Faithful Abstraction
program.
