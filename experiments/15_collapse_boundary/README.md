# Collapse Boundary

Minimal rewrite-system experiment for testing whether a rewrite substrate can produce novel and learnable structure without collapsing into finite normal forms or noisy-TV surface novelty.

This is not a Sanskrit experiment and not an LLM experiment. It uses small term rewriting systems and lightweight sklearn learners only.

## Install

```bash
pip install -e .
```

## Tests

```bash
pytest
```

## Run

```bash
python scripts/run_collapse_boundary.py --seed 42 --max-horizon 64 --samples 5000
```

Larger optional run:

```bash
python scripts/run_collapse_boundary.py --seed 42 --max-horizon 128 --samples 20000
```

## Systems

- `A_dead_control`: finite arithmetic normalizer. Expected to collapse.
- `B_fake_live_control`: noisy syntactic expansion. Expected to look novel but not semantically learnable.
- `C_collapsing_live_candidate`: weak non-confluent system with collapsing rules.
- `D_structured_live_candidate`: proof-like system with collapsing choices and structured labels.

## Metrics

- State novelty: unique canonical terms divided by generated terms.
- Normal-form novelty: unique normal forms divided by terminating trajectories, or `normal_form_absent`.
- Trajectory novelty: unique canonical trajectories divided by generated trajectories.
- Shape entropy: entropy over canonical term/trajectory shapes.
- Closure horizon: first horizon where marginal novelty drops below `0.01` or `0.001`.
- Learnability: lightweight OOD accuracy over next-rule, reachability, normal-form class, and trajectory-property tasks.
- Noisy-TV score: high novelty plus low compression gain plus flat OOD learnability.
- Compression ratio: gzip compressed size divided by raw serialized term size.

## Outputs

Required tables and JSON:

```text
outputs/system_summary.json
outputs/horizon_metrics.csv
outputs/novelty_curves.csv
outputs/learnability_curves.csv
outputs/noisy_tv_report.json
outputs/compression_report.csv
outputs/closure_horizon_report.json
outputs/trajectory_shape_counts.csv
outputs/term_shape_counts.csv
outputs/final_decision.json
```

Required plots:

```text
outputs/novelty_vs_horizon.png
outputs/learnability_vs_horizon.png
outputs/novelty_learnability_phase_plot.png
outputs/compression_vs_horizon.png
outputs/closure_horizon_comparison.png
```

## Interpretation

The experiment should explicitly distinguish dead, fake-live, live-but-not-learnable, and live-and-learnable behavior. A system is promising only when novelty remains nontrivial, OOD learnability beats majority and memorization baselines, and fake-live diagnostics do not explain the signal.

This connects to the long-term LLM substrate goal only as a substrate falsification test: if rewrite trajectories cannot produce novel and learnable structure here, adding Sanskrit rendering or LLM training would be premature.

## Experiment 15.0.1 — measurement repair

`scripts/run_measurement_repair.py` re-runs the EXACT four systems (same seed, same
horizons, same sampling) with repaired novelty instruments. It does **not** change any
rewrite rule, add Sanskrit, or train an LLM. Three defects fixed:

1. **Per-channel sustained-plateau closure horizon.** The old estimator collapsed all
   channels into one horizon and froze on the first dip, declaring `h=2` for A, B and C
   alike. The new estimator computes a closure horizon per channel (state / trajectory /
   normal_form / semantic) and only declares a plateau when the marginal novelty stays
   below epsilon for `K` consecutive steps (default `K=3`), flagging `non_monotonic_plateau`
   when novelty dips then re-expands.
2. **Three-axis classification** (`state_axis`, `trajectory_axis`, `semantic_axis`), each
   `open | saturating | trivial | degenerate` — never a bare "dead".
3. **Semantic-class novelty channel.** Two trajectories are semantically equivalent if they
   share a normal form (terminating) or a bounded-depth observation prefix (non-terminating).
   No invented semantics — only what the system already exposes. A label-sequence quotient is
   reported as a secondary proxy.

```bash
python scripts/run_measurement_repair.py --seed 42 --samples 20000 --max-horizon 128
```

Why this matters: we are not trying to make a rewrite system look alive. We are checking
whether the instrument can tell new meaning from new noise — the whole question behind
"is there an inexhaustible, non-collapsing substrate for training LLMs."

Outputs in `outputs_15_0_1/`:

```text
per_channel_novelty_curves.csv
per_channel_closure_horizon.json
three_axis_classification.json
semantic_vs_syntactic_gap.csv
comparison_old_vs_new.md
per_channel_novelty_vs_horizon.png
```

## Experiment 15.2 — enumeration to exhaustion (System C only)

`scripts/run_enumeration_exhaustion.py` recovers the true, uncensored
`N_semantic(cap)` for System C and reads its functional form. System C only; only the
existing `G_expand` depth cap is parameterized (`build_collapsing_system(cap)`); no
sampling, no Sanskrit, no LLM.

Two instruments:

1. **Prescribed full reachable-state BFS** — demonstrates it **censors at cap≥6**:
   System C's reachable *state* space is doubly-exponential in the cap (a blow-up of
   syntactic intermediate `F`-trees), so it hits the node budget while the semantic space
   is tiny. Under the literal instrument the verdict is `inconclusive_all_censored`; raising
   the budget cannot help (the 15.1 trap).
2. **Exact semantic-space enumeration** — the correct instrument. Because the collapsing
   redexes discard context (`NF(F(p,q)) = NF(p) ∪ NF(q)`), the reachable normal-form set is
   enumerable exactly and cheaply without materializing the `F`-intermediates. Fully
   exhausted, no budget: `N_semantic(cap) = 2^(cap-2)`.

The scaling law over the uncensored points is a clean **exponential** (R²≈1, per-cap
multiplier ≈2), so by the task's criterion C is an `open_candidate`. **Caveat:** C's normal
forms are exactly the free binary words `{a,b}^(cap-2)` — the combinatorially trivial
exponential, the normal-form-level analogue of noisy-TV. "Open" means the class *count* is
unbounded by structure, not that the meanings are non-trivial; that is what the mandated
next step (a learnability probe) must decide.

```bash
python scripts/run_enumeration_exhaustion.py --mode full
```

Outputs in `outputs_15_2/`: `enumeration_by_layer.csv`, `exhaustion_report.csv`,
`scaling_law_fit.json`, `uncensored_points.csv`, `obs_depth_check.csv`, `final_decision.json`,
`summary.md`, and three plots (`N_semantic_vs_cap_uncensored.png`, `N_semantic_by_layer.png`,
`per_level_multiplier_vs_layer.png`).
