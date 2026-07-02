# B1 — Auxiliary-Variable Identifiability Gate

**File:** `experiments/B/B1_Auxiliary-Variable_Identifiability_Gate.md`
**Task type:** bounded synthetic identifiability experiment
**Status:** post-S4.1, constructive/falsifying gate
**Allowed:** small Python implementation, synthetic data, preregistered metrics, controls, audit outputs
**Forbidden:** LLM training, internet data, natural language corpus training, Sanskrit parser, substrate/derivability claims

---

## 0. Immutable project goal

Keep this goal visible at every step:

> Train an LLM / learner so that its world-model is **derived**, not merely generalized from internet-like data.

Current refined project hypothesis:

> The attainable form is not “derive the world from nothing,” but “minimal empirical calibration, maximal derivational unfolding.”

B1 tests a tiny version of this:

> Can an objective latent structure be separated from perception/coloring only when a minimal auxiliary variable is supplied?

---

## 1. Why B1 exists

S0–S4.1 produced a disciplined boundary-accounting infrastructure but did not generate a semantic boundary.

B0 and S4 established:

```text id="jyjuxu"
human-authored boundary ≠ derived boundary
toy replay ≠ world boundary
accounting protocol ≠ boundary generator
```

The next step must not be another accounting protocol.

B1 tests a constructive/falsifying claim:

> In a synthetic toy-world with known latent truth, objective structure and perception-coloring are not identifiable from observations alone, but become recoverable when a suitable auxiliary variable is supplied.

This operationalizes the intuition:

```text id="x98hk0"
objective boundary = relational structure
perception / viability = coloring layer
auxiliary variable = minimal calibration axis
```

---

## 2. Gate question

Can a learner recover an objective latent structure from observations that are mixed with observer/coloring bias:

```text id="t8u6xm"
y = z_objective + bias_u + noise
```

where:

```text id="g7x8eq"
z_objective = objective latent scalar / order
u = auxiliary variable, e.g. observer/species/instrument class
bias_u = perception-coloring / baseline shift
```

such that:

```text id="l8uz3o"
without u: recovery fails;
with u + minimal calibration anchors: recovery succeeds;
controls show that success is not leakage, lookup, or human-authored outcome labeling.
```

---

## 3. Required decision vocabulary

Use exactly one:

```text id="w3xk45"
B1-PASS-AUXILIARY-IDENTIFIABILITY-SIGNAL
B1-FAIL-NO-AUX-RECOVERS
B1-FAIL-WITH-AUX-NO-RECOVERY
B1-FAIL-AUX-LEAKAGE
B1-FAIL-CONTROL-LEAKAGE
B1-FAIL-HUMAN-AUTHORED-OUTCOMES
B1-FAIL-REPEATS-S4-ACCOUNTING
B1-INCONCLUSIVE
HALT-GOAL-DRIFT
```

Meaning:

```text id="j0lefq"
B1-PASS-AUXILIARY-IDENTIFIABILITY-SIGNAL
- No-auxiliary recovery fails, auxiliary recovery succeeds, and controls pass.

B1-FAIL-NO-AUX-RECOVERS
- The objective factor is recoverable without auxiliary variable, making the gate non-discriminating.

B1-FAIL-WITH-AUX-NO-RECOVERY
- Auxiliary variable does not enable recovery.

B1-FAIL-AUX-LEAKAGE
- Auxiliary variable or data fields directly encode the true objective factor.

B1-FAIL-CONTROL-LEAKAGE
- Shuffled/random controls still succeed.

B1-FAIL-HUMAN-AUTHORED-OUTCOMES
- The experiment uses human-authored final labels/outcomes instead of generated latent truth.

B1-FAIL-REPEATS-S4-ACCOUNTING
- B1 only audits supplied labels instead of generating/recovering structure from synthetic interaction/data.

B1-INCONCLUSIVE
- Metrics are mixed, unstable, or below preregistered confidence.

HALT-GOAL-DRIFT
- Work becomes literature review, philosophy essay, S-demo packaging, framework naming, LLM work, or unbounded ML.
```

---

## 4. Required input files

Read these files if present:

```text id="qzdavt"
research/MAP-S0_Derivational_Semantic_Ecology.md
research/MAP-S1_Literature-grounded_Constraint_Refinement.md
research/closed_directions_ledger.md

experiments/B/B0_Boundary-Origin_Claim-Strength_Ledger.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_decision.json
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_report.md
experiments/B/B0_boundary_origin_claim_strength_ledger/B0_s2_reinterpretation.md

experiments/S/S4_tiny_boundary_accounting_replay_implementation/S4_1_decision.json
experiments/S/S4_tiny_boundary_accounting_replay_implementation/S4_1_repair_report.md
experiments/S/S4_tiny_boundary_accounting_replay_implementation/S4_decision.json
experiments/S/S4_tiny_boundary_accounting_replay_implementation/S4_report.md
```

If files are missing, list them as `MISSING`.

Continue only if S4.1 decision exists and is:

```text id="jraz2j"
S4.1-PASS-GATE-CHAIN-VERIFICATION-REPAIRED
```

---

## 5. Allowed output directory

Create:

```text id="0askp2"
experiments/B/B1_auxiliary_variable_identifiability_gate/
```

Inside it, create exactly:

```text id="k0flpc"
README.md
B1_preregistration.json
B1_report.md
B1_decision.json
identifiability_toy.py
run_b1.py
outputs/dataset_manifest.json
outputs/no_aux_results.json
outputs/with_aux_results.json
outputs/control_results.json
outputs/metrics.json
outputs/leakage_audit.json
outputs/final_report.md
```

Do not modify files outside this directory.

Do not edit MAP files.

Do not edit S0/S1/S2/S3/S4/B0 files.

Do not edit `research/closed_directions_ledger.md`.

Commit required after successful completion.

---

## 6. Implementation constraints

Use:

```text id="niz4fv"
Python 3
standard library only
deterministic random seed
no network
no external ML libraries
no LLM calls
no internet data
no natural language corpus
```

The implementation must be small and auditable.

Forbidden:

```text id="o4s748"
final_status fields
expected_final_status fields
human-authored outcome labels
manual assignment of recovered z_objective
direct lookup from item_id to true z_objective during learner fit
direct lookup from auxiliary variable to final answer
using true z_objective outside evaluation metrics
using observer labels that uniquely identify item identity
claiming substrate / derivability / grounding / LLM safety
```

---

## 7. Synthetic toy-world

Implement a deterministic synthetic world.

### 7.1 Latent factors

Define:

```text id="93lu1p"
z_obj_i ∈ R
```

as the objective latent scalar for item `i`.

Define:

```text id="5d3p9b"
u ∈ {U0, U1, U2, U3}
```

as an auxiliary variable representing observer/species/instrument class.

Define:

```text id="t0cj0j"
bias_u ∈ R
```

as perception-coloring / baseline shift for observer `u`.

Observation:

```text id="ec5cdf"
y_i,u = z_obj_i + bias_u + noise
```

Important:

```text id="c7n108"
z_obj_i and bias_u are known to the experiment only for evaluation and data generation.
The learner must not use true z_obj_i during fitting.
```

---

### 7.2 Confounded no-auxiliary regime

Create test observations so that raw `y` alone does not recover `z_obj`.

Recommended deterministic construction:

```text id="wvzckw"
U0 has positive bias and mostly low z_obj items.
U1 has smaller positive bias and lower-mid z_obj items.
U2 has smaller negative bias and upper-mid z_obj items.
U3 has negative bias and high z_obj items.
```

Thus:

```text id="v3tqqn"
y = z_obj + bias_u
```

is compressed/confounded across groups.

No-auxiliary learner sees:

```text id="jbgd3s"
y
```

but not `u`.

It may use only raw observation values and generic transformations.

---

### 7.3 With-auxiliary regime

With-auxiliary learner sees:

```text id="lmkj72"
y + u
```

and a small set of calibration anchors observed across all `u`.

Calibration anchors must not include true `z_obj` labels.

They may include the same item observed under multiple `u`, allowing estimation of relative bias:

```text id="yqpk63"
mean_y(anchor, u) - mean_y(anchor, reference_u)
```

The learner estimates relative observer bias and de-biases observations.

This models:

```text id="xx8hca"
minimal calibration contact
```

not full supervision.

---

## 8. Required learners

Implement at least two learners.

### 8.1 No-auxiliary learner

Input:

```text id="ll6mue"
y only
```

Output:

```text id="28bawa"
estimated_z_obj
```

Allowed strategy:

```text id="83gw4j"
rank or normalize y as proxy for z_obj
```

This learner must not use `u`.

### 8.2 With-auxiliary calibration learner

Input:

```text id="cmg6g5"
y
u
calibration anchor overlaps
```

Output:

```text id="a72itp"
estimated_z_obj = y - estimated_bias_u
```

Allowed strategy:

```text id="q2m00g"
estimate relative bias_u from anchor overlaps;
subtract estimated bias_u;
rank or normalize residual as z_obj estimate.
```

This learner must not use true `z_obj` during fitting.

---

## 9. Required metrics

Implement:

```text id="zbj2ed"
Pearson correlation between estimated_z_obj and true z_obj on held-out non-anchor items.
Rank correlation may be added but Pearson is required.
```

Preregistered thresholds:

```text id="i994os"
no_aux_abs_corr <= 0.30
with_aux_corr >= 0.90
improvement >= 0.60
shuffled_aux_corr <= 0.50
no_anchor_with_aux_corr <= 0.50
random_world_corr <= 0.30
```

If using multiple seeds:

```text id="90ggsz"
all primary thresholds must hold on aggregate mean;
at least 80% of seeds must individually satisfy directional result.
```

A single deterministic seed is acceptable for B1 if dataset construction is fully documented.

---

## 10. Required controls

### C1 — Shuffled auxiliary control

Randomly permute `u` labels while preserving `y`.

Expected:

```text id="av4grb"
with-auxiliary recovery should fail or drop below threshold.
```

Pass threshold:

```text id="4py0h6"
shuffled_aux_corr <= 0.50
```

### C2 — No-anchor control

Provide `u` but remove calibration anchor overlaps.

Expected:

```text id="80n96d"
relative bias cannot be estimated reliably.
```

Pass threshold:

```text id="12x0nw"
no_anchor_with_aux_corr <= 0.50
```

### C3 — Random-world control

Generate observations where `y` is independent of `z_obj` after controls.

Expected:

```text id="h85l18"
no method should recover objective factor.
```

Pass threshold:

```text id="d83k0d"
random_world_corr <= 0.30
```

### C4 — Auxiliary leakage audit

Check:

```text id="rnypnz"
u does not uniquely identify item_id.
u does not directly encode z_obj.
training fit does not read true z_obj.
calibration anchors do not include true z_obj.
evaluation truth is used only after predictions are produced.
```

Any violation fails B1 as:

```text id="hsi8kd"
B1-FAIL-AUX-LEAKAGE
```

---

## 11. Required preregistration

Create:

```text id="34wtay"
B1_preregistration.json
```

It must include:

```json id="0izafc"
{
  "decision_options": [],
  "primary_hypothesis": "...",
  "thresholds": {
    "no_aux_abs_corr_max": 0.30,
    "with_aux_corr_min": 0.90,
    "improvement_min": 0.60,
    "shuffled_aux_corr_max": 0.50,
    "no_anchor_with_aux_corr_max": 0.50,
    "random_world_corr_max": 0.30
  },
  "forbidden_claims": [
    "substrate claim",
    "derivability claim",
    "LLM safety claim",
    "semantic boundary generator claim",
    "real-world transfer claim"
  ],
  "downstream_allowed_only_if_pass": [
    "B1 postmortem",
    "B2 relational order-dimension gate spec"
  ]
}
```

---

## 12. Required reports and outputs

### 12.1 `outputs/dataset_manifest.json`

Must include:

```text id="czlwyj"
seed
number_of_items
number_of_auxiliary_classes
bias_values
noise_level
anchor_count
heldout_count
confounding_design
forbidden_fields_absent
```

### 12.2 `outputs/no_aux_results.json`

Must include predictions and metrics for no-auxiliary learner.

### 12.3 `outputs/with_aux_results.json`

Must include bias estimates, de-biased predictions, and metrics.

### 12.4 `outputs/control_results.json`

Must include C1–C3 results.

### 12.5 `outputs/leakage_audit.json`

Must include C4 checks.

### 12.6 `outputs/metrics.json`

Must summarize all metrics and threshold decisions.

### 12.7 `outputs/final_report.md`

Must summarize:

```text id="8kg5af"
primary result
controls
leakage audit
interpretation
what was not shown
```

### 12.8 `B1_report.md`

Must contain exactly:

```text id="ypldeq"
# B1 — Auxiliary-Variable Identifiability Gate

## 0. Verdict
## 1. Goal anchor
## 2. Inputs used
## 3. Hypothesis
## 4. Synthetic world design
## 5. Learners
## 6. Primary metrics
## 7. Controls
## 8. Leakage audit
## 9. Pass / fail analysis
## 10. What was NOT shown
## 11. Downstream permission
## 12. Durable result
```

### 12.9 `B1_decision.json`

Must be valid JSON:

```json id="vyk1pu"
{
  "decision": "...",
  "reason": "...",
  "s4_1_decision_confirmed": false,
  "dataset_generated": false,
  "no_aux_recovery_failed": false,
  "with_aux_recovery_succeeded": false,
  "improvement_threshold_passed": false,
  "shuffled_aux_control_passed": false,
  "no_anchor_control_passed": false,
  "random_world_control_passed": false,
  "aux_leakage_detected": false,
  "human_authored_outcomes_detected": false,
  "repeats_s4_accounting": false,
  "admissible_for_next_gate": false,
  "llm_training_allowed": false,
  "substrate_claim_allowed": false,
  "derivability_claim_allowed": false,
  "semantic_boundary_generator_claim_allowed": false,
  "real_world_transfer_claim_allowed": false,
  "next_allowed_work": []
}
```

If B1 passes:

```json id="80i4fe"
{
  "decision": "B1-PASS-AUXILIARY-IDENTIFIABILITY-SIGNAL",
  "admissible_for_next_gate": true,
  "next_allowed_work": [
    "B1 postmortem",
    "B2 relational order-dimension gate spec"
  ]
}
```

Never set these true:

```json id="tneey4"
"llm_training_allowed"
"substrate_claim_allowed"
"derivability_claim_allowed"
"semantic_boundary_generator_claim_allowed"
"real_world_transfer_claim_allowed"
```

---

## 13. Pass conditions

B1 passes only if all hold:

```text id="tcxsq4"
1. S4.1 pass is confirmed.
2. Dataset is generated from latent z_obj and auxiliary bias_u, not human-authored final labels.
3. No-auxiliary recovery fails: no_aux_abs_corr <= 0.30.
4. With-auxiliary recovery succeeds: with_aux_corr >= 0.90.
5. Improvement threshold passes: with_aux_corr - abs(no_aux_corr) >= 0.60.
6. Shuffled auxiliary control passes: shuffled_aux_corr <= 0.50.
7. No-anchor control passes: no_anchor_with_aux_corr <= 0.50.
8. Random-world control passes: random_world_corr <= 0.30.
9. Leakage audit detects no auxiliary leakage.
10. True z_obj is used only for evaluation after predictions are produced.
11. No human-authored outcome labels are used.
12. No LLM/model/substrate/derivability/real-world-transfer claim is made.
```

---

## 14. Failure conditions

Fail as `B1-FAIL-NO-AUX-RECOVERS` if no-auxiliary learner exceeds threshold.

Fail as `B1-FAIL-WITH-AUX-NO-RECOVERY` if with-auxiliary learner fails threshold.

Fail as `B1-FAIL-AUX-LEAKAGE` if auxiliary variable or fit procedure leaks true objective factor.

Fail as `B1-FAIL-CONTROL-LEAKAGE` if shuffled/no-anchor/random-world controls pass incorrectly.

Fail as `B1-FAIL-HUMAN-AUTHORED-OUTCOMES` if outcomes are manually labeled rather than generated from latent factors.

Fail as `B1-FAIL-REPEATS-S4-ACCOUNTING` if the task only audits supplied fields and does not recover structure from synthetic data.

Fail as `B1-INCONCLUSIVE` if metrics are unstable or threshold results are mixed.

Fail as `HALT-GOAL-DRIFT` if the work becomes philosophy, literature review, demo packaging, or unbounded ML.

---

## 15. Mandatory “what was NOT shown”

Include in `B1_report.md`:

```text id="fs2h9b"
- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No semantic boundary generator was implemented.
- No claim that objective/perceptual separation is generally possible.
- No claim that real-world perception can be disentangled by this toy result.
- No claim that auxiliary variables solve grounding.
- No claim that synthetic identifiability transfers to internet-scale data.
- No claim that viability coloring is truth.
- No claim that passing B1 proves the project goal.
```

---

## 16. Required commands

Run from repository root:

```bash id="dchpr9"
python3 experiments/B/B1_auxiliary_variable_identifiability_gate/run_b1.py
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/B1_preregistration.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/B1_decision.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/outputs/dataset_manifest.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/outputs/no_aux_results.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/outputs/with_aux_results.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/outputs/control_results.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/outputs/metrics.json >/dev/null
python3 -m json.tool experiments/B/B1_auxiliary_variable_identifiability_gate/outputs/leakage_audit.json >/dev/null
```

---

## 17. Git discipline

Before changes:

```bash id="t8s5v1"
git status --short
```

After running B1:

```bash id="d78s2r"
git status --short
git diff -- experiments/B/B1_auxiliary_variable_identifiability_gate/
```

Stage only:

```bash id="xusjkq"
git add experiments/B/B1_auxiliary_variable_identifiability_gate/
```

Also stage the B1 spec file only if newly created:

```bash id="ea1y2q"
git add experiments/B/B1_Auxiliary-Variable_Identifiability_Gate.md
```

Do not stage unrelated files.

Commit with:

```bash id="ejn3t3"
git commit -m "Add B1 auxiliary-variable identifiability gate"
```

After commit:

```bash id="hhmqu4"
git status --short
git log -1 --oneline
```

Final response must include:

```text id="o0iq8m"
- B1 decision
- files created
- commands run
- JSON validation status
- commit hash
- whether unrelated changes remain unstaged
```

---

## 18. Final instruction

The desired result is not to prove the project goal.

The desired result is to test a narrow claim:

> In a finite synthetic toy-world, objective/perceptual separation fails without auxiliary calibration and succeeds with explicit auxiliary calibration, without leakage.

If B1 passes, it supports only:

```text id="rsmh6y"
minimal calibration can make a hidden objective factor recoverable in a toy setting
```

It does not prove real-world disentanglement, grounding, substrate, or LLM safety.

