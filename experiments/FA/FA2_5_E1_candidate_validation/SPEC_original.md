# FA2.5.E1 — Faithful Candidate Validation

## Specification v2.0

```markdown
# FA2.5.E1
## Faithful Candidate Validation

Status:
Critical kill-gate experiment.

Purpose:

Determine whether the compact invariant families discovered in FA1/FA2
can be assembled into a genuine faithful abstraction candidate.

This experiment does NOT test monotonicity.

This experiment answers an earlier question:

Does a candidate abstraction exist at all?

Only if the answer is YES may T-C be executed.

---

# Context

18.1 established:

Projection blindness exists.

BA established:

Mechanism replacement alone is insufficient.

Layer discipline is required.

FA1 established:

False-safe witnesses possess strong semantic structure.

FA2 established:

Witnesses admit compact compression.

However,

FA2 intentionally did NOT establish whether these compact invariants
actually discriminate false-safe from ordinary SAFE states.

That question is the sole purpose of FA2.5.

---

# Inputs

Use:

experiments/FA1_E1_false_safe_witness_taxonomy/

experiments/FA2_E1_minimal_invariant_compression_test/

experiments/BA4_layer_audit/

No Justitia source modifications.

No collapse modifications.

No oracle variables.

---

# Dataset

Build two balanced populations.

Population A

False-safe witnesses
(from FA1).

Population B

SAFE states
which remain SAFE
through the prediction horizon.

Population sizes should be approximately equal.

If balancing requires sampling,

record seed and procedure.

---

# Candidate Construction

Construct one candidate abstraction using only
layer-eligible,
non-oracle information.

Candidate coordinates may include only
coordinates surviving BA4.

Expected coordinate families:

- spread summary
- mass summary
- policy-visible concentration
- compact history summaries
- compact consequence summaries

Forbidden:

- oracle time-to-collapse
- future labels
- reporting-only metrics
- capture_index
- permanence
- dashboard statistics
- post-hoc variables

Every coordinate must be justified.

---

# Baselines

Candidate must be compared against:

B0

Current 18.0 abstraction.

B1

History-variable baseline.

This baseline should represent the strongest
straightforward CEGAR/predicate-style refinement
using history variables only.

Codex may choose the simplest reasonable implementation.

Document it completely.

B2

Raw-variable baseline.

Use the same number of coordinates as the candidate
whenever possible.

Random selection is NOT sufficient.

Choose the strongest interpretable baseline.

---

# Measurements

For every model report:

Precision

Recall

Specificity

False-positive rate

False-negative rate

ROC-AUC

PR-AUC

Balanced accuracy

Confusion matrix

Calibration if available

---

# Structural Measurements

Additionally report:

number of coordinates

layer eligibility

oracle usage

history usage

state-space increase

estimated WSTS compatibility risk

estimated monotonicity risk

interpretability assessment

---

# Candidate Acceptance Rule

Candidate is accepted only if ALL conditions hold.

C1

Precision exceeds
18.0 baseline
by a statistically meaningful margin.

C2

Recall does not collapse.

C3

No oracle information.

C4

Only layer-eligible coordinates.

C5

Performance is not matched
by the history-variable baseline.

If B1 performs equally well,

record:

Equivalent_to_standard_history_refinement.

Candidate rejected.

---

# Decision Logic

Case A

Faithful_candidate_supported

Conditions:

Candidate clearly outperforms
all baselines,
including history-variable refinement.

Interpretation:

Proceed to T-C.

---

Case B

Equivalent_to_CEGAR

History-variable baseline
matches candidate.

Interpretation:

H_FA1 weakened.

Treat candidate as standard refinement.

Proceed only if useful for Justitia.

---

Case C

No_discriminative_candidate

Compression exists,
but discrimination fails.

Interpretation:

Witness compression
does not imply faithful abstraction.

Terminate FA branch.

---

Case D

Oracle_only

Only oracle coordinates
achieve discrimination.

Interpretation:

No constructive candidate exists.

Terminate FA branch.

---

Case E

Inconclusive.

---

# Required Outputs

experiments/FA2_5_E1_candidate_validation/outputs/

Required:

candidate_definition.md

candidate_coordinates.csv

baseline_definitions.md

dataset_summary.csv

metrics.csv

confusion_matrices.csv

roc_data.csv

precision_recall_data.csv

candidate_vs_baselines.md

cegar_equivalence_analysis.md

layer_eligibility_check.md

candidate_validity.json

hypothesis_assessment.json

final_report.md

implementation_notes.md

---

# Final Report Must Answer

1.

Does a faithful candidate exist?

2.

Does it discriminate false-safe from SAFE?

3.

Is discrimination obtained without oracle information?

4.

Is the candidate layer-eligible?

5.

Is the candidate genuinely different
from history-variable refinement?

6.

Should T-C be executed?

YES or NO.

This decision is mandatory.

---

# Critical Instruction

Actively attempt to reject the candidate.

Passing this experiment is intentionally difficult.

The purpose of FA2.5 is not to optimise performance.

The purpose is to determine whether a faithful abstraction candidate
actually exists.

If no candidate survives the acceptance rule,

the experiment is considered successful.

It has falsified the current research direction early.
```
