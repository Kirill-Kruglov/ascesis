# Blind Type-B Arbiter

A focused working package for one research direction: **can an active, type-blind arbiter
keep a population in equilibrium when part of that population is adversarial and actively
games the signals the arbiter can see?**

The picture: an AGI/ASI modelled not as an optimizer of "the good" (which is ill-posed when
values are plural and contested), but as an active **feeder** for a population — including
agents that search for and exploit reward hacking under hard optimization. The feeder never
classifies agents. It only dispenses resource and reacts to the realized consequences of past
dispensing after a lag, with stochastic audits.

This package is self-contained: read `SPEC.md` for the design and findings, `references.md`
for field ownership, and `run.py` for the test. It was extracted from the
`ascesis_of_learning_grace` research trail once it passed a minimal proof threshold; the full
trial-and-error history is in the git commit log.

## Current result (one paragraph)

The substrate is alive (it passes the locked existence checks C1' and C2'). The key,
non-tautological finding: the active blind arbiter (`geometric` rule) holds the population's
true permanence above a boundary `R* = 0.833` **even though its observable signal has
decoupled from the true types to `corr = 0.203`** — the signal is nearly useless, yet the
arbiter still defends the true floor, through its lagged reaction to consequences rather than
through reading the signal. Defending the floor under this Goodhart pressure **requires active
intervention**; a passive keeper does not hold it.

`R = horizon_harm / horizon_observation` is the safety/development trade-off curve: above `R*`
equilibrium holds, below it no blind mechanism does.

## Honest caveats

- Non-spatial toy; only one regime (`geometric`) achieves a boundary.
- Active intervention is required (not a passive keeper).
- The boundary is probabilistic: at/above `R*`, permanence holds on roughly 0.60-0.67 of
  held-out seeds — the ">= 51% under a safety trade-off" regime, not "always works".
- This is a direction with potential that passed a minimal proof threshold, not a solved
  problem or a claim of novelty. The value is the honest path and the bridges, credited to
  their fields in `references.md`.

## Run

```sh
python3 run.py
```

Regenerates `results/`: raw data, `run_manifest.json`, `report.md`, `validation_report.md`,
and SVG plots (permanence-vs-`R`, signal-gene correlation over time, and the three required
failure modes: camouflage faster than the window, collective hack, collective punishment).

## Open next steps

- Read the locked hypotheses (boundary location/sharpness; whether any regime moves `R*`)
  carefully, ideally with a second pair of eyes on the boundary-finding code.
- Understand why only `geometric` finds a boundary (a symmetry-of-effort check across regimes).
- A separate passive-keeper comparison.
- A spatial / multi-agent version, only if the non-spatial result holds up.
