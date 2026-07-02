from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from worldcore.types import Fact, Task, UNIVERSAL_RULES, WorldState


@dataclass(frozen=True)
class Derivation:
    conclusion: Fact
    premises: tuple[Fact, ...]
    rule: str


def fact_key(fact: Fact) -> str:
    return fact.to_text()


def _hash_payload(payload: object) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def extract_proof(world: WorldState, task: Task, proof_id: str | None = None) -> dict[str, object]:
    facts, depths, derivations = _traced_closure(world)
    answer, final = _final_conclusion(facts, task.query)
    proof_id = proof_id or _hash_payload([task.task_id, task.canonical_task_hash, fact_key(final) if final else "unknown"])
    chosen = _choose_derivations(final, derivations) if final is not None else {}
    reachable_derivations = _reachable_derivations(final, chosen) if final is not None else []
    reachable_facts = _reachable_facts(final, chosen) if final is not None else set()
    initial_facts = {fact for fact in reachable_facts if fact not in chosen}
    derived_facts = {derivation.conclusion for derivation in reachable_derivations}
    supporting = sorted(fact_key(fact) for fact in initial_facts)
    intermediates = sorted(fact_key(fact) for fact in derived_facts if final is None or fact != final)

    nodes: list[dict[str, object]] = []
    edges: list[dict[str, str]] = []
    for fact in sorted(reachable_facts, key=fact_key):
        role = "conclusion" if final == fact else ("lemma" if fact in derived_facts else "fact")
        nodes.append({"id": fact_key(fact), "kind": "fact", "label": fact_key(fact), "role": role})
    for idx, derivation in enumerate(reachable_derivations):
        inf_id = f"rule:{idx}:{derivation.rule}:{fact_key(derivation.conclusion)}"
        nodes.append({"id": inf_id, "kind": "inference", "label": derivation.rule, "role": "rule"})
        for premise in derivation.premises:
            edges.append({"source": fact_key(premise), "target": inf_id, "label": "derived_from"})
        edges.append({"source": inf_id, "target": fact_key(derivation.conclusion), "label": "concludes"})

    metrics = proof_metrics(world, task, final, chosen, derivations)
    proof = {
        "proof_id": proof_id,
        "world_id": world.world_id,
        "task_id": task.task_id,
        "answer": str(answer),
        "query": fact_key(task.query),
        "final_conclusion": fact_key(final) if final is not None else None,
        "proof_graph": {"nodes": nodes, "edges": edges},
        "proof_dag": {"nodes": nodes, "edges": edges},
        "rule_sequence": [derivation.rule for derivation in reachable_derivations],
        "supporting_facts": supporting,
        "intermediate_lemmas": intermediates,
        "metrics": metrics,
    }
    return proof


def write_proof(path: Path, proof: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proof, indent=2, sort_keys=True), encoding="utf-8")


def proof_metrics(
    world: WorldState,
    task: Task,
    final: Fact | None,
    chosen: dict[Fact, Derivation],
    all_derivations: dict[Fact, list[Derivation]],
) -> dict[str, float | int | str]:
    reachable_derivations = _reachable_derivations(final, chosen) if final is not None else []
    reachable_facts = _reachable_facts(final, chosen) if final is not None else set()
    length = len(reachable_derivations)
    fact_depths = _proof_fact_depths(final, chosen) if final is not None else {}
    inference_depths = []
    for derivation in reachable_derivations:
        premise_depth = max((fact_depths.get(premise, 0) for premise in derivation.premises), default=0)
        inference_depths.append(premise_depth + 1)
    depth = max(inference_depths, default=0)
    width = max(Counter(inference_depths).values(), default=0)
    fanins = [len(derivation.premises) for derivation in reachable_derivations]
    fact_to_inference_count: Counter[Fact] = Counter()
    children_per_inference = []
    for derivation in reachable_derivations:
        children_per_inference.append(1)
        for premise in derivation.premises:
            fact_to_inference_count[premise] += 1
    intermediate = {derivation.conclusion for derivation in reachable_derivations if derivation.conclusion != final}
    reuse = sum(1 for fact in intermediate if fact_to_inference_count[fact] > 1)
    fanout_values = [fact_to_inference_count[fact] for fact in reachable_facts if fact_to_inference_count[fact] > 0]
    alternatives = sum(max(0, len(all_derivations.get(derivation.conclusion, [])) - 1) for derivation in reachable_derivations)
    initial_count = max(1, len(world.facts) + len(world.entities))
    derived_fact_count = len({derivation.conclusion for derivation in all_derivations.values() for derivation in derivation})
    density = derived_fact_count / initial_count
    entropy = _rule_entropy([derivation.rule for derivation in reachable_derivations])
    shape = classify_proof_shape(length, depth, width, fanins, reuse, reachable_derivations)
    difficulty = difficulty_score(
        minimal_length=length,
        width=width,
        branching=_mean(children_per_inference),
        alternatives=alternatives,
        proof_entropy=entropy,
        reuse=reuse,
        fan_in=_mean(fanins),
    )
    return {
        "proof_id": "",
        "task_id": task.task_id,
        "reasoning_pattern": task.reasoning_pattern,
        "answer": str(task.answer),
        "length": length,
        "depth": depth,
        "width": width,
        "branching_factor": _mean(children_per_inference),
        "reuse": reuse,
        "fan_in": _mean(fanins),
        "fan_out": _mean(fanout_values),
        "alternative_proofs": alternatives,
        "proof_density": density,
        "minimal_proof_length": length,
        "proof_entropy": entropy,
        "difficulty": difficulty,
        "shape": shape,
        "canonical_proof_hash": canonical_proof_hash(final, chosen),
    }


def classify_proof_shape(
    length: int,
    depth: int,
    width: int,
    fanins: list[int],
    reuse: int,
    derivations: list[Derivation],
) -> str:
    if length == 0:
        return "NoProofOrAtomic"
    max_fanin = max(fanins, default=0)
    if reuse > 0:
        return "Diamond"
    if width >= 3 and depth <= 2:
        return "Star"
    if width > 1 and max_fanin > 1:
        return "Mixed"
    if width > 1:
        return "Fork"
    if max_fanin > 1:
        return "Merge"
    if length == depth:
        return "Linear chain"
    return "Mixed"


def canonical_proof_hash(final: Fact | None, chosen: dict[Fact, Derivation]) -> str:
    if final is None:
        return _hash_payload({"shape": "unknown"})
    derivations = _reachable_derivations(final, chosen)
    payload = []
    for derivation in derivations:
        payload.append(
            {
                "rule": derivation.rule,
                "premises": sorted(_fact_signature(fact) for fact in derivation.premises),
                "conclusion": _fact_signature(derivation.conclusion),
            }
        )
    return _hash_payload(sorted(payload, key=lambda item: json.dumps(item, sort_keys=True)))


def structural_vector(proof: dict[str, object]) -> dict[str, float]:
    metrics = proof["metrics"]
    return {
        "length": float(metrics["length"]),
        "depth": float(metrics["depth"]),
        "width": float(metrics["width"]),
        "branching": float(metrics["branching_factor"]),
        "reuse": float(metrics["reuse"]),
        "fan_in": float(metrics["fan_in"]),
        "fan_out": float(metrics["fan_out"]),
        "alternatives": float(metrics["alternative_proofs"]),
        "density": float(metrics["proof_density"]),
        "entropy": float(metrics["proof_entropy"]),
        "difficulty": float(metrics["difficulty"]),
    }


def proof_novelty_curve(proofs: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    rows = []
    for idx, proof in enumerate(proofs, start=1):
        value = str(proof["metrics"]["canonical_proof_hash"])
        before = len(seen)
        seen.add(value)
        rows.append({"generated": idx, "new": int(len(seen) > before), "unique": len(seen), "proof_novelty": len(seen) / idx})
    return rows


def shape_counts(proofs: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, float]]:
    counts = Counter(str(proof["metrics"]["shape"]) for proof in proofs)
    total = sum(counts.values())
    rows = []
    entropy = 0.0
    for shape, count in counts.most_common():
        pct = count / total if total else 0.0
        if pct:
            entropy -= pct * math.log2(pct)
        rows.append({"shape": shape, "count": count, "fraction": pct})
    largest = max((row["fraction"] for row in rows), default=0.0)
    return rows, {"largest_cluster_fraction": largest, "shape_entropy": entropy, "num_shapes": len(rows)}


def difficulty_score(
    minimal_length: int,
    width: int,
    branching: float,
    alternatives: int,
    proof_entropy: float,
    reuse: int,
    fan_in: float,
) -> float:
    components = [
        min(1.0, minimal_length / 8.0),
        min(1.0, width / 4.0),
        min(1.0, branching / 3.0),
        min(1.0, alternatives / 4.0),
        min(1.0, proof_entropy / 2.0),
        min(1.0, reuse / 3.0),
        min(1.0, fan_in / 3.0),
    ]
    return sum(components) / len(components)


def _traced_closure(world: WorldState, max_iterations: int = 20) -> tuple[set[Fact], dict[Fact, int], dict[Fact, list[Derivation]]]:
    facts = set(world.facts)
    depths: dict[Fact, int] = {fact: 0 for fact in facts}
    derivations: dict[Fact, list[Derivation]] = defaultdict(list)
    for entity in world.entities:
        type_fact = Fact(entity.type, (entity.id,))
        facts.add(type_fact)
        depths.setdefault(type_fact, 0)

    for _ in range(max_iterations):
        before = len(facts)
        _trace_universal(world, facts, depths, derivations)
        _trace_unary(facts, depths, derivations)
        _trace_binary(facts, depths, derivations)
        if len(facts) == before:
            break
    return facts, depths, derivations


def _add_derivation(
    facts: set[Fact],
    depths: dict[Fact, int],
    derivations: dict[Fact, list[Derivation]],
    conclusion: Fact,
    premises: tuple[Fact, ...],
    rule: str,
) -> None:
    depth = max((depths.get(premise, 0) for premise in premises), default=0) + 1
    candidate = Derivation(conclusion, tuple(sorted(premises)), rule)
    if candidate not in derivations[conclusion]:
        derivations[conclusion].append(candidate)
    if conclusion not in facts:
        facts.add(conclusion)
        depths[conclusion] = depth
    else:
        depths[conclusion] = min(depths.get(conclusion, depth), depth)


def _blocked(fact: Fact, facts: set[Fact]) -> bool:
    return fact.predicate.startswith("NOT_") or fact.negated() in facts


def _usable(fact: Fact, facts: set[Fact]) -> bool:
    return not _blocked(fact, facts)


def _trace_universal(world: WorldState, facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    for entity in world.entities:
        for rule in UNIVERSAL_RULES:
            if entity.type == rule.if_type:
                premise = Fact(rule.if_type, (entity.id,))
                _add_derivation(facts, depths, derivations, Fact(rule.then_predicate, (entity.id,)), (premise,), f"universal:{rule.if_type}->{rule.then_predicate}")


def _trace_unary(facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    for fact in list(facts):
        if _blocked(fact, facts):
            continue
        if fact.predicate == "Feeds":
            _add_derivation(facts, depths, derivations, Fact("Helps", fact.args), (fact,), "implication:Feeds->Helps")
        elif fact.predicate == "Knows":
            _add_derivation(facts, depths, derivations, Fact("Believes", fact.args), (fact,), "implication:Knows->Believes")


def _trace_binary(facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    by_pred: dict[str, list[Fact]] = defaultdict(list)
    for fact in facts:
        if not fact.predicate.startswith("NOT_"):
            by_pred[fact.predicate].append(fact)
    _trace_parent(by_pred, facts, depths, derivations)
    _trace_transitive("Before", by_pred, facts, depths, derivations)
    _trace_transitive("PartOf", by_pred, facts, depths, derivations)
    _trace_located(by_pred, facts, depths, derivations)
    _trace_access(by_pred, facts, depths, derivations)
    _trace_part_location(by_pred, facts, depths, derivations)
    _trace_causal_temporal(by_pred, facts, depths, derivations)


def _trace_parent(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    edges = by_pred.get("ParentOf", []) + by_pred.get("AncestorOf", [])
    for left in edges:
        for right in edges:
            if _usable(left, facts) and _usable(right, facts) and left.args[1] == right.args[0] and left.args[0] != right.args[1]:
                _add_derivation(facts, depths, derivations, Fact("AncestorOf", (left.args[0], right.args[1])), (left, right), "transitivity:ParentOf/AncestorOf")


def _trace_transitive(predicate: str, by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    for left in by_pred.get(predicate, []):
        for right in by_pred.get(predicate, []):
            if _usable(left, facts) and _usable(right, facts) and left.args[1] == right.args[0] and left.args[0] != right.args[1]:
                _add_derivation(facts, depths, derivations, Fact(predicate, (left.args[0], right.args[1])), (left, right), f"transitivity:{predicate}")


def _trace_located(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    for left in by_pred.get("LocatedIn", []):
        for right in by_pred.get("LocatedIn", []):
            if _usable(left, facts) and _usable(right, facts) and left.args[1] == right.args[0] and left.args[0] != right.args[1]:
                _add_derivation(facts, depths, derivations, Fact("LocatedIn", (left.args[0], right.args[1])), (left, right), "transitivity:LocatedIn")


def _trace_access(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    uses = {(fact.args[0], fact.args[1]): fact for fact in by_pred.get("Uses", []) if _usable(fact, facts)}
    for owns in by_pred.get("Owns", []):
        if not _usable(owns, facts):
            continue
        uses_fact = uses.get((owns.args[0], owns.args[1]))
        if uses_fact:
            _add_derivation(facts, depths, derivations, Fact("HasAccessTo", owns.args), (owns, uses_fact), "implication:Owns+Uses->HasAccessTo")


def _trace_part_location(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    for part in by_pred.get("PartOf", []):
        for located in by_pred.get("LocatedIn", []):
            if _usable(part, facts) and _usable(located, facts) and part.args[1] == located.args[0]:
                _add_derivation(facts, depths, derivations, Fact("LocatedIn", (part.args[0], located.args[1])), (part, located), "mixed:PartOf+LocatedIn->LocatedIn")


def _trace_causal_temporal(by_pred: dict[str, list[Fact]], facts: set[Fact], depths: dict[Fact, int], derivations: dict[Fact, list[Derivation]]) -> None:
    for cause in by_pred.get("Causes", []):
        for before in by_pred.get("Before", []):
            if _usable(cause, facts) and _usable(before, facts) and cause.args[1] == before.args[0]:
                _add_derivation(facts, depths, derivations, Fact("Before", (cause.args[0], before.args[1])), (cause, before), "mixed:Causes+Before->Before")


def _final_conclusion(facts: set[Fact], query: Fact) -> tuple[bool | str, Fact | None]:
    negated = query.negated()
    if query.predicate.startswith("NOT_"):
        if query in facts:
            return True, query
        if negated in facts:
            return False, negated
        return "unknown", None
    if negated in facts:
        return False, negated
    if query in facts:
        return True, query
    return "unknown", None


def _choose_derivations(final: Fact | None, derivations: dict[Fact, list[Derivation]]) -> dict[Fact, Derivation]:
    chosen: dict[Fact, Derivation] = {}
    visiting: set[Fact] = set()

    def choose(fact: Fact) -> None:
        if fact in chosen or fact in visiting or fact not in derivations:
            return
        visiting.add(fact)
        options = sorted(derivations[fact], key=lambda item: (len(item.premises), item.rule, tuple(fact_key(p) for p in item.premises)))
        derivation = options[0]
        chosen[fact] = derivation
        for premise in derivation.premises:
            choose(premise)
        visiting.remove(fact)

    if final is not None:
        choose(final)
    return chosen


def _reachable_derivations(final: Fact | None, chosen: dict[Fact, Derivation]) -> list[Derivation]:
    if final is None:
        return []
    ordered: list[Derivation] = []
    seen: set[Fact] = set()

    def visit(fact: Fact) -> None:
        if fact in seen:
            return
        seen.add(fact)
        derivation = chosen.get(fact)
        if derivation is None:
            return
        for premise in derivation.premises:
            visit(premise)
        ordered.append(derivation)

    visit(final)
    return ordered


def _reachable_facts(final: Fact | None, chosen: dict[Fact, Derivation]) -> set[Fact]:
    if final is None:
        return set()
    facts = {final}
    queue = deque([final])
    while queue:
        fact = queue.popleft()
        derivation = chosen.get(fact)
        if derivation is None:
            continue
        for premise in derivation.premises:
            if premise not in facts:
                facts.add(premise)
                queue.append(premise)
    return facts


def _proof_fact_depths(final: Fact | None, chosen: dict[Fact, Derivation]) -> dict[Fact, int]:
    depths: dict[Fact, int] = {}
    visiting: set[Fact] = set()

    def depth(fact: Fact) -> int:
        if fact in depths:
            return depths[fact]
        if fact in visiting:
            return 0
        visiting.add(fact)
        derivation = chosen.get(fact)
        if derivation is None:
            value = 0
        else:
            value = max((depth(premise) for premise in derivation.premises), default=0) + 1
        visiting.remove(fact)
        depths[fact] = value
        return value

    if final is not None:
        depth(final)
    return depths


def _rule_entropy(rules: list[str]) -> float:
    total = len(rules)
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in Counter(rules).values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def _fact_signature(fact: Fact) -> tuple[str, int]:
    return (fact.predicate, len(fact.args))


def _mean(values: Iterable[float | int]) -> float:
    values = list(values)
    return sum(float(value) for value in values) / len(values) if values else 0.0



def closure_audit(world: WorldState) -> dict[str, object]:
    facts, depths, derivations = _traced_closure(world)
    initial = set(world.facts) | {Fact(entity.type, (entity.id,)) for entity in world.entities}
    derived = facts - initial
    rule_applications = []
    nodes = []
    edges = []
    for fact in sorted(facts, key=fact_key):
        nodes.append(
            {
                "id": fact_key(fact),
                "kind": "fact",
                "label": fact_key(fact),
                "role": "initial" if fact in initial else "derived",
                "depth": depths.get(fact, 0),
            }
        )
    app_idx = 0
    for conclusion, options in sorted(derivations.items(), key=lambda item: fact_key(item[0])):
        for derivation in options:
            app_id = f"rule:{app_idx}:{derivation.rule}:{fact_key(conclusion)}"
            rule_applications.append(
                {
                    "id": app_id,
                    "rule": derivation.rule,
                    "premises": [fact_key(fact) for fact in derivation.premises],
                    "conclusion": fact_key(conclusion),
                }
            )
            nodes.append({"id": app_id, "kind": "inference", "label": derivation.rule})
            for premise in derivation.premises:
                edges.append({"source": fact_key(premise), "target": app_id, "label": "derivable_by_rule"})
            edges.append({"source": app_id, "target": fact_key(conclusion), "label": "concludes"})
            app_idx += 1
    return {
        "world_id": world.world_id,
        "initial_facts": sorted(fact_key(fact) for fact in initial),
        "derived_facts": sorted(fact_key(fact) for fact in derived),
        "closure_facts": sorted(fact_key(fact) for fact in facts),
        "rule_applications": rule_applications,
        "derivation_graph": {"nodes": nodes, "edges": edges},
        "initial_fact_count": len(initial),
        "derived_fact_count": len(derived),
        "closure_size": len(facts),
        "closure_expansion_ratio": len(derived) / max(1, len(initial)),
    }


def proof_opportunities_for_world(world: WorldState) -> list[dict[str, object]]:
    _, _, derivations = _traced_closure(world)
    opportunities = []
    for conclusion, options in sorted(derivations.items(), key=lambda item: fact_key(item[0])):
        for idx, derivation in enumerate(sorted(options, key=lambda item: (item.rule, tuple(fact_key(p) for p in item.premises)))):
            chosen = _choose_derivations(conclusion, derivations)
            chosen[conclusion] = derivation
            task = Task(
                world_id=world.world_id,
                task_id=f"opportunity:{world.world_id}:{fact_key(conclusion)}:{idx}",
                facts=tuple(sorted(world.facts)),
                query=conclusion,
                answer=True,
                proof_depth=0,
                reasoning_pattern=reasoning_family_from_rule(derivation.rule),
            )
            metrics = proof_metrics(world, task, conclusion, chosen, derivations)
            opportunity_id = _hash_payload([world.world_id, fact_key(conclusion), idx, derivation.rule, [fact_key(p) for p in derivation.premises]])
            opportunities.append(
                {
                    "world_id": world.world_id,
                    "opportunity_id": opportunity_id,
                    "goal_fact": fact_key(conclusion),
                    "rule": derivation.rule,
                    "reasoning_family": reasoning_family_from_rule(derivation.rule),
                    "premises": ";".join(fact_key(fact) for fact in derivation.premises),
                    "proof_shape": metrics["shape"],
                    "proof_length": metrics["length"],
                    "proof_depth": metrics["depth"],
                    "proof_alternatives": metrics["alternative_proofs"],
                    "canonical_proof_hash": metrics["canonical_proof_hash"],
                    "difficulty": metrics["difficulty"],
                }
            )
    return opportunities


def reasoning_family_from_rule(rule: str) -> str:
    lower = rule.lower()
    if "transitivity" in lower:
        return "transitivity"
    if "feeds" in lower or "owns" in lower or "uses" in lower:
        return "implication"
    if "knows" in lower or "believes" in lower:
        return "belief"
    if "causes" in lower or "before" in lower and "mixed" in lower:
        return "causal"
    if "partof" in lower or "locatedin" in lower:
        return "part-of"
    if "not_" in lower or "neg" in lower:
        return "negation"
    if "mixed" in lower:
        return "mixed"
    if "universal" in lower:
        return "implication"
    return "mixed"
