# FA2.5 Faithful Candidate Validation

Critical kill-gate experiment. This does not modify Justitia, does not modify collapse, does not use oracle information, and does not test monotonicity.

## Decision

Classification: **No_discriminative_candidate**.
History baseline relation: **Equivalent_to_standard_history_refinement**.
Should T-C be executed? **NO**.
Reason: Candidate fails discrimination acceptance criteria; history relation is still recorded separately.

## Dataset

| item | count | detail |
|---|---:|---|
| all_harvested_states | 24000 | BA1 baseline replay |
| available_A_false_safe | 5839 | 18.0 SAFE and future collapse |
| available_B_safe_remain_safe | 10724 | 18.0 SAFE and no future collapse |
| selected_A_false_safe | 5839 | all available A |
| selected_B_safe_remain_safe | 5839 | sampled with seed 2525 |
| train_rows | 8191 | group split fraction 0.7 |
| test_rows | 3487 | held-out trajectory groups |
| test_A_false_safe | 1784 | split label/population count |
| test_B_safe_remain_safe | 1703 | split label/population count |
| train_A_false_safe | 4055 | split label/population count |
| train_B_safe_remain_safe | 4136 | split label/population count |

## Metrics

| model | precision | recall | specificity | FPR | FNR | ROC-AUC | PR-AUC | balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B0_current_18_0 | 0.861006 | 0.767377 | 0.870229 | 0.129771 | 0.232623 | 0.846349 | 0.872060 | 0.818803 |
| B1_history_CEGAR | 0.838689 | 0.746076 | 0.849677 | 0.150323 | 0.253924 | 0.892945 | 0.886923 | 0.797877 |
| B2_raw_current_state | 0.810596 | 0.686099 | 0.832061 | 0.167939 | 0.313901 | 0.764238 | 0.830061 | 0.759080 |
| Candidate_FA2_compact | 0.776955 | 0.529148 | 0.840869 | 0.159131 | 0.470852 | 0.679281 | 0.742772 | 0.685009 |

## Acceptance Criteria

- C1 precision margin over 18.0: `False`; gain `-0.084052` with required margin `0.05`.
- C2 recall does not collapse: `True`.
- C3 no oracle information: `True`.
- C4 layer eligible only: `True`.
- C5 not matched by history baseline: `False`.

## Required Answers

1. Does a faithful candidate exist? `False`.
2. Does it discriminate false-safe from SAFE? See metrics table; discrimination is present, but candidate acceptance depends on all criteria.
3. Is discrimination obtained without oracle information? `True`.
4. Is the candidate layer-eligible? `True`.
5. Is the candidate genuinely different from history-variable refinement? `False`; relation `Equivalent_to_standard_history_refinement`.
6. Should T-C be executed? **NO**.

Final answer: T-C should not be executed unless a distinct candidate passes the kill-gate.
