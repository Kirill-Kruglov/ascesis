# FA2.5 Baseline Definitions

B0 uses the current 18.0 abstract counters only.

B1 is intentionally strong: it is a straightforward CEGAR/predicate-style history-variable refinement using delayed aid, delayed response, neighbor delta, policy-visible concentration, delayed welfare, and compact bad-consequence predicates.

B2 uses five interpretable non-oracle current-state coordinates, matching the candidate coordinate count.

| model | coordinates | oracle | history | note |
|---|---:|---|---|---|
| B0_current_18_0 | 2 | no | no | high but known projection-blind |
| Candidate_FA2_compact | 5 | no | yes, compact delayed consequence flag | high; compact but empirical min-zone threshold |
| B1_history_CEGAR | 13 | no | yes, strong baseline | medium; standard history-variable refinement |
| B2_raw_current_state | 5 | no | no | high; not witness-structured |
