# CEGAR Equivalence Analysis

History baseline matches candidate under epsilon `0.02`: `True`.

The B1 baseline is deliberately strong and uses standard delayed observation/history variables rather than the FA2 compact candidate structure.

If B1 matches or exceeds the candidate, the result is recorded as `Equivalent_to_standard_history_refinement` rather than protected as an FA-specific success.

| metric | candidate | B1 history baseline | delta candidate-minus-B1 |
|---|---:|---:|---:|
| precision | 0.776955 | 0.838689 | -0.061735 |
| recall | 0.529148 | 0.746076 | -0.216928 |
| specificity | 0.840869 | 0.849677 | -0.008808 |
| roc_auc | 0.679281 | 0.892945 | -0.213665 |
| pr_auc | 0.742772 | 0.886923 | -0.144151 |
| balanced_accuracy | 0.685009 | 0.797877 | -0.112868 |
