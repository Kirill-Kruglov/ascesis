# 06 Sugarscape Governor SPEC

Status: pre-registered before the first run of this experiment directory.

## Question

Can the narrowed active spine, `non-scalarizable value structures exist and require non-scalar agents`, survive in a richer independent ecological model rather than only in toy environments?

Toy test 02 shows the mechanism cleanly. This experiment asks whether the same distinction remains visible in a Sugarscape-style ecology whose core dynamics were not built for this project.

## Source Model

The ecological core follows the canonical Sugarscape family from Epstein and Axtell, *Growing Artificial Societies* (1996): spatial sugar landscape, local vision, metabolism, growback, wealth inequality, aging, death, and reproduction.

Implementation target: Mesa's Sugarscape G1mt-style example, commonly described as growing Sugarscape with metabolism and trade. This repository uses a small self-contained Python implementation of those standard rules so the test can run without installing Mesa, while preserving the recognizable Sugarscape mechanics. Manual verification is required before publication-grade use if an exact upstream Mesa example must be vendored or imported instead.

## Hypothesis

In an environment where a scarce resource must be allocated between two population needs, an emergent non-tradeable reproduction floor can appear from demography. Near that floor, `incomplete_preference` governor should produce longer population survival than `geometric_mean` governor on held-out seeds.

## Failure Criterion

If `geometric_mean` survives as long as, or longer than, `incomplete_preference` on held-out seeds, incompleteness is not needed in this independent ecological setting. That is a valid negative result.

## Governors

- `arithmetic_mean`: chooses the allocation that maximizes a linear immediate estimate of current feeding and reproduction reserve.
- `geometric_mean`: chooses the allocation that maximizes expected log balance of the two axes, with a variance penalty. This is the corrected hedger pattern from test 02, not the under-tuned earlier version.
- `incomplete_preference`: uses a partial order. In scarcity, when both current feeding and reproduction reserve are under stress, it acts from a conservative maximal set and refuses allocations that push either axis below its operational floor.

## Environment Split

- Train seeds: `6000..6029`
- Held-out seeds: `7000..7029`

No tuning is performed in this first implementation. The split is still recorded to preserve discipline if later iterations tune drought severity or governor parameters.

## Resource Shock

Each run includes an acute drought interval (`45..135`) that lowers sugar growback. This is not a penalty for violating a floor. It is an ecological shock that changes resource availability.

## Metrics

- time to population collapse;
- population survival under resource shock;
- wealth Gini coefficient;
- held-out fraction where `incomplete_preference` has longer collapse time than `geometric_mean`;
- full survival curves across seeds, reported as median and interquartile bands.

Collapse is measured when population reaches zero. A demographic floor is estimated post hoc as the last time after which the population never recovers above `10%` of initial population. The governor does not observe or optimize this floor directly.

## Artifact Checks

1. Emergent floor check: the governor objective contains no explicit penalty for crossing a population or reproduction threshold.
2. Hedger sanity check: in a scalar risk probe, `geometric_mean` must choose the balanced action.
3. Seed-noise check: report distributions and interquartile bands, not a single run.
4. A/B identity check: all governors use identical seeds and environment parameters.

## Win Criterion

On held-out seeds, `incomplete_preference` is provisionally supported only if its median collapse time is higher than `geometric_mean` and the held-out pairwise win rate is above `0.55`.

If the condition fails, report the negative result.
