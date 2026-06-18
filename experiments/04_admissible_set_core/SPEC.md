# SPEC: 04_admissible_set_core

## Pre-registration

This SPEC fixes the admissible-set toy governor before running. For publication-grade runs, commit this file first and record the commit SHA in `results/run_manifest.json`.

## Question

Can a bottom-up governor construct a nonempty admissible set from incompatible agents' constraints without aggregating their preferences into one scalar function?

## Hypothesis

A constraint-framed governor can preserve a nonempty admissible set for moderate disagreement and frame width. Failure hypothesis: under realistic disagreement, the intersection collapses to empty too quickly, making the bottom-up governor operationally weak.

## Environment

Trajectory candidates are points in a 2D policy/outcome grid. Each agent has an ideal point and accepts trajectories within a frame width. The governor returns the intersection of all accepted sets.

## Metrics

- Admissible set size as a fraction of candidate universe.
- Empty-set rate by number of agents `N` and frame width.

## Sweep

- Agents: 2, 4, 8, 16, 32.
- Frame widths: 0.15, 0.25, 0.35, 0.45, 0.55.
- Seeds: 4000..4049.

## Held-out Rule

This is a feasibility sweep, not a tuned contest. If frame rules are modified after inspecting outputs, make a new preregistration commit.

## Symmetry of Effort

No competing side is tuned here. Improvement iterations are logged as zero.

## Negative Results

If the admissible set collapses for realistic widths, that is evidence against the operational viability of this governor sketch.

## Artifact Check Revision

Adds `clustered` preference generation alongside the original dispersed IID profile. This checks whether admissible-set collapse persists under structured disagreement or only under worst-case-like random dispersion.

## Cross-cutting cleavages revision

Adds `cross_cutting` preference generation: agents combine independent high/low positions on two axes, so factions overlap rather than forming one aligned cluster. This is intended as a more realistic middle case between optimistic clustered agreement and pessimistic IID dispersion.
