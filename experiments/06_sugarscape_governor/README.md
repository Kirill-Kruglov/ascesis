# 06 Sugarscape Governor

Ecological validation for the narrowed active spine: `non-scalarizable value structures exist and require non-scalar agents`.

This experiment adds a thin governor layer to a Sugarscape-style ecology. The Sugarscape core is kept recognizable: spatial sugar, growback, vision, movement, metabolism, aging, death, reproduction, and wealth inequality. The governor does not compete as a population. It only chooses how a scarce seasonal budget is split between current feeding support and reproduction reserve.

## Source

- Epstein and Axtell, 1996, *Growing Artificial Societies*.
- Mesa Sugarscape G1mt-style example: growing Sugarscape with metabolism and trade-like wealth dynamics.

The code is self-contained for reproducibility. Before publication-grade use, a human should decide whether to vendor/import the exact upstream Mesa example or keep this transparent minimal implementation.

## Run

```sh
python3 run.py
```

Outputs:

- raw data: `results/raw/results.json`, `results/raw/results.csv`;
- readable report: `results/report.md`;
- validation report: `results/validation_report.md`;
- survival curve: `results/population_survival.svg`.

## Interpretation

Toy test 02 only diverges in environments that declare no valid scalar currency, so its separation is stipulated rather than emergent. This test asks whether the distinction still appears when the reproduction floor must emerge from demography. The result is negative by the pre-registered criterion: on held-out seeds the corrected geometric hedger survives strictly longer than the incomplete-preference governor (median collapse 180 vs 119; pairwise win rate 0.23 against a 0.55 threshold). This environment does not support incompleteness as necessary, and the negative is not to be reversed by trying a different ecology profile.
