from __future__ import annotations

import random
from typing import Callable

from collapse_boundary.types import RewriteRule, RewriteSystem, Term


def atom(name: str) -> Term:
    return Term(name)


def app(symbol: str, *children: Term) -> Term:
    return Term(symbol, tuple(children))


def num(n: int) -> Term:
    term = atom("0")
    for _ in range(n):
        term = app("s", term)
    return term


def recursive_rule(name: str, root_fn: Callable[[Term], list[tuple[Term, str, bool]]], collapsing: bool = False) -> RewriteRule:
    def fn(term: Term) -> list[tuple[Term, str, bool]]:
        out = list(root_fn(term))
        for idx, child in enumerate(term.children):
            for new_child, rule_name, is_collapsing in fn(child):
                children = list(term.children)
                children[idx] = new_child
                out.append((Term(term.symbol, tuple(children)), rule_name, is_collapsing))
        return out
    return RewriteRule(name, fn, collapsing)


# System A: dead normalizing arithmetic.
def r_add0(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "add" and len(t.children) == 2 and t.children[0].symbol == "0":
        return [(t.children[1], "add_zero", True)]
    return []


def r_adds(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "add" and len(t.children) == 2 and t.children[0].symbol == "s":
        return [(app("s", app("add", t.children[0].children[0], t.children[1])), "add_succ", False)]
    return []


def r_mul0(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "mul" and len(t.children) == 2 and t.children[0].symbol == "0":
        return [(atom("0"), "mul_zero", True)]
    return []


def r_muls(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "mul" and len(t.children) == 2 and t.children[0].symbol == "s":
        x, y = t.children[0].children[0], t.children[1]
        return [(app("add", y, app("mul", x, y)), "mul_succ", False)]
    return []


def sample_dead(rng: random.Random, depth: int) -> Term:
    # Fixed small domain on purpose: this is the dead finite-control baseline.
    a = rng.randint(0, 3)
    b = rng.randint(0, 3)
    if rng.random() < 0.5:
        return app("add", num(a), num(b))
    return app("mul", num(a), num(b))


# System B: fake-live noisy syntactic expansion.
def r_noise_bits(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "Noise" and len(t.children) == 1:
        return [
            (app("Noise", app("bit0", t.children[0])), "noise_bit0", False),
            (app("Noise", app("bit1", t.children[0])), "noise_bit1", False),
        ]
    return []


def r_wrap(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "A" and len(t.children) == 1:
        return [(app("A", app("wrap", t.children[0])), "wrap", False)]
    return []


def sample_fake(rng: random.Random, depth: int) -> Term:
    base = atom(f"seed{rng.randint(0, 7)}")
    return app("Noise" if rng.random() < 0.7 else "A", base)


# System C: collapsing non-confluent candidate.
def r_F_left(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "F" and len(t.children) == 2:
        return [(t.children[0], "F_left", True)]
    return []


def r_F_right(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "F" and len(t.children) == 2:
        return [(t.children[1], "F_right", True)]
    return []


def make_r_G_expand(depth_cap: int = 12) -> Callable[[Term], list[tuple[Term, str, bool]]]:
    def r_G_expand(t: Term) -> list[tuple[Term, str, bool]]:
        if t.symbol == "G" and len(t.children) == 1 and t.depth() < depth_cap:
            x = t.children[0]
            return [(app("F", app("G", app("a", x)), app("G", app("b", x))), "G_expand", False)]
        return []

    return r_G_expand


r_G_expand = make_r_G_expand(12)


def sample_collapse(rng: random.Random, depth: int) -> Term:
    x = atom(f"x{rng.randint(0, max(2, depth + 2))}")
    if rng.random() < 0.5:
        return app("G", x)
    return app("F", app("G", app("a", x)), app("G", app("b", x)))


# System D: structured proof-like candidate.
def r_choose_left(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "choose" and len(t.children) == 2:
        return [(t.children[0], "choose_left", True)]
    return []


def r_choose_right(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "choose" and len(t.children) == 2:
        return [(t.children[1], "choose_right", True)]
    return []


def r_compose(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "compose" and len(t.children) == 3:
        ra, rb, x = t.children
        return [(app("step", rb, app("step", ra, x)), "compose_steps", False)]
    return []


def r_lemma_drop(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "lemma" and len(t.children) == 1:
        return [(t.children[0], "lemma_drop", True)]
    return []


def r_lemma_cache(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "lemma" and len(t.children) == 1:
        return [(app("cached", t.children[0]), "lemma_cache", False)]
    return []


def r_cached_use(t: Term) -> list[tuple[Term, str, bool]]:
    if t.symbol == "cached" and len(t.children) == 1:
        return [(t.children[0], "cached_use", True)]
    return []


def sample_structured(rng: random.Random, depth: int) -> Term:
    x = atom(f"goal{rng.randint(0, max(2, depth + 2))}")
    ra = atom(rng.choice(["intro", "elim", "rewrite", "assoc"]))
    rb = atom(rng.choice(["simpl", "modus", "transport", "cut"]))
    core = app("compose", ra, rb, x)
    if rng.random() < 0.5:
        return app("choose", app("lemma", core), app("lemma", app("step", ra, x)))
    return app("lemma", app("choose", core, app("step", rb, x)))


def build_collapsing_system(depth_cap: int = 12) -> RewriteSystem:
    return RewriteSystem(
        "C_collapsing_live_candidate",
        (
            recursive_rule("F_left", r_F_left, True),
            recursive_rule("F_right", r_F_right, True),
            recursive_rule("G_expand", make_r_G_expand(depth_cap)),
        ),
        sample_collapse,
        "collapsing",
    )


def build_systems() -> list[RewriteSystem]:
    return [
        RewriteSystem(
            "A_dead_control",
            (
                recursive_rule("add_zero", r_add0, True),
                recursive_rule("add_succ", r_adds),
                recursive_rule("mul_zero", r_mul0, True),
                recursive_rule("mul_succ", r_muls),
            ),
            sample_dead,
            "dead",
        ),
        RewriteSystem(
            "B_fake_live_control",
            (recursive_rule("noise_bit0", r_noise_bits), recursive_rule("wrap", r_wrap)),
            sample_fake,
            "fake_live",
        ),
        build_collapsing_system(12),
        RewriteSystem(
            "D_structured_live_candidate",
            (
                recursive_rule("choose_left", r_choose_left, True),
                recursive_rule("choose_right", r_choose_right, True),
                recursive_rule("compose_steps", r_compose),
                recursive_rule("lemma_drop", r_lemma_drop, True),
                recursive_rule("lemma_cache", r_lemma_cache),
                recursive_rule("cached_use", r_cached_use, True),
            ),
            sample_structured,
            "structured",
        ),
    ]
