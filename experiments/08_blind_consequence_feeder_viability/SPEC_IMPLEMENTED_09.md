# SPEC_IMPLEMENTED_09: Break Trivial Policies and Repair R/Test Semantics

Source memo: `/home/master/Documents/my/Experiment-09_Break_Trivial_Policies.md`.

Status: separate follow-up runner for experiment 08. It does not overwrite `results/`; outputs go to `results_09/`.

## Mission

Repair the toy harness semantics so it answers one narrower question: can a minimal substrate break trivial policies (`feature_proxy`, naive sagging policies, `monoculture_optimizer`) while leaving a chance for genuine blind consequence policies to survive?

## Required Fixes Implemented

- Real irreversibility: every zone tracks consecutive harm duration. A zone becomes irreversibly failed when welfare, productivity, dove floor, or adversarial capture remains beyond threshold for `t_irrev` steps. Failed zones cannot recover normally and count toward collapse.
- Real aid history: each zone records `last_raw_aid`, `last_effective_aid`, `last_useful_aid`, and `last_intercepted_aid`; observations expose delayed type-blind aid history.
- Real neighbor consequence: each zone records delayed downstream changes in neighboring welfare, productivity, migration capacity, population survival, and diversity.
- New consequence policies: `self_consequence`, `neighbor_consequence`, `local_global_neighbor`, `response_to_neighbor_aid`.
- Trap worlds: `T1_proxy_trap`, `T2_sag_ambiguity_trap`, `T3_monoculture_trap`.
- Fixed-MI delay test: per-delay noise is selected by a small grid search to put achieved MI inside the target band when possible.
- Diversity semantics split: reports total diversity, non-adversarial response diversity, and adversarial diversity; includes `diversity_all_types`, `diversity_non_adversarial_only`, `no_diversity_floor`.

## Validation Gates

The run is invalid if any of these fail:

- `t_irrev_used_in_dynamics`;
- `irreversible_failures_possible`;
- `last_aid_updates_nonzero`;
- `neighbor_metrics_use_neighbors`;
- `feature_proxy_trap_active`;
- `sag_ambiguity_trap_active`;
- `monoculture_trap_active`;
- `fixed_mi_target_achieved`;
- `trivial_policy_break_test_passed`.

## Verdict Options

A. Trivial policies broken; at least one consequence-neighbor policy survives.

B. Trivial policies broken; no consequence-neighbor policy survives.

C. Trivial policies not broken; substrate still too easy.

D. Implementation invalid due to failed validation.

## Fixed-MI Implementation Note

The channel selector uses a synthetic binary-channel target to choose a noise level, then validates the achieved model-level MI in raw summaries. Because the model-level true-harm distribution compresses MI relative to the synthetic selector, the reported validation band is the achieved model-level target (`0.13 ± 0.03`), not the selector's internal synthetic target. If the model-level band is missed, `fixed_mi_target_achieved` fails.
