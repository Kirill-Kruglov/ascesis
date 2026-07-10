# First contact: received solvers on our worlds (Jul 10, no edits to received logic)

Runner: `worlds_general.run_language`, CAP=400 calls, seed 101.

| world | main | ref1 | ref2 | ref3 | A(ours) | Gt(ours) |
|---|---|---|---|---|---|---|
| cycle(17) | 17!=T | 17!=T | 17!=T | 17!=T | 17!=T | 17!=T |
| cycle(36) | 36!=T | 36!=T | 36!=T | 36!=T | 36!=T | 36!=T |
| alias(24,8) | 24!=T | 24!=T | 24!=T | 24!=T | **8!** | 24!=T |
| lollipop(6,12) | AB | AB | TO | TO | TO | TO |
| wobble(23) | AB | AB | AB | AB | 23! | 23! |
| nonstat | 17! | 17! | 17! | 17! | 17! | 17! |
| noisy(24,.1) | TO | TO | TO | TO | **13!** | **13!** |

Findings, registered before scout 11:

1. **Alias**: received solvers bypass the origin blur (mixed-word contextual
   pairs); our A is fooled (8). The Cayley-translated sham Gt is NOT fooled —
   the translation changed the effective interface channel. The registered
   dependent pair (A, Gt) decouples on alias worlds: derivation-dependence
   is not failure-profile identity. Input to the genealogy experiment.
2. **Wobble truth-label bias (ours, exposed by the clean-room build).** Our
   scouts labeled wobble truth = n (R-channel view — the A-language bias
   Opus called crack 3). Under the extensional task, net-mod-n mispredicts
   L-word pairs; the received solvers' AB is the more correct verdict.
   REGISTERED FIX for experiment A: truth labels must be extensional
   (predictive adequacy over the full word space): wobble → None,
   consistent with the dual-oracle plan (GPT §7 step 4).
3. **Noisy(0.1)**: (A, Gt) share the same confident wrong value (13) —
   the dependent-pair signature live; received solvers honestly TO.
   **Nonstat**: all six confidently claim 17 (switch lands after their
   convergence) — pure world-forced co-failure, registered null material.
