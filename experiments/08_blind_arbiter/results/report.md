# 08 Blind Type-B Arbiter Report

SPEC hash (declared): `f5079dc50c5fe55d0234b13905cadcd3f7267878a131d023f3a4defa551ac177`
SPEC hash (actual): `f5079dc50c5fe55d0234b13905cadcd3f7267878a131d023f3a4defa551ac177`

## Split / Grid

- train seeds: `3100..3129` (30)
- held-out seeds: `4100..4129` (30)
- R grid (actual): `0.182, 0.333, 0.375, 0.571, 0.833, 1.200, 2.000, 3.333, 6.500`
- settings: `[{"name": "r01", "capture_rate": 0.55, "lag": 9, "audit_period": 2}, {"name": "r02", "capture_rate": 0.45, "lag": 7, "audit_period": 2}, {"name": "r03", "capture_rate": 0.35, "lag": 6, "audit_period": 2}, {"name": "r04", "capture_rate": 0.28, "lag": 5, "audit_period": 2}, {"name": "r05", "capture_rate": 0.22, "lag": 4, "audit_period": 2}, {"name": "r06", "capture_rate": 0.18, "lag": 3, "audit_period": 2}, {"name": "r07", "capture_rate": 0.14, "lag": 2, "audit_period": 2}, {"name": "r08", "capture_rate": 0.1, "lag": 1, "audit_period": 2}, {"name": "r09", "capture_rate": 0.08, "lag": 0, "audit_period": 2}]`

## Calibration Gate

- C1 pass (R<<1 fails for all): `False`
- C2 pass (scalar hacked: corr(s,a) falls and permanence degrades): `False`
- calibration gate: `False`

## Located R* (held-out)

| regime | R* | permanence rate around R* | notes |
|---|---:|---:|---|
| scalar | None | 0.000 | shift relative to scalar: n/a |
| geometric | 0.182 | 1.000 | shift relative to scalar: n/a |
| lexicographic | None | 0.000 | shift relative to scalar: n/a |

## Summary Numbers

- scalar: mean permanence `0.000`, mean corr(s,a) `1.000`
- geometric: mean permanence `1.000`, mean corr(s,a) `0.742`
- lexicographic: mean permanence `0.004`, mean corr(s,a) `0.672`

## Failure Modes

- camouflage faster than the window: `True`
- collective hack: `True`
- collective punishment of the innocent: `True`

## Interpretive Verdict

stand does not measure the question; calibration gate failed.

## SPEC Under-Specification Notes
- capture / replicator dynamics: the exact functional form of share transfer under capture was not fully pinned down; this implementation uses a transfer-plus-replicator hybrid with symmetric loss distribution.
- signal mutation: the exact mutation kernel was underspecified; this implementation uses resource-following drift plus noise, with no direct access to hidden a_g.
- audit process: the stochastic audit timing and focus are modeled as Bernoulli timing with random focus; the SPEC does not fully pin down its distribution.
