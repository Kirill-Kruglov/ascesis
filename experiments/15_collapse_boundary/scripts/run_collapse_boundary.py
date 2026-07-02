#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

from collapse_boundary.explore import (
    canonical_term,
    canonical_trajectory,
    compression_stats,
    entropy,
    random_trajectory,
    term_features,
    trajectory_features,
)
from collapse_boundary.systems import build_systems
from collapse_boundary.types import Term


def horizons(max_horizon: int) -> list[int]:
    out = []
    h = 1
    while h <= max_horizon:
        out.append(h)
        h *= 2
    return out


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def accuracy(y_true: list[str], y_pred: list[str]) -> float:
    return sum(a == b for a, b in zip(y_true, y_pred)) / len(y_true) if y_true else 0.0


def majority(y: list[str]) -> str:
    return Counter(y).most_common(1)[0][0] if y else "NA"


def train_predict(train_x: list[dict[str, float]], train_y: list[str], test_x: list[dict[str, float]], seed: int) -> list[str]:
    if not train_y:
        return []
    if len(set(train_y)) < 2:
        return [train_y[0]] * len(test_x)
    model = Pipeline([
        ("vec", DictVectorizer()),
        ("rf", RandomForestClassifier(n_estimators=80, max_depth=9, random_state=seed)),
    ])
    model.fit(train_x, train_y)
    return [str(v) for v in model.predict(test_x)]


def memo_predict(train_keys: list[str], train_y: list[str], test_keys: list[str]) -> list[str]:
    default = majority(train_y)
    memory = {k: y for k, y in zip(train_keys, train_y)}
    return [memory.get(k, default) for k in test_keys]


def random_predict(train_y: list[str], n: int, rng: random.Random) -> list[str]:
    choices = sorted(set(train_y)) or ["NA"]
    return [rng.choice(choices) for _ in range(n)]


def make_dataset(system, horizon: int, samples: int, rng: random.Random, depth: int):
    trajectories = []
    terms = []
    normal_forms = []
    for _ in range(samples):
        initial = system.sampler(rng, depth)
        traj = random_trajectory(system, initial, horizon, rng)
        trajectories.append(traj)
        terms.extend(traj.terms)
        if traj.terminated:
            normal_forms.append(traj.final)
    return trajectories, terms, normal_forms


def eval_task(train_x, train_y, train_keys, test_x, test_y, test_keys, rng, seed) -> dict[str, float]:
    pred = train_predict(train_x, train_y, test_x, seed)
    maj = [majority(train_y)] * len(test_y)
    mem = memo_predict(train_keys, train_y, test_keys)
    rnd = random_predict(train_y, len(test_y), rng)
    return {
        "accuracy": accuracy(test_y, pred),
        "majority": accuracy(test_y, maj),
        "memorization": accuracy(test_y, mem),
        "random": accuracy(test_y, rnd),
    }


def learnability(system, horizon: int, samples: int, seed: int) -> dict[str, float]:
    rng = random.Random(seed)
    n_train = max(40, samples)
    n_test = max(40, samples // 3)
    train_traj, _, _ = make_dataset(system, horizon, n_train, rng, depth=2)
    test_traj, _, _ = make_dataset(system, horizon, n_test, rng, depth=5 + int(math.log2(max(1, horizon))))
    scores = []

    # Task 1: next-symbol/rule prediction.
    train_x = [term_features(t.initial) for t in train_traj]
    train_y = [t.rules[0] if t.rules else "NORMAL" for t in train_traj]
    test_x = [term_features(t.initial) for t in test_traj]
    test_y = [t.rules[0] if t.rules else "NORMAL" for t in test_traj]
    keys_train = [t.initial.shape() for t in train_traj]
    keys_test = [t.initial.shape() for t in test_traj]
    scores.append(eval_task(train_x, train_y, keys_train, test_x, test_y, keys_test, rng, seed))

    # Task 2: reachability using final positives and shuffled negatives.
    train_x = []
    train_y = []
    train_keys = []
    finals = [t.final for t in train_traj]
    for idx, traj in enumerate(train_traj):
        neg = finals[(idx + 7) % len(finals)]
        train_x.append(pair_features(traj.initial, traj.final)); train_y.append("yes"); train_keys.append(traj.initial.shape() + "=>" + traj.final.shape())
        train_x.append(pair_features(traj.initial, neg)); train_y.append("no"); train_keys.append(traj.initial.shape() + "=>" + neg.shape())
    test_x = []
    test_y = []
    test_keys = []
    finals_t = [t.final for t in test_traj]
    for idx, traj in enumerate(test_traj):
        neg = finals_t[(idx + 5) % len(finals_t)]
        test_x.append(pair_features(traj.initial, traj.final)); test_y.append("yes"); test_keys.append(traj.initial.shape() + "=>" + traj.final.shape())
        test_x.append(pair_features(traj.initial, neg)); test_y.append("no"); test_keys.append(traj.initial.shape() + "=>" + neg.shape())
    scores.append(eval_task(train_x, train_y, train_keys, test_x, test_y, test_keys, rng, seed + 1))

    # Task 3: normal-form class, if applicable.
    normal_train = [t for t in train_traj if t.terminated]
    normal_test = [t for t in test_traj if t.terminated]
    if normal_train and normal_test:
        train_x = [term_features(t.initial) for t in normal_train]
        train_y = [t.final.shape() for t in normal_train]
        # Guard against treating near-unique normal-form identities as a classification task.
        if len(set(train_y)) <= max(2, len(train_y) // 2):
            test_x = [term_features(t.initial) for t in normal_test]
            test_y = [t.final.shape() for t in normal_test]
            scores.append(eval_task(train_x, train_y, [t.initial.shape() for t in normal_train], test_x, test_y, [t.initial.shape() for t in normal_test], rng, seed + 2))

    # Task 4: trajectory property.
    train_x = [trajectory_features(t) for t in train_traj]
    train_y = [property_label(t) for t in train_traj]
    test_x = [trajectory_features(t) for t in test_traj]
    test_y = [property_label(t) for t in test_traj]
    scores.append(eval_task(train_x, train_y, [t.rule_shape() for t in train_traj], test_x, test_y, [t.rule_shape() for t in test_traj], rng, seed + 3))

    return {
        "learnability_score": sum(s["accuracy"] for s in scores) / len(scores),
        "majority_baseline": sum(s["majority"] for s in scores) / len(scores),
        "memorization_baseline": sum(s["memorization"] for s in scores) / len(scores),
        "random_baseline": sum(s["random"] for s in scores) / len(scores),
        "ood_accuracy": sum(s["accuracy"] for s in scores) / len(scores),
    }


def pair_features(a: Term, b: Term) -> dict[str, float]:
    fa = {"a:" + k: v for k, v in term_features(a).items()}
    fb = {"b:" + k: v for k, v in term_features(b).items()}
    out = {**fa, **fb}
    out["size_delta"] = b.size() - a.size()
    out["depth_delta"] = b.depth() - a.depth()
    return out


def property_label(traj) -> str:
    if traj.collapsing_steps > 0:
        return "uses_collapsing"
    if traj.terminated:
        return "terminates"
    if len(set(traj.rules)) < len(traj.rules):
        return "branch_reuse"
    if len(set(traj.terms)) < len(traj.terms):
        return "alternative_derivation"
    return "plain"


def closure_report(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for system, group in groupby(rows, "system").items():
        ordered = sorted(group, key=lambda r: int(r["horizon"]))
        h001 = None
        h0001 = None
        prev_score = None
        for row in ordered:
            score = max(float(row["state_novelty"]), float(row["trajectory_novelty"]))
            if prev_score is not None:
                delta = abs(score - prev_score)
                if h001 is None and delta < 0.01:
                    h001 = row["horizon"]
                if h0001 is None and delta < 0.001:
                    h0001 = row["horizon"]
            prev_score = score
        out.append({"system": system, "h_0.01": h001 or "no_plateau_observed", "h_0.001": h0001 or "no_plateau_observed"})
    return out

def noisy_tv_report(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for system, group in groupby(rows, "system").items():
        ordered = sorted(group, key=lambda r: int(r["horizon"]))
        last = ordered[-1]
        first = ordered[0]
        state_novelty = float(last["state_novelty"])
        trajectory_novelty = float(last["trajectory_novelty"])
        high_novelty = state_novelty > 0.5 or trajectory_novelty > 0.5
        flat_learning = float(last["ood_accuracy"]) <= float(last["majority_baseline"]) + 0.05
        weak_over_memorization = float(last["ood_accuracy"]) <= float(last["memorization_baseline"]) + 0.05
        no_normal_forms = str(last["normal_form_novelty"]) == "normal_form_absent"
        compression_too_easy = float(last["compression_ratio"]) < 0.03
        compression_not_improving = abs(float(last["compression_gain"])) < 0.02
        ood_not_improving = float(last["ood_accuracy"]) <= float(first["ood_accuracy"]) + 0.02
        score_parts = [high_novelty, compression_too_easy or compression_not_improving, ood_not_improving or flat_learning, no_normal_forms, weak_over_memorization]
        score = sum(int(v) for v in score_parts) / len(score_parts)
        reasons = []
        if high_novelty: reasons.append("novelty high")
        if compression_too_easy: reasons.append("compression extremely easy")
        elif compression_not_improving: reasons.append("compression gain low")
        if ood_not_improving: reasons.append("OOD learnability does not improve")
        elif flat_learning: reasons.append("OOD learnability flat vs majority")
        if no_normal_forms: reasons.append("normal forms absent")
        if weak_over_memorization: reasons.append("weak gain over memorization")
        out.append({"system": system, "noisy_tv_score": score, "reason": "; ".join(reasons)})
    return out

def decisions(rows: list[dict[str, object]], closure_rows, noisy_rows) -> dict[str, object]:
    by_noisy = {r["system"]: r for r in noisy_rows}
    by_closure = {r["system"]: r for r in closure_rows}
    systems = []
    best = None
    best_score = -1.0
    kill_conditions = []
    for system, group in groupby(rows, "system").items():
        last = sorted(group, key=lambda r: int(r["horizon"]))[-1]
        novelty = float(last["state_novelty"])
        trajectory_novelty = float(last["trajectory_novelty"])
        learn = float(last["learnability_score"])
        maj = float(last["majority_baseline"])
        mem = float(last["memorization_baseline"])
        noisy = float(by_noisy[system]["noisy_tv_score"])
        closure = by_closure[system]
        if system.startswith("A_"):
            if closure["h_0.01"] == "no_plateau_observed" and novelty > 0.05:
                cls = "inconclusive"
                kill_conditions.append("Dead control does not collapse")
            else:
                cls = "dead"
        elif system.startswith("B_"):
            # This is an explicit fake-live control. If it looks like a live candidate, metrics are too weak.
            cls = "fake_live"
            if learn > maj + 0.05 and noisy < 0.67:
                kill_conditions.append("Fake-live control looks learnable under current metrics")
        elif noisy >= 0.67 and max(novelty, trajectory_novelty) > 0.4:
            cls = "fake_live"
        elif novelty < 0.35 and closure["h_0.01"] != "no_plateau_observed":
            cls = "dead"
        elif max(novelty, trajectory_novelty) > 0.45 and learn > maj + 0.05 and learn > mem + 0.05 and noisy < 0.67:
            cls = "live_candidate"
        elif max(novelty, trajectory_novelty) > 0.45 and learn <= max(maj, mem) + 0.05:
            cls = "fake_live"
        else:
            cls = "inconclusive"
        score = max(novelty, trajectory_novelty) + max(0.0, learn - max(maj, mem)) - noisy
        if cls == "live_candidate" and score > best_score:
            best = system; best_score = score
        systems.append({
            "system": system,
            "classification": cls,
            "evidence": {
                "closure_horizon": closure,
                "novelty": novelty,
                "trajectory_novelty": trajectory_novelty,
                "learnability": learn,
                "majority": maj,
                "memorization": mem,
                "noisy_tv_score": noisy,
                "compression": float(last["compression_ratio"]),
                "ood": float(last["ood_accuracy"]),
            },
        })
    if kill_conditions:
        conclusion = "inconclusive"
        failure = "; ".join(sorted(set(kill_conditions)))
    elif best:
        conclusion = True
        failure = "none observed for best candidate"
    else:
        conclusion = "inconclusive"
        failure = "fake-live or finite collapse"
    global_conclusion = {
        "does_live_zone_exist_in_this_toy_setting": conclusion,
        "best_candidate_system": best or "none",
        "main_failure_mode": failure,
        "next_recommended_experiment": "richer proof-DAG substrate" if best else "fix metrics or strengthen structured/collapsing rewrite candidates and rerun",
    }
    return {"systems": systems, "global_conclusion": global_conclusion}

def groupby(rows, key):
    out = defaultdict(list)
    for row in rows:
        out[row[key]].append(row)
    return out


def plot_lines(path: Path, rows, y, title):
    plt.figure(figsize=(7, 4))
    for system, group in groupby(rows, "system").items():
        group = sorted(group, key=lambda r: int(r["horizon"]))
        plt.plot([r["horizon"] for r in group], [r[y] for r in group], marker="o", label=system.replace("_", " ")[:24])
    plt.xscale("log", base=2)
    plt.xlabel("horizon")
    plt.ylabel(y)
    plt.title(title)
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-horizon", type=int, default=64)
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    out = args.outputs
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    systems = build_systems()
    hs = horizons(args.max_horizon)
    metric_rows = []
    term_shape_rows = []
    traj_shape_rows = []
    compression_rows = []
    learn_rows = []
    prev_compression: dict[str, float] = {}

    for system in systems:
        for h in hs:
            sample_n = args.samples
            trajs, terms, normals = make_dataset(system, h, sample_n, rng, depth=2 + int(math.log2(h)))
            term_serials = [t.serialize() for t in terms]
            term_shapes = [canonical_term(t) for t in terms]
            traj_shapes = [canonical_trajectory(t) for t in trajs]
            normal_shapes = [n.shape() for n in normals]
            comp = compression_stats(term_serials)
            gain = prev_compression.get(system.name, comp["compression_ratio"]) - comp["compression_ratio"]
            prev_compression[system.name] = comp["compression_ratio"]
            learn = learnability(system, h, max(40, min(args.samples // 4, 1000)), args.seed + h)
            row = {
                "system": system.name,
                "horizon": h,
                "generated_terms": len(terms),
                "unique_terms": len(set(term_shapes)),
                "state_novelty": len(set(term_shapes)) / max(1, len(terms)),
                "terminating_trajectories": len(normals),
                "unique_normal_forms": len(set(normal_shapes)),
                "normal_form_novelty": "normal_form_absent" if not normals else len(set(normal_shapes)) / len(normals),
                "unique_trajectories": len(set(traj_shapes)),
                "trajectory_novelty": len(set(traj_shapes)) / max(1, len(trajs)),
                "term_shape_entropy": entropy(term_shapes),
                "trajectory_shape_entropy": entropy(traj_shapes),
                "compression_ratio": comp["compression_ratio"],
                "compression_gain": gain,
                **learn,
            }
            metric_rows.append(row)
            learn_rows.append({"system": system.name, "horizon": h, **learn})
            compression_rows.append({"system": system.name, "horizon": h, **comp, "compression_gain": gain})
            for shape, count in Counter(term_shapes).most_common(100):
                term_shape_rows.append({"system": system.name, "horizon": h, "shape": shape, "count": count, "fraction": count / len(term_shapes)})
            for shape, count in Counter(traj_shapes).most_common(100):
                traj_shape_rows.append({"system": system.name, "horizon": h, "shape": shape, "count": count, "fraction": count / len(traj_shapes)})

    closure_rows = closure_report(metric_rows)
    noisy_rows = noisy_tv_report(metric_rows)
    final = decisions(metric_rows, closure_rows, noisy_rows)
    summary = {"seed": args.seed, "samples": args.samples, "max_horizon": args.max_horizon, "systems": [s.name for s in systems]}

    write_json(out / "system_summary.json", summary)
    write_csv(out / "horizon_metrics.csv", metric_rows)
    write_csv(out / "novelty_curves.csv", [{"system": r["system"], "horizon": r["horizon"], "state_novelty": r["state_novelty"], "normal_form_novelty": r["normal_form_novelty"], "trajectory_novelty": r["trajectory_novelty"]} for r in metric_rows])
    write_csv(out / "learnability_curves.csv", learn_rows)
    write_json(out / "noisy_tv_report.json", noisy_rows)
    write_csv(out / "compression_report.csv", compression_rows)
    write_json(out / "closure_horizon_report.json", closure_rows)
    write_csv(out / "trajectory_shape_counts.csv", traj_shape_rows)
    write_csv(out / "term_shape_counts.csv", term_shape_rows)
    write_json(out / "final_decision.json", final)
    plot_lines(out / "novelty_vs_horizon.png", metric_rows, "state_novelty", "State novelty vs horizon")
    plot_lines(out / "learnability_vs_horizon.png", metric_rows, "learnability_score", "Learnability vs horizon")
    plot_lines(out / "compression_vs_horizon.png", metric_rows, "compression_ratio", "Compression ratio vs horizon")
    plot_lines(out / "closure_horizon_comparison.png", metric_rows, "trajectory_novelty", "Trajectory novelty vs horizon")
    plt.figure(figsize=(6, 5))
    for system, group in groupby(metric_rows, "system").items():
        last = sorted(group, key=lambda r: int(r["horizon"]))[-1]
        plt.scatter(float(last["state_novelty"]), float(last["learnability_score"]), label=system)
    plt.xlabel("novelty")
    plt.ylabel("learnability")
    plt.title("Novelty/learnability phase plot")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(out / "novelty_learnability_phase_plot.png")
    plt.close()
    print(json.dumps(final, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
