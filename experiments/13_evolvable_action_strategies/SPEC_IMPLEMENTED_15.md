# SPEC_IMPLEMENTED_15: Anti-Concentration vs Consequence Governance

Source memo: `/home/master/Documents/my/Experiment-15_Anti-Concentration_vs_Consequence_Governance.md`.

Status: follow-up on Experiment 14. This runner uses the Experiment 13 evolvable-strategy substrate and separates three policy families without adding new mechanisms:

- Part A: static type-blind anti-concentration without delayed consequence feedback.
- Part B: delayed consequence governance without fixed concentration caps.
- Part C: combined anti-concentration and consequence governance.

Outputs go to `results_15/`.

## Execution Order

The report and manifest present Part A first. If static anti-concentration alone is sufficient, that changes the theory: the arbiter is closer to a leverage/concentration limiter than a consequence-governance mechanism.

## Policy Families

Part A policies: `uniform_resource_cap`, `max_zone_share_cap`, `max_lineage_share_cap`, `anti_hhi_allocator`, `random_allocation_plus_cap`, `static_equalizing_allocator`.

Part B policies: `neighbor_consequence_allocator`, `response_to_aid_allocator`, `delayed_harm_throttle`, `consequence_weighted_resource_flow`, `consequence_weighted_migration_friction`.

Part C policies: `anti_concentration_plus_consequence_neighbor`, `anti_concentration_plus_response_to_aid`, `anti_concentration_plus_delayed_harm_throttle`, `full_exp14_best_policy`.

## Classification

Type AC: anti-concentration alone is sufficient.

Type CG: consequence governance alone is sufficient.

Type AC+CG: only combined policies are sufficient.

Type None: no viable region found.

Verdict options A-F follow the source memo.
