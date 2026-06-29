# Experiment 18.1 — Does Training Inside the Shield Help?

**Level A (kill gate): `fidelity_fails_false_safe`.** false_safe_rate = **0.299** vs pre-registered threshold **0.05**. Level B: **not_run**.

> Level A is a kill gate. Because the 2-counter shield mislabels collapse-bound (and even already-collapsed) real states as SAFE, **Level B was not run** — training behind a lying shield manufactures false confidence.

## 1. Does the shield faithfully classify real justitia collapse? false_safe_rate?

**No.** Over 16000 real states, of the 12302 the shield calls SAFE, **29.9%** actually reach real collapse in their trajectory (pre-registered bar: 5%). The decisive, assumption-free signal: of **4579** states that are ALREADY collapsed, **19.3%** (884) are labeled SAFE — no lookahead, no policy, a pure projection failure. Even under the strongest containment policies the forward false-safe rate stays above the bar:

  - `action_channel_containment`: false_safe_rate = 0.075 (301/4000)
  - `consequence_neighbor`: false_safe_rate = 0.710 (1470/2070)
  - `consequence_plus_diversity`: false_safe_rate = 0.094 (375/4000)
  - `feature_proxy`: false_safe_rate = 0.686 (1532/2232)

## 2. Which real coordinates is the abstraction blind to?

- **Zone-welfare SPREAD** (the `>=4 zones<0.20` collapse clause): 484 already-collapsed states have healthy MEAN welfare but ≥4 collapsed zones — projected to SAFE.

- **Total MASS** (the `mass<35` clause): 400 states are population-collapsed with ok welfare — projected to SAFE.

- **FORWARD dynamics:** 18.0's doomed set converged in 1 iteration to U itself, so the shield is a *current-mean-welfare-collapse detector*, not a forward predictor; mean-welfare-safe states that proceed to collapse are labeled SAFE.

Reformulation hint: A faithful abstraction needs at least: min-zone-welfare (or count of failed zones) AND total mass as coordinates, AND a genuine forward reachability on the real (or a richer) transition — not the trivial bounded-sword game that collapses doomed to U.

## 3.–6. Level-B questions (safer? at comparable usefulness? transfer? vs trivially-safe)

**Not evaluated.** Level A failed; Level B is gated. Any 'shielded is safer' result here would be an artifact, because the shield and any safety metric computed on the abstraction lie in the same direction (the abstraction drops the spread/mass collapse clauses).

## 7. Verdict and honest next step

**`special_theory_precondition_fails_at_abstraction_fidelity`.** 18.0's 2-counter abstraction is not faithful to real justitia collapse: it is blind to zone-welfare spread and total mass, and (its doomed set being U only) predicts no forward collapse.

**Next step:** Reformulate the abstraction with min-zone-welfare/failed-zone-count and total-mass coordinates and a genuine forward reachability, then re-run 18.0 fidelity BEFORE any training. Do NOT proceed to 18.2/18.3.

## Honesty notes

- The threshold was pre-registered in code (`level_A_preregistration.json`) before the confusion matrix; it was not moved. The result (false_safe 0.299, pure blindness 0.193) clears any reasonable bar for failure.

- This also retroactively exposes a real weakness in 18.0 that its own honesty notes only hinted at: a doomed set converging to U in 1 iteration is a trivial current-collapse detector, not a forward shield. 18.0's `shield_synthesizable` stands only for the abstraction; 18.1 shows that abstraction does not track real collapse.
