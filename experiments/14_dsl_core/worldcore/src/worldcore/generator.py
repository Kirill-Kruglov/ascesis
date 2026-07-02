from __future__ import annotations

import random
from dataclasses import replace

from worldcore.canonical import canonical_task_hash, canonical_world_hash
from worldcore.solver import answer_query, contradictions
from worldcore.types import Entity, Fact, PREDICATES, PredicateSpec, Task, TYPES, WorldState


def make_rng(seed: int | None = None) -> random.Random:
    return random.Random(seed)


def generate_entities(rng: random.Random, num_entities: int, prefix: str = "") -> tuple[Entity, ...]:
    required = ["Human", "Animal", "Place", "Object", "Tool", "Event", "Food", "Plant", "Group", "Property"]
    types = required[: min(num_entities, len(required))]
    while len(types) < num_entities:
        types.append(rng.choice(TYPES))
    rng.shuffle(types)
    counters: dict[str, int] = {}
    entities = []
    for typ in types:
        counters[typ] = counters.get(typ, 0) + 1
        stem = f"{typ[0].lower()}{counters[typ]}"
        entities.append(Entity(f"{prefix}{stem}", typ))
    return tuple(entities)


def valid_assignments(entities: tuple[Entity, ...], spec: PredicateSpec) -> list[tuple[str, ...]]:
    by_type: dict[str, list[str]] = {}
    for entity in entities:
        by_type.setdefault(entity.type, []).append(entity.id)
    choices = []
    for allowed_types in spec.arg_types:
        ids = [entity_id for typ in allowed_types for entity_id in by_type.get(typ, [])]
        if not ids:
            return []
        choices.append(ids)
    assignments: list[tuple[str, ...]] = [()]
    for ids in choices:
        assignments = [prefix + (entity_id,) for prefix in assignments for entity_id in ids]
    return [args for args in assignments if len(set(args)) == len(args)]


def random_valid_fact(rng: random.Random, entities: tuple[Entity, ...], specs: tuple[PredicateSpec, ...] = PREDICATES) -> Fact:
    candidates = [spec for spec in specs if valid_assignments(entities, spec)]
    spec = rng.choice(candidates)
    args = rng.choice(valid_assignments(entities, spec))
    predicate = spec.name
    if predicate in {"LocatedIn", "Before", "PartOf"} and rng.random() < 0.03:
        predicate = f"NOT_{predicate}"
    return Fact(predicate, args)


def generate_random_world(
    rng: random.Random,
    world_id: str,
    num_entities: int = 10,
    max_facts: int = 18,
    entity_prefix: str = "",
) -> WorldState:
    entities = generate_entities(rng, num_entities, entity_prefix)
    facts: set[Fact] = set()
    attempts = 0
    while len(facts) < max_facts and attempts < max_facts * 20:
        facts.add(random_valid_fact(rng, entities))
        attempts += 1
    return WorldState(world_id=world_id, entities=entities, facts=frozenset(facts))


def generate_chain_world(rng: random.Random, world_id: str, depth: int, predicate: str = "Before", entity_prefix: str = "") -> tuple[WorldState, Fact, set[Fact]]:
    if predicate == "Before":
        entities = tuple(Entity(f"{entity_prefix}e{i}", "Event") for i in range(depth + 1))
        facts = {Fact("Before", (f"{entity_prefix}e{i}", f"{entity_prefix}e{i + 1}")) for i in range(depth)}
        query = Fact("Before", (f"{entity_prefix}e0", f"{entity_prefix}e{depth}"))
    elif predicate == "ParentOf":
        typ = rng.choice(["Human", "Animal"])
        entities = tuple(Entity(f"{entity_prefix}x{i}", typ) for i in range(depth + 1))
        facts = {Fact("ParentOf", (f"{entity_prefix}x{i}", f"{entity_prefix}x{i + 1}")) for i in range(depth)}
        query = Fact("AncestorOf", (f"{entity_prefix}x0", f"{entity_prefix}x{depth}"))
    else:
        entities = tuple(Entity(f"{entity_prefix}o{i}", "Object") for i in range(depth + 1))
        facts = {Fact("PartOf", (f"{entity_prefix}o{i}", f"{entity_prefix}o{i + 1}")) for i in range(depth)}
        query = Fact("PartOf", (f"{entity_prefix}o0", f"{entity_prefix}o{depth}"))
    distractors = _distractors(rng, entities, count=max(0, depth - 1))
    world = WorldState(world_id, entities, frozenset(facts | distractors))
    return world, query, facts


def generate_mixed_world(rng: random.Random, world_id: str, pattern: str = "mixed", depth: int = 3, entity_prefix: str = "") -> tuple[WorldState, Fact, set[Fact], int]:
    p = entity_prefix
    if pattern == "implication+transitivity":
        entities = (Entity(f"{p}h0", "Human"), Entity(f"{p}a0", "Animal"), Entity(f"{p}p0", "Place"), Entity(f"{p}p1", "Place"))
        support = {Fact("Feeds", (f"{p}h0", f"{p}a0")), Fact("LocatedIn", (f"{p}a0", f"{p}p0")), Fact("LocatedIn", (f"{p}p0", f"{p}p1"))}
        query = Fact("Helps", (f"{p}h0", f"{p}a0"))
        rules = 2
    elif pattern == "transitivity+negation":
        entities = tuple(Entity(f"{p}e{i}", "Event") for i in range(max(depth + 1, 4)))
        support = {Fact("Before", (f"{p}e{i}", f"{p}e{i + 1}")) for i in range(depth)}
        bad = Fact("Before", (f"{p}e{depth - 1}", f"{p}e{depth}"))
        support.add(bad.negated())
        query = Fact("Before", (f"{p}e0", f"{p}e{depth}"))
        rules = 2
    elif pattern == "causal+temporal":
        entities = tuple(Entity(f"{p}e{i}", "Event") for i in range(3))
        support = {Fact("Causes", (f"{p}e0", f"{p}e1")), Fact("Before", (f"{p}e1", f"{p}e2"))}
        query = Fact("Before", (f"{p}e0", f"{p}e2"))
        rules = 2
    elif pattern == "belief+fact":
        entities = (Entity(f"{p}h0", "Human"), Entity(f"{p}e0", "Event"))
        support = {Fact("Knows", (f"{p}h0", f"{p}e0"))}
        query = Fact("Believes", (f"{p}h0", f"{p}e0"))
        rules = 1
    elif pattern == "part-of+location":
        entities = (Entity(f"{p}o0", "Object"), Entity(f"{p}o1", "Object"), Entity(f"{p}p0", "Place"))
        support = {Fact("PartOf", (f"{p}o0", f"{p}o1")), Fact("LocatedIn", (f"{p}o1", f"{p}p0"))}
        query = Fact("LocatedIn", (f"{p}o0", f"{p}p0"))
        rules = 2
    else:
        entities = (Entity(f"{p}h0", "Human"), Entity(f"{p}a0", "Animal"), Entity(f"{p}p0", "Place"), Entity(f"{p}p1", "Place"), Entity(f"{p}o0", "Object"), Entity(f"{p}t0", "Tool"))
        if rng.random() < 0.5:
            support = {Fact("Owns", (f"{p}h0", f"{p}t0")), Fact("Uses", (f"{p}h0", f"{p}t0"))}
            query = Fact("HasAccessTo", (f"{p}h0", f"{p}t0"))
        else:
            support = {Fact("LocatedIn", (f"{p}a0", f"{p}p0")), Fact("LocatedIn", (f"{p}p0", f"{p}p1"))}
            query = Fact("LocatedIn", (f"{p}a0", f"{p}p1"))
        rules = 1
    distractors = _distractors(rng, entities, 3)
    return WorldState(world_id, entities, frozenset(support | distractors)), query, support, rules


def generate_adversarial_pair(rng: random.Random, pair_id: str, entity_prefix: str = "adv_") -> tuple[tuple[WorldState, Task], tuple[WorldState, Task]]:
    p = entity_prefix
    entities = (Entity(f"{p}{pair_id}_a", "Event"), Entity(f"{p}{pair_id}_b", "Event"), Entity(f"{p}{pair_id}_c", "Event"))
    base_support = {Fact("Before", (entities[0].id, entities[1].id)), Fact("Before", (entities[1].id, entities[2].id))}
    query = Fact("Before", (entities[0].id, entities[2].id))
    world_true = WorldState(f"adv_{pair_id}_true", entities, frozenset(base_support))
    world_false = WorldState(f"adv_{pair_id}_false", entities, frozenset(base_support | {Fact("NOT_Before", (entities[1].id, entities[2].id)), query.negated()}))
    task_true = _make_task(world_true, f"adv_{pair_id}_true", query, "adversarial_transitivity", base_support, 0, 1, override_answer=True, intended_depth=2)
    task_false = _make_task(world_false, f"adv_{pair_id}_false", query, "adversarial_transitivity+negation", base_support, 1, 2, intended_depth=2)
    return (world_true, task_true), (world_false, task_false)


def generate_task(
    rng: random.Random,
    task_id: str,
    family: str | None = None,
    proof_depth: int | None = None,
    entity_prefix: str = "",
) -> tuple[WorldState, Task]:
    families = ["entailment", "contradiction", "negation", "unknown", "transitivity", "mixed", "distractor"]
    family = family or rng.choice(families)
    depth = proof_depth or rng.randint(1, 4)
    world_id = f"world_{task_id}"
    p = entity_prefix

    if family == "transitivity":
        world, query, support = generate_chain_world(rng, world_id, max(2, depth), rng.choice(["Before", "ParentOf", "PartOf"]), p)
        return world, _make_task(world, task_id, query, "transitivity", support, len(world.facts - support), 1, intended_depth=max(2, depth))
    if family in {"mixed", "implication+transitivity", "transitivity+negation", "causal+temporal", "belief+fact", "part-of+location"}:
        pattern = family if family != "mixed" else rng.choice(["implication+transitivity", "causal+temporal", "belief+fact", "part-of+location"])
        world, query, support, rules = generate_mixed_world(rng, world_id, pattern, max(3, depth), p)
        return world, _make_task(world, task_id, query, pattern, support, len(world.facts - support), rules, intended_depth=max(1, depth))
    if family == "contradiction":
        entities = (Entity(f"{p}h0", "Human"), Entity(f"{p}p0", "Place"), Entity(f"{p}p1", "Place"))
        fact = Fact("LocatedIn", (f"{p}h0", f"{p}p0"))
        support = {fact, fact.negated(), Fact("LocatedIn", (f"{p}p0", f"{p}p1"))}
        world = WorldState(world_id, entities, frozenset(support))
        return world, _make_task(world, task_id, fact.negated(), "contradiction", support, 0, 1, override_answer=True, intended_depth=1)
    if family == "negation":
        entities = (Entity(f"{p}h0", "Human"), Entity(f"{p}p0", "Place"))
        fact = Fact("LocatedIn", (f"{p}h0", f"{p}p0"))
        support = {fact.negated()}
        world = WorldState(world_id, entities, frozenset(support))
        return world, _make_task(world, task_id, fact, "negation", support, 0, 1, intended_depth=1)
    if family == "unknown":
        world = generate_random_world(rng, world_id, 9, 10, p)
        entities_by_type = {entity.type: entity.id for entity in world.entities}
        query = Fact("Owns", (entities_by_type.get("Human", world.entities[0].id), entities_by_type.get("Object", world.entities[-1].id)))
        attempts = 0
        while answer_query(world, query)[0] != "unknown" and attempts < 20:
            world = generate_random_world(rng, world_id, 9, 10, p)
            attempts += 1
        return world, _make_task(world, task_id, query, "unknown", set(), len(world.facts), 0, intended_depth=0)
    if family == "distractor":
        world, query, support = generate_chain_world(rng, world_id, max(2, depth), "Before", p)
        extra = _distractors(rng, world.entities, 15)
        world = replace(world, facts=frozenset(set(world.facts) | extra))
        return world, _make_task(world, task_id, query, "transitivity", support, len(world.facts - support), 1, intended_depth=max(2, depth))

    world = generate_random_world(rng, world_id, 10, 14, p)
    query = sorted(world.facts)[0]
    return world, _make_task(world, task_id, query, "entailment", {query}, len(world.facts) - 1, 0, intended_depth=0)


def generate_tasks(rng: random.Random, count: int, max_depth: int = 4, entity_prefix: str = "") -> list[Task]:
    tasks = []
    families = ["entailment", "contradiction", "negation", "unknown", "transitivity", "mixed", "distractor"]
    for idx in range(count):
        family = families[idx % len(families)]
        _, task = generate_task(rng, f"task_{idx}", family=family, proof_depth=1 + (idx % max_depth), entity_prefix=entity_prefix)
        tasks.append(task)
    return tasks


def _make_task(
    world: WorldState,
    task_id: str,
    query: Fact,
    pattern: str,
    support: set[Fact],
    distractors: int,
    rules_used: int,
    override_answer: bool | str | None = None,
    intended_depth: int | None = None,
) -> Task:
    answer, inferred_depth = answer_query(world, query)
    if override_answer is not None:
        answer = override_answer
    if pattern == "contradiction" and contradictions(world):
        answer = True
    task = Task(
        world_id=world.world_id,
        task_id=task_id,
        facts=tuple(sorted(world.facts)),
        query=query,
        answer=answer,
        proof_depth=max(intended_depth if intended_depth is not None else inferred_depth, 0),
        reasoning_pattern=pattern,
        num_distractors=max(0, distractors),
        num_supporting_facts=len(support),
        num_irrelevant_facts=max(0, len(world.facts) - len(support)),
        num_predicates=len({fact.positive_predicate() for fact in world.facts} | {query.positive_predicate()}),
        num_entities=len(world.entities),
        num_inference_rules_used=rules_used,
    )
    task.canonical_world_hash = canonical_world_hash(world)
    task.canonical_task_hash = canonical_task_hash(task)
    return task


def _distractors(rng: random.Random, entities: tuple[Entity, ...], count: int) -> set[Fact]:
    facts = set()
    attempts = 0
    while len(facts) < count and attempts < count * 30:
        fact = random_valid_fact(rng, entities)
        if fact.predicate not in {"Before", "ParentOf", "PartOf", "LocatedIn", "Causes", "Knows"}:
            facts.add(fact)
        attempts += 1
    return facts
