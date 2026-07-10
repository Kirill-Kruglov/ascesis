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

## C8 first contact (Jul 11): the common-prior cell fires 24/24

| world | A (Fable) | opus-A (clean room, Anthropic) | gpt-A | gpt-B |
|---|---|---|---|---|
| alias(24,8) | 8! | **8!** | 24=T | AB |
| noisy(24,.1) | 13! | **13?** | TO | AB |
| wobble | 23! | AB | AB | AB |

Mini-battery (4 alias + 4 noisy worlds × 3 seeds): **A == opus-A on the
wrong VALUE in 24/24 cases; A == gpt-A in 0/24.** On noisy the wrong
value varies with seed (13 → 9 → 1) and opus-A varies IN LOCKSTEP:
its main solver converged to the same linear origin scan as our A —
identical schedule, identical exposure to the same oracle stream.
Clone-by-convergent-design at zero communication.

Registered findings:
1. **The clean room does not produce independence when priors are
   shared.** "Common causes are W and I only" was false; the model-family
   prior is a common cause, now measured (Eckhardt–Lee co-error, live).
   Review Y's K2b attack is empirically confirmed before the main run.
2. The five-minds doctrine is measurable independence engineering:
   family diversity, not session diversity, carries it (n=2: same family
   → same walk, 24/24).
3. Scout 11's (A, gpt-A) CLEAN is retroactively strengthened: the
   cross-prior contrast (0/24 vs 24/24) anchors the C8 diagnostic axis.
4. The encoding axis is alive too: gpt-B abstains on alias where gpt-A
   solves — same prior, different specification, different behavior.

## Scout 16 (OC at scale) + Grok/Gemini first contact (Jul 11)

OC at scale (R_INST=8, K=5, frozen rule): derived 4/4 flagged on
schedule-adaptive bases (W static missed, as diagnosed); clones 3/4.
"FPR 2/10" dissolves on inspection: (A,oA) was MISLABELED independent —
the instrument correctly caught the documented common-prior pair; and
(A,P) exposes that ALL same-author pairs (A/W/M/P are one author) are
not certified-independent. Certified cross-prior pairs (X,oA): clean 3/3.
Estimand lesson: OC's FPR must be computed on certified cross-prior
pairs only; the bank inherits C8 classes.

Grok/Gemini contact — the registered prediction FELL both ways:

| pair | value agreement with A (24 cells) |
|---|---|
| A ~ opus-A | 24/24 |
| A ~ grok | 12/24 |
| A ~ gemini | 0/24 |

Gemini's memo SAYS "linear scanner" yet decouples fully (its validation
battery defeats the alias blur: finds true n); Grok's memo says
"birthday" yet half-couples (origin-channel probes fall into A's trap).
**Coupling follows the effective probe channel + validation discipline,
not the declared algorithm class.** The C8 unit of dependence refines:
not family, not declared mechanism — the converged channel; the prior
only shifts channel probabilities (Anthropic → origin-scan 24/24; Grok
mixed 12; GPT/Gemini contextual+validated 0). The bank now holds SIX
provenance families across FOUR priors — the certified cross-prior
independents the lock-scale OC was missing.
