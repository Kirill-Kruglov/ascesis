# FA2.E1 — Minimal Invariant Compression Test

## Specification v1.0

```markdown id="z6c4cm"
# FA2.E1
## Minimal Invariant Compression Test

Purpose:
Test whether false-safe witnesses from FA1.E1 can be covered by a compact sequence of missing-information invariants.

This is not a shield synthesis experiment.
Do not modify Justitia.
Do not modify collapse definition.
Do not modify the 18.0 shield.
Do not claim safety.

This experiment tests H_FA1.1:

Faithful abstraction requires a small set of missing information invariants,
but these invariants are not limited to omitted collapse clauses;
they include temporal, history/control, and policy-visible observation invariants.

---

# Inputs

Use outputs from:

experiments/FA1_E1_false_safe_witness_taxonomy/outputs/

Required input files:
- witness_taxonomy.csv
- witness_class_summary.json or final_report.md
- hypothesis_assessment.json
- representative_witnesses.md
- ambiguous_witnesses.md

Use BA4.1 layer audit if needed:

experiments/BA4_layer_audit/justitia_layer_audit.md
experiments/BA4_layer_audit/layer_audit.csv
experiments/BA4_layer_audit/function_audit.csv

No new Justitia simulations are required unless Codex determines FA1 output lacks fields needed for compression analysis.
If new simulation is needed, report exactly why.

---

# Core Question

Can a small ordered set of eligible information invariants explain most false-safe witnesses?

---

# Candidate Invariants

Test at minimum the following invariant families.

## I1 — Omitted collapse clauses

- failed_zone_count >= 4
- total_mass < 35

Expected to cover:
- spread_blind
- mass_blind

Layer:
- L4 eligible

---

## I2 — Policy-visible concentration

- Obs.resource_concentration > 0.62
- or equivalent policy-visible concentration threshold from FA1

Expected to cover:
- policy_visible_concentration_blind

Layer:
- conditional L2/L3

Important:
Do not substitute reporting resource_hhi.

---

## I3 — History / delayed consequence summary

Compact summaries of:
- response_to_aid
- neighbor_delta
- last_aid

Examples:
- any negative response_to_aid flag
- neighbor_delta below threshold
- last_aid high and response low
- delayed harm signal present

Expected to cover:
- history_blind

Layer:
- conditional L2/L3

Codex may propose the smallest threshold/boolean summary that reproduces FA1 history class labels.
Do not use raw full history unless necessary.

---

## I4 — Bounded future-risk / time-to-collapse proxy

Candidate summaries:
- time_to_collapse <= k
- future collapse within horizon h
- bounded reachability class
- monotone risk proxy if available

Expected to cover:
- forward_dynamics_blind

Layer:
- L4 plus conditional L1 temporal

Important:
This is the most dangerous invariant.
It may be circular if defined using future labels only.
Therefore report two versions:

1. oracle temporal invariant:
   uses future collapse label/time-to-collapse directly;
   allowed only for measuring theoretical compressibility.

2. non-oracle proxy candidate:
   uses current-state variables available at step time;
   may be approximate.

---

## I5 — Unknown/mixed resolver

Try to identify whether unknown_or_mixed witnesses become covered by combinations of I1–I4.

Do not force assignment.
If no compact explanation exists, keep them unresolved.

---

# Ordered Refinement Sets

Evaluate cumulative coverage for at least these sets:

R0:
current 18.0 abstraction only

R1:
R0 + I1

R2:
R1 + I2

R3:
R2 + I3

R4-oracle:
R3 + I4 oracle temporal invariant

R4-proxy:
R3 + I4 non-oracle proxy candidate

R5:
R4 + best compact mixed resolver, if any

---

# Measurements

For every refinement set report:

- witness coverage count
- witness coverage fraction
- newly covered witnesses
- residual unknown/mixed
- number of invariant coordinates added
- coordinate type:
  threshold / count / aggregate / temporal / history / policy-control
- layer eligibility
- whether invariant is oracle or non-oracle
- estimated state-space blowup
- estimated WSTS compatibility risk:
  low / medium / high
- monotonicity risk:
  low / medium / high
- circularity risk:
  none / low / medium / high

---

# Compression Metrics

Compute:

1. Coverage@k

Coverage fraction by first k invariants.

2. Marginal coverage

Additional witnesses covered by each invariant.

3. Compression ratio

witnesses covered / invariant coordinates added.

4. Eligible compression ratio

witnesses covered by non-oracle, layer-eligible invariants / invariant coordinates.

5. Residual complexity

fraction not covered by compact invariants.

---

# Decision Logic

## Case A — Compact_non_oracle_supported

A small non-oracle invariant set covers most witnesses.

Suggested threshold:
top 3–4 non-oracle invariants cover >= 0.80
and unknown/mixed <= 0.10.

Interpretation:
H_FA1.1 strongly supported.
Proceed to CEGAR-like refinement experiment.

---

## Case B — Compact_only_with_oracle_temporal

High coverage requires oracle time-to-collapse or future labels.

Interpretation:
Current witnesses are compressible, but not constructively useful.
H_FA1.1 weakened.
Need non-oracle temporal proxy research.

---

## Case C — History_temporal_barrier

History/temporal classes dominate and cannot be captured by compact non-oracle invariants.

Interpretation:
Faithful abstraction may require richer memory/reachability structure.
WSTS path at risk.

---

## Case D — Noncompact_refinement

Coverage grows slowly with invariants or many raw variables are needed.

Interpretation:
H_FA1 weakened or rejected.
Minimal missing information may not remain compact.

---

## Case E — Inconclusive

Input data insufficient or invariant definitions unstable.

---

# Required Outputs

Directory:

experiments/FA2_E1_minimal_invariant_compression_test/outputs/

Required files:

- invariant_catalog.csv
- refinement_sets.csv
- coverage_by_refinement.csv
- marginal_coverage.csv
- residual_witnesses.csv
- temporal_oracle_analysis.json
- non_oracle_proxy_analysis.json
- wsts_risk_assessment.md
- compression_summary.json
- hypothesis_assessment.json
- final_report.md
- implementation_notes.md

---

# Required Report Questions

1. How much coverage is achieved by omitted collapse clauses alone?

2. How much coverage is achieved by adding policy-visible concentration?

3. How much coverage is achieved by adding compact history summaries?

4. Is high coverage possible without oracle temporal information?

5. Which invariant has the highest marginal coverage?

6. Which invariant has the highest compression ratio?

7. What fraction remains unresolved?

8. Which invariants are WSTS-compatible or WSTS-risky?

9. Does FA2 support compact faithful refinement?

10. What is the strongest counterexample against H_FA1.1?

---

# Critical Instructions

Actively try to falsify H_FA1.1.

Do not count future-label oracle invariants as constructive refinement.

Do not treat reporting-only metrics as eligible.

Do not use capture_index or permanence as safety evidence.

Do not propose a new shield.

Do not claim safety.

If compact coverage is achieved only by oracle time-to-collapse,
say so clearly.

If non-oracle proxies fail,
that is a valuable result.
```
