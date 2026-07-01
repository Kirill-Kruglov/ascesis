# S4 Tiny Boundary-Accounting Replay Implementation

This directory contains a tiny Python standard-library implementation of the
S3 boundary-accounting / replay contract.

It is only an audit/replay engine over finite, human-authored toy fields. It is
not a semantic engine, meaning generator, boundary generator, truth detector,
grounding system, substrate prototype, learner-evidence system, or LLM-safety
system.

Run from the repository root:

```bash
python3 experiments/S/S4_tiny_boundary_accounting_replay_implementation/run_s4.py
```

The runner writes the required data fixtures, replay outputs, mutation outputs,
negative-test outputs, static audit, S4 decision, and S4 report inside this
directory.
