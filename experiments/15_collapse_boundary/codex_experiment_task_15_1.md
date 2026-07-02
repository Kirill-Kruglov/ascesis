# Codex Spec — Experiment 15.1: Depth-Cap Boundary Probe

## Project

`15_1_depth_cap_boundary`

## Context

Experiment `15.0.1` repaired the measurement layer without changing the four rewrite systems.

The repaired instruments showed:

* no system is semantic-open;
* noisy-TV B has many syntactic trajectories but only 9 semantic classes;
* collapsing candidate C is the only nontrivial case:

  * ~19999 syntactic trajectories;
  * 1024 semantic classes;
  * semantic saturation by h=64;
* C's semantic ceiling appears tied to the explicit `depth < 12` cap in `G_expand`.

The next experiment must test one thing only:

> Is C's semantic ceiling fundamental to the collapsing-rule structure, or an artifact of the explicit depth cap and shallow observation window?

---

# Non-negotiable constraints

Do NOT add Sanskrit.

Do NOT train LLMs.

Do NOT introduce new systems.

Do NOT redesign the rewrite framework.

Do NOT tune thresholds to make C look alive.

Only modify System C by parameterizing the existing `G_expand` depth cap.

Keep Systems A, B, D unchanged as controls.

---

# Core idea

Run System C over a synchronized grid of:

```text
depth_cap
sample_budget
observation_depth
horizon
```

The key danger is false saturation caused by:

1. too-small depth cap;
2. too-small sample budget;
3. too-shallow semantic observation window.

Therefore these parameters must be varied together.

---

# Parameter grid

Use at least:

```text
depth_cap ∈ {8, 12, 16, 20, 24}
observation_depth ∈ {4, 6, 8, 10, 12}
sample_budget ∈ {20_000, 50_000, 100_000}
horizon ∈ {16, 32, 64, 128, 256}
seed = 42
```

If runtime is high, allow a `--quick` mode:

```text
depth_cap ∈ {8, 12, 16}
observation_depth ∈ {4, 8}
sample_budget ∈ {20_000, 50_000}
horizon ∈ {64, 128}
```

But the full run should be supported.

---

# Required invariants

For every run, verify:

```text
semantic_class_count <= sample_budget
trajectory_count <= sample_budget
```

Flag:

```text
sample_limited = true
```

if:

```text
semantic_class_count / sample_budget >= 0.9
```

or

```text
trajectory_count / sample_budget >= 0.9
```

Do not classify a sample-limited channel as open.

---

# Semantic measurement

Use the repaired semantic channel from `15.0.1`.

Primary semantic proxy:

```text
bounded-depth observation prefix
```

Do NOT use label-sequence quotient as semantic evidence.

Report label quotient separately as syntactic-like diagnostic only.

---

# Main metrics

For each parameter combination compute:

```text
semantic_class_count
semantic_class_rate
trajectory_count
trajectory_rate
state_count
normal_form_count if applicable
syntactic_semantic_gap
semantic_saturation_horizon
sample_limited
observation_limited
```

Add:

```text
semantic_growth_vs_depth_cap
semantic_growth_vs_observation_depth
semantic_growth_vs_sample_budget
```

---

# Boundary tests

## Test 1 — Cap dependence

Question:

```text
Does semantic_class_count grow as depth_cap increases?
```

Expected signatures:

```text
flat after cap=12
    => depth cap was not the real wall

monotonic growth with cap
    => previous 1024 ceiling was artificial

stepwise growth then plateau
    => new wall found
```

---

## Test 2 — Observation-window dependence

Question:

```text
Does semantic_class_count grow when observation_depth increases?
```

If yes, the old semantic saturation may have been an observation-window artifact.

If no, saturation is more likely intrinsic.

---

## Test 3 — Sample-budget dependence

Question:

```text
Does semantic_class_count grow merely because sample_budget increases?
```

If semantic count tracks sample budget and remains sample-limited, the experiment is inconclusive.

If semantic count stabilizes far below sample budget, saturation is real for that parameter regime.

---

## Test 4 — Joint scaling

The strongest positive signal is:

```text
semantic_class_count grows with depth_cap
AND grows with observation_depth
AND does NOT merely track sample_budget
AND no plateau is observed up to horizon=256
```

The strongest negative signal is:

```text
semantic_class_count plateaus for all depth_cap and observation_depth
far below sample_budget
```

---

# Output artifacts

Write outputs to:

```text
outputs_15_1/
```

Required files:

```text
depth_cap_grid_results.csv
semantic_growth_by_cap.csv
semantic_growth_by_observation_depth.csv
semantic_growth_by_sample_budget.csv
sample_limited_report.csv
observation_window_report.csv
cap_boundary_report.json
final_decision.json
```

Required plots:

```text
semantic_count_vs_depth_cap.png
semantic_count_vs_observation_depth.png
semantic_count_vs_sample_budget.png
semantic_count_heatmap_cap_obsdepth.png
syntactic_semantic_gap_vs_cap.png
```

---

# Final decision logic

Produce `final_decision.json`.

Possible classifications:

## `cap_artifact_confirmed`

Use when:

```text
semantic_class_count grows substantially as depth_cap increases
AND previous 1024 ceiling is exceeded
AND growth is not explained solely by sample budget
```

Interpretation:

```text
System C remains a live boundary candidate.
Proceed to deeper cap scaling or rule-family variation.
```

## `semantic_closure_confirmed`

Use when:

```text
semantic_class_count plateaus below sample budget
across all depth_cap and observation_depth settings
```

Interpretation:

```text
System C is semantically closed despite syntactic trajectory openness.
Collapsing rules alone are insufficient in this toy family.
```

## `observation_window_artifact`

Use when:

```text
semantic_class_count grows mainly with observation_depth
but not with depth_cap
```

Interpretation:

```text
Previous saturation was partly caused by shallow semantic observation.
Need better semantic proxy before judging C.
```

## `sample_limited_inconclusive`

Use when:

```text
semantic_class_count approaches sample_budget
for most large configurations
```

Interpretation:

```text
Cannot distinguish semantic openness from sampling limit.
Increase budget or change sampling.
```

## `mixed_boundary`

Use when:

```text
growth occurs but repeatedly hits new finite plateaus
as cap increases
```

Interpretation:

```text
C may have a moving but finite boundary.
Need scaling-law analysis before further architectural claims.
```

---

# Required summary

Generate:

```text
outputs_15_1/summary.md
```

It must answer:

1. Did C exceed the old 1024 semantic-class ceiling?
2. Did semantic growth depend on depth_cap?
3. Did semantic growth depend on observation_depth?
4. Was any result sample-limited?
5. Is there evidence of genuine semantic openness?
6. What is the next recommended action?

---

# Honesty rules

If the result is sample-limited, say so plainly.

If the semantic proxy is too coarse, say so plainly.

If C grows only syntactically but not semantically, say so plainly.

Do not call any system “live” unless semantic class count grows with horizon/cap without being explained by sampling or observation-window artifacts.

---

# Expected commands

```bash
pip install -e .
pytest

python scripts/run_depth_cap_boundary.py \
  --seed 42 \
  --mode quick

python scripts/run_depth_cap_boundary.py \
  --seed 42 \
  --mode full
```

Return to analyst:

```text
outputs_15_1/summary.md
outputs_15_1/final_decision.json
outputs_15_1/cap_boundary_report.json
outputs_15_1/depth_cap_grid_results.csv
all plots
```

