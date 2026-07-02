import importlib.util
from pathlib import Path
from types import SimpleNamespace

from semantic_taxonomy.taxonomy import OPERATOR_TAXONOMY

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_semantic_taxonomy", ROOT / "scripts" / "run_semantic_taxonomy.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_static_taxonomy_has_expected_priors() -> None:
    assert OPERATOR_TAXONOMY["P4_alpha_rename"]["candidate_class"] == "A"
    assert OPERATOR_TAXONOMY["P1_remove_edge"]["final_class"] == "B"
    assert OPERATOR_TAXONOMY["P8_merge_internal_nodes"]["final_class"] == "B"


def test_alpha_rename_audit_passes_on_small_sample() -> None:
    records = mod.build_records(seed=42, num_dags=8, max_depth=3, per_depth_cap=20)
    audit = mod.audit_operator(records, "P4_alpha_rename", sample_size=40, seed=42)
    assert audit["final_class"] == "A"
    assert audit["audit_changed"] == 0


def test_theory_change_attack_breaks_more_than_representation_only() -> None:
    records = mod.build_records(seed=42, num_dags=12, max_depth=3, per_depth_cap=20)
    args = SimpleNamespace(max_analyzed_classes=30, pairs_per_class=2, cross_pairs_per_class=2, max_attack_budget=2, candidate_budget=24, beam_width=4)
    rep, _ = mod.analyze(records, {"P4_alpha_rename"}, args, "representation_only")
    theory, _ = mod.analyze(records, {"P1_remove_edge", "P2_add_edge", "P3_reverse_edge", "P8_merge_internal_nodes"}, args, "theory_change")
    assert rep["surviving_fraction"] >= theory["surviving_fraction"]
