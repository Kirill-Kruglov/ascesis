# Operator Classification

| operator | candidate | final | audit tested | changed | justification |
|---|---:|---:|---:|---:|---|
| P1_remove_edge | B | B | 400 | 48 | Removing an edge removes a dependency/path and changes the causal theory. |
| P2_add_edge | B | B | 400 | 69 | Adding an edge introduces a new dependency/path and changes the causal theory. |
| P3_reverse_edge | B | B | 400 | 84 | Reversing an edge changes causal direction, ancestors, interventions and d-separation. |
| P4_alpha_rename | A | A | 401 | 0 | Renames an internal unmentioned variable while preserving graph structure over mentioned variables. |
| P5_split_mediator | A | B | 400 | 7 | Edge subdivision is representation-like only if the verifier abstracts away direct-edge/path-length facts; current verifier may observe them. |
| P6_delete_path | B | B | 400 | 90 | Deleting a complete path intentionally removes causal support. |
| P7_replace_chain | A | B | 397 | 29 | Chain replacement can be proof refactoring only if all external verifier consequences are preserved. |
| P8_merge_internal_nodes | B | B | 400 | 22 | Merging nodes conflates variables/mechanisms and changes the theory. |
| P9_split_node | A | A | 401 | 0 | Node split can be representation-preserving only if the split node is unmentioned and all verifier signatures are preserved. |
| P10_replace_subgraph | A | A | 343 | 0 | Equal-interface subgraph replacement needs verifier audit; current signatures may expose internal structure. |
| P11_swap_branches | B | B | 383 | 32 | Swapping branches changes which causes support which effects. |
| P12_alternative_derivation | B | B | 400 | 9 | Alternative derivation changes direct-edge/path evidence under the current verifier. |