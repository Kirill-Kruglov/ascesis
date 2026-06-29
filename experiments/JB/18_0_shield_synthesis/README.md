# Experiment 18.0 — Shield Synthesis from the justitia Boundary

Tests one precondition of the project's special theory, cheaply, before any training:
**can the justitia collapse-boundary be expressed as a decidable safety invariant — i.e.
can a shield be synthesized for it?** No training, no LLM, no language rendering.

## How this connects to the goal

The special theory is: train an LLM inside a safe boundary so the model never learns
collapse-trajectories — safer than internet-trained, even if content inside the boundary is
still generalized rather than derived. That theory is worthless if the boundary cannot be
made into a decidable shield. This experiment tests that one precondition using the justitia
code that already exists. If the boundary synthesizes, we have earned the right to test
whether training inside it actually helps (18.1). If it does not, we have saved ourselves the
entire training program and learned exactly what must be reformulated.

## What it does (Steps 0–4)

- **Step 0** — characterize the *actual* justitia substrate (`outputs_18_0/substrate_characterization.md`).
  The real collapse condition (`substrate.py:683/756`) is
  `mean(zone_welfare) < 0.32 OR #{zones: welfare<0.20} >= 4 OR total_mass < 35`.
  Powers: **scales** = anti-concentration (resource-HHI cap); **sword** = consequence-gated
  containment/escrow.
- **Step 1** — harvest real states; test upward-closure of the unsafe set U under the natural
  badness order (`upward_closure_report.json`).
- **Step 2** — measure the sword's per-step reaction magnitude (the decidability danger point)
  and the abstract monotonicity condition (`monotonicity_report.json`).
- **Step 3** — synthesize the shield by backward-reachability coverability on a monotone
  2-counter abstraction (`backward_reachability_report.json`, `shield_sample.json`).
- **Step 4** — positive control (scales-only) + negative control (injected unbounded reaction)
  (`control_report.json`).

## Result

`shield_synthesizable`. U is upward-closed (100% of 99,580 toward-worse perturbations stay in
U); the sword reaction is bounded (≤0.082 welfare / 0.032 concentration per step, never an
unbounded reset); the abstracted coupling is a monotone WSTS whose backward coverability
terminates and `pre(↑U)` stays upward-closed. The negative control (unbounded reaction) is
caught by the monotonicity / `pre`-upward-closure tests, so the instrument is trustworthy.
**Precondition holds → proceed to 18.1.**

Honest scope: the full substrate is a stochastic ABM, not literally a WSTS; the shield is
synthesized for an abstraction whose monotonicity is *justified by the empirically-measured
bounded reaction*, not assumed. The decidability signal is monotonicity, not mere termination
(a finite grid halts regardless).

## Run

```bash
python scripts/run_shield_synthesis.py --mode full     # 5 worlds × 4 policies × 8 seeds
pytest tests/                                            # unit tests for the shield logic
```

Requires the justitia repo at `/home/master/llm_projects/justitia` (imported read-only).
