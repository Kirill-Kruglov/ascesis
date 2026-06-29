#!/usr/bin/env python3
"""FA1.E1 false-safe witness taxonomy.

Diagnostic-only runner. It does not modify Justitia, the concrete collapse
predicate, or the 18.0 shield. It replays the BA1 baseline grid and records the
per-state information needed to classify false-safe witnesses by the smallest
missing semantic coordinate visible from BA4.1.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
JUSTITIA_MODEL = Path("/home/master/llm_projects/justitia/model")
SHIELD_SRC = Path("/home/master/llm_projects/ascesis/experiments/18_0_shield_synthesis/src")

for p in [JUSTITIA_MODEL, SHIELD_SRC]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import substrate as base  # noqa: E402
from shield import ShieldParams, compute_doomed  # noqa: E402


WELFARE_MEAN_FLOOR = 0.32
ZONE_WELFARE_FLOOR = 0.20
MASS_FLOOR = 35.0
SHIELD_PARAMS = ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)
DOOMED = compute_doomed(SHIELD_PARAMS, "bounded")["doomed"]


CLASS_META = {
    "spread_blind": {
        "candidate": "failed_zone_count >= 4",
        "eligible_layer": "L4 eligible",
        "kind": "aggregate_threshold",
    },
    "mass_blind": {
        "candidate": "total_mass < 35",
        "eligible_layer": "L4 eligible",
        "kind": "aggregate_threshold",
    },
    "mean_blind": {
        "candidate": "mean_welfare projection resolution",
        "eligible_layer": "L4 eligible",
        "kind": "variable_threshold_resolution",
    },
    "forward_dynamics_blind": {
        "candidate": "bounded future reachability / time-to-collapse",
        "eligible_layer": "L4 plus conditional L1 temporal",
        "kind": "temporal",
    },
    "history_blind": {
        "candidate": "delayed response_to_aid / neighbor_delta / last_aid",
        "eligible_layer": "conditional L2/L3",
        "kind": "temporal_policy_observation",
    },
    "control_blind": {
        "candidate": "containment_timer / policy-control state / allocation",
        "eligible_layer": "conditional L1/L2",
        "kind": "policy_control_invariant",
    },
    "policy_visible_concentration_blind": {
        "candidate": "Obs.resource_concentration > 0.62",
        "eligible_layer": "conditional L2/L3",
        "kind": "variable_threshold",
    },
    "layer_confusion_blind": {
        "candidate": "reporting/projection concentration or capture diagnostic",
        "eligible_layer": "L5 ineligible by default",
        "kind": "reporting_projection_diagnostic",
    },
    "unknown_or_mixed": {
        "candidate": "multiple or unresolved missing coordinates",
        "eligible_layer": "unknown/mixed",
        "kind": "mixed",
    },
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def rate(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def safe_mean(xs) -> float:
    return statistics.fmean(xs) if xs else 0.0


def shannon_from_counts(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    entropy = 0.0
    for c in counts.values():
        if c:
            p = c / total
            entropy -= p * math.log(p, 2)
    return entropy


def project(mean_welfare: float, resource_hhi: float) -> tuple[int, int]:
    deficit = max(0.0, 1.0 - mean_welfare)
    a = min(SHIELD_PARAMS.Amax, round(SHIELD_PARAMS.A_collapse * deficit / (1.0 - WELFARE_MEAN_FLOOR)))
    c = min(SHIELD_PARAMS.Cmax, round(resource_hhi * SHIELD_PARAMS.Cmax))
    return c, a


def shield_label(mean_welfare: float, resource_hhi: float) -> tuple[tuple[int, int], str]:
    abstract = project(mean_welfare, resource_hhi)
    return abstract, "DOOMED" if abstract in DOOMED else "SAFE"


def collapse_clauses(zone_welfare: list[float], total_mass: float) -> dict:
    mean_welfare = safe_mean(zone_welfare)
    failed = sum(1 for w in zone_welfare if w < ZONE_WELFARE_FLOOR)
    mean_clause = mean_welfare < WELFARE_MEAN_FLOOR
    spread_clause = failed >= 4
    mass_clause = total_mass < MASS_FLOOR
    return {
        "mean_clause": mean_clause,
        "spread_clause": spread_clause,
        "mass_clause": mass_clause,
        "collapse": bool(mean_clause or spread_clause or mass_clause),
        "mean_welfare": mean_welfare,
        "min_zone_welfare": min(zone_welfare) if zone_welfare else 0.0,
        "failed_zone_count": failed,
        "total_mass": total_mass,
    }


def collapse_clause_name(state: dict) -> str:
    names = []
    if state.get("mean_clause"):
        names.append("mean")
    if state.get("spread_clause"):
        names.append("spread")
    if state.get("mass_clause"):
        names.append("mass")
    return "+".join(names) if names else "none"


def summarize_tuple(xs) -> dict[str, float]:
    vals = list(xs) if xs is not None else []
    if not vals:
        return {"min": 0.0, "mean": 0.0, "max": 0.0}
    return {"min": min(vals), "mean": safe_mean(vals), "max": max(vals)}


def gini(xs: list[float]) -> float:
    vals = sorted(max(0.0, x) for x in xs)
    n = len(vals)
    total = sum(vals)
    if n == 0 or total <= 0:
        return 0.0
    weighted = sum((i + 1) * x for i, x in enumerate(vals))
    return (2 * weighted) / (n * total) - (n + 1) / n


def zone_welfare(model: base.EvolvableStrategyModel) -> list[float]:
    return [(z.wellness + z.productivity + z.recovery) / 3 for z in model.zones]


def zone_mass(model: base.EvolvableStrategyModel) -> list[float]:
    return [model._zone_mass(z) for z in model.zones]


def reporting_hhi(masses: list[float]) -> float:
    total = sum(masses) + base.EPS
    return sum((m / total) ** 2 for m in masses)


def exploit_share(model: base.EvolvableStrategyModel, total_mass: float) -> float:
    exploit = sum(l.mass for z in model.zones for l in z.lineages if model._exploit_score(l) > 0.42)
    return exploit / max(base.EPS, total_mass)


def coop_share(model: base.EvolvableStrategyModel, total_mass: float) -> float:
    coop = sum(l.mass for z in model.zones for l in z.lineages if model._cooperative_score(l) > 0.50)
    return coop / max(base.EPS, total_mass)


def capture_index(model: base.EvolvableStrategyModel, step: int, total_mass: float, resource_hhi: float) -> float:
    exploit = exploit_share(model, total_mass)
    coop = coop_share(model, total_mass)
    neighbor_harm = sum(z.neighbor_harm_volume for z in model.zones) / max(1, step + 1)
    aid_interception = sum(z.aid_interception_volume for z in model.zones) / max(1, step + 1)
    return clamp(
        0.22 * clamp((resource_hhi - 1.0 / base.ZONES) / 0.35)
        + 0.28 * clamp(exploit / 0.58)
        + 0.20 * clamp(neighbor_harm / 0.18)
        + 0.15 * clamp(aid_interception / 1.15)
        + 0.15 * clamp((0.42 - coop) / 0.42)
    )


def allocation_summary(alloc: list[float]) -> dict:
    return {
        "allocation_max": max(alloc) if alloc else 0.0,
        "allocation_min": min(alloc) if alloc else 0.0,
        "allocation_gini": gini(alloc),
    }


def obs_summary(obs: base.Obs | None) -> dict:
    if obs is None:
        return {
            "delayed_obs_step": -1,
            "delayed_obs_mean_welfare": 0.0,
            "delayed_obs_min_welfare": 0.0,
            "delayed_obs_failed_zone_count": 0,
            "obs_last_aid_max": 0.0,
            "obs_last_aid_mean": 0.0,
            "obs_response_to_aid_min": 0.0,
            "obs_response_to_aid_mean": 0.0,
            "obs_neighbor_delta_min": 0.0,
            "obs_neighbor_delta_mean": 0.0,
            "obs_resource_concentration_max": 0.0,
            "obs_resource_concentration_mean": 0.0,
            "bad_consequence_count": 0,
        }
    welfare = [(obs.wellness[i] + obs.productivity[i] + obs.recovery[i]) / 3 for i in range(len(obs.wellness))]
    aid = summarize_tuple(obs.last_aid)
    response = summarize_tuple(obs.response_to_aid)
    neighbor = summarize_tuple(obs.neighbor_delta)
    conc = summarize_tuple(obs.resource_concentration)
    bad_count = 0
    for i in range(len(obs.last_aid)):
        if obs.last_aid[i] > 0.035 and (
            obs.neighbor_delta[i] < -0.030
            or obs.response_to_aid[i] < -0.025
            or obs.resource_concentration[i] > 0.62
        ):
            bad_count += 1
    return {
        "delayed_obs_step": obs.step,
        "delayed_obs_mean_welfare": safe_mean(welfare),
        "delayed_obs_min_welfare": min(welfare) if welfare else 0.0,
        "delayed_obs_failed_zone_count": sum(1 for w in welfare if w < ZONE_WELFARE_FLOOR),
        "obs_last_aid_max": aid["max"],
        "obs_last_aid_mean": aid["mean"],
        "obs_response_to_aid_min": response["min"],
        "obs_response_to_aid_mean": response["mean"],
        "obs_neighbor_delta_min": neighbor["min"],
        "obs_neighbor_delta_mean": neighbor["mean"],
        "obs_resource_concentration_max": conc["max"],
        "obs_resource_concentration_mean": conc["mean"],
        "bad_consequence_count": bad_count,
    }


def containment_summary(model: base.EvolvableStrategyModel) -> dict:
    timers = [z.containment_timer for z in model.zones]
    return {
        "containment_active_count": sum(1 for t in timers if t > 0),
        "containment_timer_max": max(timers) if timers else 0,
        "containment_timer_sum": sum(timers),
        "containment_events_total": sum(z.containment_events for z in model.zones),
    }


def manual_step(model: base.EvolvableStrategyModel, step: int) -> tuple[base.Obs, list[float], int]:
    containment_before = sum(z.containment_events for z in model.zones)
    model._store_pre_step()
    model._apply_shocks(step)
    if model.params.mode == "audit":
        model._apply_audit_oracle()
    obs = model._delayed_obs()
    alloc = model.choose_alloc()
    for i, z in enumerate(model.zones):
        model._apply_zone_dynamics(z, base.BUDGET * alloc[i], alloc[i], obs, i)
    model._migrate()
    model._update_neighbor_metrics()
    model._update_irreversible(step)
    model.obs_queue.append(model._observe(step))
    containment_after = sum(z.containment_events for z in model.zones)
    return obs, alloc, containment_after - containment_before


def snapshot(model: base.EvolvableStrategyModel, step: int, obs: base.Obs, alloc: list[float], containment_this_step: int) -> dict:
    zw = zone_welfare(model)
    zm = zone_mass(model)
    total_mass = sum(zm)
    hhi = reporting_hhi(zm)
    clauses = collapse_clauses(zw, total_mass)
    abstract, label = shield_label(clauses["mean_welfare"], hhi)
    row = {
        "step": step,
        "zone_welfare": zw,
        "zone_mass": zm,
        "resource_hhi": hhi,
        "capture_index": capture_index(model, step, total_mass, hhi),
        "exploitative_strategy_mass": exploit_share(model, total_mass),
        "cooperative_strategy_mass": coop_share(model, total_mass),
        "current_collapse_clause": collapse_clause_name(clauses),
        "shield_c": abstract[0],
        "shield_a": abstract[1],
        "shield_abstract_state": f"({abstract[0]},{abstract[1]})",
        "shield_label": label,
        "shield_accept": label == "SAFE",
        "containment_events_this_step": containment_this_step,
        **clauses,
        **containment_summary(model),
        **obs_summary(obs),
        **allocation_summary(alloc),
    }
    row["collapse_code"] = bool(row["collapse"])
    return row


def harvest(worlds: list[str], policies: list[str], seeds: list[int], steps: int) -> list[dict]:
    states = []
    for world in worlds:
        for policy in policies:
            for seed in seeds:
                model = base.EvolvableStrategyModel(
                    seed,
                    base.Params(mode="governance", world=world, policy=policy),
                    record_trajectory=False,
                )
                traj_key = f"{world}|{policy}|{seed}"
                for step in range(steps):
                    obs, alloc, containment_this_step = manual_step(model, step)
                    st = snapshot(model, step, obs, alloc, containment_this_step)
                    st.update({
                        "run": "baseline",
                        "world": world,
                        "policy": policy,
                        "seed": seed,
                        "traj_key": traj_key,
                    })
                    states.append(st)
    return states


def augment_future(states: list[dict]) -> None:
    grouped = defaultdict(list)
    for s in states:
        grouped[s["traj_key"]].append(s)
    for seq in grouped.values():
        seq.sort(key=lambda s: s["step"])
        next_collapse_idx = None
        next_clause = "none"
        for i in range(len(seq) - 1, -1, -1):
            if seq[i]["collapse"]:
                next_collapse_idx = i
                next_clause = seq[i]["current_collapse_clause"]
            s = seq[i]
            s["future_collapse"] = next_collapse_idx is not None
            s["future_collapse_step"] = seq[next_collapse_idx]["step"] if next_collapse_idx is not None else ""
            s["first_collapse_clause_triggered"] = next_clause if next_collapse_idx is not None else "none"
            s["steps_to_future_collapse"] = (
                seq[next_collapse_idx]["step"] - s["step"] if next_collapse_idx is not None else ""
            )
            s["false_safe"] = bool(s["shield_accept"] and s["future_collapse"])


def classify_witness(s: dict) -> tuple[str, str, str]:
    if s["collapse"]:
        omitted = [name for name in ["spread", "mass", "mean"] if s[f"{name}_clause"]]
        if s["spread_clause"] and not s["mean_clause"] and not s["mass_clause"]:
            return "spread_blind", "high", "Current state already satisfies real spread-collapse clause, but 18.0 projection contains only mean-welfare/resource_hhi."
        if s["mass_clause"] and not s["mean_clause"] and not s["spread_clause"]:
            return "mass_blind", "high", "Current state already satisfies real mass-collapse clause, but total_mass is absent from 18.0 projection."
        if s["mean_clause"]:
            return "mean_blind", "medium", "Current state is mean-collapsed while shield still labels SAFE; this indicates projection/rounding boundary loss."
        return "unknown_or_mixed", "medium", f"Current state is collapsed by multiple omitted clauses: {','.join(omitted)}."

    history_signal = (
        s["obs_last_aid_max"] > 0.035
        and (s["obs_neighbor_delta_min"] < -0.030 or s["obs_response_to_aid_min"] < -0.025)
    )
    concentration_signal = s["obs_last_aid_max"] > 0.035 and s["obs_resource_concentration_max"] > 0.62
    control_signal = (
        s["containment_active_count"] > 0
        or s["containment_events_this_step"] > 0
        or (s["policy"] in {"action_channel_containment", "consequence_plus_diversity"} and s["bad_consequence_count"] > 0)
    )
    reporting_only_signal = (
        s["capture_index"] > 0.65
        or (s["resource_hhi"] > 0.28 and not concentration_signal)
    )

    signals = sum(1 for v in [history_signal, concentration_signal, control_signal, reporting_only_signal] if v)
    if signals > 1:
        return "unknown_or_mixed", "medium", "Future collapse state has multiple plausible missing coordinates, so no single minimal candidate is defensible."
    if control_signal:
        return "control_blind", "medium", "Current state is not collapsed, but policy/control state is active or triggering and is absent from the 18.0 projection."
    if concentration_signal:
        return "policy_visible_concentration_blind", "medium", "Delayed policy-visible resource concentration crosses the bad-consequence threshold, distinct from reporting HHI."
    if history_signal:
        return "history_blind", "medium", "Delayed response/neighbor/last-aid history carries a harmful consequence signal absent from the 18.0 projection."
    if reporting_only_signal:
        return "layer_confusion_blind", "low", "The available explanatory signal is a reporting/projection diagnostic rather than a clean transition/collapse coordinate."
    return "forward_dynamics_blind", "high", "Current concrete state is not collapsed; false-safe status comes from later concrete collapse under future dynamics."


def witness_rows(states: list[dict]) -> list[dict]:
    rows = []
    for s in states:
        if not s["false_safe"]:
            continue
        cls, confidence, reason = classify_witness(s)
        meta = CLASS_META[cls]
        rows.append({
            "run": s["run"],
            "world": s["world"],
            "policy": s["policy"],
            "seed": s["seed"],
            "step": s["step"],
            "current_mean_clause": int(s["mean_clause"]),
            "current_spread_clause": int(s["spread_clause"]),
            "current_mass_clause": int(s["mass_clause"]),
            "current_collapse_clause": s["current_collapse_clause"],
            "future_collapse_step": s["future_collapse_step"],
            "first_collapse_clause_triggered": s["first_collapse_clause_triggered"],
            "shield_abstract_state": s["shield_abstract_state"],
            "shield_c": s["shield_c"],
            "shield_a": s["shield_a"],
            "shield_label": s["shield_label"],
            "mean_welfare": round(s["mean_welfare"], 8),
            "failed_zone_count": s["failed_zone_count"],
            "total_mass": round(s["total_mass"], 8),
            "min_zone_welfare": round(s["min_zone_welfare"], 8),
            "resource_hhi": round(s["resource_hhi"], 8),
            "capture_index": round(s["capture_index"], 8),
            "containment_active_count": s["containment_active_count"],
            "containment_timer_max": s["containment_timer_max"],
            "containment_timer_sum": s["containment_timer_sum"],
            "containment_events_this_step": s["containment_events_this_step"],
            "delayed_obs_step": s["delayed_obs_step"],
            "delayed_obs_mean_welfare": round(s["delayed_obs_mean_welfare"], 8),
            "delayed_obs_min_welfare": round(s["delayed_obs_min_welfare"], 8),
            "delayed_obs_failed_zone_count": s["delayed_obs_failed_zone_count"],
            "obs_last_aid_max": round(s["obs_last_aid_max"], 8),
            "obs_last_aid_mean": round(s["obs_last_aid_mean"], 8),
            "obs_response_to_aid_min": round(s["obs_response_to_aid_min"], 8),
            "obs_response_to_aid_mean": round(s["obs_response_to_aid_mean"], 8),
            "obs_neighbor_delta_min": round(s["obs_neighbor_delta_min"], 8),
            "obs_neighbor_delta_mean": round(s["obs_neighbor_delta_mean"], 8),
            "obs_resource_concentration_max": round(s["obs_resource_concentration_max"], 8),
            "obs_resource_concentration_mean": round(s["obs_resource_concentration_mean"], 8),
            "bad_consequence_count": s["bad_consequence_count"],
            "allocation_max": round(s["allocation_max"], 8),
            "allocation_min": round(s["allocation_min"], 8),
            "allocation_gini": round(s["allocation_gini"], 8),
            "steps_to_future_collapse": s["steps_to_future_collapse"],
            "assigned_witness_class": cls,
            "minimal_missing_information_candidate": meta["candidate"],
            "eligible_layer_from_BA4_1": meta["eligible_layer"],
            "candidate_kind": meta["kind"],
            "confidence": confidence,
            "reason": reason,
        })
    return rows


def summarize(states: list[dict], witnesses: list[dict]) -> dict:
    n = len(states)
    safe = sum(1 for s in states if s["shield_accept"])
    false_safe = len(witnesses)
    cls_counts = Counter(w["assigned_witness_class"] for w in witnesses)
    for cls in CLASS_META:
        cls_counts.setdefault(cls, 0)
    per_policy = {}
    for policy in sorted({s["policy"] for s in states}):
        ps = [s for s in states if s["policy"] == policy]
        pfs = [s for s in ps if s["false_safe"]]
        per_policy[policy] = {
            "n_states": len(ps),
            "n_safe": sum(1 for s in ps if s["shield_accept"]),
            "false_safe_count": len(pfs),
            "false_safe_rate_over_safe": rate(len(pfs), sum(1 for s in ps if s["shield_accept"])),
        }
    per_policy_class = defaultdict(Counter)
    for w in witnesses:
        per_policy_class[w["policy"]][w["assigned_witness_class"]] += 1
    return {
        "n_states": n,
        "n_safe": safe,
        "n_doomed": n - safe,
        "shield_acceptance_rate": rate(safe, n),
        "current_collapse_rate": rate(sum(1 for s in states if s["collapse"]), n),
        "future_collapse_rate": rate(sum(1 for s in states if s["future_collapse"]), n),
        "total_false_safe_witnesses": false_safe,
        "false_safe_rate_over_safe": rate(false_safe, safe),
        "false_safe_due_current_collapse": sum(1 for w in witnesses if w["current_collapse_clause"] != "none"),
        "false_safe_due_forward_dynamics": sum(1 for w in witnesses if w["current_collapse_clause"] == "none"),
        "class_counts": dict(cls_counts),
        "class_fractions": {k: rate(v, false_safe) for k, v in cls_counts.items()},
        "omitted_real_collapse_clause_witnesses_spread_plus_mass": cls_counts["spread_blind"] + cls_counts["mass_blind"],
        "history_control_information_witnesses": (
            cls_counts["history_blind"]
            + cls_counts["control_blind"]
            + cls_counts["policy_visible_concentration_blind"]
        ),
        "layer_confusion_witnesses": cls_counts["layer_confusion_blind"],
        "unknown_or_mixed_fraction": rate(cls_counts["unknown_or_mixed"], false_safe),
        "class_entropy_bits": shannon_from_counts(cls_counts),
        "per_policy": per_policy,
        "per_policy_class_counts": {p: dict(c) for p, c in per_policy_class.items()},
    }


def candidate_rows(witnesses: list[dict]) -> list[dict]:
    counts = Counter(w["minimal_missing_information_candidate"] for w in witnesses)
    rows = []
    total = len(witnesses)
    acc = 0
    for rank, (candidate, count) in enumerate(counts.most_common(), start=1):
        acc += count
        rows.append({
            "rank": rank,
            "minimal_missing_information_candidate": candidate,
            "count": count,
            "fraction": rate(count, total),
            "cumulative_count": acc,
            "cumulative_fraction": rate(acc, total),
        })
    return rows


def layer_rows(witnesses: list[dict]) -> list[dict]:
    counts = Counter(w["eligible_layer_from_BA4_1"] for w in witnesses)
    total = len(witnesses)
    return [
        {
            "eligible_layer_from_BA4_1": layer,
            "count": count,
            "fraction": rate(count, total),
        }
        for layer, count in counts.most_common()
    ]


def decide(summary: dict, candidates: list[dict]) -> dict:
    total = summary["total_false_safe_witnesses"]
    cls = Counter(summary["class_counts"])
    omitted = summary["omitted_real_collapse_clause_witnesses_spread_plus_mass"]
    dynamics = cls["forward_dynamics_blind"]
    history_control = summary["history_control_information_witnesses"]
    top3 = candidates[2]["cumulative_fraction"] if len(candidates) >= 3 else (candidates[-1]["cumulative_fraction"] if candidates else 0.0)
    mostly_layer_ineligible = rate(summary["layer_confusion_witnesses"], total) > 0.35
    unknown_high = summary["unknown_or_mixed_fraction"] > 0.25

    if total == 0:
        case = "Case E — Inconclusive"
        interp = "No false-safe witnesses were extracted."
    elif rate(omitted, total) > 0.50:
        case = "Case A — Collapse_clause_dominant"
        interp = "Most false-safe witnesses are explained by omitted real collapse clauses."
    elif rate(dynamics, total) > 0.50:
        case = "Case B — Dynamics_dominant"
        interp = "Most false-safe witnesses require forward-dynamics information beyond current collapse clauses."
    elif rate(history_control, total) > 0.35:
        case = "Case C — History_control_dominant"
        interp = "A large fraction requires delayed observation, policy-visible concentration, or control state."
    elif top3 < 0.60 or mostly_layer_ineligible or unknown_high:
        case = "Case D — Mixed_information"
        interp = "No compact set of layer-eligible candidates covers the majority."
    else:
        case = "Case E — Inconclusive"
        interp = "Extracted evidence does not cleanly satisfy a dominant case."

    h_fa1 = "supported" if case in {"Case A — Collapse_clause_dominant", "Case B — Dynamics_dominant", "Case C — History_control_dominant"} else "weakened_or_inconclusive"
    return {
        "classification": case,
        "interpretation": interp,
        "H_FA1_assessment": h_fa1,
        "falsification_checks": {
            "top3_candidate_coverage": top3,
            "unknown_or_mixed_fraction": summary["unknown_or_mixed_fraction"],
            "layer_ineligible_fraction": rate(summary["layer_confusion_witnesses"], total),
            "class_entropy_bits": summary["class_entropy_bits"],
            "policy_class_counts": summary["per_policy_class_counts"],
        },
        "do_not_claim_safety": True,
        "do_not_propose_new_shield": True,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def example_table(rows: list[dict], limit: int = 3) -> list[str]:
    lines = [
        "| class | world | policy | seed | step | current clause | future step | first future clause | candidate | confidence | reason |",
        "|---|---|---|---:|---:|---|---:|---|---|---|---|",
    ]
    for r in rows[:limit]:
        lines.append(
            f"| {r['assigned_witness_class']} | {r['world']} | {r['policy']} | {r['seed']} | {r['step']} | "
            f"{r['current_collapse_clause']} | {r['future_collapse_step']} | {r['first_collapse_clause_triggered']} | "
            f"{r['minimal_missing_information_candidate']} | {r['confidence']} | {r['reason']} |"
        )
    return lines


def write_representatives(path: Path, witnesses: list[dict]) -> None:
    by_class = defaultdict(list)
    for w in witnesses:
        by_class[w["assigned_witness_class"]].append(w)
    lines = ["# Representative False-Safe Witnesses", ""]
    for cls in CLASS_META:
        rows = by_class.get(cls, [])
        lines += [f"## {cls}", "", f"Count: `{len(rows)}`.", ""]
        if rows:
            lines += example_table(rows, limit=3)
            lines.append("")
        else:
            lines += ["No witnesses assigned to this class.", ""]
    path.write_text("\n".join(lines) + "\n")


def write_ambiguous(path: Path, witnesses: list[dict]) -> None:
    amb = [w for w in witnesses if w["assigned_witness_class"] in {"unknown_or_mixed", "layer_confusion_blind"} or w["confidence"] == "low"]
    lines = [
        "# Ambiguous / Layer-Confusion Witnesses",
        "",
        f"Ambiguous or low-confidence witness count: `{len(amb)}`.",
        "",
    ]
    if amb:
        lines += example_table(amb, limit=20)
        lines.append("")
    else:
        lines.append("No ambiguous or low-confidence witnesses were extracted.")
    path.write_text("\n".join(lines) + "\n")


def write_final_report(path: Path, summary: dict, candidates: list[dict], layers: list[dict], assessment: dict) -> None:
    lines = [
        "# FA1.E1 False-Safe Witness Taxonomy",
        "",
        "Diagnostic-only experiment. Justitia source, concrete collapse definition, and the 18.0 shield were not modified.",
        "",
        "## Decision",
        "",
        f"Classification: **{assessment['classification']}**.",
        f"Interpretation: {assessment['interpretation']}",
        f"H_FA1 assessment: `{assessment['H_FA1_assessment']}`.",
        "",
        "## Baseline Extraction",
        "",
        f"- States harvested: `{summary['n_states']}`.",
        f"- Shield SAFE states: `{summary['n_safe']}` (`{summary['shield_acceptance_rate']:.6f}`).",
        f"- Future-collapse states: `{summary['future_collapse_rate']:.6f}`.",
        f"- False-safe witnesses: `{summary['total_false_safe_witnesses']}` (`{summary['false_safe_rate_over_safe']:.6f}` over SAFE states).",
        f"- Current-collapse false-safe witnesses: `{summary['false_safe_due_current_collapse']}`.",
        f"- Future-dynamics false-safe witnesses: `{summary['false_safe_due_forward_dynamics']}`.",
        "",
        "## Witness Classes",
        "",
        "| class | count | fraction |",
        "|---|---:|---:|",
    ]
    for cls, count in sorted(summary["class_counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {cls} | {count} | {summary['class_fractions'][cls]:.6f} |")
    lines += [
        "",
        "## Primary Metrics",
        "",
        f"- Omitted real collapse clauses (`spread_blind + mass_blind`): `{summary['omitted_real_collapse_clause_witnesses_spread_plus_mass']}`.",
        f"- History/control/concentration witnesses: `{summary['history_control_information_witnesses']}`.",
        f"- Layer-confusion witnesses: `{summary['layer_confusion_witnesses']}`.",
        f"- Unknown/mixed fraction: `{summary['unknown_or_mixed_fraction']:.6f}`.",
        f"- Class entropy: `{summary['class_entropy_bits']:.6f}` bits.",
        "",
        "## Minimal Information Candidates",
        "",
        "| rank | candidate | count | fraction | cumulative fraction |",
        "|---:|---|---:|---:|---:|",
    ]
    for row in candidates:
        lines.append(
            f"| {row['rank']} | {row['minimal_missing_information_candidate']} | {row['count']} | "
            f"{row['fraction']:.6f} | {row['cumulative_fraction']:.6f} |"
        )
    lines += [
        "",
        "## BA4.1 Layer Eligibility",
        "",
        "| layer eligibility | count | fraction |",
        "|---|---:|---:|",
    ]
    for row in layers:
        lines.append(f"| {row['eligible_layer_from_BA4_1']} | {row['count']} | {row['fraction']:.6f} |")
    lines += [
        "",
        "## Falsification Checks",
        "",
        f"- Top-3 candidate coverage: `{assessment['falsification_checks']['top3_candidate_coverage']:.6f}`.",
        f"- Unknown/mixed fraction: `{assessment['falsification_checks']['unknown_or_mixed_fraction']:.6f}`.",
        f"- Layer-ineligible fraction: `{assessment['falsification_checks']['layer_ineligible_fraction']:.6f}`.",
        "",
        "No safety claim is made here. This experiment maps missing information only; it does not synthesize or recommend a new shield.",
    ]
    path.write_text("\n".join(lines) + "\n")


def write_notes(path: Path, args, summary: dict) -> None:
    lines = [
        "# FA1.E1 Implementation Notes",
        "",
        "- Replayed the BA1 baseline Justitia grid with `mode='governance'` only.",
        "- The transition loop mirrors `EvolvableStrategyModel.step` but exposes delayed observation, allocation, and control summaries per step.",
        "- Shield projection uses 18.0 `ShieldParams(A_collapse=40, trig=34, K=1, Rc=1, Ra=2, Cmax=44, Amax=44)` and `compute_doomed(..., 'bounded')` unchanged.",
        "- Concrete collapse predicate is unchanged: mean zone welfare `< 0.32`, or failed-zone count `>= 4` using zone welfare `< 0.20`, or total mass `< 35`.",
        "- Classification is conservative: current omitted collapse clauses are assigned first; future-collapse cases are assigned to history/control/concentration only when explicit BA4.1 policy/control signals are active.",
        "- `capture_index` and reporting `resource_hhi` are treated as low-confidence layer-confusion evidence, not as transition mechanisms.",
        "",
        "## Run Configuration",
        "",
        f"- worlds: `{args.worlds}`",
        f"- policies: `{args.policies}`",
        f"- seeds: `{args.seeds}`",
        f"- steps: `{args.steps}`",
        "",
        "## BA1 Consistency",
        "",
        f"- Extracted false-safe count: `{summary['total_false_safe_witnesses']}`.",
        f"- Extracted shield acceptance rate: `{summary['shield_acceptance_rate']:.6f}`.",
        f"- Extracted future collapse rate: `{summary['future_collapse_rate']:.6f}`.",
    ]
    path.write_text("\n".join(lines) + "\n")


def parse_csv_list(value: str, default: list[str]) -> list[str]:
    if value == "all":
        return default
    return [x.strip() for x in value.split(",") if x.strip()]


def parse_seeds(value: str) -> list[int]:
    if ".." in value:
        a, b = value.split("..", 1)
        return list(range(int(a), int(b) + 1))
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worlds", default="all")
    parser.add_argument("--policies", default="all")
    parser.add_argument("--seeds", default="9600..9607")
    parser.add_argument("--steps", type=int, default=base.STEPS)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    worlds = parse_csv_list(args.worlds, list(base.WORLDS))
    policies = parse_csv_list(args.policies, list(base.POLICIES))
    seeds = parse_seeds(args.seeds)

    states = harvest(worlds, policies, seeds, args.steps)
    augment_future(states)
    witnesses = witness_rows(states)
    summary = summarize(states, witnesses)
    candidates = candidate_rows(witnesses)
    layers = layer_rows(witnesses)
    assessment = decide(summary, candidates)

    write_csv(OUT / "witness_taxonomy.csv", witnesses)
    write_json(OUT / "witness_class_summary.json", summary)
    write_csv(OUT / "minimal_information_candidates.csv", candidates)
    write_csv(OUT / "layer_eligibility_summary.csv", layers)
    write_representatives(OUT / "representative_witnesses.md", witnesses)
    write_ambiguous(OUT / "ambiguous_witnesses.md", witnesses)
    write_json(OUT / "hypothesis_assessment.json", assessment)
    write_final_report(OUT / "final_report.md", summary, candidates, layers, assessment)
    write_notes(OUT / "implementation_notes.md", args, summary)

    print(json.dumps({
        "classification": assessment["classification"],
        "H_FA1_assessment": assessment["H_FA1_assessment"],
        "total_false_safe_witnesses": summary["total_false_safe_witnesses"],
        "false_safe_due_current_collapse": summary["false_safe_due_current_collapse"],
        "false_safe_due_forward_dynamics": summary["false_safe_due_forward_dynamics"],
        "class_counts": summary["class_counts"],
        "top_candidate": candidates[0] if candidates else None,
        "outputs": str(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
