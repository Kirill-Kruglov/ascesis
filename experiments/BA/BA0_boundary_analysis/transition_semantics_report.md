# BA0.2 - Justitia Transition Semantics Extraction

Source inspected: `/home/master/llm_projects/justitia/`.

No Justitia code was modified and no new experiments were run. The transition semantics are concentrated in:

- `/home/master/llm_projects/justitia/model/substrate.py`
- `/home/master/llm_projects/justitia/model/governance.py`
- `/home/master/llm_projects/justitia/model/families.py`
- `/home/master/llm_projects/justitia/model/atlas.py`

`emit_explorable.py` and result/report files read or aggregate trajectories; they do not define additional environment transition rules.

## State Variables

Per-zone state:

- `Zone.wellness`
- `Zone.productivity`
- `Zone.recovery`
- `Zone.migration_capacity`
- `Zone.lineages`
- `Zone.containment_timer`
- `Zone.last_aid`
- `Zone.last_response`
- `Zone.neighbor_delta`
- cumulative counters: `neighbor_harm_volume`, `aid_interception_volume`, `extraction_volume`, `containment_events`, `containment_cost`, `false_containment`, `migration_events`, mutation/payoff counters.

Per-lineage state:

- `Lineage.mass`
- `Lineage.strategy`
- `Lineage.resource_stock`
- `Lineage.last_payoff`
- `Lineage.mutation_var`

Derived welfare/mass metrics:

- zone welfare: `(wellness + productivity + recovery) / 3`
- mean welfare: `safe_mean(zone_welfare)`
- minimum zone welfare: `min(zone_welfare)`
- zone mass: `sum(lineage.mass for lineage in zone.lineages)`
- total mass: `sum(zone_mass) + EPS`
- failed zones: zones where `min(wellness, productivity, recovery) < 0.18` or `zone_mass < 4.0`

## Rule 1 - World Initialization

1. Source: `model/substrate.py`, `EvolvableStrategyModel._base_zone`, `EvolvableStrategyModel._init_world`.
2. Inputs: `seed`, `Params.world`, `ZONES`, initial strategy templates, random draws.
3. Update:

```text
base zone:
  wellness ~ U(0.64, 0.78)
  productivity ~ U(0.62, 0.80)
  recovery ~ U(0.50, 0.70)
  migration_capacity ~ U(0.48, 0.70)
  lineages = [cooperative mass 18, resilient_mutant mass 4]

world-specific edits:
  W1: add deceptive_exploit mass 16 to zones 1,4,7
  W2: add pure_extractor mass 20 to zones 1,4,7; wellness *= 0.82
  W3: zones 0,3 catastrophe=True, welfare components set low; zones 1,4 add deceptive_exploit and wellness=0.38
  W4: zones 0,3 catastrophe=True with low wellness/productivity and scavenger mass 15; zones 1,4 add scavenger mass 10
  W5: replace each zone with productive_mono mass 28 + cooperative mass 1; productivity=0.90, wellness=0.78
  W6: add resilient_mutant mass 8 to zones 2,5,8; pure_extractor mass 8 to zones 1,4,7
```

4. Trigger: model construction.
5. Worse states get stronger corrective response: no; this is initial condition, not corrective.
6. Monotone under deficit order: not applicable as a transition from prior state; across worlds it is not monotone because worse worlds also change hidden strategy composition.
7. Minimal counterexample shape: W2 lowers wellness but increases exploit mass; W3 lowers welfare and flags catastrophe; neither is an ordered single-coordinate deficit.

## Rule 2 - Robust Initialization Perturbations

1. Source: `model/governance.py`, `RobustModel._init_world`; `model/families.py`, `AntiConcentrationVsConsequenceModel._init_world`.
2. Inputs: `adversarial_pressure`, `initial_exploit_mass_scale`, `initial_resource_concentration_scale`, `resource_concentration_pressure`.
3. Update:

```text
if adversarial_pressure != 1:
  for exploit_score(lineage) > 0.30:
    multiply exploit-like strategy fields by adversarial_pressure

if initial_exploit_mass_scale != 1:
  for exploit_score(lineage) > 0.42:
    lineage.mass *= initial_exploit_mass_scale

if initial_resource_concentration_scale > 1:
  largest lineage in each zone mass *= scale
elif scale < 1:
  lineage.mass = lineage.mass * scale + equal_zone_mass * (1 - scale)

families resource_concentration_pressure:
  largest lineage in each zone mass *= resource_concentration_pressure
```

4. Trigger: robust/atlas/family model construction.
5. Worse states get stronger corrective response: no; these are scenario perturbations.
6. Monotone under deficit order: no. Increasing exploit mass can raise total mass while worsening future welfare/capture.
7. Minimal counterexample shape: two states identical except one has larger exploit mass. It has higher total mass, but stronger extraction later can lower welfare.

## Rule 3 - Observation and Delayed Signal

1. Source: `model/substrate.py`, `EvolvableStrategyModel._observe`, `_delayed_obs`.
2. Inputs: current zone components, prior `last_aid`, `last_response`, `neighbor_delta`, lineages.
3. Update:

```text
Obs.wellness[i] = z.wellness
Obs.productivity[i] = z.productivity
Obs.recovery[i] = z.recovery
Obs.sag[i] = 1 if min(wellness, productivity, recovery) < 0.42 else 0
Obs.global_welfare = mean((wellness + productivity) / 2)
obs_queue appends current observation; policy reads delayed obs_queue[0]
```

4. Trigger: initialization and each `step`.
5. Worse states get stronger corrective response: indirectly, because `sag` and `need` in scoring use this observation.
6. Monotone under deficit order: observation itself is monotone for direct components, but delayed observation can break monotone response to current deficits.
7. Minimal counterexample shape: state A is currently worse than B, but A had a better delayed observation; policy allocates less support to A.

## Rule 4 - Policy Score

1. Source: `model/substrate.py`, `EvolvableStrategyModel._score`; `model/governance.py`, `RobustModel._score`; `model/families.py`, `_static_score_a`, `_score_b`, `_score_c`; `model/atlas.py`, `_score_c_no_consequence`, `_score_c`.
2. Inputs: delayed observation, policy name, ablation, response diversity, resource concentration, zone mass share, bad-consequence predicate.
3. Base update:

```text
need = 1 - min(obs.wellness[i], obs.productivity[i], obs.recovery[i])

feature_proxy:
  score = 2.0 * apparent_cooperation + 0.15 * need

consequence_neighbor:
  score = 0.75 * need + 2.4 * neighbor_delta + 0.35 * response_to_aid

response_to_aid:
  probe = 0.45 if obs.sag[i] and obs.last_aid[i] < 0.04 else 0
  score = 0.8 * need + 2.2 * response_to_aid + probe

action_channel_containment:
  bad = _bad_consequence(obs, i)
  score = 0.85 * need + 1.6 * neighbor_delta + 0.55 * response_to_aid - 0.65 * bad

consequence_plus_diversity:
  div_gap = max(0, diversity_floor - response_diversity)
  score = 0.75 * need + 1.7 * neighbor_delta + 0.65 * response_to_aid + div_gap - 0.45 * bad
```

Governance ablations replace or remove terms:

```text
feature_proxy_only: apparent_cooperation
random_allocation: random()
no_neighbor_consequence: 0.80*need + 0.60*response_to_aid + 0.85*div_gap
no_response_to_aid: 0.75*need + 1.7*neighbor_delta + 0.95*div_gap
no_diversity_support: remove div_gap
no_containment: remove bad penalty/containment trigger
```

Families:

```text
Part A static anti-concentration:
  uniform_resource_cap: 1
  max_zone_share_cap: 1 - zone_mass_share
  max_lineage_share_cap: 1 - max_lineage_share_zone
  anti_hhi_allocator: 1 - resource_hhi_zone
  static_equalizing_allocator: 1 / max(0.05, zone_mass) + 0.25*(1-resource_hhi_zone)

Part B consequence:
  neighbor_consequence_allocator: 0.75*need + 2.4*neighbor_delta
  response_to_aid_allocator: 0.80*need + 2.2*response_to_aid + probe
  delayed_harm_throttle: 0.85*need + 1.8*neighbor_delta + 0.35*response_to_aid - 0.55*bad

Part C anti-concentration + consequence:
  anti = 0.75*(1-resource_hhi_zone) + 0.35*(1-zone_mass_share)
  score = anti + consequence terms
```

4. Trigger: `choose_alloc`.
5. Worse states get stronger corrective response: partially. Lower wellness/productivity/recovery increases `need`, but negative `neighbor_delta`, negative `response_to_aid`, `bad`, high concentration caps, or random allocation can dominate.
6. Monotone under deficit order: generally no. The score is monotone in `need` holding other terms fixed, but not under the full state order.
7. Minimal counterexample shape: Zone A has lower welfare than B but also negative delayed `neighbor_delta` or `bad=True`; with `action_channel_containment`, A can receive lower score than B.

## Rule 5 - Bad Consequence Trigger

1. Source: `model/substrate.py`, `EvolvableStrategyModel._bad_consequence`.
2. Inputs: delayed observation for zone `i`.
3. Update:

```text
bad = obs.last_aid[i] > 0.035 and (
  obs.neighbor_delta[i] < -0.030
  or obs.response_to_aid[i] < -0.025
  or obs.resource_concentration[i] > 0.62
)
```

4. Trigger: scoring, containment timer activation, audit trigger.
5. Worse states get stronger corrective response: not directly; it reacts to harmful response after aid and concentration, not raw welfare deficit.
6. Monotone under deficit order: no. A worse low-welfare zone with no prior aid can have `bad=False`; a better zone with high concentration after aid can have `bad=True`.
7. Minimal counterexample shape: A has low welfare and no last aid; B has higher welfare, last aid > 0.035, high HHI. B triggers containment, A does not.

## Rule 6 - Allocation Normalization, Floors, Caps, Redistribution

1. Source: `model/substrate.py`, `EvolvableStrategyModel.choose_alloc`; `model/governance.py`, `RobustModel.choose_alloc`; `model/families.py`, `AntiConcentrationVsConsequenceModel.choose_alloc`, `_apply_cap`; `model/atlas.py`, `BoundaryAtlasModel.choose_alloc`.
2. Inputs: scores, policy, containment timers, caps, floors.
3. Base update:

```text
scores = [_score(obs, i)]
shifted[i] = max(0.01, scores[i] - min(scores) + 0.04)
floor = 0.018 unless feature_proxy else 0
alloc = normalize(shifted, total=1 - floor*ZONES)
alloc[i] += floor

if action-channel policy:
  cap = 0.18 if zone containment_timer > 0 else 0.32
  excess above cap is redistributed equally to receivers with capped allocation < 0.24
  alloc = normalize(capped)
```

Families:

```text
_apply_cap:
  cap = cap_share + 0.08*(1-cap_strength)
  excess above cap redistributed equally to below-cap receivers
```

Atlas variants:

```text
C_dyn_no_consequence:
  score = anti + need only; no caps
C_dyn_only:
  consequence score; no caps
C_caps_only:
  maps dynamics to action_channel_containment with no anti-concentration
```

4. Trigger: each `step`.
5. Worse states get stronger corrective response: only through score. Caps can prevent stronger response to the worst zone.
6. Monotone under deficit order: no globally. Normalization is relative; increasing one zone's need can reduce all other zones' allocations.
7. Minimal counterexample shape: one zone becomes worse, its allocation rises, but another already-failed zone loses allocation because the budget is fixed.

## Rule 7 - Containment Timer and Containment Event Updates

1. Source: `model/substrate.py`, `choose_alloc`, `_apply_zone_dynamics`; `model/governance.py`, `choose_alloc`, `_apply_zone_dynamics`; `model/families.py`, `choose_alloc`; `model/atlas.py`, `choose_alloc`.
2. Inputs: `bad`, `policy`, `audit_intervention`, `containment_strength`, `containment_duration`, `mode`.
3. Update:

```text
if policy in action-channel family and _bad_consequence(obs, i):
  z.containment_timer = max(z.containment_timer, containment_duration)
  z.containment_events += 1
  z.containment_cost += coefficient * containment_strength * action_channel_cost_scale

in _apply_zone_dynamics:
  containment = z.containment_timer > 0 or (mode == audit and _audit_trigger(...))
  if containment:
    containment_cost += 0.025 * strength
    if z.catastrophe: false_containment += 1
  if z.containment_timer > 0: z.containment_timer -= 1
```

4. Trigger: bad consequence, audit trigger, or active timer.
5. Worse states get stronger corrective response: not directly; response is stronger to bad consequence signals, not necessarily lower welfare.
6. Monotone under deficit order: no. Low welfare alone does not trigger containment.
7. Minimal counterexample shape: a catastrophic low-welfare zone with no bad delayed signal receives no containment; a healthier high-HHI zone with bad signal receives containment.

## Rule 8 - Audit Oracle Suppression

1. Source: `model/substrate.py`, `EvolvableStrategyModel._apply_audit_oracle`.
2. Inputs: `audit_intervention`, lineages, `exploit_score`.
3. Update:

```text
if audit_intervention == oracle_suppress_exploit_strategy_params:
  for exploit_score(lineage) > 0.42:
    extraction_rate *= 0.18
    aid_interception_rate *= 0.18
    neighbor_harm_rate *= 0.18
    deception_investment *= 0.28
    replication_aggressiveness *= 0.42
    lineage.mass *= 0.25
    z.containment_events += 1
```

4. Trigger: every `step` in audit mode with oracle intervention.
5. Worse states get stronger corrective response: no; response targets exploit score, not deficit.
6. Monotone under deficit order: no. It can reduce total mass in an already low-mass zone if exploit lineages dominate.
7. Minimal counterexample shape: two zones equally poor; only one contains high exploit-score lineage and loses 75% of that lineage mass.

## Rule 9 - Type-Blind Audit Trigger

1. Source: `model/substrate.py`, `_audit_trigger`, `_audit_active`; effects in `_apply_zone_dynamics`.
2. Inputs: audit intervention name, bad consequence, zone state.
3. Update:

```text
if audit_intervention in type_blind_*:
  trigger = _bad_consequence(obs, i)
  containment features activated according to intervention:
    extraction_cap
    aid_escrow
    anti_concentration
    migration_friction
    replication_throttle
    combined_type_blind_containment
```

4. Trigger: audit mode and bad consequence.
5. Worse states get stronger corrective response: not by welfare deficit; by bad-consequence signal.
6. Monotone under deficit order: no, for same reason as Rule 5.
7. Minimal counterexample shape: lower welfare but no prior-aid harm is untreated; higher welfare but high post-aid concentration is treated.

## Rule 10 - Shocks

1. Source: `model/substrate.py`, `EvolvableStrategyModel._apply_shocks`; `model/governance.py`, `RobustModel._apply_shocks`.
2. Inputs: `world`, `step`, `catastrophe`, weighted resilience, strategy diversity, `catastrophe_severity`.
3. Update:

```text
W3/W4 at steps 22,45 for catastrophe zones:
  hit = 0.30 * (1 - 0.55 * weighted_resilience)
  wellness -= hit
  productivity -= 0.8*hit
  recovery -= 0.7*hit

W5 at step 50 if strategy_diversity < 0.25:
  wellness *= 0.32
  productivity *= 0.25
  recovery *= 0.42

W5 after step 50 if strategy_diversity < 0.35:
  wellness -= 0.030
  productivity -= 0.026

RobustModel severity:
  actual drop = base drop * catastrophe_severity
```

4. Trigger: world-specific shock times and diversity/catastrophe conditions.
5. Worse states get stronger corrective response: no; this is adverse dynamics. More resilience reduces damage.
6. Monotone under deficit order: no as a corrective rule; shocks can make already weak zones worse.
7. Minimal counterexample shape: two equal low-welfare zones, one catastrophe flagged or low-diversity; only that zone receives shock.

## Rule 11 - Aid Escrow Support

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; `model/governance.py`, `RobustModel._apply_zone_dynamics`.
2. Inputs: `raw_aid`, containment, policy/audit feature flags, `strength`, welfare/productivity/recovery.
3. Update:

```text
if aid_escrow and min(wellness, productivity, recovery) < 0.58:
  escrowed = raw_aid * 0.58 * strength
  aid_for_lineages -= escrowed
  wellness += 0.20 * escrowed
  productivity += 0.14 * escrowed
  recovery += 0.18 * escrowed
  containment_cost += 0.05 * escrowed
```

4. Trigger: containment active and aid-escrow feature active and min component < 0.58.
5. Worse states get stronger corrective response: thresholded yes; below 0.58 receives escrow support. Magnitude still depends on allocation and containment, not deficit depth.
6. Monotone under deficit order: partly. Holding raw aid fixed, worse below threshold gets same escrow amount, not more; zones just above threshold get none.
7. Minimal counterexample shape: A min=0.57 and B min=0.30 with same raw aid receive equal escrow boost; B remains worse but not stronger response.

## Rule 12 - Anti-Concentration Aid Reduction

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; `model/governance.py`, `RobustModel._apply_zone_dynamics`.
2. Inputs: containment, resource HHI, `strength`, `raw_aid`.
3. Update:

```text
if anti_concentration and resource_hhi_zone > 0.46:
  aid_for_lineages *= max(0.18, 1 - 0.70*strength)
  containment_cost += 0.02 * raw_aid
```

4. Trigger: containment active and high lineage/resource concentration.
5. Worse states get stronger corrective response: not by deficit; it suppresses aid to concentrated lineage structures.
6. Monotone under deficit order: no. A low-mass/welfare zone with high HHI can lose lineage-directed aid.
7. Minimal counterexample shape: an impoverished single-lineage zone has high HHI and loses aid_for_lineages; a richer diversified zone does not.

## Rule 13 - Extraction, Interception, Useful Aid, Neighbor Harm

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; mirrored in `model/governance.py`.
2. Inputs: aid_for_lineages, zone mass, weighted extraction/interception/harm, containment cap factors.
3. Update:

```text
cap_factor = max(0.08, 1 - 0.78*strength) if extraction_cap else 1
harm_factor = max(0.10, 1 - 0.75*strength) if containment else 1

extracted = aid_for_lineages * weighted_extract * cap_factor
intercepted = aid_for_lineages * weighted_intercept * cap_factor
useful = max(0, aid_for_lineages - 0.55*extracted - 0.65*intercepted)
neighbor_harm = zone_mass * weighted_harm * 0.010 * harm_factor
```

4. Trigger: every zone dynamics update.
5. Worse states get stronger corrective response: no. Extraction/interception/harm are strategy/mass driven.
6. Monotone under deficit order: no. Lower mass lowers neighbor harm, but lower welfare does not reduce extraction; higher mass can worsen neighbors.
7. Minimal counterexample shape: A has lower welfare but cooperative strategies; B has higher welfare and high exploit strategies. B produces larger harm despite being less deficient.

## Rule 14 - Direct Zone Welfare Component Updates

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; mirrored in `model/governance.py`.
2. Inputs: useful aid, weighted cooperation/productivity/resilience, extracted/intercepted aid, weighted harm.
3. Update:

```text
before_state = mean(wellness, productivity, recovery)

wellness =
  clamp(wellness + 0.13*useful + 0.030*weighted_coop - 0.055*extracted - 0.035*weighted_harm)

productivity =
  clamp(productivity + 0.11*useful + 0.040*weighted_prod - 0.050*intercepted - 0.026*weighted_harm)

recovery =
  clamp(recovery + 0.12*useful + 0.050*weighted_res - 0.028*extracted)

last_response = after_state - before_state
```

4. Trigger: every zone dynamics update.
5. Worse states get stronger corrective response: only via allocation/useful aid; the local formula itself does not multiply by deficit.
6. Monotone under deficit order: not guaranteed. Clamping and harmful strategy terms can make lower-welfare zones improve less.
7. Minimal counterexample shape: A has lower welfare but high extraction/harm strategies; B has higher welfare and cooperative strategies. A receives aid but extracted term dominates, so its welfare drops.

## Rule 15 - Neighbor Welfare Damage

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; mirrored in `model/governance.py`.
2. Inputs: `neighbor_harm`, neighbor indices.
3. Update:

```text
for neighbor n of zone i:
  n.wellness -= 0.58 * neighbor_harm
  n.productivity -= 0.45 * neighbor_harm
  n.recovery -= 0.30 * neighbor_harm
```

4. Trigger: every zone dynamics update.
5. Worse states get stronger corrective response: no; this is harm propagation.
6. Monotone under deficit order: no. A high-mass harmful zone can damage already failed neighbors.
7. Minimal counterexample shape: two states differ only by neighbor mass/harm. The state with more mass can suffer lower neighbor welfare despite higher total mass.

## Rule 16 - Lineage Payoff

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; scaled in `model/governance.py`.
2. Inputs: useful aid, extracted/intercepted aid, neighbor harm, strategy fields, containment feature flags.
3. Update:

```text
exploit_component =
  0.45*extraction_rate*extracted
  + 0.55*aid_interception_rate*intercepted
  + 0.40*neighbor_harm_rate*neighbor_harm*10

coop_component =
  0.20*cooperation*useful
  + 0.16*productive*useful
  + 0.12*resilience*(1 if catastrophe else 0.25)

deception_cost = 0.030*deception
channel_penalty = sum(containment feature penalties)
payoff = share*useful*0.08 + exploit_component + coop_component - deception_cost - channel_penalty
```

Governance scales exploit payoff components by `extraction_payoff_scale`, `interception_payoff_scale`, `harm_payoff_scale`.

4. Trigger: every lineage in every zone dynamics update.
5. Worse states get stronger corrective response: no. It rewards strategy-channel payoff unless containment penalties offset.
6. Monotone under deficit order: no. Exploitative behavior may receive positive payoff in harmed/worse zones.
7. Minimal counterexample shape: zone with low welfare and high aid lets exploit lineages intercept/extract more, increasing exploit payoff.

## Rule 17 - Lineage Mass Growth, Resource Stock, Pruning

1. Source: `model/substrate.py`, `_apply_zone_dynamics`; mirrored in `model/governance.py`.
2. Inputs: payoff, replication aggressiveness, resource HHI, replication throttle.
3. Update:

```text
growth = 1 + 0.015 + 0.085*payoff + 0.035*replication_aggressiveness - 0.020*resource_hhi_zone
if replication_throttle:
  growth -= 0.16*strength

lineage.mass = max(0.01, min(180, lineage.mass * max(0.20, growth)))
resource_stock = 0.80*resource_stock + 0.20*max(0, payoff)
remove lineages with mass <= 0.02
sort by mass descending
keep top 14 lineages
```

4. Trigger: every lineage update.
5. Worse states get stronger corrective response: no.
6. Monotone under deficit order: no. Total mass can grow in worse states if exploit payoff is high; total mass can shrink under throttle/pruning.
7. Minimal counterexample shape: two equal low-welfare zones; exploit-dominated one gains mass from extraction payoff, cooperative one has lower payoff and grows less.

## Rule 18 - Mutation

1. Source: `model/substrate.py`, `_mutate_strategy`, `_apply_zone_dynamics`; `model/governance.py`, `RobustModel._mutate_strategy`.
2. Inputs: mutation rate, lineage mass, mutation variance, exploit mutation bias.
3. Update:

```text
if random() < mutation_rate and lineage.mass > 2:
  child.mass = lineage.mass * 0.045
  lineage.mass *= 0.955
  child.strategy[k] = clamp(parent.strategy[k] + gaussian(0, mutation_var))
  child.mutation_var = clamp(parent.mutation_var + gaussian(0, 0.006), 0.008, 0.080)

RobustModel exploit_mutation_bias:
  increase exploit fields on child
  decrease cooperation/productive fields by 0.5*bias
```

4. Trigger: stochastic per-lineage mutation.
5. Worse states get stronger corrective response: no.
6. Monotone under deficit order: no. Mutation may create more exploitative children in worse or better states.
7. Minimal counterexample shape: identical states except random mutation creates exploit-biased child in one, lowering future welfare.

## Rule 19 - Migration and Local Mass Redistribution

1. Source: `model/substrate.py`, `EvolvableStrategyModel._migrate`.
2. Inputs: zone migration capacity, lineage migration_follow_rate, containment timer, policy.
3. Update:

```text
rate = 0.012 * migration_capacity * migration_follow_rate
if friction:
  rate *= 0.30
movers = lineage.mass * rate
lineage.mass -= movers
destination neighbor receives new lineage mass = movers * 0.96
child.resource_stock = parent.resource_stock * 0.5
```

4. Trigger: every step after zone dynamics, if movers > 0.01.
5. Worse states get stronger corrective response: no. Movement follows strategy and capacity, not deficit.
6. Monotone under deficit order: no. Migration loses 4% of moved mass and can move exploit strategies into weaker neighbors.
7. Minimal counterexample shape: low-mass zone loses its remaining mobile lineage to a neighbor; total mass decreases by migration loss.

## Rule 20 - Neighbor Consequence Metric Update

1. Source: `model/substrate.py`, `EvolvableStrategyModel._update_neighbor_metrics`.
2. Inputs: current and previous neighbor wellness/productivity/recovery.
3. Update:

```text
for each zone z:
  neighbor_delta =
    mean((neighbor.wellness - neighbor.prev_wellness)
       + (neighbor.productivity - neighbor.prev_productivity)
       + 0.5*(neighbor.recovery - neighbor.prev_recovery))
```

4. Trigger: after migration each step.
5. Worse states get stronger corrective response: indirect; negative neighbor_delta can reduce future allocation in some policies or indicate bad consequences.
6. Monotone under deficit order: no, because it uses change, not level.
7. Minimal counterexample shape: a very poor neighbor improves slightly, yielding positive delta; a healthier neighbor worsens slightly, yielding negative delta.

## Rule 21 - Failed-Zone Count and Irreversible Failure

1. Source: `model/substrate.py`, `EvolvableStrategyModel._update_irreversible`.
2. Inputs: per-zone welfare components and zone mass.
3. Update:

```text
failed = count_zones(
  min(wellness, productivity, recovery) < 0.18
  or zone_mass < 4.0
)
irreversible_failures = max(previous_irreversible_failures, failed)
if failed >= 4 and first_irrev < 0:
  first_irrev = step
```

4. Trigger: each step after neighbor metrics.
5. Worse states get stronger corrective response: no; this is accounting, not response.
6. Monotone under deficit order: yes for instantaneous `failed` if lower welfare/lower mass only. The stored `irreversible_failures` is path-dependent monotone in time.
7. Minimal counterexample shape: none for instantaneous threshold under the stated order. Path counterexample: two states with equal current values but different histories can have different `irreversible_failures`.

## Rule 22 - Step Ordering

1. Source: `model/substrate.py`, `EvolvableStrategyModel.step`.
2. Inputs: current model state, step index.
3. Update:

```text
_store_pre_step()
_apply_shocks(step)
if audit mode: _apply_audit_oracle()
obs = _delayed_obs()
alloc = choose_alloc()
for each zone:
  _apply_zone_dynamics(zone, BUDGET*alloc[i], alloc[i], obs, i)
_migrate()
_update_neighbor_metrics()
_update_irreversible(step)
obs_queue.append(_observe(step))
```

4. Trigger: each simulation step.
5. Worse states get stronger corrective response: only through subrules; no global monotone guarantee.
6. Monotone under deficit order: no. Shocks, delayed observations, relative allocation, migration, mutation, and strategy payoffs break global monotonicity.
7. Minimal counterexample shape: worse current state with better delayed observation and cooperative lineages can receive less aid but improve; better current state with exploit lineages can receive more aid and worsen.

## Rule 23 - Trajectory Snapshot Metrics

1. Source: `model/substrate.py`, `EvolvableStrategyModel._trajectory_snapshot`.
2. Inputs: current zones and lineages.
3. Update:

```text
zone_welfare[i] = (wellness + productivity + recovery)/3
zone_mass[i] = sum(lineage.mass)
total_mass = sum(zone_mass) + EPS
exploit_share = exploit_mass / total_mass
coop_capacity = coop_mass / total_mass
resource_hhi = sum((zone_mass / total_mass)^2)
welfare = mean(zone_welfare)
minimum_zone_welfare = min(zone_welfare)
collapse = mean(zone_welfare) < 0.32
        or count(zone_welfare < 0.20) >= 4
        or total_mass < 35
```

4. Trigger: after each step if `record_trajectory=True`.
5. Worse states get stronger corrective response: no; measurement only.
6. Monotone under deficit order: metrics are mostly monotone in welfare/mass, except ratio metrics can move non-monotonically when total mass changes.
7. Minimal counterexample shape: reducing mass in one exploit zone can lower total mass but also lower exploit_share/capture_index.

## Rule 24 - Final Metrics

1. Source: `model/substrate.py`, `EvolvableStrategyModel.metrics`.
2. Inputs: final zones, lineages, cumulative volumes, failure counters.
3. Update:

```text
zone_welfare = [(wellness + productivity + recovery)/3]
masses = [zone_mass]
total_mass = sum(masses) + EPS
welfare = mean(zone_welfare)
minimum_zone_welfare = min(zone_welfare)
resource_hhi = sum((m/total_mass)^2)
exploitative_strategy_mass = exploit_mass / total_mass
cooperative_strategy_mass = coop_mass / total_mass
collapse = 1 if mean(zone_welfare)<0.32 or count(w<0.20)>=4 or total_mass<35 else 0
permanence = 1 if not collapse and capture_index<=threshold and welfare>=0.55 and response_div>=0.35 and coop_capacity>0.18 else 0
irreversible_failures = stored max failed-zone count
```

4. Trigger: end of `run`.
5. Worse states get stronger corrective response: no; measurement only.
6. Monotone under deficit order: welfare/min welfare/collapse thresholds are monotone; capture and ratio components are not strictly monotone in total mass.
7. Minimal counterexample shape: removing exploit mass decreases total mass but can improve capture_index; lower total mass does not always mean worse capture metric.

## Rule 25 - Capture Index

1. Source: `model/substrate.py`, `_trajectory_snapshot`, `metrics`.
2. Inputs: `resource_hhi`, `exploit_share`, `neighbor_harm`, `aid_interception`, `coop_capacity`.
3. Update:

```text
capture_index =
  0.22 * clamp((resource_hhi - 1/ZONES)/0.35)
  + 0.28 * clamp(exploit_share/0.58)
  + 0.20 * clamp(neighbor_harm/0.18)
  + 0.15 * clamp(aid_interception/1.15)
  + 0.15 * clamp((0.42 - coop_capacity)/0.42)
```

4. Trigger: snapshot and final metrics.
5. Worse states get stronger corrective response: no; measurement.
6. Monotone under deficit order: no. It is not directly ordered by welfare/mass/failure.
7. Minimal counterexample shape: lower total mass caused by suppressing exploit lineages can reduce exploit share and capture index, even though mass deficit worsens.

## Rule 26 - Governance Ablation Dynamics

1. Source: `model/governance.py`, `RobustModel._apply_zone_dynamics`.
2. Inputs: ablation name and base dynamics inputs.
3. Update:

```text
no_containment: disables containment feature use
no_aid_escrow: disables escrow support
no_migration_friction: disables migration friction
no_replication_throttle: disables replication throttle
no_anti_concentration: disables anti-concentration aid reduction / extraction cap switch
action_channel_cost_scale: multiplies containment costs
extraction/interception/harm payoff scales multiply exploit payoff terms
```

4. Trigger: robust model runs.
5. Worse states get stronger corrective response: depends on enabled components; ablations can remove corrective response.
6. Monotone under deficit order: no.
7. Minimal counterexample shape: same low-welfare zone under `no_aid_escrow` receives no direct wellness/productivity/recovery boost that it receives under full.

## Rule 27 - Family A Static Anti-Concentration

1. Source: `model/families.py`, `AntiConcentrationVsConsequenceModel._static_score_a`, `choose_alloc`, `_apply_cap`.
2. Inputs: zone mass share, lineage share, HHI, cap strength/share.
3. Update:

```text
score is independent of welfare:
  uniform, inverse zone mass share, inverse max lineage share, inverse HHI, random, or static equalization
alloc = normalize(score-shift)
alloc capped by cap_share + 0.08*(1-cap_strength)
excess redistributed
dynamics run as consequence_neighbor with no_containment
```

4. Trigger: family A runs.
5. Worse states get stronger corrective response: only if worse means lower mass under equalizing allocator. Not welfare-responsive.
6. Monotone under deficit order: no for welfare; partially for lower mass under `static_equalizing_allocator`.
7. Minimal counterexample shape: low-welfare zone with high mass/concentration receives less than higher-welfare low-mass zone.

## Rule 28 - Family B Consequence Governance

1. Source: `model/families.py`, `_score_b`, `choose_alloc`, `_apply_zone_dynamics`.
2. Inputs: delayed consequences, need, bad consequence, no fixed caps.
3. Update:

```text
scores use need + neighbor_delta/response_to_aid/bad terms.
delayed_harm_throttle and consequence_weighted_migration_friction can set containment_timer on bad consequence.
dynamics temporarily map to action_channel_containment with no_anti_concentration.
```

4. Trigger: family B runs.
5. Worse states get stronger corrective response: partially through `need`, but no fixed cap/anti-concentration.
6. Monotone under deficit order: no because delayed consequence terms can dominate.
7. Minimal counterexample shape: worse zone with bad signal is penalized; better zone with positive response gets more allocation.

## Rule 29 - Family C Combined Anti-Concentration + Consequence

1. Source: `model/families.py`, `_score_c`, `choose_alloc`, `_apply_zone_dynamics`; `model/atlas.py`, `BoundaryAtlasModel`.
2. Inputs: anti-concentration score, need, delayed consequences, bad consequence, cap parameters.
3. Update:

```text
anti = 0.75*(1-resource_hhi_zone) + 0.35*(1-zone_mass_share)
score = anti + consequence terms
bad consequence can set containment_timer
alloc capped and redistributed
dynamics map to action_channel_containment full components

atlas variants:
  C_dyn_no_consequence: anti + need, no caps
  C_dyn_only: consequence dynamics without caps
  C_full: combined
  C_caps_only: action_channel_containment with no anti-concentration
```

4. Trigger: family C / atlas runs.
5. Worse states get stronger corrective response: partly via need and anti-concentration, but not purely welfare-based.
6. Monotone under deficit order: no. High concentration and low mass terms can override welfare need.
7. Minimal counterexample shape: lower-welfare high-HHI zone scores lower than higher-welfare low-HHI zone because anti term favors low concentration.

## Rule 30 - Explore Output Aggregation

1. Source: `model/emit_explorable.py`, representative trace extraction and aggregate summaries.
2. Inputs: completed model outputs and trajectories.
3. Update:

```text
final_welfare_mean = mean(final["welfare"])
final_min_welfare_mean = mean(final["minimum_zone_welfare"])
zone_mass trace = [snapshot["zone_mass"]]
zone_welfare trace = [snapshot["zone_welfare"]]
```

4. Trigger: explorable data emission.
5. Worse states get stronger corrective response: no; reporting only.
6. Monotone under deficit order: aggregation of welfare is monotone in welfare values, but not a transition.
7. Minimal counterexample shape: not applicable.

## Overall Monotonicity Assessment

The Justitia transition system is not monotone under the simple deficit order:

```text
worse = lower welfare, more failed zones, lower mass
```

The main reasons are:

1. Policy response reads delayed observations, not current state.
2. Allocation is relative and budget-normalized; helping one deficit can reduce support elsewhere.
3. Bad-consequence triggers are based on prior aid harm, neighbor delta, response-to-aid, and concentration, not raw welfare.
4. Exploitative lineages can gain mass/payoff in low-welfare states.
5. Anti-concentration can reduce lineage-directed aid in low-welfare but concentrated zones.
6. Migration redistributes mass with loss and can move harmful lineages into neighbors.
7. Ratio metrics such as exploit share, cooperative share, HHI, and capture index can improve when total mass falls.

The closest monotone subrules are:

- direct threshold accounting of instantaneous failed zones;
- need term `1 - min(wellness, productivity, recovery)` when all other score inputs are fixed;
- aid escrow threshold support once containment and allocation are fixed.

But the full transition map is not monotone because these monotone fragments are embedded in delayed, relative, strategy-dependent dynamics.

## Minimal Global Counterexample Shapes

1. Worse but not treated:
   - Zone A has lower current welfare but no delayed aid/bad-consequence signal.
   - Zone B has higher current welfare but prior aid caused negative neighbor delta or high concentration.
   - B receives containment/support response; A may not.

2. Worse and exploit-dominated:
   - Zone A has lower welfare and high exploit lineage mass.
   - It receives aid because of need.
   - Aid is extracted/intercepted, exploit payoff rises, total exploit mass grows, and welfare can fall.

3. Lower mass can improve capture:
   - Suppressing exploit lineages lowers total mass.
   - Under the deficit order this is worse by mass.
   - Capture index can improve because exploit share/harm/interception fall.

4. Budget competition:
   - One zone becomes worse and receives larger allocation.
   - A second failed zone receives less due to normalization and may cross the failure threshold.

5. Concentrated poor zone:
   - A low-welfare, low-diversity, high-HHI zone triggers anti-concentration.
   - Aid to lineages is reduced; direct escrow only occurs if containment and threshold conditions hold.
   - A richer but diversified zone can receive more effective lineage aid.
