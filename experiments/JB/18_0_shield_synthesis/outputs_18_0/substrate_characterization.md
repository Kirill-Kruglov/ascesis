# Substrate characterization — justitia (from the actual code)

Source read: `justitia/model/substrate.py` (`EvolvableStrategyModel`) and
`justitia/model/atlas.py` (`BoundaryAtlasModel`, families A/B/C). This characterizes
the **code**, not the essay's metaphors; where they differ, the code wins.

## State variables (what defines a configuration)

A configuration is `ZONES = 9` zones on a ring (`neighbors[i] = {i-1, i+1} mod 9`).
Each `Zone` holds (`substrate.py:122`):
- `wellness, productivity, recovery` ∈ [0,1] — the three welfare components (clamped);
- `migration_capacity`, `catastrophe` (bool);
- `lineages`: a list (≤14) of `Lineage(mass, strategy, resource_stock, …)`, where
  `strategy` is 9 continuous fields in [0,1] (`STRATEGY_FIELDS`: extraction_rate,
  aid_interception_rate, neighbor_harm_rate, deception_investment, migration_follow_rate,
  replication_aggressiveness, cooperation_investment, shock_resilience_contribution,
  productive_contribution);
- per-zone accumulators: `containment_timer`, `neighbor_harm_volume`,
  `aid_interception_volume`, `extraction_volume`, `containment_cost`, … (cumulative).

Derived per-zone quantities used downstream:
- **zone welfare** `(wellness+productivity+recovery)/3` (`_trajectory_snapshot:666`);
- **zone mass** `sum(l.mass for l in lineages)` (`_zone_mass`);
- **resource concentration** `_resource_hhi_zone` = Σ(share²) over lineage mass+stock — an HHI;
- strategy/response diversity (Shannon over post-hoc buckets).

## Transition dynamics (one `step`, `substrate.py:651`)

`_store_pre_step` → `_apply_shocks` → (audit oracle) → `choose_alloc` (allocate a fixed
`BUDGET = 6.0` across zones by a consequence/feature score, possibly with caps) →
`_apply_zone_dynamics` per zone (aid is extracted/intercepted by exploitative lineages,
useful aid raises welfare, neighbor harm lowers neighbors' welfare, lineages grow/shrink by
payoff, mutate, are pruned to ≤14) → `_migrate` → `_update_neighbor_metrics` →
`_update_irreversible`. The model is **stochastic** (per-seed RNG) and **high-dimensional**.

## The collapse / unsafe condition (the ACTUAL computational definition)

The essay speaks of "welfare of the worst-off region" and a permanence/survival measure.
In code there are two precise predicates:

1. **`collapse`** (`_trajectory_snapshot:683`, identical in `metrics:756`):
   ```
   collapse = mean(zone_welfare) < 0.32
              or sum(1 for w in zone_welfare if w < 0.20) >= 4
              or total_mass < 35
   ```
   This is the catastrophe set **U**. It is a monotone Boolean combination of threshold
   tests on degradation coordinates (mean welfare ↓, count of failed zones ↑, total mass ↓).

2. **`permanence`** (`metrics:757`) — the positive *survival/thriving* predicate:
   ```
   permanence = (collapse == 0) and capture_index <= capture_threshold
                and mean(zone_welfare) >= 0.55 and response_diversity >= 0.35
                and cooperative_strategy_mass > 0.18
   ```
   Permanence is strictly stronger than "not collapsed". For the **shield** the unsafe set
   is `collapse` (the catastrophe to be kept out of); permanence is the richer thriving
   target one would shield *toward*. A third, even stronger absorbing notion exists —
   `irreversible_failures` (`_update_irreversible:642`): a zone fails if
   `min(wellness,productivity,recovery) < 0.18 or zone_mass < 4`, and ≥4 failed zones marks
   first irreversibility. All three are monotone threshold predicates (upward-closed in the
   badness order).

`capture_index` (`metrics:749`) is a composite of resource-concentration, exploit-mass,
neighbor-harm, aid-interception and cooperation-loss components — the "accumulated harm"
aggregate.

## The two referee powers (as they appear in code)

- **scales = anti-concentration (concentration limit).** Lever `anti_concentration`
  (`_apply_zone_dynamics:530`): when a zone's resource HHI exceeds 0.46, aid to lineages is
  multiplied down by `max(0.18, 1 - 0.70*strength)`. Family **A** (`anti_hhi_allocator`,
  `atlas.py`) scores allocation by `1 - hhi`. Anti-concentration limits how much influence
  piles up → an **upward-closed** unsafe direction (more concentration is worse).

- **sword = consequence-gated response to observed harm.** Trigger `_bad_consequence`
  (`substrate.py:385`): `last_aid > 0.035 and (neighbor_delta < -0.030 or
  response_to_aid < -0.025 or resource_concentration > 0.62)`. On trigger the referee raises
  a `containment_timer` and applies bounded corrections: extraction cap (`cap_factor =
  max(0.08, 1-0.78*strength)`), harm cap, aid escrow that **restores welfare** by
  `0.20*escrowed` (escrow ≤ `raw_aid*0.58*strength`), migration friction, replication
  throttle. Family **B** (`delayed_harm_throttle`) is the consequence gate; family **C**
  (`anti_concentration_plus_delayed_harm_throttle`) is the **coupling** — scales gated by
  the sword.

## The danger point for decidability (the sword reaction)

Every sword correction is **bounded per step**: additive welfare gains with coefficients ×
(aid ≤ BUDGET·cap ≈ 1.92) and **clamped to [0,1]**; concentration/aid reductions are
bounded multiplicative factors with floors; mass changes are clamped to [0.01, 180]. The
accumulated-harm *volumes* are cumulative and are **never reset** — the sword lowers the
*rate*, not the accumulated total, by a bounded amount each step. So the corrective
reaction cannot reset an unbounded amount in one step, which is precisely the property the
WSTS monotonicity / decidability argument requires (verified empirically in Step 2).
