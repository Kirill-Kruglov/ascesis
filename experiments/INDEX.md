# Experiment Family Index

Tracked/untracked git state is irrelevant for content meaning in this index. It records where the evidence currently lives after reorganization.

| family | role | canonical path | start file / report |
|---|---|---|---|
| 01-08 legacy active-spine experiments | Original toy benchmarks and validation trail for the non-scalar/incomplete-preference active spine and blind-consequence feeder branch. Experiments 09-12 are historically contained inside `08_blind_consequence_feeder_viability/` as successive implemented specs and result folders. | `experiments/01_goodhart_bench/` through `experiments/08_blind_consequence_feeder_viability/` | `experiments/README.md`, `experiments/validation_summary.md`, each experiment `README.md` / `SPEC.md` / `results/report.md`; for 09-12 use `experiments/08_blind_consequence_feeder_viability/SPEC_IMPLEMENTED_09.md` through `SPEC_IMPLEMENTED_12.md` |
| 13 evolvable action strategies | Intermediate post-08 executable experiment package before the DSL/collapse-boundary sequence. | `experiments/13_evolvable_action_strategies/` | `experiments/13_evolvable_action_strategies/SPEC_IMPLEMENTED.md` |
| 14-17F DSL, collapse, consequence, backbone, and latent geometry sequence | DSL/worldcore and collapse-boundary work leading into consequence/backbone/latent-geometry diagnostics. | `experiments/14_dsl_core/`, `experiments/15_collapse_boundary/`, `experiments/16_consequence_vs_feature/`, `experiments/17*_*/` | `experiments/14_dsl_core/EXPERIMENTS.md`, `experiments/15_collapse_boundary/README.md`, later `GPT_Codex_Spec_Experiment.md`, `summary.md`, or `final_report.md` outputs |
| JB / Justitia Boundary | Shield synthesis, abstraction fidelity kill-gate, and standard CEGAR boundary assessment. | `experiments/JB/` | `experiments/JB/INDEX.md` |
| BA / Boundary Analysis | Static and empirical analysis of why the Justitia boundary abstraction failed. | `experiments/BA/` | `experiments/BA/INDEX.md` |
| FA / Faithful Abstraction | False-safe witness taxonomy, invariant compression, candidate validation, and T-C gate state. | `experiments/FA/` | `experiments/FA/INDEX.md` |

## Preservation Note

Do not prune `outputs/`, `results/`, or `raw/` directories from this index pass. They are evidence artifacts unless a later explicit archive policy says otherwise.
