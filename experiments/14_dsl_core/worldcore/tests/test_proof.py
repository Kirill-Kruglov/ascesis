from worldcore.generator import generate_adversarial_pair, generate_task, make_rng
from worldcore.proof import extract_proof


def test_extracts_nonempty_proof_for_transitivity() -> None:
    world, task = generate_task(make_rng(10), "proof_trans", family="transitivity", proof_depth=4, entity_prefix="pt_")
    proof = extract_proof(world, task, proof_id="p")
    assert proof["proof_id"] == "p"
    assert proof["proof_graph"]["nodes"]
    assert proof["metrics"]["length"] >= 1
    assert proof["metrics"]["canonical_proof_hash"]


def test_negative_adversarial_proof_uses_negated_conclusion() -> None:
    _, false_pair = generate_adversarial_pair(make_rng(11), "proof_adv", entity_prefix="pa_")
    proof = extract_proof(false_pair[0], false_pair[1], proof_id="p_false")
    assert proof["answer"] == "False"
    assert str(proof["final_conclusion"]).startswith("NOT_")
