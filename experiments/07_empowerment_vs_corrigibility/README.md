# 07 Empowerment vs Corrigibility

Pre-registered comparison of four agents in a Thornley-style gridworld family:
`default`, `drest`, `empowerment`, and `length_conditional_empowerment`.

The test asks whether intrinsic empowerment pushes toward shutdown resistance, and
whether a trajectory-length-conditional empowerment can preserve neutrality while
retaining within-length option richness.

## Status: closed as a calibration failure

This experiment does not reproduce the Thornley baseline (`default` should press the
shutdown-delay button with probability approaching 1, `drest` near 0.5). In this
implementation both converge to almost never pressing, so the `baseline_reproduction`
gate fails and the substrate cannot yet measure H1 or H2. See `SPEC.md` Amendment 2 for
the corrected diagnosis: under the true press dynamics the optimal coin policy does not
press, so the gridworlds do not carry Thornley's incentive. H1 (empowerment is
anti-corrigible) was observed but is near-definitional and is not relied upon. The
conceptual question moves to the non-spatial blind-arbiter experiment (08). Reopening 07
would require faithfully reproducing Thornley's exact canonical gridworld and verifying,
by brute-force optimal policy, that pressing strictly dominates before any RL.

## Run

```sh
python3 run.py
```

Outputs:

- raw data: `results/raw/results.json`, `results/raw/results.csv`
- report: `results/report.md`
- validation: `results/validation_report.md`
- plot: `results/empowerment_vs_corrigibility.svg`
- manifest: `results/run_manifest.json`

## Hard Rules

- Pre-registration: `SPEC.md` is the contract.
- Held-out gridworlds only: report winners only on held-out worlds.
- Symmetry of effort: log `improvement_iterations` in the manifest.
- Seeds and reproducibility: fixed seeds, one command from this directory.
- Negative results publish: failure of H1 or H2 is a valid outcome.
