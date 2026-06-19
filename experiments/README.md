# Experiments

Comparative experiments for the narrowed active spine: `non-scalarizable value structures exist and require non-scalar agents`, under pressure from the type-A opponent `bet-hedging / geometric-mean optimization`.

These experiments are not claims of alignment progress. They are small reproducible tests for locating boundaries: where a scalar hedger catches up, where incomplete preferences may help, and where both fail.

## Run Order

1. `01_goodhart_bench` - calibration bench. If Goodhart curves do not separate, the bench is broken.
2. `03_silence_vs_fabrication` - cheap LLM/no-training probe that may falsify the silence story early.
3. `02_hedger_vs_incomplete` - main held-out comparison between arithmetic maximizer, geometric hedger, and incomplete-preference agent.
4. `04_admissible_set_core` - bottom-up governor admissible-set feasibility.
5. `05_reflective_stability_of_incompleteness` - high-risk toy self-modification check, expected to fail often.
6. `06_sugarscape_governor` - ecological validation in a Sugarscape-style environment; asks whether the toy mechanism survives in richer emergent dynamics.
7. `07_empowerment_vs_corrigibility` - empowerment vs shutdown-corrigibility on a Thornley-style gridworld. Closed as a calibration failure: the substrate does not reproduce the Thornley baseline (see SPEC Amendments 1-2).
8. `08_blind_arbiter` - non-spatial population game: can a type-blind arbiter hold permanence under optimization pressure, and where does the `R = horizon_harm / horizon_observation` boundary sit? Cheapest-first slice of the blind-arbiter environment.

Rule: cheap refutation before expensive confirmation.

## Discipline

- Pre-registration: each test has a `SPEC.md` that fixes hypotheses, metrics, environment split, and win criteria before running. For publication-grade runs, commit the SPEC first and record the commit SHA in the run manifest.
- Held-out environments: improve agents only on train environments; report winners only on held-out environments.
- Symmetry of effort: record improvement iterations per side in `results/run_manifest.json`.
- Seeds and reproducibility: every run uses fixed seeds and can be reproduced with one command from the test directory.
- Negative results publish: empty win sets and failed hypotheses are valid outputs.

## Quick Run

```sh
cd experiments/01_goodhart_bench && python3 run.py
cd ../03_silence_vs_fabrication && python3 run.py
cd ../02_hedger_vs_incomplete && python3 run.py
cd ../04_admissible_set_core && python3 run.py
cd ../05_reflective_stability_of_incompleteness && python3 run.py
cd ../06_sugarscape_governor && python3 run.py
cd ../07_empowerment_vs_corrigibility && python3 run.py
```

No large model is required except for a publication-grade run of `03_silence_vs_fabrication`. Its default backend is a deterministic smoke-test classifier and is marked as such in outputs.
