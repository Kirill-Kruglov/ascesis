# FA2.E1 WSTS / Monotonicity Risk Assessment

This is a diagnostic assessment only. It does not synthesize a shield and does not claim safety.

## Invariant Risks

| invariant | layer | WSTS risk | monotonicity risk | circularity risk | note |
|---|---|---|---|---|---|
| I1a failed_zone_count >= 4 | L4 eligible | low | low | none | Real spread-collapse count is monotone under failed-zone order. |
| I1b total_mass < 35 | L4 eligible | low | low | none | Real mass collapse threshold is monotone under lower-mass order. |
| I2 Obs.resource_concentration > 0.62 after aid | conditional L2/L3 | medium | medium | none | Policy-visible concentration is delayed/observed and distinct from reporting HHI; monotonicity is not guaranteed. |
| I3 delayed harmful response/neighbor signal after aid | conditional L2/L3 | medium | high | none | History variables can improve or worsen under delayed response, so monotonicity risk is high. |
| I4_oracle oracle future collapse / time-to-collapse exists | L4 plus conditional L1 temporal | high | high | high | Future reachability label is circular for construction and may encode the transition system itself. |
| I4_proxy current minimum-zone-welfare risk band | L4 eligible, but proxy threshold is empirical | medium | low | low | Current min-zone-welfare threshold is compact, but empirical and uncalibrated against non-witness states. |
| I5 I2 or I3 mixed resolver | inherits I2/I3 conditional L2/L3 | medium | high | none | No new coordinate; inherits I2/I3 history and observation risks. |

## Refinement Risk Summary

| refinement | coverage | WSTS risk | monotonicity risk | circularity risk |
|---|---:|---|---|---|
| R0 | 0.000000 | none | none | none |
| R1 | 0.192499 | low | low | none |
| R2 | 0.432951 | medium | medium | none |
| R3 | 0.766398 | medium | high | none |
| R4-oracle | 1.000000 | high | high | high |
| R4-proxy | 0.998287 | medium | high | low |
| R5 | 0.998287 | medium | high | low |

The main risk is not reporting-layer confusion in this dataset; it is whether the temporal proxy is discriminative outside the false-safe witness set.
