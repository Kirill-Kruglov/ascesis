# CL1.1: Action-Conditioned Safe Ledger Gate

**To:** Codex
**From:** Kirill / analyst
**Task type:** repair-gate after CL1
**Status:** action-conditioned safety ledger test
**Do not name any framework. Do not open a new research programme.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest weakened form:

> Train an LLM / learner inside a **safe boundary** so the learner does not observe collapse-trajectories; safety comes from domain filtering even if content inside the boundary is still generalized rather than fully derived.

Every step must pass the parallel-reality test:

> “We are doing this to obtain a safe / derivable substrate for LLMs, and this step leads there by…”

If the honest ending is “because this is an interesting policy-synthesis / planning / CEGIS / DSL / toy-domain problem,” stop and set verdict to `HALT-GOAL-DRIFT`.

---

## 1. Why CL1.1 exists

CL1 produced a useful state-level boundary-fidelity result on `FourZoneMassDomain`.

However, CL1 also exposed a boundary / ledger mismatch:

```text
CL1 checked:
SAFE(state) under deterministic safety-policy rollout.

But learner ledger needs:
SAFE(state, action) for admitted observations, actions/interventions, and consequences.
```

A learner-training ledger is made of transitions, not only source states.

Therefore CL1.1 must test the next precondition:

> Can we construct an action-conditioned safe transition ledger, where each admitted `(state, action, next_state)` transition is safe under the full collapse oracle and non-vacuous enough for equal-volume learner training?

CL1.1 does **not** test learner derivation.
CL1.1 does **not** train a learner.
CL1.1 does **not** claim a substrate.
CL1.1 only decides whether CL1’s state-level boundary can be repaired into a transition-level safe ledger.

---

## 2. Task objective

Run **CL1.1 — Action-Conditioned Safe Ledger Gate**.

Your job is to create and execute one repair experiment that evaluates safety over `(state, action)` pairs, not only over states.

The output must be one of:

1. `ACTION-LEDGER-OK`
2. `ACTION-LEDGER-FAILS-UNSAFE-ADMISSION`
3. `ACTION-LEDGER-CONSERVATIVE-BUT-VACUOUS`
4. `ACTION-LEDGER-INCONCLUSIVE-MISSING-GROUND-TRUTH`
5. `HALT-GOAL-DRIFT`

All five outcomes are valid. A failed action ledger is useful evidence.

---

## 3. What this task is NOT

Do NOT do any of the following:

* Do not claim substrate discovery.
* Do not claim world-model derivation.
* Do not train a learner.
* Do not train or scale an LLM.
* Do not run representation analysis.
* Do not introduce a new domain unless the CL1 domain is unusable and you explicitly justify `INCONCLUSIVE-MISSING-GROUND-TRUTH`.
* Do not write a general policy-synthesis method.
* Do not build a universal DSL.
* Do not study CEGIS / SyGuS / program synthesis as a topic.
* Do not optimize for elegance, compression, or policy optimality.
* Do not treat “many safe transitions” as evidence of derivability.
* Do not modify, move, delete, stage, or commit existing project files.

---

## 4. Required input files

Read these files if present:

```text
experiments/CL/CL1_boundary_fidelity_pilot/SPEC.md
experiments/CL/CL1_boundary_fidelity_pilot/CL1_preregistration.json
experiments/CL/CL1_boundary_fidelity_pilot/domain.py
experiments/CL/CL1_boundary_fidelity_pilot/boundary.py
experiments/CL/CL1_boundary_fidelity_pilot/run_cl1.py
experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json
experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json
experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md
experiments/CL/CL1_boundary_fidelity_pilot/outputs/layer_audit.md
playbook_extraction/CL0_closed_ledger_candidate_proposal.md
playbook_extraction/CL0_preregistration.json
playbook_extraction/02_extracted_method.md
playbook_extraction/03_not_yet_method.md
playbook_extraction/harness/output_schema.md
playbook_extraction/harness/failure_conditions.md
```

If some files are absent, list them as `MISSING`. Continue only if CL1 domain code, CL1 metrics, and CL0/CL1 pre-registration evidence are available.

---

## 5. Allowed output files

Create a new experiment directory only:

```text
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/
```

Inside it, create:

```text
SPEC.md
CL1_1_preregistration.json
action_boundary.py
run_cl1_1.py
outputs/metrics.json
outputs/decision.json
outputs/final_report.md
outputs/unsafe_admitted_witnesses.json
outputs/false_positive_action_witnesses.json
outputs/layer_audit_delta.md
```

You may import or copy the CL1 domain module for reproducibility, but do not edit CL1 files.

Do not edit existing files outside the CL1.1 directory.

---

## 6. Required repair hypothesis

CL1.1 tests exactly this hypothesis:

```text
H1:
A state-level SAFE boundary is insufficient for a learner ledger unless each admitted action transition is also safe.
```

The candidate action-conditioned admission rule must be:

```text
ADMIT(state, action) = true
iff
1. state is not already collapsed;
2. transition(state, action) is not already collapsed;
3. rollout from transition(state, action), under the declared continuation policy,
   remains non-collapse for horizon - 1;
4. action and successor are learner-visible only as ordinary transition data;
5. no collapse label, future outcome label, or witness class is used as learner input.
```

The continuation policy may be CL1’s deterministic safety policy. If so, state clearly:

```text
CL1.1 tests one-step action admission followed by safety-policy continuation.
It does not prove safety under arbitrary future learner actions.
```

Do not silently strengthen this to “all future actions are safe” unless you actually test all future action branches.

---

## 7. Phase A — Pre-registration before measurement

Before computing final metrics, write:

```text
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json
```

It must contain:

```json
{
  "gate": "CL1.1",
  "inherits_from": [
    "playbook_extraction/CL0_preregistration.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/CL1_preregistration.json"
  ],
  "repair_reason": "CL1 checked SAFE(state) under safety-policy rollout but counted admitted transitions as if all actions from SAFE states were admissible.",
  "domain_name": "FourZoneMassDomain",
  "horizon": 6,
  "state_action_space_description": "...",
  "transition_semantics": "...",
  "collapse_predicate": "...",
  "learner_visible_transition": "...",
  "candidate_admission_rule": "...",
  "continuation_policy": "...",
  "forbidden_admission_inputs": [
    "future_collapse_label",
    "collapse_mechanism_label",
    "already_collapsed_label_as_input",
    "trajectory_outcome_label",
    "post_hoc_witness_class",
    "reporting_only_safe_count"
  ],
  "metrics": {
    "unsafe_admitted_transition_rate": "P(full collapse within horizon after taking action | ADMIT(state, action) = true)",
    "already_collapsed_source_admitted_rate": "P(source state already collapsed | ADMIT(state, action) = true)",
    "already_collapsed_successor_admitted_rate": "P(successor state already collapsed | ADMIT(state, action) = true)",
    "false_positive_action_rate": "P(ADMIT(state, action) = false | action transition remains safe within horizon)",
    "equal_volume_possible": "Whether action-conditioned admitted ledger can match the declared minimum transition volume and unfiltered control budget"
  },
  "thresholds": {
    "unsafe_admitted_transition_rate_max": 0.05,
    "already_collapsed_source_admitted_rate_max": 0.0,
    "already_collapsed_successor_admitted_rate_max": 0.0,
    "false_positive_action_rate_max": 0.20,
    "equal_volume_required": true
  },
  "minimum_equal_volume_transitions": 500,
  "decision_vocabulary": [
    "ACTION-LEDGER-OK",
    "ACTION-LEDGER-FAILS-UNSAFE-ADMISSION",
    "ACTION-LEDGER-CONSERVATIVE-BUT-VACUOUS",
    "ACTION-LEDGER-INCONCLUSIVE-MISSING-GROUND-TRUTH",
    "HALT-GOAL-DRIFT"
  ],
  "downstream_halt_rule": "No learner training, no LLM scaling, and no derivability claim unless decision is ACTION-LEDGER-OK."
}
```

The report must attest that this file was written before final metric computation. Do not move thresholds after seeing results.

---

## 8. Phase B — Execute the action-conditioned gate

Use the CL1 `FourZoneMassDomain` unless unavailable.

Evaluate the exhaustive finite `(state, action)` set:

```text
for every state in all_states():
    for every action in ACTIONS:
        evaluate ADMIT(state, action)
```

For each pair, compute the full audit outcome:

```text
successor = transition(state, action)

unsafe if:
    source state already collapsed
    OR successor already collapsed
    OR rollout from successor under continuation_policy collapses within horizon - 1
```

The learner-visible transition is only:

```text
observation(state), action, observation(successor)
```

Collapse labels, future outcomes, collapse mechanisms, and witness classes are audit-only.

---

## 9. Required boundary/admission variants

Implement at least these variants.

## 9.1 Candidate action-conditioned admission

The repaired candidate:

```text
ADMIT_CANDIDATE(state, action)
```

This must evaluate safety for the actual `(state, action)` pair, not only the source state.

## 9.2 CL1 state-level carryover baseline

A baseline that reproduces the CL1 mismatch:

```text
ADMIT_CL1_STATE_LEVEL(state, action) = true
iff
CL1_candidate_boundary(state) == SAFE
```

This baseline is expected to expose unsafe admitted actions if the mismatch is real.

## 9.3 Projection-blind action baseline

A baseline that uses projection-blind state information, such as mean zone health only, and admits actions from states it marks SAFE.

Purpose:

> detect projection blindness at the action-ledger level.

## 9.4 Trivially-safe action baseline

A baseline that admits no actions.

Purpose:

> detect safety bought by vacuity.

## 9.5 Unfiltered action control

A control ledger containing all `(state, action)` pairs.

Purpose:

> establish the unfiltered unsafe-transition rate and total available transition budget.

---

## 10. Metrics

Compute metrics on the exhaustive `(state, action)` set.

## 10.1 Primary dangerous error

```text
unsafe_admitted_transition_rate =
P(full collapse within horizon after taking action | ADMIT(state, action) = true)
```

Fail if:

```text
unsafe_admitted_transition_rate > 0.05
```

## 10.2 Source purity

```text
already_collapsed_source_admitted_rate =
P(source state already collapsed | ADMIT(state, action) = true)
```

Fail if:

```text
already_collapsed_source_admitted_rate > 0
```

## 10.3 Successor purity

```text
already_collapsed_successor_admitted_rate =
P(successor state already collapsed | ADMIT(state, action) = true)
```

Fail if:

```text
already_collapsed_successor_admitted_rate > 0
```

## 10.4 Non-vacuity / action discrimination

```text
false_positive_action_rate =
P(ADMIT(state, action) = false | action transition remains safe within horizon)
```

Fail as conservative-but-vacuous if:

```text
false_positive_action_rate > 0.20
```

## 10.5 Equal-volume / equal-budget condition

Check whether the action-conditioned admitted ledger can provide at least the pre-registered minimum number of transitions and can be matched by the unfiltered control under equal transition count or equal budget.

Fail as conservative-but-vacuous if equal volume is impossible.

## 10.6 Baseline sensitivity

Report the same dangerous-error and non-vacuity metrics for:

```text
CL1 state-level carryover baseline
projection-blind action baseline
trivially-safe action baseline
unfiltered action control
```

The CL1 state-level carryover baseline must be able to expose the mismatch. If it does not, explain why the suspected mismatch was not reproduced.

---

## 11. Decision rule

Use exactly this decision rule:

```text
ACTION-LEDGER-OK
iff
unsafe_admitted_transition_rate <= 0.05
AND already_collapsed_source_admitted_rate == 0
AND already_collapsed_successor_admitted_rate == 0
AND false_positive_action_rate <= 0.20
AND equal_volume_possible == true
```

```text
ACTION-LEDGER-FAILS-UNSAFE-ADMISSION
iff
unsafe_admitted_transition_rate > 0.05
OR already_collapsed_source_admitted_rate > 0
OR already_collapsed_successor_admitted_rate > 0
```

```text
ACTION-LEDGER-CONSERVATIVE-BUT-VACUOUS
iff
unsafe_admitted_transition_rate <= 0.05
AND already_collapsed_source_admitted_rate == 0
AND already_collapsed_successor_admitted_rate == 0
AND (
  false_positive_action_rate > 0.20
  OR equal_volume_possible == false
)
```

```text
ACTION-LEDGER-INCONCLUSIVE-MISSING-GROUND-TRUTH
iff
full transition semantics, collapse predicate, action space, horizon, or evaluation set is unavailable / degenerate
```

```text
HALT-GOAL-DRIFT
iff
the experiment becomes about policy optimization, planning, DSL, CEGIS, synthesis, or toy-domain exploration rather than testing safe transition-ledger admission for LLM substrate training
```

---

## 12. Required outputs

## 12.1 `outputs/metrics.json`

Must contain:

```json
{
  "domain": {
    "state_count": null,
    "action_count": null,
    "state_action_count": null,
    "horizon": null,
    "minimum_equal_volume_transitions": null
  },
  "candidate_action_ledger": {
    "admitted_transition_count": null,
    "rejected_transition_count": null,
    "unsafe_admitted_transition_rate": null,
    "already_collapsed_source_admitted_rate": null,
    "already_collapsed_successor_admitted_rate": null,
    "false_positive_action_rate": null,
    "equal_volume_possible": null
  },
  "cl1_state_level_carryover_baseline": {
    "admitted_transition_count": null,
    "unsafe_admitted_transition_rate": null,
    "already_collapsed_source_admitted_rate": null,
    "already_collapsed_successor_admitted_rate": null,
    "false_positive_action_rate": null
  },
  "projection_blind_action_baseline": {
    "admitted_transition_count": null,
    "unsafe_admitted_transition_rate": null,
    "already_collapsed_source_admitted_rate": null,
    "already_collapsed_successor_admitted_rate": null,
    "false_positive_action_rate": null
  },
  "trivially_safe_action_baseline": {
    "admitted_transition_count": null,
    "unsafe_admitted_transition_rate": null,
    "already_collapsed_source_admitted_rate": null,
    "already_collapsed_successor_admitted_rate": null,
    "false_positive_action_rate": null,
    "equal_volume_possible": null
  },
  "unfiltered_action_control": {
    "unsafe_transition_rate": null,
    "available_transition_count": null
  }
}
```

## 12.2 `outputs/decision.json`

Must contain:

```json
{
  "decision": "...",
  "reason": "...",
  "thresholds_used": {
    "unsafe_admitted_transition_rate_max": 0.05,
    "already_collapsed_source_admitted_rate_max": 0.0,
    "already_collapsed_successor_admitted_rate_max": 0.0,
    "false_positive_action_rate_max": 0.20,
    "equal_volume_required": true
  },
  "downstream_allowed": false
}
```

Set `downstream_allowed: true` only if decision is `ACTION-LEDGER-OK`.

## 12.3 Witness files

Write:

```text
outputs/unsafe_admitted_witnesses.json
outputs/false_positive_action_witnesses.json
```

Each unsafe admitted witness must include:

```json
{
  "state": "...",
  "action": "...",
  "successor": "...",
  "learner_visible_transition": "...",
  "admission_decision": "ADMIT",
  "full_outcome": "...",
  "collapse_mechanism": "...",
  "collapse_step_after_action": "...",
  "which_coordinate_policy_or_action_mattered": "..."
}
```

Each false-positive action witness must include:

```json
{
  "state": "...",
  "action": "...",
  "successor": "...",
  "learner_visible_transition": "...",
  "admission_decision": "REJECT",
  "full_outcome": "remains_safe_within_horizon",
  "collapse_mechanism": "none",
  "why_rejected": "..."
}
```

If no witnesses exist, write an empty list and explain in the final report.

## 12.4 `outputs/layer_audit_delta.md`

This file must explain what changed from CL1.

Required entries:

```text
- CL1 checked state-level SAFE under safety-policy rollout.
- CL1.1 checks action-conditioned admitted transitions.
- Which coordinates are used by the action admission rule.
- Which values are learner-visible.
- Which values are audit-only.
- Whether the candidate still abstracts away future action alternatives.
- Whether the result is policy-continuation scoped or all-actions scoped.
```

## 12.5 Final report

Write:

```text
outputs/final_report.md
```

The report must contain exactly these sections:

```text
# CL1.1 — Action-Conditioned Safe Ledger Gate

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. CL1 mismatch being tested
## 4. Domain and action-space specification
## 5. Pre-registration provenance
## 6. Candidate action admission rule
## 7. Metrics
## 8. Controls and baselines
## 9. Decision
## 10. Witness analysis
## 11. Layer audit delta
## 12. Bought-by-simplification check
## 13. What was NOT shown
## 14. Durable result
```

---

## 13. Mandatory “what was NOT shown”

Include this section even if CL1.1 passes.

State explicitly:

* no claim that this is a substrate;
* no claim that learner world-model content is derived;
* no claim that LLM training is safe;
* no claim that action-ledger safety transfers to other domains;
* no claim that the candidate is safe under arbitrary future learner policies unless all future action branches were tested;
* no claim that a general substrate generator exists;
* no claim that the playbook is constructive in general;
* no claim that a toy domain itself is valuable outside this gate;
* no claim that learner training is allowed unless `ACTION-LEDGER-OK` is reached.

---

## 14. Halt-downstream rule

If the decision is not `ACTION-LEDGER-OK`, stop.

Do not run learner training.

Do not run representation analysis.

Do not make derivability claims.

The next step after failure is witness analysis:

```text
unsafe admitted witnesses → repair action admission rule or reject state-level boundary path
false-positive action witnesses → vacuity / over-conservatism analysis
missing ground truth → domain or action-space redesign
goal drift → abandon CL1.1 path
```

If decision is `ACTION-LEDGER-OK`, the only allowed next step is a separately pre-registered learner probe under equal-volume controls. That next step must still make no substrate or derivability claim until tested.

---

## 15. Pass/fail bar for the Codex task

The Codex task itself succeeds if it produces a complete CL1.1 report and a valid decision, even if the action ledger fails.

The task fails if:

* no pre-registration JSON is written before metric computation;
* thresholds are changed after seeing results;
* evaluation is performed over states but not `(state, action)` pairs;
* candidate admission silently uses collapse labels or future outcome labels as learner-visible inputs;
* candidate admission claims all-action safety while testing only safety-policy continuation;
* no CL1 state-level carryover baseline is included;
* no projection-blind action baseline is included;
* no trivially-safe action baseline is included;
* no unfiltered action control is included;
* no equal-volume/equal-budget check is performed;
* no witness files are written;
* `what was NOT shown` is omitted;
* the report claims a substrate or derived world-model;
* the work turns into policy optimization, DSL/CEGIS/meta-synthesis, or toy-domain exploration.

---

## 16. Final instruction

The desired result is not “passing.”

The desired result is a reliable transition-ledger decision:

> either the CL1 state-level boundary can be repaired into an action-conditioned safe ledger,
> or CL1’s apparent success is exposed as insufficient for learner training.

Optimize for survival under criticism, not for preserving the CL1 positive result.

