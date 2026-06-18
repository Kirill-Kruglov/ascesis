# SPEC: 05_reflective_stability_of_incompleteness

## Pre-registration

This SPEC fixes the high-risk toy self-modification experiment before running. For publication-grade runs, commit this file first and record the commit SHA in `results/run_manifest.json`.

## Question

Does an agent with a partial order preserve incompleteness under self-modification, or does it complete the order for instrumental convenience?

## Hypothesis

Failure hypothesis, expected: the agent completes its partial order whenever the convenience benefit exceeds the penalty for violating incomparability. A stable construction, if found, would require explicit preservation incentives or proof obligations and would be a serious candidate for deeper work.

## Toy Model

The agent repeatedly chooses whether to keep a partial order or install a complete scalar tie-breaker. Completion gives planning convenience but incurs an incomparability-violation penalty when the environment presents ontologically incommensurable choices.

## Metrics

- Fraction of runs that remain partial through time.
- First completion time.
- Trace of order type over time.

## Sweep

- Convenience benefit: 0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.2, 0.4, 0.8.
- Violation penalty: 0.0, 0.1, 0.2, 0.4, 0.8.
- Seeds: 5000..5049.
- Horizon: 40.

## Held-out Rule

No tuning is performed. If the transition rule changes after results are inspected, make a new preregistration commit.

## Symmetry of Effort

No competing side is tuned here. Improvement iterations are logged as zero.

## Negative Results

Collapse to complete ordering is the expected negative result and should be published if observed.

## Artifact Check Revision

Adds a fine-grained convenience sweep from 0.00 to 0.10 to distinguish gradual instrumental erosion from a hard-coded threshold artifact.

## Maintenance cost revision

Adds ongoing maintenance costs for complete ordering: `0.00`, `0.02`, and `0.05`. If incompleteness still collapses under high maintenance cost, the erosion signal is stronger. If partiality survives when complete-order maintenance is costly, the earlier result was partly an artifact of a free tie-breaker.
