# Constraint Map Seed after CL branch

## 0. Purpose

This seed prepares the next analytic phase after closing the CL branch. It is
not an experiment spec and not a proposal to continue learner tuning.

The purpose is to carry forward the constraints produced by CL0-CL2.2 without
treating the CL branch as substrate evidence.

## 1. Known impossible / closed directions

1. State-level `SAFE(state)` cannot stand in for learner-ledger admission.
2. An oracle-filtered action ledger is not substrate or derivability evidence.
3. A rule-family learner that encodes the transition family cannot count as learning-from-ledger evidence.
4. A global shuffled-target control is not sufficient when the learner has strong transition-family prior.
5. The current `FourZoneMassDomain` safe ledger plus generic subset-table learner produced no evidence-bearing transition-learning signal.

## 2. Known preconditions that survived

1. Boundary fidelity must be tested before learner claims.
2. Learner ledgers must be action-conditioned or transition-conditioned.
3. Layer audits and projection-blind baselines remain useful controls.
4. Equal-volume comparison remains necessary.
5. Negative controls must target both field leakage and learner prior.

## 3. Boundary between safety and derivability

CL1.1 showed a safe action ledger can exist on one toy lawful domain under an
oracle filter. That is a safety precondition only.

Derivability would require evidence that learner content is learned from the
ledger in a data-dependent way and then survives representation / internal
structure gates. CL2.2 did not supply that evidence.

## 4. What any next direction must satisfy

1. It must provide an action-conditioned or transition-conditioned safety interface.
2. It must separate oracle filtering from learner-visible data.
3. It must show data-dependence with a learner that does not encode the target transition law.
4. It must include controls against prior-dependence and marginal artifacts.
5. It must not claim transfer from a toy domain without a separate transfer gate.
6. It must not move to representation or derivability probes before learner evidence exists.

## 5. Candidate analytic questions

- What kind of lawful domain makes transition structure learnable without encoding the transition law into the learner?
- What is the minimal interface between substrate and learner that allows data-dependent learning?
- Can derivability be reframed as constraints on the data-generating process rather than on the learner?
- What does "noise is computation" change, if anything, under the constraints already found?
- Can accumulated negative results define a search-space boundary without becoming a new meta-synthesis project?

## 6. Forbidden next moves

- Tune learner until success.
- Treat CL1.1 ledger as substrate.
- Treat rule-family prior as learning.
- Jump to representation probe.
- Scale to LLM.
- Start general DSL / CEGIS / generator theory.
