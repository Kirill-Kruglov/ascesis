#!/usr/bin/env python3
"""FA2.E1 minimal invariant compression test.

This runner consumes FA1.E1 false-safe witness outputs only. It does not run
Justitia, modify the concrete collapse predicate, modify the 18.0 shield, or
claim safety. It measures whether the extracted false-safe witnesses are covered
by a compact ordered set of missing-information invariants.
"""
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
ASCESIS = Path("/home/master/llm_projects/ascesis")
FA1_OUT = ASCESIS / "experiments/FA1_E1_false_safe_witness_taxonomy/outputs"


def f(row: dict, key: str, default: float = 0.0) -> float:
    value = row.get(key, "")
    if value == "" or value is None:
        return default
    return float(value)


def b(row: dict, key: str) -> bool:
    return str(row.get(key, "0")) in {"1", "true", "True"}


def rate(num: int | float, den: int | float) -> float:
    return float(num) / float(den) if den else 0.0


def read_witnesses() -> list[dict]:
    path = FA1_OUT / "witness_taxonomy.csv"
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def invariant_catalog() -> list[dict]:
    return [
        {
            "id": "I1a",
            "family": "I1_omitted_collapse_clauses",
            "name": "failed_zone_count >= 4",
            "definition": "current_spread_clause == 1",
            "coordinate_count": 1,
            "coordinate_type": "count_threshold",
            "layer_eligibility": "L4 eligible",
            "oracle": "no",
            "estimated_state_space_blowup": "x2 if Boolean; up to x10 if count 0..9 retained",
            "wsts_compatibility_risk": "low",
            "monotonicity_risk": "low",
            "circularity_risk": "none",
            "expected_class": "spread_blind",
        },
        {
            "id": "I1b",
            "family": "I1_omitted_collapse_clauses",
            "name": "total_mass < 35",
            "definition": "current_mass_clause == 1",
            "coordinate_count": 1,
            "coordinate_type": "aggregate_threshold",
            "layer_eligibility": "L4 eligible",
            "oracle": "no",
            "estimated_state_space_blowup": "x2 if Boolean; larger if mass bucket retained",
            "wsts_compatibility_risk": "low",
            "monotonicity_risk": "low",
            "circularity_risk": "none",
            "expected_class": "mass_blind",
        },
        {
            "id": "I2",
            "family": "I2_policy_visible_concentration",
            "name": "Obs.resource_concentration > 0.62 after aid",
            "definition": "obs_last_aid_max > 0.035 and obs_resource_concentration_max > 0.62",
            "coordinate_count": 1,
            "coordinate_type": "policy_visible_threshold",
            "layer_eligibility": "conditional L2/L3",
            "oracle": "no",
            "estimated_state_space_blowup": "x2 for threshold flag; xN if concentration bucket retained",
            "wsts_compatibility_risk": "medium",
            "monotonicity_risk": "medium",
            "circularity_risk": "none",
            "expected_class": "policy_visible_concentration_blind",
        },
        {
            "id": "I3",
            "family": "I3_history_delayed_consequence",
            "name": "delayed harmful response/neighbor signal after aid",
            "definition": "obs_last_aid_max > 0.035 and (obs_neighbor_delta_min < -0.030 or obs_response_to_aid_min < -0.025)",
            "coordinate_count": 2,
            "coordinate_type": "history_threshold",
            "layer_eligibility": "conditional L2/L3",
            "oracle": "no",
            "estimated_state_space_blowup": "x4 for two Boolean flags; larger if delayed values bucketed",
            "wsts_compatibility_risk": "medium",
            "monotonicity_risk": "high",
            "circularity_risk": "none",
            "expected_class": "history_blind",
        },
        {
            "id": "I4_oracle",
            "family": "I4_temporal_oracle",
            "name": "oracle future collapse / time-to-collapse exists",
            "definition": "steps_to_future_collapse is finite and current_collapse_clause == none",
            "coordinate_count": 1,
            "coordinate_type": "temporal_oracle",
            "layer_eligibility": "L4 plus conditional L1 temporal",
            "oracle": "yes",
            "estimated_state_space_blowup": "x2 for oracle reachability label; unbounded if exact time retained",
            "wsts_compatibility_risk": "high",
            "monotonicity_risk": "high",
            "circularity_risk": "high",
            "expected_class": "forward_dynamics_blind",
        },
        {
            "id": "I4_proxy",
            "family": "I4_temporal_non_oracle_proxy",
            "name": "current minimum-zone-welfare risk band",
            "definition": "min_zone_welfare <= 0.96",
            "coordinate_count": 1,
            "coordinate_type": "current_state_threshold_proxy",
            "layer_eligibility": "L4 eligible, but proxy threshold is empirical",
            "oracle": "no",
            "estimated_state_space_blowup": "x2 for threshold flag",
            "wsts_compatibility_risk": "medium",
            "monotonicity_risk": "low",
            "circularity_risk": "low",
            "expected_class": "forward_dynamics_blind",
        },
        {
            "id": "I5",
            "family": "I5_mixed_resolver",
            "name": "I2 or I3 mixed resolver",
            "definition": "unknown_or_mixed witness covered by already-added I2 or I3 predicates",
            "coordinate_count": 0,
            "coordinate_type": "combination",
            "layer_eligibility": "inherits I2/I3 conditional L2/L3",
            "oracle": "no",
            "estimated_state_space_blowup": "none beyond I2/I3",
            "wsts_compatibility_risk": "medium",
            "monotonicity_risk": "high",
            "circularity_risk": "none",
            "expected_class": "unknown_or_mixed",
        },
    ]


def predicate(inv_id: str, row: dict) -> bool:
    if inv_id == "I1a":
        return b(row, "current_spread_clause")
    if inv_id == "I1b":
        return b(row, "current_mass_clause")
    if inv_id == "I2":
        return f(row, "obs_last_aid_max") > 0.035 and f(row, "obs_resource_concentration_max") > 0.62
    if inv_id == "I3":
        return f(row, "obs_last_aid_max") > 0.035 and (
            f(row, "obs_neighbor_delta_min") < -0.030 or f(row, "obs_response_to_aid_min") < -0.025
        )
    if inv_id == "I4_oracle":
        return row.get("current_collapse_clause") == "none" and row.get("steps_to_future_collapse", "") != ""
    if inv_id == "I4_proxy":
        return f(row, "min_zone_welfare") <= 0.96
    if inv_id == "I5":
        return row.get("assigned_witness_class") == "unknown_or_mixed" and (predicate("I2", row) or predicate("I3", row))
    raise KeyError(inv_id)


def coverage(rows: list[dict], inv_ids: list[str]) -> set[int]:
    covered = set()
    for i, row in enumerate(rows):
        if any(predicate(inv_id, row) for inv_id in inv_ids):
            covered.add(i)
    return covered


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def refinement_defs() -> list[dict]:
    return [
        {
            "id": "R0",
            "description": "current 18.0 abstraction only",
            "invariants": [],
            "oracle": "no",
        },
        {
            "id": "R1",
            "description": "R0 + I1 omitted collapse clauses",
            "invariants": ["I1a", "I1b"],
            "oracle": "no",
        },
        {
            "id": "R2",
            "description": "R1 + I2 policy-visible concentration",
            "invariants": ["I1a", "I1b", "I2"],
            "oracle": "no",
        },
        {
            "id": "R3",
            "description": "R2 + I3 compact history/delayed consequence",
            "invariants": ["I1a", "I1b", "I2", "I3"],
            "oracle": "no",
        },
        {
            "id": "R4-oracle",
            "description": "R3 + I4 oracle temporal reachability",
            "invariants": ["I1a", "I1b", "I2", "I3", "I4_oracle"],
            "oracle": "yes",
        },
        {
            "id": "R4-proxy",
            "description": "R3 + I4 non-oracle current minimum-zone-welfare proxy",
            "invariants": ["I1a", "I1b", "I2", "I3", "I4_proxy"],
            "oracle": "no",
        },
        {
            "id": "R5",
            "description": "R4-proxy + best compact mixed resolver",
            "invariants": ["I1a", "I1b", "I2", "I3", "I4_proxy", "I5"],
            "oracle": "no",
        },
    ]


def count_coordinates(inv_ids: list[str], catalog_by_id: dict[str, dict]) -> int:
    return sum(int(catalog_by_id[inv_id]["coordinate_count"]) for inv_id in inv_ids)


def combined_type(inv_ids: list[str], catalog_by_id: dict[str, dict]) -> str:
    vals = []
    for inv_id in inv_ids:
        vals.append(catalog_by_id[inv_id]["coordinate_type"])
    return "; ".join(vals) if vals else "none"


def combined_layer(inv_ids: list[str], catalog_by_id: dict[str, dict]) -> str:
    vals = []
    for inv_id in inv_ids:
        val = catalog_by_id[inv_id]["layer_eligibility"]
        if val not in vals:
            vals.append(val)
    return "; ".join(vals) if vals else "current 18.0 only"


def max_risk(inv_ids: list[str], catalog_by_id: dict[str, dict], key: str) -> str:
    order = {"none": 0, "low": 1, "medium": 2, "high": 3}
    if not inv_ids:
        return "none"
    risks = [catalog_by_id[inv_id][key] for inv_id in inv_ids]
    return max(risks, key=lambda x: order.get(x, 0))


def refinement_rows(rows: list[dict], catalog: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    catalog_by_id = {r["id"]: r for r in catalog}
    total = len(rows)
    parent = {
        "R0": None,
        "R1": "R0",
        "R2": "R1",
        "R3": "R2",
        "R4-oracle": "R3",
        "R4-proxy": "R3",
        "R5": "R4-proxy",
    }
    covered_by_refinement: dict[str, set[int]] = {}
    coords_by_refinement: dict[str, int] = {}
    coverage_rows = []
    refinement_set_rows = []
    residual_rows = []
    for ref in refinement_defs():
        invs = ref["invariants"]
        cov = coverage(rows, invs)
        parent_id = parent[ref["id"]]
        parent_cov = covered_by_refinement.get(parent_id, set()) if parent_id else set()
        parent_coords = coords_by_refinement.get(parent_id, 0) if parent_id else 0
        newly = cov - parent_cov
        residual = set(range(total)) - cov
        residual_unknown = sum(1 for i in residual if rows[i]["assigned_witness_class"] == "unknown_or_mixed")
        coords = count_coordinates(invs, catalog_by_id)
        coverage_rows.append({
            "refinement_set": ref["id"],
            "description": ref["description"],
            "invariants": ";".join(invs) if invs else "none",
            "witness_coverage_count": len(cov),
            "witness_coverage_fraction": rate(len(cov), total),
            "newly_covered_witnesses": len(newly),
            "residual_witnesses": len(residual),
            "residual_unknown_mixed": residual_unknown,
            "number_invariant_coordinates_added": coords,
            "coordinate_type": combined_type(invs, catalog_by_id),
            "layer_eligibility": combined_layer(invs, catalog_by_id),
            "oracle": ref["oracle"],
            "estimated_state_space_blowup": " * ".join(catalog_by_id[i]["estimated_state_space_blowup"] for i in invs) if invs else "none",
            "wsts_compatibility_risk": max_risk(invs, catalog_by_id, "wsts_compatibility_risk"),
            "monotonicity_risk": max_risk(invs, catalog_by_id, "monotonicity_risk"),
            "circularity_risk": max_risk(invs, catalog_by_id, "circularity_risk"),
            "compression_ratio": rate(len(cov), coords),
            "marginal_compression_ratio": rate(len(newly), max(1, coords - parent_coords)),
        })
        refinement_set_rows.append({
            "refinement_set": ref["id"],
            "description": ref["description"],
            "invariants": ";".join(invs) if invs else "none",
            "coordinate_count": coords,
            "oracle": ref["oracle"],
        })
        if ref["id"] in {"R3", "R4-proxy", "R4-oracle"}:
            for i in sorted(residual):
                residual_rows.append({
                    "after_refinement_set": ref["id"],
                    "world": rows[i]["world"],
                    "policy": rows[i]["policy"],
                    "seed": rows[i]["seed"],
                    "step": rows[i]["step"],
                    "assigned_witness_class": rows[i]["assigned_witness_class"],
                    "current_collapse_clause": rows[i]["current_collapse_clause"],
                    "future_collapse_step": rows[i]["future_collapse_step"],
                    "first_collapse_clause_triggered": rows[i]["first_collapse_clause_triggered"],
                    "mean_welfare": rows[i]["mean_welfare"],
                    "min_zone_welfare": rows[i]["min_zone_welfare"],
                    "failed_zone_count": rows[i]["failed_zone_count"],
                    "total_mass": rows[i]["total_mass"],
                    "obs_resource_concentration_max": rows[i]["obs_resource_concentration_max"],
                    "obs_neighbor_delta_min": rows[i]["obs_neighbor_delta_min"],
                    "obs_response_to_aid_min": rows[i]["obs_response_to_aid_min"],
                    "obs_last_aid_max": rows[i]["obs_last_aid_max"],
                })
        covered_by_refinement[ref["id"]] = cov
        coords_by_refinement[ref["id"]] = coords
    return refinement_set_rows, coverage_rows, residual_rows


def marginal_rows(rows: list[dict], catalog: list[dict]) -> list[dict]:
    total = len(rows)
    previous = set()
    out = []
    ordered = ["I1a", "I1b", "I2", "I3", "I4_proxy", "I4_oracle", "I5"]
    by_id = {r["id"]: r for r in catalog}
    for inv_id in ordered:
        cov = coverage(rows, [inv_id])
        new = cov - previous
        coords = int(by_id[inv_id]["coordinate_count"])
        class_counts = Counter(rows[i]["assigned_witness_class"] for i in new)
        out.append({
            "invariant_id": inv_id,
            "invariant_name": by_id[inv_id]["name"],
            "standalone_coverage_count": len(cov),
            "standalone_coverage_fraction": rate(len(cov), total),
            "marginal_coverage_count_in_order": len(new),
            "marginal_coverage_fraction_in_order": rate(len(new), total),
            "coordinate_count": coords,
            "marginal_compression_ratio": rate(len(new), max(1, coords)),
            "new_class_counts": json.dumps(dict(class_counts), sort_keys=True),
            "oracle": by_id[inv_id]["oracle"],
            "layer_eligibility": by_id[inv_id]["layer_eligibility"],
        })
        previous |= cov
    return out


def temporal_oracle_analysis(rows: list[dict]) -> dict:
    future_rows = [r for r in rows if r["current_collapse_clause"] == "none"]
    steps = [int(float(r["steps_to_future_collapse"])) for r in future_rows if r.get("steps_to_future_collapse", "") != ""]
    by_class = Counter(r["assigned_witness_class"] for r in future_rows)
    return {
        "oracle_invariant": "steps_to_future_collapse is finite and current_collapse_clause == none",
        "covers_current_not_collapsed_false_safe_witnesses": len(future_rows),
        "coverage_fraction_all_witnesses": rate(len(future_rows), len(rows)),
        "class_counts": dict(by_class),
        "steps_to_collapse_min": min(steps) if steps else None,
        "steps_to_collapse_median": statistics.median(steps) if steps else None,
        "steps_to_collapse_mean": statistics.fmean(steps) if steps else None,
        "steps_to_collapse_max": max(steps) if steps else None,
        "circularity_risk": "high",
        "constructive_refinement_status": "not_constructive_future_label_oracle",
    }


def proxy_candidates(rows: list[dict]) -> list[dict]:
    residual = [r for r in rows if not any(predicate(inv, r) for inv in ["I1a", "I1b", "I2", "I3"])]
    candidates = []
    specs = []
    for col in ["mean_welfare", "min_zone_welfare", "delayed_obs_min_welfare"]:
        for t in [0.70, 0.80, 0.85, 0.90, 0.92, 0.94, 0.96]:
            specs.append((f"{col} <= {t}", lambda r, col=col, t=t: f(r, col) <= t))
    for t in [250, 300, 400, 500, 750, 1000]:
        specs.append((f"total_mass <= {t}", lambda r, t=t: f(r, "total_mass") <= t))
    for n in [1, 2, 3]:
        specs.append((f"failed_zone_count >= {n}", lambda r, n=n: f(r, "failed_zone_count") >= n))
    for t in [-0.05, -0.03, -0.02, -0.01, 0.0]:
        specs.append((f"obs_neighbor_delta_min <= {t}", lambda r, t=t: f(r, "obs_neighbor_delta_min") <= t))
    for name, pred in specs:
        covered = [r for r in residual if pred(r)]
        candidates.append({
            "proxy": name,
            "residual_after_R3_coverage_count": len(covered),
            "residual_after_R3_coverage_fraction": rate(len(covered), len(residual)),
            "covered_class_counts": dict(Counter(r["assigned_witness_class"] for r in covered)),
        })
    candidates.sort(key=lambda r: (-r["residual_after_R3_coverage_count"], r["proxy"]))
    return candidates


def non_oracle_proxy_analysis(rows: list[dict]) -> dict:
    candidates = proxy_candidates(rows)
    best = candidates[0] if candidates else None
    r3_residual = [r for r in rows if not any(predicate(inv, r) for inv in ["I1a", "I1b", "I2", "I3"])]
    proxy_cov = [r for r in r3_residual if predicate("I4_proxy", r)]
    missed = [r for r in r3_residual if not predicate("I4_proxy", r)]
    return {
        "R3_residual_count": len(r3_residual),
        "R3_residual_class_counts": dict(Counter(r["assigned_witness_class"] for r in r3_residual)),
        "selected_proxy": "min_zone_welfare <= 0.96",
        "selected_proxy_reason": "highest single-threshold coverage among non-oracle current/delayed fields available in FA1 witness rows",
        "selected_proxy_coverage_count": len(proxy_cov),
        "selected_proxy_coverage_fraction_of_R3_residual": rate(len(proxy_cov), len(r3_residual)),
        "selected_proxy_missed_count": len(missed),
        "selected_proxy_missed_examples": [
            {
                "world": r["world"],
                "policy": r["policy"],
                "seed": r["seed"],
                "step": r["step"],
                "min_zone_welfare": r["min_zone_welfare"],
                "future_collapse_step": r["future_collapse_step"],
            }
            for r in missed[:10]
        ],
        "top_candidate_thresholds": candidates[:12],
        "constructive_limit": "FA1 witness-only input supports witness coverage, but not false-positive/precision estimates against non-false-safe SAFE states.",
    }


def decide(summary: dict, coverage_rows: list[dict], proxy: dict) -> dict:
    by_id = {r["refinement_set"]: r for r in coverage_rows}
    r3 = by_id["R3"]
    r4p = by_id["R4-proxy"]
    r4o = by_id["R4-oracle"]
    unresolved = 1.0 - r4p["witness_coverage_fraction"]
    top_non_oracle = r4p["witness_coverage_fraction"]
    unknown_fraction = summary["unknown_or_mixed_fraction"]
    proxy_constructive_limit = "false-positive/precision" in proxy["constructive_limit"]

    if top_non_oracle >= 0.80 and unknown_fraction <= 0.10 and not proxy_constructive_limit:
        case = "Case A — Compact_non_oracle_supported"
        interpretation = "A small non-oracle invariant set covers most witnesses with enough calibration."
    elif r4o["witness_coverage_fraction"] >= 0.95 and r4p["witness_coverage_fraction"] < 0.80:
        case = "Case B — Compact_only_with_oracle_temporal"
        interpretation = "High coverage requires future-label oracle temporal information."
    elif r3["witness_coverage_fraction"] >= 0.70 and proxy_constructive_limit:
        case = "Case E — Inconclusive"
        interpretation = "Compact non-oracle witness coverage is high, but FA1 witness-only data cannot estimate proxy precision or false positives."
    elif top_non_oracle < 0.80:
        case = "Case C — History_temporal_barrier"
        interpretation = "History/temporal residuals cannot be captured by compact non-oracle invariants."
    else:
        case = "Case D — Noncompact_refinement"
        interpretation = "Coverage grows slowly or requires too many raw variables."

    return {
        "classification": case,
        "interpretation": interpretation,
        "H_FA1_1_assessment": "partially_supported_but_precision_unproven" if case == "Case E — Inconclusive" else ("supported" if case == "Case A — Compact_non_oracle_supported" else "weakened"),
        "non_oracle_R3_coverage": r3["witness_coverage_fraction"],
        "non_oracle_R4_proxy_coverage": r4p["witness_coverage_fraction"],
        "oracle_R4_coverage": r4o["witness_coverage_fraction"],
        "residual_complexity_fraction_after_R4_proxy": unresolved,
        "strongest_counterexample": "The selected non-oracle temporal proxy is a broad min_zone_welfare threshold learned from false-safe witnesses only; without non-false-safe SAFE states, coverage may be non-discriminative.",
        "do_not_claim_safety": True,
        "do_not_propose_new_shield": True,
    }


def compression_summary(rows: list[dict], coverage_rows: list[dict], marginal: list[dict], assessment: dict) -> dict:
    total = len(rows)
    class_counts = Counter(r["assigned_witness_class"] for r in rows)
    by_id = {r["refinement_set"]: r for r in coverage_rows}
    non_oracle_coords = by_id["R4-proxy"]["number_invariant_coordinates_added"]
    non_oracle_cov = by_id["R4-proxy"]["witness_coverage_count"]
    highest_marginal = max(marginal, key=lambda r: r["marginal_coverage_count_in_order"])
    highest_ratio = max(
        [r for r in marginal if r["coordinate_count"] > 0],
        key=lambda r: r["marginal_compression_ratio"],
    )
    cumulative = 0.0
    coverage_at_k = []
    for i, row in enumerate([r for r in marginal if r["oracle"] == "no"], start=1):
        cumulative += row["marginal_coverage_fraction_in_order"]
        coverage_at_k.append({"k": i, "invariant": row["invariant_id"], "cumulative_coverage_fraction": cumulative})
    return {
        "total_witnesses": total,
        "class_counts": dict(class_counts),
        "coverage_at_refinements": {
            r["refinement_set"]: r["witness_coverage_fraction"] for r in coverage_rows
        },
        "coverage_at_k_non_oracle": coverage_at_k,
        "highest_marginal_invariant": highest_marginal["invariant_id"],
        "highest_marginal_coverage": highest_marginal["marginal_coverage_count_in_order"],
        "highest_marginal_compression_ratio_invariant": highest_ratio["invariant_id"],
        "highest_marginal_compression_ratio": highest_ratio["marginal_compression_ratio"],
        "compression_ratio_R4_proxy": rate(non_oracle_cov, non_oracle_coords),
        "eligible_compression_ratio_R4_proxy": rate(non_oracle_cov, non_oracle_coords),
        "residual_complexity_after_R4_proxy": 1.0 - by_id["R4-proxy"]["witness_coverage_fraction"],
        "classification": assessment["classification"],
    }


def write_wsts_assessment(path: Path, catalog: list[dict], coverage_rows: list[dict]) -> None:
    lines = [
        "# FA2.E1 WSTS / Monotonicity Risk Assessment",
        "",
        "This is a diagnostic assessment only. It does not synthesize a shield and does not claim safety.",
        "",
        "## Invariant Risks",
        "",
        "| invariant | layer | WSTS risk | monotonicity risk | circularity risk | note |",
        "|---|---|---|---|---|---|",
    ]
    notes = {
        "I1a": "Real spread-collapse count is monotone under failed-zone order.",
        "I1b": "Real mass collapse threshold is monotone under lower-mass order.",
        "I2": "Policy-visible concentration is delayed/observed and distinct from reporting HHI; monotonicity is not guaranteed.",
        "I3": "History variables can improve or worsen under delayed response, so monotonicity risk is high.",
        "I4_oracle": "Future reachability label is circular for construction and may encode the transition system itself.",
        "I4_proxy": "Current min-zone-welfare threshold is compact, but empirical and uncalibrated against non-witness states.",
        "I5": "No new coordinate; inherits I2/I3 history and observation risks.",
    }
    for row in catalog:
        lines.append(
            f"| {row['id']} {row['name']} | {row['layer_eligibility']} | {row['wsts_compatibility_risk']} | "
            f"{row['monotonicity_risk']} | {row['circularity_risk']} | {notes[row['id']]} |"
        )
    lines += [
        "",
        "## Refinement Risk Summary",
        "",
        "| refinement | coverage | WSTS risk | monotonicity risk | circularity risk |",
        "|---|---:|---|---|---|",
    ]
    for row in coverage_rows:
        lines.append(
            f"| {row['refinement_set']} | {row['witness_coverage_fraction']:.6f} | "
            f"{row['wsts_compatibility_risk']} | {row['monotonicity_risk']} | {row['circularity_risk']} |"
        )
    lines += [
        "",
        "The main risk is not reporting-layer confusion in this dataset; it is whether the temporal proxy is discriminative outside the false-safe witness set.",
    ]
    path.write_text("\n".join(lines) + "\n")


def write_final_report(path: Path, summary: dict, assessment: dict, coverage_rows: list[dict], marginal: list[dict], proxy: dict, oracle: dict) -> None:
    by_id = {r["refinement_set"]: r for r in coverage_rows}
    lines = [
        "# FA2.E1 Minimal Invariant Compression Test",
        "",
        "Diagnostic-only analysis over FA1.E1 false-safe witnesses. No new Justitia simulations were run.",
        "",
        "## Decision",
        "",
        f"Classification: **{assessment['classification']}**.",
        f"Interpretation: {assessment['interpretation']}",
        f"H_FA1.1 assessment: `{assessment['H_FA1_1_assessment']}`.",
        "",
        "## Input",
        "",
        f"- FA1 false-safe witnesses: `{summary['total_witnesses']}`.",
        f"- FA1 classes: `{summary['class_counts']}`.",
        "",
        "## Ordered Refinement Coverage",
        "",
        "| set | description | coverage count | coverage fraction | newly covered | coordinates | oracle |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in coverage_rows:
        lines.append(
            f"| {row['refinement_set']} | {row['description']} | {row['witness_coverage_count']} | "
            f"{row['witness_coverage_fraction']:.6f} | {row['newly_covered_witnesses']} | "
            f"{row['number_invariant_coordinates_added']} | {row['oracle']} |"
        )
    lines += [
        "",
        "## Required Questions",
        "",
        f"1. Omitted collapse clauses alone cover `{by_id['R1']['witness_coverage_count']}` witnesses (`{by_id['R1']['witness_coverage_fraction']:.6f}`).",
        f"2. Adding policy-visible concentration raises coverage to `{by_id['R2']['witness_coverage_count']}` (`{by_id['R2']['witness_coverage_fraction']:.6f}`).",
        f"3. Adding compact history summaries raises coverage to `{by_id['R3']['witness_coverage_count']}` (`{by_id['R3']['witness_coverage_fraction']:.6f}`).",
        f"4. Non-oracle proxy coverage reaches `{by_id['R4-proxy']['witness_coverage_fraction']:.6f}`, but precision cannot be measured from witness-only input.",
        f"5. Highest marginal coverage: `{summary['highest_marginal_invariant']}` with `{summary['highest_marginal_coverage']}` newly covered witnesses.",
        f"6. Highest marginal compression ratio: `{summary['highest_marginal_compression_ratio_invariant']}` with `{summary['highest_marginal_compression_ratio']:.3f}` witnesses per coordinate; cumulative R4-proxy compression is `{summary['compression_ratio_R4_proxy']:.3f}` witnesses per coordinate.",
        f"7. Fraction unresolved after R4-proxy: `{summary['residual_complexity_after_R4_proxy']:.6f}`.",
        "8. I1 is low WSTS risk; I2 is medium; I3 is high monotonicity risk; I4-oracle is high circularity risk; I4-proxy is medium WSTS risk due empirical calibration.",
        f"9. FA2 supports compact witness coverage, but not a fully constructive faithful refinement because proxy precision is unmeasured.",
        f"10. Strongest counterexample: {assessment['strongest_counterexample']}",
        "",
        "## Temporal Analysis",
        "",
        f"- Oracle temporal invariant covers `{oracle['covers_current_not_collapsed_false_safe_witnesses']}` current-not-collapsed false-safe witnesses (`{oracle['coverage_fraction_all_witnesses']:.6f}` of all witnesses).",
        f"- Steps to collapse: min `{oracle['steps_to_collapse_min']}`, median `{oracle['steps_to_collapse_median']}`, mean `{oracle['steps_to_collapse_mean']:.3f}`, max `{oracle['steps_to_collapse_max']}`.",
        f"- Selected non-oracle proxy: `{proxy['selected_proxy']}`, covering `{proxy['selected_proxy_coverage_count']}` of `{proxy['R3_residual_count']}` R3 residual witnesses.",
        "",
        "No safety claim is made. This experiment measures compression of missing information only.",
    ]
    path.write_text("\n".join(lines) + "\n")


def write_notes(path: Path) -> None:
    lines = [
        "# FA2.E1 Implementation Notes",
        "",
        "- Input source: `experiments/FA1_E1_false_safe_witness_taxonomy/outputs/witness_taxonomy.csv`.",
        "- No new Justitia simulation was run because FA1 already exported current collapse clauses, future collapse step, delayed observation summaries, policy-visible concentration, and allocation/control summaries.",
        "- `I2` uses `Obs.resource_concentration` fields from FA1; it does not use reporting `resource_hhi`.",
        "- `I3` uses compact delayed consequence flags, not raw history.",
        "- `I4_oracle` is reported only for theoretical compressibility and is not counted as constructive refinement.",
        "- `I4_proxy` was selected by single-threshold coverage over the R3 residual using current/delayed fields available at step time.",
        "- The major limitation is that FA1 witness output does not include non-false-safe SAFE states, so non-oracle proxy false-positive rates cannot be estimated in this experiment.",
    ]
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    witnesses = read_witnesses()
    fa1_summary = read_json(FA1_OUT / "witness_class_summary.json")
    catalog = invariant_catalog()
    ref_sets, cov_rows, residual = refinement_rows(witnesses, catalog)
    marginal = marginal_rows(witnesses, catalog)
    oracle = temporal_oracle_analysis(witnesses)
    proxy = non_oracle_proxy_analysis(witnesses)
    pre_summary = {
        "total_witnesses": len(witnesses),
        "class_counts": fa1_summary["class_counts"],
        "unknown_or_mixed_fraction": fa1_summary["unknown_or_mixed_fraction"],
    }
    assessment = decide(pre_summary, cov_rows, proxy)
    summary = compression_summary(witnesses, cov_rows, marginal, assessment)
    summary["class_counts"] = fa1_summary["class_counts"]

    write_csv(OUT / "invariant_catalog.csv", catalog)
    write_csv(OUT / "refinement_sets.csv", ref_sets)
    write_csv(OUT / "coverage_by_refinement.csv", cov_rows)
    write_csv(OUT / "marginal_coverage.csv", marginal)
    write_csv(OUT / "residual_witnesses.csv", residual)
    write_json(OUT / "temporal_oracle_analysis.json", oracle)
    write_json(OUT / "non_oracle_proxy_analysis.json", proxy)
    write_wsts_assessment(OUT / "wsts_risk_assessment.md", catalog, cov_rows)
    write_json(OUT / "compression_summary.json", summary)
    write_json(OUT / "hypothesis_assessment.json", assessment)
    write_final_report(OUT / "final_report.md", summary, assessment, cov_rows, marginal, proxy, oracle)
    write_notes(OUT / "implementation_notes.md")

    print(json.dumps({
        "classification": assessment["classification"],
        "H_FA1_1_assessment": assessment["H_FA1_1_assessment"],
        "total_witnesses": len(witnesses),
        "R1_coverage": next(r for r in cov_rows if r["refinement_set"] == "R1")["witness_coverage_fraction"],
        "R3_coverage": next(r for r in cov_rows if r["refinement_set"] == "R3")["witness_coverage_fraction"],
        "R4_proxy_coverage": next(r for r in cov_rows if r["refinement_set"] == "R4-proxy")["witness_coverage_fraction"],
        "R4_oracle_coverage": next(r for r in cov_rows if r["refinement_set"] == "R4-oracle")["witness_coverage_fraction"],
        "outputs": str(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
