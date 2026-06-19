# 08 Blind Type-B Arbiter (Non-Spatial Population Game)

Can a type-blind arbiter hold permanence of a population under optimization pressure and
signal-behavior decoupling (Goodhart), and where does the boundary in
`R = horizon_harm / horizon_observation` sit?

This is the cheapest-first slice of the blind-arbiter environment: a non-spatial population
game (shares on a simplex, replicator-style dynamics, a blind arbiter that reacts to realized
consequences after a lag), with no spatial grid and no multi-agent RL. If the `R`-boundary
does not appear even here, the idea is refuted cheaply; if it does, a spatial / MARL version
can follow. See `SPEC.md` for the pre-registered design and `CODEX_PROMPT.md` for the
implementation brief.

The priority is the validity of the test, not the result. The headline `R < 1` failure is
near-definitional (calibration); the real content is the location and sharpness of `R*`, the
three required failure-mode plots, and whether any arbiter regime moves `R*`.

## Status

Pre-registration only. `SPEC.md` is committed before code exists. Code and result artifacts
are committed by their author (Codex); the maintainers commit the markdown.

## Run (planned interface)

```sh
python3 run.py
```

Outputs (matching experiments 01-06): `results/raw/results.json` and `.csv`,
`results/run_manifest.json` (seeds, R grid, regimes, `improvement_iterations`, SPEC sha256),
`results/report.md`, `results/validation_report.md`, and a permanence-survival-vs-`R` plot.

## Field grounding

Replicator permanence (Hofbauer & Sigmund), ESS / Hawk-Dove (Maynard Smith), indirect
reciprocity (Nowak & Sigmund 2005), mechanism design under hidden types (Myerson; Holmstrom),
Stackelberg / automated mechanism design. These need `field_check.md` entries before any
publication-grade use; the bridge to the project is resource-time-bounded safety (bridge 2)
and the safety/liveness and viability nodes (22, 27).
