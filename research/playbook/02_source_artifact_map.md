# Source Artifact Map

This ledger lists source artifacts to mine for a future playbook. It is not the playbook itself.

| source type | examples | extract |
|---|---|---|
| Experiment specs | `experiments/*/SPEC*` | Hypothesis structure, preregistration discipline, success/failure criteria, execution constraints. |
| BA specs | `experiments/BA/**/SPEC_original.md` | Boundary-analysis kill-gates, mechanism-ablation framing, layer discipline, counterexample taxonomy. |
| FA specs | `experiments/FA/**/SPEC_original.md` | Faithful-abstraction kill-gates, candidate-validation criteria, no-oracle rules, T-C stop conditions. |
| JB specs | `experiments/JB/**/SPEC_original.md` | Boundary/shield/fidelity decision gates, safety-precondition checks, CEGAR boundary assessment schema. |
| FA review packet | `research/faithful_abstraction_v1/REVIEW_PACKET.md` | Review packet discipline, evidence mapping, critique-ready summary format. |
| FA bridge map | `research/faithful_abstraction_v1/BRIDGE_MAP_18_1_TO_FA2.md` | Cross-experiment continuity, claim traceability, handoff logic between failed preconditions and new hypotheses. |
| Door-1 postmortem | `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` | Negative-result discipline, durable knowledge extraction, what survives after a substrate fails. |
| Reorganization inventory | `repo_reorg_inventory/*.md` | Artifact-map discipline, evidence preservation rules, stale/duplicate handling, final-decision reporting. |

## Extraction Targets

- hypothesis structure
- kill-gate format
- evidence ledger pattern
- final decision schema
- review packet discipline
- negative-result discipline
