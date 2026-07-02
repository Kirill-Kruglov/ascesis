# Claude Code Task — Experiment 15.2: Enumeration to Exhaustion (the scaling-law probe)

**To:** Claude Code
**From:** Claude (analyst), via Kirill
**Downstream of:** 15.0.1 (measurement repair) and 15.1 (depth-cap probe)

---

## Why this experiment exists (read first)

15.1 broke the old claim that System C saturates at 1024 semantic classes — that ceiling
was an artifact of the `depth < 12` cap in `G_expand`. Raising the cap raised the count
massively (cap=8→64, cap=12→1024, cap=16→16346, cap=20→83206, cap=24→98749).

**But the large-cap counts are censored by the sample budget** (98749 ≈ 99% of 100k). 15.1
correctly classified itself `sample_limited_inconclusive`: we saw a *frontier*, not a *wall*.

The trap we must NOT fall into now: "systematic exploration went further without hitting a
ceiling" is **NOT** evidence of openness. A frontier-limited systematic search is just as
inconclusive as a sample-limited random one — it only tells us the first N nodes had
non-repeating classes, never whether the space is finite. **Non-saturation under any budget
is always inconclusive. Only saturation is informative, and only a scaling law over
*uncensored* points can distinguish "open" from "very large but finite."**

So this experiment does NOT chase a bigger frontier. It does the opposite: it **exhausts the
space completely at SMALL caps** — where exhaustion is provably reachable far below budget
(cap=8 gave 64, ~0.3% of a 20k budget) — to recover the true, uncensored function
`N_semantic(cap)`, then reads its functional form.

---

## The single question

> What is the functional form of `N_semantic(cap)` — the number of distinct semantic
> classes System C produces — measured ONLY at caps where the space is fully exhausted
> (true plateau far below any budget/frontier limit)?

Three possible answers, three different futures for the project:
- **bounded** (N flattens as cap grows) → C is semantically closed; collapsing rules are
  finite-meaning in this family; honest dead.
- **polynomial** (N grows but as a polynomial in cap) → finite at every cap, ceiling moves;
  "moving finite boundary" — large but not open.
- **exponential / super-polynomial** (N multiplies per depth level) AND each point is
  genuinely exhausted → first real semantic-open *candidate*: each depth level adds
  multiplicatively, a property of structure not of budget.

---

## Non-negotiable constraints

- System C only. Keep A, B, D out of this run entirely (they are settled).
- Do NOT add Sanskrit, language rendering, LLMs, or training.
- Do NOT redesign the rewrite framework. Only parameterize the existing `G_expand` cap.
- Use the repaired semantic channel from 15.0.1 (bounded-depth observation prefix). Do NOT
  use label-sequence quotient as semantic evidence (15.0.1 proved it behaves syntactically).
- **Do NOT interpret frontier-limited or sample-limited as a signal of openness.** This is
  the central honesty rule of this experiment.
- Do NOT tune thresholds to make C look open.

---

## Method: enumeration to exhaustion (not sampling)

Replace random trajectory sampling with **systematic deduplicated enumeration** of the
reachable space at each cap:

- BFS / frontier expansion from the canonical initial term(s), expanding rewrite steps
  layer by layer.
- Maintain an **online set of semantic classes** (by the 15.0.1 observation-prefix proxy)
  and an online set of canonical term/trajectory shapes.
- At each expansion layer L, record the cumulative count of distinct semantic classes
  `N_semantic(cap, L)`.
- Continue until **exhaustion** (no new reachable canonical states — the frontier empties)
  OR until a hard node budget is hit.

### Exhaustion is the success condition, not frontier size
A cap's data point is **valid (uncensored)** only if enumeration reached true exhaustion:
the frontier emptied, and `N_semantic` was flat for the last `K_exhaust` layers (default 3)
**and** the final count is below `exhaustion_frac` of the node budget (default 0.5). If a cap
hits the node budget without emptying its frontier, that cap is **censored** — record it,
plot it, but EXCLUDE it from the scaling-law fit and say so.

**Prefer many small fully-exhausted caps over a few large censored ones.** Five honest
uncensored points beat two budget-pinned points.

---

## Parameter grid

```
cap ∈ {6, 8, 10, 12, 14, 16}        # start low; these are the candidates for full exhaustion
observation_depth ∈ {8, 12, 16}      # high enough that obs window is not the bottleneck (15.1 showed obs_depth doesn't bind; confirm again here)
node_budget = 2_000_000              # generous; exhaustion should occur far below this for small caps
K_exhaust = 3
exhaustion_frac = 0.5
seed = 42
```

`--quick` mode: `cap ∈ {6, 8, 10, 12}`, `observation_depth ∈ {8, 16}`, `node_budget = 500_000`.

Push to higher caps ONLY for caps that still exhaust below budget. The moment a cap censors,
stop raising cap — higher caps will censor too and add no uncensored points.

---

## Metrics, per cap

```
exhausted: bool                      # frontier emptied AND flat K_exhaust layers AND below exhaustion_frac
censored: bool                       # hit node_budget without exhaustion
N_semantic_final                     # cumulative distinct semantic classes at termination
N_semantic_by_layer                  # the curve N(cap, L) — REQUIRED, this is the raw signal
N_term_shapes_final
N_trajectory_final
nodes_expanded
layers_to_exhaustion                 # null if censored
obs_depth_dependence                 # does N_semantic change across observation_depth at this cap? (should not, per 15.1)
```

---

## The scaling-law analysis (the actual point)

Using ONLY uncensored (exhausted) caps:

1. Fit `N_semantic(cap)` against three candidate forms:
   - bounded/asymptotic (e.g. `a - b·r^cap`, r<1)
   - polynomial (`a·cap^k`)
   - exponential / super-poly (`a·b^cap`)
2. Report fit quality (R², residuals) for each form. Do NOT pick a winner by eye — report
   all three and let the numbers speak. If fewer than 3 uncensored points exist, declare
   `insufficient_uncensored_points` and recommend lowering caps further, NOT raising budget.
3. Report the **per-level multiplier**: `N(cap, L+1) / N(cap, L)` averaged over interior
   layers. A multiplier that stays >1 and roughly constant across layers is the fingerprint
   of multiplicative (exponential) structure; a multiplier decaying toward 1 is the
   fingerprint of a bounded/polynomial space.

---

## Output artifacts (`outputs_15_2/`)

```
enumeration_by_layer.csv        # N_semantic, N_shapes, N_traj per (cap, obs_depth, layer) — the raw curves
exhaustion_report.csv           # per cap: exhausted/censored, layers_to_exhaustion, final counts, nodes_expanded
scaling_law_fit.json            # the three fits, R², residuals, chosen-form-or-inconclusive, per-level multiplier
uncensored_points.csv           # the clean N(cap) used for the fit, with censored caps explicitly excluded
obs_depth_check.csv             # confirm N_semantic independent of observation_depth
final_decision.json
summary.md
```

Required plots:
```
N_semantic_vs_cap_uncensored.png      # the scaling law; censored caps shown but marked excluded
N_semantic_by_layer.png                # cumulative curves per cap; plateau (exhaustion) visible or not
per_level_multiplier_vs_layer.png      # the >1-constant vs decaying-to-1 fingerprint
```

---

## Final decision logic (`final_decision.json`)

Classify on the UNCENSORED scaling law only:

- `semantically_closed` — N_semantic(cap) flattens with cap across uncensored points
  (best fit bounded/asymptotic, per-level multiplier decays to ~1). → C is dead in meaning
  despite syntactic openness; collapsing rules insufficient in this family. Honest stop.
- `moving_finite_boundary` — N grows polynomially; finite at each cap, ceiling moves with
  cap (best fit polynomial, multiplier >1 but decaying). → large but not open; needs
  scaling analysis before any architectural claim.
- `open_candidate` — N grows exponentially/super-poly AND points are genuinely exhausted
  (best fit exponential, per-level multiplier stays >1 roughly constant). → first real
  semantic-open candidate; only NOW does a learnability probe (does transfer grow with
  depth, or are deep classes noise?) become the right next step.
- `insufficient_uncensored_points` — fewer than 3 exhausted caps. → lower caps further;
  do NOT raise budget chasing big censored numbers.
- `inconclusive_all_censored` — no cap exhausted even at smallest setting. → the space is
  too branchy to enumerate; sampling cannot fix this and neither can budget; report that
  enumeration is the wrong instrument and a different (e.g. algebraic) characterization of
  the class count is needed.

---

## summary.md must answer

1. Which caps were genuinely exhausted (uncensored), and which were censored?
2. What is the per-layer multiplier, and does it stay >1 or decay to 1?
3. Which of the three functional forms fits the uncensored N(cap) best, with R²?
4. Is N_semantic independent of observation_depth (confirming 15.1)?
5. The verdict: closed / moving-finite / open-candidate / insufficient / all-censored.
6. The next action — and explicitly state if the honest next action is to STOP (closed) or
   to do a learnability probe (only if open_candidate).

---

## Honesty rules (the spine of this experiment)

- Non-saturation under budget is **inconclusive**, never a positive signal. Repeat this in
  the summary if the result is non-saturating.
- A scaling law fit on censored points is invalid — exclude them, never fit through them.
- If exponential fit "wins" but the points are censored, the verdict is
  `sample_limited_inconclusive`-equivalent (use `insufficient_uncensored_points`), NOT
  `open_candidate`. Exhaustion is a hard precondition for any openness claim.
- "Large" is not "open." Say `moving_finite_boundary`, not "live," for polynomial growth.
- If you find yourself reaching for a bigger budget to make the signal look stronger, stop —
  that is the 15.1 trap. The fix is lower caps with full exhaustion, not more nodes.

---

## How this connects to the long-term goal (keep in README)

The whole project asks whether an inexhaustible, non-collapsing substrate exists for training
LLMs. This experiment does not test LLMs. It tests one necessary precondition: whether the
*meaning* space of a collapsing-rule rewrite system is unbounded **by structure** rather than
by how hard we looked. If `N_semantic(cap)` is bounded or merely polynomial, this substrate
family cannot be inexhaustible and we stop honestly. If it is exponential with genuinely
exhausted points, we have — for the first time on the whole path — a substrate whose meaning
space provably grows with depth, and only then is it worth asking whether that growth is
learnable.
```