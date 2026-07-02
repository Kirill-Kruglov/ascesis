from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, order=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()

    def serialize(self) -> str:
        if not self.children:
            return self.symbol
        return f"{self.symbol}(" + ",".join(child.serialize() for child in self.children) + ")"

    def shape(self) -> str:
        if not self.children:
            return "_"
        return f"{self.symbol}(" + ",".join(child.shape() for child in self.children) + ")"

    def top(self) -> str:
        return self.symbol

    def size(self) -> int:
        return 1 + sum(child.size() for child in self.children)

    def depth(self) -> int:
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)


@dataclass(frozen=True)
class RewriteStep:
    before: Term
    after: Term
    rule_name: str
    collapsing: bool


RuleFn = Callable[[Term], list[tuple[Term, str, bool]]]


@dataclass(frozen=True)
class RewriteRule:
    name: str
    fn: RuleFn
    collapsing: bool = False


@dataclass
class RewriteSystem:
    name: str
    rules: tuple[RewriteRule, ...]
    sampler: Callable[[object, int], Term]
    family: str

    def rewrites(self, term: Term) -> list[RewriteStep]:
        out: list[RewriteStep] = []
        for rule in self.rules:
            for after, name, collapsing in rule.fn(term):
                out.append(RewriteStep(term, after, name or rule.name, collapsing or rule.collapsing))
        return out
