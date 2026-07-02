# Codex Task — CL1: Minimal Lawful Domain Boundary-Fidelity Pilot

**To:** Codex
**From:** Kirill / analyst
**Task type:** executable boundary-fidelity pilot
**Status:** continuation of CL0, not a substrate claim
**Do not name any framework. Do not open a new research programme.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest weakened form:

> Train an LLM / learner inside a **safe boundary** so the learner does not observe collapse-trajectories; safety comes from domain filtering even if content inside the boundary is still generalized rather than fully derived.

Every step must pass the parallel-reality test:

> “We are doing this to obtain a safe / derivable substrate for LLMs, and this step leads there by…”

If the honest ending is “because this is an interesting toy domain / CEGIS / DSL / methodology problem,” stop and set verdict to `HALT-GOAL-DRIFT`.

---

## 1. Why CL1 exists

CL0 produced a weakened candidate:

> a layer-audited safe-transition ledger over a generated lawful domain, with pre-registered false-safe and non-vacuity gates.

CL0 did **not** produce a substrate.
CL0 did **not** show learner derivation.
CL0 did **not** justify learner training.

Therefore CL1 must test only the next precondition:

> Can we instantiate one minimal generated lawful domain with full transition semantics, collapse ground truth, learner-visible observations, and a boundary rule, then run the CL0 fidelity/non-vacuity gate without overclaiming?

---

## 2. Task objective

Run **CL1 — Minimal Lawful Domain Boundary-Fidelity Pilot**.

Your job is to create and execute one minimal pilot experiment that tests whether the CL0 boundary protocol can be implemented without repeating known failure modes.

The output must be one of:

1. `BOUNDARY-FIDELITY-OK`
2. `BOUNDARY-FAILS-FALSE-SAFE`
3. `BOUNDARY-CONSERVATIVE-BUT-VACUOUS`
4. `INCONCLUSIVE-MISSING-GROUND-TRUTH`
5. `HALT-GOAL-DRIFT`

All five outcomes are valid. A failed boundary is useful evidence.

---

## 3. What this task is NOT

Do NOT do any of the following:

* Do not claim a substrate has been found.
* Do not claim world-model derivation.
* Do not train an LLM.
* Do not run learner training downstream of a failed boundary gate.
* Do not write a general substrate generator.
* Do not build a universal DSL.
* Do not study CEGIS / SyGuS / program synthesis as a topic.
* Do not repair Justitia as a Door-1 candidate.
* Do not optimize for elegance or compression.
* Do not treat a toy domain as progress unless it tests the CL0 safety boundary.
* Do not modify, move, delete, stage, or commit existing project files.

---

## 4. Required input files

Read these files if present:

```text
playbook_extraction/CL0_closed_ledger_candidate_proposal.md
playbook_extraction/CL0_preregistration.json
playbook_extraction/02_extracted_method.md
playbook_extraction/03_not_yet_method.md
playbook_extraction/harness/output_schema.md
playbook_extraction/harness/failure_conditions.md
research/closed_directions_ledger.md
research/door1_postmortem/Door1_Extracted_Knowledge_v1.md
research/faithful_abstraction_v1/01_empirical_basis.md
experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md
experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md
experiments/BA/BA4_layer_audit/justitia_layer_audit.md
experiments/15_collapse_boundary/outputs_15_2/summary.md
experiments/JB/18_1_shielded_training/outputs_18_1/summary.md
experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json
experiments/JB/18_1_shielded_training/claude_code_task_18_1_shielded_training.md
```

If some files are absent, list them as `MISSING` and continue only if CL0 outputs and enough closed-direction evidence are present.

---

## 5. Allowed output files

Create a new experiment directory only:

```text
experiments/CL/CL1_boundary_fidelity_pilot/
```

Inside it, create:

```text
SPEC.md
CL1_preregistration.json
domain.py
boundary.py
run_cl1.py
outputs/metrics.json
outputs/decision.json
outputs/final_report.md
outputs/false_safe_witnesses.json
outputs/false_positive_witnesses.json
outputs/layer_audit.md
```

Do not edit existing files outside this directory.

---

## 6. Required experiment design

CL1 has two phases.

---

# Phase A — Pre-registration before measurement

Before computing final metrics, write:

```text
experiments/CL/CL1_boundary_fidelity_pilot/CL1_preregistration.json
```

It must contain:

```json
{
  "gate": "CL1",
  "inherits_from": "playbook_extraction/CL0_preregistration.json",
  "domain_name": "...",
  "domain_rationale": "...",
  "horizon": "...",
  "random_seed": "...",
  "state_space_description": "...",
  "transition_semantics": "...",
  "collapse_predicate": "...",
  "learner_visible_observation": "...",
  "boundary_rule": "...",
  "layer_eligible_coordinates": [],
  "forbidden_boundary_coordinates": [],
  "metrics": {
    "false_safe_rate": "...",
    "already_collapsed_labeled_safe_rate": "...",
    "false_positive_rate": "...",
    "equal_volume_possible": "..."
  },
  "thresholds": {
    "false_safe_rate_max": 0.05,
    "already_collapsed_labeled_safe_rate_max": 0.0,
    "false_positive_rate_max": 0.20,
    "equal_volume_required": true
  },
  "decision_vocabulary": [
    "BOUNDARY-FIDELITY-OK",
    "BOUNDARY-FAILS-FALSE-SAFE",
    "BOUNDARY-CONSERVATIVE-BUT-VACUOUS",
    "INCONCLUSIVE-MISSING-GROUND-TRUTH",
    "HALT-GOAL-DRIFT"
  ],
  "downstream_halt_rule": "No learner training, no LLM scaling, and no derivability claim unless decision is BOUNDARY-FIDELITY-OK."
}
```

The report must attest that this file was written before final metric computation. Do not move thresholds after seeing results.

---

# Phase B — Execute the gate

Implement and run a minimal generated lawful domain.

The domain must satisfy all requirements below.

## 6.1 Domain requirements

The domain must be generated, executable, and lawful:

```text
state_t+1 = transition(state_t, action_t, exogenous_t)
```

It must include:

1. explicit full state;
2. explicit transition rule;
3. explicit action or intervention space;
4. explicit learner-visible observation;
5. explicit hidden audit-only collapse predicate;
6. at least one non-collapse trajectory family;
7. at least one collapse-bound trajectory family;
8. a horizon fixed before measurement;
9. enough states/transitions to test both false-safe and false-positive errors.

The domain may be synthetic. Synthetic is acceptable only if it is used as an adversarial pilot for boundary fidelity, not as a substrate claim.

## 6.2 Non-degeneracy requirements

The domain must not be trivially separable by a single reporting metric.

It must contain at least two distinct collapse mechanisms, for example:

```text
local failed-zone / spread-like mechanism
global mass / resource-like mechanism
```

The exact mechanisms may differ, but the domain must be capable of reproducing the lesson of 18.1:

> a projection that omits a collapse-relevant coordinate can label collapse-bound states SAFE.

If the domain cannot produce false-safe witnesses under a deliberately projection-blind baseline, mark the experiment `INCONCLUSIVE-MISSING-GROUND-TRUTH` or redesign before final measurement.

## 6.3 Layer audit requirements

Produce:

```text
outputs/layer_audit.md
```

For every coordinate used by the boundary, classify its role:

```text
DYNAMICS
POLICY / CONTROL
OBSERVATION
PROJECTION
REPORTING
AUDIT-ONLY
```

Rules:

* `AUDIT-ONLY` collapse labels and future outcomes may not be learner-visible.
* `REPORTING` metrics may not be used as boundary evidence unless justified as dynamics/policy/observation relevant.
* Any projected-away coordinate must be listed.
* Any coordinate whose omission could hide collapse must be listed as a risk.

---

## 7. Boundary rules and controls

Implement at least these boundary variants:

## 7.1 Candidate boundary

A layer-audited boundary that uses only allowed coordinates and predicts:

```text
SAFE(state) = no collapse within horizon according to the boundary rule
DOOMED(state) = collapse possible / likely within horizon according to the boundary rule
```

The candidate boundary must not use future collapse labels directly.

## 7.2 Projection-blind baseline

A deliberately weaker boundary that omits at least one known collapse-relevant coordinate.

Purpose:

> ensure the experiment can detect 18.1-style projection blindness.

If this baseline does not create worse false-safe behaviour than the candidate, explain why.

## 7.3 Trivially-safe baseline

A baseline that classifies all states as `DOOMED`.

Purpose:

> detect whether the candidate is merely safe by admitting nothing.

## 7.4 Unfiltered control

A control ledger with no boundary filtering.

Purpose:

> test whether shielded and unfiltered ledgers can be sampled under equal volume or equal budget.

---

## 8. Metrics

Compute these metrics on a held-out evaluation set or exhaustive state set.

## 8.1 Primary dangerous error

```text
false_safe_rate =
P(full collapse within horizon | boundary says SAFE)
```

Fail if:

```text
false_safe_rate > 0.05
```

## 8.2 Purity failure

```text
already_collapsed_labeled_safe_rate =
P(boundary says SAFE | state is already collapsed)
```

Fail if:

```text
already_collapsed_labeled_safe_rate > 0
```

## 8.3 Non-vacuity

```text
false_positive_rate =
P(boundary says DOOMED | full trajectory remains SAFE)
```

Fail as conservative-but-vacuous if:

```text
false_positive_rate > 0.20
```

## 8.4 Equal-volume / equal-budget condition

Check whether a shielded training ledger and unfiltered control ledger can be sampled with equal number of transitions or equal fixed collection budget.

Fail as conservative-but-vacuous if this is impossible.

---

## 9. Decision rule

Use exactly this decision rule:

```text
BOUNDARY-FIDELITY-OK
iff
false_safe_rate <= 0.05
AND already_collapsed_labeled_safe_rate == 0
AND false_positive_rate <= 0.20
AND equal_volume_possible == true
```

```text
BOUNDARY-FAILS-FALSE-SAFE
iff
false_safe_rate > 0.05
OR already_collapsed_labeled_safe_rate > 0
```

```text
BOUNDARY-CONSERVATIVE-BUT-VACUOUS
iff
false_safe_rate <= 0.05
AND already_collapsed_labeled_safe_rate == 0
AND (
  false_positive_rate > 0.20
  OR equal_volume_possible == false
)
```

```text
INCONCLUSIVE-MISSING-GROUND-TRUTH
iff
full transition semantics, collapse predicate, horizon, or evaluation set is unavailable / degenerate
```

```text
HALT-GOAL-DRIFT
iff
the experiment becomes about a toy domain, DSL, CEGIS, synthesis, or methodology rather than testing a safety precondition for LLM substrate training
```

---

## 10. Required outputs

## 10.1 `outputs/metrics.json`

Must contain:

```json
{
  "candidate_boundary": {
    "false_safe_rate": null,
    "already_collapsed_labeled_safe_rate": null,
    "false_positive_rate": null,
    "equal_volume_possible": null
  },
  "projection_blind_baseline": {
    "false_safe_rate": null,
    "already_collapsed_labeled_safe_rate": null,
    "false_positive_rate": null
  },
  "trivially_safe_baseline": {
    "false_safe_rate": null,
    "already_collapsed_labeled_safe_rate": null,
    "false_positive_rate": null,
    "equal_volume_possible": null
  },
  "unfiltered_control": {
    "collapse_rate_within_horizon": null,
    "available_transition_count": null
  }
}
```

## 10.2 `outputs/decision.json`

Must contain:

```json
{
  "decision": "...",
  "reason": "...",
  "thresholds_used": {
    "false_safe_rate_max": 0.05,
    "already_collapsed_labeled_safe_rate_max": 0.0,
    "false_positive_rate_max": 0.20,
    "equal_volume_required": true
  },
  "downstream_allowed": false
}
```

Set `downstream_allowed: true` only if decision is `BOUNDARY-FIDELITY-OK`.

## 10.3 Witness files

Write:

```text
outputs/false_safe_witnesses.json
outputs/false_positive_witnesses.json
```

Each witness must include:

```json
{
  "state": "...",
  "observation": "...",
  "boundary_decision": "...",
  "full_outcome": "...",
  "collapse_mechanism": "...",
  "which_coordinate_or_projection_mattered": "..."
}
```

If no witnesses exist, write an empty list and explain in the final report.

## 10.4 Final report

Write:

```text
outputs/final_report.md
```

The report must contain exactly these sections:

```text
# CL1 — Minimal Lawful Domain Boundary-Fidelity Pilot

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. Domain specification
## 4. Layer audit summary
## 5. Pre-registration provenance
## 6. Metrics
## 7. Controls and baselines
## 8. Decision
## 9. Witness analysis
## 10. Bought-by-simplification check
## 11. What was NOT shown
## 12. Durable result
```

---

## 11. Mandatory “what was NOT shown”

Include this section even if CL1 passes.

State explicitly:

* no claim that this is a substrate;
* no claim that learner world-model content is derived;
* no claim that LLM training is safe;
* no claim that boundary fidelity transfers to other domains;
* no claim that a general substrate generator exists;
* no claim that the playbook is constructive in general;
* no claim that a toy domain itself is valuable outside this gate.

---

## 12. Halt-downstream rule

If the decision is not `BOUNDARY-FIDELITY-OK`, stop.

Do not run learner training.

Do not run representation analysis.

Do not make derivability claims.

The next step after failure is witness analysis:

```text
false-safe witnesses → projection/layer repair or candidate rejection
false-positive witnesses → vacuity analysis or candidate rejection
missing ground truth → domain redesign
goal drift → abandon CL1 path
```

---

## 13. Pass/fail bar for the Codex task

The Codex task itself succeeds if it produces a complete CL1 report and a valid decision, even if the boundary fails.

The task fails if:

* no pre-registration JSON is written before metric computation;
* thresholds are changed after seeing results;
* no full transition semantics is implemented;
* no collapse predicate is defined;
* learner observations include hidden future collapse labels;
* no projection-blind baseline is included;
* no trivially-safe baseline is included;
* no equal-volume/equal-budget check is performed;
* no witness files are written;
* `what was NOT shown` is omitted;
* the report claims a substrate or derivable world-model;
* the work turns into DSL/CEGIS/meta-synthesis exploration.

---

## 14. Final instruction

The desired result is not “success.”

The desired result is a reliable boundary decision:

> either the candidate boundary is faithful and non-vacuous on one minimal lawful domain,
> or the experiment exposes exactly why it is unsafe, vacuous, under-specified, or drifting.

Optimize for survival under criticism, not for passing the gate.
