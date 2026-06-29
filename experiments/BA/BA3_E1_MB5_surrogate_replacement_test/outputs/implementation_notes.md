# BA3.E1 Implementation Notes

- Justitia source files were not modified.
- BA1 baseline and BA1 MB5 removal summaries were reused exactly and copied into BA3 outputs.
- New surrogate variants were run on the BA1 diagnostic grid unless otherwise noted.
- Worlds: `['W1_proxy_goodhart', 'W2_pure_capture', 'W3_catastrophe_ambiguity', 'W4_scavenger_catastrophe', 'W5_monoculture_shock', 'W6_mutation_corridor']`.
- Policies: `['feature_proxy', 'consequence_neighbor', 'response_to_aid', 'action_channel_containment', 'consequence_plus_diversity']`.
- Seeds: `[9600, 9601, 9602, 9603, 9604, 9605, 9606, 9607]`.
- 18.0 shield parameters/projection are reused from BA1.
- `S4c_projection_resource_hhi` is implemented as a harness-side projection wrapper, not a Justitia transition subclass.

## Wrapper Functions

- S1/S2/S3 override `_resource_hhi_zone` and `_apparent_cooperation`.
- S4a overrides `_observe` only.
- S4b overrides `_trajectory_snapshot` and `metrics` only.
- S4d overrides capture-index reporting in `_trajectory_snapshot` and `metrics`.
