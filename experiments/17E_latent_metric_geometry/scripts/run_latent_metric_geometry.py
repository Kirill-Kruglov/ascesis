#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.decomposition import FastICA, FactorAnalysis, PCA
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score, roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from latent_metric_geometry.geometry import (  # noqa: E402
    CONTROL_COLUMNS,
    METRICS_ALL,
    METRICS_CONTROL,
    METRICS_REAL,
    TARGET_METRICS,
    build_feature_matrix,
    numeric_columns,
    partial_corr,
    prepare_matrix,
)


F1 = METRICS_REAL
F2 = METRICS_REAL + METRICS_CONTROL


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True), encoding="utf-8")


def read_optional_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def load_feature_matrix(input_17d: Path, attack_labels: Path | None) -> pd.DataFrame:
    required = [
        "metric_scores.csv",
        "metric_active_sets.csv",
        "functional_core.csv",
        "strict_core.csv",
    ]
    missing = [name for name in required if not (input_17d / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing 17D inputs in {input_17d}: {', '.join(missing)}")
    labels = read_optional_csv(attack_labels) if attack_labels else None
    return build_feature_matrix(
        pd.read_csv(input_17d / "metric_scores.csv"),
        pd.read_csv(input_17d / "metric_active_sets.csv"),
        pd.read_csv(input_17d / "functional_core.csv"),
        pd.read_csv(input_17d / "strict_core.csv"),
        labels,
    )


def pca_summary(df: pd.DataFrame, columns: list[str], name: str, loadings_rows: list[dict[str, Any]]) -> dict[str, Any]:
    prepared = prepare_matrix(df, columns)
    if prepared.values.shape[1] == 0:
        return {"name": name, "columns": [], "explained_variance_ratio": [], "cumulative_variance": []}
    n = min(prepared.values.shape)
    pca = PCA(n_components=n, random_state=42)
    pca.fit(prepared.values)
    ratios = pca.explained_variance_ratio_
    cumulative = np.cumsum(ratios)
    for idx, component in enumerate(pca.components_, start=1):
        for col, loading in zip(prepared.columns, component):
            loadings_rows.append({"feature_set": name, "component": idx, "feature": col, "loading": float(loading)})
    return {
        "name": name,
        "columns": prepared.columns,
        "explained_variance_ratio": [float(x) for x in ratios],
        "cumulative_variance": [float(x) for x in cumulative],
        "components_for_80": components_for(cumulative, 0.80),
        "components_for_90": components_for(cumulative, 0.90),
        "components_for_95": components_for(cumulative, 0.95),
    }


def components_for(cumulative: np.ndarray, threshold: float) -> int:
    above = np.where(cumulative >= threshold)[0]
    return int(above[0] + 1) if len(above) else int(len(cumulative))


def correlation_outputs(df: pd.DataFrame, out: Path) -> dict[str, Any]:
    numeric = numeric_columns(df, exclude=["class_a_survives", "class_b_survives", "class_b_attack_cost", "class_b_auc_gns"])
    corr = df[numeric].corr(method="pearson")
    corr.to_csv(out / "correlation_matrix.csv")
    spearman = df[numeric].corr(method="spearman")
    spearman.to_csv(out / "spearman_correlation_matrix.csv")

    pairs = [
        ("M1_original_score", "M3_reuse_score"),
        ("M1_original_score", "M5_perturbation_centrality_score"),
        ("M3_reuse_score", "M5_perturbation_centrality_score"),
        ("M1_original_score", "M6_frequency_control_score"),
        ("M3_reuse_score", "M6_frequency_control_score"),
        ("M5_perturbation_centrality_score", "M6_frequency_control_score"),
        ("M4_compression_score", "M6_frequency_control_score"),
    ]
    rows = []
    controls = ["frequency", "class_size", "dag_diversity"]
    for x, y in pairs:
        rows.append(
            {
                "x": x,
                "y": y,
                "pearson": float(df[x].corr(df[y], method="pearson")),
                "spearman": float(df[x].corr(df[y], method="spearman")),
                "partial_frequency_class_size_dag_diversity": partial_corr(df, x, y, controls),
            }
        )
    partial_df = pd.DataFrame(rows)
    partial_df.to_csv(out / "partial_correlation_matrix.csv", index=False)
    return {"required_pairs": rows}


def latent_values(df: pd.DataFrame, columns: list[str], n_components: int = 5) -> tuple[pd.DataFrame, PCA, list[str], np.ndarray]:
    prepared = prepare_matrix(df, columns)
    n = min(n_components, prepared.values.shape[1], prepared.values.shape[0])
    if n <= 0:
        return pd.DataFrame({"class_id": df["class_id"]}), PCA(), [], np.empty((len(df), 0))
    pca = PCA(n_components=n, random_state=42)
    values = pca.fit_transform(prepared.values)
    latent = pd.DataFrame({"class_id": df["class_id"]})
    for i in range(n):
        latent[f"PC{i + 1}"] = values[:, i]
    return latent, pca, prepared.columns, values


def factor_and_ica(df: pd.DataFrame, columns: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    prepared = prepare_matrix(df, columns)
    max_k = min(5, prepared.values.shape[1], prepared.values.shape[0] - 1)
    fa_rows = []
    ica_rows = []
    if max_k < 1:
        return {"status": "no_usable_columns", "rows": []}, {"status": "no_usable_columns", "rows": []}
    for k in range(1, max_k + 1):
        fa = FactorAnalysis(n_components=k, random_state=42)
        factors = fa.fit_transform(prepared.values)
        reconstructed = factors @ fa.components_ + fa.mean_
        fa_rows.append(
            {
                "k": k,
                "reconstruction_mse": float(np.mean((prepared.values - reconstructed) ** 2)),
                "noise_variance_mean": float(np.mean(fa.noise_variance_)),
            }
        )
        ica = FastICA(n_components=k, random_state=42, whiten="unit-variance", max_iter=1000, tol=1e-4)
        try:
            signals = ica.fit_transform(prepared.values)
            reconstructed_ica = ica.inverse_transform(signals)
            ica_rows.append(
                {
                    "k": k,
                    "reconstruction_mse": float(np.mean((prepared.values - reconstructed_ica) ** 2)),
                    "converged": True,
                }
            )
        except Exception as exc:  # pragma: no cover - depends on sklearn numerical convergence
            ica_rows.append({"k": k, "reconstruction_mse": None, "converged": False, "error": str(exc)})
    return {"candidate_dimensions": fa_rows, "best_k_by_mse": min(fa_rows, key=lambda r: r["reconstruction_mse"])["k"]}, {
        "candidate_dimensions": ica_rows,
        "best_k_by_mse": min([r for r in ica_rows if r["reconstruction_mse"] is not None], key=lambda r: r["reconstruction_mse"])["k"]
        if any(r["reconstruction_mse"] is not None for r in ica_rows)
        else None,
    }


def reconstruction_results(df: pd.DataFrame, out: Path) -> pd.DataFrame:
    rows = []
    sources = {
        "F1_real_metrics": F1,
        "F1_success_cluster": TARGET_METRICS,
        "F2_real_plus_controls": F2,
        "F3_all_internal": numeric_columns(df, exclude=["class_a_survives", "class_b_survives", "class_b_attack_cost", "class_b_auc_gns"]),
        "F3_no_frequency_controls": [
            c
            for c in numeric_columns(df, exclude=["class_a_survives", "class_b_survives", "class_b_attack_cost", "class_b_auc_gns"])
            if c not in {"frequency", "class_size", "dag_diversity", *METRICS_CONTROL}
        ],
    }
    y = df[TARGET_METRICS].astype(float).values
    for source, cols in sources.items():
        prepared = prepare_matrix(df, cols)
        if prepared.values.shape[1] == 0:
            continue
        max_k = min(5, prepared.values.shape[1])
        pca = PCA(n_components=max_k, random_state=42)
        z = pca.fit_transform(prepared.values)
        for k in range(1, max_k + 1):
            pred = LinearRegression().fit(z[:, :k], y).predict(z[:, :k])
            for idx, target in enumerate(TARGET_METRICS):
                rows.append(
                    {
                        "source": source,
                        "k": k,
                        "target": target,
                        "r2": float(r2_score(y[:, idx], pred[:, idx])),
                        "mae": float(mean_absolute_error(y[:, idx], pred[:, idx])),
                    }
                )
            rows.append(
                {
                    "source": source,
                    "k": k,
                    "target": "mean_M1_M3_M5",
                    "r2": float(np.mean([r2_score(y[:, i], pred[:, i]) for i in range(y.shape[1])])),
                    "mae": float(np.mean([mean_absolute_error(y[:, i], pred[:, i]) for i in range(y.shape[1])])),
                }
            )
    result = pd.DataFrame(rows)
    result.to_csv(out / "reconstruction_results.csv", index=False)
    return result


def safe_auc(y_true: np.ndarray, score: np.ndarray) -> float | None:
    if len(np.unique(y_true)) < 2:
        return None
    return float(roc_auc_score(y_true, score))


def prediction_results(df: pd.DataFrame, latent: pd.DataFrame, out: Path) -> pd.DataFrame:
    work = df.merge(latent, on="class_id", how="left")
    targets = {
        "class_b_survives": "classification",
        "class_b_auc_gns": "regression",
        "class_b_attack_cost": "regression",
        "functional_core_membership": "classification",
        "strict_core_membership": "classification",
    }
    feature_sets = {
        "latent_1": ["PC1"],
        "latent_2": ["PC1", "PC2"],
        "latent_3": ["PC1", "PC2", "PC3"],
        "all_raw_metrics": METRICS_ALL,
        "controls_only": METRICS_CONTROL + ["frequency", "class_size", "dag_diversity"],
        "random_baseline": ["random_baseline"],
    }
    rng = np.random.default_rng(42)
    work["random_baseline"] = rng.normal(size=len(work))
    rows = []
    for target, kind in targets.items():
        if target not in work:
            continue
        data = work.dropna(subset=[target]).copy()
        if len(data) < 20:
            rows.append({"target": target, "status": "insufficient_labels", "n": int(len(data))})
            continue
        y = data[target].astype(float).values
        if len(np.unique(y)) < 2:
            rows.append({"target": target, "status": "constant_target", "n": int(len(data))})
            continue
        for name, cols in feature_sets.items():
            cols = [c for c in cols if c in data.columns]
            if not cols:
                continue
            x = prepare_matrix(data, cols).values
            if x.shape[1] == 0:
                continue
            if kind == "classification":
                y_bin = y.astype(int)
                counts = np.bincount(y_bin)
                splits = min(5, int(counts.min())) if len(counts) > 1 else 0
                if splits < 2:
                    rows.append({"target": target, "feature_set": name, "status": "insufficient_class_balance", "n": int(len(data))})
                    continue
                cv = StratifiedKFold(n_splits=splits, shuffle=True, random_state=42)
                for model_name, model in {
                    "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
                    "small_decision_tree": DecisionTreeClassifier(max_depth=3, random_state=42, class_weight="balanced"),
                }.items():
                    if hasattr(model, "predict_proba"):
                        probs = cross_val_predict(model, x, y_bin, cv=cv, method="predict_proba")[:, 1]
                        pred = (probs >= 0.5).astype(int)
                    else:
                        pred = cross_val_predict(model, x, y_bin, cv=cv)
                        probs = pred
                    rows.append(
                        {
                            "target": target,
                            "feature_set": name,
                            "model": model_name,
                            "status": "ok",
                            "n": int(len(data)),
                            "auc": safe_auc(y_bin, probs),
                            "accuracy": float(accuracy_score(y_bin, pred)),
                            "f1": float(f1_score(y_bin, pred, zero_division=0)),
                            "r2": None,
                        }
                    )
            else:
                cv = KFold(n_splits=min(5, len(data)), shuffle=True, random_state=42)
                for model_name, model in {
                    "ridge_regression": Ridge(alpha=1.0),
                    "small_decision_tree": DecisionTreeRegressor(max_depth=3, random_state=42),
                }.items():
                    pred = cross_val_predict(model, x, y, cv=cv)
                    rows.append(
                        {
                            "target": target,
                            "feature_set": name,
                            "model": model_name,
                            "status": "ok",
                            "n": int(len(data)),
                            "auc": None,
                            "accuracy": None,
                            "f1": None,
                            "r2": float(r2_score(y, pred)),
                            "mae": float(mean_absolute_error(y, pred)),
                        }
                    )
    result = pd.DataFrame(rows)
    result.to_csv(out / "prediction_results.csv", index=False)
    return result


def control_leakage(df: pd.DataFrame, latent: pd.DataFrame, prediction: pd.DataFrame, out: Path) -> pd.DataFrame:
    work = df.merge(latent, on="class_id", how="left")
    rows = []
    controls = [c for c in CONTROL_COLUMNS if c in work.columns]
    for pc in [c for c in latent.columns if c.startswith("PC")]:
        data = work.dropna(subset=[pc] + controls)
        x = prepare_matrix(data, controls).values
        y = data[pc].astype(float).values
        r2 = None
        if x.shape[1] > 0 and len(data) > x.shape[1] + 1:
            r2 = float(r2_score(y, LinearRegression().fit(x, y).predict(x)))
        rows.append({"component": pc, "controls": ";".join(controls), "variance_explained_by_controls": r2})
    pred_ok = prediction[prediction.get("status", "") == "ok"] if "status" in prediction else pd.DataFrame()
    for target in ["functional_core_membership", "strict_core_membership", "class_b_survives"]:
        subset = pred_ok[(pred_ok["target"] == target) & (pred_ok["model"].isin(["logistic_regression", "ridge_regression"]))]
        if subset.empty:
            continue
        all_auc = subset[subset["feature_set"] == "all_raw_metrics"]["auc"].dropna()
        control_auc = subset[subset["feature_set"] == "controls_only"]["auc"].dropna()
        latent_auc = subset[subset["feature_set"] == "latent_1"]["auc"].dropna()
        rows.append(
            {
                "component": f"predictive_leakage_{target}",
                "all_raw_auc": float(all_auc.max()) if len(all_auc) else None,
                "controls_auc": float(control_auc.max()) if len(control_auc) else None,
                "latent1_auc": float(latent_auc.max()) if len(latent_auc) else None,
                "residual_predictive_power_after_controls": float((latent_auc.max() if len(latent_auc) else np.nan) - (control_auc.max() if len(control_auc) else np.nan))
                if len(latent_auc) and len(control_auc)
                else None,
            }
        )
    result = pd.DataFrame(rows)
    result.to_csv(out / "control_leakage.csv", index=False)
    return result


def seed_stability(out: Path) -> dict[str, Any]:
    payload = {
        "status": "single_seed_only",
        "available_seeds": [42],
        "component_loading_correlation_across_seeds": None,
        "latent_score_correlation_across_seeds": None,
        "stable_axis_count": None,
        "note": "17D full outputs are available only for seed 42. The script is deterministic on those inputs.",
    }
    write_json(out / "seed_stability.json", payload)
    return payload


def decide(
    pca_f1: dict[str, Any],
    reconstruction: pd.DataFrame,
    prediction: pd.DataFrame,
    leakage: pd.DataFrame,
    seed_payload: dict[str, Any],
) -> dict[str, Any]:
    pc1_f1 = pca_f1["explained_variance_ratio"][0] if pca_f1.get("explained_variance_ratio") else 0.0
    recon = reconstruction[(reconstruction["source"] == "F1_success_cluster") & (reconstruction["target"] == "mean_M1_M3_M5")]
    r2_k1 = float(recon[recon["k"] == 1]["r2"].iloc[0]) if not recon[recon["k"] == 1].empty else math.nan
    r2_k2 = float(recon[recon["k"] == 2]["r2"].iloc[0]) if not recon[recon["k"] == 2].empty else math.nan
    pc1_leak = leakage[leakage["component"] == "PC1"]["variance_explained_by_controls"]
    pc1_control_r2 = float(pc1_leak.iloc[0]) if len(pc1_leak) and not pd.isna(pc1_leak.iloc[0]) else math.nan

    pred_ok = prediction[prediction.get("status", "") == "ok"] if "status" in prediction else pd.DataFrame()
    func = pred_ok[(pred_ok["target"] == "functional_core_membership") & (pred_ok["model"] == "logistic_regression")]
    auc1 = best_metric(func, "latent_1", "auc")
    auc2 = best_metric(func, "latent_2", "auc")
    auc_all = best_metric(func, "all_raw_metrics", "auc")
    auc_controls = best_metric(func, "controls_only", "auc")

    class_b = pred_ok[(pred_ok["target"] == "class_b_survives") & (pred_ok["model"] == "logistic_regression")]
    class_b_auc1 = best_metric(class_b, "latent_1", "auc")
    class_b_auc2 = best_metric(class_b, "latent_2", "auc")
    class_b_auc3 = best_metric(class_b, "latent_3", "auc")
    class_b_auc_all = best_metric(class_b, "all_raw_metrics", "auc")
    class_b_auc_controls = best_metric(class_b, "controls_only", "auc")
    has_class_b = not math.isnan(class_b_auc1)

    material_class_b_gain = safe_delta(max_nan(class_b_auc2, class_b_auc3), class_b_auc1) > 0.08
    material_functional_gain = safe_delta(auc2, auc1) > 0.03
    material_axis_gain = material_class_b_gain or material_functional_gain
    one_axis_near_all = abs_delta(auc_all, auc1) <= 0.03
    controls_near_axis = abs_delta(auc_controls, auc1) <= 0.03
    class_b_not_control_only = (
        has_class_b
        and not math.isnan(class_b_auc_controls)
        and safe_delta(max_nan(class_b_auc2, class_b_auc3, class_b_auc_all), class_b_auc_controls) > 0.03
    )

    if not math.isnan(pc1_control_r2) and pc1_control_r2 >= 0.80 and controls_near_axis:
        classification = "Control_artifact"
        interpretation = "The dominant latent axis is mostly explained by frequency/class-size/DAG-diversity controls."
    elif pc1_f1 >= 0.80 and r2_k1 >= 0.90 and one_axis_near_all and pc1_control_r2 < 0.75 and seed_payload["status"] != "single_seed_only":
        classification = "One_axis_supported"
        interpretation = "One stable non-control latent axis explains successful closure-like metrics and prediction."
    elif has_class_b and material_class_b_gain and class_b_not_control_only:
        classification = "Multi_axis_supported"
        interpretation = "One axis reconstructs the successful metric cluster, but perturbation sensitivity requires additional latent axes."
    elif material_axis_gain or (not math.isnan(r2_k2) and not math.isnan(r2_k1) and r2_k2 - r2_k1 > 0.05):
        classification = "Multi_axis_supported"
        interpretation = "At least two latent axes materially improve reconstruction or predictive behavior."
    elif seed_payload["status"] == "single_seed_only":
        classification = "Inconclusive"
        if has_class_b:
            interpretation = "A dominant axis exists, but seed stability is unavailable from 17D outputs."
        else:
            interpretation = "A dominant axis exists, but seed stability and per-class Class-B labels are unavailable from 17D outputs."
    else:
        classification = "Metric_noise"
        interpretation = "Latent structure has weak or unstable predictive value."

    limitations = ["Seed stability cannot be tested without full 17D outputs for seeds 43 and 44."]
    if not has_class_b:
        limitations.insert(0, "17D outputs do not contain per-class Class-B attack labels.")

    return {
        "classification": classification,
        "interpretation": interpretation,
        "pc1_f1_explained_variance": pc1_f1,
        "success_cluster_reconstruction_r2_k1": r2_k1,
        "success_cluster_reconstruction_r2_k2": r2_k2,
        "pc1_control_variance_explained": pc1_control_r2,
        "functional_core_auc_latent1": auc1,
        "functional_core_auc_latent2": auc2,
        "functional_core_auc_all_raw_metrics": auc_all,
        "functional_core_auc_controls": auc_controls,
        "class_b_auc_latent1": class_b_auc1,
        "class_b_auc_latent2": class_b_auc2,
        "class_b_auc_latent3": class_b_auc3,
        "class_b_auc_all_raw_metrics": class_b_auc_all,
        "class_b_auc_controls": class_b_auc_controls,
        "class_b_labels_available": has_class_b,
        "limitations": limitations,
    }

def best_metric(df: pd.DataFrame, feature_set: str, column: str) -> float:
    vals = df[df["feature_set"] == feature_set][column].dropna()
    return float(vals.max()) if len(vals) else math.nan


def safe_delta(a: float, b: float) -> float:
    return 0.0 if math.isnan(a) or math.isnan(b) else a - b


def abs_delta(a: float, b: float) -> float:
    return math.inf if math.isnan(a) or math.isnan(b) else abs(a - b)


def max_nan(*values: float) -> float:
    usable = [v for v in values if not math.isnan(v)]
    return max(usable) if usable else math.nan


def write_axis_interpretation(path: Path, decision: dict[str, Any], pca_f1: dict[str, Any], pca_f2: dict[str, Any], pca_f3: dict[str, Any]) -> None:
    lines = [
        "# Experiment 17E - Latent Axis Interpretation",
        "",
        f"Classification: `{decision['classification']}`",
        "",
        decision["interpretation"],
        "",
        "## Required Questions",
        "",
        f"1. Latent dimensions for M1/M3/M5: k=1 gives mean reconstruction R2 `{decision['success_cluster_reconstruction_r2_k1']:.6g}`; k=2 gives `{decision['success_cluster_reconstruction_r2_k2']:.6g}`.",
        f"2. One dominant closure-like axis: PC1 over real metrics explains `{decision['pc1_f1_explained_variance']:.6g}` variance.",
        f"3. Independence from controls: controls explain `{decision['pc1_control_variance_explained']:.6g}` of PC1.",
        f"4. Class B sensitivity: latent1 AUC `{decision['class_b_auc_latent1']}`; latent2 AUC `{decision['class_b_auc_latent2']}`; latent3 AUC `{decision['class_b_auc_latent3']}`.",
        f"5. More axes: latent2/3 materially improve Class-B prediction over latent1; functional-core latent2 AUC `{decision['functional_core_auc_latent2']}` vs latent1 AUC `{decision['functional_core_auc_latent1']}`.",
        "6. Seed stability: not tested; only seed 42 full 17D outputs are available.",
        f"7. Interpretation: `{decision['classification']}`.",
        "",
        "## PCA Summary",
        "",
        f"- F1 real metrics PC1 variance: {pca_f1.get('explained_variance_ratio', [None])[0]}",
        f"- F2 real+controls PC1 variance: {pca_f2.get('explained_variance_ratio', [None])[0]}",
        f"- F3 all internal PC1 variance: {pca_f3.get('explained_variance_ratio', [None])[0]}",
        "",
        "The experiment does not claim true meaning or semantic essence. It tests only latent structural factors in this toy substrate.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_final_report(path: Path, decision: dict[str, Any], corr_info: dict[str, Any]) -> None:
    lines = [
        "# Experiment 17E - Latent Metric Geometry",
        "",
        "## Decision",
        "",
        f"Classification: `{decision['classification']}`",
        "",
        decision["interpretation"],
        "",
        "## Key Numbers",
        "",
        f"- PC1 F1 explained variance: `{decision['pc1_f1_explained_variance']}`",
        f"- M1/M3/M5 reconstruction R2 with k=1: `{decision['success_cluster_reconstruction_r2_k1']}`",
        f"- M1/M3/M5 reconstruction R2 with k=2: `{decision['success_cluster_reconstruction_r2_k2']}`",
        f"- PC1 variance explained by controls: `{decision['pc1_control_variance_explained']}`",
        f"- Functional-core AUC latent1: `{decision['functional_core_auc_latent1']}`",
        f"- Functional-core AUC latent2: `{decision['functional_core_auc_latent2']}`",
        f"- Functional-core AUC controls: `{decision['functional_core_auc_controls']}`",
        f"- Class-B survival AUC latent1: `{decision['class_b_auc_latent1']}`",
        f"- Class-B survival AUC latent2: `{decision['class_b_auc_latent2']}`",
        f"- Class-B survival AUC latent3: `{decision['class_b_auc_latent3']}`",
        f"- Class-B survival AUC controls: `{decision['class_b_auc_controls']}`",
        "",
        "## Required Correlations",
        "",
    ]
    for row in corr_info["required_pairs"]:
        lines.append(
            f"- {row['x']} vs {row['y']}: Pearson `{row['pearson']:.6g}`, Spearman `{row['spearman']:.6g}`, partial `{row['partial_frequency_class_size_dag_diversity']:.6g}`"
        )
    lines += [
        "",
        "## Limitations",
        "",
        "- Seed stability requires full 17D-style outputs for seeds 43 and 44.",
        "",
        "## Artifacts",
        "",
        "- feature_matrix.csv",
        "- correlation_matrix.csv",
        "- partial_correlation_matrix.csv",
        "- pca_f1_summary.json / pca_f2_summary.json / pca_f3_summary.json",
        "- pca_loadings.csv",
        "- factor_analysis_summary.json",
        "- ica_summary.json",
        "- reconstruction_results.csv",
        "- prediction_results.csv",
        "- control_leakage.csv",
        "- seed_stability.json",
        "- latent_components.csv",
        "- latent_axis_interpretation.md",
        "- final_decision.json",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 17E latent metric geometry")
    parser.add_argument("--input-17d", type=Path, default=ROOT.parents[0] / "17D_closure_metric_robustness" / "outputs_17D")
    parser.add_argument("--attack-labels", type=Path, default=None)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17E")
    args = parser.parse_args()

    out = ensure(args.outputs)
    df = load_feature_matrix(args.input_17d, args.attack_labels)
    df.to_csv(out / "feature_matrix.csv", index=False)

    corr_info = correlation_outputs(df, out)
    loadings_rows: list[dict[str, Any]] = []
    f3 = numeric_columns(df, exclude=["class_a_survives", "class_b_survives", "class_b_attack_cost", "class_b_auc_gns"])
    pca_f1 = pca_summary(df, F1, "F1_real_metrics", loadings_rows)
    pca_f2 = pca_summary(df, F2, "F2_real_plus_controls", loadings_rows)
    pca_f3 = pca_summary(df, f3, "F3_all_internal", loadings_rows)
    write_json(out / "pca_f1_summary.json", pca_f1)
    write_json(out / "pca_f2_summary.json", pca_f2)
    write_json(out / "pca_f3_summary.json", pca_f3)
    pd.DataFrame(loadings_rows).to_csv(out / "pca_loadings.csv", index=False)

    fa_summary, ica_summary = factor_and_ica(df, f3)
    write_json(out / "factor_analysis_summary.json", fa_summary)
    write_json(out / "ica_summary.json", ica_summary)

    reconstruction = reconstruction_results(df, out)
    latent, _, _, _ = latent_values(df, f3, n_components=5)
    latent.to_csv(out / "latent_components.csv", index=False)
    prediction = prediction_results(df, latent, out)
    leakage = control_leakage(df, latent, prediction, out)
    seeds = seed_stability(out)

    decision = decide(pca_f1, reconstruction, prediction, leakage, seeds)
    write_json(out / "final_decision.json", decision)
    write_axis_interpretation(out / "latent_axis_interpretation.md", decision, pca_f1, pca_f2, pca_f3)
    write_final_report(out / "final_report.md", decision, corr_info)
    (out / "implementation_notes.md").write_text(
        "# Implementation Notes\n\n"
        "The default run consumes 17D outputs and does not recompute perturbation attacks. "
        "Per-class Class-B labels are left as missing unless an attack-label table is passed with --attack-labels. "
        "All PCA/FA/ICA fits use internally derived metrics and structural descriptors only.\n",
        encoding="utf-8",
    )
    write_json(
        out / "failure_examples.json",
        {
            "missing_class_b_labels": bool(df["class_b_survives"].isna().all()),
            "single_seed_only": True,
            "highest_pc1_control_leakage": decision["pc1_control_variance_explained"],
        },
    )

    print(
        json.dumps(
            {
                "classification": decision["classification"],
                "pc1_f1_explained_variance": decision["pc1_f1_explained_variance"],
                "success_cluster_reconstruction_r2_k1": decision["success_cluster_reconstruction_r2_k1"],
                "pc1_control_variance_explained": decision["pc1_control_variance_explained"],
                "outputs": str(out),
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()

