# Experiment 15.0.1 — old vs new measurement

We did NOT change the four rewrite systems, seeds, or horizons. We repaired three instruments and recomputed. Below: what each repair changed, per system.

- seed=42, samples=20000, horizons=[1, 2, 4, 8, 16, 32, 64, 128], obs_depth=4, epsilon=0.01, K=3

## Defect 1 — closure horizon: single collapsed `h` -> per-channel sustained plateau

| system | OLD h_0.01 (all channels) | NEW state | NEW trajectory | NEW normal_form | NEW semantic | non-monotonic? |
|---|---|---|---|---|---|---|
| A_dead_control | 2 | 2 | 32 | 2 | 2 | trajectory, semantic_label |
| B_fake_live_control | 2 | 2 | none | none | 2 | state, trajectory, semantic_label |
| C_collapsing_live_candidate | 2 | none | 32 | none | none | state, trajectory, semantic, semantic_label |
| D_structured_live_candidate | 2 | 2 | 8 | 4 | 2 | trajectory |

`none` = the marginal novelty-*rate* never reached a K=3 sustained plateau; this alone is NOT a verdict of openness — a non-monotonic rate can still have a saturated *count* (see Defect 3 / the count-based axis, e.g. C-semantic). The point here is only that the old estimator froze A, B and C all at h=2 by firing on the first shared early dip, whereas the repaired per-channel estimator separates them and flags non-monotonicity.

## Defect 2 — single label -> three-axis classification

| system | OLD classification | NEW state_axis | NEW trajectory_axis | NEW semantic_axis |
|---|---|---|---|---|
| A_dead_control | dead | trivial | saturating | trivial |
| B_fake_live_control | fake_live | open | saturating | trivial |
| C_collapsing_live_candidate | dead | saturating | open | saturating |
| D_structured_live_candidate | dead | trivial | trivial | trivial |

## Defect 3 — new semantic-class channel vs syntactic (noisy-TV made measurable)

The decisive quantity is the **count** of distinct semantic classes as a function of horizon — a novelty *rate* can look 'moderate' purely because a finite class set is divided by a large sample budget. Below: where each channel's count saturates.

| system | syntactic count (trajectory) | semantic class count | semantic saturates at horizon | sample-limited? |
|---|---|---|---|---|
| A_dead_control | 2201 | 8 | 16 | no |
| B_fake_live_control | 13953 | 9 | 4 | no |
| C_collapsing_live_candidate | 19999 (= sample cap) | 1024 | 64 | yes (trajectory) |
| D_structured_live_candidate | 364 | 2 | 8 | no |

A huge syntactic count with a tiny, frozen semantic count = syntactic novelty without new meaning (= noisy-TV). The semantic count saturating to a finite set = the substrate is semantically closed at that size.

## Interpretation (the single question this experiment answers)

- **A_dead_control**: state-trivial / trajectory-saturating / semantic-trivial
- **B_fake_live_control**: state-open / trajectory-saturating / semantic-trivial
- **C_collapsing_live_candidate**: state-saturating / trajectory-open(sample-limited) / semantic-saturating
- **D_structured_live_candidate**: state-trivial / trajectory-trivial / semantic-trivial

## Conclusion (kill / honesty condition)

**No system is semantic-open.** Every system's distinct-semantic-class count saturates to a finite set (A=8, B=9, C=1024, D=2). This is the task's first honesty condition: the repaired instruments do NOT rescue a live zone, so Experiment 15's negative conclusion **stands and is now trustworthy** — it was not merely a closure-horizon artifact.

What the repair *does* reveal (which the old single 'dead' label hid): the collapsing candidate C carries by far the richest bounded semantic set (1024 classes) versus the noisy-TV control B (9) and the structured candidate D (2). C's semantic ceiling is imposed by its `depth<12` cap on `G_expand`; that bound — not a measurement defect — is the precise target for Experiment 15.1. C's maximal trajectory novelty is sample-limited (it fills the entire sample budget) and is syntactic only, so it is NOT evidence of liveness.
