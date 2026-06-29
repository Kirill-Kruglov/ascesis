# JB0.E1 Standard CEGAR Boundary Assessment

This is not FA, not T-C, and not shield synthesis. It assesses whether standard history/predicate CEGAR gives a practically useful Justitia boundary.

## Decision

Classification: **Conservative_but_vacuous**.
Stop reason: `vacuity`.
Should Justitia remain a Door-1 substrate candidate? **NO**.
Should T-C be considered after this result? **NO**.
Reason: False-safe reduction required classifying too many held-out SAFE states as unsafe/doomed.

## Best JB0 Boundary

- Iteration: `1`.
- Precision: `0.649543`.
- Recall: `0.956839`.
- False-safe rate: `0.043161`.
- False-positive rate: `0.540810`.
- Balanced accuracy: `0.708014`.
- Predicates: `1`.
- Abstract cell upper bound: `2`.

## FA2.5 Baseline Comparison

| baseline | precision | recall | false-safe/FNR | FPR | ROC-AUC | balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|
| B0_current_18_0 | 0.861006 | 0.767377 | 0.232623 | 0.129771 | 0.846349 | 0.818803 |
| B1_history_CEGAR | 0.838689 | 0.746076 | 0.253924 | 0.150323 | 0.892945 | 0.797877 |
| B2_raw_current_state | 0.810596 | 0.686099 | 0.313901 | 0.167939 | 0.764238 | 0.759080 |

## Selected Predicates

| rank | predicate | family | layer | history depth |
|---:|---|---|---|---:|
| 1 | policy == consequence_plus_diversity | control_policy | conditional L2/L5 config | 0 |

## Required Answers

1. Does standard CEGAR produce a useful boundary? `False`.
2. Improvement over 18.0: best false-safe `0.043161` vs B0 FNR `0.232623`; precision/balanced accuracy must also be considered.
3. Improvement over FA2.5 history baseline: best false-safe `0.043161` vs B1 FNR `0.253924`.
4. Predicates selected: `P_policy_consequenceplusdiversity`.
5. Did refinement plateau? `False`.
6. Did state/cell count explode? `False`.
7. Did the conservative boundary become vacuous? `True`.
8. Are selected predicates layer-eligible? `True`.
9. Should Justitia remain a Door-1 substrate candidate? **NO**.
10. Should T-C be considered after this result? **NO**.

No safety claim is made.
