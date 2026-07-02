from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


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
    "dag_diversity",
    "operator_diversity",
    "depth_max",
    "M6_frequency_control_score",
    "M7_random_matched_score",
]
LOG_COLUMNS = ["class_size", "dag_diversity", "frequency", "reuse_count"]


@dataclass(frozen=True)
class PreparedMatrix:
    frame: pd.DataFrame
    columns: list[str]
    values: np.ndarray
    means: dict[str, float]
    scales: dict[str, float]


def active_sets_wide(active_sets: pd.DataFrame) -> pd.DataFrame:
    active_sets = active_sets.copy()
    active_sets["metric"] = "active_" + active_sets["metric"].str.replace(
        "_original", "", regex=False
    ).str.replace("_reuse", "", regex=False).str.replace(
        "_perturbation_centrality", "", regex=False
    )
    return (
        active_sets.pivot_table(index="class_id", columns="metric", values="active", aggfunc="max")
        .fillna(False)
        .astype(bool)
        .reset_index()
    )


def build_feature_matrix(
    metric_scores: pd.DataFrame,
    metric_active_sets: pd.DataFrame,
    functional_core: pd.DataFrame,
    strict_core: pd.DataFrame,
    attack_labels: pd.DataFrame | None = None,
) -> pd.DataFrame:
    df = metric_scores.copy()
    rename = {
        "freq": "frequency",
        "M1_original": "M1_original_score",
        "M2_intervention": "M2_intervention_score",
        "M3_reuse": "M3_reuse_score",
        "M4_compression": "M4_compression_score",
        "M5_perturbation_centrality": "M5_perturbation_centrality_score",
        "M6_frequency_control": "M6_frequency_control_score",
        "M7_random_matched": "M7_random_matched_score",
    }
    df = df.rename(columns=rename)
    df["expression_depth"] = df["depth_max"]
    df["reuse_rate"] = df["M3_reuse_score"]
    df["reuse_count"] = df["class_size"] * df["operator_diversity"]
    df["intervention_role"] = df["intervention_score"]
    df["conditional_role"] = df["conditional_score"]
    df["raw_score"] = df["M1_original_score"]

    act = active_sets_wide(metric_active_sets)
    df = df.merge(act, on="class_id", how="left")
    for name in ["active_M1", "active_M3", "active_M5"]:
        if name not in df:
            df[name] = False
        df[name] = df[name].fillna(False).astype(bool)

    functional = set(functional_core.get("class_id", pd.Series(dtype=str)).astype(str))
    strict = set(strict_core.get("class_id", pd.Series(dtype=str)).astype(str))
    df["functional_core_membership"] = df["class_id"].astype(str).isin(functional)
    df["strict_core_membership"] = df["class_id"].astype(str).isin(strict)

    df["class_a_survives"] = np.nan
    df["class_b_survives"] = np.nan
    df["class_b_attack_cost"] = np.nan
    df["class_b_auc_gns"] = np.nan
    if attack_labels is not None and not attack_labels.empty:
        keep = [
            c
            for c in ["class_id", "class_a_survives", "class_b_survives", "class_b_attack_cost", "class_b_auc_gns"]
            if c in attack_labels.columns
        ]
        df = df.drop(columns=[c for c in keep if c != "class_id" and c in df.columns]).merge(
            attack_labels[keep], on="class_id", how="left"
        )
    return df


def numeric_columns(df: pd.DataFrame, exclude: Iterable[str] = ()) -> list[str]:
    excluded = set(exclude) | {"class_id"}
    cols = []
    for col in df.columns:
        if col in excluded:
            continue
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
            cols.append(col)
    return cols


def prepare_matrix(df: pd.DataFrame, columns: list[str]) -> PreparedMatrix:
    work = df[columns].copy()
    for col in LOG_COLUMNS:
        if col in work:
            work[col] = np.log1p(work[col].clip(lower=0))
    work = work.replace([np.inf, -np.inf], np.nan).fillna(work.median(numeric_only=True))
    usable = []
    for col in work.columns:
        vals = work[col].astype(float)
        if vals.nunique(dropna=True) > 1 and vals.std(ddof=0) > 1e-12:
            usable.append(col)
    work = work[usable].astype(float)
    scaler = StandardScaler()
    values = scaler.fit_transform(work.values) if usable else np.empty((len(df), 0))
    return PreparedMatrix(
        frame=work,
        columns=usable,
        values=values,
        means=dict(zip(usable, scaler.mean_ if usable else [])),
        scales=dict(zip(usable, scaler.scale_ if usable else [])),
    )


def partial_corr(df: pd.DataFrame, x: str, y: str, controls: list[str]) -> float:
    cols = [x, y] + [c for c in controls if c in df.columns and c not in {x, y}]
    data = df[cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(data) < 4:
        return float("nan")
    xx = data[x].astype(float).values
    yy = data[y].astype(float).values
    cc = data[[c for c in controls if c in data.columns and c not in {x, y}]].astype(float).values
    if cc.shape[1] == 0:
        return float(pd.Series(xx).corr(pd.Series(yy)))
    cc = np.column_stack([np.ones(len(cc)), cc])
    rx = xx - cc @ np.linalg.lstsq(cc, xx, rcond=None)[0]
    ry = yy - cc @ np.linalg.lstsq(cc, yy, rcond=None)[0]
    sx, sy = rx.std(), ry.std()
    if sx <= 1e-12 or sy <= 1e-12:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])

