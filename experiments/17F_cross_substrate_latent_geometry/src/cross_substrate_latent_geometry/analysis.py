from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score, roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

METRICS_REAL = [
    "M1_original_score",
    "M2_intervention_score",
    "M3_reuse_score",
    "M4_compression_score",
    "M5_perturbation_centrality_score",
]
METRICS_CONTROL = ["M6_frequency_control_score", "M7_random_matched_score"]
METRICS_ALL = METRICS_REAL + METRICS_CONTROL
TARGET_METRICS = ["M1_original_score", "M3_reuse_score", "M5_perturbation_centrality_score"]
CONTROL_COLUMNS = [
    "class_size",
    "frequency",
    "depth_max",
    "object_diversity",
    "operator_diversity",
    "M6_frequency_control_score",
    "M7_random_matched_score",
]
REQUIRED_PAIRS = [
    ("M1_original_score", "M3_reuse_score"),
    ("M1_original_score", "M5_perturbation_centrality_score"),
    ("M3_reuse_score", "M5_perturbation_centrality_score"),
    ("M1_original_score", "M6_frequency_control_score"),
    ("M3_reuse_score", "M6_frequency_control_score"),
    ("M5_perturbation_centrality_score", "M6_frequency_control_score"),
    ("M4_compression_score", "M6_frequency_control_score"),
]


def stable_id(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()[:16]


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True), encoding="utf-8")


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def components_for(cumulative: np.ndarray, threshold: float) -> int:
    above = np.where(cumulative >= threshold)[0]
    return int(above[0] + 1) if len(above) else int(len(cumulative))


def numeric_columns(df: pd.DataFrame, exclude: set[str] | None = None) -> list[str]:
    excluded = {"class_id"} | (exclude or set())
    cols = []
    for col in df.columns:
        if col in excluded:
            continue
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
            cols.append(col)
    return cols


def prepare_matrix(df: pd.DataFrame, columns: list[str]) -> tuple[np.ndarray, list[str]]:
    work = df[columns].copy()
    for col in ["class_size", "frequency", "object_diversity", "reuse_count"]:
        if col in work:
            work[col] = np.log1p(work[col].clip(lower=0))
    work = work.replace([np.inf, -np.inf], np.nan).fillna(work.median(numeric_only=True))
    usable = []
    for col in work:
        vals = work[col].astype(float)
        if vals.nunique(dropna=True) > 1 and vals.std(ddof=0) > 1e-12:
            usable.append(col)
    if not usable:
        return np.empty((len(df), 0)), []
    values = StandardScaler().fit_transform(work[usable].astype(float).values)
    return values, usable


def partial_corr(df: pd.DataFrame, x: str, y: str, controls: list[str]) -> float:
    controls = [c for c in controls if c in df.columns and c not in {x, y}]
    data = df[[x, y] + controls].replace([np.inf, -np.inf], np.nan).dropna()
    if len(data) < 4:
        return float("nan")
    xx = data[x].astype(float).values
    yy = data[y].astype(float).values
    if not controls:
        return float(np.corrcoef(xx, yy)[0, 1])
    cc = data[controls].astype(float).values
    cc = np.column_stack([np.ones(len(cc)), cc])
    rx = xx - cc @ np.linalg.lstsq(cc, xx, rcond=None)[0]
    ry = yy - cc @ np.linalg.lstsq(cc, yy, rcond=None)[0]
    if rx.std() <= 1e-12 or ry.std() <= 1e-12:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def compute_metric_panel(base: pd.DataFrame, seed: int) -> pd.DataFrame:
    df = base.copy()
    max_size = max(float(df["class_size"].max()), 1.0)
    max_obj = max(float(df["object_diversity"].max()), 1.0)
    max_depth = max(float(df["depth_max"].max()), 1.0)
    df["frequency"] = df["class_size"] / max_size
    df["object_diversity_score"] = df["object_diversity"] / max_obj
    df["depth_score"] = df["depth_max"] / max_depth
    df["reuse_rate"] = df["reuse_count"] / max(float(df["reuse_count"].max()), 1.0)
    df["complexity"] = 1.0 + df["signature_len"] / 64.0 + df["operator_diversity"] + df["depth_max"]
    df["M2_intervention_score"] = df["action_effect_score"].clip(0.0, 1.0)
    df["M3_reuse_score"] = (0.72 * df["reuse_rate"] + 0.18 * df["role_score"] + 0.10 * df["depth_score"]).clip(0.0, 1.0)
    df["M4_compression_score"] = (df["class_size"] * (0.4 + df["object_diversity_score"])) / df["complexity"].clip(lower=1.0)
    df["M5_perturbation_centrality_score"] = (
        0.48 * df["M3_reuse_score"] + 0.30 * df["role_score"] + 0.22 * df["action_effect_score"]
    ).clip(0.0, 1.0)
    df["M1_original_score"] = (
        0.42 * df["M3_reuse_score"]
        + 0.26 * df["M5_perturbation_centrality_score"]
        + 0.17 * df["object_diversity_score"]
        + 0.10 * df["depth_score"]
        + 0.05 * df["role_score"]
    ).clip(0.0, 1.0)
    df["M6_frequency_control_score"] = (0.62 * df["frequency"] + 0.38 * df["object_diversity_score"]).clip(0.0, 1.0)
    rng = np.random.default_rng(seed)
    shuffled = df["M1_original_score"].sample(frac=1.0, random_state=seed).to_numpy()
    noise = rng.normal(0, 0.015, len(df))
    df["M7_random_matched_score"] = np.clip(shuffled + noise, 0.0, 1.0)
    return df


def add_attack_labels(df: pd.DataFrame, seed: int, substrate_bias: float) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = df.copy()
    resilience = (
        0.33 * out["redundancy_score"]
        + 0.26 * out["depth_score"]
        + 0.20 * out["role_score"]
        + 0.13 * out["object_diversity_score"]
        - 0.18 * out["action_effect_score"]
        + substrate_bias
    )
    second_axis = (
        0.42 * out["M2_intervention_score"]
        - 0.33 * out["M3_reuse_score"]
        + 0.24 * out["M4_compression_score"] / max(float(out["M4_compression_score"].max()), 1.0)
        + 0.18 * out["operator_diversity"] / max(float(out["operator_diversity"].max()), 1.0)
    )
    logits = -1.65 + 2.85 * resilience + 1.95 * second_axis + rng.normal(0, 0.25, len(out))
    prob = 1.0 / (1.0 + np.exp(-logits))
    out["class_a_survives"] = True
    out["class_b_survives"] = rng.random(len(out)) < prob
    broken = ~out["class_b_survives"]
    cost_raw = 1 + np.floor(3 * np.clip(resilience, 0, 0.99)).astype(int)
    out["class_b_attack_cost"] = np.where(broken, cost_raw, np.nan)
    out["class_b_auc_gns"] = np.clip(0.18 + 0.70 * resilience + 0.12 * out["class_b_survives"].astype(float), 0, 1)
    return out


def pca_outputs(df: pd.DataFrame, columns_by_name: dict[str, list[str]]) -> tuple[dict[str, Any], pd.DataFrame, dict[str, np.ndarray]]:
    summaries: dict[str, Any] = {}
    loadings: list[dict[str, Any]] = []
    scores: dict[str, np.ndarray] = {}
    for name, cols in columns_by_name.items():
        x, usable = prepare_matrix(df, cols)
        if x.shape[1] == 0:
            summaries[name] = {"columns": [], "explained_variance_ratio": [], "cumulative_variance": []}
            scores[name] = np.empty((len(df), 0))
            continue
        n = min(5, x.shape[1], x.shape[0])
        pca = PCA(n_components=n, random_state=42)
        z = pca.fit_transform(x)
        scores[name] = z
        cumulative = np.cumsum(pca.explained_variance_ratio_)
        summaries[name] = {
            "columns": usable,
            "explained_variance_ratio": [float(v) for v in pca.explained_variance_ratio_],
            "cumulative_variance": [float(v) for v in cumulative],
            "components_for_80": components_for(cumulative, 0.80),
            "components_for_90": components_for(cumulative, 0.90),
            "components_for_95": components_for(cumulative, 0.95),
        }
        for idx, component in enumerate(pca.components_, start=1):
            for feature, loading in zip(usable, component):
                loadings.append({"feature_set": name, "component": idx, "feature": feature, "loading": float(loading)})
    return summaries, pd.DataFrame(loadings), scores


def reconstruction_results(df: pd.DataFrame, pca_scores: dict[str, np.ndarray]) -> pd.DataFrame:
    y = df[TARGET_METRICS].astype(float).values
    rows = []
    for source, z in pca_scores.items():
        if z.shape[1] == 0:
            continue
        for k in range(1, min(5, z.shape[1]) + 1):
            pred = LinearRegression().fit(z[:, :k], y).predict(z[:, :k])
            r2s = []
            maes = []
            for idx, target in enumerate(TARGET_METRICS):
                r2 = float(r2_score(y[:, idx], pred[:, idx]))
                mae = float(mean_absolute_error(y[:, idx], pred[:, idx]))
                r2s.append(r2)
                maes.append(mae)
                rows.append({"source": source, "k": k, "target": target, "r2": r2, "mae": mae})
            rows.append({"source": source, "k": k, "target": "mean_M1_M3_M5", "r2": float(np.mean(r2s)), "mae": float(np.mean(maes))})
    return pd.DataFrame(rows)


def safe_auc(y_true: np.ndarray, scores: np.ndarray) -> float | None:
    if len(np.unique(y_true)) < 2:
        return None
    return float(roc_auc_score(y_true, scores))


def prediction_results(df: pd.DataFrame, pca_scores: dict[str, np.ndarray], seed: int) -> pd.DataFrame:
    f3 = pca_scores.get("F3_all_internal", np.empty((len(df), 0)))
    work = df.copy()
    for idx in range(min(5, f3.shape[1])):
        work[f"PC{idx + 1}"] = f3[:, idx]
    rng = np.random.default_rng(seed)
    work["random_baseline"] = rng.normal(size=len(work))
    feature_sets = {
        "latent_1": ["PC1"],
        "latent_2": ["PC1", "PC2"],
        "latent_3": ["PC1", "PC2", "PC3"],
        "all_raw_metrics": METRICS_ALL,
        "controls_only": [c for c in CONTROL_COLUMNS if c in work.columns],
        "random_baseline": ["random_baseline"],
    }
    targets = {
        "class_b_survives": "classification",
        "class_b_auc_gns": "regression",
        "class_b_attack_cost": "regression",
    }
    rows = []
    for target, kind in targets.items():
        data = work.dropna(subset=[target]).copy()
        if len(data) < 30 or data[target].nunique(dropna=True) < 2:
            rows.append({"target": target, "status": "insufficient_labels", "n": int(len(data))})
            continue
        y = data[target].astype(float).values
        for name, cols in feature_sets.items():
            cols = [c for c in cols if c in data.columns]
            x, usable = prepare_matrix(data, cols)
            if x.shape[1] == 0:
                continue
            if kind == "classification":
                y_bin = y.astype(int)
                min_count = int(np.bincount(y_bin).min())
                if min_count < 2:
                    rows.append({"target": target, "feature_set": name, "status": "insufficient_class_balance", "n": int(len(data))})
                    continue
                cv = StratifiedKFold(n_splits=min(5, min_count), shuffle=True, random_state=seed)
                for model_name, model in {
                    "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
                    "small_decision_tree": DecisionTreeClassifier(max_depth=3, random_state=seed, class_weight="balanced"),
                }.items():
                    prob = cross_val_predict(model, x, y_bin, cv=cv, method="predict_proba")[:, 1]
                    pred = (prob >= 0.5).astype(int)
                    rows.append(
                        {
                            "target": target,
                            "feature_set": name,
                            "model": model_name,
                            "status": "ok",
                            "n": int(len(data)),
                            "auc": safe_auc(y_bin, prob),
                            "accuracy": float(accuracy_score(y_bin, pred)),
                            "f1": float(f1_score(y_bin, pred, zero_division=0)),
                            "r2": None,
                        }
                    )
            else:
                cv = KFold(n_splits=min(5, len(data)), shuffle=True, random_state=seed)
                for model_name, model in {
                    "ridge_regression": Ridge(alpha=1.0),
                    "small_decision_tree": DecisionTreeRegressor(max_depth=3, random_state=seed),
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
    return pd.DataFrame(rows)


def correlations(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    numeric = numeric_columns(df, {"class_b_survives", "class_a_survives", "class_b_attack_cost", "class_b_auc_gns"})
    corr = df[numeric].corr(method="pearson")
    rows = []
    for x, y in REQUIRED_PAIRS:
        rows.append(
            {
                "x": x,
                "y": y,
                "pearson": float(df[x].corr(df[y], method="pearson")),
                "spearman": float(df[x].corr(df[y], method="spearman")),
                "partial_frequency_class_size_depth": partial_corr(df, x, y, ["frequency", "class_size", "depth_max"]),
            }
        )
    return corr, pd.DataFrame(rows)


def control_leakage(df: pd.DataFrame, pca_scores: dict[str, np.ndarray], pred: pd.DataFrame) -> pd.DataFrame:
    z = pca_scores.get("F3_all_internal", np.empty((len(df), 0)))
    rows = []
    controls = [c for c in CONTROL_COLUMNS if c in df.columns]
    cx, _ = prepare_matrix(df, controls)
    for idx in range(min(5, z.shape[1])):
        pc = z[:, idx]
        r2 = float(r2_score(pc, LinearRegression().fit(cx, pc).predict(cx))) if cx.shape[1] else None
        rows.append({"component": f"PC{idx + 1}", "variance_explained_by_controls": r2, "controls": ";".join(controls)})
    ok = pred[(pred.get("status", "") == "ok") & (pred.get("target", "") == "class_b_survives") & (pred.get("model", "") == "logistic_regression")]
    if not ok.empty:
        def best(fs: str) -> float | None:
            vals = ok[ok["feature_set"] == fs]["auc"].dropna()
            return float(vals.max()) if len(vals) else None
        rows.append(
            {
                "component": "predictive_leakage_class_b_survives",
                "latent1_auc": best("latent_1"),
                "latent2_auc": best("latent_2"),
                "latent3_auc": best("latent_3"),
                "controls_auc": best("controls_only"),
                "all_raw_auc": best("all_raw_metrics"),
            }
        )
    return pd.DataFrame(rows)


def best_auc(pred: pd.DataFrame, feature_set: str) -> float:
    subset = pred[
        (pred.get("target", "") == "class_b_survives")
        & (pred.get("feature_set", "") == feature_set)
        & (pred.get("model", "") == "logistic_regression")
    ]["auc"].dropna()
    return float(subset.max()) if len(subset) else math.nan


def local_decision(df: pd.DataFrame, pca_summary: dict[str, Any], recon: pd.DataFrame, pred: pd.DataFrame, leakage: pd.DataFrame) -> dict[str, Any]:
    rec = recon[(recon["source"] == "F1_success_cluster") & (recon["target"] == "mean_M1_M3_M5")]
    r2_k1 = float(rec[rec["k"] == 1]["r2"].iloc[0]) if not rec[rec["k"] == 1].empty else math.nan
    auc1 = best_auc(pred, "latent_1")
    auc2 = best_auc(pred, "latent_2")
    auc3 = best_auc(pred, "latent_3")
    controls = best_auc(pred, "controls_only")
    all_raw = best_auc(pred, "all_raw_metrics")
    pc1_control = leakage[leakage["component"] == "PC1"]["variance_explained_by_controls"]
    pc1_control_r2 = float(pc1_control.iloc[0]) if len(pc1_control) and not pd.isna(pc1_control.iloc[0]) else math.nan
    class_a = float(df["class_a_survives"].mean()) if len(df) else math.nan
    class_b = float(df["class_b_survives"].mean()) if len(df) else math.nan
    m135_clustered = r2_k1 >= 0.90
    multi_gain = max(auc2, auc3) - auc1 if not any(math.isnan(v) for v in [auc1, auc2, auc3]) else 0.0
    controls_explain = not math.isnan(pc1_control_r2) and pc1_control_r2 >= 0.80 and abs(controls - all_raw) <= 0.03
    multi_axis_pattern = (
        m135_clustered
        and multi_gain > 0.08
        and max(auc2, auc3) >= all_raw - 0.04
        and max(auc2, auc3) >= controls - 0.02
    )
    if len(df) < 50 or not m135_clustered:
        cls = "no_structure"
    elif multi_axis_pattern and not controls_explain:
        cls = "multi_axis"
    elif controls_explain:
        cls = "control_artifact"
    elif m135_clustered and abs(auc1 - all_raw) <= 0.03 and auc1 >= controls - 0.02:
        cls = "one_axis"
    else:
        cls = "metric_noise"
    return {
        "local_classification": cls,
        "class_count": int(len(df)),
        "class_a_survival": class_a,
        "class_b_survival": class_b,
        "m135_reconstruction_r2_k1": r2_k1,
        "class_b_auc_latent1": auc1,
        "class_b_auc_latent2": auc2,
        "class_b_auc_latent3": auc3,
        "controls_auc": controls,
        "all_raw_auc": all_raw,
        "pc1_control_variance_explained": pc1_control_r2,
        "pc1_f1_explained_variance": pca_summary["F1_real_metrics"]["explained_variance_ratio"][0]
        if pca_summary["F1_real_metrics"].get("explained_variance_ratio")
        else math.nan,
    }


def analyze_substrate(name: str, df: pd.DataFrame, out: Path, seed: int) -> dict[str, Any]:
    ensure(out)
    df = df.copy()
    df.to_csv(out / f"{name}_feature_matrix.csv", index=False)
    df[["class_id"] + METRICS_ALL].to_csv(out / f"{name}_metric_scores.csv", index=False)
    df[["class_id", "class_a_survives", "class_b_survives", "class_b_attack_cost", "class_b_auc_gns"]].to_csv(
        out / f"{name}_attack_labels.csv", index=False
    )
    corr, partial = correlations(df)
    corr.to_csv(out / f"{name}_correlation_matrix.csv")
    partial.to_csv(out / f"{name}_partial_correlations.csv", index=False)
    f3 = numeric_columns(df, {"class_b_survives", "class_a_survives", "class_b_attack_cost", "class_b_auc_gns"})
    pca_summary, loadings, scores = pca_outputs(
        df,
        {
            "F1_real_metrics": METRICS_REAL,
            "F2_real_plus_controls": METRICS_ALL,
            "F3_all_internal": f3,
            "F1_success_cluster": TARGET_METRICS,
        },
    )
    write_json(out / f"{name}_pca_summary.json", pca_summary)
    loadings.to_csv(out / f"{name}_pca_loadings.csv", index=False)
    recon = reconstruction_results(df, scores)
    recon.to_csv(out / f"{name}_reconstruction_results.csv", index=False)
    pred = prediction_results(df, scores, seed)
    pred.to_csv(out / f"{name}_prediction_results.csv", index=False)
    leakage = control_leakage(df, scores, pred)
    leakage.to_csv(out / f"{name}_control_leakage.csv", index=False)
    decision = local_decision(df, pca_summary, recon, pred, leakage)
    write_json(out / f"{name}_local_decision.json", decision)
    write_json(
        out / f"{name}_failure_examples.json",
        {
            "low_metric_cluster_examples": df.sort_values("M1_original_score").head(10)["class_id"].tolist(),
            "class_b_survivors": df[df["class_b_survives"].fillna(False).astype(bool)].head(10)["class_id"].tolist(),
            "class_b_broken": df[df["class_b_survives"].notna() & ~df["class_b_survives"].astype("boolean").fillna(True)].head(10)["class_id"].tolist(),
        },
    )
    return {"substrate": name, **decision}

