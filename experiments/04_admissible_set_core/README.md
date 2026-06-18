# 04_admissible_set_core

Toy bottom-up governor: build an admissible set by intersecting constraints, not by aggregating a utility function.

Run:

```sh
python3 run.py
```

Outputs:

- `results/raw/results.json`
- `results/raw/results.csv`
- `results/report.md`
- `results/admissible_set_size.svg`
- `results/run_manifest.json`

## Hard Rules

- Pre-registration: `SPEC.md` fixes hypothesis, metrics, environments, and win criteria before publication-grade runs. Commit the SPEC first; `run.py` records the git HEAD, dirty status, and SPEC hash in `results/run_manifest.json`.
- Held-out environments: tune only on train environments where a train/held-out split exists; declare winners only on held-out environments.
- Symmetry of effort: log improvement iterations for each side in `results/run_manifest.json`.
- Seeds and reproducibility: fixed seeds; reproduce with `python3 run.py` from this directory.
- Negative results publish: empty win lists and failed hypotheses are valid outputs.

