# CL1.1 Layer Audit Delta

- CL1 checked state-level SAFE under safety-policy rollout.
- CL1.1 checks action-conditioned admitted transitions.
- The candidate action admission rule uses source `zones`, `mass`, `phase`, the selected `action`, successor `zones`, `mass`, `phase`, and deterministic safety-policy continuation for the remaining horizon.
- Learner-visible values are only `observe(state)`, `action`, and `observe(successor)`.
- Audit-only values are collapse predicate results, collapse mechanisms, full rollout outcomes, witness classes, rates, and post-hoc counts.
- The candidate still abstracts away future action alternatives after the first admitted action.
- The result is policy-continuation scoped, not all-actions scoped.
- The CL1 state-level carryover baseline is retained to test whether admitting all actions from CL1 SAFE states leaks unsafe action transitions.
