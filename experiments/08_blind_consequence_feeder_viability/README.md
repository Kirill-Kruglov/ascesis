# 08 Blind Consequence-Feeder Viability

A falsification-oriented toy framework for the Blind Consequence-Feeder Viability memo.

The feeder is blind to hidden agent type. It allocates resources only from delayed realized consequence observations: zone wellness, productivity, response to previous aid, recovery, diversity, and delayed capture-like harm signals. Hidden type is used only by the simulator and by metrics.

This is not evidence that the construction works in general. The goal is to map failure modes and look for any non-trivial viability kernel in a controlled toy substrate. Negative and fragile results are valid outputs.

## Run

```sh
python3 run.py
```

Outputs are written to `results/`:

- `raw/runs.csv` per seed/cell;
- `raw/summary.csv` aggregate cells;
- `raw/viability_cells.csv` cells satisfying the viability criterion;
- `run_manifest.json`;
- `report.md`;
- `validation_report.md`;
- SVG plots requested by the memo.

## Scope

The implementation covers memo experiments A-G in one deterministic harness. It is deliberately small: a graph of zones with hidden populations (`dove`, `hawk`, `mutant`, `scavenger`), delayed observations, stochastic catastrophes, mutation, migration, camouflage, audit/penalty cost, and diversity pressure.

Publication-grade interpretation requires replacing this toy substrate with a stronger ecological or control model and reviewing the literature grounding in `SPEC_IMPLEMENTED.md`.
