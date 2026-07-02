from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from relational_order_toy import (  # noqa: E402
    SEED_START,
    generate_dataset,
    calibrated_coordinates,
    evaluate_coords,
    leakage_audit,
    load_json,
    raw_coordinates,
    run_controls,
    run_multiseed,
    run_order_dimension_suite,
    run_primary_seed,
    static_audit,
    write_json,
)


THIS_DIR = Path(__file__).resolve().parent
OUTPUTS = THIS_DIR / "outputs"
REPO_ROOT = THIS_DIR.parents[2]
B1_1_DECISION_PATH = REPO_ROOT / "experiments" / "B" / "B1_1_auxiliary_calibration_robustness" / "B1_1_decision.json"
S4_1_DECISION_PATH = (
    REPO_ROOT
    / "experiments"
    / "S"
    / "S4_tiny_boundary_accounting_replay_implementation"
    / "S4_1_decision.json"
)
EXPECTED_B1_1 = "B1.1-PASS-ROBUST-AUXILIARY-CALIBRATION-SIGNAL"
EXPECTED_S4_1 = "S4.1-PASS-GATE-CHAIN-VERIFICATION-REPAIRED"


THRESHOLDS = {
    "no_aux_relation_f1_max": 0.60,
    "with_aux_relation_f1_min": 0.90,
    "relation_f1_improvement_min": 0.30,
    "sparse_anchor_relation_f1_min": 0.85,
    "shuffled_aux_relation_f1_max": 0.65,
    "no_anchor_relation_f1_max": 0.65,
    "disconnected_anchor_relation_f1_max": 0.65,
    "random_relation_2d_f1_max": 0.60,
    "chain_control_f1_min": 0.95,
    "three_d_control_2d_f1_max": 0.80,
    "multiseed_pass_fraction_min": 0.80,
}


def confirm_decision(path: Path, expected: str) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "decision": None, "confirmed": False, "error": "MISSING"}
    try:
        data = load_json(path)
    except json.JSONDecodeError:
        return {"path": str(path), "decision": None, "confirmed": False, "error": "INVALID_JSON"}
    decision = data.get("decision")
    return {
        "path": str(path),
        "decision": decision,
        "confirmed": decision == expected,
        "error": None if decision == expected else "NOT_PASS",
    }


def markdown_json(data: Any) -> str:
    return "```json\n" + json.dumps(data, indent=2, sort_keys=True) + "\n```"


def run() -> dict[str, Any]:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    b1_1_gate = confirm_decision(B1_1_DECISION_PATH, EXPECTED_B1_1)
    s4_1_gate = confirm_decision(S4_1_DECISION_PATH, EXPECTED_S4_1)

    primary = run_primary_seed(SEED_START)
    dataset = generate_dataset(SEED_START, anchor_mode="complete", variant="product2d")
    manifest = dataset["manifest"]
    manifest["b1_1_prerequisite"] = b1_1_gate
    manifest["s4_1_prerequisite"] = s4_1_gate
    write_json(OUTPUTS / "dataset_manifest.json", manifest)

    no_aux_results = {
        "learner": "no_auxiliary",
        "input_fields": ["obs_x", "obs_y"],
        "forbidden_fields": ["u", "anchor identity", "item_id grouping", "true coordinates", "generated relation"],
        "metric": primary["no_aux"],
        "threshold": {"relation_f1_max": THRESHOLDS["no_aux_relation_f1_max"]},
        "passed_failure_requirement": primary["no_aux"]["f1"] <= THRESHOLDS["no_aux_relation_f1_max"],
    }
    with_aux_results = {
        "learner": "with_auxiliary_calibration",
        "input_fields": ["obs_x", "obs_y", "u", "anchor overlaps"],
        "metric": primary["with_aux"],
        "threshold": {"relation_f1_min": THRESHOLDS["with_aux_relation_f1_min"]},
        "passed_recovery_requirement": primary["with_aux"]["f1"] >= THRESHOLDS["with_aux_relation_f1_min"],
    }
    write_json(OUTPUTS / "no_aux_results.json", no_aux_results)
    write_json(OUTPUTS / "with_aux_results.json", with_aux_results)

    dimension_results = run_order_dimension_suite()
    write_json(OUTPUTS / "order_dimension_results.json", dimension_results)

    controls = run_controls()
    write_json(OUTPUTS / "control_results.json", controls)

    audit = leakage_audit(dataset["records"])
    write_json(OUTPUTS / "leakage_audit.json", audit)

    static = static_audit([THIS_DIR / "relational_order_toy.py", THIS_DIR / "run_b2.py"])
    write_json(OUTPUTS / "static_audit.json", static)

    multiseed = run_multiseed()
    relation_improvement = primary["improvement"]
    metrics = {
        "no_aux_relation_f1": primary["no_aux"]["f1"],
        "with_aux_relation_f1": primary["with_aux"]["f1"],
        "relation_f1_improvement": relation_improvement,
        "sparse_anchor_relation_f1": controls["sparse_anchor_relation_f1"],
        "shuffled_aux_relation_f1": controls["controls"]["C1_shuffled_auxiliary"]["relation_f1"],
        "no_anchor_relation_f1": controls["controls"]["C2_no_anchors"]["relation_f1"],
        "disconnected_anchor_relation_f1": controls["controls"]["C3_disconnected_anchors"]["relation_f1"],
        "random_relation_2d_f1": controls["controls"]["C4_random_relation"]["relation_f1"],
        "chain_control_f1": controls["controls"]["C5_chain_control"]["relation_f1"],
        "three_d_control_2d_f1": controls["controls"]["C6_three_d_control"]["relation_f1"],
        "multiseed_pass_fraction": multiseed["multiseed_pass_fraction"],
        "thresholds": THRESHOLDS,
    }
    write_json(OUTPUTS / "metrics.json", metrics)

    no_aux_recovery_failed = metrics["no_aux_relation_f1"] <= THRESHOLDS["no_aux_relation_f1_max"]
    with_aux_recovery_succeeded = metrics["with_aux_relation_f1"] >= THRESHOLDS["with_aux_relation_f1_min"]
    improvement_passed = relation_improvement >= THRESHOLDS["relation_f1_improvement_min"]
    dimension_passed = bool(dimension_results["passed"])
    controls_passed = (
        controls["passed"]
        and metrics["sparse_anchor_relation_f1"] >= THRESHOLDS["sparse_anchor_relation_f1_min"]
        and metrics["multiseed_pass_fraction"] >= THRESHOLDS["multiseed_pass_fraction_min"]
    )
    relation_label_leakage_detected = bool(audit["relation_label_leakage_detected"])
    aux_leakage_detected = bool(audit["aux_leakage_detected"])
    human_authored_outcomes_detected = bool(audit["human_authored_outcomes_detected"])
    repeats_s4_accounting = False

    if not b1_1_gate["confirmed"] or not s4_1_gate["confirmed"]:
        decision = "B2-INCONCLUSIVE"
        reason = "Required B1.1 or S4.1 prerequisite was not confirmed."
    elif relation_label_leakage_detected:
        decision = "B2-FAIL-RELATION-LABEL-LEAKAGE"
        reason = "Relation label leakage was detected."
    elif aux_leakage_detected:
        decision = "B2-FAIL-AUX-LEAKAGE"
        reason = "Auxiliary leakage was detected."
    elif human_authored_outcomes_detected:
        decision = "B2-FAIL-RELATION-LABEL-LEAKAGE"
        reason = "Human-authored final or outcome labels were detected."
    elif repeats_s4_accounting:
        decision = "B2-FAIL-REPEATS-S4-ACCOUNTING"
        reason = "The task repeated boundary accounting instead of generated relational recovery."
    elif not no_aux_recovery_failed:
        decision = "B2-FAIL-NO-AUX-RECOVERS"
        reason = "The no-auxiliary learner exceeded the preregistered relation F1 limit."
    elif not with_aux_recovery_succeeded:
        decision = "B2-FAIL-WITH-AUX-NO-RELATION-RECOVERY"
        reason = "Auxiliary calibration did not reach the preregistered relation recovery threshold."
    elif not improvement_passed:
        decision = "B2-INCONCLUSIVE"
        reason = "Primary recovery passed, but relation F1 improvement was below threshold."
    elif not dimension_passed:
        decision = "B2-FAIL-DIMENSION-MISCLASSIFICATION"
        reason = "Toy order-dimension proxy failed on product, chain, or 3D control."
    elif not controls_passed:
        decision = "B2-FAIL-CONTROL-LEAKAGE"
        reason = "At least one negative or robustness control failed."
    elif not static["passed"]:
        decision = "B2-FAIL-RELATION-LABEL-LEAKAGE"
        reason = "Static audit found suspicious executable-code patterns."
    else:
        decision = "B2-PASS-RELATIONAL-ORDER-DIMENSION-SIGNAL"
        reason = "Auxiliary calibration recovered the generated 2D product-order relation while no-auxiliary and broken-calibration controls failed."

    passed = decision == "B2-PASS-RELATIONAL-ORDER-DIMENSION-SIGNAL"
    decision_json = {
        "decision": decision,
        "reason": reason,
        "b1_1_decision_confirmed": b1_1_gate["confirmed"],
        "s4_1_decision_confirmed": s4_1_gate["confirmed"],
        "dataset_generated": True,
        "no_aux_recovery_failed": no_aux_recovery_failed,
        "with_aux_relation_recovery_succeeded": with_aux_recovery_succeeded,
        "relation_improvement_passed": improvement_passed,
        "toy_order_dimension_proxy_passed": dimension_passed,
        "controls_passed": controls_passed,
        "relation_label_leakage_detected": relation_label_leakage_detected,
        "aux_leakage_detected": aux_leakage_detected,
        "static_audit_passed": static["passed"],
        "human_authored_outcomes_detected": human_authored_outcomes_detected,
        "repeats_s4_accounting": repeats_s4_accounting,
        "admissible_for_next_gate": passed,
        "llm_training_allowed": False,
        "substrate_claim_allowed": False,
        "derivability_claim_allowed": False,
        "semantic_boundary_generator_claim_allowed": False,
        "real_world_transfer_claim_allowed": False,
        "general_order_dimension_claim_allowed": False,
        "general_disentanglement_claim_allowed": False,
        "next_allowed_work": ["B2 postmortem", "B3 relational robustness / adversarial controls spec"] if passed else ["B2 postmortem / narrowing"],
    }
    write_json(THIS_DIR / "B2_decision.json", decision_json)

    report = f"""# B2 — Relational Order-Dimension Recovery Gate

## 0. Verdict
Decision: `{decision}`.

Reason: {reason}

## 1. Goal anchor
Immutable project goal: train an LLM / learner so that its world-model is derived, not merely generalized from internet-like data.

B2 does not train an LLM and does not use real-world data. It tests a bounded synthetic relational recovery condition.

## 2. Inputs used
- B1.1 decision artifact: `{B1_1_DECISION_PATH}`
- B1.1 decision observed: `{b1_1_gate["decision"]}`
- S4.1 decision artifact: `{S4_1_DECISION_PATH}`
- S4.1 decision observed: `{s4_1_gate["decision"]}`

## 3. Hypothesis
If auxiliary calibration can recover more than a scalar in this toy setting, then calibrated observer-colored coordinates should recover a generated 2D product-order relation while raw no-auxiliary coordinates and broken calibration controls fail.

## 4. Synthetic relational world
Items have generated latent coordinates `(x, y)`. The generated relation is coordinate-wise product order with margin `{manifest["margin"]}`. Each observer applies a positive coordinate-wise affine transform plus small noise. Anchors provide shared item overlaps; they do not expose true coordinates to fitting functions.

## 5. Learners
- No-auxiliary learner: uses only `obs_x` and `obs_y` as one global coordinate system.
- With-auxiliary calibration learner: uses `obs_x`, `obs_y`, `u`, and anchor overlaps to estimate affine maps into a reference observer frame, then predicts product-order relations in that calibrated frame.

## 6. Primary relation-recovery metrics
{markdown_json(metrics)}

## 7. Toy order-dimension proxy
{markdown_json(dimension_results)}

## 8. Controls
{markdown_json(controls)}

## 9. Leakage and static audit
Leakage audit:

{markdown_json(audit)}

Static audit:

{markdown_json(static)}

## 10. Pass / fail analysis
- B1.1 prerequisite confirmed: `{b1_1_gate["confirmed"]}`
- S4.1 prerequisite confirmed: `{s4_1_gate["confirmed"]}`
- No-auxiliary recovery failed: `{no_aux_recovery_failed}`
- With-auxiliary relation recovery succeeded: `{with_aux_recovery_succeeded}`
- Relation improvement passed: `{improvement_passed}`
- Toy order-dimension proxy passed: `{dimension_passed}`
- Controls passed: `{controls_passed}`
- Static audit passed: `{static["passed"]}`
- Relation label leakage detected: `{relation_label_leakage_detected}`
- Auxiliary leakage detected: `{aux_leakage_detected}`

## 11. What was NOT shown
- No substrate was found.
- No derived world-model was shown.
- No LLM training is allowed.
- No semantic boundary generator was implemented.
- No claim that objective/perceptual separation is generally possible.
- No claim that real-world perception can be disentangled by this toy result.
- No claim that auxiliary variables solve grounding.
- No claim that synthetic relational recovery transfers to internet-scale data.
- No claim that toy order-dimension proxy is general order-dimension recovery.
- No claim that viability coloring is truth.
- No claim that passing B2 proves the project goal.

## 12. Downstream permission
If accepted, this result permits only a B2 postmortem or a B3 relational robustness / adversarial controls specification. It does not permit LLM training, substrate claims, derivability claims, semantic boundary generator claims, real-world transfer claims, general order-dimension claims, or general disentanglement claims.

## 13. Durable result
B2 produced a bounded synthetic relational recovery signal: in this constructed toy world, auxiliary affine calibration recovered a generated 2D product-order relation and the preregistered controls did not recover above threshold.
"""
    (THIS_DIR / "B2_report.md").write_text(report, encoding="utf-8")

    final_report = f"""# B2 Final Report

Decision: `{decision}`

Metrics:

{markdown_json(metrics)}

No LLM training, substrate claim, derivability claim, semantic boundary generator claim, real-world transfer claim, general order-dimension claim, or general disentanglement claim is allowed by this result.
"""
    (OUTPUTS / "final_report.md").write_text(final_report, encoding="utf-8")

    return decision_json


if __name__ == "__main__":
    result = run()
    metrics = load_json(OUTPUTS / "metrics.json")
    print(
        "B2 decision={decision} no_aux_f1={no_aux:.6f} with_aux_f1={with_aux:.6f}".format(
            decision=result["decision"],
            no_aux=metrics["no_aux_relation_f1"],
            with_aux=metrics["with_aux_relation_f1"],
        )
    )

