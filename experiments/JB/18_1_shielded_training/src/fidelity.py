"""Experiment 18.1 Level A — abstraction-fidelity (the kill gate).

Tests whether 18.0's 2-counter shield faithfully classifies real justitia
collapse. Reuses 18.0's harvester, shield, and ShieldParams unchanged; the only
thing 18.0 left unspecified is the explicit projection real_state -> (c, a), so we
fix it here as the most CHARITABLE operationalization of 18.0's stated
correspondence (`a >= A_collapse <=> collapse`, `c <- concentration`):

    a = round(A_collapse * max(0, 1 - mean_welfare) / (1 - 0.32))   # a>=A_collapse <=> mean_welfare<0.32
    c = round(resource_hhi * Cmax)

so the projection reproduces the real PRIMARY collapse clause exactly. The fidelity
question is then: does this projection's SAFE/DOOMED label track real collapse?
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

SHIELD_SRC = Path("/home/master/llm_projects/ascesis/experiments/18_0_shield_synthesis/src")
if str(SHIELD_SRC) not in sys.path:
    sys.path.insert(0, str(SHIELD_SRC))

from justitia_harvest import collapse_pred, harvest_states  # noqa: E402,F401  (re-exported)
from shield import ShieldParams, compute_doomed  # noqa: E402

WELFARE_COLLAPSE = 0.32  # real primary collapse threshold on mean welfare


def project(mean_welfare: float, resource_hhi: float, p: ShieldParams) -> tuple[int, int]:
    """Operationalization of 18.0's correspondence; a>=A_collapse <=> mean_welfare<0.32."""
    deficit = max(0.0, 1.0 - mean_welfare)
    a = min(p.Amax, round(p.A_collapse * deficit / (1.0 - WELFARE_COLLAPSE)))
    c = min(p.Cmax, round(resource_hhi * p.Cmax))
    return c, a


def shield_label(state: dict, doomed: set, p: ShieldParams) -> str:
    return "DOOMED" if project(state["mean_welfare"], state["resource_hhi"], p) in doomed else "SAFE"


def group_trajectories(states: list[dict]) -> dict:
    traj = defaultdict(list)
    for s in states:
        traj[(s["world"], s["policy"], s["seed"])].append(s)
    for k in traj:
        traj[k].sort(key=lambda s: s["step"])
    return traj


def future_collapse_flags(seq: list[dict], horizon: int | None) -> list[bool]:
    """For each state: does collapse occur at or after it (within `horizon` steps,
    or anywhere in the rest of the trajectory if horizon is None)?"""
    n = len(seq)
    flags = [False] * n
    if horizon is None:
        acc = False
        for i in range(n - 1, -1, -1):
            acc = acc or seq[i]["collapse"]
            flags[i] = acc
    else:
        for i in range(n):
            flags[i] = any(seq[j]["collapse"] for j in range(i, min(n, i + horizon + 1)))
    return flags


def confusion(states: list[dict], p: ShieldParams, horizon: int | None = None) -> dict:
    doomed = compute_doomed(p, "bounded")["doomed"]
    traj = group_trajectories(states)

    tp = fp = tn = fn = 0  # positive class = real collapse (within horizon); predicted positive = DOOMED
    safe = doomed_n = 0
    false_safe = 0
    per_policy = defaultdict(lambda: [0, 0])  # policy -> [false_safe, n_safe]

    # policy-independent pure-blindness: CURRENTLY collapsed states labelled SAFE
    cur_collapsed = 0
    cur_collapsed_safe = 0
    blind_spread = blind_mass = blind_mean = 0

    for (world, policy, seed), seq in traj.items():
        gt = future_collapse_flags(seq, horizon)
        for i, s in enumerate(seq):
            lab = shield_label(s, doomed, p)
            real = gt[i]
            if lab == "SAFE":
                safe += 1
                per_policy[policy][1] += 1
                if real:
                    false_safe += 1
                    per_policy[policy][0] += 1
            else:
                doomed_n += 1
            # confusion (predicted DOOMED == predicted collapse)
            if lab == "DOOMED" and real:
                tp += 1
            elif lab == "DOOMED" and not real:
                fp += 1
            elif lab == "SAFE" and not real:
                tn += 1
            else:
                fn += 1
            # pure abstraction blindness on the current step
            if s["collapse"]:
                cur_collapsed += 1
                if lab == "SAFE":
                    cur_collapsed_safe += 1
                    if s["n_zones_below_0_20"] >= 4 and s["mean_welfare"] >= WELFARE_COLLAPSE:
                        blind_spread += 1
                    if s["total_mass"] < 35 and s["mean_welfare"] >= WELFARE_COLLAPSE:
                        blind_mass += 1
                    if s["mean_welfare"] < WELFARE_COLLAPSE:
                        blind_mean += 1

    false_safe_rate = false_safe / safe if safe else 0.0
    false_doomed_rate = fp / doomed_n if doomed_n else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {
        "horizon": "rest_of_trajectory" if horizon is None else horizon,
        "n_states": len(states),
        "n_safe": safe,
        "n_doomed": doomed_n,
        "confusion_matrix": {"tp_doomed_collapse": tp, "fp_doomed_nocollapse": fp,
                             "tn_safe_nocollapse": tn, "fn_safe_collapse": fn},
        "false_safe_rate": false_safe_rate,
        "false_doomed_rate": false_doomed_rate,
        "doomed_precision_vs_collapse": precision,
        "doomed_recall_vs_collapse": recall,
        "per_policy_false_safe_rate": {pol: {"false_safe_rate": fs / n if n else 0.0,
                                             "false_safe": fs, "n_safe": n}
                                       for pol, (fs, n) in sorted(per_policy.items())},
        "pure_abstraction_blindness": {
            "n_currently_collapsed": cur_collapsed,
            "currently_collapsed_labeled_SAFE": cur_collapsed_safe,
            "rate": cur_collapsed_safe / cur_collapsed if cur_collapsed else 0.0,
            "blind_via_spread_clause": blind_spread,   # >=4 zones<0.20 but mean welfare ok
            "blind_via_mass_clause": blind_mass,        # total_mass<35 but mean welfare ok
            "via_mean_welfare_misround": blind_mean,    # projection rounding edge
        },
    }


def blind_coordinates_report() -> dict:
    """Which real coordinates the 2-counter abstraction cannot see."""
    return {
        "abstraction_coordinates": ["c = concentration (resource_hhi)", "a = mean-welfare deficit"],
        "real_collapse_uses": ["mean(zone_welfare)<0.32", "#{zone_welfare<0.20}>=4 (zone-welfare SPREAD)",
                               "total_mass<35 (population MASS)"],
        "blind_to": [
            "zone-welfare SPREAD: the '>=4 zones<0.20' clause — a state with healthy MEAN welfare "
            "but 4 collapsed zones is real-collapse, projected to SAFE.",
            "total MASS: the 'mass<35' clause — population collapse with ok welfare, projected to SAFE.",
            "FORWARD dynamics: 18.0's doomed set converged in 1 iteration to U itself, so the shield is a "
            "current-mean-welfare-collapse DETECTOR, not a forward-collapse predictor; mean-welfare-safe "
            "states that proceed to collapse are labeled SAFE.",
        ],
        "reformulation_hint": "A faithful abstraction needs at least: min-zone-welfare (or count of "
                              "failed zones) AND total mass as coordinates, AND a genuine forward "
                              "reachability on the real (or a richer) transition — not the trivial "
                              "bounded-sword game that collapses doomed to U.",
    }
