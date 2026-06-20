# Blind Arbiter

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

## Current result (one paragraph, after a strict audit)

An earlier draft claimed the active blind arbiter "holds permanence above a boundary R*"; a
strict audit (`results/audit_report.md`) withdrew that. The honest result is weaker: a
non-spatial blind active arbiter does **not** reliably hold the population's true permanence
under Goodhart. Its permanence is non-monotonic and hovers near coin-flip across mid-to-high
`R` (about 0.43-0.67 for the best regime, with wide overlapping confidence bands and no value
of `R` above which it stays above 0.5). The signal is fully decoupled where it matters
(correlation ~0.07 at the supposed boundary). What does survive is an ordering — scalar
(permanence 0, dies by concentration) < lexicographic (~0.4) < geometric (~0.5) — so active
balancing and reacting to lagged consequences helps, but it does not amount to holding
equilibrium. Defending the floor at all requires active intervention; a passive keeper is not
expected to do better (a separate test, not yet run).

## Honest caveats

- Non-spatial toy; 30 held-out seeds; wide confidence bands.
- No sustained boundary: the earlier "holds above R*" / "safety-development trade-off curve"
  framing was withdrawn after audit.
- C1'(b) (the "alive" check) passes only marginally (geometric high-R mean permanence 0.511,
  inside the noise).
- This is a weak/negative result for the optimistic "active feeder holds equilibrium" thesis,
  not a solved problem and not a claim of novelty. The value is the honest path and the bridges,
  credited to their fields in `references.md`.

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
