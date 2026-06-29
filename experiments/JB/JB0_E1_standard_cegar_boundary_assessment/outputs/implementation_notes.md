# JB0.E1 Implementation Notes

- Justitia source semantics and collapse definition were not modified.
- No oracle time-to-collapse or future labels were used as features.
- Dataset construction reuses FA2.5: all false-safe witnesses vs sampled SAFE-and-remain-SAFE states, split by trajectory group.
- Budgets: max predicates `20`, max abstract cells `100000`, max history window `8`, max iterations `20`.
- Predicate abstraction uses Boolean cells with smoothed empirical risk learned on training groups.
- Threshold selection first tries recall >= 0.90 with FPR <= 0.25; if unavailable, it falls back to best balanced accuracy, which can expose vacuity.
- T-C was not run.
