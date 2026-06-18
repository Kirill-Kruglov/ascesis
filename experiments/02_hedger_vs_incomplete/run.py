#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RAW = RESULTS / "raw"
SEEDS = list(range(2000, 2050))
EPISODE = 60
CAP = 1000.0
AGENTS = ["arithmetic_mean", "geometric_mean", "incomplete_preference"]

ENVIRONMENTS = [
    {
        "name": "train_scalar_stationary", "split": "train", "kind": "scalarizable", "regime_shift": False,
        "valid_geometric_mean_available": True,
        "actions": [
            {"name": "balanced", "gain": (1.05, 1.05), "risk": 0.02, "constraint_ok": True},
            {"name": "axis_a", "gain": (1.22, 0.92), "risk": 0.06, "constraint_ok": True},
            {"name": "axis_b", "gain": (0.92, 1.22), "risk": 0.06, "constraint_ok": True},
            {"name": "reserve", "gain": (1.01, 1.01), "risk": 0.00, "constraint_ok": True},
        ],
    },
    {
        "name": "train_scalar_shift", "split": "train", "kind": "scalarizable", "regime_shift": True,
        "valid_geometric_mean_available": True,
        "actions": [
            {"name": "balanced", "gain": (1.04, 1.04), "risk": 0.03, "constraint_ok": True},
            {"name": "early_a_late_b", "gain": (1.18, 0.96), "late_gain": (0.96, 1.18), "risk": 0.05, "constraint_ok": True},
            {"name": "lottery", "gain": (1.34, 0.84), "late_gain": (0.84, 1.34), "risk": 0.12, "constraint_ok": True},
            {"name": "reserve", "gain": (1.01, 1.01), "risk": 0.00, "constraint_ok": True},
        ],
    },
    {
        "name": "heldout_scalar_risk", "split": "heldout", "kind": "scalarizable", "regime_shift": False,
        "valid_geometric_mean_available": True,
        "actions": [
            {"name": "balanced", "gain": (1.045, 1.045), "risk": 0.03, "constraint_ok": True},
            {"name": "axis_a", "gain": (1.25, 0.90), "risk": 0.08, "constraint_ok": True},
            {"name": "axis_b", "gain": (0.90, 1.25), "risk": 0.08, "constraint_ok": True},
            {"name": "reserve", "gain": (1.01, 1.01), "risk": 0.00, "constraint_ok": True},
        ],
    },
    {
        "name": "heldout_scalar_shift", "split": "heldout", "kind": "scalarizable", "regime_shift": True,
        "valid_geometric_mean_available": True,
        "actions": [
            {"name": "balanced", "gain": (1.035, 1.035), "risk": 0.025, "constraint_ok": True},
            {"name": "specialist", "gain": (1.28, 0.88), "late_gain": (0.88, 1.28), "risk": 0.09, "constraint_ok": True},
            {"name": "reserve", "gain": (1.01, 1.01), "risk": 0.00, "constraint_ok": True},
        ],
    },
    {
        "name": "heldout_incommensurable_threshold", "split": "heldout", "kind": "incommensurable", "regime_shift": False,
        "valid_geometric_mean_available": False,
        "actions": [
            {"name": "extractive_growth", "gain": (1.42, None), "risk": 0.05, "constraint_ok": False, "invalid_proxy_constraint_value": 0.78},
            {"name": "preserve_threshold", "gain": (1.08, None), "risk": 0.02, "constraint_ok": True, "invalid_proxy_constraint_value": 1.00},
            {"name": "risky_compromise", "gain": (1.20, None), "risk": 0.08, "constraint_ok": "stochastic", "invalid_proxy_constraint_value": 0.91},
            {"name": "reserve", "gain": (1.01, None), "risk": 0.00, "constraint_ok": True, "invalid_proxy_constraint_value": 1.00},
        ],
    },
    {
        "name": "heldout_incommensurable_sacred_floor", "split": "heldout", "kind": "incommensurable", "regime_shift": False,
        "valid_geometric_mean_available": False,
        "actions": [
            {"name": "major_gain_violate_floor", "gain": (1.55, None), "risk": 0.04, "constraint_ok": False, "invalid_proxy_constraint_value": 0.74},
            {"name": "modest_gain_preserve_floor", "gain": (1.06, None), "risk": 0.01, "constraint_ok": True, "invalid_proxy_constraint_value": 1.00},
            {"name": "uncertain_mitigation", "gain": (1.23, None), "risk": 0.10, "constraint_ok": "stochastic", "invalid_proxy_constraint_value": 0.88},
            {"name": "reserve", "gain": (1.01, None), "risk": 0.00, "constraint_ok": True, "invalid_proxy_constraint_value": 1.00},
        ],
    },
]


def git_value(args):
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "unavailable"


def spec_hash():
    return hashlib.sha256((ROOT / "SPEC.md").read_bytes()).hexdigest()


def action_expected(agent, action, env):
    a, b = action["gain"]
    if agent == "arithmetic_mean":
        if env["kind"] == "incommensurable":
            # Invalid scalar baseline: arithmetic proxy treats the boolean as a tradeable number.
            b = action["invalid_proxy_constraint_value"]
        return a + b - 0.3 * action["risk"]
    if agent == "geometric_mean":
        if env["kind"] == "incommensurable":
            # Explicitly invalid proxy; report marks valid_geometric_mean_available=false.
            b = action["invalid_proxy_constraint_value"]
            return math.log(max(a, 1e-9)) + math.log(max(b, 1e-9)) - 8.0 * action["risk"] ** 2
        # Correct hedging approximation: expected log growth with a variance penalty.
        # For regime shifts, evaluate the declared early/late phases symmetrically.
        phases = [action["gain"]]
        if env.get("regime_shift") and "late_gain" in action:
            phases.append(action["late_gain"])
        log_terms = [math.log(max(x, 1e-9)) + math.log(max(y, 1e-9)) for x, y in phases]
        return sum(log_terms) / len(log_terms) - 8.0 * action["risk"] ** 2
    raise ValueError(agent)


def pareto_maximal(actions):
    maximal = []
    for x in actions:
        dominated = False
        for y in actions:
            if x is y:
                continue
            x_a = x["gain"][0]
            y_a = y["gain"][0]
            x_ok = x["constraint_ok"] is True
            y_ok = y["constraint_ok"] is True
            if y_ok and (not x_ok) and y_a >= x_a:
                dominated = True
            if x_ok == y_ok and y_a >= x_a and y["risk"] <= x["risk"] and (y_a > x_a or y["risk"] < x["risk"]):
                dominated = True
        if not dominated:
            maximal.append(x)
    return maximal


def choose_action(agent, env, seed):
    rng = random.Random(seed)
    actions = env["actions"]
    if agent in ("arithmetic_mean", "geometric_mean"):
        return max(actions, key=lambda a: (action_expected(agent, a, env), -a["risk"], a["name"])), False
    if agent == "incomplete_preference":
        if env["kind"] == "scalarizable":
            # Partial order over two numeric axes, conservative tie-break within maximal set.
            maximal = []
            for x in actions:
                xb = x["gain"]
                dominated = any(y["gain"][0] >= xb[0] and y["gain"][1] >= xb[1] and (y["gain"][0] > xb[0] or y["gain"][1] > xb[1]) for y in actions)
                if not dominated:
                    maximal.append(x)
            min_risk = min(a["risk"] for a in maximal)
            conservative = [a for a in maximal if a["risk"] == min_risk]
            return rng.choice(sorted(conservative, key=lambda a: a["name"])), len(maximal) > 1
        maximal = pareto_maximal(actions)
        admissible = [a for a in maximal if a["constraint_ok"] is True]
        if not admissible:
            return next(a for a in actions if a["name"] == "reserve"), True
        # Act from maximal admissible set; do not rank threshold violation against material gain.
        best_gain = max(a["gain"][0] for a in admissible)
        best = [a for a in admissible if a["gain"][0] == best_gain]
        return rng.choice(sorted(best, key=lambda a: a["name"])), True
    raise ValueError(agent)


def step(action, env, t, rng):
    a = action["gain"][0]
    if env.get("regime_shift") and t >= EPISODE // 2 and "late_gain" in action:
        a = action["late_gain"][0]
    numeric = max(0.0, a + rng.gauss(0, action["risk"]))
    numeric = min(1.70, numeric)
    violation = False
    if env["kind"] == "incommensurable":
        ok = action["constraint_ok"]
        if ok is False:
            violation = True
        elif ok == "stochastic":
            violation = rng.random() < min(0.85, 0.20 + action["risk"] * 4)
    return numeric, violation


def run_episode(agent, env, seed):
    stable_env = sum((i + 1) * ord(ch) for i, ch in enumerate(env["name"]))
    rng = random.Random(seed * 17 + stable_env % 10000)
    action, incomparable = choose_action(agent, env, seed)
    score = 0.0
    violations = 0
    for t in range(EPISODE):
        numeric, violation = step(action, env, t, rng)
        score += numeric
        violations += int(violation)
    score = min(CAP, score)
    if env["kind"] == "incommensurable":
        survived = violations == 0 and score >= EPISODE * 1.0
    else:
        survived = score >= EPISODE * 1.0
    return {"action": action["name"], "score": score, "survived": survived, "violations": violations, "incomparable": incomparable}


def summarize():
    detail, summary = [], []
    for env in ENVIRONMENTS:
        for agent in AGENTS:
            episodes = [run_episode(agent, env, seed) for seed in SEEDS]
            summary.append({
                "environment": env["name"], "split": env["split"], "kind": env["kind"], "agent": agent,
                "valid_geometric_mean_available": env["valid_geometric_mean_available"],
                "action_mode": max(set(e["action"] for e in episodes), key=[e["action"] for e in episodes].count),
                "survival_rate": sum(e["survived"] for e in episodes) / len(episodes),
                "mean_score": sum(e["score"] for e in episodes) / len(episodes),
                "mean_violations": sum(e["violations"] for e in episodes) / len(episodes),
                "incomparable_rate": sum(e["incomparable"] for e in episodes) / len(episodes),
            })
            for seed, ep in zip(SEEDS, episodes):
                detail.append({"environment": env["name"], "split": env["split"], "kind": env["kind"], "agent": agent, "seed": seed, **ep})
    wins, divergences = [], []
    for env in [e for e in ENVIRONMENTS if e["split"] == "heldout"]:
        inc = next(r for r in summary if r["environment"] == env["name"] and r["agent"] == "incomplete_preference")
        hed = next(r for r in summary if r["environment"] == env["name"] and r["agent"] == "geometric_mean")
        if inc["action_mode"] != hed["action_mode"]:
            divergences.append({"environment": env["name"], "geometric_mean": hed["action_mode"], "incomplete_preference": inc["action_mode"], "valid_geometric_mean_available": env["valid_geometric_mean_available"]})
        if env["valid_geometric_mean_available"] and inc["survival_rate"] > hed["survival_rate"] and inc["mean_violations"] <= hed["mean_violations"]:
            wins.append(env["name"])
    hedger_not_applicable = [e["name"] for e in ENVIRONMENTS if e["split"] == "heldout" and not e["valid_geometric_mean_available"]]
    finite_values = all(math.isfinite(r["mean_score"]) and 0 <= r["mean_score"] <= CAP for r in summary)
    nonscalar = [e for e in ENVIRONMENTS if e["kind"] == "incommensurable"]
    artifact_checks = {
        "finite_values": "passed" if finite_values else "failed",
        "agent_divergence": "passed" if divergences else "failed",
        "non_scalarizable_check": "passed" if all(not e["valid_geometric_mean_available"] for e in nonscalar) else "failed",
        "heldout_divergences": divergences,
        "hedger_not_applicable": hedger_not_applicable,
        "scalar_artifact_removed": "passed" if "heldout_scalar_risk" not in wins else "failed",
    }
    return summary, detail, wins, artifact_checks


def write_svg(rows):
    envs = [e["name"] for e in ENVIRONMENTS if e["split"] == "heldout"]
    width, height = 980, 430
    margin = 70
    barw = 18
    colors = {"arithmetic_mean": "#6b7280", "geometric_mean": "#b45309", "incomplete_preference": "#047857"}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    parts.append('<text x="490" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Held-out survival rate by environment</text>')
    plotw = width - 2 * margin
    for ei, env in enumerate(envs):
        x0 = margin + ei * (plotw / len(envs)) + 28
        for ai, agent in enumerate(AGENTS):
            r = next(r for r in rows if r["environment"] == env and r["agent"] == agent)
            h = r["survival_rate"] * 260
            x = x0 + ai * (barw + 4)
            y = height - margin - h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{barw}" height="{h:.1f}" fill="{colors[agent]}"/>')
        parts.append(f'<text x="{x0+30:.1f}" y="{height-38}" text-anchor="middle" font-family="sans-serif" font-size="10" transform="rotate(18 {x0+30:.1f} {height-38})">{env}</text>')
    parts.append(f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="#111"/>')
    for i, agent in enumerate(AGENTS):
        parts.append(f'<rect x="720" y="{55+i*22}" width="14" height="14" fill="{colors[agent]}"/>')
        parts.append(f'<text x="740" y="{67+i*22}" font-family="sans-serif" font-size="12">{agent}</text>')
    parts.append('</svg>')
    (RESULTS / "survival_by_environment.svg").write_text("\n".join(parts))


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    summary, detail, wins, artifact_checks = summarize()
    (RAW / "results.json").write_text(json.dumps({"summary": summary, "detail": detail, "incomplete_strict_wins_vs_hedger_when_geometric_mean_valid": wins, "hedger_not_applicable": artifact_checks["hedger_not_applicable"], "artifact_checks": artifact_checks}, indent=2))
    with (RAW / "results.csv").open("w", newline="") as f:
        fields = ["environment", "split", "kind", "agent", "valid_geometric_mean_available", "action_mode", "survival_rate", "mean_score", "mean_violations", "incomparable_rate"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(summary)
    write_svg(summary)
    report = ["# 02 Hedger vs Incomplete Report", "", f"SPEC hash: `{spec_hash()}`", "", "| environment | split | kind | agent | valid GM? | action | survival | score | violations | incomparable |", "|---|---|---|---|---:|---|---:|---:|---:|---:|"]
    for r in summary:
        report.append(f"| {r['environment']} | {r['split']} | {r['kind']} | {r['agent']} | {str(r['valid_geometric_mean_available']).lower()} | {r['action_mode']} | {r['survival_rate']:.2f} | {r['mean_score']:.2f} | {r['mean_violations']:.2f} | {r['incomparable_rate']:.2f} |")
    report += ["", "## Held-out Strict Wins Where Geometric Mean Is Valid", "", json.dumps(wins), "", "## Hedger Not Applicable", "", json.dumps(artifact_checks["hedger_not_applicable"]), "", "These are not wins over hedging. They are cases where the scalar hedger is undefined because the environment declares no valid common currency.", "", "## Sacred / Protected Values Legitimacy", "", "The `heldout_incommensurable_sacred_floor` environment is intended as a toy protected-value threshold: some violations are not tradeable for more of another good. This is grounded in Tetlock/Fiske work on taboo trade-offs and protected or sacred values. If that literature is accepted as a legitimate non-scalarizable structure, this branch remains live; if the toy floor is judged artificial, the result is an artifact.", "", "## Artifact Checks", "", f"- finite_values: `{artifact_checks['finite_values']}`", f"- agent_divergence: `{artifact_checks['agent_divergence']}`", f"- non_scalarizable_check: `{artifact_checks['non_scalarizable_check']}`", f"- scalar_artifact_removed: `{artifact_checks['scalar_artifact_removed']}`", f"- heldout_divergences: `{json.dumps(artifact_checks['heldout_divergences'])}`"]
    (RESULTS / "report.md").write_text("\n".join(report) + "\n")
    verdict = "valid result" if all(artifact_checks[k] == "passed" for k in ["finite_values", "agent_divergence", "non_scalarizable_check"]) else "artifact, not yet measuring the question"
    validation = ["# Validation Report: 02 Hedger vs Incomplete", "", "## Measures", "Does a held-out class of environments exist where incomplete preferences strictly outperform geometric-mean optimization? Links: `field_check.md` nodes 13 and 15; `questions.md` Bet-Hedging Challenge.", "", "## Artifact Checks", "", "| check | result | interpretation |", "|---|---|---|"]
    validation.append(f"| finite_values | {artifact_checks['finite_values']} | Bounded additive scores replace the prior 1e17 axis explosion. |")
    validation.append(f"| agent_divergence | {artifact_checks['agent_divergence']} | Held-out divergences: `{json.dumps(artifact_checks['heldout_divergences'])}`. |")
    validation.append(f"| non_scalarizable_check | {artifact_checks['non_scalarizable_check']} | Incommensurable envs set `valid_geometric_mean_available=false`; hedger there is undefined, not defeated. |")
    validation.append(f"| scalar_artifact_removed | {artifact_checks['scalar_artifact_removed']} | Corrected geometric hedger should remove the prior scalar-risk win by incomplete preferences. |")
    validation += ["", "## Hedger Not Applicable", "", json.dumps(artifact_checks["hedger_not_applicable"]), "", "## Sacred / Protected Values Legitimacy", "", "Manual decision required: if sacred/protected values are accepted as real non-scalarizable structures, the incommensurable branch remains live. If the sacred floor is judged artificial, this test does not support the branch.", "", "## Raw And Human-Readable Outputs", "", "- Raw: `results/raw/results.json`, `results/raw/results.csv`", "- Human-readable: `results/report.md`, `results/survival_by_environment.svg`", "", "## Verdict", "", f"{verdict}. Publication-grade status: needs human review of non-scalarizable environment legitimacy before publication; scalar-risk artifact status is `{artifact_checks['scalar_artifact_removed']}`."]
    (RESULTS / "validation_report.md").write_text("\n".join(validation) + "\n")
    manifest = {"git_head": git_value(["rev-parse", "HEAD"]), "git_commit_time": git_value(["show", "-s", "--format=%cI", "HEAD"]), "git_status_short": git_value(["status", "--short"]), "spec_sha256": spec_hash(), "seeds": [min(SEEDS), max(SEEDS)], "heldout_environments": [e["name"] for e in ENVIRONMENTS if e["split"] == "heldout"], "improvement_iterations": {a: 0 for a in AGENTS}}
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
