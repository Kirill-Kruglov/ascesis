# Experiment 17C — Consequence Invariance vs Interpretive Closure

## Project

`17C_interpretive_closure_test`

## Purpose

Test whether consequence-invariant classes are sufficient for semantic stability, or whether semantic stability requires an additional closed interpretation loop.

This experiment attacks the current working hypothesis after 17A.2:

```text
H2-rel:
Meaning = globally forced consequence class
relative to representation-preserving transformations.
```

The competing hypothesis is:

```text
H3:
Meaning = globally forced consequence class
+ closed interpretation loop.
```

## Background

Experiment 17A.2 showed:

```text
Backbone survives representation-preserving edits.
Backbone fails under theory-changing edits.
```

This supports representation-relative consequence invariance.

But it does not test whether consequence invariance alone is enough to count as semantic content.

Biological theories of semantic closure suggest that meaning may require a loop:

```text
symbol / code
→ derived consequences
→ interpreter / phenotype
→ maintains or constrains future interpretation
```

This experiment asks whether adding such a loop changes the stability, selectivity, or non-triviality of consequence classes.

---

# Research Question

Are globally forced consequence classes sufficient by themselves, or do they require an interpretive closure mechanism to become semantically non-arbitrary?

---

# Core Design

Construct two substrates using the same DAG generator and consequence verifier family as 17A.2.

## Substrate A — Open Consequence Substrate

A standard consequence system:

```text
DAG
→ consequence signature
→ consequence class
```

No feedback from derived consequences into future admissibility, interpretation, or generation.

## Substrate B — Closed Interpretation Substrate

A modified system with an internal interpreter state.

```text
DAG
→ consequence signature
→ interpreter state
→ admissibility / weighting / survival of future consequences
→ updated interpreter state
```

The interpreter must be internal and rule-governed.

It must not use external labels, internet data, human semantic judgments, or learned embeddings.

---

# Key Constraint

Do not make Substrate B simply stronger by adding more information.

The closure loop must only use information already derivable from the substrate.

Allowed examples:

```text
consequence frequency
causal role persistence
intervention sensitivity
dependency centrality
self-maintenance score
reuse in future derivations
```

Forbidden examples:

```text
LLM semantic labels
human-written categories
external ontologies
text embeddings
internet knowledge
hand-picked "important" variables
```

---

# Operational Definitions

## Consequence Signature

Reuse the existing consequence verifier machinery from 17A.2 where possible.

A consequence signature may include:

```text
Reachable(X, Y)
Ancestor(X, Y)
Blocked(X, Y | Z)
Independent(X, Y | Z)
Effect(X -> Y)
P(Y | X)
P(Y | do(X))
P(Y | do(X), Z)
```

## Interpretation State

For each generated world/DAG, define an interpreter state `I_t`.

`I_t` must summarize which consequences are functionally active in maintaining the substrate’s own future derivations.

Possible implementation:

```text
I_t[c] = score for consequence c
```

where score depends only on internal quantities, for example:

```text
persistence across representation-preserving variants
reuse in downstream derivations
sensitivity under interventions
role in maintaining reachable derivation paths
```

## Closed Loop

A consequence is semantically closed if it both:

1. is derivable from the current substrate;
2. affects the future derivability, admissibility, or weighting of consequences inside the same substrate.

Minimal loop:

```text
generate DAG
derive consequence signatures
compute interpreter state
use interpreter state to constrain or weight next derivation step
repeat for depth T
```

---

# Experimental Conditions

Run at least three conditions.

## Condition A: Open

No closure.

```text
generator → verifier → consequence classes
```

## Condition B: Weak Closure

Interpreter state reweights future sampling but does not forbid derivations.

```text
I_t affects sampling probability
```

## Condition C: Strong Closure

Interpreter state can reject or prune future derivations that fail internal viability criteria.

```text
I_t affects admissibility
```

---

# Perturbation Classes

Reuse 17A.2 taxonomy.

## Class A — Representation Preserving

```text
P4_alpha_rename
P9_split_node
P10_replace_subgraph
```

## Class B — Theory Changing

```text
P1_remove_edge
P2_add_edge
P3_reverse_edge
P5_split_mediator
P6_delete_path
P7_replace_chain
P8_merge_internal_nodes
P11_swap_branches
P12_alternative_derivation
```

---

# Required Measurements

For each condition:

```text
analyzed_classes
surviving_classes_under_Class_A
broken_classes_under_Class_A
surviving_fraction_under_Class_A
mean_auc_gns_under_Class_A

surviving_classes_under_Class_B
broken_classes_under_Class_B
surviving_fraction_under_Class_B
mean_auc_gns_under_Class_B

mean_attack_cost_broken
min_attack_cost
```

Additionally measure closure-specific metrics:

```text
closure_participation_rate
mean_interpreter_score
semantic_survival_fraction
dead_consequence_fraction
loop_reuse_rate
closure_stability_under_Class_A
closure_stability_under_Class_B
```

---

# Core Comparisons

## Test 1 — Does closure change Class A invariance?

Expected if H2-rel is sufficient:

```text
Open and Closed substrates both survive Class A similarly.
```

Expected if closure matters:

```text
Closed substrate preserves a stricter or more stable subset under Class A.
```

## Test 2 — Does closure improve selectivity under Class B?

Expected if H2-rel is sufficient:

```text
Class B breakage is similar with or without closure.
```

Expected if H3 is true:

```text
Closed substrate separates semantically active classes from formal artifacts.
```

## Test 3 — Are there consequence-invariant but semantically dead classes?

A class is suspicious if:

```text
survives Class A
but has near-zero interpreter participation
and does not affect future derivations
```

Report all such classes.

These are potential counterexamples to:

```text
meaning = consequence invariance
```

## Test 4 — Are there closure-active classes that fail raw invariance?

A class is interesting if:

```text
does not survive broad raw perturbation
but remains stable inside the closed loop
```

These may indicate that meaning depends on functional role, not raw global invariance.

---

# Decision Logic

## Classification: H2_sufficient

Use if:

```text
Closed loop adds no explanatory separation.
Consequence-invariant classes and closure-active classes mostly coincide.
Open and Closed substrates behave similarly under Class A and Class B.
```

## Classification: H3_supported

Use if:

```text
Many consequence-invariant classes are closure-dead
or
closure-active classes form a significantly different subset
or
closure improves semantic selectivity under theory-changing perturbations.
```

## Classification: Closure_artifact

Use if:

```text
Closure effects are caused only by trivial pruning, sampling bias, or collapse of class diversity.
```

## Classification: Inconclusive

Use if:

```text
closure metrics cannot be separated from implementation artifacts
or
too few classes remain for meaningful comparison.
```

---

# Kill Conditions

Reject H3 for this substrate if:

```text
closure-active classes ≈ consequence-invariant classes
and closure adds no measurable selectivity
and no closure-dead invariant classes are found.
```

Reject H2-rel as sufficient if:

```text
many Class-A-invariant classes are closure-dead
or
closed-loop semantic classes differ strongly from raw consequence classes.
```

Reject the experiment as invalid if:

```text
closure simply reduces diversity
closure uses external semantic information
closure changes the verifier instead of adding an interpretive loop
closure makes derivation non-terminating
closure makes results depend on arbitrary hand-picked labels
```

---

# Minimum Run

Use parameters comparable to 17A.2:

```text
--seed 42
--num-dags 500
--max-depth 6
```

If runtime allows, also run:

```text
--seed 43
--seed 44
--num-dags 1000
--max-depth 8
```

---

# Required Outputs

Create output directory:

```text
experiments/17C_Interpretive_Closure/outputs_17C/
```

Required artifacts:

```text
open_summary.json
weak_closure_summary.json
strong_closure_summary.json

open_attack.csv
weak_closure_attack.csv
strong_closure_attack.csv

closure_metrics.csv
closure_dead_classes.csv
closure_active_classes.csv

class_a_comparison.json
class_b_comparison.json
h2_vs_h3_decision.json

failure_examples.json
implementation_notes.md
final_decision.md
```

---

# Required Questions

Answer explicitly:

1. Do consequence-invariant classes coincide with closure-active classes?

2. Are there Class-A-invariant classes that are closure-dead?

3. Does interpretive closure improve selectivity under theory-changing perturbations?

4. Does closure merely prune the space, or does it identify a distinct semantic subset?

5. Does this experiment support H2-rel, H3, or neither?

6. What is the strongest counterexample found against H2-rel?

7. What is the strongest counterexample found against H3?

---

# Reporting Format

Final report must include:

```text
Final Decision
Core Result
Open vs Weak Closure vs Strong Closure
Class A Results
Class B Results
Closure-Specific Metrics
Counterexamples
Failure Modes
Interpretation
Artifacts
```

Do not over-interpret.

Clearly separate:

```text
what was measured
what was inferred
what remains open
```

---

# Scientific Interpretation Rules

If closure helps, do not conclude immediately that biological semantic closure is required.

Only conclude:

```text
For this substrate, raw consequence invariance is not sufficient to identify all semantically active classes.
```

If closure does not help, do not conclude that semantic closure is false.

Only conclude:

```text
This implementation found no evidence that an internal interpretive loop adds explanatory power beyond consequence invariance.
```

---

# Expected Value

This experiment is valuable even if negative.

Possible outcomes:

```text
H2-rel survives stronger falsification.
H3 becomes a better working hypothesis.
Both fail because closure is ill-defined.
The experiment exposes a new hidden assumption in the project.
```

Any of these outcomes is useful.

