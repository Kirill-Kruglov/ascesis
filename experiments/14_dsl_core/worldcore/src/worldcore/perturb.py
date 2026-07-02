from __future__ import annotations

import random

from worldcore.types import Entity, Fact, WorldState


def renamed_world(world: WorldState, seed: int = 0) -> WorldState:
    rng = random.Random(seed)
    entities = list(world.entities)
    by_type: dict[str, list[Entity]] = {}
    for entity in entities:
        by_type.setdefault(entity.type, []).append(entity)

    mapping: dict[str, str] = {}
    renamed_entities: list[Entity] = []
    for typ, group in by_type.items():
        ids = [entity.id for entity in group]
        shuffled = ids[:]
        rng.shuffle(shuffled)
        for idx, old_id in enumerate(shuffled):
            new_id = f"{typ.lower()}_renamed_{idx}"
            mapping[old_id] = new_id
            renamed_entities.append(Entity(new_id, typ))

    renamed_facts = frozenset(Fact(fact.predicate, tuple(mapping.get(arg, arg) for arg in fact.args)) for fact in world.facts)
    return WorldState(f"{world.world_id}_renamed", tuple(sorted(renamed_entities)), renamed_facts)
