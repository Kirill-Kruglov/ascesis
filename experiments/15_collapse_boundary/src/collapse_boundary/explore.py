from __future__ import annotations

import gzip
import json
import random
from collections import Counter
from dataclasses import dataclass

from collapse_boundary.types import RewriteStep, RewriteSystem, Term


@dataclass
class Trajectory:
    initial: Term
    terms: list[Term]
    rules: list[str]
    collapsing_steps: int
    terminated: bool

    @property
    def final(self) -> Term:
        return self.terms[-1]

    def serialize(self) -> str:
        return " -> ".join(term.serialize() for term in self.terms)

    def canonical_shape(self) -> str:
        return " -> ".join(term.shape() for term in self.terms)

    def rule_shape(self) -> str:
        return ";".join(self.rules) if self.rules else "NORMAL"


def random_trajectory(system: RewriteSystem, initial: Term, horizon: int, rng: random.Random) -> Trajectory:
    terms = [initial]
    rules: list[str] = []
    collapsing = 0
    current = initial
    terminated = False
    for _ in range(horizon):
        steps = system.rewrites(current)
        if not steps:
            terminated = True
            break
        step = rng.choice(steps)
        current = step.after
        terms.append(current)
        rules.append(step.rule_name)
        collapsing += int(step.collapsing)
    else:
        terminated = len(system.rewrites(current)) == 0
    return Trajectory(initial, terms, rules, collapsing, terminated)


def limited_reachable(system: RewriteSystem, initial: Term, horizon: int, max_nodes: int = 256) -> tuple[set[Term], list[tuple[Term, Term, str]]]:
    seen = {initial}
    frontier = [initial]
    edges: list[tuple[Term, Term, str]] = []
    for _ in range(horizon):
        next_frontier = []
        for term in frontier:
            for step in system.rewrites(term)[:16]:
                edges.append((term, step.after, step.rule_name))
                if step.after not in seen and len(seen) < max_nodes:
                    seen.add(step.after)
                    next_frontier.append(step.after)
        if not next_frontier or len(seen) >= max_nodes:
            break
        frontier = next_frontier
    return seen, edges


def is_normal(system: RewriteSystem, term: Term) -> bool:
    return not system.rewrites(term)


def entropy(values: list[str]) -> float:
    import math

    counts = Counter(values)
    total = len(values)
    if total == 0:
        return 0.0
    out = 0.0
    for count in counts.values():
        p = count / total
        if p:
            out -= p * math.log2(p)
    return out


def compression_stats(strings: list[str]) -> dict[str, float]:
    raw = "\n".join(strings).encode("utf-8")
    comp = gzip.compress(raw)
    ratio = len(comp) / max(1, len(raw))
    return {"raw_size": len(raw), "compressed_size": len(comp), "compression_ratio": ratio}


def term_features(term: Term) -> dict[str, float]:
    counts: Counter[str] = Counter()

    def walk(t: Term) -> None:
        counts[f"sym:{t.symbol}"] += 1
        counts[f"arity:{len(t.children)}"] += 1
        for child in t.children:
            walk(child)

    walk(term)
    counts["size"] = term.size()
    counts["depth"] = term.depth()
    return dict(counts)


def trajectory_features(traj: Trajectory) -> dict[str, float]:
    counts = Counter(f"rule:{rule}" for rule in traj.rules)
    counts.update({f"top:{term.top()}": 1 for term in traj.terms})
    counts["length"] = len(traj.rules)
    counts["collapsing_steps"] = traj.collapsing_steps
    counts["terminated"] = int(traj.terminated)
    counts["initial_size"] = traj.initial.size()
    counts["final_size"] = traj.final.size()
    counts["size_delta"] = traj.final.size() - traj.initial.size()
    return dict(counts)


def canonical_term(term: Term) -> str:
    return term.shape()


def canonical_trajectory(traj: Trajectory) -> str:
    return traj.canonical_shape() + " :: " + traj.rule_shape()


def observation_prefix(term: Term, depth: int) -> str:
    """Böhm-tree-like bounded observation: the structural shape of `term` truncated
    to `depth` levels, with anything deeper replaced by `*`. Leaf identities are
    erased (`_`) so this captures observable behavior, not input variable names.
    Depth 0 observes nothing (`*`)."""
    if depth <= 0:
        return "*"
    if not term.children:
        return "_"
    return term.symbol + "(" + ",".join(observation_prefix(child, depth - 1) for child in term.children) + ")"


def semantic_class(traj: Trajectory, obs_depth: int) -> str:
    """Cheap semantic-equivalence key for a trajectory, using ONLY what the system
    already exposes (no invented semantics):
      - terminating trajectory: its normal form (two terms sharing a normal form are
        semantically equivalent);
      - non-terminating trajectory: a bounded-depth observation prefix of the final
        term (two trajectories with the same depth-d observable prefix are equivalent).
    """
    if traj.terminated:
        return "NF:" + traj.final.shape()
    return "OBS:" + observation_prefix(traj.final, obs_depth)


def label_class(traj: Trajectory) -> str:
    """Alternative semantic proxy (defect-3 option 3): quotient a trajectory by its
    sequence of rule labels (operation / proof-step types the system already carries)."""
    return traj.rule_shape()
