# Validation Report: Strategic Camouflage

| check | result | interpretation |
|---|---|---|
| spec_hash | passed | declared `f9183429305c2961e0191362e1b5c873a528ed20483ea92c0c396f34de8b1e6e`, actual `f9183429305c2961e0191362e1b5c873a528ed20483ea92c0c396f34de8b1e6e` |
| calibration_gate | failed | free concealment drove adversary c toward 1, but did not reproduce the baseline coin-flip permanence region. |
| type_blind_runtime_assert | passed | feeder `decide()` asserts no `behavior_gene`, `true_x`, or `concealment` on observation. |
| true_gene_metric | passed | permanence and adversary extinction are computed from hidden true state, not signal. |
| selfish_c_integrity | passed | c hill-climb optimizes group payoff; no reveal bonus or designer nudge is present. |
| finite_values | passed | aggregate metrics are finite. |

## Verdict

stand invalid: strategic calibration failed; H_s1/H_s2/H_s3 should not be read.
