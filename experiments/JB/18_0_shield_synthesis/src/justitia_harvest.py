"""Harvest real states from the justitia substrate and run the empirical parts of
Experiment 18.0 (Step 1 upward-closure, Step 2 reaction-magnitude) against the
ACTUAL code — not the essay's metaphors.

The collapse predicate is reproduced verbatim from model/substrate.py
(`_trajectory_snapshot` / `metrics`):

    collapse = mean(zone_welfare) < 0.32
               or sum(1 for w in zone_welfare if w < 0.20) >= 4
               or total_mass < 35
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

JUSTITIA = Path("/home/master/llm_projects/justitia/model")
if str(JUSTITIA) not in sys.path:
    sys.path.insert(0, str(JUSTITIA))

import substrate as base  # noqa: E402

WELFARE_MEAN_FLOOR = 0.32
ZONE_WELFARE_FLOOR = 0.20
MASS_FLOOR = 35.0


def collapse_pred(zone_welfare: list[float], total_mass: float) -> bool:
    """Verbatim justitia collapse condition (the unsafe set U)."""
    mean_w = sum(zone_welfare) / len(zone_welfare)
    return (mean_w < WELFARE_MEAN_FLOOR
            or sum(1 for w in zone_welfare if w < ZONE_WELFARE_FLOOR) >= 4
            or total_mass < MASS_FLOOR)


def harvest_states(worlds, policies, seeds) -> list[dict]:
    """Run the real model and collect per-step states with the collapse coordinates."""
    states = []
    for world in worlds:
        for policy in policies:
            for seed in seeds:
                p = base.Params(mode="governance", world=world, policy=policy)
                m = base.EvolvableStrategyModel(seed, p, record_trajectory=True)
                m.run()
                prev = None
                for snap in m.trajectory:
                    zw = list(snap["zone_welfare"])
                    total_mass = sum(snap["zone_mass"])
                    st = {
                        "world": world, "policy": policy, "seed": seed, "step": snap["step"],
                        "zone_welfare": zw,
                        "mean_welfare": sum(zw) / len(zw),
                        "min_zone_welfare": min(zw),
                        "n_zones_below_0_20": sum(1 for w in zw if w < ZONE_WELFARE_FLOOR),
                        "total_mass": total_mass,
                        "resource_hhi": snap["resource_hhi"],          # concentration
                        "capture_index": snap["capture_index"],         # accumulated-harm composite
                        "exploit_mass": snap["exploitative_strategy_mass"],
                        "containment_this_step": snap["containment_events_this_step"],
                        "collapse": collapse_pred(zw, total_mass),
                        "collapse_code": bool(snap["collapse"]),         # cross-check vs code's own flag
                    }
                    st["prev"] = prev
                    states.append(st)
                    prev = {"mean_welfare": st["mean_welfare"], "min_zone_welfare": st["min_zone_welfare"],
                            "resource_hhi": st["resource_hhi"], "capture_index": st["capture_index"],
                            "total_mass": st["total_mass"], "containment_this_step": st["containment_this_step"]}
    return states


# ---------------------------------------------------------------------------
# Step 1 — upward-closure of the unsafe set U under the natural badness order.
# ordering: s ⪯ s' ("s' at least as bad") iff
#   every zone welfare <= , total_mass <= , resource_hhi >= , capture_index >=
# ---------------------------------------------------------------------------
def worsen(state: dict, rng: random.Random) -> tuple[list[float], float, float, float]:
    """Perturb a state strictly toward 'worse' along the badness order."""
    zw = [max(0.0, w - rng.uniform(0.0, 0.15)) for w in state["zone_welfare"]]
    mass = max(0.0, state["total_mass"] * (1.0 - rng.uniform(0.0, 0.25)))
    hhi = min(1.0, state["resource_hhi"] + rng.uniform(0.0, 0.15))
    cap = min(1.0, state["capture_index"] + rng.uniform(0.0, 0.15))
    return zw, mass, hhi, cap


def upward_closure_report(states: list[dict], seed: int = 42, n_perturb: int = 20) -> dict:
    rng = random.Random(seed)
    u_states = [s for s in states if s["collapse"]]
    non_u = [s for s in states if not s["collapse"]]

    # If natural U-states are scarce, also construct near-boundary U-states by
    # scaling real welfare vectors down to just under the collapse threshold.
    constructed = []
    for s in rng.sample(non_u, min(len(non_u), 400)):
        scale = (WELFARE_MEAN_FLOOR - 0.02) / max(1e-6, s["mean_welfare"])
        if scale < 1.0:
            zw = [w * scale for w in s["zone_welfare"]]
            if collapse_pred(zw, s["total_mass"]):
                cs = dict(s)
                cs["zone_welfare"] = zw
                cs["mean_welfare"] = sum(zw) / len(zw)
                constructed.append(cs)

    test_u = u_states + constructed
    checked = 0
    stayed = 0
    counterexamples = []
    for s in test_u:
        for _ in range(n_perturb):
            zw, mass, hhi, cap = worsen(s, rng)
            checked += 1
            if collapse_pred(zw, mass):
                stayed += 1
            elif len(counterexamples) < 10:
                counterexamples.append({"from_mean_welfare": s["mean_welfare"],
                                        "worse_mean_welfare": sum(zw) / len(zw),
                                        "worse_total_mass": mass})

    # Does concentration ALONE define U? (it must not — U is a welfare/mass predicate)
    hi_conc_safe = sum(1 for s in states if s["resource_hhi"] >= 0.40 and not s["collapse"])
    lo_conc_unsafe = sum(1 for s in states if s["resource_hhi"] < 0.20 and s["collapse"])

    return {
        "ordering": "componentwise badness: zone_welfare<= , total_mass<= , resource_hhi>= , capture_index>=",
        "collapse_predicate": "mean(zone_welfare)<0.32 OR #{zone_welfare<0.20}>=4 OR total_mass<35",
        "n_states_total": len(states),
        "n_natural_U_states": len(u_states),
        "n_constructed_boundary_U_states": len(constructed),
        "n_upward_perturbations_checked": checked,
        "fraction_staying_in_U": (stayed / checked) if checked else 1.0,
        "counterexamples": counterexamples,
        "upward_closed": (checked == 0) or (stayed == checked),
        "concentration_alone_insufficient": {
            "high_concentration_but_safe_states": hi_conc_safe,
            "low_concentration_but_collapsed_states": lo_conc_unsafe,
            "note": "U is upward-closed only in an order that INCLUDES the welfare/mass "
                    "degradation coordinates; concentration alone does not define U.",
        },
        "code_flag_agreement_fraction": sum(1 for s in states if s["collapse"] == s["collapse_code"]) / max(1, len(states)),
    }


# ---------------------------------------------------------------------------
# Step 2 — sword reaction magnitude: is the per-step corrective reaction bounded?
# We measure per-step improvements (welfare up, concentration/capture down) and
# check no single step resets an unbounded amount.
# ---------------------------------------------------------------------------
def reaction_magnitude_report(states: list[dict]) -> dict:
    import statistics

    def deltas(active: bool):
        d_welf, d_hhi, d_cap, d_minw = [], [], [], []
        for s in states:
            pv = s["prev"]
            if pv is None:
                continue
            if (s["containment_this_step"] > 0) != active:
                continue
            d_welf.append(s["mean_welfare"] - pv["mean_welfare"])
            d_minw.append(s["min_zone_welfare"] - pv["min_zone_welfare"])
            d_hhi.append(s["resource_hhi"] - pv["resource_hhi"])
            d_cap.append(s["capture_index"] - pv["capture_index"])
        return d_welf, d_minw, d_hhi, d_cap

    def summ(xs, improving_sign):
        # improving_sign=+1: improvement = positive delta (welfare up); -1: improvement = negative delta (hhi/capture down)
        if not xs:
            return {"n": 0}
        improvements = [improving_sign * x for x in xs]
        return {
            "n": len(xs),
            "max_per_step_improvement": max(improvements),
            "max_abs_per_step_change": max(abs(x) for x in xs),
            "mean_change": statistics.fmean(xs),
            "p99_abs_change": sorted(abs(x) for x in xs)[int(0.99 * (len(xs) - 1))],
        }

    out = {}
    for active, label in [(True, "containment_active"), (False, "containment_inactive")]:
        dw, dmw, dhhi, dcap = deltas(active)
        out[label] = {
            "welfare_up": summ(dw, +1),
            "min_zone_welfare_up": summ(dmw, +1),
            "concentration_down": summ(dhhi, -1),
            "capture_down": summ(dcap, -1),
        }

    # Structural bound from code: per-step welfare gain from escrow <= 0.20 * raw_aid,
    # raw_aid <= BUDGET*alloc_cap = 6*0.32 ~ 1.92, clamped to [0,1]; concentration/aid
    # reductions are bounded multiplicative factors; no single step resets accumulated harm.
    active_w = out["containment_active"]["welfare_up"].get("max_per_step_improvement", 0.0)
    active_hhi = out["containment_active"]["concentration_down"].get("max_per_step_improvement", 0.0)
    bounded = (active_w <= 0.5) and (active_hhi <= 0.5)  # well under any "unbounded reset"
    return {
        "per_step_change_distributions": out,
        "structural_bound_note": "escrow welfare gain <= 0.20*raw_aid (raw_aid<=~1.92), all coords "
                                 "clamped to [0,1]; concentration/aid reductions are bounded "
                                 "multiplicative factors; accumulated-harm volumes are cumulative "
                                 "and never reset. => per-step reaction is bounded by construction.",
        "max_welfare_restoration_per_step_when_active": active_w,
        "max_concentration_reduction_per_step_when_active": active_hhi,
        "sword_reaction_bounded": bool(bounded),
        "unbounded_reset_observed": not bool(bounded),
    }
