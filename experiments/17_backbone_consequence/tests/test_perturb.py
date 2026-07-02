import random

from backbone_consequence.perturb import is_acyclic, one_step_perturbations, perturbation_samples
from consequence_feature.dag import CausalDAG
from consequence_feature.expressions import make_expr
from consequence_feature.verifier import consequence_signature, freeze_signature


def test_one_step_perturbations_preserve_acyclicity() -> None:
    dag = CausalDAG("d", ("A", "B", "C"), (("A", "B"), ("B", "C")), 0.2, 1)
    perturbed = one_step_perturbations(dag, protected={"A", "C"})
    assert perturbed
    assert all(is_acyclic(p.dag) for p in perturbed)


def test_alpha_rename_does_not_touch_protected_variables() -> None:
    dag = CausalDAG("d", ("A", "B", "C"), (("A", "B"), ("B", "C")), 0.2, 1)
    perturbed = one_step_perturbations(dag, protected={"A", "C"})
    alpha = [p for p in perturbed if p.operations == ("P4_alpha_rename",)]
    assert alpha
    assert all("A" in p.dag.nodes and "C" in p.dag.nodes for p in alpha)


def test_k_budget_samples_are_verifier_compatible() -> None:
    dag = CausalDAG("d", ("N0", "N1", "N2"), (("N0", "N1"), ("N1", "N2")), 0.2, 1)
    expr = make_expr(dag, 1, "Reachable", "N0", "N2")
    samples = perturbation_samples(dag, 2, protected={"N0", "N2"}, rng=random.Random(1), samples=8)
    assert samples
    for item in samples:
        sig = freeze_signature(consequence_signature(item.dag, expr))
        assert sig


def test_remove_edge_can_destroy_reachability_signature() -> None:
    dag = CausalDAG("d", ("N0", "N1"), (("N0", "N1"),), 0.2, 1)
    expr = make_expr(dag, 1, "Reachable", "N0", "N1")
    original = freeze_signature(consequence_signature(dag, expr))
    removed = [p for p in one_step_perturbations(dag, protected={"N0", "N1"}) if p.operations == ("P1_remove_edge",)][0]
    changed = freeze_signature(consequence_signature(removed.dag, expr))
    assert changed != original
