# Experiment 16 - Consequence vs Feature

## Decision

Classification: `feature_proxy_failure`.

Feature equivalence is forgeable and too coarse; consequence relation works against AST syntax but is not fewer than feature classes.

## Run Parameters

- seed: 42
- max_depth: 6
- num_dags: 200
- per_depth_cap: 120

## Required Questions

1. Does feature-based equivalence behave like forgeable syntax? Yes; same-feature/different-consequence examples exist = True.
2. Does consequence-based equivalence nontrivially merge expressions? Yes; consequence/AST ratio at max depth = 0.3883.
3. Are there same-feature/different-consequence examples? True.
4. Are there different-feature/same-consequence examples? True.
5. Does consequence-class count grow without becoming free syntax? Yes; growth ratio depth1->max = 17.07.
6. Is derivability complete enough to trust the result? Yes; success rate = 1.
7. Should we proceed to richer causal-world fragments? Yes.

## Aggregate Growth

| depth | num_expressions | feature_class_count | consequence_class_count | ast_identity_class_count | feature_class_entropy | consequence_class_entropy |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 18186 | 846 | 2550 | 18186 | 5.77285 | 6.66752 |
| 2 | 33822 | 1692 | 6380 | 33822 | 6.7231 | 7.91126 |
| 3 | 54150 | 2891 | 16658 | 54150 | 7.25653 | 9.24313 |
| 4 | 73254 | 4689 | 23670 | 73254 | 7.83097 | 9.7548 |
| 5 | 92358 | 6486 | 29224 | 92358 | 8.24677 | 10.0787 |
| 6 | 112074 | 10523 | 43519 | 112074 | 8.60578 | 10.634 |

## Key Evidence

- expressions at max depth: 112074
- feature classes at max depth: 10523
- consequence classes at max depth: 43519
- AST identity classes at max depth: 112074
- consequence vs AST identity ratio: 0.3883
- consequence vs feature ratio: 4.136
- consequence fewer than feature classes: False
- semantic collapse: False
- consequence free-monoid-like: False

## Honesty Notes

- Consequence signatures are verifier-derived from reachability, ancestors, d-separation, interventions and path properties.
- Feature keys intentionally use shallow surface properties and do not include verifier output.
- Label-free AST identity is reported only as the free-syntax baseline.