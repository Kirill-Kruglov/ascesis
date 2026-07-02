from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any, Iterable


def entropy(keys: Iterable[Any]) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    out = 0.0
    for count in counts.values():
        p = count / total
        if p:
            out -= p * math.log2(p)
    return out


def class_stats(keys: list[Any]) -> dict[str, float]:
    counts = Counter(keys)
    n = len(keys)
    if n == 0:
        return {
            "class_count": 0,
            "entropy": 0.0,
            "largest_class_fraction": 0.0,
            "singleton_fraction": 0.0,
            "class_count_ratio": 0.0,
        }
    return {
        "class_count": len(counts),
        "entropy": entropy(keys),
        "largest_class_fraction": max(counts.values()) / n,
        "singleton_fraction": sum(1 for v in counts.values() if v == 1) / len(counts),
        "class_count_ratio": len(counts) / n,
    }


def group_indices(keys: list[Any]) -> dict[Any, list[int]]:
    groups: dict[Any, list[int]] = defaultdict(list)
    for idx, key in enumerate(keys):
        groups[key].append(idx)
    return groups


def first_pair_same_key_diff_other(primary: list[Any], secondary: list[Any]) -> tuple[int, int] | None:
    for indices in group_indices(primary).values():
        seen: dict[Any, int] = {}
        for idx in indices:
            other = secondary[idx]
            if other not in seen:
                seen[other] = idx
            if len(seen) >= 2:
                vals = list(seen.values())
                return vals[0], vals[1]
    return None
