# FA1.E1 False-Safe Witness Taxonomy

Diagnostic-only experiment. Justitia source, concrete collapse definition, and the 18.0 shield were not modified.

## Decision

Classification: **Case C — History_control_dominant**.
Interpretation: A large fraction requires delayed observation, policy-visible concentration, or control state.
H_FA1 assessment: `supported`.

## Baseline Extraction

- States harvested: `24000`.
- Shield SAFE states: `16563` (`0.690125`).
- Future-collapse states: `0.553167`.
- False-safe witnesses: `5839` (`0.352533` over SAFE states).
- Current-collapse false-safe witnesses: `1124`.
- Future-dynamics false-safe witnesses: `4715`.

## Witness Classes

| class | count | fraction |
|---|---:|---:|
| history_blind | 1932 | 0.330879 |
| forward_dynamics_blind | 1364 | 0.233602 |
| policy_visible_concentration_blind | 1115 | 0.190957 |
| spread_blind | 724 | 0.123994 |
| mass_blind | 400 | 0.068505 |
| unknown_or_mixed | 304 | 0.052064 |
| control_blind | 0 | 0.000000 |
| layer_confusion_blind | 0 | 0.000000 |
| mean_blind | 0 | 0.000000 |

## Primary Metrics

- Omitted real collapse clauses (`spread_blind + mass_blind`): `1124`.
- History/control/concentration witnesses: `3047`.
- Layer-confusion witnesses: `0`.
- Unknown/mixed fraction: `0.052064`.
- Class entropy: `2.334520` bits.

## Minimal Information Candidates

| rank | candidate | count | fraction | cumulative fraction |
|---:|---|---:|---:|---:|
| 1 | delayed response_to_aid / neighbor_delta / last_aid | 1932 | 0.330879 | 0.330879 |
| 2 | bounded future reachability / time-to-collapse | 1364 | 0.233602 | 0.564480 |
| 3 | Obs.resource_concentration > 0.62 | 1115 | 0.190957 | 0.755438 |
| 4 | failed_zone_count >= 4 | 724 | 0.123994 | 0.879431 |
| 5 | total_mass < 35 | 400 | 0.068505 | 0.947936 |
| 6 | multiple or unresolved missing coordinates | 304 | 0.052064 | 1.000000 |

## BA4.1 Layer Eligibility

| layer eligibility | count | fraction |
|---|---:|---:|
| conditional L2/L3 | 3047 | 0.521836 |
| L4 plus conditional L1 temporal | 1364 | 0.233602 |
| L4 eligible | 1124 | 0.192499 |
| unknown/mixed | 304 | 0.052064 |

## Falsification Checks

- Top-3 candidate coverage: `0.755438`.
- Unknown/mixed fraction: `0.052064`.
- Layer-ineligible fraction: `0.000000`.

No safety claim is made here. This experiment maps missing information only; it does not synthesize or recommend a new shield.
