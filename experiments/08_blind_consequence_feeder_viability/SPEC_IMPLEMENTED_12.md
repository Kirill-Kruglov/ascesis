# SPEC_IMPLEMENTED_12: Causal Audit of Capture Dynamics

Source memo: `/home/master/Documents/my/Experiment-12_Causal_Audit_of_Capture_Dynamics.md`.

Status: diagnostic follow-up runner on top of Experiment 11. It does not add feeder policies. It applies explicit causal probes to test whether capture is reachable by any type-blind intervention or only by hidden-type oracle interventions. Outputs go to `results_12/` and do not overwrite earlier outputs.

## Mission

Experiments 09-11 failed because capture stayed at 1.0 in capture-relevant worlds. Experiment 12 audits whether the substrate exposes any non-type causal lever that can reduce capture, or whether capture can be changed only by oracle access to hidden type.

## Worlds

The runner uses Experiment 11 substrate worlds: `PURE_CAPTURE`, `MIXED_CAPTURE_CATASTROPHE`, `SCAVENGER_CATASTROPHE`, and `FIXED_MI_DELAY` as the available fixed-MI capture analogue. `PURE_CATASTROPHE` is retained as a sanity check only.

## Intervention Ladder

- `no_intervention`: baseline.
- `oracle_kill_hawks`: non-blind, directly suppresses hawk/scavenger populations.
- `oracle_freeze_hawk_reproduction`: non-blind, prevents hawk/scavenger population increases.
- `type_blind_freeze_all_reproduction_in_bad_zones`: delayed bad-neighbor consequence suppresses all local reproduction.
- `type_blind_resource_cap_bad_zones`: delayed bad-neighbor consequence caps local resource/population concentration.
- `type_blind_no_outgoing_migration_bad_zones`: delayed bad-neighbor consequence blocks outgoing migration.
- `type_blind_no_interceptable_aid_bad_zones`: delayed bad-neighbor consequence converts aid to non-interceptable local recovery.
- `type_blind_edge_cut_bad_zones`: delayed bad-neighbor consequence suppresses outgoing neighbor harm.
- `global_density_cap`: type-blind population/concentration cap applied globally.
- `combined_type_blind_maximal`: all type-blind probes combined.

Oracle probes are explicitly labeled non-blind in raw outputs. Type-blind probes use only delayed consequence observation for triggers; they do not read population composition or hidden type in the intervention decision path.

## Classification

A. Type-blind causal control of capture exists in this substrate.

B. Type-blind control partially reduces capture but not enough for viability.

C. Capture is controllable only by hidden-type oracle interventions.

D. Even oracle interventions do not reduce capture; metric/dynamics invalid.
