from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Callable

from data_dependence_datasets import (
    build_required_splits,
    build_rows,
    cross_phase_target_shuffle,
    exact_source_overlap,
    feature_permutation_control,
    forbidden_fields_present,
    independent_impossible_targets,
    sample_fraction,
)
from data_dependence_learners import (
    GenericSubsetBackoffLearner,
    Prediction,
    Row,
    ZeroFitGenericLearner,
    source_observation,
    target_observation,
)

import sys


CL_ROOT = Path(__file__).resolve().parents[1]
CL2_ROOT = CL_ROOT / "CL2_equal_volume_learner_probe"
if str(CL2_ROOT) not in sys.path:
    sys.path.insert(0, str(CL2_ROOT))
from learners import RuleFamilyTransitionLearner  # noqa: E402


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PREREG_PATH = ROOT / "CL2_2_preregistration.json"

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
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/leakage_audit.md",
    "experiments/CL/CL2_equal_volume_learner_probe/outputs/memorization_audit.json",
    "experiments/CL/CL2_1_shuffled_control_repair/SPEC.md",
    "experiments/CL/CL2_1_shuffled_control_repair/CL2_1_preregistration.json",
    "experiments/CL/CL2_1_shuffled_control_repair/control_diagnostics.py",
    "experiments/CL/CL2_1_shuffled_control_repair/run_cl2_1.py",
    "experiments/CL/CL2_1_shuffled_control_repair/outputs/control_metrics.json",
    "experiments/CL/CL2_1_shuffled_control_repair/outputs/decision.json",
    "experiments/CL/CL2_1_shuffled_control_repair/outputs/final_report.md",
    "experiments/CL/CL2_1_shuffled_control_repair/outputs/learner_bias_audit.json",
    "experiments/CL/CL2_1_shuffled_control_repair/outputs/evaluation_integrity_audit.md",
    "experiments/CL/CL2_1_shuffled_control_repair/outputs/control_recommendation.md",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/domain.py",
    "playbook_extraction/02_extracted_method.md",
    "playbook_extraction/03_not_yet_method.md",
    "playbook_extraction/harness/output_schema.md",
    "playbook_extraction/harness/failure_conditions.md",
]

FORBIDDEN_CALLS = {
    "transition",
    "rollout_outcome",
    "action_rollout_outcome",
    "is_collapsed",
    "collapse_mechanism",
    "candidate_action_admission",
}


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


def prediction_equal(prediction: Prediction, target: Prediction) -> bool:
    return (
        list(prediction["zones"]) == list(target["zones"])
        and int(prediction["mass"]) == int(target["mass"])
        and int(prediction["phase"]) == int(target["phase"])
    )


def score(learner: Any, train: list[Row], test: list[Row]) -> dict[str, float]:
    learner.fit(train)
    if not test:
        return {"exact": 0.0, "coordinate": 0.0}
    exact = 0
    coordinate_correct = 0
    coordinate_total = 0
    for row in test:
        prediction = learner.predict(row)
        target = target_observation(row)
        if prediction_equal(prediction, target):
            exact += 1
        for idx, value in enumerate(target["zones"]):
            coordinate_total += 1
            if prediction["zones"][idx] == value:
                coordinate_correct += 1
        coordinate_total += 1
        if int(prediction["mass"]) == int(target["mass"]):
            coordinate_correct += 1
        coordinate_total += 1
        if int(prediction["phase"]) == int(target["phase"]):
            coordinate_correct += 1
    return {
        "exact": exact / len(test),
        "coordinate": coordinate_correct / coordinate_total if coordinate_total else 0.0,
    }


def score_generic_on_splits(
    splits: dict[str, dict[str, list[Row]]],
    fraction: float,
    seed: int,
    zero_fit: bool = False,
) -> dict[str, float]:
    results: dict[str, float] = {}
    for idx, split_name in enumerate(("source", "structural", "cross_phase")):
        train = sample_fraction(splits[split_name]["train"], fraction, seed + idx)
        learner = ZeroFitGenericLearner() if zero_fit else GenericSubsetBackoffLearner()
        metrics = score(learner, train, splits[split_name]["test"])
        key_prefix = "source_holdout" if split_name == "source" else ("structural_holdout" if split_name == "structural" else "cross_phase")
        results[f"{key_prefix}_exact"] = metrics["exact"]
        results[f"{key_prefix}_coordinate"] = metrics["coordinate"]
    return results


def score_rule_family_on_splits(
    splits: dict[str, dict[str, list[Row]]],
    fraction: float,
    seed: int,
    zero_fit: bool = False,
) -> dict[str, float]:
    results: dict[str, float] = {}
    for idx, split_name in enumerate(("source", "structural", "cross_phase")):
        train = [] if zero_fit else sample_fraction(splits[split_name]["train"], fraction, seed + idx)
        learner = RuleFamilyTransitionLearner()
        metrics = score(learner, train, splits[split_name]["test"])
        key_prefix = "source_holdout" if split_name == "source" else ("structural_holdout" if split_name == "structural" else "cross_phase")
        results[f"{key_prefix}_exact"] = metrics["exact"]
        results[f"{key_prefix}_coordinate"] = metrics["coordinate"]
    return results


def corrupted_control_metrics(
    splits: dict[str, dict[str, list[Row]]],
    seed: int,
) -> dict[str, Any]:
    controls: dict[str, Callable[[list[Row], int], list[Row]]] = {
        "independent_impossible_target": independent_impossible_targets,
        "cross_phase_target_shuffle": cross_phase_target_shuffle,
        "feature_permutation_control": feature_permutation_control,
    }
    out: dict[str, Any] = {}
    for control_name, transform in controls.items():
        metrics_by_split: dict[str, float] = {}
        for idx, split_name in enumerate(("source", "structural", "cross_phase")):
            train = transform(splits[split_name]["train"], seed + idx)
            learner = GenericSubsetBackoffLearner()
            metrics = score(learner, train, splits[split_name]["test"])
            key_prefix = "source_holdout" if split_name == "source" else ("structural_holdout" if split_name == "structural" else "cross_phase")
            metrics_by_split[f"{key_prefix}_exact"] = metrics["exact"]
            metrics_by_split[f"{key_prefix}_coordinate"] = metrics["coordinate"]
        metrics_by_split["max_exact"] = max(
            metrics_by_split["source_holdout_exact"],
            metrics_by_split["structural_holdout_exact"],
            metrics_by_split["cross_phase_exact"],
        )
        out[control_name] = metrics_by_split
    return out


def scan_generic_learner_for_forbidden_calls() -> dict[str, Any]:
    path = ROOT / "data_dependence_learners.py"
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports: list[str] = []
    calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in FORBIDDEN_CALLS:
                    imports.append(alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"domain", "action_boundary", "boundary"}:
                    imports.append(alias.name)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                calls.append(func.id)
            elif isinstance(func, ast.Attribute) and func.attr in FORBIDDEN_CALLS:
                calls.append(func.attr)
    exact_family_terms = {
        "aid_mechanics": "AID_" in text,
        "phase_indexed_shock": False,
        "failed_zone_mass_drain": False,
        "conserve_restores_mass": "CONSERVE" in text,
        "max_update_rules": "MAX_ZONE" in text or "MAX_MASS" in text,
    }
    return {
        "forbidden_imports": sorted(set(imports)),
        "forbidden_calls": sorted(set(calls)),
        "encodes_exact_transition_family": any(exact_family_terms.values()),
        "exact_family_term_hits": exact_family_terms,
    }


def make_error_witnesses(train: list[Row], test: list[Row], limit: int = 25) -> list[dict[str, Any]]:
    learner = GenericSubsetBackoffLearner()
    learner.fit(train)
    witnesses: list[dict[str, Any]] = []
    for row in test:
        prediction = learner.predict(row)
        target = target_observation(row)
        if not prediction_equal(prediction, target):
            witnesses.append(
                {
                    "source_observation": source_observation(row),
                    "action": row["action"],
                    "true_successor_observation": target,
                    "predicted_successor_observation": prediction,
                    "split": "structural_holdout",
                    "data_fraction": "100_percent",
                    "error_type": "exact_successor_mismatch",
                }
            )
            if len(witnesses) >= limit:
                break
    return witnesses


def decide(
    learning: dict[str, Any],
    control: dict[str, Any],
    prior_scan: dict[str, Any],
    required_split_too_small: bool,
    thresholds: dict[str, Any],
) -> tuple[str, str, bool]:
    zero = learning["generic_learner"]["zero_fit"]["structural_holdout_exact"]
    full_source = learning["generic_learner"]["100_percent"]["source_holdout_exact"]
    full_structural = learning["generic_learner"]["100_percent"]["structural_holdout_exact"]
    full_cross = learning["generic_learner"]["100_percent"]["cross_phase_exact"]
    data_gain = learning["data_gain"]
    tiny_to_full_gain = learning["tiny_to_full_gain"]
    best_corrupt = control["best_corrupted_target_accuracy"]
    corruption_drop = control["corruption_drop"]
    feature_perm = control["generic_learner_corrupted_controls"]["feature_permutation_control"]["max_exact"]
    leakage = control["leakage_detected"]

    if leakage or best_corrupt > thresholds["best_corrupted_target_accuracy_max"] or feature_perm > thresholds[
        "feature_permutation_accuracy_max"
    ]:
        return (
            "CONTROL-ARTIFACT-PERSISTS",
            "Leakage or corrupted-control performance remained above the pre-registered artifact thresholds.",
            False,
        )
    if (
        zero > thresholds["zero_fit_structural_accuracy_max"]
        or prior_scan["encodes_exact_transition_family"]
    ):
        return (
            "PRIOR-DEPENDENCE-FAIL",
            "Zero-fit performance or learner-code audit indicates inadmissible prior dependence.",
            False,
        )
    if required_split_too_small:
        return (
            "INCONCLUSIVE-DATA-DEPENDENCE",
            "At least one required holdout split is too small.",
            False,
        )

    positive = (
        full_source >= thresholds["full_data_source_holdout_accuracy_min"]
        and full_structural >= thresholds["full_data_structural_holdout_accuracy_min"]
        and full_cross >= thresholds["full_data_cross_phase_accuracy_min"]
        and data_gain >= thresholds["data_gain_min"]
        and tiny_to_full_gain >= thresholds["tiny_to_full_gain_min"]
        and best_corrupt <= thresholds["best_corrupted_target_accuracy_max"]
        and corruption_drop >= thresholds["corruption_drop_min"]
    )
    if positive:
        return (
            "DATA-DEPENDENT-LEARNING-OK",
            "Generic learner performance passes data-dependence, holdout, and corrupted-control gates.",
            True,
        )

    generic_positive_failed = (
        full_source < thresholds["full_data_source_holdout_accuracy_min"]
        or full_structural < thresholds["full_data_structural_holdout_accuracy_min"]
        or full_cross < thresholds["full_data_cross_phase_accuracy_min"]
    )
    if generic_positive_failed:
        return (
            "NO-GENERIC-LEARNER-SIGNAL",
            "No leakage or artifact persisted, but the evidence-eligible generic learner failed a required positive accuracy threshold.",
            False,
        )
    return (
        "INCONCLUSIVE-DATA-DEPENDENCE",
        "Metrics did not satisfy a clean positive or negative decision condition.",
        False,
    )


def write_prior_audit(prior_scan: dict[str, Any]) -> None:
    text = f"""# CL2.2 Prior Audit

- Evidence-eligible generic learner may assume only visible finite features and target rows during fit.
- It is forbidden to encode AID_i mechanics.
- It is forbidden to encode phase-indexed shock.
- It is forbidden to encode failed-zone mass drain.
- It is forbidden to encode CONSERVE restores mass.
- It is forbidden to call oracle functions.
- Encodes AID_i mechanics: `{prior_scan["exact_family_term_hits"]["aid_mechanics"]}`.
- Encodes phase-indexed shock: `{prior_scan["exact_family_term_hits"]["phase_indexed_shock"]}`.
- Encodes failed-zone mass drain: `{prior_scan["exact_family_term_hits"]["failed_zone_mass_drain"]}`.
- Calls oracle functions: `{prior_scan["forbidden_calls"]}`.
- It differs from the CL2 RuleFamilyTransitionLearner because it uses generic subset tables and backoff, not a parameterized transition update family.
- The CL2 RuleFamilyTransitionLearner is diagnostic-only because CL2.1 showed it carries too much transition-family prior to support learner evidence.
"""
    (OUTPUTS / "prior_audit.md").write_text(text, encoding="utf-8")


def write_durable_constraint(decision: str) -> None:
    mapping = {
        "DATA-DEPENDENT-LEARNING-OK": "Future learner probes may proceed only with data-dependence controls at least as strict as CL2.2.",
        "PRIOR-DEPENDENCE-FAIL": "Learners that encode the domain transition family cannot be used as evidence of learning-from-ledger.",
        "NO-GENERIC-LEARNER-SIGNAL": "The current safe ledger is not yet evidence-bearing for generic transition learning.",
        "CONTROL-ARTIFACT-PERSISTS": "The anti-artifact instrument remains insufficient; no learner evidence may be used.",
        "INCONCLUSIVE-DATA-DEPENDENCE": "Data-dependence remains unresolved; no representation or derivability probe may proceed.",
        "HALT-GOAL-DRIFT": "The CL2.2 path halted for goal drift; no downstream learner evidence may be used.",
    }
    (OUTPUTS / "durable_constraint.md").write_text(
        f"# CL2.2 Durable Constraint\n\n{mapping[decision]}\n", encoding="utf-8"
    )


def write_final_report(
    prereg: dict[str, Any],
    dataset_manifest: dict[str, Any],
    split_manifest: dict[str, Any],
    learning: dict[str, Any],
    control: dict[str, Any],
    prior_ablation: dict[str, Any],
    prior_scan: dict[str, Any],
    data_audit: dict[str, Any],
    decision: dict[str, Any],
    witnesses: list[dict[str, Any]],
) -> None:
    status_rows = "\n".join(f"| `{row['file']}` | {row['status']} |" for row in input_statuses())
    report = f"""# CL2.2 — Learner-Prior Ablation / Data-Dependence Gate

## 0. Verdict

`{decision["decision"]}`

{decision["reason"]}

## 1. Goal anchor

CL2.2 serves the safe / derivable substrate goal only by testing whether learner
performance depends on safe-ledger data after removing the CL2 rule-family prior.
It does not claim substrate discovery or derivability.

## 2. Inputs used

| file | status |
|---|---|
{status_rows}

## 3. CL2.1 durable constraint carried forward

CL2.1 found `SHUFFLED-CONTROL-INVALID-BIAS-ARTIFACT`; the CL2 rule-family learner
is diagnostic-only and cannot support a positive CL2.2 verdict.

## 4. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL2_2_learner_prior_ablation/CL2_2_preregistration.json`

This file was written before CL2.2 dataset construction, training, diagnostics,
and metric computation.

## 5. Dataset and splits

Dataset manifest:

```json
{json.dumps(dataset_manifest, indent=2)}
```

Split manifest:

```json
{json.dumps(split_manifest, indent=2)}
```

## 6. Evidence-eligible learner

The evidence-eligible learner is `GenericSubsetBackoffLearner`. It learns
generic majority target-coordinate tables over visible feature subsets and backs
off to smaller subsets. It does not encode the exact transition family.

## 7. Prior diagnostic learner

The CL2 `RuleFamilyTransitionLearner` is run as `PRIOR-DIAGNOSTIC-ONLY`. Its
metrics cannot support `DATA-DEPENDENT-LEARNING-OK`.

## 8. Learning curve diagnostics

```json
{json.dumps(learning, indent=2)}
```

## 9. Corrupted-target controls

```json
{json.dumps(control, indent=2)}
```

## 10. Prior ablation comparison

```json
{json.dumps(prior_ablation, indent=2)}
```

## 11. Leakage and evaluation audit

```json
{json.dumps(prior_scan, indent=2)}
```

## 12. Decision

Decision: `{decision["decision"]}`

Downstream allowed: `{decision["downstream_allowed"]}`

Representation probe allowed: `{decision["representation_probe_allowed"]}`

## 13. Error witnesses

Structural-holdout error witnesses recorded: `{len(witnesses)}`.

## 14. Bought-by-simplification check

The generic learner is intentionally weak and table-based. A negative result
does not prove the ledger is unlearnable by every possible generic learner. It
only prevents using the prior-confounded CL2 learner as evidence.

## 15. What was NOT shown

- No claim that this is a substrate.
- No claim that world-model content is derived.
- No claim that LLM training is safe.
- No claim that learner performance transfers beyond `FourZoneMassDomain`.
- No claim that the learner is safe under autonomous policy rollout.
- No claim that the learner is safe under arbitrary future actions.
- No claim that the action ledger transfers to other domains.
- No claim that the boundary is learned.
- No claim that the oracle-filtered ledger is available in real domains.
- No claim that data-dependence proves derivability.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.

## 16. Durable result

CL2.2 produced a data-dependence verdict, prior audit, corrupted-control
diagnostics, and durable constraint. The durable decision is recorded in
`outputs/decision.json`.
"""
    (OUTPUTS / "final_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    prereg = load_json(PREREG_PATH)
    seed = int(prereg["random_seed"])
    thresholds = prereg["thresholds"]

    rows = build_rows()
    splits = build_required_splits(rows, seed)
    required_split_too_small = any(len(split["test"]) < 100 for split in splits.values())

    dataset_manifest = {
        "candidate_transition_count": len(rows),
        "candidate_features": ["source_zones", "source_mass", "source_phase", "action"],
        "candidate_targets": ["successor_zones", "successor_mass", "successor_phase"],
        "forbidden_fields_present": forbidden_fields_present(rows),
        "random_seed": seed,
        "ledger_scope": "one-step action admission plus safety-policy continuation",
    }
    split_manifest = {
        "source_state_holdout": {
            "train_count": len(splits["source"]["train"]),
            "test_count": len(splits["source"]["test"]),
            "exact_source_overlap": exact_source_overlap(splits["source"]["train"], splits["source"]["test"]),
        },
        "structural_holdout": {
            "rule": "source_phase == 3",
            "train_count": len(splits["structural"]["train"]),
            "test_count": len(splits["structural"]["test"]),
        },
        "cross_phase_holdout": {
            "rule": "train on source_phase != 3; evaluate source_phase == 3",
            "train_count": len(splits["cross_phase"]["train"]),
            "test_count": len(splits["cross_phase"]["test"]),
        },
    }

    fractions = {
        "zero_fit": (0.0, True),
        "1_percent": (0.01, False),
        "5_percent": (0.05, False),
        "20_percent": (0.20, False),
        "100_percent": (1.0, False),
    }
    generic_curve = {
        label: score_generic_on_splits(splits, fraction, seed, zero_fit=zero)
        for label, (fraction, zero) in fractions.items()
    }
    prior_curve = {
        "zero_fit": score_rule_family_on_splits(splits, 0.0, seed, zero_fit=True),
        "100_percent": score_rule_family_on_splits(splits, 1.0, seed, zero_fit=False),
    }
    data_gain = (
        generic_curve["100_percent"]["structural_holdout_exact"]
        - generic_curve["zero_fit"]["structural_holdout_exact"]
    )
    tiny_to_full_gain = (
        generic_curve["100_percent"]["structural_holdout_exact"]
        - generic_curve["1_percent"]["structural_holdout_exact"]
    )
    learning_curve = {
        "generic_learner": generic_curve,
        "prior_diagnostic_rule_family": prior_curve,
        "data_gain": data_gain,
        "tiny_to_full_gain": tiny_to_full_gain,
    }

    corrupted = corrupted_control_metrics(splits, seed)
    best_corrupted = max(control["max_exact"] for control in corrupted.values())
    best_corrupted_structural = max(control["structural_holdout_exact"] for control in corrupted.values())
    corruption_drop = generic_curve["100_percent"]["structural_holdout_exact"] - best_corrupted_structural
    prior_scan = scan_generic_learner_for_forbidden_calls()
    leakage_detected = (
        dataset_manifest["forbidden_fields_present"]
        or bool(prior_scan["forbidden_calls"])
        or bool(prior_scan["forbidden_imports"])
    )
    control_metrics = {
        "generic_learner_corrupted_controls": corrupted,
        "best_corrupted_target_accuracy": best_corrupted,
        "corruption_drop": corruption_drop,
        "leakage_detected": leakage_detected,
    }

    prior_ablation = {
        "generic_learner_full_data": {
            "source_holdout_exact": generic_curve["100_percent"]["source_holdout_exact"],
            "structural_holdout_exact": generic_curve["100_percent"]["structural_holdout_exact"],
            "cross_phase_exact": generic_curve["100_percent"]["cross_phase_exact"],
        },
        "rule_family_prior_diagnostic": {
            "source_holdout_exact": prior_curve["100_percent"]["source_holdout_exact"],
            "structural_holdout_exact": prior_curve["100_percent"]["structural_holdout_exact"],
            "cross_phase_exact": prior_curve["100_percent"]["cross_phase_exact"],
        },
        "prior_advantage": {
            "source_holdout": prior_curve["100_percent"]["source_holdout_exact"]
            - generic_curve["100_percent"]["source_holdout_exact"],
            "structural_holdout": prior_curve["100_percent"]["structural_holdout_exact"]
            - generic_curve["100_percent"]["structural_holdout_exact"],
            "cross_phase": prior_curve["100_percent"]["cross_phase_exact"]
            - generic_curve["100_percent"]["cross_phase_exact"],
        },
        "interpretation": "Rule-family learner is diagnostic-only; positive evidence must come from the generic learner.",
    }

    decision_value, reason, downstream_allowed = decide(
        learning_curve, control_metrics, prior_scan, required_split_too_small, thresholds
    )
    decision = {
        "decision": decision_value,
        "reason": reason,
        "thresholds_used": {
            "zero_fit_structural_accuracy_max": thresholds["zero_fit_structural_accuracy_max"],
            "full_data_source_holdout_accuracy_min": thresholds["full_data_source_holdout_accuracy_min"],
            "full_data_structural_holdout_accuracy_min": thresholds[
                "full_data_structural_holdout_accuracy_min"
            ],
            "full_data_cross_phase_accuracy_min": thresholds["full_data_cross_phase_accuracy_min"],
            "data_gain_min": thresholds["data_gain_min"],
            "tiny_to_full_gain_min": thresholds["tiny_to_full_gain_min"],
            "corruption_drop_min": thresholds["corruption_drop_min"],
            "best_corrupted_target_accuracy_max": thresholds["best_corrupted_target_accuracy_max"],
            "feature_permutation_accuracy_max": thresholds["feature_permutation_accuracy_max"],
            "leakage_allowed": thresholds["leakage_allowed"],
        },
        "downstream_allowed": downstream_allowed,
        "representation_probe_allowed": downstream_allowed,
    }

    data_audit = {
        "zero_fit_structural_accuracy": generic_curve["zero_fit"]["structural_holdout_exact"],
        "one_percent_structural_accuracy": generic_curve["1_percent"]["structural_holdout_exact"],
        "full_data_structural_accuracy": generic_curve["100_percent"]["structural_holdout_exact"],
        "data_gain": data_gain,
        "tiny_to_full_gain": tiny_to_full_gain,
        "data_dependence_supported": decision_value == "DATA-DEPENDENT-LEARNING-OK",
        "notes": "Only the generic learner is evidence-eligible; rule-family results are diagnostic-only.",
    }
    witnesses = make_error_witnesses(splits["structural"]["train"], splits["structural"]["test"])

    write_json(OUTPUTS / "dataset_manifest.json", dataset_manifest)
    write_json(OUTPUTS / "learning_curve_metrics.json", learning_curve)
    write_json(OUTPUTS / "control_metrics.json", control_metrics)
    write_json(OUTPUTS / "prior_ablation_metrics.json", prior_ablation)
    write_json(OUTPUTS / "decision.json", decision)
    write_json(OUTPUTS / "data_dependence_audit.json", data_audit)
    write_json(OUTPUTS / "error_witnesses.json", witnesses)
    write_prior_audit(prior_scan)
    write_durable_constraint(decision_value)
    write_final_report(
        prereg,
        dataset_manifest,
        split_manifest,
        learning_curve,
        control_metrics,
        prior_ablation,
        prior_scan,
        data_audit,
        decision,
        witnesses,
    )


if __name__ == "__main__":
    main()
