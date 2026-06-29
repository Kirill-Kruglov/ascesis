# Representative False-Safe Witnesses

## spread_blind

Count: `724`.

| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |
|---|---|---|---:|---:|---|---:|---|---|---|---|
| spread_blind | W1_proxy_goodhart | feature_proxy | 9601 | 24 | spread | 24 | spread | failed_zone_count >= 4 | high | Current state already satisfies real spread-collapse clause, but 18.0 projection contains only mean-welfare/resource_hhi. |
| spread_blind | W1_proxy_goodhart | feature_proxy | 9604 | 24 | spread | 24 | spread | failed_zone_count >= 4 | high | Current state already satisfies real spread-collapse clause, but 18.0 projection contains only mean-welfare/resource_hhi. |
| spread_blind | W1_proxy_goodhart | feature_proxy | 9606 | 23 | spread | 23 | spread | failed_zone_count >= 4 | high | Current state already satisfies real spread-collapse clause, but 18.0 projection contains only mean-welfare/resource_hhi. |

## mass_blind

Count: `400`.

| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |
|---|---|---|---:|---:|---|---:|---|---|---|---|
| mass_blind | W5_monoculture_shock | action_channel_containment | 9600 | 23 | mass | 23 | mass | total_mass < 35 | high | Current state already satisfies real mass-collapse clause, but total_mass is absent from 18.0 projection. |
| mass_blind | W5_monoculture_shock | action_channel_containment | 9600 | 24 | mass | 24 | mass | total_mass < 35 | high | Current state already satisfies real mass-collapse clause, but total_mass is absent from 18.0 projection. |
| mass_blind | W5_monoculture_shock | action_channel_containment | 9600 | 25 | mass | 25 | mass | total_mass < 35 | high | Current state already satisfies real mass-collapse clause, but total_mass is absent from 18.0 projection. |

## mean_blind

Count: `0`.

No witnesses assigned to this class.

## forward_dynamics_blind

Count: `1364`.

| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |
|---|---|---|---:|---:|---|---:|---|---|---|---|
| forward_dynamics_blind | W1_proxy_goodhart | feature_proxy | 9600 | 0 | none | 24 | spread | bounded future reachability / time-to-collapse | high | Current concrete state is not collapsed; false-safe status comes from later concrete collapse under future dynamics. |
| forward_dynamics_blind | W1_proxy_goodhart | feature_proxy | 9600 | 1 | none | 24 | spread | bounded future reachability / time-to-collapse | high | Current concrete state is not collapsed; false-safe status comes from later concrete collapse under future dynamics. |
| forward_dynamics_blind | W1_proxy_goodhart | feature_proxy | 9600 | 2 | none | 24 | spread | bounded future reachability / time-to-collapse | high | Current concrete state is not collapsed; false-safe status comes from later concrete collapse under future dynamics. |

## history_blind

Count: `1932`.

| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |
|---|---|---|---:|---:|---|---:|---|---|---|---|
| history_blind | W1_proxy_goodhart | feature_proxy | 9600 | 12 | none | 24 | spread | delayed response_to_aid / neighbor_delta / last_aid | medium | Delayed response/neighbor/last-aid history carries a harmful consequence signal absent from the 18.0 projection. |
| history_blind | W1_proxy_goodhart | feature_proxy | 9600 | 13 | none | 24 | spread | delayed response_to_aid / neighbor_delta / last_aid | medium | Delayed response/neighbor/last-aid history carries a harmful consequence signal absent from the 18.0 projection. |
| history_blind | W1_proxy_goodhart | feature_proxy | 9600 | 14 | none | 24 | spread | delayed response_to_aid / neighbor_delta / last_aid | medium | Delayed response/neighbor/last-aid history carries a harmful consequence signal absent from the 18.0 projection. |

## control_blind

Count: `0`.

No witnesses assigned to this class.

## policy_visible_concentration_blind

Count: `1115`.

| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |
|---|---|---|---:|---:|---|---:|---|---|---|---|
| policy_visible_concentration_blind | W1_proxy_goodhart | feature_proxy | 9600 | 3 | none | 24 | spread | Obs.resource_concentration > 0.62 | medium | Delayed policy-visible resource concentration crosses the bad-consequence threshold, distinct from reporting HHI. |
| policy_visible_concentration_blind | W1_proxy_goodhart | feature_proxy | 9600 | 4 | none | 24 | spread | Obs.resource_concentration > 0.62 | medium | Delayed policy-visible resource concentration crosses the bad-consequence threshold, distinct from reporting HHI. |
| policy_visible_concentration_blind | W1_proxy_goodhart | feature_proxy | 9600 | 5 | none | 24 | spread | Obs.resource_concentration > 0.62 | medium | Delayed policy-visible resource concentration crosses the bad-consequence threshold, distinct from reporting HHI. |

## layer_confusion_blind

Count: `0`.

No witnesses assigned to this class.

## unknown_or_mixed

Count: `304`.

| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |
|---|---|---|---:|---:|---|---:|---|---|---|---|
| unknown_or_mixed | W1_proxy_goodhart | feature_proxy | 9604 | 18 | none | 24 | spread | multiple or unresolved missing coordinates | medium | Future collapse state has multiple plausible missing coordinates, so no single minimal candidate is defensible. |
| unknown_or_mixed | W1_proxy_goodhart | feature_proxy | 9604 | 20 | none | 24 | spread | multiple or unresolved missing coordinates | medium | Future collapse state has multiple plausible missing coordinates, so no single minimal candidate is defensible. |
| unknown_or_mixed | W1_proxy_goodhart | feature_proxy | 9604 | 22 | none | 24 | spread | multiple or unresolved missing coordinates | medium | Future collapse state has multiple plausible missing coordinates, so no single minimal candidate is defensible. |
