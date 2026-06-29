# Experiment 18.0 — Shield Synthesis from the justitia Boundary

**Classification: `shield_synthesizable`.** Precondition for the special theory holds: `True`. Proceed to 18.1: `True`.

## 1. The collapse condition in the actual justitia code

`collapse = mean(zone_welfare) < 0.32  OR  #{zones: welfare<0.20} >= 4  OR  total_mass < 35` (`substrate.py:683/756`). This is the unsafe set **U**. My reimplementation matches the code's own collapse flag on **100.0%** of 16000 harvested states. `permanence` is the stronger thriving predicate; the shield keeps the system out of `collapse`.

## 2. Is the unsafe set upward-closed? Under what ordering?

**Yes.** Ordering: componentwise badness: zone_welfare<= , total_mass<= , resource_hhi>= , capture_index>=. Of **99580** upward (toward-worse) perturbations of U-states, **100.0%** stayed in U (0 counterexamples). U is a monotone Boolean combination of threshold tests on degradation coordinates. **Caveat:** concentration alone does NOT define U — 252 high-concentration-but-safe and 1339 low-concentration-but-collapsed states exist, so the ordering MUST include the welfare/mass coordinates (exactly what the shield abstraction's `a` coordinate carries).

## 3. Is the transition relation monotone? Is the sword reaction bounded?

**Monotone (bounded reaction): yes.** Abstract monotonicity test on the bounded sword: fraction_monotone = 1.000. Real-substrate reaction is bounded: when containment is active the max per-step welfare restoration is **0.082** and max concentration reduction **0.032** (mean welfare change +0.0032/step). No step resets an unbounded amount — escrow/anti-concentration corrections are clamped and accumulated-harm volumes are never reset. `sword_reaction_bounded = True`.

## 4. Did backward reachability terminate (= shield synthesizable)?

**Yes.** On the monotone N^2 abstraction (scales gated by bounded sword), backward coverability reached a fixpoint in **1** iteration(s); doomed fraction **0.111**, doomed basis [(0, 40)]. `pre(↑U)` stays upward-closed (`True`) — the WSTS coverability invariant holds. The synthesized shield (`shield_sample.json`) marks a gated boundary band where the sword is *required* (`must_react`) to avoid collapse.

## 5. If it failed — blocking issue & reformulation hint

Not a failure. (blocking_issue = `None`, reformulation_hint = `None`.)

## 6. Controls — does the instrument discriminate?

- **Positive (scales-only, no sword):** synthesizes cleanly — backward reachability terminated in 41 iterations (doomed fraction 1.000: with no corrective power every non-trivial state is doomed, which is the correct semantics). `clean_synthesis = True`.

- **Negative (injected unbounded reaction):** the monotonicity test **catches it** (fraction_monotone = 0.143, reaction magnitude up to 41), and `pre(↑U)` is **no longer upward-closed** (`False`). `test_discriminates = True`. This proves the instrument can detect failure, so its success is trustworthy (15.x lesson).

## 7. Does the special theory's precondition hold — proceed to 18.1?

**True.** The justitia collapse boundary is upward-closed and the sword's corrective reaction is bounded, so the abstracted coupling is a monotone WSTS for which backward-reachability coverability terminates and synthesizes a shield. The special theory's precondition — *the boundary is expressible as a decidable safety invariant* — **holds at the abstraction faithful to the measured dynamics**. Residual risk: the abstraction's bounded-reaction assumption is what makes it a WSTS; Step 2 confirms the real sword reaction is bounded, so the assumption is grounded. **Proceed to 18.1: True.**

## Honesty notes

- The full justitia substrate is a high-dimensional stochastic ABM, not literally a WSTS; the shield is synthesized for a 2-counter abstraction whose monotonicity is *justified by the empirically-measured bounded reaction*, not assumed.

- Termination alone is not the signal: on a finite grid even a non-monotone system halts. The decidability signal is **monotonicity / `pre`-upward-closure**, tested directly and shown to discriminate (negative control).
