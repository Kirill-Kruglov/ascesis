# SPEC_IMPLEMENTED_11: Action-Channel Containment Instead of Zone Punishment

Source memo: `/home/master/Documents/my/Experiment--11_Action-Channel_Containment-Instead_of_Zone_Punishment.md`.

Status: follow-up runner on top of Experiment 10. It keeps the Experiment 09/10 substrate and adds type-blind action-channel controls. Outputs go to `results_11/` and do not overwrite earlier outputs.

## Mission

Experiment 10 showed that type-blind zone-level enforcement can fire and cost resources without reducing capture in capture-relevant worlds. Experiment 11 tests whether the failed granularity is the issue: instead of asking which zone should receive less, it asks which harmful causal channel should be rate-limited.

## Policies

Comparators retained: `no_enforcement`, `neighbor_penalty`, `neighbor_quarantine`, plus Experiment 09 validation trap policies.

Action-channel policies:

- `action_containment_extraction_cap`: delayed bad neighbor consequence limits capturable/interceptable extraction from aid in that zone.
- `action_containment_influence_throttle`: delayed bad neighbor consequence reduces outgoing harm from that zone to neighbors.
- `action_containment_anti_concentration`: allocation caps prevent a zone from accumulating excessive resource share unless delayed neighbor consequences are positive.
- `action_containment_migration_friction`: delayed bad neighbor consequence reduces outward migration flow from the zone.
- `action_containment_aid_escrow`: aid to sagging zones first repairs local non-transferable recovery capacity before becoming capturable resource.
- `action_containment_replication_throttle`: delayed bad neighbor consequence suppresses all local replication multipliers, type-blind.
- `combined_action_containment`: extraction cap + influence throttle + anti-concentration + migration friction + aid escrow + replication throttle.
- `combined_action_containment_plus_diversity`: combined containment plus non-adversarial diversity support.
- `combined_action_containment_plus_response_to_aid`: combined containment plus response-to-aid scoring.

## Blindness Discipline

Policy observation is still the delayed `Obs` object from Experiment 09/10. It does not expose population composition, hidden type, hawk counts, dove counts, or adversarial labels. Controls are triggered only by delayed realized neighbor consequences and aid history.

## Success Criterion

A cell is action-containment viable iff all hold:

- permanence >= 0.60;
- capture <= 0.20;
- collapse <= 0.20;
- fraction irreversible zones <= 0.25;
- adversarial share <= 0.35;
- mean welfare >= 0.55;
- non-adversarial diversity >= 0.45;
- containment cost share <= 0.35;
- false containment in pure catastrophe <= 0.20;
- containment events > 0 in capture-relevant worlds.

Strict `capture == 0` is reported separately.

## Validation Gates

Invalid if hidden type enters policy observation, controls fire without delayed consequence evidence, controls have zero cost, T1/T2/T3 trivial policies survive, action containment never fires, all zones are starved, pure-catastrophe false-containment test is absent, or capture remains 1.0 for every action-containment setting in capture-relevant worlds.

## Verdict Options

A. Action-channel containment creates a non-trivial viability kernel.

B. Action-channel containment reduces capture but costs/collateral destroy viability.

C. Action-channel containment does not reduce capture enough.

D. Result invalid due to failed validation.
