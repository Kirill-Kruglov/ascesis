# JB0.E1 — Standard CEGAR Boundary Assessment

## Specification v1.0

```markdown
# JB0.E1
## Standard CEGAR Boundary Assessment for Justitia

Purpose:
Test whether standard history/predicate CEGAR can produce a practically useful conservative Justitia boundary.

This is not FA.
This is not a new abstraction theory.
This is not T-C.
This is not shield synthesis for deployment.

It is a boundary assessment:
How far can standard refinement go before plateau, explosion, or useful success?

---

# Goal Anchor

The long-term project goal remains:

Build an analytically understandable, safety-faithful substrate for future LLM training, where world-structure is derived rather than learned from internet-scale proxy data.

Justitia is only one candidate substrate.

This experiment asks whether Justitia still has a viable Door-1 path through standard CEGAR-style refinement.

---

# Inputs

Use current Justitia.

Do not modify:
- Justitia source semantics;
- collapse definition;
- environment dynamics;
- training loop;
- Level B;
- shield deployment.

Use prior outputs if useful:
- experiments/FA1_E1_false_safe_witness_taxonomy/outputs/
- experiments/FA2_5_E1_candidate_validation/outputs/
- experiments/BA4_layer_audit/

---

# Hypotheses

H0 — Useful standard CEGAR path exists.

A standard predicate/history refinement can produce a useful conservative boundary with acceptable precision/recall and manageable complexity.

H1 — CEGAR plateaus.

Refinement improves early, then stalls below useful quality.

H2 — CEGAR explodes.

Useful quality requires too many predicates/history variables/state cells.

H3 — CEGAR becomes vacuous.

Conservative boundary avoids false-safe only by classifying too much as unsafe/doomed.

---

# Required Baselines

B0:
Current 18.0 abstraction.

B1:
Best FA2.5 history CEGAR baseline.

B2:
Raw current-state baseline from FA2.5.

JB0 must compare against these.

---

# Refinement Families

Use only standard, interpretable CEGAR/predicate-style refinements.

Allowed families:

1. Current collapse predicates:
   - mean_welfare threshold;
   - failed_zone_count;
   - total_mass.

2. History variables:
   - last_aid;
   - response_to_aid;
   - neighbor_delta;
   - delayed observation summaries;
   - rolling harm / response windows.

3. Control/policy variables:
   - containment_timer;
   - audit/containment active;
   - allocation class;
   - policy-visible concentration.

4. Simple trajectory summaries:
   - rolling welfare loss;
   - rolling mass loss;
   - rolling failed-zone count;
   - bounded k-window summaries.

5. Conservative predicates:
   - risk bands;
   - thresholded monotone danger flags.

Forbidden:
- oracle time-to-collapse;
- future labels;
- capture_index as safety evidence;
- permanence;
- reporting-only metrics;
- dashboard-only ratios;
- learned opaque embeddings;
- arbitrary high-dimensional raw state without explicit CEGAR justification.

---

# Refinement Loop

Implement an iterative refinement loop.

At each iteration:

1. Train/select the current predicate boundary using training groups.
2. Evaluate on held-out trajectory groups.
3. Extract remaining false-safe witnesses.
4. Choose the next predicate/history variable using standard CEGAR logic:
   it must separate a meaningful subset of current false-safe witnesses.
5. Add it.
6. Re-evaluate.

Stop when any stop condition triggers.

---

# Stop Conditions

Stop if:

1. Useful success achieved.
2. Two consecutive refinements improve balanced accuracy by < 0.005.
3. Two consecutive refinements improve false-safe rate by < 0.005.
4. Predicate count exceeds predefined budget.
5. Abstract state count / cell count exceeds budget.
6. Conservative boundary becomes vacuous.

Budgets must be reported and justified.

Suggested initial budgets:
- max predicates: 20
- max abstract cells: 100,000
- max history window: 8
- max iterations: 20

Codex may adjust with justification.

---

# Metrics

For each iteration report:

- precision;
- recall;
- specificity;
- false-positive rate;
- false-negative rate;
- false-safe rate;
- false-unsafe / false-doomed rate;
- ROC-AUC;
- PR-AUC;
- balanced accuracy;
- confusion matrix;
- number of predicates;
- abstract state/cell count;
- history depth;
- layer eligibility;
- conservative/vacuity score.

---

# Useful Boundary Criteria

A useful conservative boundary requires:

1. false-safe materially below B0 and B1;
2. recall high enough not to miss future collapse;
3. precision not vacuous;
4. false-positive rate not catastrophic;
5. predicate count manageable;
6. all predicates layer-eligible;
7. no oracle information.

Suggested thresholds:

- recall >= 0.90
- precision >= 0.80
- false-safe rate <= 0.10
- false-positive rate <= 0.25
- predicates <= 20

These are not safety claims.
They are practical usefulness thresholds for boundary assessment.

---

# Decision Logic

Case A — Useful_CEGAR_boundary

Criteria:
A standard history/predicate refinement reaches useful boundary thresholds without oracle information, without vacuity, and with manageable complexity.

Interpretation:
Justitia remains viable as a substrate candidate.
Next step may be monotonicity / WSTS analysis on the resulting candidate.

---

Case B — CEGAR_plateau

Criteria:
Refinement improves early but stalls below useful thresholds.

Interpretation:
Standard CEGAR is insufficient for Justitia.
This is evidence against Door-1 via standard refinement.

---

Case C — CEGAR_state_explosion

Criteria:
Quality improves only by exceeding predicate/cell/history budgets.

Interpretation:
Justitia may require too much history/path information for a compact analytically useful boundary.

---

Case D — Conservative_but_vacuous

Criteria:
False-safe is reduced, but precision collapses or most states become doomed/unsafe.

Interpretation:
A conservative shield may be formally safe but not useful for the project goal.

---

Case E — Inconclusive

Implementation or data insufficient.

---

# Required Outputs

Directory:

experiments/JB0_E1_standard_cegar_boundary_assessment/outputs/

Required files:

- baseline_metrics.csv
- refinement_trace.csv
- predicate_catalog.csv
- witness_reduction_by_iteration.csv
- heldout_metrics.csv
- confusion_matrices.csv
- abstract_state_growth.csv
- plateau_analysis.json
- vacuity_analysis.json
- cegar_boundary_decision.json
- remaining_witnesses.md
- best_boundary_definition.md
- implementation_notes.md
- final_report.md

---

# Final Report Must Answer

1. Does standard CEGAR produce a useful boundary?
2. How far does it improve over 18.0?
3. How far does it improve over FA2.5 history baseline?
4. Which predicates were selected?
5. Did refinement plateau?
6. Did state/cell count explode?
7. Did the conservative boundary become vacuous?
8. Are selected predicates layer-eligible?
9. Should Justitia remain a Door-1 substrate candidate?
10. Should T-C be considered after this result?

---

# Discipline

Actively try to falsify the usefulness of standard CEGAR.

Do not rescue the experiment by inventing non-standard FA machinery.

Do not claim safety.

Do not run T-C.

Do not proceed to shield synthesis.

The purpose is to identify the practical boundary of the standard method on Justitia.
```
