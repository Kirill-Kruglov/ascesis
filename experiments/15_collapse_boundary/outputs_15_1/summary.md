# Experiment 15.1 - Depth-Cap Boundary Probe

## Decision

Classification: `sample_limited_inconclusive`.

Cannot distinguish semantic openness from sampling limit.

## Required Questions

1. Did C exceed the old 1024 semantic-class ceiling? Yes; max semantic_class_count = 98843.
2. Did semantic growth depend on depth_cap? Yes; delta = 98685, ratio = 1543.
3. Did semantic growth depend on observation_depth? No clear substantial dependence; delta = 0, ratio = 1.
4. Was any result sample-limited? Yes; semantic sample-limited fraction = 0.1493, any-channel sample-limited fraction = 0.9333.
5. Is there evidence of genuine semantic openness? No, not without caveats.
6. Next recommended action: Increase sampling budget or change sampler before making liveness claims.

## Growth Tables

### Semantic Growth by Depth Cap

| depth_cap | semantic_class_count | trajectory_count | semantic_class_rate | trajectory_rate | sample_limited_any | semantic_growth_from_previous | semantic_growth_ratio_from_previous |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | 64 | 88834 | 0.00064 | 0.88834 | False |  |  |
| 12 | 1024 | 99983 | 0.01024 | 0.99983 | True | 960 | 16 |
| 16 | 16346 | 100000 | 0.16346 | 1 | True | 15322 | 15.9629 |
| 20 | 83206 | 100000 | 0.83206 | 1 | True | 66860 | 5.0903 |
| 24 | 98749 | 100000 | 0.98749 | 1 | True | 15543 | 1.1868 |

### Semantic Growth by Observation Depth

| observation_depth | semantic_class_count | trajectory_count | semantic_class_rate | trajectory_rate | sample_limited_any | semantic_growth_from_previous | semantic_growth_ratio_from_previous |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 98749 | 100000 | 0.98749 | 1 | True |  |  |
| 6 | 98749 | 100000 | 0.98749 | 1 | True | 0 | 1 |
| 8 | 98749 | 100000 | 0.98749 | 1 | True | 0 | 1 |
| 10 | 98749 | 100000 | 0.98749 | 1 | True | 0 | 1 |
| 12 | 98749 | 100000 | 0.98749 | 1 | True | 0 | 1 |

### Semantic Growth by Sample Budget

| sample_budget | semantic_class_count | trajectory_count | semantic_class_rate | trajectory_rate | sample_limited_any | semantic_growth_from_previous | semantic_growth_ratio_from_previous |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20000 | 19949 | 20000 | 0.99745 | 1 | True |  |  |
| 50000 | 49675 | 50000 | 0.9935 | 1 | True | 29726 | 2.4901 |
| 100000 | 98749 | 100000 | 0.98749 | 1 | True | 49074 | 1.9879 |

## Honesty Notes

- The primary semantic proxy is bounded-depth observation prefix / normal-form class, reused from 15.0.1.
- Label-sequence quotient is recorded only as a syntactic-like diagnostic and is not used as semantic evidence.
- Any sample-limited channel must not be classified as open.
- Syntactic trajectory growth without semantic growth is not evidence of liveness.