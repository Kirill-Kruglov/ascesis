from worldcore.generator import generate_task, make_rng
from worldcore.proof import closure_audit, proof_opportunities_for_world


def test_closure_audit_exports_rule_applications() -> None:
    world, _ = generate_task(make_rng(20), "closure", family="transitivity", proof_depth=4, entity_prefix="cl_")
    audit = closure_audit(world)
    assert audit["initial_fact_count"] > 0
    assert audit["closure_size"] >= audit["initial_fact_count"]
    assert audit["rule_applications"]
    assert audit["derivation_graph"]["nodes"]


def test_proof_opportunities_include_canonical_hashes() -> None:
    world, _ = generate_task(make_rng(21), "op", family="implication+transitivity", proof_depth=4, entity_prefix="op_")
    opportunities = proof_opportunities_for_world(world)
    assert opportunities
    assert all(op["canonical_proof_hash"] for op in opportunities)
    assert {op["world_id"] for op in opportunities} == {world.world_id}
