# Experiment 17C - Consequence Invariance vs Interpretive Closure

## Final Decision

Classification: `H3_supported`.

Closure-active subset differs materially from raw consequence-invariant classes.

## Core Result

Closure active classes: 11974 / 29934
Closure-dead Class-A-invariant classes: 743

## Open vs Weak Closure vs Strong Closure

Open Class A survive: 1
Weak Class A survive: 1; weighted=1.0
Strong Class A survive: 1

Open Class B survive: 0.131111
Weak Class B survive: 0.131111; weighted=0.1129280696974645
Strong Class B survive: 0.00333333

## Required Questions

1. Do consequence-invariant classes coincide with closure-active classes? No.
2. Are there Class-A-invariant classes that are closure-dead? Yes; count=743.
3. Does interpretive closure improve selectivity under theory-changing perturbations? Yes.
4. Does closure merely prune the space, or identify a distinct semantic subset? Distinct subset.
5. Does this support H2-rel, H3, or neither? H3_supported.
6. Strongest counterexample against H2-rel: Class-A-invariant but closure-dead classes in `closure_dead_classes.csv`.
7. Strongest counterexample against H3: closure-active classes still break under Class B in `strong_closure_attack.csv`.

## Artifacts

See outputs_17C/*.json, *.csv, implementation_notes.md, final_decision.md.