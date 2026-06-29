# BA1.E1 Mechanism Revision

The five-way taxonomy is useful but not perfectly separable in the current code.

## Supported Splits

- MB1 should be split into observation delay and explicit response-memory fields. Both enter `_delayed_obs` / `Obs`, but they are not the same mechanism.
- MB2 should be split into allocation normalization and containment caps/redistribution. The weak ablation had to keep interpretive triggers while removing resource competition.
- MB5 should be split into policy-visible relative observables and diagnostic/final metrics. The former can be neutralized; the latter remain part of measurement and 18.0 projection.

## Inseparable Components

- MB3 and MB2 touch the same `choose_alloc` path for containment policies: bad-consequence interpretation sets timers before capped redistribution acts.
- MB4 affects future welfare indirectly through mass, payoff, mutation, migration, and pruning. Freezing it preserves immediate welfare formulas but changes the long-run substrate semantics.

## Taxonomy Verdict

- Final diagnostic decision: `Case C / H2_supported`.
- The taxonomy is supported as a first pass, but the implementation suggests submechanisms rather than five cleanly orthogonal axes.
