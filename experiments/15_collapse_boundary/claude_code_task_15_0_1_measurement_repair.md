# Claude Code Task — Experiment 15.0.1: Measurement Repair (NOT system strengthening)

## Context for you, Claude Code

This is a diagnostic-repair task, downstream of Experiment 15 (`15_collapse_boundary`).
Experiment 15 ran four rewrite systems (A dead control, B noisy-TV control, C collapsing-rule candidate, D structured candidate) and concluded "live zone not found — inconclusive."

**Before we trust that conclusion, three measurement defects must be fixed.** We are NOT changing the four systems. We are NOT strengthening candidates. We are NOT adding Sanskrit or LLMs. We only repair instruments and re-run on the SAME systems with the SAME seeds, then compare.

This mirrors a discipline we have held throughout: do not change the object under study until you trust the instrument measuring it. The previous result may be correct — but it rests on at least one metric (closure horizon) that is almost certainly broken.

**Do not optimize for any system looking "live." The goal is trustworthy measurement, including trustworthy negative results.**

---

## The three defects (in priority order)

### Defect 1 — Closure horizon collapses to h=2 for A, B, AND C identically

This is the red flag. A dead normalizer (state novelty 0.006), a noisy-TV system (state novelty 0.62), and a collapsing candidate (trajectory novelty 0.9999) cannot genuinely share `h_0.01 = 2`. The marginal-novelty-delta estimator is firing on an early shared plateau and missing the late expansion the report itself notes for B and C.

**Hypothesis to test:** the closure-horizon estimator declares plateau on the FIRST dip below epsilon, rather than confirming a SUSTAINED plateau. A system that dips then re-expands is wrongly frozen at the first dip.

**Required fix:**
- Compute closure horizon SEPARATELY for each novelty channel: state novelty, trajectory novelty, normal-form novelty, AND (new) semantic-class novelty (see Defect 3). Never a single horizon collapsing all channels.
- Require a plateau to be SUSTAINED: marginal novelty must stay below epsilon for K consecutive horizon steps (make K a parameter, default K=3) before declaring plateau. Report the first sustained plateau, not the first dip.
- If novelty re-expands after a dip, report `non_monotonic_plateau` with the horizons where dips and re-expansions occur, rather than a single number.
- Output per-channel horizon curves so we can SEE the shape, not just the threshold crossing.

### Defect 2 — "dead/live" classification mixes state and trajectory axes into one verdict

System C has trajectory novelty 0.9999 (maximal, non-saturating) but was labeled "dead" on the basis of low state novelty. Whether that is "dead" depends entirely on which axis matters — and our own prior work (the proof-DAG cycle) suggested trajectories, not states, carry the reasoning content. We must stop emitting a single dead/live label that silently privileges one axis.

**Required fix:**
- Replace the single `classification` field with a 2D classification: one verdict per axis.
  - `state_axis: {saturating | open | trivial}`
  - `trajectory_axis: {saturating | open | trivial}`
  - `semantic_axis: {saturating | open | trivial}` (new, see Defect 3)
- Keep a combined human-readable summary, but it must NAME which axes are open and which closed, e.g. `"trajectory-open / state-closed / semantic-?"`. Never a bare "dead."
- This directly exposes whether C is "dead everywhere" or "open in trajectories, closed in states" — a distinction the current report cannot make and which is central to whether we are measuring the right thing.

### Defect 3 — Novelty is measured over syntactic shapes only; no semantic-equivalence channel

Both A (dead) and the report's own analysis suggest that what matters for eventual LLM usefulness is whether NEW MEANING appears, not new syntax. noisy-TV (B) proves syntactic novelty is cheap and worthless. We have no metric for semantic novelty, so we currently cannot tell "new structure" from "new surface."

**Required fix (minimal, no new systems):**
- For each system, define a cheap semantic-equivalence relation over terms/trajectories using ONLY information the rewrite system already exposes — do NOT invent semantics. Acceptable cheap proxies, in order of preference:
  1. Normal form (where it exists): two terms are semantically equivalent if they share a normal form. (Captures: dead systems have few semantic classes despite syntactic variety.)
  2. For non-terminating systems (B, C): a bounded-depth Böhm-tree-like prefix / observation up to fixed depth d, comparing the OBSERVABLE behavior prefix rather than full term. Two trajectories are equivalent if their depth-d observation prefixes coincide.
  3. For C/D specifically: the structured labels the systems already carry (operation type, dependency relation, proof-step type, source-target) — quotient trajectories by their label sequence.
- Compute `semantic_class_novelty = unique semantic classes / generated objects` as a first-class channel alongside state/trajectory novelty, at every horizon.
- This is the single most important new measurement. The whole project's question — content vs. noise — is exactly the gap between syntactic novelty and semantic-class novelty. If semantic-class novelty plateaus while syntactic novelty grows, that IS noisy-TV, made measurable.

---

## What to run and report

- Re-run the EXACT four systems from Experiment 15, same seeds (42), same horizons (1,2,4,8,16,32,64; optional 128), same sample counts. No system changes.
- Produce a side-by-side comparison: OLD metrics (from Experiment 15 outputs, if present in the repo; otherwise note absent) vs NEW metrics.
- For each system output the three-axis classification and the per-channel horizon curves.

### Required new/updated outputs
```
outputs_15_0_1/per_channel_novelty_curves.csv      # state, trajectory, normal_form, semantic — every horizon
outputs_15_0_1/per_channel_closure_horizon.json     # separate horizon per channel, with sustained-plateau logic + non_monotonic flags
outputs_15_0_1/three_axis_classification.json        # state/trajectory/semantic verdict per system
outputs_15_0_1/semantic_vs_syntactic_gap.csv         # the noisy-TV-made-measurable table
outputs_15_0_1/comparison_old_vs_new.md              # what changed and why, per system
outputs_15_0_1/per_channel_novelty_vs_horizon.png    # one plot, all channels, faceted by system
```

### The single interpretive question this experiment must answer
```
For each system, on WHICH axes (state / trajectory / semantic) does novelty
remain open vs saturate — and specifically, does semantic-class novelty
saturate while syntactic novelty keeps growing (= noisy-TV) or do they
grow together (= candidate live structure)?
```

---

## Hard constraints (do not violate)

- Do NOT modify the four rewrite systems' rules. (That is Experiment 15.1, deliberately deferred.)
- Do NOT add Sanskrit, language rendering, or any LLM/training.
- Do NOT introduce a semantic notion the rewrite system doesn't already expose — only quotient by normal form, bounded observation prefix, or existing structured labels.
- Do NOT tune thresholds to make any system look live. Report whatever the repaired instruments show, including "still dead on all axes."
- Keep everything deterministic and seeded. Add tests for the sustained-plateau logic (a hand-built novelty curve that dips then re-expands MUST yield `non_monotonic_plateau`, not an early single horizon).

---

## Kill / honesty conditions to emit explicitly

- If, after repair, all systems still saturate on the SEMANTIC axis at similar low horizons → strong evidence the toy rewrite approach is genuinely dead (not a measurement artifact), and the Experiment 15 conclusion stands and is now trustworthy. Say so plainly.
- If C (or any system) turns out trajectory-open AND semantic-open while state-closed → the original single-label "dead" was a measurement artifact; this is a real candidate and Experiment 15's negative conclusion must be revised. Say so plainly.
- If the semantic-equivalence proxy itself collapses everything to one class (i.e. the proxy is too coarse) → report `semantic_proxy_degenerate` and do not draw conclusions from that channel; recommend a better proxy rather than faking a result.

---

## Why this matters (one line, keep it in the README)

We are not trying to make a rewrite system look alive. We are checking whether our instrument can tell the difference between new meaning and new noise — because that distinction, not Sanskrit and not scale, is the whole question behind "is there an inexhaustible, non-collapsing substrate for training LLMs."
```