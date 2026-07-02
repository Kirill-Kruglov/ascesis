import importlib.util
from pathlib import Path

from interpretive_closure.closure import compute_closure_state, group_records

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_interpretive_closure", ROOT / "scripts" / "run_interpretive_closure.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_closure_state_partitions_classes() -> None:
    records = mod.run17a2.build_records(seed=42, num_dags=12, max_depth=3, per_depth_cap=20)
    state = compute_closure_state(records, strong_quantile=0.5)
    groups = group_records(records)
    assert len(state["active_keys"] | state["dead_keys"]) == len(groups)
    assert state["active_keys"].isdisjoint(state["dead_keys"])
    assert 0 < state["metrics"]["closure_participation_rate"] < 1


def test_records_for_keys_filters_to_active_set() -> None:
    records = mod.run17a2.build_records(seed=42, num_dags=8, max_depth=3, per_depth_cap=20)
    state = compute_closure_state(records, strong_quantile=0.5)
    subset = mod.records_for_keys(records, state["active_keys"])
    assert subset
    assert all(r["consequence_key"] in state["active_keys"] for r in subset)


def test_decision_detects_dead_invariant_classes() -> None:
    closure_state = {"metrics": {"num_classes": 100}}
    open_summary = {"class_a": {"surviving_fraction": 1.0}, "class_b": {"surviving_fraction": 0.1}}
    weak_summary = open_summary
    strong_summary = {"class_a": {"surviving_fraction": 1.0}, "class_b": {"surviving_fraction": 0.5}}
    class FakeDf:
        def __len__(self):
            return 40
    decision = mod.decide(open_summary, weak_summary, strong_summary, closure_state, FakeDf(), FakeDf())
    assert decision["classification"] == "H3_supported"
