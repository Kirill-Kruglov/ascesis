# Validation Report: Strategic Camouflage

| check | result | interpretation |
|---|---|---|
| spec_hash | passed | declared `4fe5ff79ebb93cfc7c87e4132e77b2c715c981cb09c55d4a78492393e6a1725f`, actual `4fe5ff79ebb93cfc7c87e4132e77b2c715c981cb09c55d4a78492393e6a1725f` |
| calibration_gate | passed | corrected gate (a)/(b)/(c): strategic c->1, strategic permanence collapse, passive-control parent coin-flip. |
| type_blind_runtime_assert | passed | feeder `decide()` asserts no `behavior_gene`, `true_x`, or `concealment` on observation. |
| true_gene_metric | passed | permanence and adversary extinction are computed from hidden true state, not signal. |
| selfish_c_integrity | passed | c hill-climb optimizes group payoff; no reveal bonus or designer nudge is present. |
| finite_values | passed | aggregate metrics are finite. |

## Verdict

valid surface run; corrected gate (a)/(b)/(c) passed and H_s1/H_s2/H_s3 are readable under the registered thresholds.
