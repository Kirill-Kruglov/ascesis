# BA2.E1 Semantic Benefit vs Structural Cost Map

**Decision:** `H_BA2_rejected`.
**Reason:** at least one clean mechanism has high structural cost and low semantic benefit.
**Strongest counterexample:** `MB2`.
**Investigate first:** `MB5`.

## Benefit / Cost Plane

| mechanism | semantic benefit | structural cost | ratio | validity |
|---|---:|---:|---:|---|
| MB1 | 0.1357 | 0.2719 | 0.4990 | comparable_enough_for_diagnostic |
| MB2 | 0.0271 | 0.3775 | 0.0717 | comparable_enough_for_diagnostic |
| MB3 | 0.1415 | 0.4053 | 0.3491 | comparable_enough_for_diagnostic |
| MB4 | 0.1658 | 0.9221 | 0.1798 | severe_semantic_shift |
| MB5 | 0.0094 | 0.3908 | 0.0240 | comparable_enough_for_diagnostic |

## Required Questions

1. Does every monotonicity breaker provide semantic benefit? No. Clean high-cost/low-benefit mechanisms: `['MB2', 'MB5']`.
2. Are there dominated mechanisms? Yes, see `dominance_graph.csv`; clean dominated edges: `3`.
3. Is there a Pareto frontier? Yes.
4. Pareto-optimal mechanisms: all=`['MB4', 'MB3', 'MB1']`, comparable-only=`['MB3', 'MB1']`.
5. Worst benefit/cost ratio: `MB5`.
6. Investigate first: `MB5`.
7. Strongest counterexample against H_BA2: `MB2`.

## Interpretation

The BA1 data do not support the strong form of H_BA2. Some mechanisms that complicate monotonicity appear to carry measurable semantic value, but at least one clean mechanism lands in the high-cost/low-benefit region. MB4 remains semantically indispensable rather than cleanly rankable: its ablation removes collapse dynamics and therefore cannot be used as a normal benefit/cost point.

## Formula Summary

- Semantic benefit = weighted positive loss in false-safe, false-unsafe, pure blindness, collapse recall, balanced prediction quality, plus clause-coverage displacement.
- Structural cost = weighted static mechanism complexity plus empirical reduction in BA1 monotonicity witnesses/counterexamples when removed, plus isolation cost for severe semantic shifts.
- Dominance uses the specified rule: A dominates B if benefit(A) >= benefit(B) and cost(A) <= cost(B), with at least one strict inequality.
