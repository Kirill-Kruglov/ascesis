import importlib.util
from pathlib import Path

from consequence_feature.dag import CausalDAG
from consequence_feature.expressions import make_expr
from consequence_feature.verifier import consequence_signature, freeze_signature

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_backbone_stress", ROOT / "scripts" / "run_backbone_stress.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def rec(dag, expr):
    return mod.expr_record(expr, dag, freeze_signature(consequence_signature(dag, expr)))


def test_cross_dag_attack_can_break_equivalence() -> None:
    dag_a = CausalDAG("a", ("N0", "N1"), tuple(), 0.1, 1)
    dag_b = CausalDAG("b", ("N0", "N1"), tuple(), 0.1, 2)
    expr_a = make_expr(dag_a, 1, "Reachable", "N0", "N1")
    expr_b = make_expr(dag_b, 1, "Reachable", "N0", "N1")
    pair = (rec(dag_a, expr_a), rec(dag_b, expr_b))
    assert mod.equivalent(dag_a, expr_a, dag_b, expr_b) is True
    result = mod.attack_pair(pair, max_budget=1, beam_width=8, max_candidates=20, mode="left_only")
    assert result["valid"] is True
    assert result["broken"] is True
    assert result["cost"] == 1
