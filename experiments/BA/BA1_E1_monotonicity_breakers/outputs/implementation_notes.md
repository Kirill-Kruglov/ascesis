# BA1.E1 Implementation Notes

No Justitia source file was modified.

## Fixed Inputs

- Justitia model path: `/home/master/llm_projects/justitia/model/substrate.py`.
- Collapse predicate unchanged: `mean(zone_welfare)<0.32 OR count(zone_welfare<0.20)>=4 OR total_mass<35`.
- 18.0 shield abstraction unchanged: `ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)`.
- Projection unchanged from 18.1: `a = round(A_collapse*(1-mean_welfare)/(1-0.32))`, `c = round(resource_hhi*Cmax)`.
- Bounded-coupling doomed set is computed by the existing 18.0 `compute_doomed`; in this setting it is U-only.

## Ground Truth

- `future_collapse` means real collapse occurs at the current or later step in the same trajectory.
- `false_safe_rate = P(future_collapse | shield says SAFE)`.
- `false_unsafe_rate = P(no future_collapse | shield says DOOMED)`.
- `pure_blindness` is the rate of currently-collapsed states labelled SAFE by the unchanged 18.0 shield.

## Run Grid

- Worlds: `['W1_proxy_goodhart', 'W2_pure_capture', 'W3_catastrophe_ambiguity', 'W4_scavenger_catastrophe', 'W5_monoculture_shock', 'W6_mutation_corridor']`.
- Policies: `['feature_proxy', 'consequence_neighbor', 'response_to_aid', 'action_channel_containment', 'consequence_plus_diversity']`.
- Seeds: `[9600, 9601, 9602, 9603, 9604, 9605, 9606, 9607]`.
- Steps per trajectory are Justitia's current `STEPS` constant.

## Ablation Caveats

- MB1 removes both delay and explicit memory observables from policy input.
- MB2 removes allocation competition by uniform per-zone allocation but keeps bad-consequence policy triggers.
- MB3 disables bad-consequence/audit interpretation.
- MB4 freezes lineage mass/adaptation and migration after immediate welfare dynamics are applied.
- MB5 neutralizes policy-visible concentration observables; measured resource HHI remains observable for diagnostics.
