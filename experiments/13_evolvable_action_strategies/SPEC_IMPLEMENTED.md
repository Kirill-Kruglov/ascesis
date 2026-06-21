# SPEC_IMPLEMENTED: Experiment 13 - Evolvable Action Strategies

Source memo: `/home/master/Documents/my/Experiment-13_Replace_Hidden_Types_with_Evolvable_Action_Strategies.md`.

Status: standalone minimal substrate. This experiment does not reuse the hidden-type population mechanics from Experiments 09-12. There are no fixed `dove`, `hawk`, or `scavenger` causal primitives. Lineages carry continuous heritable strategy parameters; labels such as exploitative-like or cooperative-like are derived only for post-hoc metrics.

## Core Question

Can a blind consequence-feeder select against harmful strategies without observing hidden strategy parameters, if harmfulness is expressed through controllable action channels?

## Hidden Strategy Vector

Each lineage has population mass, resource stock, mutation variance, and continuous hidden parameters:

- `extraction_rate`
- `aid_interception_rate`
- `neighbor_harm_rate`
- `deception_investment`
- `migration_follow_rate`
- `replication_aggressiveness`
- `cooperation_investment`
- `shock_resilience_contribution`
- `productive_contribution`

The feeder observation object excludes these fields. Runtime checks assert that no strategy parameters or derived labels enter policy observation.

## Policies

- `feature_proxy`
- `consequence_neighbor`
- `response_to_aid`
- `action_channel_containment`
- `consequence_plus_diversity`

## Worlds

- `W1_proxy_goodhart`
- `W2_pure_capture`
- `W3_catastrophe_ambiguity`
- `W4_scavenger_catastrophe`
- `W5_monoculture_shock`
- `W6_mutation_corridor`

## Causal Audit

Before governance results are interpreted, the runner repeats a simplified Experiment 12 in the new substrate:

- `audit_no_intervention`
- `oracle_suppress_exploit_strategy_params`
- `type_blind_extraction_cap`
- `type_blind_aid_escrow`
- `type_blind_anti_concentration`
- `type_blind_migration_friction`
- `type_blind_replication_throttle`
- `combined_type_blind_containment`

Audit classes:

A. Type-blind levers reduce exploitative strategy mass.

B. Only oracle reduces exploitative strategy mass.

C. Neither reduces it.

## Final Verdict Options

A. Evolvable-strategy substrate exposes type-blind causal levers and a non-trivial viability kernel exists.

B. Type-blind levers reduce exploitation, but no viability kernel exists.

C. Exploitation remains controllable only by oracle strategy access.

D. Model invalid due to failed validation.
