# Validation Report: Camouflage-Cost x Audit Surface

| check | result | interpretation |
|---|---|---|
| spec_hash | passed | declared `705956aeed7da99b221d6ae0c1c2bc5c54b2099585a2a8134eede86155be200e`, actual `705956aeed7da99b221d6ae0c1c2bc5c54b2099585a2a8134eede86155be200e` |
| baseline_calibration_gate | passed | gamma=0 and audit-off reproduces geometric coin-flip baseline before H1/H2/H3 are read. |
| type_blind_runtime_assert | passed | `decide()` asserts the observation has no `behavior_gene` or `true_x`; audit false positives do not read type. |
| true_gene_metric | passed | permanence is computed from hidden true shares/genes, not from signal. |
| gamma0_audit_no_effect_check | failed | absolute gamma=0 best audit effect `0.400`; threshold `<0.10`. |
| gamma0_positive_leak_stop | passed | positive gamma=0 audit lift `-0.400` would indicate leakage; negative effect is not a leakage stop but still fails H2 part (ii). |
| finite_values | passed | all aggregate metrics are finite. |

## Verdict

valid surface run; H1/H2/H3 verdicts are readable under the registered thresholds.
