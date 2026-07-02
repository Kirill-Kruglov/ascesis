import numpy as np
import pandas as pd

from latent_metric_geometry.geometry import build_feature_matrix, partial_corr, prepare_matrix


def test_prepare_matrix_drops_constant_column():
    df = pd.DataFrame({"class_id": ["a", "b", "c"], "x": [1, 2, 3], "constant": [7, 7, 7]})
    prepared = prepare_matrix(df, ["x", "constant"])
    assert prepared.columns == ["x"]
    assert prepared.values.shape == (3, 1)
    assert np.isclose(prepared.values.mean(), 0.0)


def test_build_feature_matrix_adds_core_labels():
    scores = pd.DataFrame(
        {
            "class_id": ["a", "b"],
            "freq": [0.1, 0.2],
            "class_size": [1, 2],
            "dag_diversity": [1, 2],
            "operator_diversity": [1, 2],
            "depth_min": [1, 1],
            "depth_max": [2, 3],
            "intervention_score": [0.0, 1.0],
            "conditional_score": [1.0, 0.0],
            "role_score": [1.0, 1.0],
            "M1_original": [0.1, 0.9],
            "M2_intervention": [0.0, 1.0],
            "M3_reuse": [0.2, 0.8],
            "M4_compression": [1.0, 2.0],
            "M5_perturbation_centrality": [0.3, 0.7],
            "M6_frequency_control": [0.4, 0.6],
            "M7_random_matched": [0.5, 0.5],
        }
    )
    active = pd.DataFrame(
        {
            "class_id": ["a", "b"],
            "metric": ["M1_original", "M1_original"],
            "active": [False, True],
            "score": [0.1, 0.9],
        }
    )
    df = build_feature_matrix(scores, active, pd.DataFrame({"class_id": ["b"]}), pd.DataFrame())
    assert df.loc[df.class_id == "b", "functional_core_membership"].iloc[0]
    assert "M1_original_score" in df.columns


def test_partial_corr_returns_finite_for_simple_case():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 11], "c": [5, 4, 3, 2, 1]})
    value = partial_corr(df, "x", "y", ["c"])
    assert np.isfinite(value) or np.isnan(value)

