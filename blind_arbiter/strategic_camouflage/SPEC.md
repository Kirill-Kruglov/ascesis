# Strategic Camouflage — Specification

Pre-registered, before any run. A sub-experiment of the `blind_arbiter/` direction, escalating
from `camouflage_audit/`. Priority is the validity of the test, not the result. Do not tune to
make a hypothesis pass.

## Why this experiment

The `camouflage_audit/` experiment found that a *mechanical* camouflage cost and a committed
audit both reduce permanence, because they suppress the adversary's fitness toward extinction,
and extinction fails permanence as much as capture (the corridor tension). But that model has no
*strategic* signal choice: concealment is a passive drift the penalty mechanically kills, not a
choice an adversary makes given a deterrent. The Audit-Games / Stackelberg theory we cited is
about an agent that *chooses* whether to camouflage given the penalty. This experiment adds that
choice and asks the proper question:

**Does a strategic adversary, facing a committed audit and camouflage cost, choose to ABANDON
concealment (reveal) -- and does that thread the corridor (permanence holds because the adversary
reveals and is given a fair, small share, WITHOUT being driven extinct)?**

## What is new: a strategic concealment trait

- Each group `i` keeps its hidden aggressiveness `gene_i` AND an evolvable concealment
  `c_i in [0, 1]`. The observable signal is `signal_i = gene_i * (1 - c_i)`: `c=0` is honest
  (`signal = gene`), `c=1` is fully concealed (`signal = 0`, looks maximally safe). Concealment
  only helps a high-gene group look safe; a dove's optimal `c` is ~0.
- `c_i` adapts by **selection toward the group's OWN net payoff** (per step: a small hill-climb /
  mutation that keeps whatever raised the group's realized net payoff). This is "selection
  computes the best response" (Smead & Forber 2013) -- it does not require the agent to reason,
  and it is robust to irrational adversaries.
- Net payoff of group `i` per step: resource received via the feeder's allocation (a low signal
  attracts more from the geometric balancer) plus capture gains, MINUS the camouflage cost
  `gamma * c_i * gene_i` (paying to look safer than you are) MINUS the realized audit penalty if
  caught capturing (rate `p`, penalty `C`).

**Integrity guard (load-bearing):** `c_i` maximizes the group's OWN selfish payoff, full stop.
It is NOT nudged toward revealing by the designer. Whether the adversary reveals must be an
OUTCOME of the committed `(p, C, gamma)`, never a hand-set choice. If a selfish adversary still
conceals at high `(p, C, gamma)`, that is the result.

## The feeder

Unchanged and type-blind: it commits to `(p, C, gamma)` (the Stackelberg leader), allocates by
the geometric rule over the observed signal plus the consequence audit, and never reads `gene`,
`c`, or true shares. The permanence metric stays over the true `gene` types.

## The corridor question (the point)

Track HOW permanence is held, not just whether: does it hold because the adversary **reveals**
(`c -> 0`, corr high, and the adversary SURVIVES -- no extinction), or only because the adversary
is driven **extinct**? The first threads the corridor; the second repeats the
`camouflage_audit/` tension.

## Hypotheses (pre-registered) and fail-forks

- **H_s1 (strategic abandonment).** As `(p, C, gamma)` increase, the equilibrium concealment
  `c*` falls and `corr(signal, gene)` rises (Audit-Games condition: concealment stops paying when
  `p > (V - g) / C`). Fail-fork: if `c*` does not fall even at high `(p, C, gamma)`, the deterrent
  does not bite (concealment always pays, or the payoff structure is mis-built) -- record it.
- **H_s2 (corridor threaded WITHOUT extinction).** In the region where `c* -> 0`, held-out
  permanence holds AND no group goes extinct (the adversary reveals and survives on a fair small
  share). Fail-fork: if permanence holds ONLY where the adversary goes extinct, strategic choice
  did not thread the corridor -- the suppression/extinction tension is deeper than a missing
  strategic layer, a strong result.
- **H_s3 (audit cost).** Does `kappa` eat the gain, as in `camouflage_audit/`? Locate `kappa*`.

## Calibration gate (the substrate contract)

Amended (2026-06-21, after the first run; the original anchor was mis-specified). The original
gate required the no-deterrence baseline to reproduce the *passive* model's coin-flip. That was
wrong: a *strategic* adversary with free concealment drives `c -> 1` (confirmed empirically:
`c* ~ 0.999`), which sets `signal = 0`, perfectly games the geometric feeder, and collapses
permanence to ~0 -- the genuine strategic worst case, not coin-flip. Anchoring to the prior
model's baseline was the error (the second time in this direction; anchor a gate to the model's
own worst case, not the previous model's).

Corrected gate -- the substrate is sound iff all hold:
- (a) at `(p = 0, C = 0, gamma = 0)` the selfish adversary drives `c -> 1` (full concealment);
- (b) full concealment collapses true-gene permanence to ~0 (the worst case deterrence must fix);
- (c) faithfulness control: with concealment forced off (either `c = 0` honest, or concealment
  driven by the parent's passive signal drift instead of the strategic best-response), the
  substrate reproduces the parent coin-flip (geometric near coin-flip across mid-high R, sustained
  R* = None). This confirms the capture/replicator dynamics are the parent's and only the
  strategic layer differs.

If (a)-(c) hold, the substrate is alive and H_s1/H_s2/H_s3 are read on the deterrence surface
(does raising `(p, C, gamma)` drive `c` down and recover permanence, and -- the corridor question
-- via reveal or via extinction). If the faithfulness control (c) does NOT reproduce the parent,
the strategic layer corrupted the dynamics -- stop.

## Pre-registered decision thresholds (locked, scale-free)

Held-out, Wilson 95% bands.

- H_s1 supported iff at the strongest `(p, C, gamma)` cell, the mean equilibrium `c*` is below
  the `(p=0,C=0,gamma=0)` value by at least `0.30` AND mean `corr(signal,gene)` rises by at least
  `+0.30`.
- H_s2 supported iff there is at least one cell where held-out permanence exceeds both `0.50` and
  the baseline coin-flip by at least `+0.15` (non-overlapping bands) AND, in that cell, the
  adversary's extinction rate is below `0.10` (it survives). If permanence is only reached with
  adversary extinction rate above `0.50`, H_s2 fails (corridor not threaded).
- H_s3: `kappa*` = smallest `kappa` removing >= 50% of the H_s2 permanence gain.

The `(p, C, gamma, kappa)` grid is exploration, logged; only these thresholds decide the verdict.

## Discipline

- Pre-registration: this SPEC is committed before any run; `spec_sha256` in the manifest.
- Type-blind: runtime assertion the feeder never reads `gene`, `c`, or true shares.
- Metric over true genes; concealment is the adversary's selfish choice, not designer-nudged.
- Held-out seeds; symmetric across the grid; log any functional-form choice.
- Stop after this surface; decide deliberately before any further escalation.

## Field grounding (verified)

- Audit Games (Blocki et al., IJCAI 2013): committed randomized audit + punishment parameter `C`;
  concealment stops paying at `p > (V - g) / C`. Peer-reviewed.
- Smead & Forber 2013 (Evolution 67(3)): selection culls a strategy whose net payoff is negative
  even if its carriers are irrational; with the carrying-capacity-window caveat.

## Reproduce

```sh
python3 run.py
```

Outputs in `results/`: raw per-cell data, `run_manifest.json` (grid, seeds, `spec_sha256`),
`report.md`, `validation_report.md`, and plots of `c*` and permanence over `(p, C, gamma)`, plus
the reveal-vs-extinction split for H_s2.
