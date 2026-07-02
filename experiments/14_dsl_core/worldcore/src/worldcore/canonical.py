from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import defaultdict

from worldcore.types import Entity, Fact, Task, WorldState


def _sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _canonical_payload_for_mapping(world: WorldState, mapping: dict[str, str]) -> tuple[tuple[str, str], tuple[str, tuple[str, ...]], ...]:
    entities = tuple(sorted((mapping[entity.id], entity.type) for entity in world.entities))
    facts = tuple(sorted((fact.predicate, tuple(mapping.get(arg, arg) for arg in fact.args)) for fact in world.facts))
    return entities + facts


def _exact_canonical_payload(world: WorldState, max_permutations: int = 120_000) -> object | None:
    groups: dict[str, list[str]] = defaultdict(list)
    for entity in world.entities:
        groups[entity.type].append(entity.id)
    total = math.prod(math.factorial(len(ids)) for ids in groups.values())
    if total > max_permutations:
        return None

    typed_targets: dict[str, list[str]] = {}
    for typ, ids in groups.items():
        typed_targets[typ] = [f"{typ.lower()}_{idx}" for idx in range(len(ids))]

    best: object | None = None
    type_items = sorted(groups.items())
    permutation_sets = [itertools.permutations(sorted(ids)) for _, ids in type_items]
    for product in itertools.product(*permutation_sets):
        mapping: dict[str, str] = {}
        for (typ, _), ordered_ids in zip(type_items, product):
            for source_id, target_id in zip(ordered_ids, typed_targets[typ]):
                mapping[source_id] = target_id
        payload = _canonical_payload_for_mapping(world, mapping)
        if best is None or repr(payload) < repr(best):
            best = payload
    return best


def _refined_mapping(world: WorldState, rounds: int = 6) -> dict[str, str]:
    colors = {entity.id: entity.type for entity in world.entities}
    for _ in range(rounds):
        next_colors: dict[str, str] = {}
        for entity in world.entities:
            incident = []
            for fact in world.facts:
                for pos, arg in enumerate(fact.args):
                    if arg == entity.id:
                        context = tuple(colors.get(other, other) for other in fact.args)
                        incident.append((fact.predicate, pos, context))
            next_colors[entity.id] = json.dumps([entity.type, sorted(incident)], sort_keys=True)
        if next_colors == colors:
            break
        colors = next_colors

    by_type: dict[str, list[Entity]] = defaultdict(list)
    for entity in world.entities:
        by_type[entity.type].append(entity)

    mapping: dict[str, str] = {}
    for typ, entities in by_type.items():
        ordered = sorted(entities, key=lambda entity: (colors[entity.id], entity.id))
        for idx, entity in enumerate(ordered):
            mapping[entity.id] = f"{typ.lower()}_{idx}"
    return mapping


def canonical_world_payload(world: WorldState) -> object:
    exact = _exact_canonical_payload(world)
    if exact is not None:
        return exact
    mapping = _refined_mapping(world)
    return _canonical_payload_for_mapping(world, mapping)


def canonical_world_hash(world: WorldState) -> str:
    return _sha256_json(canonical_world_payload(world))


def canonical_task_hash(task: Task) -> str:
    query_fact = Fact("__QUERY__", task.query.args)
    world = WorldState(task.world_id, _entities_from_facts(task.facts + (query_fact,)), frozenset(task.facts + (query_fact,)))
    payload = {
        "world": canonical_world_payload(world),
        "query_predicate": task.query.predicate,
        "answer": task.answer,
        "proof_depth": task.proof_depth,
        "pattern": task.reasoning_pattern,
    }
    return _sha256_json(payload)


def _entities_from_facts(facts: tuple[Fact, ...]) -> tuple[Entity, ...]:
    # Task hashes are normally filled from generated worlds. This fallback keeps
    # manual Task construction hashable even without an explicit entity table.
    ids = sorted({arg for fact in facts for arg in fact.args})
    return tuple(Entity(entity_id, "Unknown") for entity_id in ids)


def is_isomorphic_world(w1: WorldState, w2: WorldState) -> bool:
    return canonical_world_hash(w1) == canonical_world_hash(w2)
