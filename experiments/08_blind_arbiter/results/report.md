# 08 Blind Type-B Arbiter Report

SPEC hash (declared): `c040d38edb530b8fd2ccbd5942557b3f0467a8942b6ae218bc90d22fbed8ab80`
SPEC hash (actual): `c040d38edb530b8fd2ccbd5942557b3f0467a8942b6ae218bc90d22fbed8ab80`

## Split / Grid

- train seeds: `3100..3129` (30)
- held-out seeds: `4100..4129` (30)
- R grid (actual): `0.182, 0.333, 0.375, 0.571, 0.833, 1.200, 2.000, 3.333, 6.500`
- settings: `[{"name": "r01", "capture_rate": 0.55, "lag": 9, "audit_period": 2}, {"name": "r02", "capture_rate": 0.45, "lag": 7, "audit_period": 2}, {"name": "r03", "capture_rate": 0.35, "lag": 6, "audit_period": 2}, {"name": "r04", "capture_rate": 0.28, "lag": 5, "audit_period": 2}, {"name": "r05", "capture_rate": 0.22, "lag": 4, "audit_period": 2}, {"name": "r06", "capture_rate": 0.18, "lag": 3, "audit_period": 2}, {"name": "r07", "capture_rate": 0.14, "lag": 2, "audit_period": 2}, {"name": "r08", "capture_rate": 0.1, "lag": 1, "audit_period": 2}, {"name": "r09", "capture_rate": 0.08, "lag": 0, "audit_period": 2}]`

## Calibration Gate

- C1 pass (R<=0.40, true permanence <0.10 for all regimes): `True`
- C2 pass (scalar at 0.80<=R<=1.50, true permanence <0.50 and final corr <0.70): `False`
- calibration gate: `False`
- scalar mid bucket true permanence: `0.000`
- scalar mid bucket final corr(signal, gene): `1.000`

## Located R* (held-out)

| regime | R* | true permanence rate around R* | notes |
|---|---:|---:|---|
| scalar | None | 0.000 | n/a |
| geometric | None | 0.000 | n/a |
| lexicographic | None | 0.000 | n/a |

## Summary Numbers

- scalar: mean true permanence `0.000`, mean corr(signal, gene) `1.000`
- geometric: mean true permanence `0.000`, mean corr(signal, gene) `0.646`
- lexicographic: mean true permanence `0.000`, mean corr(signal, gene) `0.651`

## Failure Modes

- camouflage faster than the window: `True`
- collective hack: `True`
- collective punishment of the innocent: `False`

## Interpretive Verdict

calibration failure: substrate does not reproduce the Thornley baseline; not valid for H1/H2.
unreachable predicate: C2; scalar corr stayed at 1.000 across calibration iterations.

## SPEC Under-Specification Notes
- capture / replicator dynamics: the exact functional form of share transfer under capture was not fully pinned down; this implementation uses a hidden true-share transfer-plus-replicator hybrid with signal-only arbitration.
- signal mutation: the exact mutation kernel was underspecified; this implementation uses allocation-following drift plus lag/audit feedback and noise, without any access to hidden behavior genes in the arbiter.
- audit process: the stochastic audit timing and focus are modeled as Bernoulli timing with random focus; the SPEC does not fully pin down its distribution.
- calibration iterations: substrate search is logged in the manifest; C1/C2 are never rewritten.
