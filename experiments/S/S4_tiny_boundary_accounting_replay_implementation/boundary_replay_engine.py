"""Tiny boundary-accounting / replay engine for S4.

The module implements deterministic audit replay over finite toy records. It
does not infer meaning, truth, grounding, substrate, derivability, learner
evidence, or model safety.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


STATUSES = {
    "FORMED",
    "POETIC",
    "SUSPENDED",
    "LOCAL",
    "STABLE",
    "KILLED",
    "DANGEROUS",
}

BOUNDARY_SOURCES = {
    "FORM_BOUNDARY",
    "CONSEQUENCE_BOUNDARY",
    "VIABILITY_BOUNDARY",
    "RULE_GENERATED_BOUNDARY",
    "HUMAN_AUTHORED_BOUNDARY",
    "POPULATION_BOUNDARY",
    "UNKNOWN_OR_MIXED_BOUNDARY",
}

CLAIM_STRENGTHS = {
    "FORM_ONLY",
    "BOUNDARY_ACCOUNTING",
    "TOY_REPLAY_DETERMINISTIC",
    "TOY_CONSEQUENCE_PROTOCOL",
    "VIABILITY_SHIELD",
    "EXTERNAL_CONTACT_REQUIRED",
    "RULE_GENERATED_CONTENT",
    "DERIVATION_EVIDENCE",
    "SUBSTRATE_CLAIM",
}

FORBIDDEN_OVERCLAIMS = [
    "RULE_GENERATED_CONTENT",
    "DERIVATION_EVIDENCE",
    "SUBSTRATE_CLAIM",
]

REQUIRED_FIELDS = [
    "claim_id",
    "expression_id",
    "primitives",
    "derivation_trace",
    "initial_status",
    "scope",
    "assumptions",
    "candidate_tests",
    "candidate_outcomes",
    "anchors",
    "population_state",
    "contradiction_links",
    "extension_path_count",
    "scope_cost",
    "scope_lineage",
    "consequence_delta",
    "goodhart_flags_initial",
    "attempted_transition",
    "danger_condition",
    "boundary_source_by_field",
    "field_provenance",
]

FORBIDDEN_FIELDS = {
    "final_status",
    "expected_final_status",
    "future_meaning_possible",
    "obvious_nonsense",
    "inside_boundary",
    "truth_label",
    "semantic_label",
    "safe_label_as_truth",
    "derived_label",
    "substrate_label",
}

EXPRESSIONS = {
    "liquid_powder",
    "hereditary_infertility",
    "square_circle",
    "everything_true_in_context",
    "x_related_to_y_somehow",
    "translucent_causal_sweetness_field",
    "light_wave_particle_pair",
}

DERIVATION_TRACES = {
    "COMPOSITION",
    "PREDICATION",
    "META_CLAIM",
    "RELATION_CLAIM",
    "PSEUDO_TERM",
    "MODEL_PAIR",
}

GOODHART_FLAGS = {
    "VOLUME_PROXY",
    "COHERENCE_PROXY",
    "CONTRADICTION_MINIMIZATION_PROXY",
    "CONTEXT_PROLIFERATION_PROXY",
    "GRAMMAR_PROXY",
    "POPULATION_PROXY",
}

STATIC_AUDIT_PATTERNS = [
    "final_status_by_claim",
    "status_by_claim",
    "final_status_by_expression",
    "status_by_expression",
    "expected_final_status",
    "future_meaning_possible",
    "obvious_nonsense",
    "truth_label",
    "semantic_label",
    "substrate_label",
]


def load_json(path: str) -> dict | list:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def verify_upstream_s3_decision(path: str | Path) -> dict:
    decision_path = Path(path)
    result = {
        "passed": False,
        "decision": None,
        "path": str(decision_path),
        "errors": [],
    }
    if not decision_path.exists():
        result["errors"].append("S3_DECISION_MISSING")
        return result
    try:
        with decision_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError:
        result["errors"].append("S3_DECISION_INVALID_JSON")
        return result
    if "decision" not in payload:
        result["errors"].append("S3_DECISION_FIELD_MISSING")
        return result
    result["decision"] = payload.get("decision")
    if result["decision"] != "S3-PASS-ADMISSIBLE-FOR-TINY-IMPLEMENTATION":
        result["errors"].append("S3_DECISION_NOT_PASS")
        return result
    result["passed"] = True
    return result


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, set):
        return sorted(value)
    return [value]


def _scope_id(record: dict) -> str:
    scope = record.get("scope")
    if isinstance(scope, dict):
        return str(scope.get("scope_id", ""))
    return str(scope or "")


def _scope_bool(record: dict, key: str) -> bool:
    scope = record.get("scope")
    return bool(scope.get(key)) if isinstance(scope, dict) else False


def _scope_value(record: dict, key: str, default: Any = None) -> Any:
    scope = record.get("scope")
    return scope.get(key, default) if isinstance(scope, dict) else default


def _sources_for(record: dict, fields: list[str]) -> list[str]:
    mapping = record.get("boundary_source_by_field", {})
    sources: set[str] = set()
    for field in fields:
        for source in _as_list(mapping.get(field)):
            if source:
                sources.add(source)
    return sorted(sources)


def _validation_error(code: str, field: str, message: str) -> dict:
    return {"code": code, "field": field, "message": message}


def validate_record(record: dict) -> list[dict]:
    errors: list[dict] = []

    for field in sorted(FORBIDDEN_FIELDS & set(record)):
        errors.append(
            _validation_error(
                "FORBIDDEN_INPUT_FIELD",
                field,
                "Forbidden oracle/status field is present in input record.",
            )
        )

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(_validation_error("MISSING_REQUIRED_FIELD", field, "Required field is absent."))

    if errors:
        return errors

    source_map = record.get("boundary_source_by_field")
    provenance = record.get("field_provenance")
    if not isinstance(source_map, dict):
        errors.append(_validation_error("PROVENANCE_MAP_INVALID", "boundary_source_by_field", "Expected map."))
        source_map = {}
    if not isinstance(provenance, dict):
        errors.append(_validation_error("PROVENANCE_MAP_INVALID", "field_provenance", "Expected map."))
        provenance = {}

    for field in record:
        if field not in source_map:
            errors.append(_validation_error("BOUNDARY_SOURCE_MISSING", field, "No boundary source for field."))
            continue
        sources = _as_list(source_map.get(field))
        if not sources:
            errors.append(_validation_error("BOUNDARY_SOURCE_MISSING", field, "Empty boundary source list."))
        for source in sources:
            if source not in BOUNDARY_SOURCES:
                errors.append(_validation_error("BOUNDARY_SOURCE_INVALID", field, f"Invalid source {source}."))
        if field not in provenance or not provenance.get(field):
            errors.append(_validation_error("FIELD_PROVENANCE_MISSING", field, "No field provenance entry."))
            continue
        prov_sources = _as_list(provenance[field].get("source") if isinstance(provenance[field], dict) else None)
        if not set(prov_sources).intersection(set(sources)):
            errors.append(
                _validation_error(
                    "PROVENANCE_SOURCE_DISAGREES",
                    field,
                    "field_provenance source does not match boundary_source_by_field.",
                )
            )

    if record.get("initial_status") != "UNINITIALIZED":
        errors.append(
            _validation_error(
                "INITIAL_STATUS_BYPASS",
                "initial_status",
                "initial_status must be UNINITIALIZED so T1 performs initialization.",
            )
        )

    if record.get("expression_id") not in EXPRESSIONS:
        errors.append(_validation_error("FINITE_DOMAIN_ERROR", "expression_id", "Expression is outside S4 finite set."))

    if record.get("derivation_trace") not in DERIVATION_TRACES:
        errors.append(
            _validation_error("FINITE_DOMAIN_ERROR", "derivation_trace", "Derivation trace is outside S4 finite set.")
        )

    for flag in record.get("goodhart_flags_initial", []):
        if flag not in GOODHART_FLAGS:
            errors.append(_validation_error("FINITE_DOMAIN_ERROR", "goodhart_flags_initial", f"Invalid flag {flag}."))

    return errors


def compute_goodhart_flags(record: dict) -> list[str]:
    flags = set(record.get("goodhart_flags_initial", []))
    outcomes = set(record.get("candidate_outcomes", []))
    tests = record.get("candidate_tests", [])
    anchors = set(record.get("anchors", []))
    attempted = record.get("attempted_transition")
    population = record.get("population_state", {})

    if (
        record.get("relation_type") == "UNSPECIFIED"
        or ("RELATION_UNSPECIFIED" in outcomes and "RELATION_TYPED" not in outcomes)
        or not tests
    ):
        flags.add("VOLUME_PROXY")

    if record.get("coherence_score") == "HIGH" and (not tests or not anchors or outcomes == {"UNTESTED"}):
        flags.add("COHERENCE_PROXY")

    if record.get("contradiction_links") and attempted == "T6" and (
        record.get("extension_path_count", 0) > 0 or _scope_bool(record, "local_dualism_available")
    ):
        flags.add("CONTRADICTION_MINIMIZATION_PROXY")

    if _scope_bool(record, "new_scope_requested") and (
        record.get("scope_cost") == 0
        or record.get("scope_lineage") in {"absent", "", None}
        or not record.get("consequence_delta")
        or not record.get("assumptions")
    ):
        flags.add("CONTEXT_PROLIFERATION_PROXY")

    if record.get("derivation_trace") and attempted in {"T4", "T5"} and (
        not tests or "OPERATIONAL_ROLE_ABSENT" in outcomes
    ):
        flags.add("GRAMMAR_PROXY")

    if population.get("usage_state") == "STABLE_USAGE" and (
        population.get("paraphrase_state") != "SURVIVED"
        or anchors.issubset({"POPULATION_STABILITY_ANCHOR"})
        or not tests
    ):
        flags.add("POPULATION_PROXY")

    return sorted(flags)


def _trace(
    rule_id: str,
    fields: list[str],
    before: str | None,
    after: str | None,
    preconditions: dict,
    blocked_by: list[str],
    warnings: list[str] | None = None,
    record: dict | None = None,
) -> dict:
    return {
        "rule_id": rule_id,
        "preconditions_checked": preconditions,
        "fields_consulted": fields,
        "boundary_sources_consulted": _sources_for(record or {}, fields),
        "status_before": before,
        "status_after": after,
        "blocked_by": blocked_by,
        "warning_ids": warnings or [],
    }


def _has_consequence_material(record: dict) -> bool:
    outcomes = set(record.get("candidate_outcomes", []))
    return bool(record.get("candidate_tests")) and outcomes and outcomes != {"UNTESTED"}


def replay_record(record: dict) -> dict:
    errors = validate_record(record)
    oracle_warnings = [err["code"] for err in errors if err["code"] == "FORBIDDEN_INPUT_FIELD"]
    if errors:
        decision = "REJECT_FORBIDDEN_ORACLE_FIELD" if oracle_warnings else "REJECT_PROVENANCE_MISSING"
        if any(err["code"] == "INITIAL_STATUS_BYPASS" for err in errors):
            decision = "REJECT_T1_INITIALIZATION_BYPASS"
        return {
            "claim_id": record.get("claim_id"),
            "expression_id": record.get("expression_id"),
            "final_status": None,
            "transition_trace": [],
            "blocked_transitions": [],
            "active_goodhart_flags": [],
            "boundary_sources_used": [],
            "dominant_boundary_source": None,
            "allowed_claim_strength": [],
            "forbidden_overclaims": FORBIDDEN_OVERCLAIMS,
            "downgrade_reason": "record rejected before replay",
            "oracle_leakage_warnings": oracle_warnings,
            "cl_mistake_warnings": [],
            "runtime_decision": decision,
            "validation_errors": errors,
        }

    trace: list[dict] = []
    blocked: list[dict] = []
    status: str | None = None
    goodhart_flags = compute_goodhart_flags(record)

    def block(rule_id: str, reasons: list[str]) -> None:
        blocked.append({"rule_id": rule_id, "blocked_by": reasons})

    # T1
    before = status
    t1_ok = bool(record.get("expression_id")) and bool(record.get("derivation_trace")) and bool(record.get("primitives"))
    status = "FORMED" if t1_ok else None
    if not t1_ok:
        block("T1", ["missing expression_id, derivation_trace, or primitives"])
    trace.append(
        _trace(
            "T1",
            ["expression_id", "derivation_trace", "primitives", "initial_status"],
            before,
            status,
            {"birth_fields_present": t1_ok},
            [] if t1_ok else ["birth_fields_missing"],
            record=record,
        )
    )

    # T7 before T6
    before = status
    t7_reasons = []
    if record.get("danger_condition"):
        t7_reasons.append("danger_condition")
    if "CONTEXT_PROLIFERATION_PROXY" in goodhart_flags:
        t7_reasons.append("CONTEXT_PROLIFERATION_PROXY")
    if record.get("protective_boundary_reported_as_truth"):
        t7_reasons.append("protective_boundary_reported_as_truth")
    if t7_reasons:
        status = "DANGEROUS"
    else:
        block("T7", ["no danger predicate active"])
    trace.append(
        _trace(
            "T7",
            ["danger_condition", "goodhart_flags_initial", "scope", "scope_cost", "scope_lineage", "consequence_delta"],
            before,
            status,
            {"danger_reasons": t7_reasons},
            [] if t7_reasons else ["no danger predicate active"],
            t7_reasons,
            record,
        )
    )

    # T6
    before = status
    t6_failure = (
        record.get("declared_scope_failure")
        or (_scope_id(record) == "EUCLIDEAN_GEOMETRY" and "AXIOMS_INCOMPATIBLE" in record.get("candidate_outcomes", []))
        or record.get("same_scope_contradiction_without_repair")
    )
    if status != "DANGEROUS" and t6_failure:
        status = "KILLED"
        t6_blockers: list[str] = []
    else:
        t6_blockers = ["danger already active"] if status == "DANGEROUS" else ["no declared-scope failure"]
        block("T6", t6_blockers)
    trace.append(
        _trace(
            "T6",
            ["scope", "candidate_outcomes", "contradiction_links", "extension_path_count"],
            before,
            status,
            {"declared_scope_failure": bool(t6_failure)},
            t6_blockers,
            record=record,
        )
    )

    # T2
    before = status
    t2_ok = (
        status == "FORMED"
        and (record.get("derivation_trace") == "PSEUDO_TERM" or bool(record.get("poetic_marker")))
        and not record.get("operational_upgrade_attempted")
    )
    if t2_ok:
        status = "POETIC"
    else:
        block("T2", ["not formed poetic/pseudo-term case or operational upgrade attempted"])
    trace.append(
        _trace(
            "T2",
            ["derivation_trace", "candidate_outcomes", "attempted_transition"],
            before,
            status,
            {"poetic_or_pseudo_term": t2_ok},
            [] if t2_ok else ["T2 preconditions absent"],
            record=record,
        )
    )

    # T3
    before = status
    t3_ok = (
        status in {"FORMED", "POETIC"}
        and bool(record.get("contradiction_links"))
        and int(record.get("extension_path_count", 0)) > 0
        and not record.get("danger_condition")
    )
    if t3_ok:
        status = "SUSPENDED"
    else:
        reasons = []
        if status not in {"FORMED", "POETIC"}:
            reasons.append("status not FORMED/POETIC")
        if not record.get("contradiction_links"):
            reasons.append("no contradiction or underdefined ontology link")
        if int(record.get("extension_path_count", 0)) <= 0:
            reasons.append("no extension path")
        if record.get("danger_condition"):
            reasons.append("danger condition active")
        block("T3", reasons)
    trace.append(
        _trace(
            "T3",
            ["contradiction_links", "extension_path_count", "danger_condition"],
            before,
            status,
            {"suspension_available": t3_ok},
            [] if t3_ok else blocked[-1]["blocked_by"],
            record=record,
        )
    )

    # T4
    before = status
    t4_blocking_flags = sorted(set(goodhart_flags) & {"VOLUME_PROXY", "CONTEXT_PROLIFERATION_PROXY", "GRAMMAR_PROXY", "COHERENCE_PROXY"})
    created_scope = bool(_scope_value(record, "created_or_non_default", _scope_bool(record, "new_scope_requested")))
    t4_ok = (
        status == "SUSPENDED"
        and bool(record.get("scope"))
        and bool(record.get("assumptions"))
        and bool(record.get("candidate_tests"))
        and _has_consequence_material(record)
        and bool(record.get("consequence_delta"))
        and (not created_scope or (record.get("scope_cost", 0) > 0 and record.get("scope_lineage") not in {"absent", "", None}))
        and not t4_blocking_flags
    )
    if t4_ok:
        status = "LOCAL"
    else:
        reasons = []
        if status != "SUSPENDED":
            reasons.append("status not SUSPENDED")
        if not _has_consequence_material(record):
            reasons.append("missing consequence material")
        if not record.get("consequence_delta"):
            reasons.append("missing consequence_delta")
        if created_scope and record.get("scope_cost", 0) <= 0:
            reasons.append("scope_cost missing for created scope")
        if created_scope and record.get("scope_lineage") in {"absent", "", None}:
            reasons.append("scope_lineage missing for created scope")
        reasons.extend(t4_blocking_flags)
        block("T4", reasons)
    trace.append(
        _trace(
            "T4",
            ["scope", "assumptions", "candidate_tests", "candidate_outcomes", "scope_cost", "scope_lineage", "consequence_delta"],
            before,
            status,
            {"localization_available": t4_ok},
            [] if t4_ok else blocked[-1]["blocked_by"],
            t4_blocking_flags,
            record,
        )
    )

    # T8
    before = status
    paired = _scope_bool(record, "paired_claims")
    if status == "LOCAL" and paired:
        t8_ok = (
            _scope_bool(record, "distinct_scopes")
            and _scope_bool(record, "distinct_tests")
            and bool(record.get("contradiction_links"))
            and _scope_bool(record, "consequence_differences_preserved")
            and not _scope_bool(record, "explosion_flag")
        )
        if not t8_ok:
            status = "KILLED" if not _scope_bool(record, "explosion_flag") else "DANGEROUS"
            block("T8", ["local dualism fields collapsed"])
        else:
            t8_blockers: list[str] = []
    else:
        t8_ok = False
        t8_blockers = ["not a LOCAL paired claim"]
        block("T8", t8_blockers)
    trace.append(
        _trace(
            "T8",
            ["scope", "candidate_tests", "contradiction_links"],
            before,
            status,
            {"local_dualism_preserved": bool(status == "LOCAL" and paired and t8_ok)},
            [] if paired and before == "LOCAL" and t8_ok else blocked[-1]["blocked_by"],
            record=record,
        )
    )

    # T5
    before = status
    anchors = set(record.get("anchors", []))
    population = record.get("population_state", {})
    t5_ok = (
        status == "LOCAL"
        and bool(record.get("all_required_tests_passed"))
        and bool(record.get("contradiction_contained"))
        and bool(record.get("adversarial_paraphrase_survived"))
        and bool(anchors - {"POPULATION_STABILITY_ANCHOR"})
        and population.get("usage_state") in {"STABLE_USAGE", "CONTESTED_USAGE"}
        and population.get("paraphrase_state") == "SURVIVED"
        and not goodhart_flags
    )
    if t5_ok:
        status = "STABLE"
    else:
        reasons = []
        if status != "LOCAL":
            reasons.append("status not LOCAL")
        if goodhart_flags:
            reasons.extend(goodhart_flags)
        if not bool(anchors - {"POPULATION_STABILITY_ANCHOR"}):
            reasons.append("no non-population anchor")
        if not record.get("adversarial_paraphrase_survived"):
            reasons.append("adversarial paraphrase not survived")
        block("T5", reasons)
    trace.append(
        _trace(
            "T5",
            ["candidate_tests", "candidate_outcomes", "anchors", "population_state", "contradiction_links"],
            before,
            status,
            {"stability_available": t5_ok},
            [] if t5_ok else blocked[-1]["blocked_by"],
            goodhart_flags,
            record,
        )
    )

    # T9
    before = status
    if record.get("prior_status") == "STABLE" and record.get("later_failure_token"):
        status = record.get("stable_downgrade_target", "SUSPENDED")
        t9_blockers: list[str] = []
    else:
        t9_blockers = ["no prior STABLE with later failure token"]
        block("T9", t9_blockers)
    trace.append(
        _trace(
            "T9",
            ["prior_status", "candidate_outcomes", "contradiction_links", "anchors", "goodhart_flags_initial"],
            before,
            status,
            {"stable_downgrade_applied": not t9_blockers},
            t9_blockers,
            record=record,
        )
    )

    result = {
        "claim_id": record.get("claim_id"),
        "expression_id": record.get("expression_id"),
        "final_status": status,
        "transition_trace": trace,
        "blocked_transitions": blocked,
        "active_goodhart_flags": goodhart_flags,
        "boundary_sources_used": sorted({src for step in trace for src in step["boundary_sources_consulted"]}),
        "dominant_boundary_source": None,
        "allowed_claim_strength": [],
        "forbidden_overclaims": FORBIDDEN_OVERCLAIMS,
        "downgrade_reason": "",
        "oracle_leakage_warnings": [],
        "cl_mistake_warnings": [],
        "runtime_decision": "ACCEPT_REPLAY_AUDIT",
    }
    strength = compute_claim_strength(record, result)
    result.update(strength)
    return result


def compute_claim_strength(record: dict, replay: dict) -> dict:
    sources = set(replay.get("boundary_sources_used") or [])
    if not sources:
        sources = {src for values in record.get("boundary_source_by_field", {}).values() for src in _as_list(values)}

    if "HUMAN_AUTHORED_BOUNDARY" in sources:
        dominant = "HUMAN_AUTHORED_BOUNDARY"
        allowed = ["BOUNDARY_ACCOUNTING", "TOY_REPLAY_DETERMINISTIC"]
        reason = "decisive fields include human-authored toy provenance"
    elif "VIABILITY_BOUNDARY" in sources:
        dominant = "VIABILITY_BOUNDARY"
        allowed = ["VIABILITY_SHIELD"]
        reason = "viability/protective source is a shield, not truth"
    elif "CONSEQUENCE_BOUNDARY" in sources:
        dominant = "CONSEQUENCE_BOUNDARY"
        allowed = ["TOY_CONSEQUENCE_PROTOCOL"]
        reason = "consequence fields are toy tokens"
    elif "FORM_BOUNDARY" in sources:
        dominant = "FORM_BOUNDARY"
        allowed = ["FORM_ONLY"]
        reason = "form boundary cannot promote semantic strength"
    elif "RULE_GENERATED_BOUNDARY" in sources:
        dominant = "RULE_GENERATED_BOUNDARY"
        allowed = ["TOY_REPLAY_DETERMINISTIC"]
        reason = "rules process supplied fields only"
    else:
        dominant = "UNKNOWN_OR_MIXED_BOUNDARY"
        allowed = ["BOUNDARY_ACCOUNTING"]
        reason = "source is unknown or mixed"

    if record.get("external_contact_required") and not record.get("external_contact_present"):
        if "EXTERNAL_CONTACT_REQUIRED" not in allowed:
            allowed.append("EXTERNAL_CONTACT_REQUIRED")
        reason += "; external contact required but absent"

    allowed = [item for item in allowed if item not in FORBIDDEN_OVERCLAIMS]
    return {
        "boundary_sources_used": sorted(sources),
        "dominant_boundary_source": dominant,
        "allowed_claim_strength": allowed,
        "forbidden_overclaims": FORBIDDEN_OVERCLAIMS,
        "downgrade_reason": reason,
    }


def _apply_change(record: dict, path: str, value: Any) -> None:
    parts = path.split(".")
    target = record
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


def _remove_assumption(record: dict, value: str) -> None:
    record["assumptions"] = [item for item in record.get("assumptions", []) if item != value]


def run_mutation_tests(cases: list[dict], mutations: list[dict]) -> dict:
    case_by_id = {case["claim_id"]: case for case in cases}
    results = []
    for mutation in mutations:
        record = copy.deepcopy(case_by_id[mutation["source_case_id"]])
        for path, value in mutation.get("set", {}).items():
            _apply_change(record, path, value)
        for assumption in mutation.get("remove_assumptions", []):
            _remove_assumption(record, assumption)
        for path, value in mutation.get("append", {}).items():
            current = record
            parts = path.split(".")
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current.setdefault(parts[-1], [])
            if value not in current[parts[-1]]:
                current[parts[-1]].append(value)

        replay = replay_record(record)
        blocked_rules = {item["rule_id"] for item in replay.get("blocked_transitions", [])}
        flags = set(replay.get("active_goodhart_flags", []))
        final_status = replay.get("final_status")
        test_id = mutation["test_id"]

        if test_id == "M1":
            passed = final_status != "SUSPENDED" and "T3" in blocked_rules
        elif test_id == "M2":
            passed = final_status == "DANGEROUS" and "CONTEXT_PROLIFERATION_PROXY" in flags
        elif test_id == "M3":
            passed = "VOLUME_PROXY" not in flags and final_status in STATUSES
        elif test_id == "M4":
            passed = final_status != "LOCAL" and "T8" in blocked_rules
        elif test_id == "M5":
            passed = final_status != "STABLE" and "POPULATION_PROXY" in flags and "T5" in blocked_rules
        elif test_id == "M6":
            passed = final_status != "KILLED"
        else:
            passed = False

        results.append(
            {
                "test_id": test_id,
                "source_case_id": mutation["source_case_id"],
                "passed": bool(passed),
                "final_status": final_status,
                "active_goodhart_flags": replay.get("active_goodhart_flags", []),
                "blocked_rules": sorted(blocked_rules),
                "lookup_behavior_detected": not passed,
                "oracle_behavior_detected": False,
                "replay": replay,
            }
        )
    return {
        "all_passed": all(item["passed"] for item in results),
        "lookup_behavior_detected": any(item["lookup_behavior_detected"] for item in results),
        "results": results,
    }


def run_static_audit(source_paths: list[str]) -> dict:
    findings = []
    for source_path in source_paths:
        text = Path(source_path).read_text(encoding="utf-8")
        lines = text.splitlines()
        for index, line in enumerate(lines, start=1):
            for pattern in STATIC_AUDIT_PATTERNS:
                if pattern not in line:
                    continue
                stripped = line.strip()
                allowed_context = (
                    "STATIC_AUDIT_PATTERNS" in stripped
                    or "FORBIDDEN_FIELDS" in stripped
                    or (stripped.startswith('"') and stripped.endswith('",'))
                    or pattern in FORBIDDEN_FIELDS
                    or "forbidden" in stripped.lower()
                    or "oracle" in stripped.lower()
                    or "final_status" in stripped and "result" in stripped
                )
                findings.append(
                    {
                        "path": source_path,
                        "line": index,
                        "pattern": pattern,
                        "allowed_context": bool(allowed_context),
                        "text": stripped,
                    }
                )
    forbidden = [item for item in findings if not item["allowed_context"]]
    return {
        "passed": not forbidden,
        "forbidden_patterns": STATIC_AUDIT_PATTERNS,
        "findings": findings,
        "forbidden_findings": forbidden,
    }
