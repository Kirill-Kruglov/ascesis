#!/usr/bin/env python3
"""JB0.E1 standard CEGAR boundary assessment for Justitia.

This is a boundary assessment, not FA, not T-C, and not shield synthesis. The
runner replays the unchanged Justitia baseline through the existing FA2.5 data
path, then builds a standard Boolean predicate abstraction over layer-eligible
current/history/control variables. Selected predicates define abstract cells;
training groups estimate per-cell risk; held-out trajectory groups test whether
the resulting conservative boundary is useful or plateaus/explodes/vacuates.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
ASCESIS = Path("/home/master/llm_projects/ascesis")
FA25_SCRIPT = ASCESIS / "experiments/FA2_5_E1_candidate_validation/scripts/run_candidate_validation.py"
FA25_OUT = ASCESIS / "experiments/FA2_5_E1_candidate_validation/outputs"

MAX_PREDICATES = 20
MAX_ABSTRACT_CELLS = 100_000
MAX_HISTORY_WINDOW = 8
MAX_ITERATIONS = 20
PLATEAU_EPS = 0.005
CELL_SMOOTHING = 1.0

USEFUL_THRESHOLDS = {
    "recall": 0.90,
    "precision": 0.80,
    "false_safe_rate": 0.10,
    "false_positive_rate": 0.25,
    "predicates": 20,
}


def load_fa25():
    spec = importlib.util.spec_from_file_location("fa25_validation", FA25_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def f(row: dict, key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value == "" or value is None:
        return default
    return float(value)


def rate(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def safe_mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def augment_rolling(states: list[dict]) -> None:
    grouped = defaultdict(list)
    for s in states:
        grouped[s["traj_key"]].append(s)
    for seq in grouped.values():
        seq.sort(key=lambda r: r["step"])
        for i, row in enumerate(seq):
            for k in [1, 2, 4, 8]:
                if i >= k:
                    prev = seq[i - k]
                    row[f"rolling_welfare_loss_{k}"] = max(0.0, prev["mean_welfare"] - row["mean_welfare"])
                    row[f"rolling_min_welfare_loss_{k}"] = max(0.0, prev["min_zone_welfare"] - row["min_zone_welfare"])
                    row[f"rolling_mass_loss_{k}"] = max(0.0, prev["total_mass"] - row["total_mass"])
                    row[f"rolling_failed_zone_gain_{k}"] = max(0.0, row["failed_zone_count"] - prev["failed_zone_count"])
                else:
                    row[f"rolling_welfare_loss_{k}"] = 0.0
                    row[f"rolling_min_welfare_loss_{k}"] = 0.0
                    row[f"rolling_mass_loss_{k}"] = 0.0
                    row[f"rolling_failed_zone_gain_{k}"] = 0.0


def harvest_dataset():
    fa25 = load_fa25()
    states = fa25.harvest_states()
    augment_rolling(states)
    rows = fa25.make_balanced_dataset(states)
    train_idx, test_idx = fa25.group_split(rows)
    return fa25, states, rows, train_idx, test_idx


def predicate_catalog(rows: list[dict]) -> list[dict]:
    predicates: list[dict] = []

    def add(pid: str, family: str, name: str, definition: str, fn, layer: str, history_depth: int = 0, kind: str = "threshold"):
        predicates.append({
            "predicate_id": pid,
            "family": family,
            "name": name,
            "definition": definition,
            "layer_eligibility": layer,
            "history_depth": history_depth,
            "kind": kind,
            "oracle": "no",
            "reporting_only": "no",
            "fn": fn,
            "selected_iteration": "",
            "selected_rank": "",
            "marginal_train_false_safe_reduction": "",
        })

    add("P_mean_collapse", "current_collapse", "mean_welfare < 0.32", "mean_welfare < 0.32", lambda r: f(r, "mean_welfare") < 0.32, "L4 eligible")
    add("P_failed_ge_4", "current_collapse", "failed_zone_count >= 4", "failed_zone_count >= 4", lambda r: f(r, "failed_zone_count") >= 4, "L4 eligible")
    add("P_mass_lt_35", "current_collapse", "total_mass < 35", "total_mass < 35", lambda r: f(r, "total_mass") < 35, "L4 eligible")

    for t in [0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95]:
        add(f"P_mean_le_{str(t).replace('.', '_')}", "risk_band", f"mean_welfare <= {t}", f"mean_welfare <= {t}", lambda r, t=t: f(r, "mean_welfare") <= t, "L4 eligible")
    for t in [0.20, 0.40, 0.60, 0.80, 0.90, 0.96]:
        add(f"P_min_le_{str(t).replace('.', '_')}", "risk_band", f"min_zone_welfare <= {t}", f"min_zone_welfare <= {t}", lambda r, t=t: f(r, "min_zone_welfare") <= t, "L4 eligible")
    for n in [1, 2, 3]:
        add(f"P_failed_ge_{n}", "risk_band", f"failed_zone_count >= {n}", f"failed_zone_count >= {n}", lambda r, n=n: f(r, "failed_zone_count") >= n, "L4 eligible")
    for t in [50, 100, 200, 500, 1000]:
        add(f"P_mass_le_{t}", "risk_band", f"total_mass <= {t}", f"total_mass <= {t}", lambda r, t=t: f(r, "total_mass") <= t, "L4 eligible")

    for t in [0.50, 0.62, 0.70, 0.80, 0.90]:
        add(f"P_obs_conc_gt_{str(t).replace('.', '_')}", "history_policy_visible_concentration", f"Obs.resource_concentration max > {t}", f"obs_resource_concentration_max > {t}", lambda r, t=t: f(r, "obs_resource_concentration_max") > t, "conditional L2/L3", history_depth=2)
    for t in [0.035, 0.50, 0.75, 1.00, 1.25]:
        add(f"P_last_aid_gt_{str(t).replace('.', '_')}", "history_last_aid", f"Obs.last_aid max > {t}", f"obs_last_aid_max > {t}", lambda r, t=t: f(r, "obs_last_aid_max") > t, "conditional L2/L3", history_depth=2)
    for t in [0.0, -0.01, -0.025, -0.05]:
        suffix = str(t).replace("-", "neg_").replace(".", "_")
        add(f"P_response_lt_{suffix}", "history_response", f"Obs.response_to_aid min < {t}", f"obs_response_to_aid_min < {t}", lambda r, t=t: f(r, "obs_response_to_aid_min") < t, "conditional L2/L3", history_depth=2)
    for t in [0.0, -0.01, -0.03, -0.05, -0.10]:
        suffix = str(t).replace("-", "neg_").replace(".", "_")
        add(f"P_neighbor_lt_{suffix}", "history_neighbor", f"Obs.neighbor_delta min < {t}", f"obs_neighbor_delta_min < {t}", lambda r, t=t: f(r, "obs_neighbor_delta_min") < t, "conditional L2/L3", history_depth=2)
    for n in [1, 2, 3]:
        add(f"P_bad_conseq_ge_{n}", "history_consequence", f"bad_consequence_count >= {n}", f"bad_consequence_count >= {n}", lambda r, n=n: f(r, "bad_consequence_count") >= n, "conditional L2/L3", history_depth=2)
    for t in [0.20, 0.40, 0.60, 0.80, 0.96]:
        add(f"P_delayed_min_le_{str(t).replace('.', '_')}", "delayed_observation", f"delayed_obs_min_welfare <= {t}", f"delayed_obs_min_welfare <= {t}", lambda r, t=t: f(r, "delayed_obs_min_welfare") <= t, "conditional L2/L3", history_depth=2)
    for n in [1, 2, 3, 4]:
        add(f"P_delayed_failed_ge_{n}", "delayed_observation", f"delayed_obs_failed_zone_count >= {n}", f"delayed_obs_failed_zone_count >= {n}", lambda r, n=n: f(r, "delayed_obs_failed_zone_count") >= n, "conditional L2/L3", history_depth=2)

    add("P_containment_active", "control_policy", "containment_active_count > 0", "containment_active_count > 0", lambda r: f(r, "containment_active_count") > 0, "conditional L1/L2")
    add("P_timer_active", "control_policy", "containment_timer_max > 0", "containment_timer_max > 0", lambda r: f(r, "containment_timer_max") > 0, "conditional L1/L2")
    for t in [0.20, 0.30, 0.40]:
        add(f"P_alloc_gini_gt_{str(t).replace('.', '_')}", "control_policy", f"allocation_gini > {t}", f"allocation_gini > {t}", lambda r, t=t: f(r, "allocation_gini") > t, "conditional L2")
    for t in [0.18, 0.24, 0.32]:
        add(f"P_alloc_max_gt_{str(t).replace('.', '_')}", "control_policy", f"allocation_max > {t}", f"allocation_max > {t}", lambda r, t=t: f(r, "allocation_max") > t, "conditional L2")
    for policy in sorted({r["policy"] for r in rows}):
        pid = policy.replace("_", "")
        add(f"P_policy_{pid}", "control_policy", f"policy == {policy}", f"policy == {policy}", lambda r, policy=policy: r["policy"] == policy, "conditional L2/L5 config")

    for k in [1, 2, 4, 8]:
        for t in [0.01, 0.03, 0.05, 0.10]:
            add(f"P_roll_welfare_loss_{k}_{str(t).replace('.', '_')}", "rolling_trajectory_summary", f"rolling_welfare_loss_{k} > {t}", f"rolling_welfare_loss_{k} > {t}", lambda r, k=k, t=t: f(r, f"rolling_welfare_loss_{k}") > t, "conditional L1/L4 temporal", history_depth=k)
            add(f"P_roll_min_loss_{k}_{str(t).replace('.', '_')}", "rolling_trajectory_summary", f"rolling_min_welfare_loss_{k} > {t}", f"rolling_min_welfare_loss_{k} > {t}", lambda r, k=k, t=t: f(r, f"rolling_min_welfare_loss_{k}") > t, "conditional L1/L4 temporal", history_depth=k)
        for t in [10, 50, 100, 250, 500]:
            add(f"P_roll_mass_loss_{k}_{t}", "rolling_trajectory_summary", f"rolling_mass_loss_{k} > {t}", f"rolling_mass_loss_{k} > {t}", lambda r, k=k, t=t: f(r, f"rolling_mass_loss_{k}") > t, "conditional L1/L4 temporal", history_depth=k)
        for n in [1, 2]:
            add(f"P_roll_failed_gain_{k}_{n}", "rolling_trajectory_summary", f"rolling_failed_zone_gain_{k} >= {n}", f"rolling_failed_zone_gain_{k} >= {n}", lambda r, k=k, n=n: f(r, f"rolling_failed_zone_gain_{k}") >= n, "conditional L1/L4 temporal", history_depth=k)

    return predicates


def cell_scores(rows: list[dict], train_idx: list[int], predicates: list[dict]) -> tuple[list[float], dict]:
    def key(row):
        return tuple(bool(p["fn"](row)) for p in predicates)

    cell_counts = defaultdict(lambda: [0, 0])
    for i in train_idx:
        k = key(rows[i])
        cell_counts[k][0] += int(rows[i]["label"])
        cell_counts[k][1] += 1
    global_pos = sum(int(rows[i]["label"]) for i in train_idx)
    global_rate = rate(global_pos, len(train_idx))
    risks = {}
    for k, (pos, n) in cell_counts.items():
        risks[k] = (pos + CELL_SMOOTHING) / (n + 2 * CELL_SMOOTHING)
    scores = [risks.get(key(row), global_rate) for row in rows]
    return scores, {
        "observed_cells": len(cell_counts),
        "abstract_cell_upper_bound": 2 ** len(predicates),
        "train_cell_risks": {str(k): v for k, v in risks.items()},
    }


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
        else:
            fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def metrics_from_confusion(c: dict[str, int]) -> dict[str, float]:
    tp, fp, tn, fn = c["tp"], c["fp"], c["tn"], c["fn"]
    recall = rate(tp, tp + fn)
    specificity = rate(tn, tn + fp)
    fpr = rate(fp, fp + tn)
    fnr = rate(fn, fn + tp)
    pred_pos = tp + fp
    total = tp + fp + tn + fn
    return {
        "precision": rate(tp, tp + fp),
        "recall": recall,
        "specificity": specificity,
        "false_positive_rate": fpr,
        "false_negative_rate": fnr,
        "false_safe_rate": fnr,
        "false_unsafe_rate": fpr,
        "balanced_accuracy": 0.5 * (recall + specificity),
        "accuracy": rate(tp + tn, total),
        "predicted_unsafe_fraction": rate(pred_pos, total),
        "conservative_vacuity_score": rate(pred_pos, total),
    }


def select_threshold(y_true: list[int], scores: list[float]) -> tuple[float, dict]:
    uniq = sorted(set(scores))
    thresholds = [uniq[0] - 1e-12] + [(a + b) / 2 for a, b in zip(uniq, uniq[1:])] + [uniq[-1] + 1e-12]
    candidates = []
    for t in thresholds:
        m = metrics_from_confusion(confusion(y_true, scores, t))
        m["threshold"] = t
        candidates.append(m)
    feasible = [
        m for m in candidates
        if m["recall"] >= USEFUL_THRESHOLDS["recall"]
        and m["false_positive_rate"] <= USEFUL_THRESHOLDS["false_positive_rate"]
    ]
    if feasible:
        best = max(feasible, key=lambda m: (m["precision"], m["balanced_accuracy"], -m["false_positive_rate"]))
    else:
        best = max(candidates, key=lambda m: (m["balanced_accuracy"], m["recall"], m["precision"], -m["false_positive_rate"]))
    return best["threshold"], best


def roc_auc(y: list[int], scores: list[float]) -> float:
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg_rank = (i + 1 + j + 1) / 2
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    n_pos = sum(y)
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.0
    rank_sum_pos = sum(ranks[i] for i, val in enumerate(y) if val == 1)
    return (rank_sum_pos - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def average_precision(y: list[int], scores: list[float]) -> float:
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    total_pos = sum(y)
    if total_pos == 0:
        return 0.0
    tp = fp = 0
    prev_recall = 0.0
    ap = 0.0
    for i in order:
        if y[i] == 1:
            tp += 1
        else:
            fp += 1
        recall = tp / total_pos
        precision = tp / (tp + fp)
        ap += (recall - prev_recall) * precision
        prev_recall = recall
    return ap


def evaluate_boundary(rows: list[dict], train_idx: list[int], test_idx: list[int], predicates: list[dict]) -> dict:
    scores, cell_info = cell_scores(rows, train_idx, predicates)
    y = [int(r["label"]) for r in rows]
    train_y = [y[i] for i in train_idx]
    train_scores = [scores[i] for i in train_idx]
    test_y = [y[i] for i in test_idx]
    test_scores = [scores[i] for i in test_idx]
    if not predicates:
        # Empty predicate abstraction corresponds to the current 18.0 SAFE slice:
        # no added CEGAR predicate marks any accepted state as unsafe.
        threshold = max(scores) + 1.0
        train_metrics = metrics_from_confusion(confusion(train_y, train_scores, threshold))
    else:
        threshold, train_metrics = select_threshold(train_y, train_scores)
    conf = confusion(test_y, test_scores, threshold)
    metrics = metrics_from_confusion(conf)
    metrics.update({
        "threshold": threshold,
        "roc_auc": roc_auc(test_y, test_scores),
        "pr_auc": average_precision(test_y, test_scores),
        "train_balanced_accuracy": train_metrics["balanced_accuracy"],
        "train_recall": train_metrics["recall"],
        "train_precision": train_metrics["precision"],
        "num_predicates": len(predicates),
        "abstract_cell_upper_bound": cell_info["abstract_cell_upper_bound"],
        "observed_abstract_cells": cell_info["observed_cells"],
        "history_depth": max([p["history_depth"] for p in predicates] or [0]),
        "layer_eligible": all(p["oracle"] == "no" and p["reporting_only"] == "no" for p in predicates),
        "vacuous": is_vacuous(metrics),
    })
    return {"metrics": metrics, "confusion": conf, "scores": scores, "threshold": threshold, "cell_info": cell_info}


def is_useful(metrics: dict) -> bool:
    return (
        metrics["recall"] >= USEFUL_THRESHOLDS["recall"]
        and metrics["precision"] >= USEFUL_THRESHOLDS["precision"]
        and metrics["false_safe_rate"] <= USEFUL_THRESHOLDS["false_safe_rate"]
        and metrics["false_positive_rate"] <= USEFUL_THRESHOLDS["false_positive_rate"]
        and metrics["num_predicates"] <= USEFUL_THRESHOLDS["predicates"]
        and metrics["layer_eligible"]
    )


def is_vacuous(metrics: dict) -> bool:
    return (
        metrics["predicted_unsafe_fraction"] >= 0.80
        or metrics["false_positive_rate"] >= 0.50
        or (metrics["recall"] >= 0.95 and metrics["precision"] < 0.65)
    )


def selection_utility(metrics: dict) -> float:
    return (
        metrics["balanced_accuracy"]
        + 0.35 * metrics["recall"]
        + 0.15 * metrics["precision"]
        - 0.25 * metrics["false_positive_rate"]
        - 0.10 * metrics["conservative_vacuity_score"]
    )


def current_false_negatives(rows: list[dict], indices: list[int], scores: list[float], threshold: float) -> set[int]:
    missed = set()
    for i in indices:
        if int(rows[i]["label"]) == 1 and scores[i] < threshold:
            missed.add(i)
    return missed


def run_cegar(rows: list[dict], train_idx: list[int], test_idx: list[int], catalog: list[dict]):
    selected: list[dict] = []
    available = list(catalog)
    trace = []
    witness_rows = []
    growth_rows = []
    confusion_rows = []
    consecutive_ba_plateau = 0
    consecutive_fs_plateau = 0
    stop_reason = "max_iterations"
    prev_metrics = None

    for iteration in range(MAX_ITERATIONS + 1):
        evaluation = evaluate_boundary(rows, train_idx, test_idx, selected)
        metrics = evaluation["metrics"]
        conf = evaluation["confusion"]
        useful = is_useful(metrics)
        selected_ids = [p["predicate_id"] for p in selected]
        trace_row = {
            "iteration": iteration,
            "selected_predicate": selected[-1]["predicate_id"] if selected else "none",
            "selected_predicates": ";".join(selected_ids) if selected else "none",
            **metrics,
            "useful_boundary": useful,
        }
        trace.append(trace_row)
        confusion_rows.append({"iteration": iteration, **conf})
        growth_rows.append({
            "iteration": iteration,
            "num_predicates": len(selected),
            "abstract_cell_upper_bound": metrics["abstract_cell_upper_bound"],
            "observed_abstract_cells": metrics["observed_abstract_cells"],
            "history_depth": metrics["history_depth"],
        })
        heldout_missed = current_false_negatives(rows, test_idx, evaluation["scores"], evaluation["threshold"])
        train_missed = current_false_negatives(rows, train_idx, evaluation["scores"], evaluation["threshold"])
        witness_rows.append({
            "iteration": iteration,
            "remaining_false_safe_train": len(train_missed),
            "remaining_false_safe_heldout": len(heldout_missed),
            "heldout_positive_count": sum(int(rows[i]["label"]) for i in test_idx),
            "heldout_false_safe_rate": metrics["false_safe_rate"],
        })

        if useful:
            stop_reason = "useful_success"
            break
        if iteration > 0 and metrics["vacuous"]:
            stop_reason = "vacuity"
            break
        if prev_metrics is not None:
            ba_improvement = metrics["balanced_accuracy"] - prev_metrics["balanced_accuracy"]
            fs_improvement = prev_metrics["false_safe_rate"] - metrics["false_safe_rate"]
            consecutive_ba_plateau = consecutive_ba_plateau + 1 if ba_improvement < PLATEAU_EPS else 0
            consecutive_fs_plateau = consecutive_fs_plateau + 1 if fs_improvement < PLATEAU_EPS else 0
            if consecutive_ba_plateau >= 2:
                stop_reason = "balanced_accuracy_plateau"
                break
            if consecutive_fs_plateau >= 2:
                stop_reason = "false_safe_rate_plateau"
                break
        prev_metrics = metrics
        if iteration >= MAX_ITERATIONS:
            stop_reason = "max_iterations"
            break
        if len(selected) >= MAX_PREDICATES:
            stop_reason = "predicate_budget_exceeded"
            break
        if 2 ** (len(selected) + 1) > MAX_ABSTRACT_CELLS:
            stop_reason = "abstract_cell_budget_exceeded"
            break

        best = None
        current_train_missed = train_missed
        for pred in available:
            candidate_selected = selected + [pred]
            ev = evaluate_boundary(rows, train_idx, test_idx, candidate_selected)
            train_ev = evaluate_boundary(rows, train_idx, train_idx, candidate_selected)
            train_metrics = train_ev["metrics"]
            candidate_scores = train_ev["scores"]
            candidate_missed = current_false_negatives(rows, train_idx, candidate_scores, train_ev["threshold"])
            reduction = len(current_train_missed) - len(candidate_missed)
            if reduction <= max(1, int(0.005 * max(1, len(current_train_missed)))):
                continue
            utility = selection_utility(train_metrics) + 0.0005 * reduction
            item = (utility, reduction, train_metrics["balanced_accuracy"], -train_metrics["false_positive_rate"], pred["predicate_id"], pred, ev)
            if best is None or item[:5] > best[:5]:
                best = item
        if best is None:
            stop_reason = "no_meaningful_predicate"
            break
        _, reduction, _, _, _, pred, _ = best
        pred["selected_iteration"] = iteration + 1
        pred["selected_rank"] = len(selected) + 1
        pred["marginal_train_false_safe_reduction"] = reduction
        selected.append(pred)
        available = [p for p in available if p["predicate_id"] != pred["predicate_id"]]

    best_iteration = max(trace, key=lambda r: (is_useful(r), r["balanced_accuracy"], -r["false_safe_rate"], r["precision"]))
    return {
        "trace": trace,
        "witness_reduction": witness_rows,
        "growth": growth_rows,
        "confusion": confusion_rows,
        "selected": selected,
        "catalog": catalog,
        "stop_reason": stop_reason,
        "best_iteration": best_iteration,
    }


def read_fa25_baselines() -> list[dict]:
    rows = []
    with (FA25_OUT / "metrics.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row["model"] in {"B0_current_18_0", "B1_history_CEGAR", "B2_raw_current_state"}:
                row["source"] = "FA2.5 held-out balanced dataset"
                rows.append(row)
    return rows


def decision(result: dict) -> dict:
    trace = result["trace"]
    best = result["best_iteration"]
    final = trace[-1]
    useful = any(is_useful(r) for r in trace)
    vacuity = any(r["vacuous"] for r in trace[1:])
    exploded = result["stop_reason"] in {"predicate_budget_exceeded", "abstract_cell_budget_exceeded"} or final["abstract_cell_upper_bound"] > MAX_ABSTRACT_CELLS
    plateau = result["stop_reason"] in {"balanced_accuracy_plateau", "false_safe_rate_plateau", "no_meaningful_predicate", "max_iterations"}
    if useful:
        cls = "Useful_CEGAR_boundary"
        door = "YES"
        reason = "Standard predicate/history CEGAR reached useful boundary thresholds without oracle information."
    elif exploded:
        cls = "CEGAR_state_explosion"
        door = "NO"
        reason = "Refinement hit predicate/cell budget before reaching useful boundary thresholds."
    elif vacuity and best["false_safe_rate"] <= USEFUL_THRESHOLDS["false_safe_rate"]:
        cls = "Conservative_but_vacuous"
        door = "NO"
        reason = "False-safe reduction required classifying too many held-out SAFE states as unsafe/doomed."
    elif plateau:
        cls = "CEGAR_plateau"
        door = "NO"
        reason = "Refinement plateaued below useful boundary thresholds."
    else:
        cls = "Inconclusive"
        door = "NO"
        reason = "Implementation did not establish a useful standard CEGAR boundary."
    return {
        "classification": cls,
        "stop_reason": result["stop_reason"],
        "best_iteration": best["iteration"],
        "best_precision": best["precision"],
        "best_recall": best["recall"],
        "best_false_safe_rate": best["false_safe_rate"],
        "best_false_positive_rate": best["false_positive_rate"],
        "best_balanced_accuracy": best["balanced_accuracy"],
        "best_predicate_count": best["num_predicates"],
        "best_abstract_cell_upper_bound": best["abstract_cell_upper_bound"],
        "useful_boundary_found": useful,
        "vacuity_observed": vacuity,
        "state_explosion_observed": exploded,
        "plateau_observed": plateau,
        "should_Justitia_remain_Door_1_substrate_candidate": door,
        "should_T_C_be_considered_after_this_result": "YES" if useful else "NO",
        "reason": reason,
        "no_safety_claim": True,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    fields = []
    for row in rows:
        out_row = {k: v for k, v in row.items() if not callable(v)}
        for key in out_row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: v for k, v in row.items() if k in fields and not callable(v)})


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def write_reports(result: dict, dec: dict, baseline_rows: list[dict]) -> None:
    selected = result["selected"]
    best = result["best_iteration"]
    final = result["trace"][-1]
    lines = [
        "# Remaining Witnesses",
        "",
        f"Stop reason: `{result['stop_reason']}`.",
        f"Best iteration: `{best['iteration']}`.",
        "",
        "| iteration | remaining false-safe heldout | false-safe rate | selected predicate |",
        "|---:|---:|---:|---|",
    ]
    for row in result["witness_reduction"]:
        trace_row = result["trace"][row["iteration"]]
        lines.append(f"| {row['iteration']} | {row['remaining_false_safe_heldout']} | {row['heldout_false_safe_rate']:.6f} | {trace_row['selected_predicate']} |")
    (OUT / "remaining_witnesses.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# Best Boundary Definition",
        "",
        f"Best iteration: `{best['iteration']}`.",
        f"Classification: `{dec['classification']}`.",
        "",
        "Selected predicates:",
        "",
    ]
    if selected:
        for p in selected[: int(best["num_predicates"])]:
            lines.append(f"- `{p['predicate_id']}`: {p['definition']} ({p['layer_eligibility']}, history depth {p['history_depth']})")
    else:
        lines.append("- none")
    lines += [
        "",
        "This boundary is an empirical predicate/cell-risk assessment only. It is not a deployed shield and does not claim safety.",
    ]
    (OUT / "best_boundary_definition.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# JB0.E1 Implementation Notes",
        "",
        "- Justitia source semantics and collapse definition were not modified.",
        "- No oracle time-to-collapse or future labels were used as features.",
        "- Dataset construction reuses FA2.5: all false-safe witnesses vs sampled SAFE-and-remain-SAFE states, split by trajectory group.",
        f"- Budgets: max predicates `{MAX_PREDICATES}`, max abstract cells `{MAX_ABSTRACT_CELLS}`, max history window `{MAX_HISTORY_WINDOW}`, max iterations `{MAX_ITERATIONS}`.",
        "- Predicate abstraction uses Boolean cells with smoothed empirical risk learned on training groups.",
        "- Threshold selection first tries recall >= 0.90 with FPR <= 0.25; if unavailable, it falls back to best balanced accuracy, which can expose vacuity.",
        "- T-C was not run.",
    ]
    (OUT / "implementation_notes.md").write_text("\n".join(lines) + "\n")

    lines = [
        "# JB0.E1 Standard CEGAR Boundary Assessment",
        "",
        "This is not FA, not T-C, and not shield synthesis. It assesses whether standard history/predicate CEGAR gives a practically useful Justitia boundary.",
        "",
        "## Decision",
        "",
        f"Classification: **{dec['classification']}**.",
        f"Stop reason: `{dec['stop_reason']}`.",
        f"Should Justitia remain a Door-1 substrate candidate? **{dec['should_Justitia_remain_Door_1_substrate_candidate']}**.",
        f"Should T-C be considered after this result? **{dec['should_T_C_be_considered_after_this_result']}**.",
        f"Reason: {dec['reason']}",
        "",
        "## Best JB0 Boundary",
        "",
        f"- Iteration: `{best['iteration']}`.",
        f"- Precision: `{best['precision']:.6f}`.",
        f"- Recall: `{best['recall']:.6f}`.",
        f"- False-safe rate: `{best['false_safe_rate']:.6f}`.",
        f"- False-positive rate: `{best['false_positive_rate']:.6f}`.",
        f"- Balanced accuracy: `{best['balanced_accuracy']:.6f}`.",
        f"- Predicates: `{best['num_predicates']}`.",
        f"- Abstract cell upper bound: `{best['abstract_cell_upper_bound']}`.",
        "",
        "## FA2.5 Baseline Comparison",
        "",
        "| baseline | precision | recall | false-safe/FNR | FPR | ROC-AUC | balanced accuracy |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in baseline_rows:
        lines.append(f"| {row['model']} | {float(row['precision']):.6f} | {float(row['recall']):.6f} | {float(row['false_negative_rate']):.6f} | {float(row['false_positive_rate']):.6f} | {float(row['roc_auc']):.6f} | {float(row['balanced_accuracy']):.6f} |")
    lines += [
        "",
        "## Selected Predicates",
        "",
        "| rank | predicate | family | layer | history depth |",
        "|---:|---|---|---|---:|",
    ]
    for p in selected:
        lines.append(f"| {p['selected_rank']} | {p['definition']} | {p['family']} | {p['layer_eligibility']} | {p['history_depth']} |")
    lines += [
        "",
        "## Required Answers",
        "",
        f"1. Does standard CEGAR produce a useful boundary? `{dec['useful_boundary_found']}`.",
        f"2. Improvement over 18.0: best false-safe `{best['false_safe_rate']:.6f}` vs B0 FNR `{float(next(r for r in baseline_rows if r['model']=='B0_current_18_0')['false_negative_rate']):.6f}`; precision/balanced accuracy must also be considered.",
        f"3. Improvement over FA2.5 history baseline: best false-safe `{best['false_safe_rate']:.6f}` vs B1 FNR `{float(next(r for r in baseline_rows if r['model']=='B1_history_CEGAR')['false_negative_rate']):.6f}`.",
        f"4. Predicates selected: `{'; '.join(p['predicate_id'] for p in selected) if selected else 'none'}`.",
        f"5. Did refinement plateau? `{dec['plateau_observed']}`.",
        f"6. Did state/cell count explode? `{dec['state_explosion_observed']}`.",
        f"7. Did the conservative boundary become vacuous? `{dec['vacuity_observed']}`.",
        "8. Are selected predicates layer-eligible? `True`.",
        f"9. Should Justitia remain a Door-1 substrate candidate? **{dec['should_Justitia_remain_Door_1_substrate_candidate']}**.",
        f"10. Should T-C be considered after this result? **{dec['should_T_C_be_considered_after_this_result']}**.",
        "",
        "No safety claim is made.",
    ]
    (OUT / "final_report.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _, states, rows, train_idx, test_idx = harvest_dataset()
    catalog = predicate_catalog(rows)
    result = run_cegar(rows, train_idx, test_idx, catalog)
    dec = decision(result)
    baseline_rows = read_fa25_baselines()

    write_csv(OUT / "baseline_metrics.csv", baseline_rows)
    write_csv(OUT / "refinement_trace.csv", result["trace"])
    write_csv(OUT / "predicate_catalog.csv", result["catalog"])
    write_csv(OUT / "witness_reduction_by_iteration.csv", result["witness_reduction"])
    write_csv(OUT / "heldout_metrics.csv", result["trace"])
    write_csv(OUT / "confusion_matrices.csv", result["confusion"])
    write_csv(OUT / "abstract_state_growth.csv", result["growth"])
    write_json(OUT / "plateau_analysis.json", {
        "plateau_observed": dec["plateau_observed"],
        "stop_reason": result["stop_reason"],
        "plateau_eps": PLATEAU_EPS,
        "final_iteration": result["trace"][-1]["iteration"],
    })
    write_json(OUT / "vacuity_analysis.json", {
        "vacuity_observed": dec["vacuity_observed"],
        "best_predicted_unsafe_fraction": result["best_iteration"]["predicted_unsafe_fraction"],
        "final_predicted_unsafe_fraction": result["trace"][-1]["predicted_unsafe_fraction"],
        "best_precision": result["best_iteration"]["precision"],
        "final_precision": result["trace"][-1]["precision"],
    })
    write_json(OUT / "cegar_boundary_decision.json", dec)
    write_reports(result, dec, baseline_rows)

    print(json.dumps({
        "classification": dec["classification"],
        "stop_reason": dec["stop_reason"],
        "best_iteration": dec["best_iteration"],
        "best_precision": dec["best_precision"],
        "best_recall": dec["best_recall"],
        "best_false_safe_rate": dec["best_false_safe_rate"],
        "best_false_positive_rate": dec["best_false_positive_rate"],
        "best_predicate_count": dec["best_predicate_count"],
        "should_Justitia_remain_Door_1_substrate_candidate": dec["should_Justitia_remain_Door_1_substrate_candidate"],
        "should_T_C_be_considered_after_this_result": dec["should_T_C_be_considered_after_this_result"],
        "outputs": str(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
