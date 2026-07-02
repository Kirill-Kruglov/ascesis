# CL-PM0 Closed-Direction Entries

## CL branch: safe action ledger without generic learner signal

### Status

CLOSED AS SUBSTRATE / DERIVABILITY PATH.
RETAINED AS BOUNDARY / LEDGER PRECONDITION EVIDENCE.

### Evidence chain

- CL0: proposed a layer-audited safe-transition ledger over a generated lawful domain as a weakened boundary candidate, not as substrate evidence.
- CL1: produced `BOUNDARY-FIDELITY-OK` on `FourZoneMassDomain`; candidate state boundary had false-safe rate `0.0`, false-positive rate `0.0`, and equal-volume possible.
- CL1.1: produced `ACTION-LEDGER-OK`; candidate action ledger admitted `31142` transitions with unsafe admitted transition rate `0.0`, while CL1 state-level carryover admitted unsafe actions at rate `0.2339757498404595`.
- CL2: produced `LEARNER-LEAKAGE-FAIL`; primary learner scored high, but shuffled-target control exceeded threshold with `shuffled_target_accuracy = 0.6463414634146342`.
- CL2.1: produced `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT`; no direct leakage/evaluation bug was found, but the primary rule-family learner's shuffled-control failure was best explained as transition-family prior artifact.
- CL2.2: produced `NO-GENERIC-LEARNER-SIGNAL`; the evidence-eligible generic learner had full-data structural accuracy `0.0`, while the rule-family learner remained diagnostic-only with `1.0` holdout accuracies.

### Closed directions

1. State-level SAFE -> learner ledger.
2. Oracle-filtered ledger -> substrate evidence.
3. Rule-family learner -> learning evidence.
4. Original shuffled-target gate -> sufficient anti-artifact control.
5. Current safe ledger -> generic transition-learning evidence.

### Durable constraints

1. Future learner ledgers must be action-conditioned or transition-conditioned.
2. A safe oracle-filtered ledger is only a precondition; it is not substrate evidence.
3. Learners that encode the domain transition family are diagnostic-only.
4. Anti-artifact controls must defeat prior-dependence and marginal artifacts, not only field leakage.
5. A safe ledger must become evidence-bearing for generic, data-dependent learning before representation or derivability probes are allowed.
6. Toy-domain boundary success does not transfer without a separate transfer gate.
7. Oracle labels, future outcomes, admission decisions, and reporting-only metrics must remain audit-only.

### Future admissibility condition

A future branch may proceed only if it supplies:

1. action-conditioned or transition-conditioned safe ledger;
2. non-oracle learner or learner-interface with data-dependence;
3. controls that defeat prior-dependence and marginal artifacts;
4. no substrate / derivability claim before representation and derivation gates.
