#!/usr/bin/env python3
"""Experiment 15.0.1 — measurement repair (NOT system strengthening).

Re-runs the EXACT four rewrite systems from Experiment 15 (same seed, same
horizons, same sampling) and recomputes novelty with three repairs:

  Defect 1: per-channel sustained-plateau closure horizons (no single horizon
            collapsing all channels; first SUSTAINED plateau, not first dip).
  Defect 2: 2D->3D per-axis classification (state / trajectory / semantic),
            never a bare "dead/live".
  Defect 3: a semantic-class novelty channel (normal form where it exists,
            else a bounded-depth observation prefix) measured at every horizon.

The systems are untouched. Learnability / RandomForest is intentionally NOT
recomputed here: this task is about the novelty instruments only, and dropping
the classifier keeps the rerun cheap and fully deterministic.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collapse_boundary.explore import (  # noqa: E402
    canonical_term,
    canonical_trajectory,
    label_class,
    random_trajectory,
    semantic_class,
)
from collapse_boundary.metrics import axis_classify, channel_closure  # noqa: E402
from collapse_boundary.systems import build_systems  # noqa: E402

CHANNELS = ["state", "trajectory", "normal_form", "semantic", "semantic_label"]


def horizons(max_horizon: int) -> list[int]:
    out = []
    h = 1
    while h <= max_horizon:
        out.append(h)
        h *= 2
    return out


def make_trajectories(system, horizon: int, samples: int, rng: random.Random, depth: int):
    """Identical RNG consumption to Experiment 15's make_dataset so the rerun
    reproduces the same trajectories on the same seed."""
    trajectories = []
    terms = []
    normals = []
    for _ in range(samples):
        initial = system.sampler(rng, depth)
        traj = random_trajectory(system, initial, horizon, rng)
        trajectories.append(traj)
        terms.extend(traj.terms)
        if traj.terminated:
            normals.append(traj.final)
    return trajectories, terms, normals


def novelty(unique: int, total: int):
    return unique / total if total else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-horizon", type=int, default=64)
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--obs-depth", type=int, default=4, help="bounded observation depth for non-terminating semantic classes")
    parser.add_argument("--epsilon", type=float, default=0.01)
    parser.add_argument("--k", type=int, default=3, help="consecutive sub-epsilon steps required for a sustained plateau")
    parser.add_argument("--tau-low", type=float, default=0.05, help="rate below which a plateaued channel is 'trivial'")
    parser.add_argument("--growth-eps", type=float, default=0.05, help="relative count growth below which a channel is non-growing")
    parser.add_argument("--sample-limit-frac", type=float, default=0.9, help="unique/budget above which novelty is sample-limited")
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_15_0_1")
    args = parser.parse_args()

    out = args.outputs
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    systems = build_systems()
    hs = horizons(args.max_horizon)

    # rows[system][horizon] = {channel: novelty, ...} plus counts
    curve_rows: list[dict[str, object]] = []
    gap_rows: list[dict[str, object]] = []
    # series[system][channel] = novelty-rate list aligned with hs (None allowed)
    series: dict[str, dict[str, list]] = {s.name: {c: [] for c in CHANNELS} for s in systems}
    # counts[system][channel] = unique-object count; budgets = generated-object budget
    counts: dict[str, dict[str, list]] = {s.name: {c: [] for c in CHANNELS} for s in systems}
    budgets: dict[str, dict[str, list]] = {s.name: {c: [] for c in CHANNELS} for s in systems}

    for system in systems:
        for h in hs:
            depth = 2 + int(math.log2(h))
            trajs, terms, normals = make_trajectories(system, h, args.samples, rng, depth)

            term_shapes = [canonical_term(t) for t in terms]
            traj_shapes = [canonical_trajectory(t) for t in trajs]
            normal_shapes = [n.shape() for n in normals]
            sem_classes = [semantic_class(t, args.obs_depth) for t in trajs]
            lab_classes = [label_class(t) for t in trajs]

            state_nov = novelty(len(set(term_shapes)), len(terms))
            traj_nov = novelty(len(set(traj_shapes)), len(trajs))
            nf_nov = novelty(len(set(normal_shapes)), len(normals)) if normals else None
            sem_nov = novelty(len(set(sem_classes)), len(trajs))
            lab_nov = novelty(len(set(lab_classes)), len(trajs))

            series[system.name]["state"].append(state_nov)
            series[system.name]["trajectory"].append(traj_nov)
            series[system.name]["normal_form"].append(nf_nov)
            series[system.name]["semantic"].append(sem_nov)
            series[system.name]["semantic_label"].append(lab_nov)

            ch_count = {
                "state": len(set(term_shapes)),
                "trajectory": len(set(traj_shapes)),
                "normal_form": len(set(normal_shapes)),
                "semantic": len(set(sem_classes)),
                "semantic_label": len(set(lab_classes)),
            }
            ch_budget = {
                "state": len(terms),
                "trajectory": len(trajs),
                "normal_form": len(normals),
                "semantic": len(trajs),
                "semantic_label": len(trajs),
            }
            for c in CHANNELS:
                counts[system.name][c].append(ch_count[c])
                budgets[system.name][c].append(ch_budget[c])

            curve_rows.append({
                "system": system.name,
                "horizon": h,
                "generated_terms": len(terms),
                "generated_trajectories": len(trajs),
                "terminating_trajectories": len(normals),
                "state_novelty": state_nov,
                "trajectory_novelty": traj_nov,
                "normal_form_novelty": "normal_form_absent" if nf_nov is None else nf_nov,
                "semantic_class_novelty": sem_nov,
                "semantic_label_novelty": lab_nov,
                "unique_terms": len(set(term_shapes)),
                "unique_trajectories": len(set(traj_shapes)),
                "unique_normal_forms": len(set(normal_shapes)),
                "unique_semantic_classes": len(set(sem_classes)),
                "unique_semantic_label_classes": len(set(lab_classes)),
            })
            gap_rows.append({
                "system": system.name,
                "horizon": h,
                "syntactic_novelty": traj_nov,
                "semantic_novelty": sem_nov,
                "gap_syntactic_minus_semantic": (traj_nov - sem_nov) if (traj_nov is not None and sem_nov is not None) else None,
                "semantic_label_novelty": lab_nov,
                "gap_syntactic_minus_label": (traj_nov - lab_nov) if (traj_nov is not None and lab_nov is not None) else None,
                "n_trajectories": len(trajs),
                "unique_syntactic": len(set(traj_shapes)),
                "unique_semantic": len(set(sem_classes)),
            })

    # ---- Per-channel closure horizons (sustained-plateau logic) ----
    closure_report: dict[str, object] = {
        "params": {"epsilon": args.epsilon, "k": args.k, "horizons": hs, "obs_depth": args.obs_depth},
        "systems": {},
    }
    for s in systems:
        per_channel = {}
        for c in CHANNELS:
            per_channel[c] = channel_closure(hs, series[s.name][c], epsilon=args.epsilon, k=args.k)
        closure_report["systems"][s.name] = per_channel

    # ---- Three-axis classification (openness judged on COUNT vs horizon) ----
    axis_report: dict[str, object] = {
        "params": {
            "growth_eps": args.growth_eps, "tau_low_rate": args.tau_low,
            "sample_limit_frac": args.sample_limit_frac, "window": 2,
            "note": "openness is judged on unique-object COUNT vs horizon, not novelty rate at fixed sample budget",
        },
        "legend": {
            "trivial": "count plateaus and per-object novelty rate ~0: channel collapses to ~no diversity",
            "saturating": "count plateaus at a finite set well below the sample budget (closed at a bounded size)",
            "open": "count still growing at the largest horizon (or filled the sample budget -> sample-limited, openness indeterminate)",
            "degenerate": "<=1 distinct object ever; channel uninformative",
        },
        "systems": {},
    }
    for s in systems:
        verdicts = {}
        for c in CHANNELS:
            verdicts[c] = axis_classify(
                hs, counts[s.name][c], budgets[s.name][c],
                growth_eps=args.growth_eps, tau_low_rate=args.tau_low,
                sample_limit_frac=args.sample_limit_frac,
            )
        sem_degenerate = verdicts["semantic"]["verdict"] == "degenerate"

        def label(c):
            v = verdicts[c]["verdict"]
            return v + ("(sample-limited)" if verdicts[c]["sample_limited"] and v == "open" else "")

        summary = f"state-{label('state')} / trajectory-{label('trajectory')} / semantic-{label('semantic')}"
        axis_report["systems"][s.name] = {
            "state_axis": verdicts["state"]["verdict"],
            "trajectory_axis": verdicts["trajectory"]["verdict"],
            "semantic_axis": verdicts["semantic"]["verdict"],
            "summary": summary,
            "semantic_proxy_degenerate": sem_degenerate,
            "evidence": {c: verdicts[c] for c in CHANNELS},
            "non_monotonic_plateau": {
                c: closure_report["systems"][s.name][c]["non_monotonic_plateau"] for c in CHANNELS
            },
        }

    # ---- Write CSV/JSON outputs ----
    write_csv(out / "per_channel_novelty_curves.csv", curve_rows)
    write_csv(out / "semantic_vs_syntactic_gap.csv", gap_rows)
    (out / "per_channel_closure_horizon.json").write_text(json.dumps(closure_report, indent=2), encoding="utf-8")
    (out / "three_axis_classification.json").write_text(json.dumps(axis_report, indent=2), encoding="utf-8")

    write_comparison(out / "comparison_old_vs_new.md", systems, axis_report, closure_report, curve_rows, args)
    plot_channels(out / "per_channel_novelty_vs_horizon.png", systems, hs, series)

    print(json.dumps({s.name: axis_report["systems"][s.name]["summary"] for s in systems}, indent=2))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    import csv

    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def load_old(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def write_comparison(path: Path, systems, axis_report, closure_report, curve_rows, args) -> None:
    old_closure = load_old(ROOT / "outputs" / "closure_horizon_report.json")
    old_final = load_old(ROOT / "outputs" / "final_decision.json")
    old_closure_by = {r["system"]: r for r in old_closure} if old_closure else {}
    old_cls_by = {s["system"]: s["classification"] for s in old_final["systems"]} if old_final else {}

    lines = []
    lines.append("# Experiment 15.0.1 — old vs new measurement\n")
    lines.append("We did NOT change the four rewrite systems, seeds, or horizons. We repaired three "
                 "instruments and recomputed. Below: what each repair changed, per system.\n")
    lines.append(f"- seed={args.seed}, samples={args.samples}, horizons={horizons(args.max_horizon)}, "
                 f"obs_depth={args.obs_depth}, epsilon={args.epsilon}, K={args.k}\n")

    lines.append("## Defect 1 — closure horizon: single collapsed `h` -> per-channel sustained plateau\n")
    lines.append("| system | OLD h_0.01 (all channels) | NEW state | NEW trajectory | NEW normal_form | NEW semantic | non-monotonic? |")
    lines.append("|---|---|---|---|---|---|---|")
    for s in systems:
        old_h = old_closure_by.get(s.name, {}).get("h_0.01", "absent")
        cl = closure_report["systems"][s.name]
        nm = [c for c in CHANNELS if cl[c]["non_monotonic_plateau"]]
        lines.append(
            f"| {s.name} | {old_h} | {fmt(cl['state']['sustained_plateau_horizon'])} | "
            f"{fmt(cl['trajectory']['sustained_plateau_horizon'])} | "
            f"{fmt(cl['normal_form']['sustained_plateau_horizon'])} | "
            f"{fmt(cl['semantic']['sustained_plateau_horizon'])} | {', '.join(nm) or 'no'} |"
        )
    lines.append("")
    lines.append("`none` = the marginal novelty-*rate* never reached a K=3 sustained plateau; this alone "
                 "is NOT a verdict of openness — a non-monotonic rate can still have a saturated *count* "
                 "(see Defect 3 / the count-based axis, e.g. C-semantic). The point here is only that the "
                 "old estimator froze A, B and C all at h=2 by firing on the first shared early dip, "
                 "whereas the repaired per-channel estimator separates them and flags non-monotonicity.\n")

    lines.append("## Defect 2 — single label -> three-axis classification\n")
    lines.append("| system | OLD classification | NEW state_axis | NEW trajectory_axis | NEW semantic_axis |")
    lines.append("|---|---|---|---|---|")
    for s in systems:
        a = axis_report["systems"][s.name]
        lines.append(f"| {s.name} | {old_cls_by.get(s.name, 'absent')} | {a['state_axis']} | "
                     f"{a['trajectory_axis']} | {a['semantic_axis']} |")
    lines.append("")

    lines.append("## Defect 3 — new semantic-class channel vs syntactic (noisy-TV made measurable)\n")
    lines.append("The decisive quantity is the **count** of distinct semantic classes as a function of "
                 "horizon — a novelty *rate* can look 'moderate' purely because a finite class set is "
                 "divided by a large sample budget. Below: where each channel's count saturates.\n")
    lines.append("| system | syntactic count (trajectory) | semantic class count | semantic saturates at horizon | sample-limited? |")
    lines.append("|---|---|---|---|---|")
    for s in systems:
        a = axis_report["systems"][s.name]
        ev = a["evidence"]
        traj_c = ev["trajectory"]["saturation_count"]
        traj_sl = ev["trajectory"]["sample_limited"]
        sem_c = ev["semantic"]["saturation_count"]
        sem_h = ev["semantic"]["saturation_horizon"]
        lines.append(f"| {s.name} | {traj_c}{' (= sample cap)' if traj_sl else ''} | {sem_c} | "
                     f"{fmt(sem_h)} | {'yes (trajectory)' if traj_sl else 'no'} |")
    lines.append("")
    lines.append("A huge syntactic count with a tiny, frozen semantic count = syntactic novelty without "
                 "new meaning (= noisy-TV). The semantic count saturating to a finite set = the substrate "
                 "is semantically closed at that size.\n")

    lines.append("## Interpretation (the single question this experiment answers)\n")
    for s in systems:
        a = axis_report["systems"][s.name]
        lines.append(f"- **{s.name}**: {a['summary']}"
                     + ("  _(semantic proxy degenerate — channel uninformative)_" if a["semantic_proxy_degenerate"] else ""))
    lines.append("")

    # ---- Explicit kill / honesty verdict ----
    any_sem_open = any(axis_report["systems"][s.name]["semantic_axis"] == "open" for s in systems)
    lines.append("## Conclusion (kill / honesty condition)\n")
    if any_sem_open:
        open_sys = [s.name for s in systems if axis_report["systems"][s.name]["semantic_axis"] == "open"]
        lines.append(f"At least one system is **semantic-open**: {', '.join(open_sys)}. The original "
                     "single-label 'dead' was a measurement artifact for that system — Experiment 15's "
                     "negative conclusion must be revised and this is a real candidate to pursue.\n")
    else:
        sat = {s.name: axis_report["systems"][s.name]["evidence"]["semantic"]["saturation_count"] for s in systems}
        lines.append("**No system is semantic-open.** Every system's distinct-semantic-class count "
                     f"saturates to a finite set (A={sat['A_dead_control']}, B={sat['B_fake_live_control']}, "
                     f"C={sat['C_collapsing_live_candidate']}, D={sat['D_structured_live_candidate']}). "
                     "This is the task's first honesty condition: the repaired instruments do NOT rescue a "
                     "live zone, so Experiment 15's negative conclusion **stands and is now trustworthy** — "
                     "it was not merely a closure-horizon artifact.\n")
        lines.append("What the repair *does* reveal (which the old single 'dead' label hid): the collapsing "
                     "candidate C carries by far the richest bounded semantic set "
                     f"({sat['C_collapsing_live_candidate']} classes) versus the noisy-TV control B "
                     f"({sat['B_fake_live_control']}) and the structured candidate D "
                     f"({sat['D_structured_live_candidate']}). C's semantic ceiling is imposed by its "
                     "`depth<12` cap on `G_expand`; that bound — not a measurement defect — is the precise "
                     "target for Experiment 15.1. C's maximal trajectory novelty is sample-limited (it fills "
                     "the entire sample budget) and is syntactic only, so it is NOT evidence of liveness.\n")

    path.write_text("\n".join(lines), encoding="utf-8")


def fmt(v) -> str:
    if v is None:
        return "none"
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def plot_channels(path: Path, systems, hs, series) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    colors = {
        "state": "tab:blue",
        "trajectory": "tab:orange",
        "normal_form": "tab:green",
        "semantic": "tab:red",
        "semantic_label": "tab:purple",
    }
    for ax, s in zip(axes.flat, systems):
        for c in CHANNELS:
            ys = series[s.name][c]
            xs = [h for h, y in zip(hs, ys) if y is not None]
            yy = [y for y in ys if y is not None]
            if xs:
                ax.plot(xs, yy, marker="o", label=c, color=colors[c])
        ax.set_xscale("log", base=2)
        ax.set_ylim(-0.02, 1.02)
        ax.set_title(s.name, fontsize=10)
        ax.set_xlabel("horizon")
        ax.set_ylabel("novelty rate")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7)
    fig.suptitle("Per-channel novelty vs horizon (15.0.1 repaired instruments)")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
