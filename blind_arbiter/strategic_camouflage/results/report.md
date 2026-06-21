# Strategic Camouflage Report

SPEC hash (declared): `f9183429305c2961e0191362e1b5c873a528ed20483ea92c0c396f34de8b1e6e`
SPEC hash (actual): `f9183429305c2961e0191362e1b5c873a528ed20483ea92c0c396f34de8b1e6e`

## Calibration Gate

- baseline strategic gate passed: `False`
- mid-high mean final adversary c*: `0.999`
- first-crossing R*: `None`
- sustained R*: `None`
- mid-high mean permanence: `0.000`
- criterion: adversary c>=0.85, sustained R*=None, mid-high mean in [0.40,0.65], finite first-crossing R*

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

## Verdict

calibration failure: the strategic substrate does not reproduce the registered baseline coin-flip parent. H_s1/H_s2/H_s3 are not readable.

The strategic layer drives the adversary toward full concealment when `(p=0, C=0, gamma=0)`, but the resulting baseline permanence is zero across the R grid rather than near coin-flip on the mid-high bucket. This indicates a substrate-transfer failure: full strategic concealment makes the hidden adversary capture the population instead of reproducing the parent `camouflage_audit/` baseline.

## H_s1/H_s2/H_s3

Not evaluated. The pre-registered gate requires stopping before reading the surface when the baseline does not reproduce.

## Underspecified Choices

- `c` adaptation uses deterministic one-step selfish payoff hill-climb over `c-delta`, `c`, `c+delta`; ties keep the existing trait, so concealment/reveal is not designer-nudged.
- Strategic `signal = gene * (1-c)` supersedes passive signal drift for the observable signal; the feeder balances observed `signal + allocation` geometrically so low observed signal attracts compensating resource, while lag/audit/capture/replicator mechanics are otherwise reused.
- Net payoff for c adaptation uses resource gain, capture gain, capture loss, camouflage cost, and expected committed-audit penalty; actual replicator fitness keeps the camouflage_audit form without adding capture as a positive fitness term.
- Committed audit cuts resource access by multiplying allocation by `1-C` for a fixed five-step window; kappa reduces feeding budget on committed-audit steps.
