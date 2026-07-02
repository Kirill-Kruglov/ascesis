# Experiment 17D - Closure Metric Robustness

## Final Decision

Classification: `Inconclusive`.

Metrics show partial convergence but not enough to separate controls/artifacts cleanly.

## Core Results

Functional core: 12057 / 29934
Strict core: 2015 / 29934
Dead invariant recheck: {'dead_invariant_total': 743, 'dead_invariant_remain_dead_majority': 52}

## Metric Summaries

- M1_original: active=11974, ClassA_survive=1, ClassB_survive=0.006667
- M2_intervention: active=11974, ClassA_survive=1, ClassB_survive=0.1817
- M3_reuse: active=11974, ClassA_survive=1, ClassB_survive=0.001667
- M4_compression: active=11974, ClassA_survive=1, ClassB_survive=0.1383
- M5_perturbation_centrality: active=11974, ClassA_survive=1, ClassB_survive=0.005
- M6_frequency_control: active=11974, ClassA_survive=1, ClassB_survive=0.1383
- M7_random_matched: active=11974, ClassA_survive=1, ClassB_survive=0.1683

## Required Questions

1. Does 17C active subset survive replacement? See pairwise_overlap.csv and functional_core.csv.
2. Do metrics converge? Functional/strict core sizes above.
3. Are closure-dead invariant classes still dead? See dead_invariant_recheck.csv.
4. Controls? See control_comparison.json.
5. Interpretation is in final_decision.json.
6. Strongest counterexamples in failure_examples.json.
7. Stable core evidence in functional_core.csv.