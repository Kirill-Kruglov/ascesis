# Camouflage-Cost x Audit Surface Report

SPEC hash (declared): `705956aeed7da99b221d6ae0c1c2bc5c54b2099585a2a8134eede86155be200e`
SPEC hash (actual): `705956aeed7da99b221d6ae0c1c2bc5c54b2099585a2a8134eede86155be200e`

## Calibration Gate

- baseline gamma=0, audit-off reproduced: `True`
- first-crossing R*: `0.8333333333333334`
- sustained R*: `None`
- mid-high mean permanence: `0.527`
- criterion: sustained R*=None, mid-high mean in [0.40,0.60], finite first-crossing R*

| R | held-out success | rate | Wilson 95% band |
|---:|---:|---:|---:|
| 0.182 | 0/30 | 0.000 | [0.000, 0.114] |
| 0.333 | 0/30 | 0.000 | [0.000, 0.114] |
| 0.375 | 1/30 | 0.033 | [0.006, 0.167] |
| 0.571 | 4/30 | 0.133 | [0.053, 0.297] |
| 0.833 | 18/30 | 0.600 | [0.423, 0.754] |
| 1.200 | 15/30 | 0.500 | [0.332, 0.668] |
| 2.000 | 20/30 | 0.667 | [0.488, 0.808] |
| 3.333 | 13/30 | 0.433 | [0.274, 0.608] |
| 6.500 | 13/30 | 0.433 | [0.274, 0.608] |

## Surface Summary

- favorable fixed R: `2.000` (`r07`)
- gamma grid: `[0.0, 0.05, 0.1, 0.2, 0.4, 0.8]`
- p grid: `[0.0, 0.1, 0.25, 0.5]`
- C grid: `[0.0, 0.25, 0.5, 0.75, 1.0]`
- kappa grid: `[0.0, 0.05, 0.1, 0.2, 0.4]`

## H1: Camouflage Cost

- gamma=0 audit-off permanence: `0.667 [0.488, 0.808]`
- max-gamma audit-off permanence: `0.233 [0.118, 0.409]`
- delta: `-0.433`
- Wilson bands non-overlap: `True`
- H1 supported: `False`

## H2: Committed Audit

- best gamma>0 audit-off gamma: `0.05`
- best gamma>0 audit-off permanence: `0.567 [0.392, 0.726]`
- best audit-on at kappa=0: gamma `0.05`, p `0.1`, C `0.25`, permanence `0.300 [0.167, 0.479]`
- audit gain at kappa=0: `-0.267`
- part (i) supported: `False`
- gamma=0 best audit effect: `-0.400`
- absolute gamma=0 audit effect: `0.400`
- part (ii) no gamma=0 audit effect: `False`
- gamma=0 audit leak bug stop: `False` (only positive audit lift at gamma=0 is treated as leakage)
- H2 supported: `False`

## H3: Audit Cost

- kappa*: `None`
- audit gain at kappa=0: `-0.267`
- half-gain threshold: `-0.133`
- H3 is not applicable when audit gain at kappa=0 is non-positive; there is no positive gain for kappa to eat.

| kappa | permanence | audit gain |
|---:|---:|---:|

## Interpretation

- Wall breaks under costly camouflage (H1): `False`.
- If H1 is false, the registered fail-fork is that the wall survives costly camouflage; in this run high gamma reduces permanence rather than breaking the wall.
- If H2 leak bug stop is true, audit helped at gamma=0 and the audit channel must be inspected before reading H2 as a result.

## Underspecified Choices

- Camouflage cost is applied directly in replicator fitness as `-gamma * max(0, gene - signal)` before share normalization.
- Committed audit catches lagged capture events above the same threshold used by the baseline capture-event diagnostic and cuts access by multiplying allocation by `1-C` for a fixed five-step window.
- Audit cost `kappa` reduces total feeding budget on audit steps; false positives target the random audit focus without reading true type, preserving type-blindness.
- Parent consequence reaction remains present at audit-off so `gamma=0,p=0,C=0` reproduces the baseline substrate; explicit audit is an additional committed punishment/cost channel.
