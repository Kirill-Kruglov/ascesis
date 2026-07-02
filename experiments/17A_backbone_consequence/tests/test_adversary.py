from backbone_stress.adversary import adversarial_candidates, has_cycle
from consequence_feature.dag import CausalDAG


def test_adversarial_candidates_include_new_families_and_are_acyclic() -> None:
    dag = CausalDAG(
        "d",
        ("A", "B", "C", "X", "Y"),
        (("A", "B"), ("B", "C"), ("A", "C"), ("X", "Y")),
        0.2,
        1,
    )
    candidates = adversarial_candidates(dag, protected={"A", "C"}, limit_per_family=12)
    ops = {c.operations[0] for c in candidates}
    assert "P6_delete_path" in ops
    assert "P7_replace_chain" in ops
    assert "P8_merge_internal_nodes" in ops
    assert "P9_split_node" in ops
    assert "P10_replace_subgraph" in ops
    assert "P12_alternative_derivation" in ops
    assert all(not has_cycle(c.dag.nodes, set(c.dag.directed_edges)) for c in candidates)


def test_protected_nodes_are_preserved() -> None:
    dag = CausalDAG("d", ("A", "B", "C"), (("A", "B"), ("B", "C")), 0.2, 1)
    candidates = adversarial_candidates(dag, protected={"A", "C"})
    assert candidates
    assert all({"A", "C"}.issubset(set(c.dag.nodes)) for c in candidates)
