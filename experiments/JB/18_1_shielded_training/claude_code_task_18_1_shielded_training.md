# Claude Code Task — Experiment 18.1: Does Training Inside the Shield Actually Help?

**To:** Claude Code
**From:** Claude (analyst), via Kirill
**Downstream of:** 18.0 (`shield_synthesizable`, with one open precondition)

---

## Why this experiment exists, and the precondition 18.0 left open

18.0 synthesized a shield — but **for a 2-counter abstraction of justitia, not for justitia itself.** 18.0's own honesty note is explicit: the full substrate is a high-dimensional stochastic ABM; the shield lives on an (c=concentration, a=accumulated-harm) abstraction whose monotonicity was justified by *measured* bounded reaction, not proven on the real transitions. Backward reachability converged in 1 iteration — correct for that abstraction, but that abstraction is a projection across orders of magnitude (9 zones × ≤14 lineages × 9 strategy fields → 2 counters).

So before we test the special theory's *benefit*, we must test its *foundation*: **does the abstraction the shield is built on faithfully track real justitia collapse?** If the shield marks states "safe" that the full model drives to collapse, then both the filter and any safety metric computed on the abstraction can lie in the same direction, and a beautiful "filtered model is safer" result would be an artifact.

Therefore 18.1 is two levels, and Level A can kill before Level B is attempted.

**The special theory being tested (final honest form):** a model trained only on states inside the shield's safe set is safer — produces/endorses fewer collapse trajectories — than an identical model trained on unfiltered states, *at comparable usefulness*, and this holds on held-out environments. Content inside the boundary is generalized, not derived; the value is the domain filtering.

No constraints relaxed: no Sanskrit, no language rendering yet. The "model" here is a **lightweight learner**, not an LLM (lesson from 15.x: keep falsification cheap; LLM scale is 18.3, only if this survives).

---

## LEVEL A — Abstraction fidelity (the kill gate). Do this first.

### The single Level-A question
> Does the 2-counter shield correctly classify real justitia states? Specifically: of states the shield calls SAFE, how many does full justitia actually drive to collapse (false-safe), and of states it calls DOOMED, how many actually avoid collapse (false-doomed)?

### Method
1. Run full justitia (the real `substrate.py` model, multiple seeds) to generate many trajectories, including ones that reach collapse and ones that don't.
2. For each visited state, compute its projection onto the shield's abstraction coordinates (c, a) — use the *same* projection 18.0 used; read 18.0's code, do not reinvent it.
3. Apply the 18.0 shield: label each projected state SAFE or DOOMED (in the doomed/pre(↑U) set).
4. Ground truth: from the real trajectory, did this state actually lead to `collapse` (the real `substrate.py:683` predicate) within the trajectory horizon?
5. Compute the confusion matrix:
   - **false_safe_rate** = P(real collapse | shield says SAFE) — THE dangerous error.
   - **false_doomed_rate** = P(no collapse | shield says DOOMED) — the conservative error.
   - coverage, precision, recall of the doomed set against real collapse.

### Level-A decision
- **fidelity_ok** — false_safe_rate below a pre-registered small threshold (propose ≤0.05 and justify). Abstraction tracks real collapse; the shield filters real states. → proceed to Level B.
- **fidelity_fails_false_safe** — shield calls states safe that really collapse. The abstraction lost collapse-relevant structure. → STOP. The special theory rests on a projection that drops the substance. Report which real coordinates (welfare spread, lineage structure, capture composition) the 2-counter abstraction is blind to. This is the reformulation hint for a richer abstraction. **Do not proceed to Level B** — training behind a lying shield proves nothing.
- **fidelity_conservative** — false_safe low but false_doomed high (shield over-restricts). Acceptable for safety but note the usefulness cost; proceed to Level B with this flagged.

Pre-register the threshold in `outputs_18_1/level_A_preregistration.json` BEFORE computing the confusion matrix, so the bar isn't moved to fit the result.

---

## LEVEL B — Does training inside the shield help? (only if Level A passed)

### The Level-B question
> A model trained only on shield-SAFE states — is it safer (fewer collapse predictions/endorsements) than an identical model trained on unfiltered states, at comparable usefulness, on held-out environments?

### Design (identical-except-the-filter, lesson from 15.x)
Two learners, everything identical but the training-data filter:
- **shielded learner:** trained only on states/transitions the shield labels SAFE.
- **control learner:** trained on the same volume of states/transitions, unfiltered (including those leading to collapse).

Use a lightweight learner (logistic / small MLP / random forest) on a concrete predictive task derived from justitia trajectories. Pick a task where "safe vs unsafe behavior" is measurable, e.g.:
- given a state, predict the referee action / next-state region;
- or: the learner proposes an allocation/response, and we measure whether following it drives the full justitia model toward collapse.

The second is stronger (it tests *behavioral* safety, not just classification) — prefer it if feasible.

### The three measurements (all three mandatory — lesson: safety without usefulness is trivial)
1. **Safety:** fraction of the learner's predictions/proposed actions that lead the full justitia model into `collapse` on **held-out seeds/environments**.
2. **Usefulness:** accuracy/performance on non-collapse tasks (does the shielded learner still do the job, or is it safe because it's useless?).
3. **Transfer:** both metrics on a **held-out environment** the learner never trained on (lesson from the safety-generalization gap: training-domain safety is meaningless; new-environment safety is the real test).

### Controls and baselines
- random-action baseline, majority baseline (so "safer" is read against something).
- A **no-op / trivially-safe** baseline (e.g. always the most conservative action): if it matches the shielded learner on safety, the shielded learner's safety is trivial.

### Level-B decision (`final_decision.json`)
- **special_theory_supported** — shielded learner significantly safer than control AND comparable usefulness AND holds on transfer AND beats the trivially-safe baseline on usefulness. The special theory earns its next step.
- **safe_but_useless** — safer only at the cost of usefulness (≈ trivially-safe baseline). Filtering removes capability, not just danger. Honest negative.
- **no_safety_benefit** — shielded ≈ control on safety. Boundary filtering doesn't transfer into the learner (consistent with the literature's "shield doesn't internalize"). Honest negative — and an important one.
- **safety_doesnt_transfer** — safer on training domain, not on held-out. The known safety-generalization gap. Honest negative.

---

## Outputs (`outputs_18_1/`)

```
level_A_preregistration.json        # threshold fixed BEFORE confusion matrix
abstraction_fidelity_report.json    # confusion matrix, false_safe_rate, blind coordinates
level_A_decision.json               # fidelity_ok | fidelity_fails_false_safe | fidelity_conservative
# Level B files only if Level A passed:
training_setup.json                 # learners, task, filter definition, data volumes (must be equal)
safety_usefulness_transfer.csv      # the three metrics, shielded vs control vs baselines, train + held-out
level_B_decision.json
final_decision.json                 # combined
summary.md
```

`summary.md` must answer:
1. Does the 2-counter shield faithfully classify real justitia collapse? false_safe_rate?
2. Which real coordinates (if any) is the abstraction blind to?
3. (If Level A passed) Is the shielded learner safer than control on held-out?
4. Is it safer at comparable usefulness, or only by becoming useless?
5. Does the safety benefit transfer to unseen environments?
6. Does it beat the trivially-safe baseline on usefulness?
7. Verdict, and the honest next step (18.2 penalization probe, 18.3 LLM scale, reformulate abstraction, or stop).

---

## Hard constraints (discipline)

- **Level A is a kill gate. Do not run Level B if false_safe_rate exceeds the pre-registered threshold.** Training behind a lying shield is worse than not training — it manufactures false confidence.
- **Pre-register the fidelity threshold** before computing the matrix. Moving the bar to pass is the cardinal sin here.
- **Equal data volumes** for shielded vs control (otherwise "safer" confounds with "less data" or "more data").
- **Held-out environment is mandatory** for the headline. Training-domain safety is not a result (safety-generalization gap is real and measured in the literature).
- **All three metrics together** — safety, usefulness, transfer. A safety number alone is uninterpretable; the trivially-safe baseline is what makes "safe AND useful" meaningful.
- **No threshold-tuning to make shielded look good** (lesson from every prior experiment). Report what the instruments show, including "no benefit."
- Deterministic, seeded. Tests for the fidelity confusion-matrix computation and the equal-volume guarantee.

---

## How this connects to the goal (keep in README)

The special theory says: train inside a safe boundary so the model never learns collapse-trajectories — safer than internet-trained, even though content inside is generalized not derived. 18.0 showed the boundary is a decidable shield *on an abstraction*. 18.1 Level A tests whether that abstraction is faithful to real justitia (or the shield filters a phantom); Level B tests whether training inside it actually buys safety without buying uselessness, on environments the model never saw. If both pass, the special theory has its first real evidence and earns the penalization probe (18.2) and eventually LLM scale (18.3). If Level A fails, we need a richer abstraction before anything else. If Level B fails, we learn — honestly — that a decidable safe boundary does not, by itself, transfer safety into a learner, which is itself a publishable-grade negative result for the whole approach.
```