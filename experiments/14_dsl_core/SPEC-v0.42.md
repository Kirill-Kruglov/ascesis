# WorldCore v0.4.2

# Proof Opportunity Audit

Status: REQUIRED before any modification of the generator or architecture.

---

# Motivation

v0.4.1 established several important facts.

Established:

* raw world generation has high novelty
* task novelty is much lower
* proof novelty almost completely collapses

However, one critical ambiguity remains.

Current evidence does **not** distinguish between:

```
H2
Task extractor collapses proof diversity.
```

and

```
H2'
The closure of generated worlds is itself poor.
The extractor simply samples almost everything that exists.
```

Until this ambiguity is resolved,

NO architectural changes should be made.

No ontology expansion.

No proof-first generation.

No Sanskrit layer.

This revision exists solely to resolve H2 vs H2'.

---

# Non-negotiable Rule

DO NOT improve the generator.

DO NOT rewrite the extractor.

DO NOT change ontology.

Only measure.

Only diagnose.

---

# 1. Full World Closure

For every sampled world

compute

```
Closure(world)
```

using the symbolic solver.

Not selected tasks.

Not selected proofs.

ALL derivable facts.

Continue until fixpoint.

Export

```
closure/
    world_XXXX.json
```

Each file must contain

```
initial facts

derived facts

rule applications

derivation graph
```

---

# 2. Closure Statistics

For every world compute

```
initial fact count

derived fact count

closure size

closure expansion ratio
```

where

```
closure expansion ratio

=

derived facts

/

initial facts
```

Produce

```
closure_statistics.csv
```

Question:

Do worlds actually contain rich derivable structure?

---

# 3. Proof Opportunity Enumeration

For every derivable fact

enumerate

ALL available proofs

or

an approximation if exhaustive enumeration is impossible.

For every proof record

```
goal fact

proof DAG

proof shape

proof length

proof depth

proof alternatives
```

Export

```
proof_opportunities.csv
```

---

# 4. Opportunity Metrics

For every world compute

```
closure size

proof opportunities

distinct proof DAGs

distinct proof shapes

average alternatives per goal

proof entropy
```

Export

```
proof_opportunity_summary.csv
```

Question

How many interesting proofs exist

BEFORE

task extraction?

---

# 5. Extractor Coverage

For every world compare

```
ALL proof opportunities
```

vs

```
Selected tasks
```

Compute

```
coverage

=

selected proofs

/

available proofs
```

Also compute

```
coverage by proof shape

coverage by proof length

coverage by reasoning family
```

Export

```
extractor_coverage.csv
```

Question

Does extractor ignore

90%

of available proofs

or

does nothing richer exist?

---

# 6. Opportunity Graph

Represent closure as

reachability graph.

Nodes

```
facts
```

Edges

```
derivable_by_rule
```

Tasks become

```
(start fact,

goal fact)
```

Measure

```
number of reachable pairs

connected components

path length distribution

number of alternative paths

average branching
```

Export

```
closure_graph_metrics.csv
```

---

# 7. Proof Opportunity Diversity

Current proof novelty is

```
selected proof novelty
```

Compute instead

```
closure proof novelty
```

Question

How many distinct proof DAGs

exist in closure

before sampling?

Export

```
closure_proof_novelty.csv
```

---

# 8. Audit Difficulty Oracle

Current Difficulty Oracle is NOT trusted.

Reason:

v0.4.1 produced

```
Pearson

length → OOD

=

1.0000

depth → OOD

=

1.0000

width → OOD

=

1.0000
```

which is almost certainly an artifact of binary proof/no-proof separation.

This revision must audit the oracle.

For every difficulty feature

report

```
distribution

variance

mutual correlation

correlation with proof shape
```

Question

Does difficulty measure

continuous structure

or merely

proof exists / proof absent?

Export

```
difficulty_audit.csv
```

---

# 9. Binary Collapse Test

Explicitly test

```
difficulty

↓

binary proof existence
```

Fit

simple logistic model

```
proof exists?

↓

difficulty
```

If

R²

or

accuracy

is near perfect

report

```
Difficulty Oracle collapsed
```

instead of

```
Difficulty validated
```

---

# 10. Forced Proof Investigation

The previous audit produced

```
accepted_test = 0
```

This is NOT a scientific result.

It is an instrument failure.

Investigate.

For every rejected candidate

store

```
rejection reason
```

Examples

```
insufficient depth

proof extraction failed

closure missing

canonicalization merged

sampling rejected

timeout

other
```

Produce

```
forced_rejection_report.csv
```

Question

Why did

accepted_test

become zero?

---

# 11. Diversity Discrepancy

Explain

```
selected proof novelty

≈0.001
```

vs

```
forced diversity

≈0.22
```

Produce

```
diversity_explanation.json
```

Possible explanations

```
canonicalization artifact

proof length

sampling artifact

closure richer

measurement bug

unknown
```

This explanation is REQUIRED.

---

# 12. Opportunity by Reasoning Family

Compute separately

```
transitivity

implication

belief

causal

part-of

negation

mixed
```

For each family report

```
closure size

proof opportunities

proof diversity

extractor coverage
```

Export

```
reasoning_family_audit.csv
```

---

# 13. Sampling Simulation

Without modifying the current extractor,

implement

alternative sampling strategies

using

the SAME closure.

Examples

```
uniform

length weighted

entropy weighted

shape weighted

rare proof weighted

random
```

Do NOT train.

Simply measure

expected proof diversity

under each sampler.

Output

```
sampling_simulation.csv
```

Question

Could diversity improve

without changing the generator?

---

# 14. H2 vs H2' Decision

Produce

```
decision_H2.json
```

Possible outcomes

---

Case H2

```
Closure rich

↓

Extractor poor
```

Evidence

```
large closure

many proof opportunities

low extractor coverage
```

Recommendation

```
rewrite extractor
```

---

Case H2'

```
Closure poor

↓

Extractor reasonable
```

Evidence

```
small closure

few proof opportunities

high extractor coverage
```

Recommendation

```
rewrite generator
```

---

Case Mixed

```
Closure moderate

Extractor moderate

Both contribute.
```

---

Case Unknown

```
Instrumentation insufficient.
```

---

# 15. Deliverables

The following files are REQUIRED.

```
closure_statistics.csv

proof_opportunities.csv

proof_opportunity_summary.csv

extractor_coverage.csv

closure_graph_metrics.csv

closure_proof_novelty.csv

difficulty_audit.csv

forced_rejection_report.csv

diversity_explanation.json

reasoning_family_audit.csv

sampling_simulation.csv

decision_H2.json
```

---

# Success Criterion

This revision is successful if it answers one question only:

```
Where does proof diversity disappear?
```

Choose exactly one:

```
World generation

Closure

Task extraction

Instrumentation
```

No architectural recommendation should be made beyond what the evidence supports.

---

# Important Research Principle

This revision deliberately postpones proof-first generation.

Proof-first architecture remains a live hypothesis.

However,

it may only be adopted

after

H2

and

H2'

have been experimentally separated.

Until then,

the project remains diagnostic rather than architectural.

