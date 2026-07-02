from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from control_diagnostics import (
    CONTROL_TRANSFORMS,
    LEARNERS,
    RuleFamilyTransitionLearner,
    build_candidate_rows,
    evaluation_integrity,
    scan_learner_code_for_forbidden_calls,
    score_control,
    split_rows,
)


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PREREG_PATH = ROOT / "CL2_1_preregistration.json"

INPUT_FILES = [
    "experiments/CL/CL2_equal_volume_learner_probe/SPEC.md",
    "experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json",
    "experiments/CL/CL2_equal_volume_learner_probe/dataset_builder.py",
    "experiments/CL/CL2_equal_volume_learner_probe/learners.py",
    "experiments/CL/CL2_equal_volume_learner_probe/run_cl2.py",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/dataset_manifest.json",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/split_manifest.json",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/metrics.json",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/decision.json",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/final_report.md",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/domain.py",
    "playbook_extraction/02_extracted_method.md",
    "playbook_extraction/03_not_yet_method.md",
    "playbook_extraction/harness/output_schema.md",
    "playbook_extraction/harness/failure_conditions.md",
]


def project_root() -> Path:
    return ROOT.parents[2]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def input_statuses() -> list[dict[str, str]]:
    base = project_root()
    return [
        {"file": path, "status": "PRESENT" if (base / path).exists() else "MISSING"}
        for path in INPUT_FILES
    ]


def primary_metrics_by_control(splits: dict[str, dict[str, list[dict[str, Any]]]], seed: int) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for name, transform in CONTROL_TRANSFORMS.items():
        results[name] = score_control(RuleFamilyTransitionLearner, splits, transform, seed)
    return results


def learner_bias_audit(
    splits: dict[str, dict[str, list[dict[str, Any]]]],
    seed: int,
    thresholds: dict[str, Any],
) -> dict[str, Any]:
    by_learner: dict[str, Any] = {}
    for learner_name, learner_factory in LEARNERS.items():
        by_learner[learner_name] = {}
        for control_name, transform in CONTROL_TRANSFORMS.items():
            metrics = score_control(learner_factory, splits, transform, seed)
            by_learner[learner_name][control_name] = {
                "random_exact": metrics["random_exact"],
                "source_holdout_exact": metrics["source_holdout_exact"],
                "structural_holdout_exact": metrics["structural_holdout_exact"],
                "max_exact": metrics["max_exact"],
            }

    primary_high_controls = {
        name
        for name, metrics in by_learner["primary_rule_family_learner"].items()
        if metrics["max_exact"] > threshold_for_control(name, thresholds)
    }
    baseline_high_controls = set()
    for learner_name in ("majority_delta_baseline", "memorizer_baseline", "copy_source_baseline"):
        for name, metrics in by_learner[learner_name].items():
            if metrics["max_exact"] > threshold_for_control(name, thresholds):
                baseline_high_controls.add(name)

    return {
        **by_learner,
        "high_score_concentrated_in_primary": bool(primary_high_controls)
        and not baseline_high_controls.issuperset(primary_high_controls),
        "primary_high_controls": sorted(primary_high_controls),
        "baseline_high_controls": sorted(baseline_high_controls),
        "bias_artifact_supported": "original_global_shuffle" in primary_high_controls
        and "independent_impossible_target" not in primary_high_controls,
        "notes": "High shuffled scores are interpreted only as diagnostic evidence, not as CL2 success.",
    }


def threshold_for_control(name: str, thresholds: dict[str, Any]) -> float:
    if name == "original_global_shuffle":
        return thresholds["global_shuffle_exact_accuracy_max"]
    if name == "independent_impossible_target":
        return thresholds["independent_impossible_target_exact_accuracy_max"]
    if name == "feature_permutation_control":
        return thresholds["feature_permutation_exact_accuracy_max"]
    return thresholds[f"{name}_exact_accuracy_max"]


def decide(
    control_metrics: dict[str, Any],
    bias: dict[str, Any],
    thresholds: dict[str, Any],
) -> tuple[str, str, bool, str]:
    integrity = control_metrics["evaluation_integrity"]
    original = control_metrics["original_global_shuffle"]["primary"]["max_exact"]
    cross_action = control_metrics["cross_action_shuffle"]["primary"]["max_exact"]
    cross_phase = control_metrics["cross_phase_shuffle"]["primary"]["max_exact"]
    impossible = control_metrics["independent_impossible_target"]["primary"]["max_exact"]
    feature_perm = control_metrics["feature_permutation_control"]["primary"]["max_exact"]

    if integrity["evaluation_mismatch_detected"]:
        return (
            "EVALUATION-BUG-DETECTED",
            "Evaluation integrity check found target fields in features, test-target use, or target comparison mismatch.",
            False,
            "NO_RERUN_ALLOWED",
        )
    if integrity["forbidden_fields_present"] or integrity["forbidden_oracle_calls"] or impossible > thresholds[
        "independent_impossible_target_exact_accuracy_max"
    ]:
        return (
            "REAL-LEAKAGE-DETECTED",
            "Forbidden fields/calls were found or independent impossible targets scored above threshold.",
            False,
            "NO_RERUN_ALLOWED",
        )

    repaired_controls = []
    if cross_action <= thresholds["cross_action_shuffle_exact_accuracy_max"]:
        repaired_controls.append("RERUN_CL2_WITH_CROSS_ACTION_SHUFFLE")
    if cross_phase <= thresholds["cross_phase_shuffle_exact_accuracy_max"]:
        repaired_controls.append("RERUN_CL2_WITH_CROSS_PHASE_SHUFFLE")
    if impossible <= thresholds["independent_impossible_target_exact_accuracy_max"]:
        repaired_controls.append("RERUN_CL2_WITH_INDEPENDENT_IMPOSSIBLE_TARGET")
    if feature_perm <= thresholds["feature_permutation_exact_accuracy_max"]:
        repaired_controls.append("RERUN_CL2_WITH_FEATURE_PERMUTATION_CONTROL")

    if not repaired_controls:
        return (
            "INCONCLUSIVE-CONTROL-FAILURE",
            "No evaluation bug or real leakage was found, but all repaired controls remained high.",
            False,
            "NO_RERUN_ALLOWED",
        )

    artifact_supported = (
        original > thresholds["global_shuffle_exact_accuracy_max"]
        and (
            cross_action <= thresholds["cross_action_shuffle_exact_accuracy_max"]
            or cross_phase <= thresholds["cross_phase_shuffle_exact_accuracy_max"]
            or impossible <= thresholds["independent_impossible_target_exact_accuracy_max"]
        )
        and bool(bias["high_score_concentrated_in_primary"])
    )

    if artifact_supported:
        return (
            "SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT",
            "Original shuffled control failure is best explained as an invalid anti-artifact control for the primary rule-family learner, not as proven CL2 success.",
            False,
            "NO_RERUN_ALLOWED",
        )

    recommendation = (
        "RERUN_CL2_WITH_MULTIPLE_REPAIRED_CONTROLS"
        if len(repaired_controls) > 1
        else repaired_controls[0]
    )
    return (
        "CONTROL-REPAIRED-CL2-RERUN-ALLOWED",
        "At least one stronger repaired negative control passed below threshold and learner-bias artifact criteria did not trigger.",
        True,
        recommendation,
    )


def write_evaluation_integrity_audit(metrics: dict[str, Any]) -> None:
    text = f"""# CL2.1 Evaluation Integrity Audit

- target fields appear in learner features: `{metrics["target_fields_in_features"]}`.
- test targets are used in fit: `{metrics["test_target_used_in_fit"]}`.
- shuffled-control test targets remain original true targets: `{metrics["shuffled_control_test_targets_remain_original"]}`.
- prediction is compared against original true test targets: `{metrics["prediction_compared_to_original_true_target"]}`.
- forbidden fields exist in rows: `{metrics["forbidden_fields_present"]}`.
- forbidden oracle calls are imported or called: `{metrics["forbidden_oracle_calls"]}`.
- independent impossible targets scored below threshold: recorded in `outputs/impossible_target_diagnostics.json`.
- evaluation mismatch found: `{metrics["evaluation_mismatch_detected"]}`.
"""
    (OUTPUTS / "evaluation_integrity_audit.md").write_text(text, encoding="utf-8")


def write_control_recommendation(recommendation: str, decision: str, thresholds: dict[str, Any]) -> None:
    if recommendation == "NO_RERUN_ALLOWED":
        text = """# CL2.1 Control Recommendation

NO_RERUN_ALLOWED

No CL2 rerun is allowed under this CL2.1 decision.
"""
    else:
        text = f"""# CL2.1 Control Recommendation

{recommendation}

Replacement pre-registered thresholds for a future CL2 rerun:

- cross-action shuffle max exact accuracy <= {thresholds["cross_action_shuffle_exact_accuracy_max"]}
- cross-phase shuffle max exact accuracy <= {thresholds["cross_phase_shuffle_exact_accuracy_max"]}
- independent impossible target max exact accuracy <= {thresholds["independent_impossible_target_exact_accuracy_max"]}
- feature permutation max exact accuracy <= {thresholds["feature_permutation_exact_accuracy_max"]}

This recommendation only allows a repaired CL2 rerun. It does not allow
representation analysis, derivability claims, autonomous rollout, LLM training,
or substrate claims.
"""
    (OUTPUTS / "control_recommendation.md").write_text(text, encoding="utf-8")


def write_final_report(
    prereg: dict[str, Any],
    control_metrics: dict[str, Any],
    shuffle_diagnostics: dict[str, Any],
    impossible_diagnostics: dict[str, Any],
    bias: dict[str, Any],
    decision: dict[str, Any],
    recommendation: str,
) -> None:
    status_rows = "\n".join(f"| `{row['file']}` | {row['status']} |" for row in input_statuses())
    report = f"""# CL2.1 — Shuffled-Control Repair / Artifact Isolation Gate

## 0. Verdict

`{decision["decision"]}`

{decision["reason"]}

## 1. Goal anchor

CL2.1 serves the safe / derivable substrate goal only by repairing the
anti-artifact instrument required before a CL2 learner-probe claim can be
trusted. It does not claim CL2 passed.

## 2. Inputs used

| file | status |
|---|---|
{status_rows}

## 3. CL2 failure being repaired

CL2 halted with `LEARNER-LEAKAGE-FAIL` because the shuffled-target control
exceeded its threshold. CL2.1 diagnoses whether that was leakage, an evaluation
bug, a marginal artifact, or an invalid control for the primary learner's
inductive bias.

## 4. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL2_1_shuffled_control_repair/CL2_1_preregistration.json`

This file was written before diagnostic metrics were computed. Thresholds were
loaded from the preregistration and not changed after seeing diagnostics.

## 5. Evaluation integrity audit

```json
{json.dumps(control_metrics["evaluation_integrity"], indent=2)}
```

## 6. Shuffle diagnostics

```json
{json.dumps(shuffle_diagnostics, indent=2)}
```

## 7. Impossible-target and feature-permutation diagnostics

```json
{json.dumps(impossible_diagnostics, indent=2)}
```

## 8. Learner bias ablation

```json
{json.dumps(bias, indent=2)}
```

## 9. Competing explanations

H1 real leakage: evaluated by forbidden fields/calls and independent impossible
target control.

H2 evaluation bug: evaluated by target-feature separation, fit/test separation,
and original-true-target comparison.

H3 marginal artifact: evaluated by within/cross action and phase shuffles.

H4 strong inductive bias: evaluated by comparing the primary rule-family learner
against majority-delta, memorizer, and copy-source baselines.

## 10. Decision

Decision: `{decision["decision"]}`

CL2 rerun allowed: `{decision["cl2_rerun_allowed"]}`

Downstream representation allowed: `{decision["downstream_representation_allowed"]}`

## 11. Replacement control recommendation

`{recommendation}`

If a rerun is allowed, it is only a repaired CL2 rerun with the replacement
controls and thresholds stated in `outputs/control_recommendation.md`.

## 12. Bought-by-simplification check

The diagnostics still use the same toy finite ledger and hand-designed learner
family. Repairing a control does not establish learner success. The only
allowed inference is whether CL2's anti-artifact instrument can be made more
trustworthy.

## 13. What was NOT shown

- No claim that CL2 passed.
- No claim that learner transition learning is admissible evidence yet.
- No claim that this is a substrate.
- No claim that world-model content is derived.
- No claim that LLM training is safe.
- No claim that action-ledger safety transfers to other domains.
- No claim that the boundary is learned.
- No claim that the oracle-filtered ledger is available in real domains.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.
- No claim that repairing a control proves the learner result.

## 14. Durable result

CL2.1 produced an instrument verdict plus detailed diagnostics for shuffled
controls, impossible targets, feature permutation, learner bias, and evaluation
integrity. The durable result is the decision in `outputs/decision.json`.
"""
    (OUTPUTS / "final_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    prereg = load_json(PREREG_PATH)
    seed = int(prereg["random_seed"])
    thresholds = prereg["thresholds"]
    rows = build_candidate_rows(horizon=6)
    splits = split_rows(rows, seed)
    code_scan = scan_learner_code_for_forbidden_calls()
    integrity = evaluation_integrity(rows, code_scan)

    primary = primary_metrics_by_control(splits, seed)
    control_metrics = {
        "evaluation_integrity": integrity,
        "original_global_shuffle": {"primary": primary["original_global_shuffle"]},
        "within_action_shuffle": {"primary": primary["within_action_shuffle"]},
        "within_phase_shuffle": {"primary": primary["within_phase_shuffle"]},
        "cross_action_shuffle": {"primary": primary["cross_action_shuffle"]},
        "cross_phase_shuffle": {"primary": primary["cross_phase_shuffle"]},
        "independent_impossible_target": {"primary": primary["independent_impossible_target"]},
        "feature_permutation_control": {"primary": primary["feature_permutation_control"]},
    }
    shuffle_diagnostics = {
        key: primary[key]
        for key in (
            "original_global_shuffle",
            "within_action_shuffle",
            "within_phase_shuffle",
            "cross_action_shuffle",
            "cross_phase_shuffle",
        )
    }
    impossible_diagnostics = {
        "independent_impossible_target": primary["independent_impossible_target"],
        "feature_permutation_control": primary["feature_permutation_control"],
    }
    bias = learner_bias_audit(splits, seed, thresholds)
    decision_value, reason, rerun_allowed, recommendation = decide(control_metrics, bias, thresholds)
    decision = {
        "decision": decision_value,
        "reason": reason,
        "thresholds_used": {
            "global_shuffle_exact_accuracy_max": thresholds["global_shuffle_exact_accuracy_max"],
            "within_action_shuffle_exact_accuracy_max": thresholds[
                "within_action_shuffle_exact_accuracy_max"
            ],
            "within_phase_shuffle_exact_accuracy_max": thresholds[
                "within_phase_shuffle_exact_accuracy_max"
            ],
            "cross_action_shuffle_exact_accuracy_max": thresholds[
                "cross_action_shuffle_exact_accuracy_max"
            ],
            "cross_phase_shuffle_exact_accuracy_max": thresholds[
                "cross_phase_shuffle_exact_accuracy_max"
            ],
            "independent_impossible_target_exact_accuracy_max": thresholds[
                "independent_impossible_target_exact_accuracy_max"
            ],
            "feature_permutation_exact_accuracy_max": thresholds[
                "feature_permutation_exact_accuracy_max"
            ],
            "evaluation_mismatch_allowed": thresholds["evaluation_mismatch_allowed"],
            "forbidden_field_allowed": thresholds["forbidden_field_allowed"],
            "forbidden_oracle_call_allowed": thresholds["forbidden_oracle_call_allowed"],
        },
        "cl2_rerun_allowed": rerun_allowed,
        "downstream_representation_allowed": False,
    }

    write_json(OUTPUTS / "control_metrics.json", control_metrics)
    write_json(OUTPUTS / "shuffle_diagnostics.json", shuffle_diagnostics)
    write_json(OUTPUTS / "impossible_target_diagnostics.json", impossible_diagnostics)
    write_json(OUTPUTS / "learner_bias_audit.json", bias)
    write_json(OUTPUTS / "decision.json", decision)
    write_evaluation_integrity_audit(integrity)
    write_control_recommendation(recommendation, decision_value, thresholds)
    write_final_report(
        prereg,
        control_metrics,
        shuffle_diagnostics,
        impossible_diagnostics,
        bias,
        decision,
        recommendation,
    )


if __name__ == "__main__":
    main()
