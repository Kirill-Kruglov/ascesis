from consequence_feature.dag import CausalDAG


def test_reachability_and_ancestors() -> None:
    dag = CausalDAG("d", ("A", "B", "C"), (("A", "B"), ("B", "C")), 0.1, 1)
    assert dag.reachable("A", "C")
    assert not dag.reachable("C", "A")
    assert dag.ancestors("C") == {"A", "B"}


def test_intervention_removes_incoming_edges_only() -> None:
    dag = CausalDAG("d", ("A", "B", "C"), (("A", "B"), ("B", "C"), ("A", "C")), 0.1, 1)
    intervened = dag.remove_incoming({"C"})
    assert ("A", "C") not in intervened.directed_edges
    assert ("B", "C") not in intervened.directed_edges
    assert ("A", "B") in intervened.directed_edges


def test_d_separation_chain_and_collider() -> None:
    chain = CausalDAG("chain", ("A", "B", "C"), (("A", "B"), ("B", "C")), 0.1, 1)
    assert not chain.d_separated("A", "C", set())
    assert chain.d_separated("A", "C", {"B"})

    collider = CausalDAG("collider", ("A", "B", "C"), (("A", "B"), ("C", "B")), 0.1, 1)
    assert collider.d_separated("A", "C", set())
    assert not collider.d_separated("A", "C", {"B"})
