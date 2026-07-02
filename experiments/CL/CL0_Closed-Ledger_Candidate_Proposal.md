# CL0: Closed-Ledger Candidate Proposal

**To:** Codex
**From:** Kirill / analyst
**Task type:** narrow substrate-search gate, not playbook development
**Status:** pre-constructive probe
**Do not name any framework. Do not open a new research programme.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest weakened form:

> Train an LLM / learner inside a **safe boundary** so that the model does not observe collapse-trajectories; safety comes from domain filtering even if the content inside the boundary is generalized rather than fully derived.

Every step must pass the parallel-reality test:

> “We are doing this to obtain a safe / derivable substrate for LLMs, and this step leads there by…”

If the honest ending is “because this is an interesting synthesis / CEGIS / DSL / methodology problem,” stop and mark the step as goal drift.

---

## 1. Task objective

Run **CL0 — Closed-Ledger Candidate Proposal**.

Your job is NOT to build a general “substrate generator.”

Your job is to test a much weaker claim:

> Can the current closed-direction ledger produce **one minimal candidate substrate family** that is explicitly constrained by prior negative results and is immediately testable by a kill-gate?

The output must be either:

1. **PASS-CANDIDATE:** one candidate substrate family + one pre-registered kill-gate; or
2. **NO-CANDIDATE:** a clear explanation that the current ledger does not yet support even one candidate without importing untested theory.

Both outcomes are valid. A forced candidate is a failure.

---

## 2. What this task is NOT

Do NOT do any of the following:

* Do not write a general theory of substrate generation.
* Do not build a universal DSL for substrates.
* Do not study CEGIS / SyGuS / program synthesis as a new research branch.
* Do not claim the falsification playbook is a constructor.
* Do not present the method as transferable unless separately tested.
* Do not create a polished framework name.
* Do not make repo-destructive changes.
* Do not commit, delete, move, or rename files unless explicitly instructed by Kirill.
* Do not optimize for elegance, compression, or mathematical beauty.
* Do not treat “interesting formal object” as progress unless it serves the LLM substrate goal.

---

## 3. Required input files

Read the following if present. If a path is absent, report it in the “Missing inputs” section and continue with the available evidence.

### Method / discipline files

* `playbook_extraction/README.md`
* `playbook_extraction/SUMMARY.md`
* `playbook_extraction/01_method_from_practice.md`
* `playbook_extraction/02_extracted_method.md`
* `playbook_extraction/03_not_yet_method.md`
* `playbook_extraction/harness/output_schema.md`
* `playbook_extraction/harness/failure_conditions.md`
* `claude_code_task_ascesis_reorg_and_development.md`

### Closed-direction / substrate evidence files

Prefer a pre-existing ledger if present:

* `research/closed_directions_ledger.md`

If it is absent or incomplete, reconstruct only the minimal ledger entries needed for this task from available evidence, especially:

* `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md`
* `research/faithful_abstraction_v1/01_empirical_basis.md`
* `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md`
* `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md`
* `experiments/BA/BA4_layer_audit/justitia_layer_audit.md`
* `experiments/15_collapse_boundary/outputs_15_2/summary.md`
* `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md`
* `experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json`
* `experiments/JB/18_1_shielded_training/claude_code_task_18_1_shielded_training.md`

Do not treat summaries as proof of transfer. Use them only as evidence of what was killed and what durable constraint survived.

---

## 4. Required output file

Write exactly one main report:

```text
playbook_extraction/CL0_closed_ledger_candidate_proposal.md
```

Optionally, if you formulate a candidate kill-gate, also write:

```text
playbook_extraction/CL0_preregistration.json
```

Do not modify existing project files except for these new CL0 output files.

---

## 5. Required report structure

The report must use the following exact sections.

# CL0 — Closed-Ledger Candidate Proposal

## 0. Verdict

One of:

* `PASS-CANDIDATE`
* `NO-CANDIDATE`
* `HALT-GOAL-DRIFT`
* `HALT-MISSING-EVIDENCE`

Include a one-paragraph reason.

## 1. Goal anchor

Restate the immutable goal in your own words.

Then complete this sentence:

> “This CL0 step serves the safe / derivable substrate goal by…”

If the completion is not direct and concrete, set verdict to `HALT-GOAL-DRIFT`.

## 2. Inputs used

List every file used.

For each file, mark it as:

* `EVIDENCE`
* `METHOD`
* `SUMMARY`
* `CONTEXT`
* `MISSING`

Implicit inputs are forbidden.

## 3. Closed-direction ledger extracted for CL0

Create a compact table:

| killed direction | evidence file | failure mode | durable constraint for future candidates |
| ---------------- | ------------- | ------------ | ---------------------------------------- |

Include at least these families if evidence is available:

* Justitia / Door-1 failure
* Standard CEGAR boundary
* FA compression / coverage proxy failure
* BA projection / layer simplification failure
* 15.2 free-monoid / noisy-TV / count-open caveat
* 18.1 shield false-safe / projection-blindness failure

Do not over-interpret. If a constraint is an inference, label it `INFERENCE`.

## 4. Candidate proposal attempt

Try to propose exactly one minimal candidate substrate family.

The candidate must be described as:

```text
Candidate family:
Core objects:
Transition / inference rule:
Boundary / shield relation:
Observation available to learner:
Why world-model content would be derived or safer:
Which closed-direction constraints it explicitly avoids:
```

If you cannot fill these fields without inventing unsupported theory, do not force the candidate. Set verdict to `NO-CANDIDATE`.

## 5. Existing-theory reduction check

Briefly check whether the proposed candidate is merely a known class in disguise, such as:

* ordinary CEGAR;
* ordinary WSTS;
* grammar-guided synthesis;
* program synthesis / SyGuS / CEGIS;
* ordinary shielded learning.

This is only a reduction check, not a literature review.

If the candidate is just a known class and has no specific relation to safe / derivable LLM substrate, set verdict to `HALT-GOAL-DRIFT` or `NO-CANDIDATE`.

## 6. Bought-by-simplification check

State what the candidate abstraction discards.

Mandatory questions:

* What variables are projected away?
* Could the projected-away variables contain collapse / unsafe information?
* Could the boundary be trivially safe but useless?
* Could the candidate achieve decidability by removing the meaningful structure?
* Could it create compression without discrimination?

If this section is vague, set verdict to `NO-CANDIDATE`.

## 7. Pre-registered kill-gate

If a candidate exists, define exactly one kill-gate.

Required fields:

```text
Question:
Metric:
Threshold:
Ground truth / oracle:
Positive controls:
Negative controls:
Trivially-safe baseline:
Equal-volume or equal-budget condition:
Decision vocabulary:
Downstream halt rule:
```

The threshold must be justified before measurement.

If no threshold can be justified, set verdict to `NO-CANDIDATE`.

## 8. What would count as failure?

List concrete failure conditions.

At minimum include:

* candidate repeats a closed direction;
* candidate is safe only by being vacuous;
* candidate compresses but does not discriminate;
* candidate requires hidden collapse information;
* candidate relies on a projection that can hide false-safe states;
* candidate cannot be killed by the proposed gate;
* candidate does not serve the LLM substrate goal.

## 9. What was NOT shown

Mandatory even if the verdict is `PASS-CANDIDATE`.

State explicitly:

* no claim that the candidate works;
* no claim that the candidate is a substrate;
* no claim that the learner derives a world-model yet;
* no claim that the method is now constructive in general;
* no claim that a general substrate generator exists;
* no claim that the playbook is transferable.

## 10. Durable result

If `PASS-CANDIDATE`:

State the exact next experiment to run and what would halt it.

If `NO-CANDIDATE`:

State the exact missing evidence or formal interface needed before another candidate proposal attempt.

If `HALT-GOAL-DRIFT`:

State which step drifted and why.

If `HALT-MISSING-EVIDENCE`:

State which missing files blocked the task.

---

## 6. Pre-registered pass/fail bar for CL0

This task passes only if the output is one of the following:

### Pass form A — useful candidate

The report produces one candidate substrate family that:

1. explicitly serves the safe / derivable LLM substrate goal;
2. cites the closed-direction constraints it avoids;
3. has a pre-registered kill-gate;
4. includes controls and a trivially-safe baseline;
5. includes a downstream halt rule;
6. includes “what was NOT shown”;
7. does not require a new general theory of substrate generation.

### Pass form B — useful negative

The report refuses to produce a candidate and explains exactly why the current ledger is insufficient.

This is a valid success if the refusal is specific and produces a durable constraint or missing-interface requirement.

### Failure forms

The task fails if any of these happen:

* It produces a literature review instead of a candidate or refusal.
* It develops “substrate generator” as a new project goal.
* It introduces a broad DSL before a candidate exists.
* It claims constructive progress without a kill-gate.
* It treats compression / elegance as evidence.
* It ignores the closed-direction ledger.
* It omits controls.
* It omits the trivially-safe baseline.
* It omits “what was NOT shown.”
* It cannot complete the parallel-reality sentence.
* It silently patches missing evidence with speculation.

---

## 7. Style requirements

Use the project’s evidence discipline:

* `FACT`
* `INFERENCE`
* `HYPOTHESIS`
* `RECOMMENDATION`

Do not blur these.

Prefer short tables over prose when listing evidence and constraints.

Every nontrivial claim must point to a repo file.

Do not hide uncertainty.

Do not make the result look stronger than it is.

---

## 8. Final instruction

The most valuable outcome is not a clever candidate.

The most valuable outcome is an honest boundary:

> either “the ledger is strong enough to propose one candidate under kill-gate,”
> or “the ledger is not yet constructive; here is exactly what is missing.”

Do not optimize for success. Optimize for survival under criticism.
