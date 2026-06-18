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
SEEDS = list(range(4000, 4050))
NS = [2, 4, 8, 16, 32]
WIDTHS = [0.15, 0.25, 0.35, 0.45, 0.55]
PROFILES = ["iid_beta", "clustered", "cross_cutting"]
GRID = [(i / 40, j / 40) for i in range(41) for j in range(41)]


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC.md").read_bytes()).hexdigest()


def agent_constraints(n, seed, profile):
    rng = random.Random(seed + n * 997)
    if profile == "iid_beta":
        return [(rng.betavariate(2, 2), rng.betavariate(2, 2)) for _ in range(n)]
    if profile == "clustered":
        centers = [(0.35, 0.40), (0.62, 0.58), (0.45, 0.68)]
        out = []
        for i in range(n):
            cx, cy = centers[i % len(centers)]
            out.append((min(1.0, max(0.0, rng.gauss(cx, 0.055))), min(1.0, max(0.0, rng.gauss(cy, 0.055)))))
        return out
    if profile == "cross_cutting":
        # Two independent cleavage dimensions: high/low A and high/low B recombine.
        # This is less coherent than aligned clusters but less adversarial than IID noise.
        centers = [(0.32, 0.32), (0.32, 0.68), (0.68, 0.32), (0.68, 0.68)]
        out = []
        for i in range(n):
            cx, cy = centers[(i + rng.randrange(len(centers))) % len(centers)]
            out.append((min(1.0, max(0.0, rng.gauss(cx, 0.06))), min(1.0, max(0.0, rng.gauss(cy, 0.06)))))
        return out
    raise ValueError(profile)


def admissible_size(n, width, seed, profile):
    ideals = agent_constraints(n, seed, profile)
    accepted = 0
    for x, y in GRID:
        ok = True
        for ax, ay in ideals:
            # L-infinity frame: no scalar aggregation of utility, only acceptance constraints.
            if max(abs(x - ax), abs(y - ay)) > width:
                ok = False
                break
        accepted += int(ok)
    return accepted, len(GRID)


def write_svg(rows):
    width, height = 920, 480
    margin = 60
    colors = {2: "#047857", 4: "#1d4ed8", 8: "#7c3aed", 16: "#b45309", 32: "#b91c1c"}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', '<text x="460" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Admissible set fraction vs frame width</text>']
    def sx(w): return margin + (w - min(WIDTHS)) / (max(WIDTHS) - min(WIDTHS)) * (width - 2 * margin)
    def sy(v): return height - margin - v * (height - 2 * margin)
    dash = {"iid_beta": "", "clustered": " stroke-dasharray=\"6 4\"", "cross_cutting": " stroke-dasharray=\"2 4\""}
    for profile in PROFILES:
        for n in NS:
            pts = [(sx(r["frame_width"]), sy(r["mean_fraction"])) for r in rows if r["n_agents"] == n and r["profile"] == profile]
            parts.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{colors[n]}" stroke-width="3"{dash[profile]}/>')
            for x, y in pts:
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{colors[n]}"/>')
    parts.append(f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="#111"/>')
    parts.append(f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="#111"/>')
    for i, n in enumerate(NS):
        parts.append(f'<rect x="710" y="{55+i*22}" width="14" height="14" fill="{colors[n]}"/>')
        parts.append(f'<text x="730" y="{67+i*22}" font-family="sans-serif" font-size="12">N={n}</text>')
    parts.append('<text x="710" y="185" font-family="sans-serif" font-size="12">solid: iid_beta</text>')
    parts.append('<text x="710" y="205" font-family="sans-serif" font-size="12">dashed: clustered</text>')
    parts.append('<text x="710" y="225" font-family="sans-serif" font-size="12">dotted: cross_cutting</text>')
    parts.append('</svg>')
    (RESULTS / "admissible_set_size.svg").write_text("\n".join(parts))


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    summary, detail = [], []
    for profile in PROFILES:
        for n in NS:
            for width in WIDTHS:
                fracs = []
                empties = 0
                for seed in SEEDS:
                    size, total = admissible_size(n, width, seed, profile)
                    frac = size / total
                    fracs.append(frac)
                    empties += int(size == 0)
                    detail.append({"profile": profile, "n_agents": n, "frame_width": width, "seed": seed, "admissible_size": size, "universe_size": total, "fraction": frac})
                summary.append({"profile": profile, "n_agents": n, "frame_width": width, "mean_fraction": sum(fracs) / len(fracs), "empty_rate": empties / len(SEEDS)})
    (RAW / "results.json").write_text(json.dumps({"summary": summary, "detail": detail}, indent=2))
    with (RAW / "results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["profile", "n_agents", "frame_width", "mean_fraction", "empty_rate"]); w.writeheader(); w.writerows(summary)
    write_svg(summary)
    clustered_large = [r for r in summary if r["profile"] == "clustered" and r["n_agents"] >= 16 and r["frame_width"] >= 0.45]
    clustered_persists = any(r["empty_rate"] >= 0.5 for r in clustered_large)
    cross_cutting_large = [r for r in summary if r["profile"] == "cross_cutting" and r["n_agents"] >= 16 and r["frame_width"] >= 0.45]
    cross_cutting_mean_empty = sum(r["empty_rate"] for r in cross_cutting_large) / len(cross_cutting_large)
    clustered_mean_empty = sum(r["empty_rate"] for r in clustered_large) / len(clustered_large)
    cross_cutting_stronger_than_clustered = cross_cutting_mean_empty >= clustered_mean_empty
    artifact_status = "passed" if not clustered_persists else "warning"
    report = ["# 04 Admissible Set Core Report", "", f"SPEC hash: `{spec_hash()}`", "", "| profile | N agents | frame width | mean admissible fraction | empty rate |", "|---|---:|---:|---:|---:|"]
    for r in summary:
        report.append(f"| {r['profile']} | {r['n_agents']} | {r['frame_width']:.2f} | {r['mean_fraction']:.4f} | {r['empty_rate']:.2f} |")
    report += ["", "## Artifact Checks", "", f"- collapse under clustered preferences check: `{artifact_status}`", f"- cross_cutting stronger than clustered collapse: `{str(cross_cutting_stronger_than_clustered).lower()}`", f"- clustered mean empty rate at N>=16,width>=0.45: `{clustered_mean_empty:.3f}`", f"- cross_cutting mean empty rate at N>=16,width>=0.45: `{cross_cutting_mean_empty:.3f}`"]
    (RESULTS / "report.md").write_text("\n".join(report) + "\n")
    validation = ["# Validation Report: 04 Admissible Set Core", "", "## Measures", "Can a bottom-up governor maintain a nonempty admissible set without scalar aggregation? Links: `field_check.md` nodes 12-14.", "", "## Artifact Checks", "", "| check | result | interpretation |", "|---|---|---|", f"| collapse under clustered preferences | {artifact_status} | Compares IID dispersed preferences to clustered structured disagreement. |", f"| cross-cutting cleavages | {'passed' if cross_cutting_stronger_than_clustered else 'warning'} | Adds independent cleavage dimensions; mean empty rate {cross_cutting_mean_empty:.3f} vs clustered {clustered_mean_empty:.3f} for N>=16,width>=0.45. |", "", "## Raw And Human-Readable Outputs", "", "- Raw: `results/raw/results.json`, `results/raw/results.csv`", "- Human-readable: `results/report.md`, `results/admissible_set_size.svg`", "", "## Verdict", "", "valid result if interpreted as profile-dependent; clustered and cross-cutting profiles are included to avoid worst-case-only pessimism."]
    (RESULTS / "validation_report.md").write_text("\n".join(validation) + "\n")
    manifest = {"git_head": git_value(["rev-parse", "HEAD"]), "git_commit_time": git_value(["show", "-s", "--format=%cI", "HEAD"]), "git_status_short": git_value(["status", "--short"]), "spec_sha256": spec_hash(), "seeds": [min(SEEDS), max(SEEDS)], "improvement_iterations": {"governor_core": 0}}
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
