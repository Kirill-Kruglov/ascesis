# Strategic Camouflage Report

SPEC hash (declared): `4fe5ff79ebb93cfc7c87e4132e77b2c715c981cb09c55d4a78492393e6a1725f`
SPEC hash (actual): `4fe5ff79ebb93cfc7c87e4132e77b2c715c981cb09c55d4a78492393e6a1725f`

## Calibration Gate

- corrected calibration gate passed: `True`
- gate (a), free concealment drives adversary c->1: `True`
- gate (b), strategic full concealment collapses permanence: `True`
- gate (c), passive-control reproduces parent coin-flip: `True`
- strategic mid-high final adversary c*: `0.999`
- strategic mid-high permanence: `0.000`
- passive-control mid-high permanence: `0.527`
- passive-control first-crossing R*: `0.8333333333333334`
- passive-control sustained R*: `None`
- criterion: (a) strategic c>=0.85, (b) strategic mid-high permanence<=0.10, (c) passive-control sustained R*=None and mid-high permanence in [0.40,0.65] with finite first crossing

### Strategic Worst-Case Curve

| R | success | permanence | Wilson 95% | adversary c* | corr | extinction |
|---:|---:|---:|---:|---:|---:|---:|
| 0.182 | 0/30 | 0.000 | [0.000, 0.114] | 0.976 | -0.933 | 0.000 |
| 0.333 | 0/30 | 0.000 | [0.000, 0.114] | 0.995 | -1.000 | 0.000 |
| 0.375 | 0/30 | 0.000 | [0.000, 0.114] | 0.999 | -1.000 | 0.000 |
| 0.571 | 0/30 | 0.000 | [0.000, 0.114] | 0.999 | -1.000 | 0.000 |
| 0.833 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | -1.000 | 0.000 |
| 1.200 | 0/30 | 0.000 | [0.000, 0.114] | 1.000 | -1.000 | 0.000 |
| 2.000 | 0/30 | 0.000 | [0.000, 0.114] | 0.999 | -1.000 | 0.000 |
| 3.333 | 0/30 | 0.000 | [0.000, 0.114] | 0.999 | -1.000 | 0.000 |
| 6.500 | 0/30 | 0.000 | [0.000, 0.114] | 0.999 | -1.000 | 0.000 |

### Passive-Control Faithfulness Curve

| R | success | permanence | Wilson 95% | corr | extinction |
|---:|---:|---:|---:|---:|---:|
| 0.182 | 0/30 | 0.000 | [0.000, 0.114] | 0.400 | 0.000 |
| 0.333 | 0/30 | 0.000 | [0.000, 0.114] | -0.533 | 0.000 |
| 0.375 | 1/30 | 0.033 | [0.006, 0.167] | -0.867 | 0.000 |
| 0.571 | 4/30 | 0.133 | [0.053, 0.297] | -0.533 | 0.000 |
| 0.833 | 18/30 | 0.600 | [0.423, 0.754] | 0.067 | 0.033 |
| 1.200 | 15/30 | 0.500 | [0.332, 0.668] | -0.200 | 0.100 |
| 2.000 | 20/30 | 0.667 | [0.488, 0.808] | -0.067 | 0.100 |
| 3.333 | 13/30 | 0.433 | [0.274, 0.608] | 0.067 | 0.100 |
| 6.500 | 13/30 | 0.433 | [0.274, 0.608] | 0.200 | 0.100 |

## Surface Summary

- fixed favorable R: `2.000` (`r07`)
- gamma grid: `[0.0, 0.1, 0.3, 0.6]`
- p grid: `[0.0, 0.25, 0.5]`
- C grid: `[0.0, 0.5, 1.0]`
- kappa grid: `[0.0, 0.1, 0.3]`

## H_s1: Strategic Abandonment

- baseline c*: `0.999`
- strongest-cell c*: `0.015`
- concealment drop: `0.984`
- baseline corr: `-1.000`
- strongest-cell corr: `1.000`
- strongest-cell adversary extinction: `1.000`
- strongest-cell adversary share: `0.036`
- corr gain: `2.000`
- H_s1 supported: `True`

## H_s2: Corridor Without Extinction

- baseline permanence: `0.000 [0.000, 0.114]`
- candidate cells over permanence threshold: `0`
- best non-extinction corridor cell: `None`
- best any-gain cell: `None`
- best observed permanence cell: `0.033 [0.006, 0.167]`
- extinction-only candidate count: `0`
- permanence only with extinction: `False`
- H_s2 supported: `False`
- best observed split: c* `0.789`, corr `0.000`, adversary extinction `0.800`, adversary share `0.220`.

## H_s3: Audit Cost

- kappa*: `None`
- gain at kappa=0: `0.000`
- half-gain threshold: `0.000`

| kappa | permanence | gain |
|---:|---:|---:|

## Interpretation

- Strategic concealment abandonment observed by H_s1 threshold: `True`.
- Corridor threaded by reveal without adversary extinction: `False`.
- If H_s2 is false and permanence appears only with high adversary extinction, the result repeats the corridor tension rather than solving it.

## Underspecified Choices

- `c` adaptation uses deterministic one-step selfish payoff hill-climb over `c-delta`, `c`, `c+delta`; ties keep the existing trait, so concealment/reveal is not designer-nudged.
- Strategic `signal = gene * (1-c)` supersedes passive signal drift for the observable signal; the feeder balances observed `signal + allocation` geometrically so low observed signal attracts compensating resource, while lag/audit/capture/replicator mechanics are otherwise reused.
- Net payoff for c adaptation uses resource gain, capture gain, capture loss, camouflage cost, and expected committed-audit penalty; actual replicator fitness keeps the camouflage_audit form without adding capture as a positive fitness term.
- Committed audit cuts resource access by multiplying allocation by `1-C` for a fixed five-step window; kappa reduces feeding budget on committed-audit steps.
