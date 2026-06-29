# T-C — Monotonicity of Faithful Justitia Abstraction

## Guarded Specification v1.0

```markdown
# T-C
## Monotonicity of Faithful Justitia Abstraction

---

# Purpose

This experiment tests the remaining open horn of the applied Justitia trilemma.

The trilemma:

F — Faithfulness:
The abstraction must preserve the concrete Justitia collapse boundary.

D — Decidability:
The abstraction must support WSTS-style decidable reachability / coverability.

P — Finite presentation:
The abstraction must be finitely specified.

Analytical review has narrowed the problem:

- finite-zone spread counting does not itself destroy wqo;
- mean, spread, and mass collapse clauses are upward-closed under a natural badness order;
- bounded monotone history summaries can remain wqo-compatible;
- the remaining danger is transition monotonicity under consequence-gated / sword-like history-dependent response.

Therefore T-C tests:

Does a faithful abstraction of Justitia preserve monotonicity of transitions?

---

# Critical Guard

Do NOT run this test on the old 18.0 two-counter abstraction.

18.1 already showed that abstraction is not faithful.

Testing monotonicity on an unfaithful abstraction repeats the core error of 18.0.

The required order is:

1. Run or consume FA2.5 discrimination/fidelity gate.
2. Construct or select an abstraction candidate that passes the gate.
3. Only then perform T-C monotonicity testing.

If no candidate passes FA2.5, report:

T-C not applicable:
no faithful abstraction candidate available.

---

# Required Input

A candidate abstraction A containing at minimum:

1. mean-welfare / mean-deficit coordinate;
2. failed-zone count or equivalent spread coordinate;
3. total-mass / mass-deficit coordinate;
4. compact history/control/consequence summaries required by FA2.5;
5. policy-visible concentration if required by FA2.5.

All coordinates must be layer-eligible under BA4.1.

Reporting-only metrics are forbidden:
- capture_index;
- permanence;
- dashboard-only ratios;
- reporting-only HHI.

---

# Analytical Assumptions Already Closed

These should be recorded but not re-tested unless implementation contradicts them.

## T-A — wqo state space

For finite-zone badness vectors, total mass deficit, and a finite number of monotone history counters,
the product order is wqo.

Reason:
finite products of wqo are wqo.

## T-B — upward-closed collapse set

The concrete collapse predicate:

mean_welfare < 0.32
OR count(zone_welfare < 0.20) >= 4
OR total_mass < 35

is upward-closed under the natural badness order:

- lower welfare = worse;
- more failed zones = worse;
- lower total mass = worse.

Spread counting is not the obstacle.

---

# Open Test

## T-C — Transition monotonicity

For abstraction A and badness order ≤:

If

s ≤ s'

and

s -> t

then there should exist t' such that

s' -> t'

and

t ≤ t'

or an accepted WSTS-compatible simulation variant.

Because Justitia has stochastic/semi-random dynamics, Codex must define the operational monotonicity test carefully.

Acceptable approaches:

1. Coupled-seed transition comparison.
2. Enumerated local transition templates.
3. Sampled witness search over abstract states.
4. Symbolic/static analysis of transition functions where feasible.

Document which is used.

---

# Main Risk Mechanisms

Focus especially on transitions involving:

- consequence-gated response;
- sword / containment / audit response;
- delayed observation;
- response_to_aid;
- neighbor_delta;
- policy-visible resource concentration;
- allocation normalization;
- migration;
- adaptive lineage dynamics.

These are the likely monotonicity breakers.

---

# Required Outputs

Directory:

experiments/TC_monotonicity_faithful_abstraction/outputs/

Required files:

- tc_input_candidate.json
- fa25_gate_reference.json
- abstraction_coordinates.csv
- order_definition.md
- monotonicity_test_method.md
- monotonicity_witnesses.csv
- transition_family_summary.csv
- nonmonotone_transition_examples.md
- overapproximation_options.md
- tc_decision.json
- final_report.md

---

# Required Measurements

Report:

1. number of tested ordered pairs s ≤ s';
2. number of monotonicity violations;
3. violation rate;
4. violation rate by transition family;
5. minimal counterexample examples;
6. whether violations depend on history variables;
7. whether violations depend on policy-visible consequence/sword response;
8. whether conservative over-approximation can restore monotonicity;
9. whether the restored abstraction becomes vacuous;
10. whether T-C supports or rejects faithful WSTS expressibility.

---

# Decision Logic

## Case 0 — No faithful candidate

FA2.5 fails or no candidate passes precision/fidelity.

Decision:

No_faithful_candidate.

Interpretation:

T-C cannot be tested yet.
The justitia faithful-boundary path fails earlier.

---

## Case A — Monotone

No material monotonicity violations.

Decision:

FDP_compatible_candidate.

Interpretation:

Faithfulness, WSTS-style decidability, and finite presentation may be jointly compatible for this abstraction candidate.

Next step:
attempt shield synthesis / coverability on candidate.

---

## Case B — Nonmonotone but conservatively recoverable

Violations exist,
but a documented over-approximation restores monotonicity while retaining non-vacuous precision.

Decision:

Conservative_WSTS_path_supported.

Interpretation:

Faithful exact abstraction may be nonmonotone,
but a safe conservative shield path may remain viable.

---

## Case C — Nonmonotone and over-approximation vacuous

Violations exist,
and every plausible monotone over-approximation collapses into trivial unsafe/all-doomed behaviour.

Decision:

Trilemma_fatal_for_Justitia.

Interpretation:

Justitia is likely not WSTS-expressible as a faithful useful shield.

This becomes a fundamental negative result for the current Justitia substrate candidate.

---

## Case D — Inconclusive

Sampling insufficient,
candidate unclear,
or monotonicity relation ill-defined.

Decision:

Inconclusive.

---

# Strong Falsification Targets

Try to falsify the optimistic path.

Find pairs s ≤ s' where:

- worse history causes weaker sword response;
- better current state with worse history receives stronger containment;
- delayed consequence flips policy response nonmonotonically;
- allocation normalization improves a worse state relative to a better state;
- migration or adaptive lineage dynamics reverses order.

---

# Interpretation Rule

Do not claim Justitia is WSTS-expressible unless:

1. candidate abstraction passes fidelity/discrimination gate;
2. collapse set is upward-closed;
3. transition monotonicity passes or is conservatively restored;
4. over-approximation is non-vacuous.

All four are required.

---

# Final Report Must Answer

1. Was FA2.5 passed?
2. What abstraction candidate was tested?
3. What order was used?
4. Is the collapse set upward-closed?
5. Are transitions monotone?
6. If not, which transition families violate monotonicity?
7. Can conservative over-approximation restore monotonicity?
8. Does the restored abstraction preserve useful precision?
9. Does T-C support a faithful WSTS path for Justitia?
10. Should Justitia remain a candidate substrate?
```
