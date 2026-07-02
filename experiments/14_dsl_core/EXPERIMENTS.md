# Codex Spec: Sanskrit-as-World v0.3 — Toy DSL Core Experiments

## Goal

Implement a minimal experimental framework to test whether a symbolic world-state generator can produce **novel + learnable** reasoning tasks without collapsing into finite-template repetition.

This is **not yet about Sanskrit**. Sanskrit must not be implemented in this phase.
The goal is to test whether the DSL/world core is alive before adding any surface-language layer.

---

# 1. Deliverables

Create a Python project with:

```text
worldcore/
  README.md
  requirements.txt
  pyproject.toml or setup.cfg
  src/worldcore/
    __init__.py
    types.py
    generator.py
    canonical.py
    solver.py
    metrics.py
    experiments.py
    perturb.py
    baselines.py
  scripts/
    run_capacity.py
    run_openendedness.py
    run_fld_sanity.py
    run_negative_control.py
  outputs/
    .gitkeep
  tests/
    test_generator.py
    test_canonical.py
    test_solver.py
    test_metrics.py
```

Use only lightweight dependencies:

```text
networkx
numpy
pandas
scikit-learn
matplotlib
tqdm
pytest
```

No LLMs. No transformers. No external APIs.

---

# 2. Core concepts

## 2.1 World state

Represent a world state as a typed directed labeled graph.

Entities have:

```python
Entity(id: str, type: str)
```

Predicates / relations have:

```python
Fact(predicate: str, args: tuple[str, ...])
```

Example:

```text
type(h1) = Human
type(a1) = Animal
Owns(h1, a1)
Feeds(h1, a1)
Animal(a1)
Human(h1)
```

Use typed predicates with arity and allowed argument types.

Example schema:

```python
PredicateSpec(
    name="Owns",
    arg_types=("Human", "Object")
)
```

## 2.2 Toy ontology

Start with approximately:

```text
Types:
  Human
  Animal
  Plant
  Tool
  Place
  Food
  Object
  Event
  Group
  Property

Predicates:
  IsA(x, Type)
  HasProperty(x, Property)
  LocatedIn(x, Place)
  Owns(Human, Object)
  Uses(Human, Tool)
  Eats(Animal|Human, Food|Plant)
  Feeds(Human, Animal)
  Helps(Human, Human)
  ParentOf(Human|Animal, Human|Animal)
  FriendOf(Human, Human)
  Causes(Event, Event)
  Before(Event, Event)
  Prevents(Event, Event)
  Wants(Human, Object|Event)
  Knows(Human, Fact/Event)
  Believes(Human, Fact/Event)
  MemberOf(Human, Group)
  LeaderOf(Human, Group)
  BiggerThan(Object|Animal, Object|Animal)
  PartOf(Object, Object)
```

It is acceptable to simplify if implementation becomes cleaner.

---

# 3. Inference rules

Implement a symbolic solver with explicit rules.

Minimum rules:

## 3.1 Transitivity

```text
ParentOf(a,b) & ParentOf(b,c) -> AncestorOf(a,c)
Before(e1,e2) & Before(e2,e3) -> Before(e1,e3)
PartOf(x,y) & PartOf(y,z) -> PartOf(x,z)
```

## 3.2 Implication templates

```text
Feeds(h,a) -> Helps(h,a)
Owns(h,o) & Uses(h,o) -> HasAccessTo(h,o)
LocatedIn(x,p) & LocatedIn(p,q) -> LocatedIn(x,q)
```

## 3.3 Contradiction

Add negative facts:

```python
Fact(predicate="NOT_LocatedIn", args=(x,p))
```

Contradiction if:

```text
P(args) and NOT_P(args)
```

## 3.4 Quantifier-like toy rules

Avoid full FOL. Implement simple universal rules as templates:

```text
ForAll x: Human(x) -> Mortal(x)
Human(socrates)
=> Mortal(socrates)
```

Represent universal rules as objects, not as strings.

---

# 4. Task types

Generate reasoning tasks from world states.

Each task should include:

```json
{
  "world_id": "...",
  "task_id": "...",
  "facts": [...],
  "query": "...",
  "answer": true/false/"unknown",
  "proof_depth": int,
  "reasoning_pattern": "transitivity|contradiction|implication|quantifier|mixed",
  "canonical_world_hash": "...",
  "canonical_task_hash": "..."
}
```

Minimum task families:

1. Entailment
2. Contradiction
3. Unknown / not entailed
4. Multi-hop transitivity
5. Mixed two-rule inference
6. Distractor-heavy tasks

---

# 5. Step 0: Analytical capacity bound

Before training anything, implement:

```bash
python scripts/run_capacity.py --config small
```

It should estimate and report:

1. Number of possible typed entity assignments.
2. Number of possible valid facts.
3. Approximate upper bound on possible world states for fixed:

   * number of entities;
   * max facts per world;
   * predicate schema.
4. Number of unique canonical graphs observed after random sampling.
5. Collision rate:

   ```text
   sampled_worlds / unique_canonical_worlds
   ```
6. Estimated saturation curve.

Output files:

```text
outputs/capacity_summary.json
outputs/capacity_curve.csv
outputs/capacity_curve.png
```

Kill criterion:

```text
If canonical unique world states saturate very early under small sampling,
the generator is too small or too template-like.
```

---

# 6. Canonicalization / graph isomorphism

Implement canonical graph hashing so entity names do not count as novelty.

Example:

```text
Human h1 owns Animal a1
Human h2 owns Animal a2
```

These must be recognized as isomorphic.

Use `networkx` graph isomorphism or a deterministic canonical relabeling.

Required functions:

```python
canonical_world_hash(world: WorldState) -> str
canonical_task_hash(task: Task) -> str
is_isomorphic_world(w1, w2) -> bool
```

Tests must verify that renamed entities produce identical canonical hashes.

---

# 7. Unified open-endedness + Kolmogorov test

Implement one experiment, not two separate experiments.

Run:

```bash
python scripts/run_openendedness.py \
  --num-worlds 50000 \
  --train-sizes 100 300 1000 3000 10000 \
  --depth-train-max 2 \
  --depth-test 3 4 5 \
  --seed 42
```

## 7.1 Metrics

For each train size N, compute:

### Novelty

```text
world_novelty_rate(N) =
  new non-isomorphic worlds / generated worlds
```

```text
task_novelty_rate(N) =
  new non-isomorphic tasks / generated tasks
```

### Learnability

Use two learners:

1. symbolic solver — positive control;
2. lightweight statistical learner:

   * logistic regression or random forest over hand-engineered graph features;
   * optionally simple bag-of-facts classifier.

Do not use LLM.

Define learnability as:

```text
A task family is learnable if:
  model performance improves with N on validation tasks
  AND improvement transfers to held-out deeper tasks
  AND symbolic solver solves those tasks near-perfectly
  AND performance gain is not explained only by memorizing canonical hashes.
```

Report:

```text
in_distribution_accuracy
ood_depth_accuracy
solver_accuracy
memorization_baseline_accuracy
random_baseline_accuracy
```

### Kolmogorov trap signal

Detect the dangerous pattern:

```text
novelty_rate remains high
BUT ood_depth_accuracy plateaus or falls
AND solver_accuracy remains high
```

Interpretation:

```text
surface/world-form novelty exists,
but the generated states no longer provide useful learnable reasoning signal.
```

Output files:

```text
outputs/openendedness_summary.json
outputs/novelty_curve.csv
outputs/learnability_curve.csv
outputs/novelty_vs_learnability.png
outputs/ood_depth_accuracy.png
outputs/kolmogorov_diagnostics.json
```

---

# 8. FLD-style sanity replication

Implement a small formal logic dataset generator.

Run:

```bash
python scripts/run_fld_sanity.py \
  --num-examples 20000 \
  --max-proof-depth 5 \
  --seed 42
```

Generate simple examples:

```text
All A are B.
All B are C.
x is A.
Query: x is C?
Answer: true.
```

Also include distractors and unknown cases.

Purpose:

```text
Check that the experimental pipeline can detect learnable synthetic reasoning
when the generator is known to be reasonable.
```

Output:

```text
outputs/fld_sanity_summary.json
outputs/fld_accuracy_by_depth.csv
outputs/fld_accuracy_by_depth.png
```

Kill criterion:

```text
If the pipeline cannot detect learning on this simple FLD-like task,
then failure on the world generator is not informative.
```

---

# 9. NLGIFT-style negative control

Implement graph tasks where synthetic instruction-style data may fail to generalize.

Run:

```bash
python scripts/run_negative_control.py \
  --num-examples 20000 \
  --seed 42
```

Task types:

1. reachability;
2. shortest path length bucket;
3. ancestor relation;
4. disconnectedness;
5. cycle detection.

Train on small graphs, test on larger graphs and altered distributions.

Output:

```text
outputs/negative_control_summary.json
outputs/negative_control_ood.csv
outputs/negative_control_ood.png
```

Expected useful outcome:

```text
The framework should be capable of showing failure.
```

If every synthetic task looks successful, the metrics are too weak.

---

# 10. Required README

The README must include:

1. How to install.
2. How to run tests.
3. How to run each experiment.
4. Explanation of each output artifact.
5. Interpretation guide:

   * what result kills the hypothesis;
   * what result keeps it alive;
   * what result is ambiguous.

---

# 11. Success / failure interpretation

## Strong negative result

Project should pause if:

```text
capacity saturates early
OR novelty persists but learnability collapses
OR solver solves OOD but learner cannot improve beyond memorization
OR FLD sanity fails
```

## Weak positive result

Project remains alive if:

```text
canonical novelty grows sublinearly but does not immediately saturate
AND learnability improves with N
AND OOD proof-depth transfer is nonzero
AND solver confirms tasks are valid
```

## Strong positive result

Proceed to Sanskrit/verifier phase only if:

```text
novelty and learnability remain coupled over scale
AND OOD depth transfer improves with more generated data
AND memorization baseline is clearly beaten
AND negative control exposes at least one failure mode
```

---

# 12. Coding style

* deterministic seeds everywhere;
* type hints;
* small functions;
* pytest tests;
* save all outputs as JSON/CSV/PNG;
* no hidden randomness without seed;
* no notebook-only code;
* CLI scripts must be runnable from project root.

---

# 13. Final command sequence expected from user

After implementation, user should be able to run:

```bash
pip install -e .
pytest

python scripts/run_capacity.py --config small
python scripts/run_openendedness.py --num-worlds 50000 --train-sizes 100 300 1000 3000 10000 --depth-train-max 2 --depth-test 3 4 5 --seed 42
python scripts/run_fld_sanity.py --num-examples 20000 --max-proof-depth 5 --seed 42
python scripts/run_negative_control.py --num-examples 20000 --seed 42
```

Then send back:

```text
outputs/capacity_summary.json
outputs/openendedness_summary.json
outputs/kolmogorov_diagnostics.json
outputs/fld_sanity_summary.json
outputs/negative_control_summary.json
all PNG plots
```
