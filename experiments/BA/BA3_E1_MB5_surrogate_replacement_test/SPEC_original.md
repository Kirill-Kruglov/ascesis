# Experiment BA3.E1 — MB5 Surrogate Replacement Test

## Specification v1.0

```markdown
# Experiment BA3.E1
## MB5 Surrogate Replacement Test

---

# Purpose

This is a diagnostic replacement experiment.

It is NOT a shield-repair experiment.

It is NOT Experiment 18.2.

It must not modify the real collapse definition, the 18.0 shield abstraction, or the shield threshold.

The purpose is to test whether MB5 relative observables are semantically necessary or merely representational overhead.

BA2.E1 identified MB5 as the worst benefit/cost mechanism:

- high structural cost;
- very low measured semantic benefit;
- worst benefit/cost ratio;
- cleanly comparable, unlike MB4.

Therefore MB5 is the first candidate for controlled replacement.

---

# Target Mechanism

MB5 = Relative Observables.

Examples:

- resource HHI;
- exploit share;
- cooperative share;
- concentration ratios;
- capture-index ratio components;
- any observable whose value depends on ratios or relative shares rather than monotone absolute deficits.

Important distinction:

This experiment targets MB5 as used by policy/diagnostic abstraction.

It must not delete all reporting metrics unless necessary.

The goal is not to blind the output layer.

The goal is to test whether relative observables are necessary for collapse fidelity or whether they can be replaced by simpler monotone-compatible surrogates.

---

# Scientific Question

Can MB5 be replaced by simpler monotone-compatible surrogate observables without increasing dangerous false-safe error?

---

# Main Hypotheses

## H0 — MB5 Necessary

Relative observables carry semantic information that cannot be replaced by simpler monotone-compatible surrogates.

Prediction:

All surrogate replacements worsen false-safe, pure blindness, collapse recall, or forward collapse prediction.

---

## H1 — MB5 Representational Overhead

Relative observables add structural cost without corresponding semantic value.

Prediction:

At least one surrogate replacement matches or improves baseline fidelity while reducing structural cost / monotonicity witness count.

---

## H2 — MB5 Functionally Split

Some MB5 sub-observables are useful while others are overhead.

Prediction:

Partial replacements outperform full removal and reveal a smaller necessary subset.

---

# Strict Constraints

Do NOT:

- change Justitia source code permanently;
- change collapse definition;
- change collapse thresholds;
- change 18.0 shield abstraction;
- tune shield parameters;
- train any model;
- run Level B;
- claim safety improvement.

All changes must be implemented as experiment-local subclasses, wrappers, or monkey patches inside the BA3.E1 experiment directory.

---

# Required Baselines

Use the same diagnostic grid as BA1.E1 unless there is a strong reason not to.

Required baseline runs:

1. baseline Justitia
2. BA1 MB5 removal / neutralization
3. new surrogate variants S1–S4 below

If BA1 outputs can be reused exactly, document reuse.
If rerun is necessary, use fixed seeds and report them.

---

# Surrogate Variants

Codex should implement the following surrogate families if feasible.

If a surrogate is impossible or invalid, report why.

---

## S1 — Absolute Deficit Surrogate

Replace relative concentration observables used in policy/scoring with absolute monotone deficit-style quantities.

Examples:

Instead of:

    resource_hhi_zone
    exploit_share
    cooperative_share
    concentration ratio

use quantities such as:

    total_exploit_mass_zone
    total_noncoop_mass_zone
    aid_interception_volume_zone
    neighbor_harm_volume_zone
    extraction_volume_zone
    mass_deficit_zone

All surrogates should be monotone or at least monotone-like under the deficit order:

    lower welfare = worse
    higher harm/extraction/interception = worse
    lower mass = worse

Goal:

Test whether ratios are unnecessary if absolute harmful mass / harm volume is retained.

---

## S2 — Thresholded Boolean Surrogate

Replace relative observables by threshold flags.

Examples:

    high_extraction_flag
    high_interception_flag
    high_neighbor_harm_flag
    low_mass_flag
    failed_zone_flag

Avoid exact ratios.

Use coarse monotone boolean indicators where possible.

Goal:

Test whether coarse finite thresholds preserve enough collapse signal while reducing structural complexity.

---

## S3 — Conservative Upper-Bound Surrogate

Replace relative observables by conservative over-approximations.

Examples:

    max_possible_exploit_pressure
    upper_bound_neighbor_harm
    upper_bound_aid_interception
    upper_bound_concentration_risk

The surrogate may overestimate danger.

False unsafe may increase.

False safe should not increase.

Goal:

Test whether safety-relevant MB5 information can be represented as conservative monotone risk rather than precise ratio.

---

## S4 — MB5 Split Test

Split MB5 into subfamilies.

At minimum:

S4a:

Policy-visible concentration observables only.

S4b:

Final/reporting ratio metrics only.

S4c:

18.0 projection-visible resource_hhi only.

S4d:

Capture-index components only.

Goal:

Determine whether MB5 is one mechanism or a bundle of distinct functions.

---

# Required Measurements

For each run compute:

false_safe_rate

false_unsafe_rate

pure_blindness

future_collapse_rate

current_collapse_rate

collapse recall

collapse precision

balanced collapse prediction quality

clause coverage:

- mean
- spread
- mass

clause overlap matrix

monotonicity witness count

minimal counterexample count

structural cost proxy

semantic benefit proxy

benefit/cost ratio

dominance relation against baseline / MB5 removal

---

# Required Comparisons

Compare each surrogate against:

1. baseline Justitia
2. MB5 removal
3. best Pareto mechanism from BA2.E1 if available
4. BA1 baseline false-safe

Important:

A surrogate is not successful merely because false-safe decreases.

It must not achieve this by severe semantic shift.

Therefore report semantic validity using the same or stricter criterion as BA1.E1.

---

# Semantic Validity Gate

A surrogate is invalid if it causes severe semantic shift.

At minimum flag severe shift if:

- future_collapse_rate changes by more than 0.35 absolute;
- shield_acceptance_rate changes by more than 0.45 absolute;
- mean welfare changes by more than 0.25 absolute;
- collapse disappears;
- all policies become trivially safe or trivially doomed.

Codex may add stricter invalidity checks.

Invalid variants may still be reported, but cannot support H1.

---

# Decision Logic

## Case A — MB5 Necessary

All valid surrogates are worse than baseline on false-safe or pure blindness.

Conclusion:

Support H0.

MB5 cannot be replaced by tested monotone-compatible surrogates.

---

## Case B — MB5 Overhead

At least one valid surrogate:

- matches or improves baseline false-safe;
- does not increase pure blindness materially;
- reduces structural cost or monotonicity witness count;
- does not trigger semantic validity failure.

Conclusion:

Support H1.

MB5 is representational overhead under current diagnostics.

---

## Case C — MB5 Split

Some subfamilies are replaceable and others are not.

Conclusion:

Support H2.

Refine MB5 into smaller mechanisms.

---

## Case D — Inconclusive

Surrogates are invalid, inseparable, or dominated by implementation artifacts.

Conclusion:

No ontology update except method warning.

---

# Strong Falsification Targets

The experiment should actively try to falsify the current interpretation.

Try to find:

1. a surrogate that preserves fidelity with lower structural cost;
2. a subfamily of MB5 that is clearly necessary;
3. a case where ratios are indispensable;
4. a case where apparent improvement comes only from semantic collapse disappearance.

---

# Required Outputs

Directory:

    experiments/BA3_E1_MB5_surrogate_replacement_test/

Required files:

    outputs/baseline_summary.json
    outputs/MB5_removal_summary.json

    outputs/S1_absolute_deficit_summary.json
    outputs/S2_threshold_boolean_summary.json
    outputs/S3_conservative_upper_bound_summary.json

    outputs/S4a_policy_visible_concentration_summary.json
    outputs/S4b_reporting_ratios_summary.json
    outputs/S4c_projection_resource_hhi_summary.json
    outputs/S4d_capture_components_summary.json

    outputs/surrogate_comparison.csv
    outputs/semantic_validity.csv
    outputs/benefit_cost_surrogate_plane.csv
    outputs/dominance_graph.csv
    outputs/pareto_frontier.csv
    outputs/monotonicity_witnesses.csv
    outputs/counterexamples.md
    outputs/mechanism_split_assessment.md
    outputs/hypothesis_assessment.json
    outputs/implementation_notes.md
    outputs/final_report.md

---

# Required Report Questions

1. Can MB5 be replaced by any valid surrogate?

2. Which surrogate has the best false-safe behavior?

3. Which surrogate has the best benefit/cost ratio?

4. Does any surrogate reduce monotonicity witness count?

5. Does any surrogate preserve collapse distribution?

6. Is MB5 necessary, overhead, or split?

7. Which MB5 subfamily is most suspicious?

8. Which MB5 subfamily appears indispensable?

9. What is the strongest counterexample against H1?

10. What is the strongest counterexample against H0?

---

# Implementation Guidance

Prefer wrapping/subclassing over editing Justitia.

Keep all original code untouched.

If a quantity cannot be replaced without changing too much of the system, mark the variant invalid rather than forcing it.

Document exact source functions touched by wrappers.

Expected relevant functions from BA0.2:

- `_resource_hhi_zone`
- `_score`
- `_bad_consequence`
- `choose_alloc`
- `_trajectory_snapshot`
- `metrics`
- capture-index computation

Do not assume this list is complete.

---

# Interpretation Rules

Do not call a surrogate successful if it wins by making collapse impossible.

Do not call a surrogate successful if it improves one metric while strongly worsening false-safe.

Do not call a surrogate successful if it only affects reporting metrics and not transition behavior.

Do not call MB5 necessary unless all valid surrogates fail.

Do not call MB5 overhead unless at least one valid surrogate passes the semantic validity gate.

---

# Final Decision Values

Use exactly one of:

    MB5_necessary
    MB5_representational_overhead
    MB5_functionally_split
    Inconclusive

---

# Success Criterion

This experiment succeeds if it determines whether MB5 is:

- semantically necessary;
- replaceable overhead;
- a mixture of necessary and replaceable submechanisms;
- or currently inseparable.

The experiment is successful even if every surrogate fails, provided the failure is informative and traceable.
```
