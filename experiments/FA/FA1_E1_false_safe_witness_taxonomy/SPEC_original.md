# FA1.E1 — False-Safe Witness Taxonomy

## Specification v1.0

```markdown
# FA1.E1
## False-Safe Witness Taxonomy

Purpose:
Build a taxonomy of false-safe witnesses by minimal missing semantic information.

This is not a repair experiment.
Do not modify Justitia.
Do not modify collapse definition.
Do not modify 18.0 shield.
Do not synthesize a new shield.

Question:
When the current abstraction labels a state SAFE but future concrete collapse occurs, what minimal information was missing?

Use:
- BA1/18.1 false-safe machinery if available.
- BA4.1 layer audit.
- Current Justitia collapse definition:
  mean(zone_welfare) < 0.32
  OR count(zone_welfare < 0.20) >= 4
  OR total_mass < 35

Required witness classes:

1. spread_blind
Missing information:
  failed_zone_count or count(zone_welfare < 0.20)

2. mass_blind
Missing information:
  total_mass or mass deficit

3. mean_blind
Missing information:
  mean_welfare resolution too coarse

4. forward_dynamics_blind
Current state not collapsed, but future collapse occurs due to transition dynamics.

5. history_blind
False-safe distinguished by delayed observation, response_to_aid, last_aid, or neighbor_delta.

6. control_blind
False-safe distinguished by containment_timer, policy mode, allocation, audit, or control state.

7. policy_visible_concentration_blind
False-safe distinguished by Obs.resource_concentration / policy-visible concentration, not reporting HHI.

8. layer_confusion_blind
False-safe appears explainable only by reporting/projection variable that is not transition-relevant.

9. unknown_or_mixed
No single minimal information class explains the witness.

For each false-safe witness report:

- run/world/policy/seed/step
- current collapse clauses
- future collapse step
- first collapse clause triggered
- shield abstract state
- shield label
- concrete variables:
  mean_welfare
  failed_zone_count
  total_mass
  min_zone_welfare
  resource_hhi
  policy
  containment_timer summary
  delayed obs summary if available
  response_to_aid summary
  neighbor_delta summary
- assigned witness class
- minimal missing information candidate
- eligible layer from BA4.1
- whether candidate is variable, aggregate, threshold, temporal, or policy/control invariant
- confidence: high/medium/low
- reason

Required outputs:

experiments/FA1_E1_false_safe_witness_taxonomy/outputs/

- witness_taxonomy.csv
- witness_class_summary.json
- minimal_information_candidates.csv
- layer_eligibility_summary.csv
- representative_witnesses.md
- ambiguous_witnesses.md
- hypothesis_assessment.json
- final_report.md
- implementation_notes.md

Primary metrics:

- total false-safe witnesses
- fraction by witness class
- cumulative coverage by top-k missing information candidates
- number of witnesses explained by real omitted collapse clauses:
  spread + mass
- number requiring history/control information
- number involving layer confusion
- unknown/mixed fraction

Decision logic:

Case A — Collapse_clause_dominant:
Most false-safe witnesses are explained by omitted real collapse clauses:
  failed_zone_count and total_mass.
Interpretation:
18.0 failure mostly came from incomplete collapse projection.

Case B — Dynamics_dominant:
Most false-safe witnesses are not currently collapsed but later collapse.
Interpretation:
Faithful abstraction requires forward-dynamics information, not only current collapse clauses.

Case C — History_control_dominant:
Many witnesses require delayed observations, response_to_aid, neighbor_delta, containment, audit, or policy state.
Interpretation:
Faithful abstraction must preserve selected control/history invariants.

Case D — Mixed_information:
No small set of minimal information candidates covers the majority.
Interpretation:
H_FA1 weakened; refinement may not remain compact.

Case E — Inconclusive:
Witness extraction is insufficient or layer assignment uncertain.

Critical instruction:
Actively try to falsify H_FA1.

A strong counterexample is:
- many false-safe witnesses require high-dimensional raw state;
- no compact invariant separates them;
- witness classes are unstable across seeds/policies;
- minimal information candidates are mostly layer-ineligible.

Do not propose a new shield.
Do not call anything safe.
This experiment only maps missing information.
```
