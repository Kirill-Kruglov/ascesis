from worldcore.generator import generate_random_world, generate_task, make_rng, valid_assignments
from worldcore.types import PREDICATE_BY_NAME


def test_random_world_facts_respect_declared_arities() -> None:
    world = generate_random_world(make_rng(1), "w", num_entities=10, max_facts=20)
    for fact in world.facts:
        predicate = fact.positive_predicate()
        assert predicate in PREDICATE_BY_NAME
        assert len(fact.args) == PREDICATE_BY_NAME[predicate].arity


def test_generate_all_required_task_families() -> None:
    rng = make_rng(2)
    for family in ["entailment", "contradiction", "unknown", "transitivity", "mixed", "distractor"]:
        _, task = generate_task(rng, f"task_{family}", family=family, proof_depth=3)
        assert task.task_id == f"task_{family}"
        assert task.canonical_world_hash
        assert task.canonical_task_hash


def test_valid_assignments_are_non_empty_for_core_predicate() -> None:
    world = generate_random_world(make_rng(3), "w", num_entities=10, max_facts=1)
    assert valid_assignments(world.entities, PREDICATE_BY_NAME["Feeds"])


def test_negation_family_can_generate_false_label() -> None:
    _, task = generate_task(make_rng(4), "task_negation", family="negation", proof_depth=1, entity_prefix="n_")
    assert task.answer is False
    assert task.reasoning_pattern == "negation"


def test_adversarial_pair_minimal_change_flips_answer() -> None:
    from worldcore.generator import generate_adversarial_pair

    true_pair, false_pair = generate_adversarial_pair(make_rng(5), "pair", entity_prefix="adv_")
    assert true_pair[1].answer is True
    assert false_pair[1].answer is False
    assert len(false_pair[0].facts) - len(true_pair[0].facts) == 2
