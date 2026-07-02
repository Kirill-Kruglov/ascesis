# worldcore

`worldcore` is a toy typed symbolic world-state generator for testing whether a DSL core can produce novel and learnable reasoning tasks before adding any Sanskrit or surface-language layer.

## Install

From this directory:

```bash
pip install -e .
```

Dependencies are intentionally light: `networkx`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `tqdm`, and `pytest`.

## Tests

```bash
pytest
```

The tests cover typed fact generation, canonical graph hashing under entity renaming, explicit solver rules, contradiction detection, and novelty metrics.

## Experiments

Capacity bound:

```bash
python scripts/run_capacity.py --config small
```

Unified open-endedness and Kolmogorov trap check:

```bash
python scripts/run_openendedness.py --num-worlds 50000 --train-sizes 100 300 1000 3000 10000 --depth-train-max 2 --depth-test 3 4 5 --seed 42
```

FLD-style sanity replication:

```bash
python scripts/run_fld_sanity.py --num-examples 20000 --max-proof-depth 5 --seed 42
```

NLGIFT-style negative control:

```bash
python scripts/run_negative_control.py --num-examples 20000 --seed 42
```

Proof diagnostics v0.4.1:

```bash
python scripts/run_proof_diagnostics.py --num-worlds 50000 --train-sizes 100 300 1000 3000 10000 --depth-train-max 2 --depth-test 4 5 --seed 42
```

Proof opportunity audit v0.4.2:

```bash
python scripts/run_opportunity_audit.py --num-worlds 10000 --seed 42
```

For large audits, this writes one `outputs/closure/world_XXXXX.json` file per sampled world unless `--max-closure-files` is set.

## Output Artifacts

`outputs/capacity_summary.json` reports typed assignment counts, valid fact counts, an upper-bound estimate, sampled canonical uniqueness, `uniqueness_ratio`, `collision_fraction`, canonical collisions, and expected saturation.

`outputs/capacity_curve.csv`, `outputs/capacity_curve.png`, and `outputs/capacity_diagnostics.png` show observed novelty, canonical collisions, and expected saturation estimates.

`outputs/openendedness_summary.json` summarizes train/OOD counts, adversarial accuracy, final metrics, and detected warning reasons.

`outputs/world_novelty_curve.csv`, `outputs/task_novelty_curve.csv`, and `outputs/novelty_curve.csv` track canonical novelty independently for worlds and tasks.

`outputs/ood_split_validation.json` validates that train and OOD do not share canonical world hashes, canonical task hashes, entity names, or templates where possible.

`outputs/memorization_analysis.json` reports hash-only memorization with seen/unseen hash counts and accuracy on each split.

`outputs/label_distribution.json` reports true/false/unknown counts and normalized entropy.

`outputs/complexity_distribution.csv` reports reasoning depth, distractors, supporting facts, irrelevant facts, predicates, entities, and inference-rule counts per task.

`outputs/learnability_curve.csv`, `outputs/novelty_vs_learnability.png`, and `outputs/ood_depth_accuracy.png` compare OOD transfer against solver, hash memorizer, majority, and random baselines.

`outputs/kolmogorov_report.json` reports novelty, OOD transfer, memorization, solver curves, and suspected failure mode.

`outputs/experiment_summary.csv` is the dashboard table with train size, novelty, solver, memorization, majority, random, graph classifier, OOD, entropy, average depth, distractors, rules, and failure-mode signals.

`outputs/proofs/*.json` stores extracted proof DAGs with explicit rule nodes, supporting facts, intermediate lemmas, and final conclusions.

`outputs/proof_metrics.csv` reports length, depth, width, branching, reuse, fan-in, fan-out, alternative proof count, proof density, minimal proof length, proof entropy, difficulty, shape, and canonical proof hash.

`outputs/proof_shape_counts.csv` groups canonicalized proof graph topologies and reports shape cluster sizes.

`outputs/proof_novelty_curve.csv`, `outputs/proof_saturation.png`, and `outputs/novelty_comparison.png` compare proof novelty against world and task novelty.

`outputs/proof_space.png` is a PCA projection of structural proof vectors.

`outputs/difficulty_distribution.csv` records normalized structural difficulty and estimated backtracking complexity.

`outputs/correlations.csv` correlates proof difficulty/shape/length/entropy with OOD correctness.

`outputs/forced_length_summary.csv` audits whether the current generator can produce proofs with minimum lengths 2, 4, 6, and 8 without architectural changes.

`outputs/decision_gate.json` classifies the bottleneck as world generation, task extraction, proof algebra, or insufficient evidence.

`outputs/closure/world_XXXXX.json` stores full closure audits with initial facts, derived facts, rule applications, and derivation graph.

`outputs/closure_statistics.csv` reports initial fact count, derived fact count, closure size, expansion ratio, and rule application count per world.

`outputs/proof_opportunities.csv` enumerates available closure-level proof opportunities before task extraction.

`outputs/proof_opportunity_summary.csv` summarizes proof opportunities, distinct proof DAGs/shapes, alternatives, entropy, and largest shape fraction per world.

`outputs/extractor_coverage.csv` compares selected task proofs against all closure opportunities overall and by shape, length, and reasoning family.

`outputs/closure_graph_metrics.csv` reports reachability graph metrics over closure facts.

`outputs/closure_proof_novelty.csv` tracks proof novelty over all closure proof opportunities.

`outputs/difficulty_audit.csv` audits difficulty feature distributions, mutual correlations, and binary proof-existence collapse.

`outputs/forced_rejection_report.csv` records forced long-proof candidate rejection reasons.

`outputs/diversity_explanation.json` explains selected proof novelty vs closure/forced diversity discrepancies.

`outputs/reasoning_family_audit.csv` reports closure opportunity diversity and extractor coverage by reasoning family.

`outputs/sampling_simulation.csv` estimates proof diversity under alternative sampling strategies over the same closure.

`outputs/decision_H2.json` distinguishes closure-rich/extractor-poor from closure-poor/extractor-reasonable cases.

`outputs/fld_sanity_summary.json`, `outputs/fld_accuracy_by_depth.csv`, and `outputs/fld_accuracy_by_depth.png` verify that the pipeline can detect learning on a simple formal-logic generator.

`outputs/negative_control_summary.json`, `outputs/negative_control_ood.csv`, and `outputs/negative_control_ood.png` check that the framework can expose at least one OOD graph-generalization failure mode.

## Interpretation

The hypothesis should be paused if capacity saturates early, OOD leakage is detected, label entropy collapses, reasoning depth/rule counts are too low, hash memorization explains OOD accuracy, solver labels disagree with generated answers, or FLD sanity fails.

The hypothesis remains alive if canonical novelty grows without immediate saturation, train/OOD hashes and entity names are disjoint, OOD accuracy improves on unseen canonical tasks as train size grows, graph-feature learning beats hash-only memorization and majority baselines, and the symbolic solver validates task labels.

Proceeding to a Sanskrit/verifier phase requires novelty and learnability to stay coupled at scale, OOD transfer to improve with more generated data, memorization to be clearly beaten, adversarial pairs to remain solved by the symbolic checker, and the negative control to expose a real failure mode.

When stop conditions are detected, the open-endedness script prints:

```text
WARNING
Current experiment cannot falsify hypothesis.
Reason:
...
```
