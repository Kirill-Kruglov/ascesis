"""Experiment 15.2 — enumeration to exhaustion (System C only).

Two instruments over the SAME System C (only the `G_expand` depth cap is
parameterized — the rewrite framework is untouched):

1. ``state_bfs`` — the literally-prescribed full reachable-state BFS. It records
   the cumulative distinct semantic classes (normal forms) and syntactic shapes
   per expansion layer, and whether the cap reached true exhaustion (frontier
   emptied below budget) or was censored (hit the node budget). On System C this
   censors almost immediately: the reachable *state* space is doubly-exponential
   in the cap (a blow-up of syntactic intermediate F-trees), even though the
   *semantic* space is tiny.

2. ``exact_normal_forms`` / ``prefix_layers`` — the correct instrument. Because
   the only collapsing redexes discard context (``NF(F(p,q)) = NF(p) ∪ NF(q)``),
   the reachable normal-form set is enumerable EXACTLY and cheaply without ever
   materializing the F-intermediates that explode the state BFS. This exhausts
   the *semantic* space (no budget, no censoring) and yields the true,
   uncensored ``N_semantic(cap)``.

Nothing here samples; everything is deterministic and exact.
"""
from __future__ import annotations

from collapse_boundary.explore import observation_prefix
from collapse_boundary.systems import build_collapsing_system
from collapse_boundary.types import Term

CANONICAL_SEED = "x0"


def start_term() -> Term:
    """The canonical initial term that generates System C's whole reachable space."""
    return Term("G", (Term(CANONICAL_SEED),))


def semantic_key(term: Term, system, obs_depth: int) -> str:
    """15.0.1 semantic-class proxy applied to a single state: normal forms key on
    their shape (obs-independent); non-terminal states key on a bounded-depth
    observation prefix."""
    if not system.rewrites(term):
        return "NF:" + term.shape()
    return "OBS:" + observation_prefix(term, obs_depth)


# --------------------------------------------------------------------------- #
# Instrument 1: the prescribed full reachable-state BFS (demonstrates censoring)
# --------------------------------------------------------------------------- #
def state_bfs(
    cap: int,
    node_budget: int,
    obs_depth: int = 12,
    k_exhaust: int = 3,
    exhaustion_frac: float = 0.5,
) -> dict[str, object]:
    system = build_collapsing_system(cap)
    start = start_term()
    seen = {start.serialize()}
    frontier = [start]
    nf_classes: set[str] = set()
    shapes: set[str] = {start.shape()}
    if not system.rewrites(start):
        nf_classes.add(start.shape())

    by_layer = [{"layer": 0, "cum_states": len(seen), "cum_nf_classes": len(nf_classes), "cum_shapes": len(shapes)}]
    censored = False
    layer = 0
    while frontier:
        layer += 1
        nxt = []
        for term in frontier:
            for step in system.rewrites(term):
                key = step.after.serialize()
                if key not in seen:
                    seen.add(key)
                    nxt.append(step.after)
                    shapes.add(step.after.shape())
                    if not system.rewrites(step.after):
                        nf_classes.add(step.after.shape())
                    if len(seen) >= node_budget:
                        censored = True
                        break
            if censored:
                break
        by_layer.append({"layer": layer, "cum_states": len(seen), "cum_nf_classes": len(nf_classes), "cum_shapes": len(shapes)})
        if censored:
            break
        frontier = nxt

    # Sustained plateau of the semantic count over the last k_exhaust layers.
    tail = [row["cum_nf_classes"] for row in by_layer[-k_exhaust:]]
    flat_tail = len(tail) >= k_exhaust and len(set(tail)) == 1
    frontier_emptied = not censored
    below_frac = len(seen) < exhaustion_frac * node_budget
    exhausted = frontier_emptied and flat_tail and below_frac

    return {
        "cap": cap,
        "instrument": "state_bfs",
        "exhausted": exhausted,
        "censored": censored,
        "frontier_emptied": frontier_emptied,
        "n_semantic_final": len(nf_classes),
        "n_term_shapes_final": len(shapes),
        "nodes_expanded": len(seen),
        "layers": layer,
        "by_layer": by_layer,
        "node_budget": node_budget,
    }


# --------------------------------------------------------------------------- #
# Instrument 2: exact semantic-space enumeration (uncensored)
# --------------------------------------------------------------------------- #
def exact_normal_forms(cap: int) -> dict[str, object]:
    """Exact set of reachable normal-form shapes (= semantic classes) for System C
    at a given cap, via memoized reachability that follows only the
    completeness-preserving reducts (size-reducing collapses, else the single
    expansion). Never materializes the exploding F-intermediates."""
    system = build_collapsing_system(cap)
    memo: dict[str, frozenset[str]] = {}

    def nf(term: Term) -> frozenset[str]:
        key = term.serialize()
        cached = memo.get(key)
        if cached is not None:
            return cached
        steps = system.rewrites(term)
        if not steps:
            result: frozenset[str] = frozenset({term.shape()})
        else:
            reducing = [s for s in steps if s.after.size() < term.size()]
            chosen = reducing if reducing else steps
            acc: set[str] = set()
            for s in chosen:
                acc |= nf(s.after)
            result = frozenset(acc)
        memo[key] = result
        return result

    classes = nf(start_term())
    return {
        "cap": cap,
        "instrument": "exact_semantic",
        "exhausted": True,         # exact set; no budget, no censoring
        "censored": False,
        "n_semantic_final": len(classes),
        "memo_states_touched": len(memo),
    }


def prefix_layers(cap: int, obs_depth: int) -> dict[str, object]:
    """Layer-by-layer cumulative semantic-class curve for one cap, walking the
    deduplicated partial-meaning prefix tree G(w) -> {G(aw), G(bw)} until the
    frontier empties (every prefix has become a terminal normal form). Frontier
    emptying = genuine exhaustion of the semantic space."""
    system = build_collapsing_system(cap)
    frontier = [start_term()]
    seen_prefixes = {start_term().serialize()}
    cum_classes: set[str] = set()
    cum_nf: set[str] = set()
    by_layer = []
    layer = 0
    while frontier:
        nf_here = 0
        for term in frontier:
            cum_classes.add(semantic_key(term, system, obs_depth))
            if not system.rewrites(term):
                cum_nf.add(term.shape())
                nf_here += 1
        by_layer.append({
            "layer": layer,
            "frontier_size": len(frontier),
            "cum_semantic_classes": len(cum_classes),
            "cum_normal_forms": len(cum_nf),
            "terminal_in_layer": nf_here,
        })
        nxt = []
        for term in frontier:
            steps = system.rewrites(term)
            if not steps:
                continue  # terminal prefix (normal form): no children
            expand = [s for s in steps if s.after.size() > term.size()]
            if not expand:
                continue
            f_term = expand[0].after
            for child_step in system.rewrites(f_term):
                if child_step.after.size() < f_term.size():
                    k = child_step.after.serialize()
                    if k not in seen_prefixes:
                        seen_prefixes.add(k)
                        nxt.append(child_step.after)
        frontier = nxt
        layer += 1

    return {
        "cap": cap,
        "obs_depth": obs_depth,
        "exhausted": True,  # frontier emptied
        "layers": len(by_layer),
        "by_layer": by_layer,
        "n_semantic_final": len(cum_nf),
        "n_semantic_classes_with_prefixes": len(cum_classes),
    }
