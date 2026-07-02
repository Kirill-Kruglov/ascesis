# Experiment 17: Backbone Consequence

Experiment 17 does not search for better generators. It reuses Experiment 16's causal DAG substrate and verifier unchanged, and asks whether consequence-equivalence classes are globally necessary: do they persist under admissible perturbations of the causal theory?

This validates whether Global Necessity is a meaningful invariant, separate from class cardinality.

Run:

```bash
python scripts/run_backbone_consequence.py --seed 42 --num-dags 500 --max-depth 6
```
