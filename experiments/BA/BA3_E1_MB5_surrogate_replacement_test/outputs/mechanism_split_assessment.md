# BA3.E1 Mechanism Split Assessment

MB5 is not a single clean implementation mechanism.

| subfamily | run | interpretation |
|---|---|---|
| S4a | `S4a_policy_visible_concentration` | policy-visible concentration can be isolated via `Obs.resource_concentration`; compare false-safe and witness deltas. Observed false-safe `0.3117`, witnesses `5652`. |
| S4b | `S4b_reporting_ratios` | reporting ratios affect diagnostics/output only; success here is not transition-level evidence. Observed false-safe `0.3525`, witnesses `2764`. |
| S4c | `S4c_projection_resource_hhi` | 18.0 projection-visible `resource_hhi`; expected weak effect because current doomed set is U-only. Observed false-safe `0.3525`, witnesses `2753`. |
| S4d | `S4d_capture_components` | capture-index components are reporting/diagnostic unless fed into a policy. Observed false-safe `0.3525`, witnesses `3081`. |

Split verdict: policy-visible and projection/reporting roles should be kept separate in future taxonomy. A reporting-only win is not evidence that transition-level MB5 is safe to remove.
