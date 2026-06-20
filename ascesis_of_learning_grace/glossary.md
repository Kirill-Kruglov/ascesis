# Glossary

Working definitions for the project. These are local project labels; where possible, they are tied back to standard fields in [field_check.md](field_check.md).

A definition here is neutral about whether a direction is live. The current research stance lives only in [status.md](status.md). Some terms below (for example Non-Maximizing Core) belong to earlier framings and are kept for reading the map and its history, not as the active direction.

## Ascesis

A method/path label, not a technical claim: disciplined restraint in inquiry and presentation. In technical prose, prefer `restraint`, `bounded optimization`, or `reflective restraint` unless the section is explicitly about method.

## Seam

A boundary process that translates between an expressive representation and a more formal or executable representation. Related standard areas: semantic parsing, formal specification, verifier-in-the-loop translation (`field_check.md` node 6).

## Remainder

The part of a case that a partial translation, classifier, verifier, or simulator cannot handle within its stated guarantee. Related standard areas: reject option, selective prediction, uncertainty-aware semantic parsing (`field_check.md` nodes 2 and 6).

## Basis

The reference commitments, goals, invariants, or specifications against which later changes are checked. Related standard areas: goal-content integrity, reflective stability, corrigibility, cryptographic commitments (`field_check.md` nodes 1 and 3).

## Fixed Point

A condition that remains stable under reflection, self-modification, or successor construction. Related standard areas: tiling agents, Vingean reflection, Loebian obstacle, reflective stability (`field_check.md` node 1).

## Non-Maximizing Core

A governor core that is not trained or specified to maximize a scalar proxy. Related standard areas: quantilization, satisficing, mild optimization, incomplete preferences, social-choice correspondences, reward-hacking limits (`field_check.md` nodes 5, 11, 12, and 13). Historical note: this was an earlier active-spine label. The claim that such a core mechanically outperforms a correct scalar hedger is closed (see `rejected_branches.md` and `status.md`); the term is retained for the map, not as a performance direction.

## Incomplete Preferences / Incommensurability

A preference structure that does not force all trajectories into a single complete ordering. Related standard areas: incomplete preferences, partial orders, maximal sets, social-choice correspondences (`field_check.md` nodes 12 and 13).

## Governor

A bottom-up constraint-framed trajectory explorer, not a top-down optimizer. It searches among admissible trajectories inside a frame shaped by plural feedback, oversight, and explicit refusal boundaries (`field_check.md` nodes 2, 11, 12, 13, and 14).

## Goodhart Inevitability

The structural failure mode in which optimization of an imperfect proxy eventually degrades the intended target. Related standard areas: reward hacking, reward-model overoptimization, Goodhart geometry (`field_check.md` node 11).

## Lyapunov Horizon

The finite time range over which a sandbox or model remains predictively coupled to the target system before divergence dominates. Related standard areas: Lyapunov time, chaos predictability, critical slowing down, early-warning signals (`field_check.md` node 8).

## Bet-Hedging

A strategy family for variable environments that sacrifices some short-run or arithmetic-mean performance to improve long-run multiplicative survival or geometric-mean fitness. Related standard areas: evolutionary bet-hedging, Kelly criterion, portfolio theory (`field_check.md` node 15). This is type A scalar optimization, not incomplete preferences.

## Geometric-Mean Fitness

Long-run multiplicative fitness measured through the geometric mean, equivalent in many models to maximizing expected log growth. Related standard areas: bet-hedging, stochastic population growth, Kelly criterion (`field_check.md` node 15).

## Kelly Criterion

A betting/allocation rule that maximizes expected logarithmic wealth growth under a specified probabilistic model. Related standard areas: information theory, growth-optimal betting, portfolio allocation (`field_check.md` node 15). It remains a complete scalar objective once probabilities and payoffs are specified.

## Aggregator Invariance (of Goodhart)

The observation that replacing one aggregation of a measured value-vector with another (arithmetic, geometric, leximin, Nash) does not remove proxy failure but relocates it. Related standard areas: Goodhart's law and its variants, reward hacking (`field_check.md` nodes 11 and 17).

## Pareto-Hacking

The failure mode of multi-axis (geometric / Pareto / Nash-product) aggregation: an agent satisfies every measured axis with cheap weak-Pareto gestures rather than improving what matters, because the aggregator forbids letting any axis collapse. Related standard areas: Goodhart variants, multi-objective optimization (`field_check.md` nodes 11, 15, and 17).

## Sycophancy (rater-axis Goodhart)

The case of Pareto-hacking where one measured axis is the human rater: the cheapest way to keep that axis high is to tell the rater what they want rather than what is true. Related standard areas: sycophancy in language models, RLHF approval gaming (`field_check.md` node 18).

## Non-Tradeable Axis

A value dimension removed from the aggregation entirely, as a hard constraint, so it cannot be weak-Pareto-eroded. Whether such axes are real in human values is successor question (a) in `status.md`. Related standard areas: protected and sacred values, taboo trade-offs (`field_check.md` node 16).

## Detection / Refusal of Invalid Scalarization

The agent-side property of recognizing that no valid scalar currency exists for the current choice and abstaining from scalarizing it, rather than surviving longer. Framed as reject-option correctness. This is successor question (b) in `status.md`. Related standard areas: reject option, selective prediction (`field_check.md` node 2; bridge 4).
