# Experiment 17 - Backbone Consequence

## Decision

Classification: `H2_supported`.

Nontrivial high-GNS consequence classes exist and outperform feature baseline.

## Run Parameters

- seed: 42
- num_dags: 500
- max_depth: 6
- expressions_per_dag_depth: 80
- max_analyzed_classes: 3500
- perturbations_per_k: 8
- GNS definition: weighted average of Persistence(k=1..4), weights 0.40/0.30/0.20/0.10, emphasizing lower-budget perturbations.

## Required Questions

1. Do frozen consequence classes exist? Yes.
2. Are they nontrivial? Yes.
3. How many? 3065 frozen classes among 3065 analyzed classes.
4. Are they more stable than feature classes? Yes; consequence mean GNS=1, feature baseline=0.
5. Are they more stable than AST identity? Yes; AST baseline=0.746211.
6. Does stability correlate with expression depth? undefined: GNS is constant across analyzed classes.
7. Does stability correlate with consequence class size? undefined: GNS is constant across analyzed classes.
8. Should Global Necessity replace class cardinality as primary invariant? Yes as a stability invariant, but it should be tracked alongside class diversity/cardinality rather than replacing them entirely.

## Coverage

- total consequence classes: 29934
- analyzed classes: 3065
- frozen classes: 3065
- nontrivial frozen classes: 2337
- mean frozen alias-pair fraction: 0.23752
- weak classes: 0
- frozen coverage: 1
- weighted frozen coverage: 1

## Baselines

- consequence mean GNS: 1
- feature mean persistence: 0
- AST identity mean persistence: 0.746211
- random mean persistence: 0.00399202

## Top High-GNS Classes

| class_id | class_size | gns | frozen | weak | nontrivial_pair_count | alias_pair_fraction | operator_diversity | dag_diversity | representative_expressions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| b480fbcf99aa331c | 197 | 1 | True | False | 2 | 0 | 2 | 120 | Blocked(N0, N2 \| N1) \| Blocked(N0, N2 \| N1) \| Blocked(N0, N2 \| N1) |
| 2b7f0d4e6e6eae6e | 194 | 1 | True | False | 2 | 0 | 2 | 120 | Blocked(N0, N1 \| N3) \| Blocked(N0, N1 \| N3) \| Blocked(N0, N1 \| N3) |
| 4c081c59a3909c3f | 194 | 1 | True | False | 2 | 0 | 2 | 119 | Blocked(N2, N0 \| N3) \| Blocked(N2, N0 \| N3) \| Blocked(N2, N0 \| N3) |
| 2b69a96860905434 | 192 | 1 | True | False | 2 | 0 | 2 | 118 | Blocked(N0, N2 \| N3) \| Blocked(N0, N2 \| N3) \| Blocked(N0, N2 \| N3) |
| 65d48fb1aa39b3e1 | 189 | 1 | True | False | 2 | 0 | 2 | 115 | Blocked(N2, N1 \| N0) \| Blocked(N2, N1 \| N0) \| Blocked(N2, N1 \| N0) |
| 05894539fcdf4840 | 188 | 1 | True | False | 2 | 0 | 2 | 115 | Blocked(N2, N3 \| N0) \| Blocked(N2, N3 \| N0) \| Blocked(N2, N3 \| N0) |
| fcadfa2dbea901bf | 187 | 1 | True | False | 2 | 0 | 2 | 116 | Blocked(N0, N3 \| N1) \| Blocked(N0, N3 \| N1) \| Blocked(N0, N3 \| N1) |
| a16e3db210295541 | 186 | 1 | True | False | 2 | 0 | 2 | 112 | Blocked(N3, N2 \| N0) \| Blocked(N3, N2 \| N0) \| Blocked(N3, N2 \| N0) |

## Honesty Notes

- The causal DAG generator and verifier are reused from Experiment 16 unchanged.
- Persistence is estimated from deterministic representative same-DAG pairs per class and bounded perturbation samples, not exhaustive pair enumeration.
- Feature, random, and AST baselines are evaluated by verifier consequence equality under perturbation, not by tautological key equality.