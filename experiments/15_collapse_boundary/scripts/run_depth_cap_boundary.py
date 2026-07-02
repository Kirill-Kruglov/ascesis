#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collapse_boundary.explore import (  # noqa: E402
    canonical_term,
    canonical_trajectory,
    label_class,
    random_trajectory,
    semantic_class,
)
from collapse_boundary.metrics import axis_classify  # noqa: E402
from collapse_boundary.systems import build_collapsing_system  # noqa: E402

OLD_SEMANTIC_CEILING = 1024
SAMPLE_LIMIT_FRAC = 0.9
GROWTH_EPS = 0.05

FULL_GRID = {
    "depth_caps": [8, 12, 16, 20, 24],
    "observation_depths": [4, 6, 8, 10, 12],
    "sample_budgets": [20_000, 50_000, 100_000],
    "horizons": [16, 32, 64, 128, 256],
}
QUICK_GRID = {
    "depth_caps": [8, 12, 16],
    "observation_depths": [4, 8],
    "sample_budgets": [20_000, 50_000],
    "horizons": [64, 128],
}


def parse_ints(value: str) -> list[int]:
    return [int(part.replace("_", "")) for part in value.split(",") if part.strip()]


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def stable_seed(seed: int, depth_cap: int, horizon: int) -> int:
    return seed + depth_cap * 1_000_003 + horizon * 9_176


def sample_trajectories(depth_cap: int, horizon: int, budget: int, seed: int):
    system = build_collapsing_system(depth_cap)
    rng = random.Random(stable_seed(seed, depth_cap, horizon))
    sampler_depth = 2 + int(math.log2(max(1, horizon)))
    trajectories = []
    for _ in range(budget):
        initial = system.sampler(rng, sampler_depth)
        trajectories.append(random_trajectory(system, initial, horizon, rng))
    return trajectories


def count_for_budget(trajs, sample_budget: int, obs_depth: int) -> dict[str, object]:
    subset = trajs[:sample_budget]
    semantic_classes = [semantic_class(traj, obs_depth) for traj in subset]
    label_classes = [label_class(traj) for traj in subset]
    trajectory_classes = [canonical_trajectory(traj) for traj in subset]
    term_classes = set()
    normal_forms = set()
    generated_terms = 0
    for traj in subset:
        generated_terms += len(traj.terms)
        for term in traj.terms:
            term_classes.add(canonical_term(term))
        if traj.terminated:
            normal_forms.add(traj.final.shape())

    semantic_count = len(set(semantic_classes))
    trajectory_count = len(set(trajectory_classes))
    state_count = len(term_classes)
    label_count = len(set(label_classes))
    semantic_rate = semantic_count / sample_budget if sample_budget else 0.0
    trajectory_rate = trajectory_count / sample_budget if sample_budget else 0.0
    sample_limited_semantic = semantic_rate >= SAMPLE_LIMIT_FRAC
    sample_limited_trajectory = trajectory_rate >= SAMPLE_LIMIT_FRAC
    if semantic_count > sample_budget or trajectory_count > sample_budget:
        raise AssertionError("unique semantic/trajectory counts must not exceed sample_budget")

    return {
        "semantic_class_count": semantic_count,
        "semantic_class_rate": semantic_rate,
        "trajectory_count": trajectory_count,
        "trajectory_rate": trajectory_rate,
        "state_count": state_count,
        "state_rate": state_count / generated_terms if generated_terms else 0.0,
        "normal_form_count": len(normal_forms),
        "normal_form_rate": len(normal_forms) / sample_budget if sample_budget else 0.0,
        "label_quotient_count": label_count,
        "label_quotient_rate": label_count / sample_budget if sample_budget else 0.0,
        "syntactic_semantic_gap": trajectory_rate - semantic_rate,
        "generated_terms": generated_terms,
        "sample_limited_semantic": sample_limited_semantic,
        "sample_limited_trajectory": sample_limited_trajectory,
        "sample_limited": sample_limited_semantic or sample_limited_trajectory,
    }


def add_horizon_diagnostics(df: pd.DataFrame, horizons: list[int]) -> pd.DataFrame:
    rows = []
    group_cols = ["depth_cap", "observation_depth", "sample_budget"]
    for _, group in df.groupby(group_cols, sort=False):
        ordered = group.sort_values("horizon").copy()
        counts = [int(v) for v in ordered["semantic_class_count"]]
        budgets = [int(v) for v in ordered["sample_budget"]]
        verdict = axis_classify(
            [int(v) for v in ordered["horizon"]],
            counts,
            budgets,
            growth_eps=GROWTH_EPS,
            sample_limit_frac=SAMPLE_LIMIT_FRAC,
        )
        ordered["semantic_saturation_horizon"] = verdict["saturation_horizon"]
        ordered["semantic_axis_verdict"] = verdict["verdict"]
        ordered["semantic_still_growing_at_max_horizon"] = verdict["still_growing"]
        rows.append(ordered)
    out = pd.concat(rows, ignore_index=True)

    obs_rows = []
    for _, group in out.groupby(["depth_cap", "sample_budget", "horizon"], sort=False):
        ordered = group.sort_values("observation_depth").copy()
        counts = list(ordered["semantic_class_count"].astype(int))
        obs_limited = False
        if len(counts) >= 2:
            prev, cur = counts[-2], counts[-1]
            obs_limited = (cur - prev) / max(1, prev) > GROWTH_EPS
        ordered["observation_limited"] = obs_limited
        obs_rows.append(ordered)
    return pd.concat(obs_rows, ignore_index=True)


def growth_table(df: pd.DataFrame, group_col: str, max_cap: int, max_obs: int, max_budget: int, max_horizon: int) -> pd.DataFrame:
    base = df.copy()
    if group_col != "depth_cap":
        base = base[base["depth_cap"] == max_cap]
    if group_col != "observation_depth":
        base = base[base["observation_depth"] == max_obs]
    if group_col != "sample_budget":
        base = base[base["sample_budget"] == max_budget]
    base = base[base["horizon"] == max_horizon]
    rows = []
    prev = None
    for value, group in base.groupby(group_col):
        sem = int(group["semantic_class_count"].max())
        traj = int(group["trajectory_count"].max())
        rows.append({
            group_col: int(value),
            "semantic_class_count": sem,
            "trajectory_count": traj,
            "semantic_class_rate": float(group["semantic_class_rate"].max()),
            "trajectory_rate": float(group["trajectory_rate"].max()),
            "sample_limited_any": bool(group["sample_limited"].any()),
            "semantic_growth_from_previous": None if prev is None else sem - prev,
            "semantic_growth_ratio_from_previous": None if prev in (None, 0) else sem / prev,
        })
        prev = sem
    return pd.DataFrame(rows).sort_values(group_col)


def sample_limited_report(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["depth_cap", "observation_depth", "sample_budget"], as_index=False)
        .agg(
            sample_limited_any=("sample_limited", "any"),
            semantic_sample_limited_any=("sample_limited_semantic", "any"),
            trajectory_sample_limited_any=("sample_limited_trajectory", "any"),
            max_semantic_rate=("semantic_class_rate", "max"),
            max_trajectory_rate=("trajectory_rate", "max"),
            max_semantic_count=("semantic_class_count", "max"),
            max_trajectory_count=("trajectory_count", "max"),
        )
    )


def observation_window_report(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (cap, budget, horizon), group in df.groupby(["depth_cap", "sample_budget", "horizon"]):
        ordered = group.sort_values("observation_depth")
        counts = list(ordered["semantic_class_count"].astype(int))
        obs = list(ordered["observation_depth"].astype(int))
        growth = counts[-1] - counts[0]
        last_step = 0 if len(counts) < 2 else counts[-1] - counts[-2]
        rows.append({
            "depth_cap": cap,
            "sample_budget": budget,
            "horizon": horizon,
            "min_observation_depth": obs[0],
            "max_observation_depth": obs[-1],
            "semantic_at_min_observation_depth": counts[0],
            "semantic_at_max_observation_depth": counts[-1],
            "absolute_growth": growth,
            "growth_ratio": counts[-1] / max(1, counts[0]),
            "last_step_growth": last_step,
            "observation_limited": (last_step / max(1, counts[-2] if len(counts) >= 2 else counts[-1])) > GROWTH_EPS,
        })
    return pd.DataFrame(rows)


def classify_growth(values: Iterable[int]) -> dict[str, object]:
    vals = list(values)
    if not vals:
        return {"substantial": False, "monotonic": False, "ratio": None, "delta": 0}
    delta = vals[-1] - vals[0]
    ratio = vals[-1] / max(1, vals[0])
    monotonic = all(b >= a for a, b in zip(vals, vals[1:]))
    substantial = delta > max(100, vals[0] * 0.25)
    return {"substantial": substantial, "monotonic": monotonic, "ratio": ratio, "delta": delta}


def make_reports(df: pd.DataFrame, args, grid: dict[str, list[int]], out: Path) -> dict[str, object]:
    max_cap = max(grid["depth_caps"])
    max_obs = max(grid["observation_depths"])
    max_budget = max(grid["sample_budgets"])
    max_horizon = max(grid["horizons"])

    by_cap = growth_table(df, "depth_cap", max_cap, max_obs, max_budget, max_horizon)
    by_obs = growth_table(df, "observation_depth", max_cap, max_obs, max_budget, max_horizon)
    by_budget = growth_table(df, "sample_budget", max_cap, max_obs, max_budget, max_horizon)
    limited = sample_limited_report(df)
    obs_report = observation_window_report(df)

    by_cap.to_csv(out / "semantic_growth_by_cap.csv", index=False)
    by_obs.to_csv(out / "semantic_growth_by_observation_depth.csv", index=False)
    by_budget.to_csv(out / "semantic_growth_by_sample_budget.csv", index=False)
    limited.to_csv(out / "sample_limited_report.csv", index=False)
    obs_report.to_csv(out / "observation_window_report.csv", index=False)

    cap_growth = classify_growth(by_cap["semantic_class_count"].astype(int))
    obs_growth = classify_growth(by_obs["semantic_class_count"].astype(int))
    budget_growth = classify_growth(by_budget["semantic_class_count"].astype(int))
    max_semantic = int(df["semantic_class_count"].max())
    exceeded_old = max_semantic > OLD_SEMANTIC_CEILING
    semantic_sample_limited_frac = float(df["sample_limited_semantic"].mean())
    any_sample_limited_frac = float(df["sample_limited"].mean())

    top = df[(df["sample_budget"] == max_budget) & (df["horizon"] == max_horizon)]
    max_corner = top[top["depth_cap"] == max_cap]
    large_caps = top[top["depth_cap"] >= sorted(grid["depth_caps"])[-2]] if len(grid["depth_caps"]) >= 2 else top
    top_plateaued = bool((top["semantic_still_growing_at_max_horizon"] == False).all())
    top_far_below_budget = bool((top["semantic_class_rate"] < SAMPLE_LIMIT_FRAC).all())
    max_corner_semantic_sample_limited_frac = float(max_corner["sample_limited_semantic"].mean()) if len(max_corner) else 0.0
    large_cap_semantic_sample_limited_frac = float(large_caps["sample_limited_semantic"].mean()) if len(large_caps) else 0.0
    max_corner_semantic_rate = float(max_corner["semantic_class_rate"].max()) if len(max_corner) else 0.0
    sample_budget_tracks_semantics = bool(budget_growth["substantial"] and max_corner_semantic_rate >= SAMPLE_LIMIT_FRAC)

    if (
        semantic_sample_limited_frac >= 0.5
        or max_corner_semantic_sample_limited_frac >= 0.5
        or large_cap_semantic_sample_limited_frac >= 0.5
        or sample_budget_tracks_semantics
    ):
        classification = "sample_limited_inconclusive"
        interpretation = "Cannot distinguish semantic openness from sampling limit."
    elif cap_growth["substantial"] and exceeded_old and not budget_growth["substantial"]:
        classification = "cap_artifact_confirmed"
        interpretation = "The old semantic ceiling was at least partly caused by the explicit depth cap."
    elif obs_growth["substantial"] and not cap_growth["substantial"]:
        classification = "observation_window_artifact"
        interpretation = "The previous semantic ceiling was strongly affected by shallow bounded observation."
    elif cap_growth["substantial"] and top_plateaued and top_far_below_budget:
        classification = "mixed_boundary"
        interpretation = "C grows with the cap but repeatedly reaches finite plateaus."
    elif top_plateaued and top_far_below_budget:
        classification = "semantic_closure_confirmed"
        interpretation = "C remains semantically closed in this grid despite syntactic trajectory growth."
    else:
        classification = "mixed_boundary"
        interpretation = "Growth evidence is mixed; more scaling data is needed."

    report = {
        "params": {
            "mode": args.mode,
            "seed": args.seed,
            "depth_caps": grid["depth_caps"],
            "observation_depths": grid["observation_depths"],
            "sample_budgets": grid["sample_budgets"],
            "horizons": grid["horizons"],
            "old_semantic_ceiling": OLD_SEMANTIC_CEILING,
            "sample_limit_frac": SAMPLE_LIMIT_FRAC,
            "growth_eps": GROWTH_EPS,
        },
        "evidence": {
            "max_semantic_class_count": max_semantic,
            "exceeded_old_1024_ceiling": exceeded_old,
            "max_trajectory_count": int(df["trajectory_count"].max()),
            "semantic_sample_limited_fraction": semantic_sample_limited_frac,
            "max_corner_semantic_sample_limited_fraction": max_corner_semantic_sample_limited_frac,
            "large_cap_semantic_sample_limited_fraction": large_cap_semantic_sample_limited_frac,
            "max_corner_semantic_rate": max_corner_semantic_rate,
            "sample_budget_tracks_semantics": sample_budget_tracks_semantics,
            "any_channel_sample_limited_fraction": any_sample_limited_frac,
            "cap_growth": cap_growth,
            "observation_depth_growth": obs_growth,
            "sample_budget_growth": budget_growth,
            "top_grid_semantic_plateaued": top_plateaued,
            "top_grid_far_below_sample_budget": top_far_below_budget,
        },
        "classification": classification,
        "interpretation": interpretation,
    }
    write_json(out / "cap_boundary_report.json", report)
    write_json(out / "final_decision.json", {
        "classification": classification,
        "interpretation": interpretation,
        "next_recommended_action": next_action(classification),
        "evidence": report["evidence"],
    })
    write_summary(out / "summary.md", report, by_cap, by_obs, by_budget, limited, obs_report)
    return report


def next_action(classification: str) -> str:
    if classification == "cap_artifact_confirmed":
        return "Proceed to deeper cap scaling or rule-family variation for System C."
    if classification == "semantic_closure_confirmed":
        return "Treat C as semantically closed in this toy family; do not use syntactic trajectory openness as live evidence."
    if classification == "observation_window_artifact":
        return "Improve the semantic proxy before judging C; bounded observation depth is driving the result."
    if classification == "sample_limited_inconclusive":
        return "Increase sampling budget or change sampler before making liveness claims."
    return "Run a scaling-law follow-up with larger caps/horizons and stricter semantic proxies."


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "(empty)"
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        values = []
        for col in df.columns:
            value = row[col]
            if pd.isna(value):
                values.append("")
            elif isinstance(value, float):
                values.append(f"{value:.6g}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_summary(path: Path, report: dict[str, object], by_cap: pd.DataFrame, by_obs: pd.DataFrame, by_budget: pd.DataFrame, limited: pd.DataFrame, obs_report: pd.DataFrame) -> None:
    ev = report["evidence"]
    classification = report["classification"]
    lines = [
        "# Experiment 15.1 - Depth-Cap Boundary Probe",
        "",
        "## Decision",
        "",
        f"Classification: `{classification}`.",
        "",
        str(report["interpretation"]),
        "",
        "## Required Questions",
        "",
        f"1. Did C exceed the old 1024 semantic-class ceiling? {'Yes' if ev['exceeded_old_1024_ceiling'] else 'No'}; max semantic_class_count = {ev['max_semantic_class_count']}.",
        f"2. Did semantic growth depend on depth_cap? {'Yes' if ev['cap_growth']['substantial'] else 'No clear substantial dependence'}; delta = {ev['cap_growth']['delta']}, ratio = {ev['cap_growth']['ratio']:.4g}.",
        f"3. Did semantic growth depend on observation_depth? {'Yes' if ev['observation_depth_growth']['substantial'] else 'No clear substantial dependence'}; delta = {ev['observation_depth_growth']['delta']}, ratio = {ev['observation_depth_growth']['ratio']:.4g}.",
        f"4. Was any result sample-limited? {'Yes' if ev['any_channel_sample_limited_fraction'] > 0 else 'No'}; semantic sample-limited fraction = {ev['semantic_sample_limited_fraction']:.4g}, any-channel sample-limited fraction = {ev['any_channel_sample_limited_fraction']:.4g}.",
        f"5. Is there evidence of genuine semantic openness? {'No, not without caveats' if classification != 'cap_artifact_confirmed' else 'Partial positive evidence: cap growth exceeded the old ceiling and was not only sample-budget growth'}.",
        f"6. Next recommended action: {next_action(classification)}",
        "",
        "## Growth Tables",
        "",
        "### Semantic Growth by Depth Cap",
        "",
        markdown_table(by_cap),
        "",
        "### Semantic Growth by Observation Depth",
        "",
        markdown_table(by_obs),
        "",
        "### Semantic Growth by Sample Budget",
        "",
        markdown_table(by_budget),
        "",
        "## Honesty Notes",
        "",
        "- The primary semantic proxy is bounded-depth observation prefix / normal-form class, reused from 15.0.1.",
        "- Label-sequence quotient is recorded only as a syntactic-like diagnostic and is not used as semantic evidence.",
        "- Any sample-limited channel must not be classified as open.",
        "- Syntactic trajectory growth without semantic growth is not evidence of liveness.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def plot_outputs(df: pd.DataFrame, out: Path, grid: dict[str, list[int]]) -> None:
    max_cap = max(grid["depth_caps"])
    max_obs = max(grid["observation_depths"])
    max_budget = max(grid["sample_budgets"])
    max_horizon = max(grid["horizons"])

    top_hb = df[(df["horizon"] == max_horizon) & (df["sample_budget"] == max_budget)]
    fig, ax = plt.subplots(figsize=(8, 5))
    for obs, group in top_hb.groupby("observation_depth"):
        ordered = group.sort_values("depth_cap")
        ax.plot(ordered["depth_cap"], ordered["semantic_class_count"], marker="o", label=f"obs={obs}")
    ax.axhline(OLD_SEMANTIC_CEILING, color="black", linestyle="--", linewidth=1, label="old 1024 ceiling")
    ax.set_title("Semantic count vs depth cap")
    ax.set_xlabel("depth_cap")
    ax.set_ylabel("semantic_class_count")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "semantic_count_vs_depth_cap.png", dpi=130)
    plt.close(fig)

    top_hb = df[(df["horizon"] == max_horizon) & (df["sample_budget"] == max_budget)]
    fig, ax = plt.subplots(figsize=(8, 5))
    for cap, group in top_hb.groupby("depth_cap"):
        ordered = group.sort_values("observation_depth")
        ax.plot(ordered["observation_depth"], ordered["semantic_class_count"], marker="o", label=f"cap={cap}")
    ax.set_title("Semantic count vs observation depth")
    ax.set_xlabel("observation_depth")
    ax.set_ylabel("semantic_class_count")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "semantic_count_vs_observation_depth.png", dpi=130)
    plt.close(fig)

    top_ho = df[(df["horizon"] == max_horizon) & (df["observation_depth"] == max_obs)]
    fig, ax = plt.subplots(figsize=(8, 5))
    for cap, group in top_ho.groupby("depth_cap"):
        ordered = group.sort_values("sample_budget")
        ax.plot(ordered["sample_budget"], ordered["semantic_class_count"], marker="o", label=f"cap={cap}")
    ax.set_title("Semantic count vs sample budget")
    ax.set_xlabel("sample_budget")
    ax.set_ylabel("semantic_class_count")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "semantic_count_vs_sample_budget.png", dpi=130)
    plt.close(fig)

    heat = top_hb.pivot_table(index="observation_depth", columns="depth_cap", values="semantic_class_count", aggfunc="max")
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(heat.values, aspect="auto", origin="lower", cmap="viridis")
    ax.set_xticks(range(len(heat.columns)))
    ax.set_xticklabels([str(c) for c in heat.columns])
    ax.set_yticks(range(len(heat.index)))
    ax.set_yticklabels([str(o) for o in heat.index])
    ax.set_title("Semantic count heatmap")
    ax.set_xlabel("depth_cap")
    ax.set_ylabel("observation_depth")
    fig.colorbar(im, ax=ax, label="semantic_class_count")
    fig.tight_layout()
    fig.savefig(out / "semantic_count_heatmap_cap_obsdepth.png", dpi=130)
    plt.close(fig)

    top_hbo = df[(df["horizon"] == max_horizon) & (df["sample_budget"] == max_budget) & (df["observation_depth"] == max_obs)].sort_values("depth_cap")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(top_hbo["depth_cap"], top_hbo["syntactic_semantic_gap"], marker="o", color="tab:red")
    ax.set_title("Syntactic-semantic gap vs depth cap")
    ax.set_xlabel("depth_cap")
    ax.set_ylabel("trajectory_rate - semantic_rate")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "syntactic_semantic_gap_vs_cap.png", dpi=130)
    plt.close(fig)


def resolve_grid(args) -> dict[str, list[int]]:
    grid = FULL_GRID if args.mode == "full" else QUICK_GRID
    out = {k: list(v) for k, v in grid.items()}
    if args.depth_caps:
        out["depth_caps"] = parse_ints(args.depth_caps)
    if args.observation_depths:
        out["observation_depths"] = parse_ints(args.observation_depths)
    if args.sample_budgets:
        out["sample_budgets"] = parse_ints(args.sample_budgets)
    if args.horizons:
        out["horizons"] = parse_ints(args.horizons)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 15.1 depth-cap boundary probe for System C")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mode", choices=["quick", "full"], default="quick")
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_15_1")
    parser.add_argument("--depth-caps", help="comma-separated override, e.g. 8,12,16")
    parser.add_argument("--observation-depths", help="comma-separated override")
    parser.add_argument("--sample-budgets", help="comma-separated override")
    parser.add_argument("--horizons", help="comma-separated override")
    args = parser.parse_args()

    out = ensure(args.outputs)
    grid = resolve_grid(args)
    max_budget = max(grid["sample_budgets"])
    rows = []
    total_batches = len(grid["depth_caps"]) * len(grid["horizons"])
    batch = 0
    for depth_cap in grid["depth_caps"]:
        for horizon in grid["horizons"]:
            batch += 1
            print(f"[{batch}/{total_batches}] depth_cap={depth_cap} horizon={horizon} max_budget={max_budget}", flush=True)
            trajs = sample_trajectories(depth_cap, horizon, max_budget, args.seed)
            for sample_budget in grid["sample_budgets"]:
                for obs_depth in grid["observation_depths"]:
                    metrics = count_for_budget(trajs, sample_budget, obs_depth)
                    rows.append({
                        "depth_cap": depth_cap,
                        "observation_depth": obs_depth,
                        "sample_budget": sample_budget,
                        "horizon": horizon,
                        **metrics,
                    })
    df = pd.DataFrame(rows).sort_values(["depth_cap", "observation_depth", "sample_budget", "horizon"])
    df = add_horizon_diagnostics(df, grid["horizons"])
    df.to_csv(out / "depth_cap_grid_results.csv", index=False)
    report = make_reports(df, args, grid, out)
    plot_outputs(df, out, grid)
    print(json.dumps({
        "classification": report["classification"],
        "max_semantic_class_count": report["evidence"]["max_semantic_class_count"],
        "exceeded_old_1024_ceiling": report["evidence"]["exceeded_old_1024_ceiling"],
        "semantic_sample_limited_fraction": report["evidence"]["semantic_sample_limited_fraction"],
        "outputs": str(out),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
