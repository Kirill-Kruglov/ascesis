#!/usr/bin/env python3
import csv
import hashlib
import json
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"
SEEDS = list(range(5000, 5050))
BENEFITS = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.2, 0.4, 0.8]
PENALTIES = [0.0, 0.1, 0.2, 0.4, 0.8]
MAINTENANCE_COSTS = [0.0, 0.02, 0.05]
HORIZON = 40


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC.md").read_bytes()).hexdigest()


def run_one(benefit, penalty, maintenance_cost, seed):
    rng = random.Random(seed + int(benefit * 1000) * 37 + int(penalty * 1000) * 101 + int(maintenance_cost * 1000) * 211)
    order = "partial"
    trace = []
    first_completion = None
    for t in range(HORIZON):
        incommensurable_pressure = 1.0 if rng.random() < 0.45 else 0.0
        keep_value = 0.05 + penalty * incommensurable_pressure
        complete_value = benefit - maintenance_cost - penalty * incommensurable_pressure + rng.gauss(0, 0.02)
        if order == "partial" and complete_value > keep_value:
            order = "complete"
            first_completion = t
        # Once completed, this toy agent does not recover partiality without an external proof obligation.
        trace.append(order)
    return {"remained_partial": order == "partial", "first_completion": first_completion, "trace": trace}


def color(v):
    # v in [0,1], green stable, red unstable.
    r = int(185 * (1 - v) + 4 * v)
    g = int(28 * (1 - v) + 120 * v)
    b = int(28 * (1 - v) + 87 * v)
    return f"#{r:02x}{g:02x}{b:02x}"


def write_svg(rows):
    cell = 42
    width, height = 620, 430
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', '<text x="235" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Fraction remaining partial</text>']
    x0, y0 = 95, 65
    for i, benefit in enumerate(BENEFITS):
        parts.append(f'<text x="{x0+i*cell+cell/2}" y="55" text-anchor="middle" font-family="sans-serif" font-size="11">b={benefit}</text>')
    for j, penalty in enumerate(PENALTIES):
        parts.append(f'<text x="72" y="{y0+j*cell+cell/2+4}" text-anchor="end" font-family="sans-serif" font-size="11">p={penalty}</text>')
        for i, benefit in enumerate(BENEFITS):
            r = next(r for r in rows if r["benefit"] == benefit and r["penalty"] == penalty)
            v = r["partial_fraction"]
            x, y = x0 + i * cell, y0 + j * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell-4}" height="{cell-4}" fill="{color(v)}"/>')
            parts.append(f'<text x="{x+cell/2-2}" y="{y+cell/2+4}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="white">{v:.2f}</text>')
    parts.append('</svg>')
    (RESULTS / "partial_stability_heatmap.svg").write_text("\n".join(parts))


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    detail, summary = [], []
    for maintenance_cost in MAINTENANCE_COSTS:
        for benefit in BENEFITS:
            for penalty in PENALTIES:
                outcomes = [run_one(benefit, penalty, maintenance_cost, seed) for seed in SEEDS]
                partial_fraction = sum(o["remained_partial"] for o in outcomes) / len(outcomes)
                completion_times = [o["first_completion"] for o in outcomes if o["first_completion"] is not None]
                summary.append({"maintenance_cost": maintenance_cost, "benefit": benefit, "penalty": penalty, "partial_fraction": partial_fraction, "mean_first_completion": None if not completion_times else sum(completion_times) / len(completion_times)})
                for seed, out in zip(SEEDS, outcomes):
                    detail.append({"maintenance_cost": maintenance_cost, "benefit": benefit, "penalty": penalty, "seed": seed, **out})
    (RAW / "results.json").write_text(json.dumps({"summary": summary, "detail": detail}, indent=2))
    with (RAW / "results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["maintenance_cost", "benefit", "penalty", "partial_fraction", "mean_first_completion"]); w.writeheader(); w.writerows(summary)
    write_svg(summary)
    fine = [r for r in summary if r["benefit"] <= 0.10]
    has_intermediate = any(0.05 < r["partial_fraction"] < 0.95 for r in fine)
    hard_step = not has_intermediate
    artifact_status = "passed" if has_intermediate else "failed"
    robust_collapse = all(r["partial_fraction"] == 0.0 for r in summary if r["benefit"] >= 0.04 and r["maintenance_cost"] == max(MAINTENANCE_COSTS))
    costly_maintenance_rescue = any(r["partial_fraction"] > 0.0 for r in summary if r["benefit"] >= 0.04 and r["maintenance_cost"] == max(MAINTENANCE_COSTS))
    report = ["# 05 Reflective Stability Report", "", f"SPEC hash: `{spec_hash()}`", "", "| maintenance cost | convenience benefit | violation penalty | partial fraction | mean first completion |", "|---:|---:|---:|---:|---:|"]
    for r in summary:
        m = "" if r["mean_first_completion"] is None else f"{r['mean_first_completion']:.2f}"
        report.append(f"| {r['maintenance_cost']:.2f} | {r['benefit']:.2f} | {r['penalty']:.2f} | {r['partial_fraction']:.2f} | {m} |")
    report += ["", "## Artifact Checks", "", f"- gradual collapse check: `{artifact_status}`", f"- hard step detected: `{str(hard_step).lower()}`", f"- robust collapse under maintenance cost: `{str(robust_collapse).lower()}`", f"- costly maintenance rescues partiality: `{str(costly_maintenance_rescue).lower()}`", "", "Expected failure mode: low penalty and high convenience should collapse to a complete order. If maintenance cost rescues partiality, previous erosion was partly an artifact of free tie-breaker maintenance."]
    (RESULTS / "report.md").write_text("\n".join(report) + "\n")
    validation = ["# Validation Report: 05 Reflective Stability", "", "## Measures", "Does incompleteness remain stable under self-modification pressure or erode into a complete order? Links: `field_check.md` node 1 and `questions.md` Active Spine Questions.", "", "## Artifact Checks", "", "| check | result | interpretation |", "|---|---|---|", f"| gradual collapse | {artifact_status} | Fine sweep over convenience 0.00..0.10 should show intermediate partial fractions, not only a hard step. |", f"| hard step detected | {str(hard_step).lower()} | `true` means the result may still be threshold-driven. |", f"| maintenance cost | {'passed' if robust_collapse or costly_maintenance_rescue else 'warning'} | Robust collapse={str(robust_collapse).lower()}; costly maintenance rescues partiality={str(costly_maintenance_rescue).lower()}. |", "", "## Raw And Human-Readable Outputs", "", "- Raw: `results/raw/results.json`, `results/raw/results.csv`", "- Human-readable: `results/report.md`, `results/partial_stability_heatmap.svg`", "", "## Verdict", "", f"{'valid result' if artifact_status == 'passed' else 'artifact, not yet measuring the question'}."]
    (RESULTS / "validation_report.md").write_text("\n".join(validation) + "\n")
    manifest = {"git_head": git_value(["rev-parse", "HEAD"]), "git_commit_time": git_value(["show", "-s", "--format=%cI", "HEAD"]), "git_status_short": git_value(["status", "--short"]), "spec_sha256": spec_hash(), "seeds": [min(SEEDS), max(SEEDS)], "improvement_iterations": {"partial_agent": 0, "complete_order_variant": 0}}
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
