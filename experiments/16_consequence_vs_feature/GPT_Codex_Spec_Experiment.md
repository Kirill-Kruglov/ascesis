# Codex Spec — Experiment 16: Consequence vs Feature

## Project

`16_consequence_vs_feature`

## Goal

Test whether a minimal causal-world substrate can define a nontrivial **consequence-based equivalence relation** that is not reducible to surface features.

This is a micro-test for Door 1 from memo v1.1:

> knowledge is derived, not generalized.

Do not build an LLM experiment.
Do not add Sanskrit.
Do not use internet data.

---

# Core question

Can we construct generated world-description terms where:

```text
feature-based equivalence
```

behaves like free syntax / noisy-TV,

but

```text
consequence-based equivalence
```

nontrivially merges different forms while preserving many distinguishable classes?

---

# Minimal substrate

Use synthetic causal DAGs.

A world model is:

```python
CausalDAG(
    nodes: list[str],
    directed_edges: list[tuple[str, str]]
)
```

Generate small DAGs with:

```text
nodes: 4, 6, 8, 10
edge_probability: 0.15, 0.25, 0.35
seed: 42
```

Ensure acyclicity.

---

# Expressions

Generate causal expressions such as:

```text
P(Y | do(X))
P(Y | X)
P(Y | do(X), Z)
P(Y | do(X), do(Z))
Effect(X -> Y)
Independent(X, Y | Z)
Reachable(X, Y)
Blocked(X, Y | Z)
```

Keep the language small and explicit.

Every expression must have:

```json
{
  "expr_id": "...",
  "surface": "...",
  "ast": "...",
  "features": {...},
  "dag_id": "...",
  "depth": ...
}
```

---

# Derivation / consequence semantics

Implement a symbolic verifier over DAGs.

Minimum supported consequences:

```text
reachability
d-separation / conditional independence
intervention edge removal
ancestor relation
causal effect existence
blocked path under conditioning
```

Two expressions are consequence-equivalent iff their verifier outputs the same consequence signature under the same DAG.

Example:

```text
same_consequence_signature(expr_a, expr_b, dag) == true
```

The signature should be structured, not text-only.

---

# Two equivalence relations

## 1. Feature-based equivalence

Group expressions by shallow surface features:

```text
operator type
mentioned variables
number of variables
presence of do()
conditioning set size
surface template
```

This intentionally represents the “forgeable” relation.

## 2. Consequence-based equivalence

Group expressions by verifier-derived consequence signature:

```text
reachable set
ancestor set
d-separated pairs
intervention-transformed graph property
effect existence
blocked/unblocked status
```

This is the candidate “non-forgeable” relation.

---

# Required tests

## T1 — Class growth with expression depth

For each DAG size and expression depth:

```text
depth = 1, 2, 3, 4, 5, 6
```

Compute:

```text
num_expressions
feature_class_count
consequence_class_count
feature_class_entropy
consequence_class_entropy
```

Expected useful outcome:

```text
feature classes grow freely
consequence classes grow more slowly but do not collapse to 1
```

---

## T2 — Forgeability probe

Find examples of:

```text
same features, different consequences
```

and

```text
different features, same consequences
```

Both must exist for a healthy consequence relation.

Output concrete examples.

---

## T3 — Free-monoid detector

Detect whether either relation behaves like pure syntax.

Flag noisy-TV if:

```text
class_count ≈ expression_count
AND equivalence mostly equals AST identity
```

---

## T4 — Collapse detector

Flag semantic collapse if:

```text
consequence_class_count <= 1
```

or if one class contains more than:

```text
95%
```

of all expressions.

---

## T5 — Derivability completion

Every consequence signature must be obtained by verifier derivation.

Report:

```text
derivation_success_rate
timeout_rate
unknown_rate
```

Kill condition:

```text
derivation_success_rate < 0.99
```

---

# Outputs

Write to:

```text
outputs_16/
```

Required files:

```text
summary.md
final_decision.json
class_growth.csv
forgeability_examples.json
equivalence_stats.csv
free_monoid_report.json
collapse_report.json
derivability_report.json
```

Required plots:

```text
feature_vs_consequence_class_growth.png
feature_vs_consequence_entropy.png
class_ratio_by_depth.png
```

---

# Final decision labels

## `consequence_relation_viable`

Use only if:

```text
consequence classes grow with depth
AND do not collapse
AND are substantially fewer than feature/free syntax classes
AND forgeability examples exist both ways
AND derivation success rate >= 0.99
```

## `feature_proxy_failure`

Use if:

```text
feature equivalence fails forgeability tests
but consequence relation works
```

This is actually a positive result for the project.

## `consequence_collapses`

Use if:

```text
consequence relation collapses to 1/few trivial classes
```

## `consequence_is_syntax`

Use if:

```text
consequence classes track expression identity or AST identity
```

## `instrumentation_failure`

Use if:

```text
verifier cannot derive signatures reliably
```

---

# Required summary questions

`summary.md` must answer:

1. Does feature-based equivalence behave like forgeable syntax?
2. Does consequence-based equivalence nontrivially merge expressions?
3. Are there same-feature/different-consequence examples?
4. Are there different-feature/same-consequence examples?
5. Does consequence-class count grow without becoming free syntax?
6. Is derivability complete enough to trust the result?
7. Should we proceed to richer causal-world fragments?

---

# Commands

```bash
pip install -e .
pytest

python scripts/run_consequence_vs_feature.py \
  --seed 42 \
  --max-depth 6 \
  --num-dags 200
```

Optional larger run:

```bash
python scripts/run_consequence_vs_feature.py \
  --seed 42 \
  --max-depth 8 \
  --num-dags 1000
```

Return:

```text
outputs_16/summary.md
outputs_16/final_decision.json
outputs_16/class_growth.csv
outputs_16/forgeability_examples.json
all plots
```

