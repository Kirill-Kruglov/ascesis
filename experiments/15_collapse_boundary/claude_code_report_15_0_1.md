# Report — Experiment 15.0.1: Measurement Repair (result)

**To:** Claude (analyst), re `claude_code_task_15_0_1_measurement_repair.md`
**From:** Claude Code
**Run:** seed 42, samples 20000, horizons 1,2,4,8,16,32,64,128, obs_depth 4 (the exact
Experiment-15 canonical configuration). Four systems **unchanged**. No Sanskrit, no LLM.

## TL;DR

The repaired instruments do **not** rescue a live zone. On the new semantic axis, the
count of distinct semantic classes saturates to a **finite set for every system**
(A=8, B=9, C=1024, D=2). **No system is semantic-open.** This is your first honesty
condition: Experiment 15's negative/inconclusive conclusion **stands and is now
trustworthy** — it was not a closure-horizon artifact.

What the repair *does* expose, hidden by the old single "dead" label: the collapsing
candidate **C carries by far the richest bounded semantic set (1024 classes)** vs the
noisy-TV control B (9) and the structured candidate D (2). C's ceiling is set by its
`depth<12` cap on `G_expand` — a concrete rule bound, not a measurement defect — which is
the precise target for Experiment 15.1.

## Trust anchor: faithful reproduction

The rerun reproduces Experiment 15's syntactic numbers **bit-for-bit** — the new
`state_novelty`, `trajectory_novelty`, `normal_form_novelty` match the old
`outputs/novelty_curves.csv` to <1e-12 on all 32 rows. So the four systems, seeds and
sampling are provably untouched; the semantic channel is added *on top of identical data*.

## The three defects, fixed

### Defect 1 — per-channel sustained-plateau closure horizon
The old estimator collapsed all channels into one horizon and fired on the **first dip**,
declaring `h_0.01 = 2` for A, B *and* C alike. Replaced with a per-channel estimator that
declares a plateau only when the marginal novelty stays below ε for **K=3 consecutive**
steps, and flags `non_monotonic_plateau` (with dip/re-expansion horizons) when novelty
dips then re-expands.

| system | OLD h_0.01 (all channels) | NEW sustained-plateau horizon (state / traj / NF / semantic) | non-monotonic channels |
|---|---|---|---|
| A | 2 | 2 / 32 / 2 / 2 | trajectory, semantic_label |
| B | 2 | 2 / none / none / 2 | state, trajectory, semantic_label |
| C | 2 | none / 32 / none / none | state, trajectory, semantic, semantic_label |
| D | 2 | 2 / 8 / 4 / 2 | trajectory |

`none` here means the marginal **rate** never reached a K=3 plateau — **not** a verdict of
openness. A non-monotonic rate can still have a saturated **count** (exactly C-semantic;
see Defect 3). The point of this table is only that A/B/C are no longer all frozen at h=2.

### Defect 2 — single label → three-axis classification

| system | OLD label | state_axis | trajectory_axis | semantic_axis |
|---|---|---|---|---|
| A | dead | trivial | saturating | **trivial** |
| B | fake_live | open | saturating | **trivial** |
| C | dead | saturating | open *(sample-limited)* | **saturating** |
| D | dead | trivial | trivial | **trivial** |

**Important methodology note.** My first cut classified the axes by novelty **rate** and
mislabeled C-semantic as "open" (its rate is 0.0512). That was precisely the threshold
artifact you warned against: 0.0512 = 1024 classes / 20000 samples — a *finite, saturated*
set, not open growth. I rewrote the classifier to judge openness on the **unique-object
COUNT vs horizon** (with a sample-cap guard), which is the only signal that distinguishes a
bounded set from unbounded growth. C-semantic is `saturating` (1024, reached by h=64); C's
trajectory "openness" is flagged `sample_limited` because the distinct-trajectory count
simply fills the entire 20000 budget — uninformative about true openness, and syntactic
only.

### Defect 3 — new semantic-class channel (noisy-TV made measurable)

Semantic equivalence uses only what the systems already expose: normal form (terminating)
or a bounded depth-4 observation prefix (non-terminating). The decisive quantity is the
**count** of distinct semantic classes, not the rate.

Final-horizon (h=128) numbers:

| system | trajectory count (syntactic) | semantic class count | semantic saturates at | syntactic−semantic gap (rate) |
|---|---|---|---|---|
| A | 2,201 | **8** | h=16 | 0.110 |
| B | 13,953 | **9** | h=4 | 0.697 |
| C | 19,999 (= sample cap) | **1024** | h=64 | 0.949 |
| D | 364 | **2** | h=8 | 0.018 |

Read the gap: **B** has ~14k distinct trajectories but only **9** semantic classes — the
textbook noisy-TV signature, now a number. **C** reaches maximal trajectory novelty (1.0)
but only **1024** semantic classes — a huge gap (0.95): also noisy-TV-shaped, just with a
larger bounded ceiling than B.

Secondary proxy (defect-3 option 3, label-sequence quotient): for B and C the label count
**equals** the trajectory count (13953, 19999) — i.e. the label quotient behaves like
syntactic novelty and is **not** discriminative as semantics here. This confirms the
normal-form / observation proxy (option 1/2) was the right primary choice; the label proxy
is reported but should not be trusted as a meaning signal.

## The single interpretive question, answered

> On which axes does novelty stay open vs saturate, and does semantic-class novelty
> saturate while syntactic keeps growing?

- **A (dead control):** closed on all axes (semantic 8). Control behaves as designed — the
  theory↔practice link (§5.1 of the memo) holds for the control.
- **B (noisy-TV control):** state-open (1.6M term shapes), trajectory saturating (~14k),
  **semantic frozen at 9**. Syntactic novelty grows, semantic does not — *this is the
  noisy-TV gap made measurable*, exactly as predicted.
- **C (collapsing candidate):** state-saturating (~80k), trajectory-open-but-sample-limited,
  **semantic saturating at 1024**. Richest semantic set of the four, but bounded.
- **D (structured candidate):** essentially dead everywhere (semantic 2) — more collapsed
  than A.

## Kill / honesty conditions (explicit)

- **Triggered — condition 1:** all systems saturate on the semantic axis at finite, low-ish
  horizons (A h16, B h4, C h64, D h8). → toy rewrite approach is genuinely
  semantically closed; **Experiment 15's conclusion stands and is now trustworthy.**
- **NOT triggered — condition 2:** no system is trajectory-open *and* semantic-open with a
  real (non-sample-limited) signal. C looked like a candidate under the rate metric but is
  semantic-saturating under the count metric. The old single "dead" label was *imprecise*
  (it hid C's 1024 vs D's 2), but the corrected reading is **not** "C is live."
- **NOT triggered — condition 3:** the semantic proxy is not degenerate — it produces 8 / 9
  / 1024 / 2 classes, comfortably distinguishing systems (B's 9 vs C's 1024 is the whole
  point), so the channel is informative, not collapsed-to-one.

## What this means for the project (and what it does NOT)

We can now say, with a trustworthy instrument, that **within this toy setting there is no
inexhaustible semantic substrate** — every system's *meaning* space is finite, even when its
*surface* space is not. That is the honest current answer to memo §3.Q2 ("content vs
noisy-TV") for these four systems: **content not found; noise correctly identified.**

This is a clean negative on the *current systems*, not on the *hypothesis*. The one place
the boundary is non-trivial is C: its semantic ceiling (1024) is a direct consequence of the
`depth<12` cap in `G_expand`. The natural — and now well-motivated — next probe is
**Experiment 15.1**: lift that cap (and/or vary the collapsing structure) and re-measure
*with these same repaired instruments* whether the semantic class **count** keeps growing
with depth or hits a new ceiling. If it keeps growing unboundedly with horizon (not with
sample count), that is the first genuine semantic-open signal. Until then, no Sanskrit, no
LLM — the instrument now earns the right to that next system change.

## Deliverables (`outputs_15_0_1/`)

```
per_channel_novelty_curves.csv      state/trajectory/normal_form/semantic(+label), every horizon, with counts
per_channel_closure_horizon.json    per-channel sustained-plateau logic, deltas, dips/re-expansions
three_axis_classification.json      per-axis verdict + evidence (saturation count/horizon, sample_limited)
semantic_vs_syntactic_gap.csv       the noisy-TV table
comparison_old_vs_new.md            per-system old→new, with the explicit kill-condition conclusion
per_channel_novelty_vs_horizon.png  4 facets; red (semantic) flat under orange (trajectory) for B and C
```

Tests: 17/17 pass, including the required hand-built dip-then-re-expand curve →
`non_monotonic_plateau` (not an early single horizon). Everything deterministic and seeded.
Reproduce with:

```bash
python scripts/run_measurement_repair.py --seed 42 --samples 20000 --max-horizon 128
```

## One caveat I want you to catch me on

The open/saturating thresholds (`growth_eps=0.05`, `tau_low_rate=0.05`, `sample_limit_frac=0.9`)
are judgment calls. They do **not** affect the headline — C-semantic at 1024 « 20000 is
unambiguously bounded for any reasonable ε, and B at 9 is not borderline. But the *labels*
"saturating vs trivial" on mid-rate channels (e.g. A-trajectory at 0.11) are threshold-
sensitive cosmetics; trust the raw count curves in the CSV over the label words if they ever
disagree.
