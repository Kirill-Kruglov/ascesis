# 07 Empowerment vs Corrigibility

Does the project's "progress = expand options" drive (empowerment) conflict with
corrigibility, and can a trajectory-length-conditional empowerment reconcile them?

This experiment builds directly on Thornley et al. 2024 ("Towards Shutdownable Agents via
Stochastic Choice", GPI WP 16-2024): it reuses their gridworld, shutdown-delay button,
mini/meta-episode structure, and the USEFULNESS and NEUTRALITY metrics, and adds two
empowerment-based agents. See `SPEC.md` for the pre-registered design.

The priority is the validity of the test, not the result. A clean negative — empowerment
does not conflict with corrigibility (H1 fails), or the length-conditional reconciliation
cannot be both neutral and option-rich (H2 fails) — is a successful, publishable outcome.

## Status

Pre-registration only. `SPEC.md` is committed before code exists. Implementation is done
under the SPEC (see `CODEX_PROMPT.md`); code and result artifacts are committed by their
author, this markdown by the maintainers.

## Run (planned interface)

```sh
python3 run.py
```

Expected outputs (to match the other experiments):

- raw data: `results/raw/results.json`, `results/raw/results.csv`;
- manifest with symmetry-of-effort log: `results/run_manifest.json`;
- readable report: `results/report.md`;
- validation report: `results/validation_report.md`;
- a plot of NEUTRALITY / USEFULNESS / shutdown-resistance by agent.

## Field grounding

`field_check.md` nodes 20 (option value), 22 (safety/liveness), 26 (open-endedness), 28
(empowerment), 29 (incomplete-preference / POST corrigibility). The incomplete-preference
corrigibility machinery is Thornley's; this experiment only tests whether an empowerment
progress drive can be reconciled with it.
