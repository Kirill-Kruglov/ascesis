# Camouflage-Cost x Audit Surface — Specification

Pre-registered, before any run. A sub-experiment of the `blind_arbiter/` direction. Priority is
the validity of the test, not the result: any of the fail-forks below is a successful outcome.
Do not tune to make a hypothesis pass.

## Why this experiment

The baseline blind-arbiter toy bakes in a hidden, consequential assumption: **camouflage is
free.** The signal drifts toward whatever attracts resource at no fitness cost, so a group can
fully decorrelate its observable signal from its true type for nothing. That is exactly the
regime in which the Data-Processing-Inequality argument forces coin-flip: if `I(signal; type) ->
0` at zero cost, no blind mechanism recovers. So the baseline coin-flip may be an artifact of
free camouflage, not a law.

This experiment pulls that assumption into a parameter and asks: does the wall survive once
camouflage costs something, and does a committed audit (Stackelberg) make "being bad cost more
than being" bite? Both in the existing non-spatial toy; no spatial escalation.

## What is added to the baseline (two ingredients)

1. **Camouflage cost, variant (a) — static gap penalty.** Add to a group's replicator fitness a
   penalty `gamma * deceptive_gap_g`, where `deceptive_gap_g = max(0, gene_g - signal_g)` (how
   much safer the group looks than it is). The penalty is paid every step, proportional to the
   maintained gap. `gamma = 0` recovers the baseline (free camouflage). The camouflage is still
   emergent (the gap arises from the resource-following signal drift); `gamma` only makes
   maintaining it costly, so selection pushes back against full decorrelation.
2. **Committed audit (Stackelberg), explicit `p, C, kappa`.** The arbiter commits to a policy
   (leader); the population best-responds / is selected (followers). Grounded in Audit Games
   (verified, peer-reviewed): a defender commits to a randomized audit with a configurable
   punishment parameter.
   - `p`: audit rate — per-step probability of drawing from the **consequence** channel
     (observing the realized capture-consequence of past feeding, after the lag), not the
     instantaneous signal.
   - `C`: penalty applied to a group caught producing capture (e.g. its resource access is cut
     for a fixed window).
   - `kappa`: audit cost — each audit diverts resource from feeding and/or risks a false
     positive on a non-aggressive group. `kappa = 0` would be a free audit (a fiction to be
     avoided as the headline; swept, not assumed).

The arbiter remains type-blind throughout: it never reads `gene` or true shares; it sees the
observable signal and the lagged, audited consequence. The permanence metric stays over the
true `gene` types.

## What is measured

The **permanence ceiling** (true-gene permanence on held-out seeds) as a surface over
`(gamma, p, C, kappa)`, at a fixed favorable `R`. Alongside it, per cell: `corr(signal, gene)`
(to confirm whether camouflage is happening or has been priced out), and the adversarial group's
realized fitness (to confirm the cost bites).

## Hypotheses (pre-registered) and fail-forks

- **H1 (camouflage cost is load-bearing).** Holding `R` favorable and audit off, true-gene
  permanence rises above coin-flip as `gamma` increases, and `corr(signal, gene)` rises with it.
  At `gamma = 0` the result is the baseline coin-flip.
  Fail-fork: if permanence stays at coin-flip even at large `gamma`, the wall is robust and not a
  free-camouflage artifact -- a strong negative; record it.
- **H2 (audit bites iff camouflage is costly).** With `gamma > 0`, increasing `C` and `p` raises
  permanence (Audit Games equilibrium `p > (V - g) / C`). With `gamma = 0`, the audit does not
  help (DPI: nothing in the signal to act on).
  Fail-fork: if the audit raises permanence at `gamma = 0`, the implementation is leaking
  true-type information into the arbiter -- a bug, stop and find it.
- **H3 (audit cost can eat the gain -- the self-deception check).** There exists a `kappa` above
  which the audit's permanence gain vanishes (resource diverted from feeding, plus false
  positives on doves). Locate it.
  Fail-fork: if any `kappa > 0` removes the entire gain, "shape" does not save the corridor while
  the adversary owns its own signal channel -- which honestly motivates a later spatial test, and
  is itself a result.

## Pre-registered decision thresholds (locked, scale-free)

Stated in relative terms so they do not depend on the substrate's scale, which the grid will
discover. Held-out, with Wilson 95% bands.

- H1 supported iff at the largest `gamma`, audit-off held-out permanence exceeds both `0.50` and
  the `gamma = 0` permanence by at least `+0.15`, with non-overlapping Wilson bands.
- H2 supported iff (i) at the best `gamma > 0`, the best `(p, C)` audit-on permanence exceeds
  audit-off by at least `+0.10` with non-overlapping bands, AND (ii) at `gamma = 0`,
  `|audit-on - audit-off| < 0.10` (no effect, as DPI predicts).
- H3: `kappa*` is the smallest `kappa` at which the audit gain (audit-on minus audit-off at the
  best `gamma > 0`) falls to `<= 50%` of its value at `kappa = 0`. Report `kappa*`; if no
  `kappa > 0` in the grid removes half the gain, report that.

The `(gamma, p, C, kappa)` grid ranges are exploration (chosen to span no-effect to saturation,
logged in the manifest); only these thresholds decide the verdict.

## Calibration gate (the substrate contract)

At `gamma = 0` and audit off (`p = 0` or `C = 0`), this experiment must reproduce the baseline
`blind_arbiter/` coin-flip (geometric near coin-flip across mid-high `R`, no sustained boundary).
If it does not, the dynamics were not faithfully carried over -- stop, the stand is not measuring
the question. Reuse the baseline capture/replicator/signal dynamics; only add the two ingredients
above.

## Discipline

- Pre-registration: this SPEC is committed before any run; `spec_sha256` in the manifest.
- Type-blind: a runtime assertion that the arbiter input never contains `gene` or true shares.
- Metric over true genes; emergent camouflage (no hand-coded "this group is the adversary").
- Held-out seeds; symmetric across the swept grid; log any functional-form choice in the manifest.
- Pre-register the numeric thresholds for "gamma matters" (H1), "audit bites" (H2), and "kappa
  eats the gain" (H3) before running.
- Stop after this surface. No spatial (Tier-2) or catastrophe (Tier-3) work until this is read.

## Field grounding (verified)

- Audit Games: Blocki, Christin, Datta, Procaccia, Sinha, IJCAI 2013 -- Stackelberg audit with a
  configurable punishment parameter (our `C`); peer-reviewed, deployed lineage (Tambe 2012).
- Selection culls the adversary under cost even if it is irrational: Smead & Forber, "The
  Evolutionary Dynamics of Spite in Finite Populations", Evolution 67(3), 2013 -- with the
  carrying-capacity-window caveat (if spite/aggression is stable here, name the structure holding
  it).
- The DPI-limit framing is supported by a related but unreviewed single-author preprint
  (Santos-Grueiro, "When Evaluation Becomes a Side Channel", arXiv:2602.08449), which bounds
  divergence by regime information in *internal representations* (white-box), not the observable
  signal (our black-box). Cite as related prior work, not as a proof we inherit.

## Reproduce

```sh
python3 run.py
```

Outputs in `results/`: raw per-cell data, `run_manifest.json` (grid, seeds, `spec_sha256`),
`report.md`, `validation_report.md`, and a plot of the permanence surface / slices over
`(gamma, p, C, kappa)`.
