# BA2.E1 Tradeoff Examples

Benefit is measured as fidelity deterioration after a single-mechanism removal.
Cost is a documented mixture of static structural complexity and BA1 witness reductions.

## Mechanism Points

| mechanism | benefit | cost | ratio | validity | note |
|---|---:|---:|---:|---|---|
| MB1 | 0.1357 | 0.2719 | 0.4990 | comparable_enough_for_diagnostic | measurable semantic benefit |
| MB2 | 0.0271 | 0.3775 | 0.0717 | comparable_enough_for_diagnostic | high-cost / low-benefit counterexample candidate |
| MB3 | 0.1415 | 0.4053 | 0.3491 | comparable_enough_for_diagnostic | measurable semantic benefit |
| MB4 | 0.1658 | 0.9221 | 0.1798 | severe_semantic_shift | apparent high value is non-comparable because removal eliminates collapse dynamics |
| MB5 | 0.0094 | 0.3908 | 0.0240 | comparable_enough_for_diagnostic | high-cost / low-benefit counterexample candidate |

## Dominance

- `MB1` dominates `MB2`.
- `MB1` dominates `MB5`.
- `MB2` dominates `MB5`.

## Pareto Frontier

- All mechanisms: `MB4`, `MB3`, `MB1`
- Comparable-only: `MB3`, `MB1`

## Metric Notes

- MB4 is not allowed to carry H_BA2 by itself because BA1 marked it `severe_semantic_shift`.
- Positive semantic benefit means removal worsens the unchanged 18.0 shield fidelity.
- Negative or zero benefit means the mechanism is not visibly reducing semantic blindness under this grid.
