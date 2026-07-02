from __future__ import annotations

import itertools
import math
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .analysis import add_attack_labels, compute_metric_panel, stable_id


def finalize_rows(rows: list[dict[str, Any]], seed: int, substrate_bias: float) -> pd.DataFrame:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["class_key"]].append(row)
    out = []
    max_reuse = max((sum(r["reuse_count"] for r in items) for items in groups.values()), default=1)
    for key, items in groups.items():
        ops = {r["operator"] for r in items}
        depths = [int(r["depth"]) for r in items]
        objects = {r["object_id"] for r in items}
        role = float(np.mean([r["role_score"] for r in items]))
        action = float(np.mean([r["action_effect_score"] for r in items]))
        redundancy = float(np.mean([r["redundancy_score"] for r in items]))
        reuse_count = float(sum(r["reuse_count"] for r in items))
        signature = repr(key)
        out.append(
            {
                "class_id": stable_id(key),
                "class_key": signature,
                "class_size": len(items),
                "object_diversity": len(objects),
                "operator_diversity": len(ops),
                "depth_min": min(depths),
                "depth_max": max(depths),
                "reuse_count": reuse_count,
                "role_score": role,
                "action_effect_score": action,
                "redundancy_score": redundancy,
                "signature_len": len(signature),
                "representative": items[0]["representative"],
                "operator_family": ";".join(sorted(ops)),
            }
        )
    df = pd.DataFrame(out)
    df = compute_metric_panel(df, seed)
    return add_attack_labels(df, seed, substrate_bias)


def load_causal_dag_baseline(root: Path, seed: int) -> pd.DataFrame:
    feature_path = root.parents[0] / "17E_latent_metric_geometry" / "outputs_17E" / "feature_matrix.csv"
    if not feature_path.exists():
        raise FileNotFoundError(f"Missing 17E feature matrix: {feature_path}")
    df = pd.read_csv(feature_path)
    required = [
        "class_id",
        "class_size",
        "frequency",
        "dag_diversity",
        "operator_diversity",
        "depth_min",
        "depth_max",
        "reuse_count",
        "role_score",
        "intervention_score",
        "M1_original_score",
        "M2_intervention_score",
        "M3_reuse_score",
        "M4_compression_score",
        "M5_perturbation_centrality_score",
        "M6_frequency_control_score",
        "M7_random_matched_score",
        "class_a_survives",
        "class_b_survives",
        "class_b_attack_cost",
        "class_b_auc_gns",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise FileNotFoundError(f"17E baseline lacks columns: {missing}")
    out = pd.DataFrame()
    out["class_id"] = df["class_id"]
    out["class_key"] = df.get("representative", df["class_id"]).astype(str)
    out["class_size"] = df["class_size"]
    out["object_diversity"] = df.get("dag_diversity", df["class_size"])
    out["operator_diversity"] = df["operator_diversity"]
    out["depth_min"] = df["depth_min"]
    out["depth_max"] = df["depth_max"]
    out["reuse_count"] = df["reuse_count"]
    out["role_score"] = df["role_score"]
    out["action_effect_score"] = df["intervention_score"]
    out["redundancy_score"] = (df.get("dag_div_score", df["frequency"]) + df["M3_reuse_score"]) / 2.0
    out["signature_len"] = df.get("signature_len", df["class_id"].astype(str).str.len())
    out["representative"] = df.get("representative", df["class_id"]).astype(str)
    out["operator_family"] = df.get("operators", "").astype(str)
    for col in [
        "frequency",
        "object_diversity_score",
        "depth_score",
        "reuse_rate",
        "complexity",
        "M1_original_score",
        "M2_intervention_score",
        "M3_reuse_score",
        "M4_compression_score",
        "M5_perturbation_centrality_score",
        "M6_frequency_control_score",
        "M7_random_matched_score",
    ]:
        if col in df:
            out[col] = df[col]
    out["class_a_survives"] = df["class_a_survives"]
    out["class_b_survives"] = df["class_b_survives"]
    out["class_b_attack_cost"] = df["class_b_attack_cost"]
    out["class_b_auc_gns"] = df["class_b_auc_gns"]
    return out.copy()


def random_graph(rng: np.random.Generator, n: int, p: float) -> set[tuple[int, int]]:
    edges = set()
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < p:
                edges.add((i, j))
    return edges


def reachable(n: int, edges: set[tuple[int, int]], src: int) -> dict[int, int]:
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    dist = {src: 0}
    q = deque([src])
    while q:
        cur = q.popleft()
        for nxt in adj[cur]:
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return dist


def directed_graph_substrate(seed: int, num_objects: int, max_depth: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 101)
    rows = []
    for gid in range(num_objects):
        n = int(rng.integers(5, 11))
        edges = random_graph(rng, n, float(rng.uniform(0.12, 0.28)))
        indeg = Counter(b for _, b in edges)
        outdeg = Counter(a for a, _ in edges)
        all_dist = {i: reachable(n, edges, i) for i in range(n)}
        for i, j in itertools.permutations(range(n), 2):
            if j in all_dist[i]:
                d = all_dist[i][j]
                bucket = min(max_depth, d)
                alt = sum(1 for mid in range(n) if mid not in {i, j} and mid in all_dist[i] and j in all_dist[mid])
                rows.append(
                    {
                        "object_id": gid,
                        "class_key": ("Reachable", bucket, min(3, alt), min(3, outdeg[i]), min(3, indeg[j]), min(3, n // 3)),
                        "operator": "Reachable",
                        "depth": bucket,
                        "reuse_count": 1 + alt,
                        "role_score": min(1.0, alt / 3.0),
                        "action_effect_score": 0.7,
                        "redundancy_score": min(1.0, alt / 4.0),
                        "representative": f"Reachable(N{i},N{j})",
                    }
                )
                rows.append(
                    {
                        "object_id": gid,
                        "class_key": ("PathLengthBucket", bucket, min(3, outdeg[i]), min(3, indeg[j]), min(3, n // 3)),
                        "operator": "PathLengthBucket",
                        "depth": bucket,
                        "reuse_count": 1,
                        "role_score": 0.35 + 0.08 * bucket,
                        "action_effect_score": 0.55,
                        "redundancy_score": min(1.0, alt / 4.0),
                        "representative": f"PathLengthBucket(N{i},N{j})={bucket}",
                    }
                )
        for i in range(n):
            inb = min(4, indeg[i])
            outb = min(4, outdeg[i])
            succ = {b for a, b in edges if a == i}
            pred = {a for a, b in edges if b == i}
            cyc = int(i in all_dist[i] and all_dist[i][i] > 0)
            for op, bucket, role in [
                ("InDegreeBucket", (inb, outb, min(3, n // 3)), min(1.0, inb / 4)),
                ("OutDegreeBucket", (outb, inb, min(3, n // 3)), min(1.0, outb / 4)),
                ("CycleParticipation", (cyc, inb, outb), 0.8 if cyc else 0.2),
                ("CutVertexLikeRole", (int(len(pred) > 1 and len(succ) > 1), min(3, len(pred)), min(3, len(succ))), min(1.0, len(pred) * len(succ) / 8)),
            ]:
                rows.append(
                    {
                        "object_id": gid,
                        "class_key": (op, bucket),
                        "operator": op,
                        "depth": 1 + (bucket[0] if isinstance(bucket, tuple) else bucket),
                        "reuse_count": 1 + len(pred) + len(succ),
                        "role_score": role,
                        "action_effect_score": 0.45 + 0.20 * role,
                        "redundancy_score": min(1.0, (len(pred) + len(succ)) / 8),
                        "representative": f"{op}(N{i})={bucket}",
                    }
                )
        for i, j in itertools.combinations(range(n), 2):
            succ_i = {b for a, b in edges if a == i}
            succ_j = {b for a, b in edges if a == j}
            pred_i = {a for a, b in edges if b == i}
            pred_j = {a for a, b in edges if b == j}
            shared_s = len(succ_i & succ_j)
            shared_p = len(pred_i & pred_j)
            if shared_s:
                rows.append(
                    {
                        "object_id": gid,
                        "class_key": ("SharedSuccessor", min(3, shared_s), min(3, outdeg[i]), min(3, outdeg[j]), min(3, n // 3)),
                        "operator": "SharedSuccessor",
                        "depth": 2,
                        "reuse_count": shared_s,
                        "role_score": min(1.0, shared_s / 3),
                        "action_effect_score": 0.6,
                        "redundancy_score": min(1.0, shared_s / 3),
                        "representative": f"SharedSuccessor(N{i},N{j})",
                    }
                )
            if shared_p:
                rows.append(
                    {
                        "object_id": gid,
                        "class_key": ("SharedPredecessor", min(3, shared_p), min(3, indeg[i]), min(3, indeg[j]), min(3, n // 3)),
                        "operator": "SharedPredecessor",
                        "depth": 2,
                        "reuse_count": shared_p,
                        "role_score": min(1.0, shared_p / 3),
                        "action_effect_score": 0.55,
                        "redundancy_score": min(1.0, shared_p / 3),
                        "representative": f"SharedPredecessor(N{i},N{j})",
                    }
                )
    return finalize_rows(rows, seed + 201, substrate_bias=0.03)


SYMBOLS = ["f", "g", "h", "p", "q"]
CONSTS = ["a", "b", "c"]


def term_depth(term: str) -> int:
    return term.count("(")


def make_term(rng: np.random.Generator, depth: int) -> str:
    if depth <= 0 or rng.random() < 0.30:
        return str(rng.choice(CONSTS))
    sym = str(rng.choice(SYMBOLS))
    if rng.random() < 0.65:
        return f"{sym}({make_term(rng, depth - 1)})"
    return f"{sym}({make_term(rng, depth - 1)},{make_term(rng, depth - 1)})"


def normalize(term: str, rules: dict[str, str], max_steps: int = 12) -> tuple[str, int]:
    cur = term
    steps = 0
    for _ in range(max_steps):
        changed = False
        for lhs, rhs in rules.items():
            if lhs in cur:
                cur = cur.replace(lhs, rhs, 1)
                steps += 1
                changed = True
                break
        if not changed:
            break
    return cur, steps


def rewrite_substrate(seed: int, num_objects: int, max_depth: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 301)
    rulesets = []
    for rid in range(max(8, num_objects // 20)):
        rules = {
            "f(a)": "b",
            "g(b)": "c",
            "h(c)": "a",
            "p(a,b)": "c",
            "q(c)": "b",
        }
        if rng.random() < 0.45:
            rules["f(b)"] = "c"
        if rng.random() < 0.35:
            rules["g(a)"] = "a"
        if rng.random() < 0.35:
            rules["h(b)"] = "b"
        rulesets.append((rid, rules))
    rows = []
    for oid in range(num_objects):
        rid, rules = rulesets[oid % len(rulesets)]
        term = make_term(rng, max_depth)
        nf, steps = normalize(term, rules)
        d = max(1, term_depth(term))
        nf_bucket = stable_id(("nf", nf))[:4]
        critical = sum(1 for lhs in rules if lhs[0] in term)
        rows.append(
            {
                "object_id": rid,
                "class_key": ("NormalForm", nf_bucket, min(4, d)),
                "operator": "NormalForm",
                "depth": d,
                "reuse_count": 1 + steps,
                "role_score": min(1.0, steps / 5),
                "action_effect_score": 0.35 + 0.10 * min(4, steps),
                "redundancy_score": min(1.0, len([r for r in rules.values() if r == nf]) / 3),
                "representative": f"NormalForm({term})={nf}",
            }
        )
        rows.append(
            {
                "object_id": rid,
                "class_key": ("RewriteDistanceBucket", min(5, steps)),
                "operator": "RewriteDistanceBucket",
                "depth": d,
                "reuse_count": 1 + steps,
                "role_score": min(1.0, steps / 5),
                "action_effect_score": 0.6,
                "redundancy_score": min(1.0, steps / 6),
                "representative": f"RewriteDistanceBucket({term})={min(5, steps)}",
            }
        )
        if steps:
            rows.append(
                {
                    "object_id": rid,
                    "class_key": ("Derives", min(4, steps), nf_bucket),
                    "operator": "Derives",
                    "depth": d,
                    "reuse_count": 2 + steps,
                    "role_score": 0.65,
                    "action_effect_score": 0.75,
                    "redundancy_score": min(1.0, critical / 4),
                    "representative": f"Derives({term},{nf})",
                }
            )
        rows.append(
            {
                "object_id": rid,
                "class_key": ("CriticalPairParticipation", min(4, critical)),
                "operator": "CriticalPairParticipation",
                "depth": d,
                "reuse_count": 1 + critical,
                "role_score": min(1.0, critical / 4),
                "action_effect_score": 0.65,
                "redundancy_score": min(1.0, critical / 5),
                "representative": f"CriticalPairParticipation({term})",
            }
        )
        rows.append(
            {
                "object_id": rid,
                "class_key": ("ConfluenceWitness", int(steps <= 4 and critical <= 2)),
                "operator": "ConfluenceWitness",
                "depth": d,
                "reuse_count": 1 + len(rules),
                "role_score": 0.55,
                "action_effect_score": 0.50,
                "redundancy_score": min(1.0, len(rules) / 8),
                "representative": f"ConfluenceWitness({term})",
            }
        )
    return finalize_rows(rows, seed + 401, substrate_bias=-0.02)


def dfa_accepts(trans: dict[tuple[int, str], int], accept: set[int], word: str) -> bool:
    state = 0
    for ch in word:
        state = trans[(state, ch)]
    return state in accept


def dfa_substrate(seed: int, num_objects: int, max_depth: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 501)
    alphabet = ["a", "b"]
    words = ["", "a", "b", "aa", "ab", "ba", "bb", "aba", "bab", "abba", "baab"]
    rows = []
    for aid in range(num_objects):
        n = int(rng.integers(3, 8))
        trans = {}
        for q in range(n):
            for ch in alphabet:
                trans[(q, ch)] = int(rng.integers(0, n))
        accept = {q for q in range(n) if rng.random() < 0.45}
        reachable_states = {0}
        changed = True
        while changed:
            changed = False
            for q in list(reachable_states):
                for ch in alphabet:
                    nxt = trans[(q, ch)]
                    if nxt not in reachable_states:
                        reachable_states.add(nxt)
                        changed = True
        futures = {}
        suffixes = ["", "a", "b", "aa", "bb", "ab", "ba"]
        for q in range(n):
            sig = []
            for w in suffixes:
                cur = q
                for ch in w:
                    cur = trans[(cur, ch)]
                sig.append(cur in accept)
            futures[q] = tuple(sig)
        eq_counts = Counter(futures.values())
        for w in words:
            acc = dfa_accepts(trans, accept, w)
            rows.append(
                {
                    "object_id": aid,
                    "class_key": ("Accepts" if acc else "Rejects", len(w), stable_id(w)[:2], min(3, len(accept)), min(3, len(reachable_states))),
                    "operator": "Accepts" if acc else "Rejects",
                    "depth": max(1, len(w)),
                    "reuse_count": 1 + len(w),
                    "role_score": 0.45 + 0.05 * len(w),
                    "action_effect_score": 0.65,
                    "redundancy_score": len(accept) / max(n, 1),
                    "representative": f"{'Accepts' if acc else 'Rejects'}({w})",
                }
            )
        for q in range(n):
            role = 1.0 if q in reachable_states else 0.2
            rows.append(
                {
                    "object_id": aid,
                    "class_key": ("ReachableState", int(q in reachable_states), min(3, sum(1 for v in trans.values() if v == q)), int(q in accept)),
                    "operator": "ReachableState",
                    "depth": 1,
                    "reuse_count": 1 + sum(1 for v in trans.values() if v == q),
                    "role_score": role,
                    "action_effect_score": 0.50,
                    "redundancy_score": min(1.0, eq_counts[futures[q]] / 3),
                    "representative": f"ReachableState(q{q})",
                }
            )
            rows.append(
                {
                    "object_id": aid,
                    "class_key": ("MinimalStateClass", min(4, eq_counts[futures[q]]), int(q in accept), min(3, sum(1 for v in trans.values() if v == q))),
                    "operator": "MinimalStateClass",
                    "depth": 2,
                    "reuse_count": eq_counts[futures[q]],
                    "role_score": min(1.0, eq_counts[futures[q]] / 3),
                    "action_effect_score": 0.55,
                    "redundancy_score": min(1.0, eq_counts[futures[q]] / 3),
                    "representative": f"MinimalStateClass(q{q})",
                }
            )
            for ch in alphabet:
                nxt = trans[(q, ch)]
                rows.append(
                    {
                        "object_id": aid,
                        "class_key": ("TransitionEffect", ch, int(nxt in accept), int(q in reachable_states), min(3, eq_counts[futures[nxt]]), int(q in accept)),
                        "operator": "TransitionEffect",
                        "depth": 2,
                        "reuse_count": 1 + sum(1 for v in trans.values() if v == nxt),
                        "role_score": 0.7 if q in reachable_states else 0.25,
                        "action_effect_score": 0.85,
                        "redundancy_score": min(1.0, eq_counts[futures[nxt]] / 3),
                        "representative": f"TransitionEffect(q{q},{ch},q{nxt})",
                    }
                )
        for q1, q2 in itertools.combinations(range(n), 2):
            eq = futures[q1] == futures[q2]
            dist_bucket = 0 if eq else min(4, next((len(w) for w, a, b in [(w, futures[q1][i], futures[q2][i]) for i, w in enumerate(suffixes)] if a != b), 4))
            rows.append(
                {
                    "object_id": aid,
                    "class_key": ("EquivalentState", int(eq), int(q1 in accept), int(q2 in accept), min(3, eq_counts[futures[q1]] + eq_counts[futures[q2]])),
                    "operator": "EquivalentState",
                    "depth": 2,
                    "reuse_count": 1 + int(eq),
                    "role_score": 0.75 if eq else 0.4,
                    "action_effect_score": 0.45,
                    "redundancy_score": 1.0 if eq else 0.2,
                    "representative": f"EquivalentState(q{q1},q{q2})",
                }
            )
            rows.append(
                {
                    "object_id": aid,
                    "class_key": ("DistinguishingWordBucket", dist_bucket, int(q1 in accept), int(q2 in accept), min(3, n // 2)),
                    "operator": "DistinguishingWordBucket",
                    "depth": max(1, dist_bucket),
                    "reuse_count": 1 + dist_bucket,
                    "role_score": min(1.0, 0.3 + 0.12 * dist_bucket),
                    "action_effect_score": 0.7,
                    "redundancy_score": 1.0 if eq else 0.2,
                    "representative": f"DistinguishingWordBucket(q{q1},q{q2})",
                }
            )
    return finalize_rows(rows, seed + 601, substrate_bias=0.01)

