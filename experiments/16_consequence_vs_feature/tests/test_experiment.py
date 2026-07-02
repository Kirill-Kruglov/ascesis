import random

from consequence_feature.dag import CausalDAG, generate_dag_grid
from consequence_feature.expressions import generate_expressions, make_expr
from consequence_feature.verifier import consequence_signature, freeze_signature


def test_generate_dag_grid_respects_requested_count() -> None:
    dags = generate_dag_grid(seed=42, num_dags=17)
    assert len(dags) == 17
    for dag in dags:
        # Edges follow some topological order, so reachability can never cycle back.
        for a, b in dag.directed_edges:
            assert not dag.reachable(b, a)


def test_different_features_can_have_same_consequence() -> None:
    dag = CausalDAG("d", ("N0", "N1"), (("N0", "N1"),), 0.1, 1)
    a = make_expr(dag, 1, "Reachable", "N0", "N1")
    b = make_expr(dag, 1, "Effect", "N0", "N1")
    assert a.feature_key() != b.feature_key()
    assert freeze_signature(consequence_signature(dag, a)) == freeze_signature(consequence_signature(dag, b))


def test_same_features_can_have_different_consequences_across_dags() -> None:
    dag_a = CausalDAG("a", ("N0", "N1"), (("N0", "N1"),), 0.1, 1)
    dag_b = CausalDAG("b", ("N0", "N1"), tuple(), 0.1, 2)
    expr_a = make_expr(dag_a, 1, "Reachable", "N0", "N1")
    expr_b = make_expr(dag_b, 1, "Reachable", "N0", "N1")
    assert expr_a.feature_key() == expr_b.feature_key()
    assert freeze_signature(consequence_signature(dag_a, expr_a)) != freeze_signature(consequence_signature(dag_b, expr_b))


def test_expression_generation_is_bounded_by_per_depth_cap() -> None:
    dag = CausalDAG("d", tuple(f"N{i}" for i in range(10)), tuple(), 0.1, 1)
    exprs = generate_expressions(dag, max_depth=6, rng=random.Random(1), per_depth_cap=20)
    assert len(exprs) <= 120
    assert {e.depth for e in exprs} == {1, 2, 3, 4, 5, 6}
