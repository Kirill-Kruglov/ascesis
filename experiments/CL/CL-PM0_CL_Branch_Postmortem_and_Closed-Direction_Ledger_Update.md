# CL-PM0: CL Branch Postmortem + Closed-Direction Ledger Update

**To:** Codex
**From:** Kirill / analyst
**Task type:** postmortem + ledger update
**Status:** close CL branch before returning to analytic substrate search
**Do not run a new experiment. Do not optimize any learner. Do not reopen CL2.**

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current honest weakened form:

> Train an LLM / learner inside a **safe boundary** so the learner does not observe collapse-trajectories; safety comes from domain filtering even if content inside the boundary is still generalized rather than fully derived.

Every postmortem claim must pass the parallel-reality test:

> “We are documenting this to obtain a safe / derivable substrate for LLMs, and this step leads there by…”

If the honest ending is “because the CL toy-domain learner sequence is interesting,” mark as `HALT-GOAL-DRIFT`.

---

## 1. Why this task exists

The CL branch produced a useful sequence of gates:

```text
CL0  → boundary candidate only, not substrate
CL1  → state-level boundary fidelity pilot
CL1.1 → action-conditioned safe ledger gate
CL2  → learner probe halted by shuffled-target gate
CL2.1 → shuffled-control failure diagnosed as bias artifact
CL2.2 → generic learner failed to produce evidence-bearing learning signal
```

The CL branch should now be closed before returning to analytic substrate search.

The purpose of CL-PM0 is to prevent future drift:

* do not treat CL1.1 as substrate discovery;
* do not treat CL2 primary learner accuracy as evidence;
* do not continue tuning learners until success;
* do not proceed to representation / derivability probes;
* extract durable constraints for the next analytic map.

---

## 2. Task objective

Produce a postmortem and update the closed-direction ledger.

The output must answer:

> What did the CL branch show, what did it fail to show, which directions are now closed, and what constraints must any future substrate-search direction satisfy?

The result must be one of:

1. `CL-BRANCH-CLOSED`
2. `HALT-MISSING-EVIDENCE`
3. `HALT-GOAL-DRIFT`

---

## 3. What this task is NOT

Do NOT do any of the following:

* Do not run a new experiment.
* Do not rerun CL2.
* Do not tune the generic learner.
* Do not introduce a new learner.
* Do not introduce a new domain.
* Do not write a CL3 spec.
* Do not claim substrate discovery.
* Do not claim derivability.
* Do not claim LLM safety.
* Do not claim the boundary is learned.
* Do not claim the safe ledger transfers.
* Do not generalize from `FourZoneMassDomain` beyond what the evidence supports.
* Do not turn this into ML benchmarking.
* Do not turn this into methodology for its own sake.
* Do not delete, move, stage, or commit files.

---

## 4. Required input files

Read these files if present.

### CL0 / CL1 / CL1.1

```text
playbook_extraction/CL0_closed_ledger_candidate_proposal.md
playbook_extraction/CL0_preregistration.json

experiments/CL/CL1_boundary_fidelity_pilot/SPEC.md
experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json
experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json
experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md
experiments/CL/CL1_boundary_fidelity_pilot/outputs/layer_audit.md

experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/SPEC.md
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/final_report.md
experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/layer_audit_delta.md
```

### CL2 / CL2.1 / CL2.2

```text
experiments/CL/CL2_equal_volume_learner_probe/SPEC.md
experiments/CL/CL2_equal_volume_learner_probe/outputs/metrics.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/decision.json
experiments/CL/CL2_equal_volume_learner_probe/outputs/final_report.md
experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md
experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json

experiments/CL/CL2_1_shuffled_control_repair/SPEC.md
experiments/CL/CL2_1_shuffled_control_repair/outputs/control_metrics.json
experiments/CL/CL2_1_shuffled_control_repair/outputs/decision.json
experiments/CL/CL2_1_shuffled_control_repair/outputs/final_report.md
experiments/CL/CL2_1_shuffled_control_repair/outputs/learner_bias_audit.json
experiments/CL/CL2_1_shuffled_control_repair/outputs/evaluation_integrity_audit.md
experiments/CL/CL2_1_shuffled_control_repair/outputs/control_recommendation.md

experiments/CL/CL2_2_learner_prior_ablation/SPEC.md
experiments/CL/CL2_2_learner_prior_ablation/outputs/learning_curve_metrics.json
experiments/CL/CL2_2_learner_prior_ablation/outputs/control_metrics.json
experiments/CL/CL2_2_learner_prior_ablation/outputs/prior_ablation_metrics.json
experiments/CL/CL2_2_learner_prior_ablation/outputs/decision.json
experiments/CL/CL2_2_learner_prior_ablation/outputs/final_report.md
experiments/CL/CL2_2_learner_prior_ablation/outputs/data_dependence_audit.json
experiments/CL/CL2_2_learner_prior_ablation/outputs/prior_audit.md
experiments/CL/CL2_2_learner_prior_ablation/outputs/durable_constraint.md
```

### Existing ledger / method files

```text
research/closed_directions_ledger.md
playbook_extraction/02_extracted_method.md
playbook_extraction/03_not_yet_method.md
playbook_extraction/harness/output_schema.md
playbook_extraction/harness/failure_conditions.md
```

If a file is missing, list it as `MISSING`.

Continue only if enough CL1.1, CL2, CL2.1, and CL2.2 evidence is present.

---

## 5. Allowed output files

Create a new postmortem directory:

```text
experiments/CL/CL_PM0_postmortem/
```

Inside it, create:

```text
CL_PM0_postmortem.md
CL_PM0_closed_direction_entries.md
CL_PM0_constraint_map_seed.md
CL_PM0_decision.json
```

Also update or create the central ledger:

```text
research/closed_directions_ledger.md
```

Allowed ledger operation:

* If the file exists, append a new section only.
* If the file does not exist, create it.
* Do not rewrite old sections.
* Do not delete or rename anything.

The appended section must be titled exactly:

```text
## CL branch: safe action ledger without generic learner signal
```

---

## 6. Required postmortem structure

Write:

```text
experiments/CL/CL_PM0_postmortem/CL_PM0_postmortem.md
```

with exactly these sections:

```text
# CL-PM0 — CL Branch Postmortem

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. Timeline of CL gates
## 4. What survived
## 5. What failed
## 6. What was killed
## 7. What remains open
## 8. Fundamental constraints extracted
## 9. Bought-by-simplification analysis
## 10. Parallel-reality check
## 11. What was NOT shown
## 12. Closed-direction ledger update summary
## 13. Next analytic work allowed
## 14. Final durable result
```

---

## 7. Required content

### 7.1 Verdict

Use one of:

```text
CL-BRANCH-CLOSED
HALT-MISSING-EVIDENCE
HALT-GOAL-DRIFT
```

Expected verdict if evidence is sufficient:

```text
CL-BRANCH-CLOSED
```

Reason:

```text
The CL branch produced a non-vacuous oracle-filtered action-safe ledger on one toy lawful domain, but failed to produce admissible evidence of generic non-oracle transition learning. Therefore no representation, derivability, substrate, or LLM-safety downstream work is allowed from this branch.
```

---

### 7.2 Timeline of CL gates

Create a compact table:

| gate | question | decision | useful result | halt / limitation |
| ---- | -------- | -------- | ------------- | ----------------- |

Include:

```text
CL0
CL1
CL1.1
CL2
CL2.1
CL2.2
```

Use only evidence from files.

---

### 7.3 What survived

Must include these survivors if supported by evidence:

```text
1. Boundary-first discipline survived.
2. State-level safety was shown insufficient for learner ledgers.
3. Action-conditioned oracle ledger exists on FourZoneMassDomain.
4. Projection-blind / state-level / trivially-safe baselines were useful controls.
5. The CL kill-gate chain prevented false learner evidence.
6. CL branch produced durable constraints for substrate search.
```

Do not overstate.

---

### 7.4 What failed

Must include:

```text
1. CL1 state-level SAFE did not imply safe action ledger.
2. CL2 learner result was not admissible because shuffled-target control failed.
3. CL2.1 showed the primary rule-family learner was confounded by transition-family prior.
4. CL2.2 showed no evidence-bearing generic learner signal on the current safe ledger.
5. The current CL learner path cannot proceed to representation / derivability.
```

---

### 7.5 What was killed

Create a table:

| killed direction | evidence | failure mode | durable constraint |
| ---------------- | -------- | ------------ | ------------------ |

Include at minimum these killed directions:

#### K1 — State-level SAFE as learner-ledger admission

Failure:

```text
SAFE(state) + all actions leaks unsafe transitions.
```

Constraint:

```text
Future learner ledgers must be action-conditioned or transition-conditioned.
```

#### K2 — Oracle-filtered action ledger as substrate evidence

Failure:

```text
Action-safe ledger exists but does not show substrate, derivability, learned boundary, or transfer.
```

Constraint:

```text
Safe ledger is only a precondition, not substrate evidence.
```

#### K3 — Rule-family learner as evidence of learning-from-ledger

Failure:

```text
RuleFamilyTransitionLearner solves the task but is confounded by transition-family prior.
```

Constraint:

```text
Learners that encode the domain transition family are diagnostic-only.
```

#### K4 — Original global shuffled-target control as sufficient anti-leakage gate

Failure:

```text
Global shuffle failed high under primary rule-family learner; CL2.1 diagnosed invalid control / bias artifact.
```

Constraint:

```text
Future learner probes need controls that distinguish data-dependence from prior-dependence.
```

#### K5 — Current CL safe ledger as evidence-bearing for generic transition learning

Failure:

```text
Generic learner showed no full-data transition learning signal under required holdouts.
```

Constraint:

```text
Current safe ledger/domain/learner interface is not yet admissible evidence for learned transition structure.
```

---

### 7.6 What remains open

This section must be careful.

Allowed open questions:

```text
- Whether a different lawful domain can produce a safe ledger that is evidence-bearing for generic learners.
- Whether a different learner class, without exact transition-family prior, can show data-dependent learning under stricter controls.
- Whether the problem is the domain, the ledger interface, the learner class, or the weakened project formulation.
- Whether future analytic work can derive a candidate direction from accumulated impossibility constraints.
```

Forbidden open questions:

```text
- “Try more learners until one works.”
- “Tune generic learner until success.”
- “Run representation analysis anyway.”
- “Scale to LLM.”
- “Claim boundary safety transfers.”
```

---

### 7.7 Fundamental constraints extracted

Create a numbered list.

At minimum include:

```text
C1. Boundary fidelity must precede learner claims.
C2. State safety is weaker than transition/action safety.
C3. Safe filtering is not derivability.
C4. Oracle-filtered data is not a learned boundary.
C5. Learner success is not evidence if bought by transition-family prior.
C6. Generic learner failure blocks representation/derivability work.
C7. Negative controls must be designed against the learner’s inductive bias, not only against field leakage.
C8. Toy-domain success cannot transfer without a separate transfer gate.
C9. A safe ledger must become evidence-bearing before model-internal claims are allowed.
```

---

### 7.8 Bought-by-simplification analysis

Explicitly answer:

```text
What did FourZoneMassDomain simplify away?
What did the oracle action ledger buy by full transition knowledge?
What did the rule-family learner buy by encoded prior?
What did the generic learner lose when prior was removed?
Which simplifications are acceptable as preconditions?
Which simplifications block the main goal?
```

---

### 7.9 Parallel-reality check

Complete:

```text
We did CL0–CL2.2 to obtain a safe / derivable substrate for LLMs, and this branch led there by...
```

The honest completion should say:

```text
...showing that a safe action ledger is possible on a toy lawful domain, but also showing that this is insufficient for learner-derived world-model evidence unless the ledger supports generic, data-dependent learning. Therefore the branch constrains future substrate search rather than providing a substrate.
```

If Codex cannot complete this without overclaiming, set verdict to `HALT-GOAL-DRIFT`.

---

### 7.10 What was NOT shown

Mandatory list:

```text
- No substrate was found.
- No derived world-model was shown.
- No LLM safety was shown.
- No learned boundary was shown.
- No transfer beyond FourZoneMassDomain was shown.
- No autonomous learner safety was shown.
- No arbitrary future action safety was shown.
- No generic transition-learning evidence was shown.
- No representation probe is allowed.
- No derivability claim is allowed.
- No general substrate generator exists.
- No general constructive playbook was shown.
```

---

## 8. Closed-direction ledger update

Write:

```text
experiments/CL/CL_PM0_postmortem/CL_PM0_closed_direction_entries.md
```

This file should contain a clean ledger-ready section.

Then append the same section to:

```text
research/closed_directions_ledger.md
```

Use this exact section heading:

```text
## CL branch: safe action ledger without generic learner signal
```

The ledger entry must contain:

```text
### Status
CLOSED AS SUBSTRATE / DERIVABILITY PATH.
RETAINED AS BOUNDARY / LEDGER PRECONDITION EVIDENCE.

### Evidence chain
- CL0:
- CL1:
- CL1.1:
- CL2:
- CL2.1:
- CL2.2:

### Closed directions
1. State-level SAFE → learner ledger.
2. Oracle-filtered ledger → substrate evidence.
3. Rule-family learner → learning evidence.
4. Original shuffled-target gate → sufficient anti-artifact control.
5. Current safe ledger → generic transition-learning evidence.

### Durable constraints
...

### Future admissibility condition
A future branch may proceed only if it supplies:
1. action-conditioned or transition-conditioned safe ledger;
2. non-oracle learner or learner-interface with data-dependence;
3. controls that defeat prior-dependence and marginal artifacts;
4. no substrate / derivability claim before representation and derivation gates.
```

---

## 9. Constraint map seed

Write:

```text
experiments/CL/CL_PM0_postmortem/CL_PM0_constraint_map_seed.md
```

This is a seed for the next analytic phase, not an experiment spec.

Required structure:

```text
# Constraint Map Seed after CL branch

## 0. Purpose
## 1. Known impossible / closed directions
## 2. Known preconditions that survived
## 3. Boundary between safety and derivability
## 4. What any next direction must satisfy
## 5. Candidate analytic questions
## 6. Forbidden next moves
```

Candidate analytic questions should include:

```text
- What kind of lawful domain makes transition structure learnable without encoding the transition law into the learner?
- What is the minimal interface between substrate and learner that allows data-dependent learning?
- Can derivability be reframed as constraints on the data-generating process rather than on the learner?
- What does “noise is computation” change, if anything, under the constraints already found?
- Can accumulated negative results define a search-space boundary without becoming a new meta-synthesis project?
```

Forbidden next moves must include:

```text
- Tune learner until success.
- Treat CL1.1 ledger as substrate.
- Treat rule-family prior as learning.
- Jump to representation probe.
- Scale to LLM.
- Start general DSL / CEGIS / generator theory.
```

---

## 10. Decision JSON

Write:

```text
experiments/CL/CL_PM0_postmortem/CL_PM0_decision.json
```

with:

```json
{
  "decision": "CL-BRANCH-CLOSED",
  "reason": "...",
  "closed_as": [
    "substrate_path",
    "derivability_path",
    "learner_evidence_path"
  ],
  "retained_as": [
    "boundary_precondition_evidence",
    "action_ledger_precondition_evidence",
    "negative_constraints_for_future_search"
  ],
  "downstream_representation_allowed": false,
  "derivability_claim_allowed": false,
  "llm_training_allowed": false,
  "next_allowed_work": [
    "postmortem review",
    "closed-direction ledger review",
    "analytic constraint-map work"
  ]
}
```

---

## 11. Final quality bar

The Codex task succeeds if:

```text
- postmortem is written;
- ledger section is written;
- central closed_direction ledger is append-only updated or created;
- constraint map seed is written;
- decision JSON is valid;
- no experiment is run;
- no downstream claim is made;
- no files outside allowed paths are modified except append-only ledger update.
```

The task fails if:

```text
- it claims CL branch found a substrate;
- it claims CL2 learner evidence is valid;
- it allows representation / derivability work;
- it suggests tuning learners as next step;
- it rewrites old ledger entries;
- it starts a new experiment;
- it turns into ML benchmarking or methodology work;
- it omits what was NOT shown;
- it omits the parallel-reality check.
```

---

## 12. Final instruction

The desired result is not to make CL look successful.

The desired result is to make the project harder to fool:

> CL branch gave useful boundary and ledger preconditions, but failed as a path to learner-derived substrate evidence. Preserve the constraints, close the branch, and prepare the map for analytic search from known impossibilities.

