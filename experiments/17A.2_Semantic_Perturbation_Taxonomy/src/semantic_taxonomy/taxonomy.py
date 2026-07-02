from __future__ import annotations

OPERATOR_TAXONOMY = {
    "P1_remove_edge": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Removing an edge removes a dependency/path and changes the causal theory.",
    },
    "P2_add_edge": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Adding an edge introduces a new dependency/path and changes the causal theory.",
    },
    "P3_reverse_edge": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Reversing an edge changes causal direction, ancestors, interventions and d-separation.",
    },
    "P4_alpha_rename": {
        "candidate_class": "A",
        "final_class": "A",
        "reason": "Renames an internal unmentioned variable while preserving graph structure over mentioned variables.",
    },
    "P5_split_mediator": {
        "candidate_class": "A",
        "final_class": "audit_required",
        "reason": "Edge subdivision is representation-like only if the verifier abstracts away direct-edge/path-length facts; current verifier may observe them.",
    },
    "P6_delete_path": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Deleting a complete path intentionally removes causal support.",
    },
    "P7_replace_chain": {
        "candidate_class": "A",
        "final_class": "audit_required",
        "reason": "Chain replacement can be proof refactoring only if all external verifier consequences are preserved.",
    },
    "P8_merge_internal_nodes": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Merging nodes conflates variables/mechanisms and changes the theory.",
    },
    "P9_split_node": {
        "candidate_class": "A",
        "final_class": "audit_required",
        "reason": "Node split can be representation-preserving only if the split node is unmentioned and all verifier signatures are preserved.",
    },
    "P10_replace_subgraph": {
        "candidate_class": "A",
        "final_class": "audit_required",
        "reason": "Equal-interface subgraph replacement needs verifier audit; current signatures may expose internal structure.",
    },
    "P11_swap_branches": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Swapping branches changes which causes support which effects.",
    },
    "P12_alternative_derivation": {
        "candidate_class": "B",
        "final_class": "B",
        "reason": "Alternative derivation changes direct-edge/path evidence under the current verifier.",
    },
}


def base_class(operator: str) -> str:
    return OPERATOR_TAXONOMY[operator]["final_class"]
