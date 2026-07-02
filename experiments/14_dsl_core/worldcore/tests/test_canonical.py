from worldcore.canonical import canonical_task_hash, canonical_world_hash, is_isomorphic_world
from worldcore.perturb import renamed_world
from worldcore.types import Entity, Fact, Task, WorldState


def test_renamed_worlds_have_identical_canonical_hashes() -> None:
    world = WorldState(
        "w",
        (Entity("h1", "Human"), Entity("a1", "Animal")),
        frozenset({Fact("Owns", ("h1", "a1")), Fact("Feeds", ("h1", "a1"))}),
    )
    renamed = renamed_world(world, seed=7)
    assert canonical_world_hash(world) == canonical_world_hash(renamed)
    assert is_isomorphic_world(world, renamed)


def test_task_hash_includes_query_under_canonical_renaming() -> None:
    task1 = Task("w", "t", (Fact("Before", ("e0", "e1")),), Fact("Before", ("e0", "e1")), True, 0, "entailment")
    task2 = Task("w", "t", (Fact("Before", ("x", "y")),), Fact("Before", ("x", "y")), True, 0, "entailment")
    assert canonical_task_hash(task1) == canonical_task_hash(task2)
