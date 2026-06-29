# Experiment BA2.E1

## Semantic Benefit vs Structural Cost Map

```markdown
# Experiment BA2.E1

## Semantic Benefit vs Structural Cost

---

# Purpose

This experiment is diagnostic.

It does NOT attempt to improve the shield.

It does NOT search for a better abstraction.

It attempts to falsify the following hypothesis:

H_BA2

    Mechanisms that violate monotonicity are
    simultaneously the mechanisms that reduce
    semantic blindness.

If false,

then at least one mechanism introduces structural
complexity without providing corresponding semantic value.

Such a mechanism becomes the strongest candidate
for elimination or redesign.

---

# Scientific Question

For every mechanism class MB_i measure two independent quantities.

Semantic Benefit

and

Structural Cost.

The experiment intentionally separates them.

---

# Inputs

Use exactly the current Justitia implementation.

Use the current collapse definition.

Use the current 18.0 abstraction.

Reuse BA1.E1 diagnostic infrastructure whenever possible.

Do NOT modify the shield.

Do NOT retrain anything.

---

# Mechanism Classes

MB1 Memory

MB2 Relative Resource Competition

MB3 Interpretive Policy

MB4 Adaptive Population Dynamics

MB5 Relative Observables

Codex may revise the taxonomy if BA1.E1 evidence suggests
a cleaner decomposition.

Such revisions must be documented.

---

# Semantic Benefit

For every mechanism estimate how much semantic information
is lost if the mechanism is removed.

This should NOT be represented by a single metric.

At minimum report:

Δ false_safe

Δ false_unsafe

Δ pure_blindness

Δ collapse recall

Δ collapse precision

Δ future collapse prediction quality

Δ clause coverage

If Codex finds better diagnostics,
they may be added.

---

# Structural Cost

Estimate how much structural complexity the mechanism introduces.

Possible indicators include:

monotonicity witness count

minimal counterexample count

history dependence

global coupling

relative observables

non-local transitions

transition branching

interaction degree

Do NOT force one formula.

Document the chosen definition.

---

# Benefit / Cost Plane

Each mechanism becomes one point.

x-axis

Structural Cost

y-axis

Semantic Benefit

Example

            high benefit

                MB3

      MB1

                    MB4

-------------------------------

MB2             MB5

          low benefit

        low cost        high cost

The actual geometry is unknown.

---

# Dominated Mechanisms

For every mechanism determine whether another mechanism
strictly dominates it.

Definition

Mechanism A dominates mechanism B if

Benefit(A) >= Benefit(B)

and

Cost(A) <= Cost(B)

with at least one strict inequality.

Report the dominance graph.

---

# Pareto Frontier

Construct the Pareto frontier.

Question:

Which mechanisms provide the best semantic benefit
per unit structural cost?

---

# Critical Challenge

Codex should actively attempt to falsify H_BA2.

Possible falsifications include:

Case 1

A mechanism has

high structural cost

low semantic benefit.

This contradicts H_BA2.

Case 2

A mechanism has

low structural cost

high semantic benefit.

This suggests an efficient abstraction target.

Case 3

No measurable trade-off exists.

The hypothesis itself is probably wrong.

---

# Required Outputs

outputs/

semantic_benefit.csv

structural_cost.csv

benefit_cost_plane.csv

dominance_graph.csv

pareto_frontier.csv

mechanism_rankings.csv

tradeoff_examples.md

counterexamples.md

hypothesis_assessment.json

final_report.md

---

# Required Questions

1.

Does every monotonicity breaker provide semantic benefit?

2.

Are there dominated mechanisms?

3.

Is there a Pareto frontier?

4.

Which mechanisms are Pareto-optimal?

5.

Which mechanism has the worst benefit/cost ratio?

6.

Which mechanism should be investigated first?

7.

What is the strongest counterexample against H_BA2?

---

# Decision Logic

Support H_BA2

if

all mechanisms lie close to the Pareto frontier
and no strongly dominated mechanism exists.

Reject H_BA2

if

one or more mechanisms exhibit

high structural cost

but

little measurable semantic benefit.

Mixed

if

trade-offs exist but only for part
of the taxonomy.

---

# Freedom

Codex is encouraged to propose better
benefit and cost metrics.

The experiment is about the existence
of the trade-off,

not about one specific scoring function.

Any disagreement with the current analytical model
must be reported explicitly.

---

# Success Criterion

The experiment succeeds if it reduces uncertainty
about whether structural complexity is necessary
or accidental.

Improving shield quality is explicitly out of scope.

Negative results are scientifically valuable.
```
