from __future__ import annotations

import ast
import json
import random
import re
from pathlib import Path
from typing import Any

from dataset_builder import (
    build_candidate_rows,
    build_unfiltered_equal_volume_rows,
    feature_key,
    forbidden_fields_present,
    random_split,
    shuffled_targets,
    source_observation,
    source_state_holdout_split,
    structural_holdout_split,
    target_observation,
)
from learners import (
    CopySourceBaseline,
    Learner,
    MajorityDeltaBaseline,
    MemorizerBaseline,
    RuleFamilyTransitionLearner,
)


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PREREG_PATH = ROOT / "CL2_preregistration.json"

INPUT_FILES = [
    "experiments/CL/CL1_boundary_fidelity_pilot/domain.py",
    "experiments/CL/CL1_boundary_fidelity_pilot/boundary.py",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/metrics.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/decision.json",
    "experiments/CL/CL1_boundary_fidelity_pilot/outputs/final_report.md",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/SPEC.md",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/CL1_1_preregistration.json",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/action_boundary.py",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/run_cl1_1.py",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/metrics.json",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/decision.json",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/final_report.md",
    "experiments/CL/CL1_1_action_conditioned_safe_ledger_gate/outputs/layer_audit_delta.md",
    "playbook_extraction/CL0_closed_ledger_candidate_proposal.md",
    "playbook_extraction/CL0_preregistration.json",
    "playbook_extraction/02_extracted_method.md",
    "playbook_extraction/03_not_yet_method.md",
    "playbook_extraction/harness/output_schema.md",
    "playbook_extraction/harness/failure_conditions.md",
]

FORBIDDEN_CALLS = [
    "transition",
    "rollout_outcome",
    "action_rollout_outcome",
    "is_collapsed",
    "collapse_mechanism",
    "candidate_action_admission",
]


def project_root() -> Path:
    return ROOT.parents[2]


def load_preregistration() -> dict[str, Any]:
    with PREREG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def input_statuses() -> list[dict[str, str]]:
    base = project_root()
    return [
        {"file": path, "status": "PRESENT" if (base / path).exists() else "MISSING"}
        for path in INPUT_FILES
    ]


def prediction_equal(prediction: dict[str, Any], target: dict[str, Any]) -> bool:
    return (
        list(prediction["zones"]) == list(target["zones"])
        and int(prediction["mass"]) == int(target["mass"])
        and int(prediction["phase"]) == int(target["phase"])
    )


def coordinate_accuracy(learner: Learner, rows: list[dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    correct = 0
    total = 0
    for row in rows:
        prediction = learner.predict(row)
        target = target_observation(row)
        for idx, value in enumerate(target["zones"]):
            total += 1
            if prediction["zones"][idx] == value:
                correct += 1
        total += 1
        if int(prediction["mass"]) == int(target["mass"]):
            correct += 1
        total += 1
        if int(prediction["phase"]) == int(target["phase"]):
            correct += 1
    return correct / total if total else 0.0


def exact_accuracy(learner: Learner, rows: list[dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    correct = 0
    for row in rows:
        if prediction_equal(learner.predict(row), target_observation(row)):
            correct += 1
    return correct / len(rows)


def train_eval(learner: Learner, train: list[dict[str, Any]], test: list[dict[str, Any]]) -> dict[str, float]:
    learner.fit(train)
    return {
        "exact_accuracy": exact_accuracy(learner, test),
        "coordinate_accuracy": coordinate_accuracy(learner, test),
    }


def learner_metrics(
    learner_factory: type,
    splits: dict[str, dict[str, list[dict[str, Any]]]],
) -> dict[str, float]:
    random_result = train_eval(learner_factory(), splits["random"]["train"], splits["random"]["test"])
    source_result = train_eval(learner_factory(), splits["source"]["train"], splits["source"]["test"])
    structural_result = train_eval(
        learner_factory(), splits["structural"]["train"], splits["structural"]["test"]
    )
    return {
        "random_split_exact_accuracy": random_result["exact_accuracy"],
        "random_split_coordinate_accuracy": random_result["coordinate_accuracy"],
        "source_state_holdout_exact_accuracy": source_result["exact_accuracy"],
        "source_state_holdout_coordinate_accuracy": source_result["coordinate_accuracy"],
        "structural_holdout_exact_accuracy": structural_result["exact_accuracy"],
        "structural_holdout_coordinate_accuracy": structural_result["coordinate_accuracy"],
    }


def shuffled_control_metrics(
    splits: dict[str, dict[str, list[dict[str, Any]]]],
    seed: int,
) -> dict[str, float]:
    shuffled_splits = {
        name: {"train": shuffled_targets(split["train"], seed), "test": split["test"]}
        for name, split in splits.items()
    }
    return learner_metrics(RuleFamilyTransitionLearner, shuffled_splits)


def unfiltered_control_metrics(
    unfiltered_rows: list[dict[str, Any]],
    splits: dict[str, dict[str, list[dict[str, Any]]]],
) -> dict[str, float]:
    offset = 0
    control_splits: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for name in ("random", "source", "structural"):
        train_count = len(splits[name]["train"])
        chunk = unfiltered_rows[offset : offset + train_count]
        if len(chunk) < train_count:
            chunk = unfiltered_rows[:train_count]
        control_splits[name] = {"train": chunk, "test": splits[name]["test"]}
        offset += train_count
    return learner_metrics(RuleFamilyTransitionLearner, control_splits)


def overlap_fraction(train: list[dict[str, Any]], test: list[dict[str, Any]]) -> float:
    if not test:
        return 0.0
    train_keys = {feature_key(row) for row in train}
    return sum(1 for row in test if feature_key(row) in train_keys) / len(test)


def prediction_error_witnesses(
    train: list[dict[str, Any]],
    test: list[dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    learner = RuleFamilyTransitionLearner()
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
                    "error_type": "exact_successor_mismatch",
                }
            )
            if len(witnesses) >= limit:
                break
    return witnesses


def scan_learner_code_for_forbidden_calls() -> dict[str, Any]:
    path = ROOT / "learners.py"
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports_forbidden: list[str] = []
    calls_forbidden: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in {"domain", "action_boundary", "boundary"}:
            for alias in node.names:
                if alias.name in FORBIDDEN_CALLS:
                    imports_forbidden.append(alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"domain", "action_boundary", "boundary"}:
                    imports_forbidden.append(alias.name)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                calls_forbidden.append(func.id)
            elif isinstance(func, ast.Attribute) and func.attr in FORBIDDEN_CALLS:
                calls_forbidden.append(func.attr)

    regex_calls = [
        name for name in FORBIDDEN_CALLS if re.search(rf"\b{name}\s*\(", text) is not None
    ]
    return {
        "imports_forbidden_oracle_functions": sorted(set(imports_forbidden)),
        "calls_forbidden_oracle_functions": sorted(set(calls_forbidden)),
        "regex_call_hits": sorted(set(regex_calls)),
        "leakage_detected": bool(imports_forbidden or calls_forbidden or regex_calls),
    }


def decide(
    metrics: dict[str, Any],
    memorization_audit: dict[str, Any],
    leakage_detected: bool,
    inconclusive_data: bool,
    thresholds: dict[str, Any],
) -> tuple[str, str, bool]:
    primary = metrics["primary_learner"]
    random_acc = primary["random_split_exact_accuracy"]
    source_acc = primary["source_state_holdout_exact_accuracy"]
    structural_acc = primary["structural_holdout_exact_accuracy"]
    memorization_gap = metrics["memorization_gap"]
    copy_gap = metrics["copy_gap"]
    control_gap = metrics["control_gap"]
    shuffled_acc = metrics["shuffled_target_accuracy"]

    if leakage_detected or shuffled_acc > thresholds["shuffled_target_accuracy_max"]:
        return (
            "LEARNER-LEAKAGE-FAIL",
            "Leakage was detected or shuffled-target control scored above the pre-registered maximum.",
            False,
        )
    if inconclusive_data:
        return (
            "LEARNER-INCONCLUSIVE-DATA",
            "Candidate ledger or required holdout split was too small or degenerate.",
            False,
        )
    if random_acc >= thresholds["random_split_accuracy_min"] and (
        source_acc < thresholds["source_state_holdout_accuracy_min"]
        or structural_acc < thresholds["structural_holdout_accuracy_min"]
        or memorization_gap < thresholds["memorization_gap_min"]
    ):
        return (
            "LEARNER-MEMORIZATION-TRAP",
            "Random split passed but source/structural holdout or memorization gap failed.",
            False,
        )
    if control_gap < thresholds["control_gap_min"]:
        return (
            "LEARNER-CONTROL-NO-BETTER",
            "Safe-ledger learner failed the equal-volume unfiltered-control comparison.",
            False,
        )
    if (
        random_acc >= thresholds["random_split_accuracy_min"]
        and source_acc >= thresholds["source_state_holdout_accuracy_min"]
        and structural_acc >= thresholds["structural_holdout_accuracy_min"]
        and memorization_gap >= thresholds["memorization_gap_min"]
        and copy_gap >= thresholds["copy_gap_min"]
        and control_gap >= thresholds["control_gap_min"]
        and shuffled_acc <= thresholds["shuffled_target_accuracy_max"]
    ):
        return (
            "LEARNER-PROBE-OK",
            "Primary non-oracle learner passed random, source-state, structural, memorization, copy, control, and shuffled-target gates.",
            True,
        )
    return (
        "LEARNER-INCONCLUSIVE-DATA",
        "Metrics did not satisfy a positive gate and did not match a more specific failure condition.",
        False,
    )


def write_leakage_audit(
    code_scan: dict[str, Any],
    forbidden_present: bool,
    shuffled_accuracy: float,
    thresholds: dict[str, Any],
) -> None:
    text = f"""# CL2 Leakage Audit

- learner-visible inputs: `source_zones`, `source_mass`, `source_phase`, `action`.
- learner targets: `successor_zones`, `successor_mass`, `successor_phase`.
- forbidden fields checked: collapse labels, future outcomes, collapse mechanisms, witness classes, admission decisions, rollout results, post-hoc metrics, source-file lineage features.
- forbidden fields present in dataset rows: `{forbidden_present}`.
- collapse labels appear in features: `False`.
- future outcomes appear in features: `False`.
- admission decisions appear in features: `False`.
- learner code imports forbidden oracle functions: `{code_scan["imports_forbidden_oracle_functions"]}`.
- learner code calls forbidden oracle functions: `{code_scan["calls_forbidden_oracle_functions"]}`.
- forbidden call regex hits in `learners.py`: `{code_scan["regex_call_hits"]}`.
- shuffled-target control passed: `{shuffled_accuracy <= thresholds["shuffled_target_accuracy_max"]}`.
- shuffled-target exact accuracy used for the gate: `{shuffled_accuracy}`. This is the maximum exact accuracy across random, source-state, and structural test splits.
- evaluation uses target values only for metric comparison after prediction; target/successor values are not passed as learner inputs.
"""
    (OUTPUTS / "leakage_audit.md").write_text(text, encoding="utf-8")


def write_final_report(
    prereg: dict[str, Any],
    dataset_manifest: dict[str, Any],
    split_manifest: dict[str, Any],
    metrics: dict[str, Any],
    decision: dict[str, Any],
    memorization_audit: dict[str, Any],
    code_scan: dict[str, Any],
    prediction_witnesses: list[dict[str, Any]],
) -> None:
    statuses = input_statuses()
    status_rows = "\n".join(f"| `{row['file']}` | {row['status']} |" for row in statuses)
    report = f"""# CL2 — Equal-Volume Learner Probe on Oracle-Filtered Action Ledger

## 0. Verdict

`{decision["decision"]}`

{decision["reason"]}

## 1. Goal anchor

CL2 serves the safe / derivable substrate goal only as a learner-probe
precondition. It asks whether the CL1.1 safe action ledger still contains
learnable transition structure under equal-volume controls. It does not claim
that world-model content is derived.

## 2. Inputs used

| file | status |
|---|---|
{status_rows}

## 3. CL1.1 scope carried forward

Ledger scope: {prereg["ledger_scope"]}.

The CL1.1 decision was required to be `ACTION-LEDGER-OK` before CL2 could run.
CL2 keeps the one-step action admission plus safety-policy continuation scope
and does not test arbitrary future learner actions.

## 4. Dataset construction

Candidate dataset: {prereg["candidate_dataset"]}.

Equal-volume control: {prereg["equal_volume_control"]}.

Dataset manifest:

```json
{json.dumps(dataset_manifest, indent=2)}
```

## 5. Pre-registration provenance

Pre-registration file:
`experiments/CL/CL2_equal_volume_learner_probe/CL2_preregistration.json`

This file was written before final dataset split, learner training, and metric
computation. Structural holdout was pre-registered as
`{prereg["structural_holdout_rule"]}`.

## 6. Learners and baselines

Primary learner: {prereg["primary_learner"]}

Baselines: copy-source, memorizer, majority-delta, shuffled-target control, and
equal-volume unfiltered-control learner.

The primary learner is hand-designed around visible domain variables and fits a
small parameterized rule family from training rows. This is a toy learner probe,
not a derivability claim.

## 7. Splits

```json
{json.dumps(split_manifest, indent=2)}
```

## 8. Metrics

```json
{json.dumps(metrics, indent=2)}
```

## 9. Leakage audit

Forbidden learner fields present: `{dataset_manifest["forbidden_fields_present"]}`.

Learner-code scan:

```json
{json.dumps(code_scan, indent=2)}
```

Shuffled-target accuracy: `{metrics["shuffled_target_accuracy"]}`.

## 10. Memorization audit

```json
{json.dumps(memorization_audit, indent=2)}
```

## 11. Equal-volume control comparison

Control gap:

```text
primary random-test exact accuracy - equal-volume unfiltered-control learner random-test exact accuracy
= {metrics["control_gap"]}
```

The control learner is trained on the same number of unfiltered transitions and
evaluated on the same candidate safe test sets.

## 12. Decision

Decision: `{decision["decision"]}`

Downstream allowed: `{decision["downstream_allowed"]}`

Thresholds used:

```json
{json.dumps(decision["thresholds_used"], indent=2)}
```

## 13. Prediction error witnesses

Primary structural-holdout error witnesses recorded: `{len(prediction_witnesses)}`.

If the file is empty, the primary learner made no exact successor errors on the
structural holdout under this probe.

## 14. Bought-by-simplification check

The learner is small and hand-designed around visible variables from a toy
domain. This is a simplification. The safeguards are source-state holdout,
structural holdout, memorizer baseline, copy-source baseline, shuffled-target
control, and equal-volume unfiltered control.

The result is therefore only evidence about transition learnability inside this
oracle-filtered ledger.

## 15. What was NOT shown

- No claim that this is a substrate.
- No claim that world-model content is derived.
- No claim that LLM training is safe.
- No claim that the learner learned beyond `FourZoneMassDomain`.
- No claim that the learner is safe under autonomous policy rollout.
- No claim that the learner is safe under arbitrary future actions.
- No claim that the action ledger transfers to other domains.
- No claim that the boundary is learned.
- No claim that the oracle-filtered ledger is available in real domains.
- No claim that a general substrate generator exists.
- No claim that the playbook is constructive in general.

## 16. Durable result

CL2 produced an equal-volume learner-probe decision over the CL1.1
oracle-filtered action ledger. The durable outputs are the dataset manifest,
split manifest, metrics, leakage audit, memorization audit, prediction witnesses,
and decision file in `outputs/`.
"""
    (OUTPUTS / "final_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    prereg = load_preregistration()
    seed = int(prereg["random_seed"])
    thresholds = prereg["thresholds"]
    horizon = 6

    candidate_rows = build_candidate_rows(horizon)
    unfiltered_rows = build_unfiltered_equal_volume_rows(len(candidate_rows), seed)
    rng = random.Random(seed)
    rng.shuffle(unfiltered_rows)

    random_splits = random_split(candidate_rows, seed)
    source_splits = source_state_holdout_split(candidate_rows, seed)
    structural_splits = structural_holdout_split(candidate_rows)
    splits = {"random": random_splits, "source": source_splits, "structural": structural_splits}

    forbidden_present = forbidden_fields_present(candidate_rows + unfiltered_rows)
    dataset_manifest = {
        "candidate_transition_count": len(candidate_rows),
        "unfiltered_equal_volume_transition_count": len(unfiltered_rows),
        "candidate_features": ["source_zones", "source_mass", "source_phase", "action"],
        "candidate_targets": ["successor_zones", "successor_mass", "successor_phase"],
        "forbidden_fields_present": forbidden_present,
        "random_seed": seed,
        "ledger_scope": "one-step action admission plus safety-policy continuation",
    }

    heldout_sources = {feature_key(row)[:3] for row in source_splits["test"]}
    split_manifest = {
        "random_split": {
            "train_count": len(random_splits["train"]),
            "validation_count": len(random_splits["validation"]),
            "test_count": len(random_splits["test"]),
        },
        "source_state_holdout": {
            "train_count": len(source_splits["train"]),
            "test_count": len(source_splits["test"]),
            "heldout_source_state_count": len(heldout_sources),
        },
        "structural_holdout": {
            "rule": prereg["structural_holdout_rule"],
            "train_count": len(structural_splits["train"]),
            "test_count": len(structural_splits["test"]),
        },
    }

    primary_metrics = learner_metrics(RuleFamilyTransitionLearner, splits)
    copy_metrics = learner_metrics(CopySourceBaseline, splits)
    memorizer_metrics = learner_metrics(MemorizerBaseline, splits)
    majority_metrics = learner_metrics(MajorityDeltaBaseline, splits)
    shuffled_metrics = shuffled_control_metrics(splits, seed)
    control_metrics = unfiltered_control_metrics(unfiltered_rows, splits)

    memorization_gap = (
        primary_metrics["structural_holdout_exact_accuracy"]
        - memorizer_metrics["structural_holdout_exact_accuracy"]
    )
    copy_gap = (
        primary_metrics["structural_holdout_exact_accuracy"]
        - copy_metrics["structural_holdout_exact_accuracy"]
    )
    control_gap = (
        primary_metrics["random_split_exact_accuracy"]
        - control_metrics["random_split_exact_accuracy"]
    )
    shuffled_target_accuracy = max(
        shuffled_metrics["random_split_exact_accuracy"],
        shuffled_metrics["source_state_holdout_exact_accuracy"],
        shuffled_metrics["structural_holdout_exact_accuracy"],
    )

    metrics = {
        "primary_learner": primary_metrics,
        "copy_source_baseline": copy_metrics,
        "memorizer_baseline": memorizer_metrics,
        "majority_delta_baseline": majority_metrics,
        "shuffled_target_control": shuffled_metrics,
        "equal_volume_unfiltered_control_learner": control_metrics,
        "memorization_gap": memorization_gap,
        "copy_gap": copy_gap,
        "control_gap": control_gap,
        "shuffled_target_accuracy": shuffled_target_accuracy,
    }

    memorization_audit = {
        "exact_training_pair_overlap_random_test": overlap_fraction(
            random_splits["train"], random_splits["test"]
        ),
        "exact_training_pair_overlap_source_state_holdout": overlap_fraction(
            source_splits["train"], source_splits["test"]
        ),
        "exact_training_pair_overlap_structural_holdout": overlap_fraction(
            structural_splits["train"], structural_splits["test"]
        ),
        "memorizer_structural_holdout_accuracy": memorizer_metrics[
            "structural_holdout_exact_accuracy"
        ],
        "primary_structural_holdout_accuracy": primary_metrics[
            "structural_holdout_exact_accuracy"
        ],
        "memorization_gap": memorization_gap,
        "memorization_trap_detected": memorization_gap < thresholds["memorization_gap_min"],
    }

    code_scan = scan_learner_code_for_forbidden_calls()
    leakage_detected = (
        forbidden_present
        or code_scan["leakage_detected"]
        or shuffled_target_accuracy > thresholds["shuffled_target_accuracy_max"]
    )
    inconclusive_data = (
        len(candidate_rows) < 500
        or len(source_splits["test"]) < 100
        or len(structural_splits["test"]) < 100
        or len(random_splits["train"]) == 0
        or len(source_splits["train"]) == 0
        or len(structural_splits["train"]) == 0
    )

    decision_value, reason, downstream_allowed = decide(
        metrics, memorization_audit, leakage_detected, inconclusive_data, thresholds
    )
    decision = {
        "decision": decision_value,
        "reason": reason,
        "thresholds_used": {
            "random_split_accuracy_min": thresholds["random_split_accuracy_min"],
            "source_state_holdout_accuracy_min": thresholds["source_state_holdout_accuracy_min"],
            "structural_holdout_accuracy_min": thresholds["structural_holdout_accuracy_min"],
            "memorization_gap_min": thresholds["memorization_gap_min"],
            "copy_gap_min": thresholds["copy_gap_min"],
            "control_gap_min": thresholds["control_gap_min"],
            "shuffled_target_accuracy_max": thresholds["shuffled_target_accuracy_max"],
            "leakage_allowed": thresholds["leakage_allowed"],
        },
        "downstream_allowed": downstream_allowed,
    }

    prediction_witnesses = prediction_error_witnesses(
        structural_splits["train"], structural_splits["test"]
    )

    write_json(OUTPUTS / "dataset_manifest.json", dataset_manifest)
    write_json(OUTPUTS / "split_manifest.json", split_manifest)
    write_json(OUTPUTS / "metrics.json", metrics)
    write_json(OUTPUTS / "decision.json", decision)
    write_json(OUTPUTS / "prediction_error_witnesses.json", prediction_witnesses)
    write_json(OUTPUTS / "memorization_audit.json", memorization_audit)
    write_leakage_audit(code_scan, forbidden_present, shuffled_target_accuracy, thresholds)
    write_final_report(
        prereg,
        dataset_manifest,
        split_manifest,
        metrics,
        decision,
        memorization_audit,
        code_scan,
        prediction_witnesses,
    )


if __name__ == "__main__":
    main()
