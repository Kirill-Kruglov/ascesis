# CL1 Layer Audit

| coordinate | roles | boundary use | learner visible | risk if projected away |
|---|---|---|---|---|
| `zones` | DYNAMICS, OBSERVATION, PROJECTION | Candidate boundary uses full zone vector for rollout. | Yes | Omitting failed-zone count can hide spread collapse. |
| `mass` | DYNAMICS, OBSERVATION, PROJECTION | Candidate boundary uses mass for rollout. | Yes | Omitting mass can hide global resource collapse. |
| `phase` | DYNAMICS, OBSERVATION, PROJECTION | Candidate boundary uses phase to know the next lawful exogenous shock. | Yes | Omitting phase can mispredict near-horizon shocks. |
| `collapse_predicate` | AUDIT-ONLY | Used only for ground truth and metric computation. | No | If made learner-visible, it leaks oracle labels. |
| `future_rollout_outcome` | AUDIT-ONLY | Used only for metric computation and candidate boundary's transition-semantics rollout, not as a stored label. | No | Stored labels would turn the boundary into an oracle. |
| `mean_zone_health` | REPORTING, PROJECTION baseline | Used only by projection-blind baseline. | Derivable from observation | As a sole coordinate, it hides spread collapse. |
| `safe_labeled_count` and rates | REPORTING | Not used as boundary evidence. | No | Using post-hoc rates as boundary input would be circular. |

Projected-away coordinates for the candidate: none of the domain's collapse-relevant
state coordinates (`zones`, `mass`, `phase`) are projected away. The candidate still
abstracts away action alternatives by evaluating the pre-registered safety policy only.

Projection-blind baseline projected-away risks: failed-zone spread, mass, and phase.
