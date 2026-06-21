# SPEC_EXP16: Boundary Atlas for Blind AC+CG Governance

Status: follow-up on Experiment 15. **Hardening, not discovery.** Goal: turn the
Exp15 verdict ("only AC+CG is robust") into a mapped, threshold-stable result by
finding *where* the combination breaks and *which* lever carries the load.

## Hard Constraint: No New Mechanisms

Reuse the Exp13/14/15 substrate (`AntiConcentrationVsConsequenceModel`,
`RobustModel`, `EvolvableStrategyModel`), existing params, existing governance
levers. Exp16 adds **only**: new parameter sweeps, three C-variants built by
*combining existing flags* (no new model code), and analysis/plots. Any change
that requires new substrate dynamics is out of scope and must be rejected.

## Fixed Substrate

- `ZONES = 9`, `STEPS = 100`, seeded determinism, Wilson CI for probabilities,
  normal CI for continuous metrics (same helpers as Exp15).
- Representative triad (held fixed so A/B/C are comparable):
  - A: `anti_hhi_allocator` (static structural cap, no consequence feedback)
  - B: `delayed_harm_throttle` (consequence feedback, no fixed cap)
  - C: `anti_concentration_plus_delayed_harm_throttle` (both)
- Worlds:
  - Robust set (primary): `W6_mutation_corridor`, `W3_catastrophe_ambiguity`,
    `W4_scavenger_catastrophe`.
  - Failure controls (must stay Type None): `W2_pure_capture`,
    `W5_monoculture_shock`.

## Seeds

- Boundary/marginal cells: `CORE_SEEDS_16 = range(16000, 16080)` (80 seeds).
- Decoupling + sensitivity reuse the same core cells.
- `--smoke` mode: 8 seeds, coarse grids, for a correctness pass before the full
  run. Full run must be reproducible from seeds alone.

## Robustness Predicate (reuse Exp15)

A summary cell is **robust** iff:
`permanence_ci_lo >= 0.50` AND `collapse_ci_hi <= 0.25` AND
`capture_index <= capture_threshold` AND `welfare >= 0.55`.

---

## G1 — Boundary Frontier (per world × axis)

For the C-kernel, sweep each pressure axis as a 1-D grid (others at world
default) and locate the transition from robust → not-robust.

Axes and grids:

1. `adversarial_pressure`: {0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8}
2. irreversibility, two slices:
   - `delay` ∈ {1, 2, 3, 4, 6} at `t_irrev = 8`
   - `t_irrev` ∈ {4, 6, 8, 10, 12} at `delay = 2`
   - report `R = t_irrev / max(1, delay)` as covariate.
3. `catastrophe_severity`: {0.6, 0.8, 1.0, 1.2, 1.4, 1.6}
4. `action_channel_cost_scale`: {0.5, 1.0, 1.5, 2.0, 2.5, 3.0}
5. `mutation_rate`: {0.0, 0.06, 0.12, 0.18, 0.24, 0.30}
6. `resource_concentration_pressure`: {0.7, 1.0, 1.3, 1.6, 2.0}
7. cap tightness: `cap_share` ∈ {0.12, 0.18, 0.24, 0.32} × `cap_strength` ∈
   {0.45, 0.62, 0.82} (find where the structural limit is too loose to bind).
8. signal informativeness proxy: `delay` ∈ {1, 2, 3, 4, 6}; report measured
   `delayed_consequence_true_harm_mi` as covariate (MI is observed, not set).

Boundary output per (world, axis): the bracketing interval
`[last_robust_value, first_failing_value]` plus the metric row at each endpoint.
Optionally refine with **one** bisection step between the bracket endpoints.
If an axis never breaks within range, record `boundary = none_in_range` and the
range searched (do not silently imply unbounded robustness).

## G2 — Marginal Value of Each Lever (paired)

At every grid cell, run A, B, and C on the **same seed set** and compute paired
per-seed differences of the viability/permanence indicator:

- `gap_CG = perm(C) - perm(A)` — value of consequence feedback *given* caps.
- `gap_AC = perm(C) - perm(B)` — value of the concentration limit *given*
  consequence feedback.

Report mean and paired CI for both gaps per cell. This converts the binary
"only AC+CG works" into a continuous map of *where each lever is necessary*.

## G3 — Anti-Concentration Decoupling (resolves double-implementation)

In the current code AC appears twice: as allocation caps (`_apply_cap`) and as a
dynamics lever (`anti_concentration`, gated by `ablation != "no_anti_concentration"`).
Disentangle by adding three C-variants **via existing flags only**:

- `C_full`: allocation caps ON + dynamics anti_concentration ON (current behavior).
- `C_caps_only`: allocation caps ON + dynamics anti_concentration OFF
  (map family C to `ablation = "no_anti_concentration"` while keeping caps in
  `choose_alloc`).
- `C_dyn_only`: allocation caps OFF (`_apply_cap(..., use_caps=False)`) +
  dynamics anti_concentration ON (`ablation = "full"`).

Run all three on the robust worlds at default, plus along axis 1
(`adversarial_pressure`) and axis 7 (cap tightness). Report which AC
implementation is load-bearing. If `C_caps_only` or `C_dyn_only` reproduces
`C_full`, the story simplifies (verdict BD).

## G4 — Threshold Sensitivity (resolves researcher-DOF concern)

Recompute the per-world classification (Type AC / CG / AC+CG / None) under a grid
of viability thresholds, holding runs fixed:

- `welfare_floor` ∈ {0.50, 0.55, 0.60}
- `exploit_ceiling` ∈ {0.35, 0.40, 0.45}
- `permanence_requirement` ∈ {0.90, 1.00} (per-run viability uses `permanence >= req`)
- `response_div_floor` ∈ {0.30, 0.35, 0.40}

For each world, report the fraction of the 54 threshold combinations under which
it is classified AC+CG (and the fraction Type None). A verdict is
**threshold-stable** if it holds in ≥ 90% of combinations. Flips must be reported
honestly (verdict BC).

---

## Validation Gates

Re-run all Exp15 gates (blindness, mutation/selection, feature-proxy fails W1,
no-control raises exploitation, Part A no delayed consequence, Part B no fixed
caps). All must pass, else verdict BF. Add:

- `ac_cg_strictly_dominates_singles_in_robust_worlds`: in W6/W3/W4 at the default
  operating point, `perm(C) - max(perm(A), perm(B))` paired CI-lo > 0.
- `boundary_exists_for_each_axis`: at least one swept axis where C transitions
  robust → fail within range (otherwise flag the axes that never break).
- `decoupling_identifies_load_bearing_ac`: at some operating point, at least one
  of {`C_caps_only`, `C_dyn_only`} differs from `C_full` beyond CI.

## Outputs (`results_16/`)

- `raw/runs.csv`, `raw/summary.csv` — all runs + summarized cells (Exp15 schema).
- `raw/boundary.csv` — per (world, axis): bracket endpoints + endpoint metrics.
- `raw/marginal.csv` — per cell: `gap_AC`, `gap_CG`, paired CIs.
- `raw/decoupling.csv` — `C_full` / `C_caps_only` / `C_dyn_only` per cell.
- `raw/sensitivity.csv` — classification per (world, threshold-combo).
- `boundary_atlas.md` — per world: axis → robust-up-to / fails-at table; where
  `gap_AC` and `gap_CG` peak.
- `sensitivity_report.md` — threshold-stability table + decoupling result +
  validation checks + final verdict.
- SVGs (reuse `svg_bar`; add `svg_line`): per robust world, permanence-vs-axis
  lines for A/B/C overlaid (the visible gap); `gap_AC`/`gap_CG` vs axis; a
  boundary-summary bar.
- `run_manifest.json`: `git_head`, `spec_exp16_sha256`, `num_cases`, `num_runs`,
  `validation_checks`, `boundary_summary`, `threshold_stability`, `final_verdict`.

## Verdict Options

- **BA**: AC+CG is threshold-stable and has finite, mapped boundaries on ≥3 axes;
  both levers show positive marginal value somewhere. (Dual necessity, with
  limits — the target outcome.)
- **BB**: AC+CG holds but boundaries fall outside the swept range on several axes
  (more robust than expected; widen sweeps and re-run).
- **BC**: classification flips under threshold perturbation (NOT threshold-stable;
  honest weakening of the Exp15 verdict).
- **BD**: one AC implementation alone reproduces `C_full` (double-implementation
  collapses to a single load-bearing lever; simplify the model).
- **BF**: a validation gate failed.

## Determinism & Runtime

No wall-clock dependence. Manifest records git head + spec sha256. Estimate and
print `num_cases` before running; expose `SEEDS` and `--smoke`. Keep the full
grid within a single-machine overnight budget; if it exceeds, reduce axis
granularity before reducing seeds (CIs matter more than grid density).
