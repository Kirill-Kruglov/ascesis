from __future__ import annotations

from collections import defaultdict, deque

from worldcore.types import Fact, UNIVERSAL_RULES, WorldState


def closure(world: WorldState, max_iterations: int = 20) -> tuple[frozenset[Fact], dict[Fact, int]]:
    facts = set(world.facts)
    depths: dict[Fact, int] = {fact: 0 for fact in facts}

    for entity in world.entities:
        type_fact = Fact(entity.type, (entity.id,))
        facts.add(type_fact)
        depths.setdefault(type_fact, 0)

    for _ in range(max_iterations):
        before = len(facts)
        _apply_universal_rules(world, facts, depths)
        _apply_unary_implications(facts, depths)
        _apply_binary_rules(facts, depths)
        if len(facts) == before:
            break
    return frozenset(facts), depths


def answer_query(world: WorldState, query: Fact) -> tuple[bool | str, int]:
    closed, depths = closure(world)
    negated = query.negated()
    if query.predicate.startswith("NOT_"):
        if query in closed:
            return True, depths.get(query, 0)
        if negated in closed:
            return False, depths.get(negated, 0)
        return "unknown", -1
    if negated in closed:
        return False, depths.get(negated, 0)
    if query in closed:
        return True, depths.get(query, 0)
    return "unknown", -1


def contradictions(world: WorldState) -> list[tuple[Fact, Fact]]:
    closed, _ = closure(world)
    pairs = []
    for fact in closed:
        if fact.predicate.startswith("NOT_"):
            continue
        negated = fact.negated()
        if negated in closed:
            pairs.append((fact, negated))
    return sorted(pairs, key=lambda pair: pair[0].to_text())


def _add_fact(facts: set[Fact], depths: dict[Fact, int], fact: Fact, depth: int) -> None:
    if fact not in facts:
        facts.add(fact)
        depths[fact] = depth
    else:
        depths[fact] = min(depths.get(fact, depth), depth)


def _is_blocked(fact: Fact, facts: set[Fact]) -> bool:
    return fact.predicate.startswith("NOT_") or fact.negated() in facts


def _apply_universal_rules(world: WorldState, facts: set[Fact], depths: dict[Fact, int]) -> None:
    for entity in world.entities:
        for rule in UNIVERSAL_RULES:
            if entity.type == rule.if_type:
                premise = Fact(rule.if_type, (entity.id,))
                _add_fact(facts, depths, Fact(rule.then_predicate, (entity.id,)), depths.get(premise, 0) + 1)


def _apply_unary_implications(facts: set[Fact], depths: dict[Fact, int]) -> None:
    for fact in list(facts):
        if _is_blocked(fact, facts):
            continue
        if fact.predicate == "Feeds":
            _add_fact(facts, depths, Fact("Helps", fact.args), depths[fact] + 1)
        elif fact.predicate == "Knows":
            _add_fact(facts, depths, Fact("Believes", fact.args), depths[fact] + 1)


def _apply_binary_rules(facts: set[Fact], depths: dict[Fact, int]) -> None:
    by_pred: dict[str, list[Fact]] = defaultdict(list)
    for fact in facts:
        if not fact.predicate.startswith("NOT_"):
            by_pred[fact.predicate].append(fact)

    _transitive_parent(by_pred, facts, depths)
    _transitive_same_predicate("Before", by_pred, facts, depths)
    _transitive_same_predicate("PartOf", by_pred, facts, depths)
    _located_in_chain(by_pred, facts, depths)
    _access_rule(by_pred, facts, depths)
    _part_location_rule(by_pred, facts, depths)
    _causal_temporal_rule(by_pred, facts, depths)


def _usable(fact: Fact, facts: set[Fact]) -> bool:
    return not _is_blocked(fact, facts)


def _transitive_parent(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int]) -> None:
    edges = by_pred.get("ParentOf", []) + by_pred.get("AncestorOf", [])
    for left in edges:
        for right in edges:
            if not (_usable(left, facts) and _usable(right, facts)):
                continue
            if left.args[1] == right.args[0] and left.args[0] != right.args[1]:
                depth = max(depths[left], depths[right]) + 1
                _add_fact(facts, depths, Fact("AncestorOf", (left.args[0], right.args[1])), depth)


def _transitive_same_predicate(predicate: str, by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int]) -> None:
    for left in by_pred.get(predicate, []):
        for right in by_pred.get(predicate, []):
            if not (_usable(left, facts) and _usable(right, facts)):
                continue
            if left.args[1] == right.args[0] and left.args[0] != right.args[1]:
                depth = max(depths[left], depths[right]) + 1
                _add_fact(facts, depths, Fact(predicate, (left.args[0], right.args[1])), depth)


def _located_in_chain(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int]) -> None:
    for left in by_pred.get("LocatedIn", []):
        for right in by_pred.get("LocatedIn", []):
            if not (_usable(left, facts) and _usable(right, facts)):
                continue
            if left.args[1] == right.args[0] and left.args[0] != right.args[1]:
                depth = max(depths[left], depths[right]) + 1
                _add_fact(facts, depths, Fact("LocatedIn", (left.args[0], right.args[1])), depth)


def _access_rule(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int]) -> None:
    uses = {(fact.args[0], fact.args[1]): fact for fact in by_pred.get("Uses", []) if _usable(fact, facts)}
    for owns in by_pred.get("Owns", []):
        if not _usable(owns, facts):
            continue
        uses_fact = uses.get((owns.args[0], owns.args[1]))
        if uses_fact:
            depth = max(depths[owns], depths[uses_fact]) + 1
            _add_fact(facts, depths, Fact("HasAccessTo", owns.args), depth)


def _part_location_rule(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int]) -> None:
    for part in by_pred.get("PartOf", []):
        for located in by_pred.get("LocatedIn", []):
            if not (_usable(part, facts) and _usable(located, facts)):
                continue
            if part.args[1] == located.args[0]:
                depth = max(depths[part], depths[located]) + 1
                _add_fact(facts, depths, Fact("LocatedIn", (part.args[0], located.args[1])), depth)


def _causal_temporal_rule(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int]) -> None:
    for cause in by_pred.get("Causes", []):
        for before in by_pred.get("Before", []):
            if not (_usable(cause, facts) and _usable(before, facts)):
                continue
            if cause.args[1] == before.args[0]:
                depth = max(depths[cause], depths[before]) + 1
                _add_fact(facts, depths, Fact("Before", (cause.args[0], before.args[1])), depth)


def shortest_proof_depth(world: WorldState, query: Fact) -> int:
    answer, depth = answer_query(world, query)
    return depth if answer is True else -1


def reachable_nodes(edges: list[tuple[int, int]], start: int) -> set[int]:
    graph: dict[int, set[int]] = defaultdict(set)
    for src, dst in edges:
        graph[src].add(dst)
    seen = {start}
    queue: deque[int] = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen
