# SPEC_IMPLEMENTED_10: Minimal Enforcement for Blind Consequence-Feeder

Source memo: `/home/master/Documents/my/Experiment-10_Minimal_Enforcement_for_Blind_Consequence-Feeder.md`.

Status: follow-up runner on top of Experiment 09. It keeps the Experiment 09 substrate and adds only costly type-blind enforcement variants. Outputs go to `results_10/` and do not overwrite Experiment 08 or 09 outputs.

## Mission

Experiment 09 broke trivial policies but found no surviving consequence-neighbor policy under strict capture semantics. Experiment 10 tests whether minimal type-blind enforcement, triggered only by delayed realized neighbor consequences, can reduce capture enough to create a non-trivial viability kernel.

## Enforcement Policies

- `neighbor_penalty`: delayed negative neighbor consequence reduces future zone allocation for `penalty_duration`.
- `neighbor_quarantine`: repeated negative neighbor consequence restricts migration out of the whole zone.
- `neighbor_audit_penalty`: stochastic costly audit triggered by bad delayed neighbor consequence; penalty is zone-level, not type-specific.
- `consequence_plus_diversity`: neighbor enforcement plus non-adversarial diversity floor plus response-to-aid discrimination.

Comparators retained from Experiment 09: `feature_proxy`, `always_cut_sagging`, `always_aid_sagging`, `monoculture_optimizer`, `self_consequence`, `neighbor_consequence`, `local_global_neighbor`, `response_to_neighbor_aid`, `diversity_non_adversarial_only`.

## Cost Semantics

Enforcement is not free. The runner records audit/quarantine/enforcement cost share and false-positive punishment rate. Penalty/quarantine reduces resource access for all agents in the zone and damages doves as collateral when applied to catastrophe zones.

## Sweep Coverage

The runner sweeps enforcement strength, audit probability, audit cost, penalty duration, quarantine strictness, observation delay, irreversible-harm horizon, adversarial strength, catastrophe severity, scavenger worlds, and migration speed/cost. `catastrophe_severity` controls the magnitude of catastrophe shocks in Experiment 10 worlds; this makes the memo parameter observable while keeping the Experiment 09 substrate shape.

## Viability Criterion

A held-out cell is viable iff all hold:

- permanence >= 0.60;
- capture <= 0.20;
- collapse <= 0.20;
- fraction irreversible zones <= 0.25;
- adversarial share <= 0.35;
- mean welfare >= 0.55;
- non-adversarial diversity >= 0.45;
- enforcement cost share <= 0.30;
- false-positive punishment rate <= 0.20.

The report also includes strict `capture == 0` counts, but strict zero capture is not the only viability criterion. Raw viability is recorded for every world. A-eligible non-trivial enforcement viability additionally requires a capture-relevant world, nonzero enforcement events or cost, and the same viability thresholds above. Pure-catastrophe control cells are not counted as an enforcement kernel if no enforcement fires.

## Validation Gates

Invalid if hidden type enters policy observation, enforcement cost is zero, penalty/quarantine happens without delayed consequence evidence, T1/T2/T3 trivial policies survive, enforcement starves all zones, capture remains 1.0 for all enforcement settings in capture-relevant worlds, or no pure-catastrophe false-positive test is run.

## Verdict Options

A. Minimal type-blind consequence enforcement creates a non-trivial viability kernel.

B. Enforcement reduces capture but costs/collateral destroy viability.

C. Enforcement does not reduce capture enough.

D. Result invalid due to failed validation.
