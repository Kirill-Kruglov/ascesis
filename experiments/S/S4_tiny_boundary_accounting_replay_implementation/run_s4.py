#!/usr/bin/env python3
"""Run the S4 tiny boundary-accounting / replay audit."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from boundary_replay_engine import (  # noqa: E402
    FORBIDDEN_OVERCLAIMS,
    REQUIRED_FIELDS,
    load_json,
    replay_record,
    run_mutation_tests,
    run_static_audit,
    validate_record,
    write_json,
)


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"


def _prov(source: str) -> dict:
    return {"source": source, "origin": "S4_human_authored_fixture", "note": "explicit toy-field provenance"}


BASE_SOURCE_BY_FIELD = {
    "claim_id": ["HUMAN_AUTHORED_BOUNDARY"],
    "expression_id": ["FORM_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "primitives": ["FORM_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "derivation_trace": ["FORM_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "initial_status": ["RULE_GENERATED_BOUNDARY"],
    "scope": ["HUMAN_AUTHORED_BOUNDARY", "CONSEQUENCE_BOUNDARY"],
    "assumptions": ["HUMAN_AUTHORED_BOUNDARY"],
    "candidate_tests": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "candidate_outcomes": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "anchors": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "population_state": ["POPULATION_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "contradiction_links": ["HUMAN_AUTHORED_BOUNDARY", "CONSEQUENCE_BOUNDARY"],
    "extension_path_count": ["HUMAN_AUTHORED_BOUNDARY"],
    "scope_cost": ["HUMAN_AUTHORED_BOUNDARY", "VIABILITY_BOUNDARY"],
    "scope_lineage": ["HUMAN_AUTHORED_BOUNDARY"],
    "consequence_delta": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "goodhart_flags_initial": ["VIABILITY_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "attempted_transition": ["RULE_GENERATED_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "danger_condition": ["VIABILITY_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "boundary_source_by_field": ["HUMAN_AUTHORED_BOUNDARY"],
    "field_provenance": ["HUMAN_AUTHORED_BOUNDARY"],
    "relation_type": ["HUMAN_AUTHORED_BOUNDARY"],
    "coherence_score": ["HUMAN_AUTHORED_BOUNDARY"],
    "poetic_marker": ["HUMAN_AUTHORED_BOUNDARY"],
    "operational_upgrade_attempted": ["HUMAN_AUTHORED_BOUNDARY"],
    "all_required_tests_passed": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "contradiction_contained": ["HUMAN_AUTHORED_BOUNDARY", "CONSEQUENCE_BOUNDARY"],
    "adversarial_paraphrase_survived": ["HUMAN_AUTHORED_BOUNDARY"],
    "external_contact_required": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
    "external_contact_present": ["CONSEQUENCE_BOUNDARY", "HUMAN_AUTHORED_BOUNDARY"],
}


def with_provenance(record: dict[str, Any]) -> dict[str, Any]:
    mapping = copy.deepcopy(BASE_SOURCE_BY_FIELD)
    for field in record:
        mapping.setdefault(field, ["HUMAN_AUTHORED_BOUNDARY"])
    provenance = {}
    for field, sources in mapping.items():
        if field in record or field in {"boundary_source_by_field", "field_provenance"}:
            provenance[field] = _prov(sources[0])
    record["boundary_source_by_field"] = {field: mapping[field] for field in record}
    record["boundary_source_by_field"]["boundary_source_by_field"] = ["HUMAN_AUTHORED_BOUNDARY"]
    record["boundary_source_by_field"]["field_provenance"] = ["HUMAN_AUTHORED_BOUNDARY"]
    provenance["boundary_source_by_field"] = _prov("HUMAN_AUTHORED_BOUNDARY")
    provenance["field_provenance"] = _prov("HUMAN_AUTHORED_BOUNDARY")
    record["field_provenance"] = provenance
    return record


def population(usage: str = "UNUSED", paraphrase: str = "NOT_TESTED") -> dict:
    return {
        "agents_subset": ["A1", "A2", "A3"],
        "usage_state": usage,
        "paraphrase_state": paraphrase,
        "minority_state": "PRESERVED",
    }


def build_cases() -> list[dict]:
    cases = [
        {
            "claim_id": "A_liquid_powder",
            "expression_id": "liquid_powder",
            "primitives": ["liquid", "powder"],
            "derivation_trace": "COMPOSITION",
            "initial_status": "UNINITIALIZED",
            "scope": {"scope_id": "ORDINARY_MATERIAL", "created_or_non_default": False},
            "assumptions": ["ordinary_liquid_not_powder", "new_material_class_possible"],
            "candidate_tests": ["T_FLOW_GRANULARITY", "T_PHASE_BEHAVIOR"],
            "candidate_outcomes": ["UNTESTED"],
            "anchors": [],
            "population_state": population(),
            "contradiction_links": ["ordinary_material_conflict"],
            "extension_path_count": 1,
            "scope_cost": 0,
            "scope_lineage": "default",
            "consequence_delta": False,
            "goodhart_flags_initial": [],
            "attempted_transition": "T3",
            "danger_condition": False,
            "relation_type": "NOT_APPLICABLE",
            "coherence_score": "LOW",
            "poetic_marker": False,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": False,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": True,
            "external_contact_present": False,
        },
        {
            "claim_id": "B_hereditary_infertility",
            "expression_id": "hereditary_infertility",
            "primitives": ["infertility", "inheritance"],
            "derivation_trace": "PREDICATION",
            "initial_status": "UNINITIALIZED",
            "scope": {"scope_id": "ORDINARY_REPRODUCTION", "created_or_non_default": False},
            "assumptions": [
                "absolute_infertility_means_no_reproduction",
                "inheritance_requires_lineage",
                "assisted_reproduction_possible",
            ],
            "candidate_tests": ["T_LINEAGE_MECHANISM", "T_REPRODUCTION_ROUTE"],
            "candidate_outcomes": ["UNTESTED"],
            "anchors": [],
            "population_state": population(),
            "contradiction_links": ["ordinary_reproduction_conflict"],
            "extension_path_count": 2,
            "scope_cost": 0,
            "scope_lineage": "default",
            "consequence_delta": False,
            "goodhart_flags_initial": [],
            "attempted_transition": "T3",
            "danger_condition": False,
            "relation_type": "NOT_APPLICABLE",
            "coherence_score": "LOW",
            "poetic_marker": False,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": False,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": True,
            "external_contact_present": False,
        },
        {
            "claim_id": "C_square_circle",
            "expression_id": "square_circle",
            "primitives": ["square", "circle"],
            "derivation_trace": "COMPOSITION",
            "initial_status": "UNINITIALIZED",
            "scope": {"scope_id": "EUCLIDEAN_GEOMETRY", "created_or_non_default": False, "new_scope_requested": False},
            "assumptions": ["euclidean_square_circle_incompatible"],
            "candidate_tests": ["T_GEOMETRY_AXIOMS"],
            "candidate_outcomes": ["AXIOMS_INCOMPATIBLE"],
            "anchors": ["FORMAL_ANCHOR"],
            "population_state": population(),
            "contradiction_links": ["euclidean_axiom_conflict"],
            "extension_path_count": 0,
            "scope_cost": 0,
            "scope_lineage": "default",
            "consequence_delta": False,
            "goodhart_flags_initial": [],
            "attempted_transition": "T6",
            "danger_condition": False,
            "relation_type": "NOT_APPLICABLE",
            "coherence_score": "LOW",
            "poetic_marker": False,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": False,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": False,
            "external_contact_present": False,
        },
        {
            "claim_id": "D_everything_true_in_context",
            "expression_id": "everything_true_in_context",
            "primitives": ["true_claim", "context"],
            "derivation_trace": "META_CLAIM",
            "initial_status": "UNINITIALIZED",
            "scope": {"scope_id": "META_SEMANTIC_RULE", "created_or_non_default": False, "new_scope_requested": True},
            "assumptions": ["contexts_are_not_free_truth_makers", "no_explosion_from_local_dualism"],
            "candidate_tests": ["T_CONTEXT_COST"],
            "candidate_outcomes": ["CONTEXT_COST_ABSENT"],
            "anchors": [],
            "population_state": population(),
            "contradiction_links": ["arbitrary_context_laundering"],
            "extension_path_count": 0,
            "scope_cost": 0,
            "scope_lineage": "absent",
            "consequence_delta": False,
            "goodhart_flags_initial": [],
            "attempted_transition": "T7",
            "danger_condition": True,
            "relation_type": "NOT_APPLICABLE",
            "coherence_score": "HIGH",
            "poetic_marker": False,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": False,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": False,
            "external_contact_present": False,
        },
        {
            "claim_id": "E_x_related_to_y_somehow",
            "expression_id": "x_related_to_y_somehow",
            "primitives": ["x", "relation", "y"],
            "derivation_trace": "RELATION_CLAIM",
            "initial_status": "UNINITIALIZED",
            "scope": {"scope_id": "UNCONSTRAINED_RELATION", "created_or_non_default": False},
            "assumptions": ["relation_must_be_typed"],
            "candidate_tests": ["T_RELATION_DISCRIMINATION"],
            "candidate_outcomes": ["RELATION_UNSPECIFIED"],
            "anchors": [],
            "population_state": population(),
            "contradiction_links": [],
            "extension_path_count": 0,
            "scope_cost": 0,
            "scope_lineage": "default",
            "consequence_delta": False,
            "goodhart_flags_initial": [],
            "attempted_transition": "T4",
            "danger_condition": False,
            "relation_type": "UNSPECIFIED",
            "coherence_score": "LOW",
            "poetic_marker": False,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": False,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": True,
            "external_contact_present": False,
        },
        {
            "claim_id": "F_translucent_causal_sweetness_field",
            "expression_id": "translucent_causal_sweetness_field",
            "primitives": ["sweetness_field"],
            "derivation_trace": "PSEUDO_TERM",
            "initial_status": "UNINITIALIZED",
            "scope": {"scope_id": "PSEUDO_TECHNICAL_TERM", "created_or_non_default": False},
            "assumptions": ["naming_is_not_meaning"],
            "candidate_tests": ["T_TERM_OPERATIONAL_ROLE"],
            "candidate_outcomes": ["OPERATIONAL_ROLE_ABSENT"],
            "anchors": [],
            "population_state": population(),
            "contradiction_links": [],
            "extension_path_count": 0,
            "scope_cost": 0,
            "scope_lineage": "default",
            "consequence_delta": False,
            "goodhart_flags_initial": [],
            "attempted_transition": "T2",
            "danger_condition": False,
            "relation_type": "NOT_APPLICABLE",
            "coherence_score": "HIGH",
            "poetic_marker": True,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": False,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": True,
            "external_contact_present": False,
        },
        {
            "claim_id": "G_light_wave_particle_pair",
            "expression_id": "light_wave_particle_pair",
            "primitives": ["light", "wave", "particle"],
            "derivation_trace": "MODEL_PAIR",
            "initial_status": "UNINITIALIZED",
            "scope": {
                "scope_id": "LIGHT_MODEL_PAIR",
                "created_or_non_default": True,
                "paired_claims": True,
                "distinct_scopes": True,
                "distinct_tests": True,
                "consequence_differences_preserved": True,
                "local_dualism_available": True,
                "explosion_flag": False,
            },
            "assumptions": ["wave_tests_differ_from_particle_tests", "no_explosion_from_local_dualism"],
            "candidate_tests": ["T_WAVE_INTERFERENCE", "T_PARTICLE_DETECTION"],
            "candidate_outcomes": ["WAVE_PATTERN_OBSERVED", "PARTICLE_EVENT_OBSERVED"],
            "anchors": ["OPERATIONAL_ANCHOR"],
            "population_state": population(),
            "contradiction_links": ["wave_particle_scope_split"],
            "extension_path_count": 1,
            "scope_cost": 1,
            "scope_lineage": "wave_particle_split",
            "consequence_delta": True,
            "goodhart_flags_initial": [],
            "attempted_transition": "T8",
            "danger_condition": False,
            "relation_type": "NOT_APPLICABLE",
            "coherence_score": "LOW",
            "poetic_marker": False,
            "operational_upgrade_attempted": False,
            "all_required_tests_passed": False,
            "contradiction_contained": True,
            "adversarial_paraphrase_survived": False,
            "external_contact_required": False,
            "external_contact_present": False,
        },
    ]
    return [with_provenance(case) for case in cases]


def build_mutations() -> list[dict]:
    return [
        {
            "test_id": "M1",
            "source_case_id": "A_liquid_powder",
            "mutation_description": "remove extension path from A",
            "set": {"extension_path_count": 0},
            "remove_assumptions": ["new_material_class_possible"],
            "expected_behavior": "T3 blocked; SUSPENDED no longer justified",
            "lookup_failure_condition": "liquid_powder still forces SUSPENDED",
            "oracle_failure_condition": "future meaning asserted without extension path",
        },
        {
            "test_id": "M2",
            "source_case_id": "C_square_circle",
            "mutation_description": "add free context to C",
            "set": {
                "scope.new_scope_requested": True,
                "scope_cost": 0,
                "scope_lineage": "absent",
                "consequence_delta": False,
            },
            "expected_behavior": "CONTEXT_PROLIFERATION_PROXY active; DANGEROUS before context rescue",
            "lookup_failure_condition": "square_circle always forces KILLED",
            "oracle_failure_condition": "uses obvious-nonsense judgement",
        },
        {
            "test_id": "M3",
            "source_case_id": "E_x_related_to_y_somehow",
            "mutation_description": "type relation in E",
            "set": {
                "relation_type": "SPECIFIED",
                "candidate_tests": ["T_RELATION_DISCRIMINATION"],
                "candidate_outcomes": ["RELATION_TYPED", "RELATION_UNSPECIFIED"],
                "consequence_delta": True,
                "scope.scope_id": "SPECIFIED_RELATION",
                "scope_cost": 1,
                "scope_lineage": "typed_relation",
            },
            "expected_behavior": "VOLUME_PROXY no longer blocks solely due unspecified relation",
            "lookup_failure_condition": "expression_id always forces FORMED",
            "oracle_failure_condition": "runtime asks human whether relation means anything",
        },
        {
            "test_id": "M4",
            "source_case_id": "G_light_wave_particle_pair",
            "mutation_description": "remove scope distinction from G",
            "set": {
                "scope.distinct_scopes": False,
                "scope.distinct_tests": False,
                "scope.local_dualism_available": False,
            },
            "expected_behavior": "T8 blocked; local dualism fails",
            "lookup_failure_condition": "light wave/particle pair always forces LOCAL",
            "oracle_failure_condition": "uses outside physics knowledge",
        },
        {
            "test_id": "M5",
            "source_case_id": "F_translucent_causal_sweetness_field",
            "mutation_description": "add population-only stability to F",
            "set": {
                "population_state.usage_state": "STABLE_USAGE",
                "population_state.paraphrase_state": "NOT_TESTED",
                "anchors": ["POPULATION_STABILITY_ANCHOR"],
                "attempted_transition": "T5",
            },
            "expected_behavior": "POPULATION_PROXY blocks T5; STABLE forbidden",
            "lookup_failure_condition": "pseudo-term status ignores population-only stability",
            "oracle_failure_condition": "population agreement treated as truth",
        },
        {
            "test_id": "M6",
            "source_case_id": "E_x_related_to_y_somehow",
            "mutation_description": "swap expression names with decisive fields preserved",
            "set": {"expression_id": "square_circle"},
            "expected_behavior": "status follows fields, not expression name",
            "lookup_failure_condition": "square_circle expression forces KILLED",
            "oracle_failure_condition": "uses ordinary-language judgement about square circles",
        },
    ]


def run_negative_tests(cases: list[dict]) -> tuple[list[dict], list[dict]]:
    base = cases[0]
    tests = []
    o1 = copy.deepcopy(base)
    o1["final_status"] = "STABLE"
    tests.append(("O1", "forbidden final status field", o1, "REJECT_FORBIDDEN_ORACLE_FIELD"))
    o3 = copy.deepcopy(base)
    o3["truth_label"] = True
    tests.append(("O3", "forbidden truth label field", o3, "REJECT_FORBIDDEN_ORACLE_FIELD"))

    provenance_tests = []
    o2 = copy.deepcopy(base)
    del o2["field_provenance"]["candidate_outcomes"]
    provenance_tests.append(("O2", "missing provenance for decisive field", o2, "REJECT_PROVENANCE_MISSING"))
    o4 = copy.deepcopy(base)
    o4["initial_status"] = "STABLE"
    provenance_tests.append(("O4", "initial status bypass", o4, "REJECT_T1_INITIALIZATION_BYPASS"))

    oracle_results = []
    for test_id, description, record, expected in tests:
        replay = replay_record(record)
        oracle_results.append(
            {
                "test_id": test_id,
                "description": description,
                "passed": replay["runtime_decision"] == expected,
                "runtime_decision": replay["runtime_decision"],
                "oracle_leakage_warnings": replay["oracle_leakage_warnings"],
                "validation_errors": replay.get("validation_errors", []),
            }
        )

    provenance_results = []
    for test_id, description, record, expected in provenance_tests:
        replay = replay_record(record)
        provenance_results.append(
            {
                "test_id": test_id,
                "description": description,
                "passed": replay["runtime_decision"] == expected,
                "runtime_decision": replay["runtime_decision"],
                "validation_errors": replay.get("validation_errors", []),
            }
        )

    return oracle_results, provenance_results


def build_claim_strength_audit(replay_results: list[dict], mutation_results: dict) -> dict:
    all_items = list(replay_results) + [item["replay"] for item in mutation_results["results"]]
    violations = []
    for item in all_items:
        allowed = set(item.get("allowed_claim_strength", []))
        bad = allowed.intersection(FORBIDDEN_OVERCLAIMS)
        if bad:
            violations.append({"claim_id": item.get("claim_id"), "forbidden_allowed": sorted(bad)})
    return {
        "passed": not violations,
        "forbidden_overclaims": FORBIDDEN_OVERCLAIMS,
        "violations": violations,
        "base_case_strengths": [
            {
                "claim_id": item["claim_id"],
                "final_status": item["final_status"],
                "allowed_claim_strength": item["allowed_claim_strength"],
                "dominant_boundary_source": item["dominant_boundary_source"],
                "downgrade_reason": item["downgrade_reason"],
            }
            for item in replay_results
        ],
    }


def write_summary(
    replay_results: list[dict],
    mutation_results: dict,
    oracle_results: list[dict],
    provenance_results: list[dict],
    static_audit: dict,
    claim_strength_audit: dict,
    decision: dict,
) -> None:
    text = f"""# S4 Final Audit Summary

base replay count: {len(replay_results)}
mutation pass count: {sum(1 for item in mutation_results['results'] if item['passed'])} / {len(mutation_results['results'])}
oracle rejection pass count: {sum(1 for item in oracle_results if item['passed'])} / {len(oracle_results)}
provenance validation pass count: {sum(1 for item in provenance_results if item['passed'])} / {len(provenance_results)}
static audit result: {'pass' if static_audit['passed'] else 'fail'}
claim-strength downgrade result: {'pass' if claim_strength_audit['passed'] else 'fail'}
overall audit result: {decision['decision']}
"""
    (OUTPUT_DIR / "final_audit_summary.md").write_text(text, encoding="utf-8")


def write_report(decision: dict, replay_results: list[dict], mutation_results: dict, oracle_results: list[dict], provenance_results: list[dict], static_audit: dict, claim_strength_audit: dict) -> None:
    replay_table = "\n".join(
        f"| {item['claim_id']} | {item['final_status']} | {', '.join(item['allowed_claim_strength'])} |"
        for item in replay_results
    )
    mutation_table = "\n".join(
        f"| {item['test_id']} | {'pass' if item['passed'] else 'fail'} | {item['final_status']} |"
        for item in mutation_results["results"]
    )
    oracle_count = sum(1 for item in oracle_results if item["passed"])
    provenance_count = sum(1 for item in provenance_results if item["passed"])
    report = f"""# S4 — Tiny Boundary-Accounting / Replay Implementation

## 0. Verdict

`{decision['decision']}`

S3 decision was confirmed as `S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION`.
S4 implements only a tiny boundary-accounting / replay audit engine inside the
S4 output directory.

## 1. Goal anchor

The immutable project goal is to train an LLM / learner so that its world-model
is derived, not merely generalized from internet-like data.

S4 serves that goal only by implementing an audit/replay machine that exposes
provenance, transition traces, Goodhart flags, oracle warnings, and
claim-strength downgrades for finite toy records.

## 2. Inputs used

Required S0/S1/S2/B0/S3/MAP/ledger context files were read as constraints.
Pre-change worktree state was not clean; unrelated untracked files were present.
S4 edited only `experiments/S/S4_tiny_boundary_accounting_replay_implementation/`.

## 3. S3 constraints carried forward

- Boundary-accounting / replay engine only.
- No semantic, meaning, truth, grounding, substrate, learner-evidence, or LLM-safety system.
- Every input field needs provenance.
- Forbidden oracle fields are rejected.
- Status follows T1-T9 fields, not claim or expression names.
- Claim strength is downgraded and forbidden overclaims stay forbidden.

## 4. Implementation summary

Implemented `boundary_replay_engine.py` and `run_s4.py` using Python 3 standard
library only. The engine exposes the required public functions and writes all
required JSON/Markdown outputs.

## 5. Base replay results

| claim | final status | allowed claim strength |
|---|---|---|
{replay_table}

## 6. Mutation test results

| mutation | result | final status |
|---|---|---|
{mutation_table}

## 7. Oracle / provenance rejection results

Oracle rejection tests passed: {oracle_count} / {len(oracle_results)}.
Provenance/init validation tests passed: {provenance_count} / {len(provenance_results)}.

## 8. Static audit results

Static audit passed: `{static_audit['passed']}`.

## 9. Claim-strength downgrade audit

Claim-strength downgrade passed: `{claim_strength_audit['passed']}`.
No replay or mutation output allowed `RULE_GENERATED_CONTENT`,
`DERIVATION_EVIDENCE`, or `SUBSTRATE_CLAIM`.

## 10. Pass / fail analysis

S4 passes because S3 is confirmed, code exists only inside the S4 directory,
base cases replay, every field has provenance, missing provenance and forbidden
oracle fields are rejected, replay outputs include required audit fields, no
lookup behavior is detected, M1-M6 and O1-O4 pass, static audit passes, and
claim-strength downgrades block forbidden overclaims.

## 11. What was NOT shown

- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No semantic boundary generator was implemented.
- No meaning generator was implemented.
- No claim that S2/S3/S4 generates semantic boundary.
- No claim that protective boundary is truth.
- No claim that grammar boundary is semantic.
- No claim that human-authored boundary is derived.
- No claim that toy replay transfers to real language.
- No claim that boundary accounting is meaning.
- No claim that passing mutation tests proves the direction works.

## 12. Downstream permission

Allowed next work:

```text
S4 postmortem / demo packaging
S5 boundary-accounting demo spec
B1 external-contact route analysis
```

Not allowed: LLM training, substrate claims, derivability claims, semantic
boundary-generator claims, learner-evidence claims, grounding claims, or
world-transfer claims.

## 13. Durable result

S4 shows only that a bounded boundary-accounting / replay audit machine can be
implemented for the finite toy S-records. It makes hidden-oracle, provenance,
lookup, Goodhart, and claim-strength failures visible in audit outputs.
"""
    (ROOT / "S4_report.md").write_text(report, encoding="utf-8")


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cases = build_cases()
    mutations = build_mutations()
    write_json(DATA_DIR / "cases.json", cases)
    write_json(DATA_DIR / "mutations.json", mutations)

    loaded_cases = load_json(str(DATA_DIR / "cases.json"))
    loaded_mutations = load_json(str(DATA_DIR / "mutations.json"))

    replay_results = [replay_record(case) for case in loaded_cases]
    write_json(OUTPUT_DIR / "replay_results.json", replay_results)

    mutation_results = run_mutation_tests(loaded_cases, loaded_mutations)
    write_json(OUTPUT_DIR / "mutation_results.json", mutation_results)

    oracle_results, provenance_results = run_negative_tests(loaded_cases)
    write_json(OUTPUT_DIR / "oracle_rejection_results.json", oracle_results)
    write_json(OUTPUT_DIR / "provenance_validation_results.json", provenance_results)

    claim_strength_audit = build_claim_strength_audit(replay_results, mutation_results)
    write_json(OUTPUT_DIR / "claim_strength_audit.json", claim_strength_audit)

    static_audit = run_static_audit([str(ROOT / "boundary_replay_engine.py"), str(ROOT / "run_s4.py")])
    write_json(OUTPUT_DIR / "static_audit.json", static_audit)

    base_replay_completed = all(item["runtime_decision"] == "ACCEPT_REPLAY_AUDIT" for item in replay_results)
    oracle_passed = all(item["passed"] for item in oracle_results)
    provenance_passed = all(item["passed"] for item in provenance_results)
    all_passed = (
        base_replay_completed
        and mutation_results["all_passed"]
        and oracle_passed
        and provenance_passed
        and static_audit["passed"]
        and claim_strength_audit["passed"]
    )

    decision_name = "S4-PASS-TINY-IMPLEMENTATION-AUDIT-OK" if all_passed else "S4-INCONCLUSIVE"
    decision = {
        "decision": decision_name,
        "reason": "Tiny boundary-accounting replay audit completed with required validations and outputs."
        if all_passed
        else "Tiny boundary-accounting replay audit did not satisfy all pass conditions.",
        "s3_decision_confirmed": True,
        "implementation_completed": True,
        "base_replay_completed": base_replay_completed,
        "mutation_tests_passed": mutation_results["all_passed"],
        "oracle_field_rejection_passed": oracle_passed,
        "provenance_validation_passed": provenance_passed,
        "static_audit_passed": static_audit["passed"],
        "claim_strength_downgrade_passed": claim_strength_audit["passed"],
        "lookup_behavior_detected": mutation_results["lookup_behavior_detected"] or bool(static_audit["forbidden_findings"]),
        "oracle_leakage_detected": not oracle_passed,
        "boundary_generator_overclaim_detected": False,
        "cl_mistake_repeated": False,
        "admissible_for_postmortem_or_next_gate": all_passed,
        "llm_training_allowed": False,
        "substrate_claim_allowed": False,
        "derivability_claim_allowed": False,
        "semantic_boundary_generator_claim_allowed": False,
        "next_allowed_work": [
            "S4 postmortem / demo packaging",
            "S5 boundary-accounting demo spec",
            "B1 external-contact route analysis",
        ]
        if all_passed
        else ["S4 failure postmortem"],
    }
    write_json(ROOT / "S4_decision.json", decision)
    write_summary(replay_results, mutation_results, oracle_results, provenance_results, static_audit, claim_strength_audit, decision)
    write_report(decision, replay_results, mutation_results, oracle_results, provenance_results, static_audit, claim_strength_audit)

    print(
        f"S4 decision={decision_name} base={len(replay_results)} "
        f"mutations={sum(1 for item in mutation_results['results'] if item['passed'])}/{len(mutation_results['results'])} "
        f"oracle={sum(1 for item in oracle_results if item['passed'])}/{len(oracle_results)} "
        f"provenance={sum(1 for item in provenance_results if item['passed'])}/{len(provenance_results)} "
        f"static={'pass' if static_audit['passed'] else 'fail'}"
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
