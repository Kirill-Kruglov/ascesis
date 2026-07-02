# Codex Spec — Experiment 15: Collapse Boundary

## Project

`15_collapse_boundary`

## Goal

Build a minimal computational experiment to test whether there is a practical boundary between:

1. **dead systems**
   confluent / terminating / normalizing rewrite systems that collapse to a small finite set of canonical forms;

2. **live systems**
   non-confluent systems with collapsing rules that generate sustained novelty;

3. **fake-live systems**
   systems that generate endless surface novelty but fail learnability, i.e. noisy-TV behavior.

The experiment is not about improving term rewriting theory.

The experiment exists to answer:

> Can a rewrite-based substrate generate novel + learnable structure suitable, in principle, for later LLM training?

---

# 1. Non-negotiable research constraints

Do not implement Sanskrit.

Do not train LLMs.

Do not build large models.

Do not optimize for impressive numbers.

The purpose is to falsify.

Every metric must be able to say:

```text
dead
fake-live
live-but-not-learnable
live-and-learnable
```

---

# 2. Systems to implement

Implement at least four rewrite-system families.

Each system should generate rewrite trajectories from initial terms.

A term may be represented as a tree:

```python
Term(symbol: str, children: tuple[Term, ...])
```

Rules:

```python
RewriteRule(lhs_pattern, rhs_template, name, collapsing: bool)
```

---

## System A: Dead control

A small confluent + terminating system.

Example families:

```text
add(0, x) -> x
add(s(x), y) -> s(add(x, y))
mul(0, x) -> 0
mul(s(x), y) -> add(y, mul(x, y))
```

or another simple normalizing arithmetic / expression simplification system.

Expected:

```text
normal forms saturate
novelty plateaus
learnability may be high but finite
```

---

## System B: Trivial fake-live control

A system with endless syntactic novelty but no semantic content.

Examples:

```text
A(x) -> A(wrap(x))
Noise(x) -> Noise(bit0(x)) | Noise(bit1(x))
```

Expected:

```text
novelty high
learnability low or collapses to distributional prediction
semantic compression low
no useful task transfer
```

This is the noisy-TV baseline.

---

## System C: Collapsing-rule live candidate

A weakly non-confluent system with collapsing rules.

Example pattern:

```text
F(x, y) -> x
F(x, y) -> y
G(x) -> F(G(a(x)), G(b(x)))
```

or other minimal systems where collapsing rules allow structurally different normal forms / trajectories.

Expected unknown.

This is the first “live zone” candidate.

---

## System D: Structured live candidate

A system with collapsing rules plus interpretable compositional structure.

It should generate trajectories that can be mapped to small semantic tasks.

Example ingredients:

```text
choose(proof1, proof2) -> proof1
choose(proof1, proof2) -> proof2
compose(rule_a, rule_b, x) -> rule_b(rule_a(x))
lemma(x) -> x
lemma(x) -> cached(x)
```

This system should preserve some structured labels:

```text
operation type
dependency relation
proof step type
source-target relation
```

Expected:

```text
novelty may grow
learnability should be testable
```

---

# 3. What to generate

For each system:

1. sample initial terms;
2. run bounded rewrite exploration up to horizons:

```text
h = 1, 2, 4, 8, 16, 32, 64
```

3. collect:

```text
all reachable terms
normal forms if present
rewrite trajectories
trajectory DAGs
canonical term shapes
canonical trajectory shapes
```

Use deterministic seeds.

---

# 4. Core metrics

For each system and horizon h compute:

## 4.1 State novelty

```text
unique canonical terms / generated terms
```

## 4.2 Normal-form novelty

```text
unique normal forms / terminating trajectories
```

If no normal forms exist, report:

```text
normal_form_absent
```

## 4.3 Trajectory novelty

```text
unique canonical rewrite trajectories / generated trajectories
```

## 4.4 Shape entropy

Entropy over canonical term shapes and trajectory shapes.

## 4.5 Closure horizon estimate

Estimate the smallest h where marginal novelty drops below thresholds:

```text
epsilon = 0.01, 0.001
```

Report:

```text
h_0.01
h_0.001
```

If no plateau is detected, report:

```text
no_plateau_observed
```

---

# 5. Learnability tests

Do not use LLMs.

Use lightweight learners only:

```text
logistic regression
random forest
small MLP if already easy
```

Generate prediction tasks from trajectories.

Minimum tasks:

## Task 1: next-symbol prediction

Given partial trajectory, predict next top-level rewrite rule.

## Task 2: reachability

Given term A and term B, predict whether B is reachable from A within bounded h.

## Task 3: normal-form class

Given initial term, predict canonical class of resulting normal form, if applicable.

## Task 4: trajectory property

Predict interpretable property:

```text
uses collapsing rule?
terminates?
contains branch reuse?
has two alternative derivations?
```

---

# 6. Novel + learnable criterion

A system is not “live” merely because novelty grows.

For each horizon h report:

```text
novelty_score
learnability_score
random_baseline
majority_baseline
memorization_baseline
OOD_accuracy
```

OOD splits must be by:

```text
larger depth
unseen initial term shapes
unseen trajectory shapes
```

A system is considered promising only if:

```text
novelty remains high
AND learner beats majority/memorization
AND OOD accuracy improves with more data
AND tasks are not solved by trivial surface features
```

---

# 7. Noisy-TV detection

Implement explicit fake-live diagnostics.

A system is noisy-TV-like if:

```text
novelty high
AND compression does not improve
AND OOD learnability flat
AND generated labels are unpredictable except by memorizing distribution
```

Report:

```json
{
  "noisy_tv_score": ...,
  "reason": ...
}
```

---

# 8. Compression diagnostics

For each system and h:

1. serialize generated terms;
2. estimate compression ratio using gzip or zlib;
3. compare compression improvement across h.

Report:

```text
raw_size
compressed_size
compression_ratio
compression_gain
```

Rationale:

```text
pure noise produces novelty without useful compressible structure
dead systems compress too easily after closure
candidate live systems should show growing structure without immediate saturation
```

---

# 9. Output files

Required outputs:

```text
outputs/system_summary.json
outputs/horizon_metrics.csv
outputs/novelty_curves.csv
outputs/learnability_curves.csv
outputs/noisy_tv_report.json
outputs/compression_report.csv
outputs/closure_horizon_report.json
outputs/trajectory_shape_counts.csv
outputs/term_shape_counts.csv
outputs/final_decision.json
```

Required plots:

```text
outputs/novelty_vs_horizon.png
outputs/learnability_vs_horizon.png
outputs/novelty_learnability_phase_plot.png
outputs/compression_vs_horizon.png
outputs/closure_horizon_comparison.png
```

---

# 10. Final decision logic

Produce:

```text
outputs/final_decision.json
```

with one result per system:

```json
{
  "system": "A_dead_control",
  "classification": "dead | fake_live | live_candidate | inconclusive",
  "evidence": {
    "closure_horizon": "...",
    "novelty": "...",
    "learnability": "...",
    "compression": "...",
    "ood": "..."
  }
}
```

Also produce global conclusion:

```json
{
  "does_live_zone_exist_in_this_toy_setting": true/false/"inconclusive",
  "best_candidate_system": "...",
  "main_failure_mode": "...",
  "next_recommended_experiment": "..."
}
```

---

# 11. Kill conditions

The experiment should explicitly say STOP if:

## Case 1

Dead control does not collapse.

Then our theory-to-practice mapping is broken.

## Case 2

Fake-live control looks good under metrics.

Then metrics are too weak.

## Case 3

Collapsing-rule systems show novelty but fail learnability.

Then collapsing rules alone are not sufficient.

## Case 4

All systems collapse at similar h.

Then current rewrite-system approach is not promising.

## Case 5

Structured live candidate beats baselines on novelty + learnability.

Then proceed to a richer proof-DAG substrate experiment.

---

# 12. README requirements

Include:

1. how to install;
2. how to run tests;
3. how to run the experiment;
4. explanation of each metric;
5. interpretation guide;
6. warning that this is not yet an LLM experiment;
7. explanation of how this connects to the long-term LLM substrate goal.

---

# 13. Expected command

From project root:

```bash
pip install -e .
pytest
python scripts/run_collapse_boundary.py --seed 42 --max-horizon 64 --samples 5000
```

Optional larger run:

```bash
python scripts/run_collapse_boundary.py --seed 42 --max-horizon 128 --samples 20000
```

---

# 14. Report back

After running, return:

```text
outputs/system_summary.json
outputs/final_decision.json
outputs/closure_horizon_report.json
outputs/noisy_tv_report.json
outputs/learnability_curves.csv
outputs/novelty_curves.csv
all plots
```

The key question for interpretation:

```text
Did any collapsing-rule system produce novelty that remained learnable,
or only novelty that behaved like noisy-TV?
```
