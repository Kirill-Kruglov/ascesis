# Glossary

Working definitions for the second circle. These are local project labels; where possible, they are tied back to standard fields in [field_check.md](field_check.md).

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

## Second Circle

The public pass through the material after the raw dialogue and field check. It is not a transcript and not a claim of novelty; it is a structured map of connections selected after the first pass (`field_check.md` as the grounding layer).

## Non-Maximizing Core

A governor core that is not trained or specified to maximize a scalar proxy. Related standard areas: quantilization, satisficing, mild optimization, incomplete preferences, social-choice correspondences, reward-hacking limits (`field_check.md` nodes 5, 11, 12, and 13).

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
