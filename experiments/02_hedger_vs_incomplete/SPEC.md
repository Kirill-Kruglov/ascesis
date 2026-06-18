# SPEC: 02_hedger_vs_incomplete

## Pre-registration / Revised Artifact-Diagnostic Spec

This revised SPEC replaces the first broken implementation. The prior version had two artifacts: unbounded multiplicative axis explosion and identical behavior for `geometric_mean` and `incomplete_preference`. This version is for validation before push; publication-grade use still requires committing this SPEC before running.

## Central Question

Does geometric-mean optimization (bet-hedging) make incomplete preferences unnecessary, or is there a held-out environment class where incompleteness strictly wins?

## Hypotheses

- Active-spine hypothesis: incomplete preferences can strictly outperform a geometric-mean hedger in held-out environments where one axis is a non-tradeable constraint and no valid common currency exists.
- Failure hypothesis: once environments are specified without artifacts, the geometric hedger catches up everywhere.

## Environment Spectrum

- Scalarizable stationary environments: both axes are positive cardinal quantities, so geometric mean is valid.
- Scalarizable regime-shift environments: both axes remain cardinal, but regimes change.
- Non-scalarizable incommensurable environments: one axis is a non-tradeable boolean/categorical constraint. No valid geometric mean exists over the true outcome. The hedger is reported as `geometric_mean_invalid_proxy` in those environments to make the artifact explicit.

## Agents

- `arithmetic_mean`: complete scalar ordering over numeric axes.
- `geometric_mean`: complete scalar ordering by expected log/geometric mean when valid; invalid proxy baseline when the environment is non-scalarizable.
- `incomplete_preference`: partial order. It returns maximal admissible actions under non-tradeable constraints and records incomparability when numeric gains cannot dominate a threshold violation.

## Metrics

- Held-out survival rate.
- Bounded mean score, capped to avoid numerical explosion.
- Violation rate for non-tradeable constraints.
- Action divergence between `geometric_mean` and `incomplete_preference`.
- Explicit list of held-out environments where `incomplete_preference` strictly exceeds `geometric_mean`/invalid proxy on survival and has no higher violation rate.

## Seeds

Seeds: 2000..2049. Episode length: 60. Scores are additive and clipped per step; no unbounded products.

## Held-out Rule

Only held-out environments decide the comparison. Do not tune agents using held-out outputs. This diagnostic run logs zero improvement iterations for all sides.

## Artifact Checks

- `finite_values`: all reported numeric values must be finite and within the declared cap.
- `agent_divergence`: `geometric_mean` and `incomplete_preference` must choose differently in at least one held-out environment, or the report must prove they cannot diverge by construction.
- `non_scalarizable_check`: every incommensurable environment must mark `valid_geometric_mean_available=false`; hedger scores there are invalid proxy baselines, not valid geometric means.

## Negative Results

If the strict-win list is empty after the artifact checks pass, publish it as evidence that this toy family did not find an incompleteness advantage.

## Revision after external validation

The geometric-mean agent was strengthened to approximate expected log growth with a variance penalty. In scalarizable environments, incomplete preferences should not beat a correctly implemented hedger merely because the hedger ignores variance. Non-scalarizable held-out environments are no longer reported as "wins over hedging"; they are reported as `hedger_not_applicable` because a valid scalar geometric mean is unavailable.

Sacred/protected-value floors are a manual-validity question. If they model real protected values, they support the narrowed branch. If not, they are an artifact.
