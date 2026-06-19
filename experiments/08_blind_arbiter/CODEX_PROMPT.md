# Codex implementation prompt — Experiment 08

You are implementing experiment 08 in the `ascesis` repository under a pre-registered spec.
Read `experiments/08_blind_arbiter/SPEC.md` first; it is the contract. Match the conventions
of experiments 01-06: a single `run.py`, pure Python plus numpy (matplotlib only for plots,
no heavy dependencies), deterministic seeds, one-command run, and the same output layout.

This is the non-spatial, cheapest-first slice: a population game on the simplex, no spatial
grid, no multi-agent RL. Do not pull in Melting Pot or Foundation.

## What to build

A population game with `G` groups (default 2) and three swappable arbiter regimes.

1. State: shares `x_g` on the simplex; each group has a hidden aggressiveness `a_g` and an
   observable signal `s_g` (`s_g(0) = clip(a_g + noise)`).
2. Step loop: the arbiter allocates a unit resource budget `r_g` using only post-`lag`
   observed consequences plus a stochastic audit (random timing and focus); given `r_g`, a
   group captures with intensity rising in `a_g * r_g`, capture transfers share at
   `capture_rate`, shares update replicator-style and renormalize, a group below
   `survival_threshold` goes extinct (absorbing); the signal `s_g` drifts toward whatever
   signal value recently attracted more resource (the emergent Goodhart engine).
3. Arbiter regimes (one interface, never reading `a_g`): `scalar`, `geometric` (geometric mean
   of observed shares), `lexicographic` (permanence-floor first; inside the floor do not
   equalize shares).
4. R axis: `R = horizon_harm / horizon_observation` exactly as defined in the SPEC (note the
   SPEC fixes an orientation inconsistency from the source description). Sweep `R` by varying
   `capture_rate` and `lag`; build the permanence-survival curve.
5. Failure modes (required, surfaced not hidden): camouflage faster than the window (`R<1`);
   collective hack (a coordinated group rewrites the effective payout); collective punishment
   of the innocent (within-group heterogeneity of `a`, so a group-level reaction harms
   low-aggression members). Log and plot all three.

## Hard requirements (project harness)

- The arbiter is blind: its input never includes `a_g`. Add a runtime assertion and a static
  note; this is artifact check `blind_arbiter`.
- Goodhart is emergent: signal-gene decoupling must arise from the dynamics and signal
  mutation, never a hand-coded penalty (`emergent_goodhart`).
- The permanence criterion is a floor, not a maximized objective: inside the floor the arbiter
  does not equalize shares (`floor_not_maximized`).
- Symmetric comparison: all regimes on identical seeds and the same `R` grid, no tie-break
  favoring any regime; log `improvement_iterations` per regime in the manifest.
- Calibration gate: C1 (R<<1 fails for all regimes) and C2 (scalar is hacked: `corr(s,a)`
  falls and permanence degrades) must hold, else the stand is not yet measuring the question --
  report that, do not dress it up.
- Pre-registration is fixed: do not change hypotheses, the R definition, or thresholds to make
  a result come out. Log any functional-form choice or deviation in the manifest, kept
  symmetric across regimes.
- Priority is the validity of the test, not the result. No boundary, or no regime difference,
  is a valid negative -- report it plainly.

## Outputs (match experiments 01-06)

- `results/raw/results.json`, `results/raw/results.csv` -- per regime, per `R`, per seed.
- `results/run_manifest.json` -- seeds, train/held-out split, R grid, regimes,
  `improvement_iterations` per regime, `spec_sha256`, any logged deviation.
- `results/report.md` -- permanence-survival curve vs `R`, located `R*` per regime, and the
  C1/C2/C3 calibration outcomes and H_boundary / H_regime verdicts.
- `results/validation_report.md` -- the artifact checks from the SPEC, each pass/fail with a
  one-line interpretation, and a final verdict.
- Plots: permanence-survival vs `R`; `corr(s,a)` over time; the three failure-mode figures.

## Commit

When the code is reviewed and the calibration gate is understood (passing, or transparently
reported as not-yet), commit the code and result artifacts yourself, so the commit is authored
by you and you appear as an actual contributor. The maintainers commit the markdown (SPEC,
README, this prompt). Use a `Co-Authored-By` trailer for the human if appropriate.

## Report back

State: the train/held-out seed split and R grid; whether the calibration gate (C1, C2) passed;
the located `R*` per regime with the permanence-survival numbers; whether any regime moved
`R*` (H_regime); whether the three failure modes appeared; and anything in the SPEC that was
under-specified or ill-posed (especially the capture/replicator dynamics and the signal
mutation).
