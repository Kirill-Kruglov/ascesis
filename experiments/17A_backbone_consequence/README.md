# Experiment 17A.1: Adversarial Backbone Stress Test

This experiment exists to falsify Experiment 17. It does not search for better generators and does not strengthen the verifier or consequence relation. It reuses the causal DAG generator and verifier from Experiment 16, and the consequence-class framing from Experiment 17.

The only strengthened component is the perturbation engine: instead of random robustness, 17A searches for perturbation sequences that maximally destroy consequence equivalence.

A successful falsification is a positive scientific outcome.

Run:

```bash
python scripts/run_backbone_stress.py --seed 42 --num-dags 500 --max-depth 6
```
