# Candidate vs Baselines

| model | precision | recall | specificity | ROC-AUC | PR-AUC | balanced accuracy | Brier |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0_current_18_0 | 0.861006 | 0.767377 | 0.870229 | 0.846349 | 0.872060 | 0.818803 | 0.173028 |
| B1_history_CEGAR | 0.838689 | 0.746076 | 0.849677 | 0.892945 | 0.886923 | 0.797877 | 0.143594 |
| B2_raw_current_state | 0.810596 | 0.686099 | 0.832061 | 0.764238 | 0.830061 | 0.759080 | 0.187425 |
| Candidate_FA2_compact | 0.776955 | 0.529148 | 0.840869 | 0.679281 | 0.742772 | 0.685009 | 0.218681 |

Classification: **No_discriminative_candidate**.
History baseline relation: **Equivalent_to_standard_history_refinement**.
Reason: Candidate fails discrimination acceptance criteria; history relation is still recorded separately.
