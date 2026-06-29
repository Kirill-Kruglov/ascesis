"""Experiment 18.0 — shield synthesis for the justitia collapse boundary.

We abstract the justitia coupling (scales gated by sword) into a 2-counter
monotone transition system on N^2 = (c, a):

  c = concentration level   (abstracts resource_hhi / capture concentration)
  a = accumulated harm / welfare-deficit  (abstracts the collapse-driving
       degradation: higher a = lower welfare; a >= A_collapse == collapse)

Unsafe set  U = { a >= A_collapse }  — upward-closed in the natural "badness"
order (componentwise <= on (c, a)), because the justitia collapse predicate
`mean(zone_welfare) < 0.32 or (#zones<0.20) >= 4 or total_mass < 35` is a
monotone Boolean combination of threshold tests on degradation coordinates.

Dynamics, one round:
  * adversary `accumulate` (uncontrollable): (c, a) -> (c+1, a+K).
       Concentration rises and drives harm up by K. Monotone (constant delta).
  * referee `sword` (controllable, consequence-gated by a >= trig):
       - bounded reaction:   (c, a) -> (c - Rc, a - Ra)   [floored at 0]
            constant delta -> MONOTONE -> WSTS -> coverability decidable.
       - unbounded reaction: (c, a) -> (c - Rc, a - c)     [floored at 0]
            harm cut by the concentration coordinate (unbounded) -> NON-MONOTONE.
       - none (scales-only control): no sword transition at all.

The safety game: adversary always accumulates; the referee may then react (if
gated). A state is `doomed` if the adversary forces reaching U no matter what
the referee does. Backward reachability computes the doomed set; the shield is,
at each safe state, the referee action that keeps the next state out of doom.

This file is pure (no I/O, no justitia import) so the monotonicity logic is unit
-testable against hand-built bounded / unbounded reactions.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShieldParams:
    A_collapse: int          # a >= A_collapse  is collapse (unsafe)
    trig: int                # sword gate: reacts only when a >= trig
    K: int = 1               # harm growth per accumulate step
    Rc: int = 1              # concentration reduction by a reaction
    Ra: int = 2              # harm reduction by a BOUNDED reaction
    Cmax: int = 60           # grid bound on concentration (for explicit backward pass)
    Amax: int = 60           # grid bound on harm
    iter_cap: int = 10_000   # backward-iteration safety cap


def accumulate(c: int, a: int, p: ShieldParams) -> tuple[int, int]:
    return c + 1, a + p.K


def gated(c: int, a: int, p: ShieldParams) -> bool:
    return a >= p.trig


def react(c: int, a: int, p: ShieldParams, mode: str) -> tuple[int, int]:
    """Referee corrective reaction. `mode` selects the reaction shape."""
    if mode == "bounded":
        return max(0, c - p.Rc), max(0, a - p.Ra)
    if mode == "unbounded":
        # harm cut by the (unbounded) concentration coordinate -> non-monotone
        return max(0, c - p.Rc), max(0, a - c)
    raise ValueError(mode)


def is_monotone_reaction(p: ShieldParams, mode: str, c_lo: int = 0, c_hi: int = 40,
                         a_lo: int = 0, a_hi: int = 40) -> dict:
    """WSTS monotonicity test on the reaction transition: for all gated s <= s',
    is react(s) <= react(s')? Returns fraction-monotone, counterexamples, and the
    distribution of reaction magnitudes (to show bounded vs unbounded)."""
    pairs = 0
    monotone = 0
    counterexamples = []
    magnitudes = []
    states = [(c, a) for c in range(c_lo, c_hi + 1) for a in range(a_lo, a_hi + 1)]
    for (c, a) in states:
        if not gated(c, a, p):
            continue
        rc, ra = react(c, a, p, mode)
        magnitudes.append((c - rc) + (a - ra))  # total harm/conc removed in one step
        for (c2, a2) in states:
            if not gated(c2, a2, p):
                continue
            if c <= c2 and a <= a2:  # s <= s'
                pairs += 1
                rc2, ra2 = react(c2, a2, p, mode)
                if rc <= rc2 and ra <= ra2:
                    monotone += 1
                elif len(counterexamples) < 12:
                    counterexamples.append({
                        "s": [c, a], "s_prime": [c2, a2],
                        "react_s": [rc, ra], "react_s_prime": [rc2, ra2],
                    })
    frac = monotone / pairs if pairs else 1.0
    return {
        "mode": mode,
        "pairs_tested": pairs,
        "fraction_monotone": frac,
        "monotone": frac >= 1.0 - 1e-12,
        "reaction_magnitude_max": max(magnitudes) if magnitudes else 0,
        "reaction_magnitude_mean": (sum(magnitudes) / len(magnitudes)) if magnitudes else 0.0,
        "reaction_bounded": (max(magnitudes) <= (p.Rc + p.Ra)) if magnitudes else True,
        "counterexamples": counterexamples,
    }


def compute_doomed(p: ShieldParams, mode: str) -> dict:
    """Backward safety-game fixpoint on the explicit grid [0..Cmax] x [0..Amax].

    D (doomed) = least set containing U and closed under: a state is doomed if,
    after the adversary's forced accumulate, EVERY referee option lands in D.
    Returns the doomed set, iterations to fixpoint, whether the fixpoint was
    reached within the cap, and the minimal-element basis (antichain) of D.
    """
    Cmax, Amax = p.Cmax, p.Amax
    grid = [(c, a) for c in range(Cmax + 1) for a in range(Amax + 1)]
    doomed = {(c, a) for (c, a) in grid if a >= p.A_collapse}

    iters = 0
    fixpoint = False
    while True:
        iters += 1
        added = False
        for (c, a) in grid:
            if (c, a) in doomed:
                continue
            ac, aa = accumulate(c, a, p)
            ac, aa = min(ac, Cmax), min(aa, Amax)  # clamp into grid
            options = [(ac, aa)]
            if gated(ac, aa, p) and mode in ("bounded", "unbounded"):
                rc, ra = react(ac, aa, p, mode)
                options.append((min(rc, Cmax), min(ra, Amax)))
            if all(o in doomed for o in options):
                doomed.add((c, a))
                added = True
        if not added:
            fixpoint = True
            break
        if iters >= p.iter_cap:
            break

    basis = minimal_basis(doomed)
    total = len(grid)
    return {
        "mode": mode,
        "iterations": iters,
        "fixpoint_reached": fixpoint,
        "doomed_size": len(doomed),
        "safe_size": total - len(doomed),
        "grid_size": total,
        "doomed_fraction": len(doomed) / total,
        "basis_size": len(basis),
        "basis": sorted(basis),
        "doomed": doomed,
    }


def minimal_basis(points: set[tuple[int, int]]) -> list[tuple[int, int]]:
    """Minimal elements (antichain) of an upward-closed-ish set under componentwise <=."""
    pts = sorted(points)
    basis = []
    for q in pts:
        if not any(b[0] <= q[0] and b[1] <= q[1] for b in basis):
            basis.append(q)
    return basis


def pre_preserves_upward_closure(p: ShieldParams, mode: str,
                                 c_hi: int = 50, a_hi: int = 50) -> dict:
    """The load-bearing WSTS decidability invariant: backward coverability requires
    that the predecessor of an upward-closed set stays upward-closed. We compute
    the exact one-step predecessor of the unsafe set under the reaction,
        Pre = { s : react(s) in U },   U = { a >= A_collapse },
    and test whether Pre is upward-closed under componentwise <=.

    bounded reaction  -> Pre = {a >= A_collapse + Ra}     (upward-closed)  -> decidable
    unbounded reaction-> Pre = {a >= A_collapse + c}      (NOT upward-closed: a worse
                          state can over-correct below U) -> coverability breaks.
    """
    states = [(c, a) for c in range(c_hi + 1) for a in range(a_hi + 1)]
    pre = set()
    for (c, a) in states:
        rc, ra = react(c, a, p, mode)
        if ra >= p.A_collapse:
            pre.add((c, a))
    violations = []
    pre_set = pre
    for (c, a) in pre:
        # any "worse" state that fell out of Pre is an upward-closure violation
        for (c2, a2) in [(c + 1, a), (c, a + 1), (c + 1, a + 1)]:
            if c2 <= c_hi and a2 <= a_hi and (c2, a2) not in pre_set:
                if len(violations) < 12:
                    violations.append({"in_pre": [c, a], "worse_not_in_pre": [c2, a2],
                                       "react_worse": list(react(c2, a2, p, mode))})
    return {
        "mode": mode,
        "pre_size": len(pre),
        "pre_is_upward_closed": len(violations) == 0,
        "violations": violations,
    }


def synthesize_shield(p: ShieldParams, mode: str, doomed: set[tuple[int, int]],
                      sample_n: int = 40) -> list[dict]:
    """For safe states, the shield = the referee action(s) whose resulting state
    stays out of the doomed set. Returns a sample of (state -> allowed actions)."""
    shield = []
    for c in range(p.Cmax + 1):
        for a in range(p.Amax + 1):
            if (c, a) in doomed:
                continue
            ac, aa = accumulate(c, a, p)
            ac, aa = min(ac, p.Cmax), min(aa, p.Amax)
            allowed = []
            if (ac, aa) not in doomed:
                allowed.append("noreact")
            if gated(ac, aa, p) and mode in ("bounded", "unbounded"):
                rc, ra = react(ac, aa, p, mode)
                if (min(rc, p.Cmax), min(ra, p.Amax)) not in doomed:
                    allowed.append("react")
            shield.append({"state": [c, a], "allowed_actions": allowed,
                           "must_react": allowed == ["react"]})
    # sample evenly
    if len(shield) > sample_n:
        step = len(shield) // sample_n
        shield = shield[::step][:sample_n]
    return shield
