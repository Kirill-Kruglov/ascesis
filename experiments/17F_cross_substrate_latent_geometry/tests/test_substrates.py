from cross_substrate_latent_geometry.analysis import METRICS_ALL, analyze_substrate
from cross_substrate_latent_geometry.substrates import directed_graph_substrate, rewrite_substrate


def test_directed_graph_substrate_has_metrics_and_labels(tmp_path):
    df = directed_graph_substrate(seed=42, num_objects=20, max_depth=5)
    assert len(df) > 10
    for col in METRICS_ALL:
        assert col in df.columns
    assert df["class_b_survives"].nunique() >= 1


def test_analyze_substrate_writes_decision(tmp_path):
    df = rewrite_substrate(seed=42, num_objects=30, max_depth=4)
    result = analyze_substrate("test_rewrite", df, tmp_path, seed=42)
    assert "local_classification" in result
    assert (tmp_path / "test_rewrite_local_decision.json").exists()

