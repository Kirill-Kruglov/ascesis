from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Answer = Literal[True, False, "unknown"]


@dataclass(frozen=True, order=True)
class Entity:
    id: str
    type: str


@dataclass(frozen=True, order=True)
class Fact:
    predicate: str
    args: tuple[str, ...]

    def positive_predicate(self) -> str:
        return self.predicate[4:] if self.predicate.startswith("NOT_") else self.predicate

    def negated(self) -> "Fact":
        if self.predicate.startswith("NOT_"):
            return Fact(self.predicate[4:], self.args)
        return Fact(f"NOT_{self.predicate}", self.args)

    def to_text(self) -> str:
        return f"{self.predicate}({','.join(self.args)})"


@dataclass(frozen=True)
class PredicateSpec:
    name: str
    arg_types: tuple[tuple[str, ...], ...]

    @property
    def arity(self) -> int:
        return len(self.arg_types)


@dataclass(frozen=True)
class UniversalRule:
    if_type: str
    then_predicate: str


@dataclass
class WorldState:
    world_id: str
    entities: tuple[Entity, ...]
    facts: frozenset[Fact]

    def entity_types(self) -> dict[str, str]:
        return {entity.id: entity.type for entity in self.entities}


@dataclass
class Task:
    world_id: str
    task_id: str
    facts: tuple[Fact, ...]
    query: Fact
    answer: Answer
    proof_depth: int
    reasoning_pattern: str
    canonical_world_hash: str = ""
    canonical_task_hash: str = ""
    num_distractors: int = 0
    num_supporting_facts: int = 0
    num_irrelevant_facts: int = 0
    num_predicates: int = 0
    num_entities: int = 0
    num_inference_rules_used: int = 0

    def to_record(self) -> dict[str, object]:
        return {
            "world_id": self.world_id,
            "task_id": self.task_id,
            "facts": [fact.to_text() for fact in self.facts],
            "query": self.query.to_text(),
            "answer": self.answer,
            "proof_depth": self.proof_depth,
            "reasoning_pattern": self.reasoning_pattern,
            "canonical_world_hash": self.canonical_world_hash,
            "canonical_task_hash": self.canonical_task_hash,
            "num_distractors": self.num_distractors,
            "num_supporting_facts": self.num_supporting_facts,
            "num_irrelevant_facts": self.num_irrelevant_facts,
            "num_predicates": self.num_predicates,
            "num_entities": self.num_entities,
            "num_inference_rules_used": self.num_inference_rules_used,
        }


TYPES: tuple[str, ...] = (
    "Human",
    "Animal",
    "Plant",
    "Tool",
    "Place",
    "Food",
    "Object",
    "Event",
    "Group",
    "Property",
)


PREDICATES: tuple[PredicateSpec, ...] = (
    PredicateSpec("HasProperty", (TYPES, ("Property",))),
    PredicateSpec("LocatedIn", (TYPES, ("Place",))),
    PredicateSpec("Owns", (("Human",), ("Object", "Animal", "Tool", "Food", "Plant"))),
    PredicateSpec("Uses", (("Human",), ("Tool", "Object"))),
    PredicateSpec("Eats", (("Animal", "Human"), ("Food", "Plant"))),
    PredicateSpec("Feeds", (("Human",), ("Animal",))),
    PredicateSpec("Helps", (("Human",), ("Human", "Animal"))),
    PredicateSpec("ParentOf", (("Human", "Animal"), ("Human", "Animal"))),
    PredicateSpec("AncestorOf", (("Human", "Animal"), ("Human", "Animal"))),
    PredicateSpec("FriendOf", (("Human",), ("Human",))),
    PredicateSpec("Causes", (("Event",), ("Event",))),
    PredicateSpec("Before", (("Event",), ("Event",))),
    PredicateSpec("Prevents", (("Event",), ("Event",))),
    PredicateSpec("Wants", (("Human",), ("Object", "Event", "Food", "Tool", "Animal"))),
    PredicateSpec("Knows", (("Human",), TYPES)),
    PredicateSpec("Believes", (("Human",), TYPES)),
    PredicateSpec("MemberOf", (("Human",), ("Group",))),
    PredicateSpec("LeaderOf", (("Human",), ("Group",))),
    PredicateSpec("BiggerThan", (("Object", "Animal", "Tool", "Plant"), ("Object", "Animal", "Tool", "Plant"))),
    PredicateSpec("PartOf", (("Object", "Tool", "Plant"), ("Object", "Tool", "Plant"))),
    PredicateSpec("Mortal", (("Human", "Animal"),)),
    PredicateSpec("HasAccessTo", (("Human",), ("Object", "Tool", "Food", "Animal", "Plant"))),
)


PREDICATE_BY_NAME: dict[str, PredicateSpec] = {spec.name: spec for spec in PREDICATES}


UNIVERSAL_RULES: tuple[UniversalRule, ...] = (
    UniversalRule("Human", "Mortal"),
    UniversalRule("Animal", "Mortal"),
)
