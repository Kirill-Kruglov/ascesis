from worldcore.solver import answer_query, contradictions
from worldcore.types import Entity, Fact, WorldState


def test_parent_transitivity_derives_ancestor() -> None:
    world = WorldState(
        "w",
        (Entity("a", "Human"), Entity("b", "Human"), Entity("c", "Human")),
        frozenset({Fact("ParentOf", ("a", "b")), Fact("ParentOf", ("b", "c"))}),
    )
    answer, depth = answer_query(world, Fact("AncestorOf", ("a", "c")))
    assert answer is True
    assert depth >= 1


def test_implication_owns_uses_access() -> None:
    world = WorldState(
        "w",
        (Entity("h", "Human"), Entity("t", "Tool")),
        frozenset({Fact("Owns", ("h", "t")), Fact("Uses", ("h", "t"))}),
    )
    answer, _ = answer_query(world, Fact("HasAccessTo", ("h", "t")))
    assert answer is True


def test_universal_rule_and_contradiction() -> None:
    world = WorldState(
        "w",
        (Entity("socrates", "Human"), Entity("p", "Place")),
        frozenset({Fact("LocatedIn", ("socrates", "p")), Fact("NOT_LocatedIn", ("socrates", "p"))}),
    )
    assert answer_query(world, Fact("Mortal", ("socrates",)))[0] is True
    assert contradictions(world)
