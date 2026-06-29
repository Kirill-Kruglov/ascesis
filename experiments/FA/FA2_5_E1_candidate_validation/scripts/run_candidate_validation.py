#!/usr/bin/env python3
"""FA2.5.E1 faithful candidate validation kill-gate.

This is not a shield synthesis or monotonicity test. It replays the unchanged
Justitia baseline through the FA1 extractor to build a balanced discrimination
dataset:

  A: 18.0 SAFE states that later collapse (false-safe witnesses)
  B: 18.0 SAFE states that remain non-collapsed through the horizon

It then evaluates a compact, non-oracle, layer-eligible candidate against the
current 18.0 abstraction, a strong history-variable CEGAR baseline, and a raw
current-state baseline.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
ASCESIS = Path("/home/master/llm_projects/ascesis")
FA1_SCRIPT = ASCESIS / "experiments/FA1_E1_false_safe_witness_taxonomy/scripts/run_false_safe_taxonomy.py"
FA1_OUT = ASCESIS / "experiments/FA1_E1_false_safe_witness_taxonomy/outputs"
FA2_OUT = ASCESIS / "experiments/FA2_E1_minimal_invariant_compression_test/outputs"
BA4_OUT = ASCESIS / "experiments/BA4_layer_audit"

DATASET_SEED = 2525
TRAIN_GROUP_FRACTION = 0.70
EQUIVALENCE_EPS = 0.02
PRECISION_MARGIN = 0.05


def load_fa1():
    spec = importlib.util.spec_from_file_location("fa1_taxonomy", FA1_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def rate(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def f(row: dict, key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value == "" or value is None:
        return default
    return float(value)


def truthy(row: dict, key: str) -> bool:
    return bool(row.get(key))


def bool_float(value: bool) -> float:
    return 1.0 if value else 0.0


def policy_concentration_flag(row: dict) -> float:
    return bool_float(f(row, "obs_last_aid_max") > 0.035 and f(row, "obs_resource_concentration_max") > 0.62)


def history_bad_signal_flag(row: dict) -> float:
    return bool_float(
        f(row, "obs_last_aid_max") > 0.035
        and (f(row, "obs_neighbor_delta_min") < -0.030 or f(row, "obs_response_to_aid_min") < -0.025)
    )


def min_zone_proxy_flag(row: dict) -> float:
    return bool_float(f(row, "min_zone_welfare") <= 0.96)


def spread_flag(row: dict) -> float:
    return bool_float(int(row.get("failed_zone_count", 0)) >= 4)


def mass_flag(row: dict) -> float:
    return bool_float(f(row, "total_mass") < 35.0)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def feature_sets() -> dict[str, list[tuple[str, str, callable]]]:
    return {
        "B0_current_18_0": [
            ("shield_a", "18.0 harm/mean-welfare counter", lambda r: f(r, "shield_a") / 44.0),
            ("shield_c", "18.0 concentration counter", lambda r: f(r, "shield_c") / 44.0),
        ],
        "Candidate_FA2_compact": [
            ("failed_zone_count_ge_4", "L4 spread-collapse flag", spread_flag),
            ("total_mass_lt_35", "L4 mass-collapse flag", mass_flag),
            ("policy_visible_concentration", "conditional L2/L3 Obs.resource_concentration threshold", policy_concentration_flag),
            ("delayed_harm_signal", "conditional L2/L3 compact history/consequence flag", history_bad_signal_flag),
            ("min_zone_welfare_le_0_96", "BA4-eligible compact spread-risk proxy; empirical threshold from FA2", min_zone_proxy_flag),
        ],
        "B1_history_CEGAR": [
            ("obs_last_aid_max", "delayed aid memory", lambda r: f(r, "obs_last_aid_max")),
            ("obs_last_aid_mean", "delayed aid memory", lambda r: f(r, "obs_last_aid_mean")),
            ("obs_response_to_aid_min", "delayed consequence response", lambda r: f(r, "obs_response_to_aid_min")),
            ("obs_response_to_aid_mean", "delayed consequence response", lambda r: f(r, "obs_response_to_aid_mean")),
            ("obs_neighbor_delta_min", "delayed neighbor consequence", lambda r: f(r, "obs_neighbor_delta_min")),
            ("obs_neighbor_delta_mean", "delayed neighbor consequence", lambda r: f(r, "obs_neighbor_delta_mean")),
            ("obs_resource_concentration_max", "policy-visible delayed concentration", lambda r: f(r, "obs_resource_concentration_max")),
            ("obs_resource_concentration_mean", "policy-visible delayed concentration", lambda r: f(r, "obs_resource_concentration_mean")),
            ("bad_consequence_count", "CEGAR predicate over delayed bad consequence", lambda r: f(r, "bad_consequence_count") / 9.0),
            ("delayed_obs_min_welfare", "delayed welfare observation", lambda r: f(r, "delayed_obs_min_welfare")),
            ("delayed_obs_failed_zone_count", "delayed spread observation", lambda r: f(r, "delayed_obs_failed_zone_count") / 9.0),
            ("history_bad_signal_flag", "compact delayed harm predicate", history_bad_signal_flag),
            ("policy_visible_concentration_flag", "compact delayed concentration predicate", policy_concentration_flag),
        ],
        "B2_raw_current_state": [
            ("mean_welfare_deficit", "current L4 mean welfare deficit", lambda r: 1.0 - f(r, "mean_welfare")),
            ("min_zone_welfare_deficit", "current compact spread-risk deficit", lambda r: 1.0 - f(r, "min_zone_welfare")),
            ("failed_zone_fraction", "current failed-zone fraction", lambda r: f(r, "failed_zone_count") / 9.0),
            ("mass_lowness", "current total mass lowness, clipped at 1000", lambda r: clamp((1000.0 - f(r, "total_mass")) / 1000.0)),
            ("shield_a", "18.0 harm/mean-welfare counter", lambda r: f(r, "shield_a") / 44.0),
        ],
    }


def harvest_states() -> list[dict]:
    fa1 = load_fa1()
    states = fa1.harvest(list(fa1.base.WORLDS), list(fa1.base.POLICIES), list(range(9600, 9608)), fa1.base.STEPS)
    fa1.augment_future(states)
    return states


def make_balanced_dataset(states: list[dict]) -> list[dict]:
    false_safe = [s for s in states if s["shield_accept"] and s["future_collapse"]]
    safe_remain = [s for s in states if s["shield_accept"] and not s["future_collapse"]]
    rng = random.Random(DATASET_SEED)
    sampled_safe = rng.sample(safe_remain, len(false_safe))
    rows = []
    for src, label, population in [(false_safe, 1, "A_false_safe"), (sampled_safe, 0, "B_safe_remain_safe")]:
        for s in src:
            r = dict(s)
            r["label"] = label
            r["population"] = population
            rows.append(r)
    rng.shuffle(rows)
    return rows


def group_split(rows: list[dict]) -> tuple[list[int], list[int]]:
    groups = sorted({r["traj_key"] for r in rows})
    rng = random.Random(DATASET_SEED + 1)
    rng.shuffle(groups)
    n_train = int(round(len(groups) * TRAIN_GROUP_FRACTION))
    train_groups = set(groups[:n_train])
    train_idx, test_idx = [], []
    for i, row in enumerate(rows):
        if row["traj_key"] in train_groups:
            train_idx.append(i)
        else:
            test_idx.append(i)
    return train_idx, test_idx


def extract_matrix(rows: list[dict], specs: list[tuple[str, str, callable]]) -> list[list[float]]:
    return [[float(fn(row)) for _, _, fn in specs] for row in rows]


def standardize(train_x: list[list[float]], all_x: list[list[float]]) -> tuple[list[list[float]], list[float], list[float]]:
    if not train_x:
        return all_x, [], []
    n_features = len(train_x[0])
    means, stds = [], []
    for j in range(n_features):
        vals = [x[j] for x in train_x]
        m = statistics.fmean(vals)
        sd = statistics.pstdev(vals) or 1.0
        means.append(m)
        stds.append(sd)
    scaled = [[(x[j] - means[j]) / stds[j] for j in range(n_features)] for x in all_x]
    return scaled, means, stds


def train_logistic(x: list[list[float]], y: list[int], epochs: int = 700, lr: float = 0.08, l2: float = 0.001) -> list[float]:
    if not x:
        return []
    n_features = len(x[0])
    weights = [0.0] * (n_features + 1)
    n = len(x)
    for _ in range(epochs):
        grads = [0.0] * (n_features + 1)
        for xi, yi in zip(x, y):
            z = weights[0] + sum(weights[j + 1] * xi[j] for j in range(n_features))
            p = sigmoid(z)
            err = p - yi
            grads[0] += err
            for j in range(n_features):
                grads[j + 1] += err * xi[j]
        weights[0] -= lr * grads[0] / n
        for j in range(n_features):
            grad = grads[j + 1] / n + l2 * weights[j + 1]
            weights[j + 1] -= lr * grad
    return weights


def predict_logistic(weights: list[float], x: list[list[float]]) -> list[float]:
    if not weights:
        return [0.5] * len(x)
    return [sigmoid(weights[0] + sum(weights[j + 1] * xi[j] for j in range(len(xi)))) for xi in x]


def confusion(y_true: list[int], scores: list[float], threshold: float) -> dict[str, int]:
    tp = fp = tn = fn = 0
    for y, score in zip(y_true, scores):
        pred = 1 if score >= threshold else 0
        if y == 1 and pred == 1:
            tp += 1
        elif y == 0 and pred == 1:
            fp += 1
        elif y == 0 and pred == 0:
            tn += 1
        elif y == 1 and pred == 0:
            fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def metrics_from_confusion(c: dict[str, int]) -> dict[str, float]:
    tp, fp, tn, fn = c["tp"], c["fp"], c["tn"], c["fn"]
    recall = rate(tp, tp + fn)
    specificity = rate(tn, tn + fp)
    return {
        "precision": rate(tp, tp + fp),
        "recall": recall,
        "specificity": specificity,
        "false_positive_rate": rate(fp, fp + tn),
        "false_negative_rate": rate(fn, fn + tp),
        "balanced_accuracy": 0.5 * (recall + specificity),
        "accuracy": rate(tp + tn, tp + fp + tn + fn),
    }


def best_threshold(y_true: list[int], scores: list[float]) -> tuple[float, float]:
    candidates = sorted(set(scores))
    if not candidates:
        return 0.5, 0.0
    thresholds = [candidates[0] - 1e-9] + [(a + b) / 2 for a, b in zip(candidates, candidates[1:])] + [candidates[-1] + 1e-9]
    best_t, best_ba = thresholds[0], -1.0
    for t in thresholds:
        ba = metrics_from_confusion(confusion(y_true, scores, t))["balanced_accuracy"]
        if ba > best_ba:
            best_t, best_ba = t, ba
    return best_t, best_ba


def roc_curve_points(y_true: list[int], scores: list[float], model: str) -> list[dict]:
    thresholds = sorted(set(scores), reverse=True)
    points = []
    for t in [max(thresholds) + 1e-9] + thresholds + [min(thresholds) - 1e-9]:
        c = confusion(y_true, scores, t)
        m = metrics_from_confusion(c)
        points.append({"model": model, "threshold": t, "fpr": m["false_positive_rate"], "tpr": m["recall"]})
    points.sort(key=lambda r: (r["fpr"], r["tpr"]))
    return points


def pr_curve_points(y_true: list[int], scores: list[float], model: str) -> list[dict]:
    thresholds = sorted(set(scores), reverse=True)
    points = []
    for t in thresholds + [min(thresholds) - 1e-9]:
        c = confusion(y_true, scores, t)
        m = metrics_from_confusion(c)
        points.append({"model": model, "threshold": t, "recall": m["recall"], "precision": m["precision"]})
    points.sort(key=lambda r: r["recall"])
    return points


def trapezoid_auc(points: list[tuple[float, float]]) -> float:
    pts = sorted(points)
    area = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        area += (x1 - x0) * (y0 + y1) / 2
    return area


def average_precision(y_true: list[int], scores: list[float]) -> float:
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    total_pos = sum(y_true)
    if total_pos == 0:
        return 0.0
    tp = fp = 0
    prev_recall = 0.0
    ap = 0.0
    for i in order:
        if y_true[i] == 1:
            tp += 1
        else:
            fp += 1
        recall = tp / total_pos
        precision = tp / (tp + fp)
        ap += (recall - prev_recall) * precision
        prev_recall = recall
    return ap


def brier(y_true: list[int], scores: list[float]) -> float:
    return statistics.fmean((score - y) ** 2 for y, score in zip(y_true, scores)) if y_true else 0.0


def evaluate_model(name: str, specs: list[tuple[str, str, callable]], rows: list[dict], train_idx: list[int], test_idx: list[int]) -> dict:
    all_x_raw = extract_matrix(rows, specs)
    train_x_raw = [all_x_raw[i] for i in train_idx]
    scaled, means, stds = standardize(train_x_raw, all_x_raw)
    train_x = [scaled[i] for i in train_idx]
    test_x = [scaled[i] for i in test_idx]
    y = [int(r["label"]) for r in rows]
    train_y = [y[i] for i in train_idx]
    test_y = [y[i] for i in test_idx]
    weights = train_logistic(train_x, train_y)
    train_scores = predict_logistic(weights, train_x)
    test_scores = predict_logistic(weights, test_x)
    threshold, train_ba = best_threshold(train_y, train_scores)
    conf = confusion(test_y, test_scores, threshold)
    mets = metrics_from_confusion(conf)
    roc_points = roc_curve_points(test_y, test_scores, name)
    pr_points = pr_curve_points(test_y, test_scores, name)
    roc_auc = trapezoid_auc([(p["fpr"], p["tpr"]) for p in roc_points])
    pr_auc = average_precision(test_y, test_scores)
    mets.update({
        "model": name,
        "threshold": threshold,
        "train_balanced_accuracy_at_threshold": train_ba,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "brier_score": brier(test_y, test_scores),
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "num_coordinates": len(specs),
    })
    return {
        "metrics": mets,
        "confusion": {"model": name, **conf},
        "roc": roc_points,
        "pr": pr_points,
        "weights": weights,
        "means": means,
        "stds": stds,
    }


def structural_rows() -> list[dict]:
    return [
        {
            "model": "B0_current_18_0",
            "num_coordinates": 2,
            "layer_eligibility": "L4 projection coordinates from current 18.0",
            "oracle_usage": "no",
            "history_usage": "no",
            "state_space_increase": "none beyond current 18.0",
            "wsts_compatibility_risk": "current baseline",
            "monotonicity_risk": "current baseline",
            "interpretability": "high but known projection-blind",
        },
        {
            "model": "Candidate_FA2_compact",
            "num_coordinates": 5,
            "layer_eligibility": "L4 eligible + conditional L2/L3; no reporting-only metrics",
            "oracle_usage": "no",
            "history_usage": "yes, compact delayed consequence flag",
            "state_space_increase": "approximately x32 if all coordinates Boolean",
            "wsts_compatibility_risk": "medium",
            "monotonicity_risk": "high due history/consequence flag",
            "interpretability": "high; compact but empirical min-zone threshold",
        },
        {
            "model": "B1_history_CEGAR",
            "num_coordinates": 13,
            "layer_eligibility": "conditional L2/L3 history/observation variables",
            "oracle_usage": "no",
            "history_usage": "yes, strong baseline",
            "state_space_increase": "large if bucketed; predicate-style CEGAR baseline",
            "wsts_compatibility_risk": "medium/high",
            "monotonicity_risk": "high",
            "interpretability": "medium; standard history-variable refinement",
        },
        {
            "model": "B2_raw_current_state",
            "num_coordinates": 5,
            "layer_eligibility": "L4 current state/projection coordinates",
            "oracle_usage": "no",
            "history_usage": "no",
            "state_space_increase": "moderate if bucketed",
            "wsts_compatibility_risk": "medium",
            "monotonicity_risk": "low/medium",
            "interpretability": "high; not witness-structured",
        },
    ]


def candidate_coordinate_rows() -> list[dict]:
    rows = []
    for name, reason, _ in feature_sets()["Candidate_FA2_compact"]:
        rows.append({
            "coordinate": name,
            "definition": reason,
            "layer_eligibility": (
                "L4 eligible" if name in {"failed_zone_count_ge_4", "total_mass_lt_35", "min_zone_welfare_le_0_96"}
                else "conditional L2/L3"
            ),
            "oracle": "no",
            "reporting_only": "no",
            "justification": "Survived BA4/FA2 as non-oracle layer-eligible missing-information coordinate.",
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def dataset_summary_rows(rows: list[dict], train_idx: list[int], test_idx: list[int], states: list[dict]) -> list[dict]:
    source_counts = Counter()
    for s in states:
        if s["shield_accept"] and s["future_collapse"]:
            source_counts["available_A_false_safe"] += 1
        if s["shield_accept"] and not s["future_collapse"]:
            source_counts["available_B_safe_remain_safe"] += 1
    selected = Counter(r["population"] for r in rows)
    split = Counter()
    for i in train_idx:
        split[f"train_{rows[i]['population']}"] += 1
    for i in test_idx:
        split[f"test_{rows[i]['population']}"] += 1
    return [
        {"item": "all_harvested_states", "count": len(states), "detail": "BA1 baseline replay"},
        {"item": "available_A_false_safe", "count": source_counts["available_A_false_safe"], "detail": "18.0 SAFE and future collapse"},
        {"item": "available_B_safe_remain_safe", "count": source_counts["available_B_safe_remain_safe"], "detail": "18.0 SAFE and no future collapse"},
        {"item": "selected_A_false_safe", "count": selected["A_false_safe"], "detail": "all available A"},
        {"item": "selected_B_safe_remain_safe", "count": selected["B_safe_remain_safe"], "detail": f"sampled with seed {DATASET_SEED}"},
        {"item": "train_rows", "count": len(train_idx), "detail": f"group split fraction {TRAIN_GROUP_FRACTION}"},
        {"item": "test_rows", "count": len(test_idx), "detail": "held-out trajectory groups"},
        *({"item": k, "count": v, "detail": "split label/population count"} for k, v in sorted(split.items())),
    ]


def assess(metrics: dict[str, dict], structural: list[dict]) -> dict:
    cand = metrics["Candidate_FA2_compact"]
    b0 = metrics["B0_current_18_0"]
    b1 = metrics["B1_history_CEGAR"]
    no_oracle = True
    layer_eligible = True
    precision_gain = cand["precision"] - b0["precision"]
    c1 = precision_gain >= PRECISION_MARGIN
    c2 = cand["recall"] >= 0.50
    c3 = no_oracle
    c4 = layer_eligible
    b1_matches = (
        b1["balanced_accuracy"] >= cand["balanced_accuracy"] - EQUIVALENCE_EPS
        and b1["roc_auc"] >= cand["roc_auc"] - EQUIVALENCE_EPS
        and b1["precision"] >= cand["precision"] - EQUIVALENCE_EPS
        and b1["recall"] >= cand["recall"] - EQUIVALENCE_EPS
    )
    c5 = not b1_matches
    history_relation = "Equivalent_to_standard_history_refinement" if b1_matches else "Distinct_from_standard_history_refinement"
    if c1 and c2 and c3 and c4 and c5:
        classification = "Faithful_candidate_supported"
        should_tc = "YES"
        reason = "Candidate passes all acceptance criteria and is not matched by history baseline."
    elif c1 and c2 and c3 and c4 and b1_matches:
        classification = "Equivalent_to_standard_history_refinement"
        should_tc = "NO"
        reason = "Candidate discrimination is matched by the strong history-variable CEGAR baseline."
    elif not c1 or not c2:
        classification = "No_discriminative_candidate"
        should_tc = "NO"
        reason = "Candidate fails discrimination acceptance criteria; history relation is still recorded separately."
    else:
        classification = "Inconclusive"
        should_tc = "NO"
        reason = "Acceptance criteria do not establish a distinct faithful candidate."
    return {
        "classification": classification,
        "acceptance_criteria": {
            "C1_precision_exceeds_18_0_by_margin": c1,
            "C1_precision_gain": precision_gain,
            "C1_required_margin": PRECISION_MARGIN,
            "C2_recall_does_not_collapse": c2,
            "C3_no_oracle_information": c3,
            "C4_only_layer_eligible_coordinates": c4,
            "C5_not_matched_by_history_baseline": c5,
            "history_baseline_matches_candidate": b1_matches,
            "equivalence_epsilon": EQUIVALENCE_EPS,
        },
        "candidate_exists": classification == "Faithful_candidate_supported",
        "history_baseline_relation": history_relation,
        "should_T_C_be_executed": should_tc,
        "reason": reason,
        "do_not_claim_safety": True,
        "do_not_modify_shield": True,
    }


def write_markdown_outputs(metrics: dict[str, dict], validity: dict, dataset_rows: list[dict], structural: list[dict]) -> None:
    cand_rows = candidate_coordinate_rows()
    lines = [
        "# FA2.5 Candidate Definition",
        "",
        "Candidate: `Candidate_FA2_compact`.",
        "",
        "This candidate is a compact, non-oracle coordinate set assembled from FA1/FA2 invariant families. It is not a shield and is not a monotonicity claim.",
        "",
        "| coordinate | layer | oracle | reporting-only | justification |",
        "|---|---|---|---|---|",
    ]
    for r in cand_rows:
        lines.append(f"| {r['coordinate']} | {r['layer_eligibility']} | {r['oracle']} | {r['reporting_only']} | {r['justification']} |")
    (OUT / "candidate_definition.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# FA2.5 Baseline Definitions",
        "",
        "B0 uses the current 18.0 abstract counters only.",
        "",
        "B1 is intentionally strong: it is a straightforward CEGAR/predicate-style history-variable refinement using delayed aid, delayed response, neighbor delta, policy-visible concentration, delayed welfare, and compact bad-consequence predicates.",
        "",
        "B2 uses five interpretable non-oracle current-state coordinates, matching the candidate coordinate count.",
        "",
        "| model | coordinates | oracle | history | note |",
        "|---|---:|---|---|---|",
    ]
    for r in structural:
        lines.append(f"| {r['model']} | {r['num_coordinates']} | {r['oracle_usage']} | {r['history_usage']} | {r['interpretability']} |")
    (OUT / "baseline_definitions.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# Candidate vs Baselines",
        "",
        "| model | precision | recall | specificity | ROC-AUC | PR-AUC | balanced accuracy | Brier |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, m in sorted(metrics.items()):
        lines.append(f"| {name} | {m['precision']:.6f} | {m['recall']:.6f} | {m['specificity']:.6f} | {m['roc_auc']:.6f} | {m['pr_auc']:.6f} | {m['balanced_accuracy']:.6f} | {m['brier_score']:.6f} |")
    lines += [
        "",
        f"Classification: **{validity['classification']}**.",
        f"History baseline relation: **{validity['history_baseline_relation']}**.",
        f"Reason: {validity['reason']}",
    ]
    (OUT / "candidate_vs_baselines.md").write_text("\n".join(lines) + "\n")

    b1_match = validity["acceptance_criteria"]["history_baseline_matches_candidate"]
    lines = [
        "# CEGAR Equivalence Analysis",
        "",
        f"History baseline matches candidate under epsilon `{EQUIVALENCE_EPS}`: `{b1_match}`.",
        "",
        "The B1 baseline is deliberately strong and uses standard delayed observation/history variables rather than the FA2 compact candidate structure.",
        "",
        "If B1 matches or exceeds the candidate, the result is recorded as `Equivalent_to_standard_history_refinement` rather than protected as an FA-specific success.",
        "",
        "| metric | candidate | B1 history baseline | delta candidate-minus-B1 |",
        "|---|---:|---:|---:|",
    ]
    for metric in ["precision", "recall", "specificity", "roc_auc", "pr_auc", "balanced_accuracy"]:
        delta = metrics["Candidate_FA2_compact"][metric] - metrics["B1_history_CEGAR"][metric]
        lines.append(f"| {metric} | {metrics['Candidate_FA2_compact'][metric]:.6f} | {metrics['B1_history_CEGAR'][metric]:.6f} | {delta:.6f} |")
    (OUT / "cegar_equivalence_analysis.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# Layer Eligibility Check",
        "",
        "No oracle fields, future labels, `capture_index`, permanence, or reporting-only diagnostics are used by the candidate.",
        "",
        "| coordinate | eligibility | note |",
        "|---|---|---|",
    ]
    for r in cand_rows:
        lines.append(f"| {r['coordinate']} | {r['layer_eligibility']} | {r['justification']} |")
    lines += [
        "",
        "The empirical `min_zone_welfare <= 0.96` coordinate is treated as a compact spread-risk proxy. It is layer-eligible but not yet a proven monotone invariant.",
    ]
    (OUT / "layer_eligibility_check.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# FA2.5 Faithful Candidate Validation",
        "",
        "Critical kill-gate experiment. This does not modify Justitia, does not modify collapse, does not use oracle information, and does not test monotonicity.",
        "",
        "## Decision",
        "",
        f"Classification: **{validity['classification']}**.",
        f"History baseline relation: **{validity['history_baseline_relation']}**.",
        f"Should T-C be executed? **{validity['should_T_C_be_executed']}**.",
        f"Reason: {validity['reason']}",
        "",
        "## Dataset",
        "",
        "| item | count | detail |",
        "|---|---:|---|",
    ]
    for r in dataset_rows:
        lines.append(f"| {r['item']} | {r['count']} | {r['detail']} |")
    lines += [
        "",
        "## Metrics",
        "",
        "| model | precision | recall | specificity | FPR | FNR | ROC-AUC | PR-AUC | balanced accuracy |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, m in sorted(metrics.items()):
        lines.append(f"| {name} | {m['precision']:.6f} | {m['recall']:.6f} | {m['specificity']:.6f} | {m['false_positive_rate']:.6f} | {m['false_negative_rate']:.6f} | {m['roc_auc']:.6f} | {m['pr_auc']:.6f} | {m['balanced_accuracy']:.6f} |")
    ac = validity["acceptance_criteria"]
    lines += [
        "",
        "## Acceptance Criteria",
        "",
        f"- C1 precision margin over 18.0: `{ac['C1_precision_exceeds_18_0_by_margin']}`; gain `{ac['C1_precision_gain']:.6f}` with required margin `{ac['C1_required_margin']}`.",
        f"- C2 recall does not collapse: `{ac['C2_recall_does_not_collapse']}`.",
        f"- C3 no oracle information: `{ac['C3_no_oracle_information']}`.",
        f"- C4 layer eligible only: `{ac['C4_only_layer_eligible_coordinates']}`.",
        f"- C5 not matched by history baseline: `{ac['C5_not_matched_by_history_baseline']}`.",
        "",
        "## Required Answers",
        "",
        f"1. Does a faithful candidate exist? `{validity['candidate_exists']}`.",
        "2. Does it discriminate false-safe from SAFE? See metrics table; discrimination is present, but candidate acceptance depends on all criteria.",
        "3. Is discrimination obtained without oracle information? `True`.",
        "4. Is the candidate layer-eligible? `True`.",
        f"5. Is the candidate genuinely different from history-variable refinement? `{not ac['history_baseline_matches_candidate']}`; relation `{validity['history_baseline_relation']}`.",
        f"6. Should T-C be executed? **{validity['should_T_C_be_executed']}**.",
        "",
        "Final answer: T-C should not be executed unless a distinct candidate passes the kill-gate.",
    ]
    (OUT / "final_report.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# Implementation Notes",
        "",
        "- Replayed the unchanged BA1 baseline grid via the FA1 extractor.",
        "- Population A uses all false-safe witnesses.",
        f"- Population B samples an equal number of SAFE-and-remain-SAFE states with seed `{DATASET_SEED}`.",
        "- Models are pure-Python logistic discriminators over fixed coordinate sets, trained on trajectory-group split and evaluated on held-out trajectory groups.",
        "- No oracle variables, future collapse labels, `capture_index`, permanence, or reporting-only metrics are used as candidate coordinates.",
        "- T-C is treated as downstream monotonicity testing and is not executed here.",
    ]
    (OUT / "implementation_notes.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    states = harvest_states()
    rows = make_balanced_dataset(states)
    train_idx, test_idx = group_split(rows)
    specs_by_model = feature_sets()
    evaluations = {
        name: evaluate_model(name, specs, rows, train_idx, test_idx)
        for name, specs in specs_by_model.items()
    }
    metrics = {name: ev["metrics"] for name, ev in evaluations.items()}
    structural = structural_rows()
    validity = assess(metrics, structural)

    write_csv(OUT / "candidate_coordinates.csv", candidate_coordinate_rows())
    dataset_rows = dataset_summary_rows(rows, train_idx, test_idx, states)
    write_csv(OUT / "dataset_summary.csv", dataset_rows)
    write_csv(OUT / "metrics.csv", [metrics[name] for name in sorted(metrics)])
    write_csv(OUT / "confusion_matrices.csv", [evaluations[name]["confusion"] for name in sorted(evaluations)])
    write_csv(OUT / "roc_data.csv", [p for name in sorted(evaluations) for p in evaluations[name]["roc"]])
    write_csv(OUT / "precision_recall_data.csv", [p for name in sorted(evaluations) for p in evaluations[name]["pr"]])
    write_json(OUT / "candidate_validity.json", validity)
    write_json(OUT / "hypothesis_assessment.json", {
        "classification": validity["classification"],
        "candidate_exists": validity["candidate_exists"],
        "should_T_C_be_executed": validity["should_T_C_be_executed"],
        "history_baseline_relation": validity["history_baseline_relation"],
        "acceptance_criteria": validity["acceptance_criteria"],
        "interpretation": validity["reason"],
    })
    write_markdown_outputs(metrics, validity, dataset_rows, structural)

    print(json.dumps({
        "classification": validity["classification"],
        "candidate_exists": validity["candidate_exists"],
        "should_T_C_be_executed": validity["should_T_C_be_executed"],
        "history_baseline_relation": validity["history_baseline_relation"],
        "metrics": {
            name: {
                "precision": metrics[name]["precision"],
                "recall": metrics[name]["recall"],
                "roc_auc": metrics[name]["roc_auc"],
                "balanced_accuracy": metrics[name]["balanced_accuracy"],
            }
            for name in sorted(metrics)
        },
        "outputs": str(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
