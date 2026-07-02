import importlib.util
from pathlib import Path

from closure_metric_robustness.metrics import compute_metric_scores, select_top_fraction

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_closure_metric_robustness", ROOT / "scripts" / "run_closure_metric_robustness.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def test_metric_scores_all_families_present() -> None:
    records = mod.run17a2.build_records(seed=42, num_dags=8, max_depth=3, per_depth_cap=20)
    table, scores = compute_metric_scores(records, seed=42)
    assert len(table) > 0
    assert set(scores) == {"M1_original", "M2_intervention", "M3_reuse", "M4_compression", "M5_perturbation_centrality", "M6_frequency_control", "M7_random_matched"}
    assert all(set(s) == set(table) for s in scores.values())


def test_select_top_fraction_size() -> None:
    scores = {i: float(i) for i in range(10)}
    assert select_top_fraction(scores, 0.3) == {7, 8, 9}


def test_overlap_rows_has_jaccard() -> None:
    active = {"a": {1,2,3}, "b": {2,3,4}}
    scores = {"a": {1:1,2:2,3:3,4:0}, "b": {1:0,2:2,3:3,4:4}}
    rows = mod.overlap_rows(active, scores)
    assert rows[0]["jaccard"] == 0.5
    assert rows[0]["overlap_coefficient"] == 2/3
