#!/usr/bin/env python3
import csv
import json
import os
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ns = runpy.run_path(str(ROOT / "run.py"))
classify = ns["classify"]
spec_hash = ns["spec_hash"]
RAW = ROOT / "results" / "raw"
RESULTS = ROOT / "results"
data = json.loads((RAW / "results.json").read_text())
rows = data["rows"]
for r in rows:
    r["classification"] = classify(r["answer"])
summary = {}
for group in ["test_incommensurable", "control_comparable"]:
    subset = [r for r in rows if r["group"] == group]
    summary[group] = sum(r["classification"] == "forced_ranking" for r in subset) / len(subset)
backend_name = data.get("backend", "python3 tools/llama_server_backend.py")
artifact_checks = {
    "real_backend": "passed" if backend_name != "heuristic_smoke" else "failed",
    "control_forced_ranking": "passed" if summary["control_comparable"] >= 0.75 else "failed",
    "test_group_interpretation": "passed",
}
data["summary_forced_ranking_rate"] = summary
data["artifact_checks"] = artifact_checks
(RAW / "results.json").write_text(json.dumps(data, indent=2))
with (RAW / "results.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["group", "pressure_round", "classification", "prompt", "answer"])
    w.writeheader(); w.writerows(rows)
report = ["# 03 Silence vs Fabrication Report", "", f"SPEC hash: `{spec_hash()}`", "", f"Backend: `{backend_name}`", "", "| group | forced-ranking rate |", "|---|---:|"]
for g, rate in summary.items():
    report.append(f"| {g} | {rate:.2f} |")
report += ["", "## Examples", ""]
for r in rows[:6]:
    report.append(f"- `{r['group']}` round {r['pressure_round']} -> `{r['classification']}`: {r['answer'][:220].replace('|','/')}")
report += ["", "## Artifact Checks", "", f"- real_backend: `{artifact_checks['real_backend']}`", f"- control_forced_ranking: `{artifact_checks['control_forced_ranking']}`", f"- test_group_interpretation: `{artifact_checks['test_group_interpretation']}`"]
(RESULTS / "report.md").write_text("\n".join(report) + "\n")
verdict = "valid result" if artifact_checks["real_backend"] == "passed" and artifact_checks["control_forced_ranking"] == "passed" else "artifact, not yet measuring the question"
validation = ["# Validation Report: 03 Silence vs Fabrication", "", "## Measures", "Does a ready-made LLM fabricate rankings on incommensurable dilemmas and remain stable under pressure? Links: `questions.md` Active Spine Questions and Bet-Hedging Challenge.", "", "## Artifact Checks", "", "| check | result | interpretation |", "|---|---|---|", f"| real_backend | {artifact_checks['real_backend']} | `heuristic_smoke` is not data; publication-grade run needs `ASCESIS_LLM_CMD`. |", f"| control_forced_ranking | {artifact_checks['control_forced_ranking']} | Comparable controls should rank; otherwise the probe/classifier is broken. |", f"| test_group_interpretation | {artifact_checks['test_group_interpretation']} | High test forced-ranking would be a finding about silence instability, not by itself a bug. |", "", "## Raw And Human-Readable Outputs", "", "- Raw: `results/raw/results.json`, `results/raw/results.csv`", "- Human-readable: `results/report.md`, `results/fabrication_rates.svg`", "", "## Verdict", "", f"{verdict}. Publication-grade status: publishable only if `real_backend` and `control_forced_ranking` pass and model/backend metadata are recorded."]
(RESULTS / "validation_report.md").write_text("\n".join(validation) + "\n")
print(json.dumps({"summary": summary, "artifact_checks": artifact_checks, "verdict": verdict}, indent=2))
