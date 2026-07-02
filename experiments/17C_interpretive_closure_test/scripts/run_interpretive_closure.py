#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXP16_SRC = ROOT.parents[0] / "16_consequence_vs_feature" / "src"
EXP17A2_SRC = ROOT.parents[0] / "17A.2_Semantic_Perturbation_Taxonomy" / "src"
EXP17A_SRC = ROOT.parents[0] / "17A_backbone_consequence" / "src"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(EXP16_SRC))
sys.path.insert(0, str(EXP17A2_SRC))
sys.path.insert(0, str(EXP17A_SRC))

from interpretive_closure.closure import compute_closure_state, group_records  # noqa: E402

RUN17A2_PATH = ROOT.parents[0] / "17A.2_Semantic_Perturbation_Taxonomy" / "scripts" / "run_semantic_taxonomy.py"
spec = importlib.util.spec_from_file_location("run_semantic_taxonomy", RUN17A2_PATH)
run17a2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run17a2)  # type: ignore[union-attr]

CLASS_A = {"P4_alpha_rename", "P9_split_node", "P10_replace_subgraph"}
CLASS_B = set(run17a2.ALL_OPS) - CLASS_A


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def records_for_keys(records: list[dict[str, Any]], keys: set[Any]) -> list[dict[str, Any]]:
    return [r for r in records if r["consequence_key"] in keys]


def weighted_summary(df: pd.DataFrame, closure_scores: dict[Any, float], label: str, id_to_key: dict[str, Any]) -> dict[str, Any]:
    if df.empty:
        return {"label": label, "analyzed_class_count": 0, "broken_class_count": 0, "surviving_class_count": 0, "surviving_fraction": 0.0, "mean_auc_gns": None}
    weights = []
    for _, row in df.iterrows():
        key = id_to_key.get(row["class_id"])
        weights.append(float(closure_scores.get(key, 0.0)) if key is not None else 0.0)
    total_w = sum(weights) or len(weights)
    broken = int(df["broken"].sum()) if "broken" in df else int(df["attack_cost"].notna().sum())
    surviving = len(df) - broken
    auc = float(df["auc_gns"].mean()) if "auc_gns" in df and len(df) else None
    weighted_auc = sum(w * a for w, a in zip(weights, df["auc_gns"].fillna(0.0))) / total_w if len(df) else None
    weighted_survive = sum(w for w, b in zip(weights, df["broken"]) if not bool(b)) / total_w if "broken" in df else None
    return {
        "label": label,
        "analyzed_class_count": int(len(df)),
        "broken_class_count": broken,
        "surviving_class_count": surviving,
        "surviving_fraction": surviving / len(df),
        "mean_auc_gns": auc,
        "weighted_auc_gns": weighted_auc,
        "weighted_surviving_fraction": weighted_survive,
    }


def merge_condition_attack(name: str, records: list[dict[str, Any]], args, out: Path, closure_state: dict[str, Any] | None = None, weak: bool = False) -> tuple[dict[str, Any], pd.DataFrame]:
    a_summary, a_df = run17a2.analyze(records, CLASS_A, args, f"{name}_class_a")
    b_summary, b_df = run17a2.analyze(records, CLASS_B, args, f"{name}_class_b")
    a_df = a_df.copy(); b_df = b_df.copy()
    a_df["perturbation_class"] = "A"
    b_df["perturbation_class"] = "B"
    attack = pd.concat([a_df, b_df], ignore_index=True)
    attack.to_csv(out / f"{name}_attack.csv", index=False)
    if closure_state and weak:
        groups = group_records(records)
        id_to_key = {run17a2.stable_id(k): k for k in groups}
        weak_a = weighted_summary(a_df, closure_state["scores"], f"{name}_class_a_weighted", id_to_key)
        weak_b = weighted_summary(b_df, closure_state["scores"], f"{name}_class_b_weighted", id_to_key)
        a_summary = {**a_summary, **{"weighted_auc_gns": weak_a["weighted_auc_gns"], "weighted_surviving_fraction": weak_a["weighted_surviving_fraction"]}}
        b_summary = {**b_summary, **{"weighted_auc_gns": weak_b["weighted_auc_gns"], "weighted_surviving_fraction": weak_b["weighted_surviving_fraction"]}}
    summary = {
        "condition": name,
        "class_a": a_summary,
        "class_b": b_summary,
    }
    return summary, attack


def closure_metrics_rows(closure_state: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for key, score in closure_state["scores"].items():
        feat = closure_state["features"][key]
        rows.append({
            "class_id": run17a2.stable_id(key),
            "interpreter_score": score,
            "closure_active": key in closure_state["active_keys"],
            "closure_dead": key in closure_state["dead_keys"],
            **feat,
        })
    return rows


def class_a_invariant_ids(open_attack: pd.DataFrame) -> set[str]:
    class_a = open_attack[open_attack["perturbation_class"] == "A"]
    return set(class_a[class_a["broken"] == False]["class_id"])


def decide(open_summary, weak_summary, strong_summary, closure_state, dead_df, active_df) -> dict[str, Any]:
    open_a = open_summary["class_a"]["surviving_fraction"]
    strong_a = strong_summary["class_a"]["surviving_fraction"]
    open_b = open_summary["class_b"]["surviving_fraction"]
    strong_b = strong_summary["class_b"]["surviving_fraction"]
    dead_invariant = len(dead_df)
    active_count = len(active_df)
    total = closure_state["metrics"]["num_classes"]
    dead_frac = dead_invariant / max(1, total)
    strong_selectivity_gain = strong_b - open_b
    if active_count < 20:
        classification = "Inconclusive"
        reason = "Too few closure-active classes remain for meaningful comparison."
    elif active_count / max(1, total) < 0.05:
        classification = "Closure_artifact"
        reason = "Closure reduces class diversity too aggressively."
    elif dead_frac > 0.25 or abs(strong_selectivity_gain) > 0.10:
        classification = "H3_supported"
        reason = "Closure-active subset differs materially from raw consequence-invariant classes."
    elif abs(open_a - strong_a) < 0.05 and abs(open_b - strong_b) < 0.05 and dead_invariant == 0:
        classification = "H2_sufficient"
        reason = "Closed loop adds no measurable explanatory separation."
    else:
        classification = "H3_supported"
        reason = "Closure exposes consequence-invariant but closure-dead classes or changes selectivity."
    return {
        "classification": classification,
        "reason": reason,
        "evidence": {
            "open_class_a_surviving_fraction": open_a,
            "strong_class_a_surviving_fraction": strong_a,
            "open_class_b_surviving_fraction": open_b,
            "strong_class_b_surviving_fraction": strong_b,
            "closure_active_count": active_count,
            "closure_total_classes": total,
            "closure_dead_invariant_count": dead_invariant,
            "closure_dead_invariant_fraction": dead_frac,
            "strong_class_b_selectivity_gain": strong_selectivity_gain,
        },
    }


def write_notes(path: Path) -> None:
    path.write_text("""# Implementation Notes\n\n- The DAG generator and consequence verifier are reused unchanged.\n- The closure loop does not use external labels, embeddings, ontologies, internet data, or human semantic judgments.\n- Interpreter state is computed from internally derivable quantities: consequence frequency, operator diversity, DAG diversity, expression depth, intervention/conditional role, and iterative reuse across operator/depth channels.\n- Weak closure reweights attack summaries by interpreter score but does not forbid derivations.\n- Strong closure prunes to closure-active consequence classes using the internally computed score threshold.\n- Class A/Class B perturbation taxonomy is reused from 17A.2.\n""", encoding="utf-8")


def write_final(path: Path, decision, open_summary, weak_summary, strong_summary, closure_state, dead_df, active_df) -> None:
    lines = [
        "# Experiment 17C - Consequence Invariance vs Interpretive Closure", "",
        "## Final Decision", "", f"Classification: `{decision['classification']}`.", "", decision["reason"], "",
        "## Core Result", "",
        f"Closure active classes: {len(active_df)} / {closure_state['metrics']['num_classes']}",
        f"Closure-dead Class-A-invariant classes: {len(dead_df)}", "",
        "## Open vs Weak Closure vs Strong Closure", "",
        f"Open Class A survive: {open_summary['class_a']['surviving_fraction']:.6g}",
        f"Weak Class A survive: {weak_summary['class_a']['surviving_fraction']:.6g}; weighted={weak_summary['class_a'].get('weighted_surviving_fraction')}",
        f"Strong Class A survive: {strong_summary['class_a']['surviving_fraction']:.6g}", "",
        f"Open Class B survive: {open_summary['class_b']['surviving_fraction']:.6g}",
        f"Weak Class B survive: {weak_summary['class_b']['surviving_fraction']:.6g}; weighted={weak_summary['class_b'].get('weighted_surviving_fraction')}",
        f"Strong Class B survive: {strong_summary['class_b']['surviving_fraction']:.6g}", "",
        "## Required Questions", "",
        f"1. Do consequence-invariant classes coincide with closure-active classes? {'No' if len(dead_df) else 'Mostly yes'}.",
        f"2. Are there Class-A-invariant classes that are closure-dead? {'Yes' if len(dead_df) else 'No'}; count={len(dead_df)}.",
        f"3. Does interpretive closure improve selectivity under theory-changing perturbations? {'Yes' if abs(decision['evidence']['strong_class_b_selectivity_gain']) > 0.10 else 'No clear improvement'}.",
        f"4. Does closure merely prune the space, or identify a distinct semantic subset? {'Distinct subset' if len(active_df) > 20 and len(dead_df) else 'Likely pruning/no separation'}.",
        f"5. Does this support H2-rel, H3, or neither? {decision['classification']}.",
        "6. Strongest counterexample against H2-rel: Class-A-invariant but closure-dead classes in `closure_dead_classes.csv`.",
        "7. Strongest counterexample against H3: closure-active classes still break under Class B in `strong_closure_attack.csv`.", "",
        "## Artifacts", "", "See outputs_17C/*.json, *.csv, implementation_notes.md, final_decision.md.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 17C interpretive closure test")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-dags", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--exprs-per-dag-depth", type=int, default=80)
    parser.add_argument("--max-analyzed-classes", type=int, default=900)
    parser.add_argument("--pairs-per-class", type=int, default=2)
    parser.add_argument("--cross-pairs-per-class", type=int, default=2)
    parser.add_argument("--max-attack-budget", type=int, default=4)
    parser.add_argument("--candidate-budget", type=int, default=60)
    parser.add_argument("--beam-width", type=int, default=8)
    parser.add_argument("--closure-quantile", type=float, default=0.60)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17C")
    args = parser.parse_args()
    out = ensure(args.outputs)
    records = run17a2.build_records(args.seed, args.num_dags, args.max_depth, args.exprs_per_dag_depth)
    attack_args = SimpleNamespace(**vars(args))

    closure_state = compute_closure_state(records, strong_quantile=args.closure_quantile)
    active_records = records_for_keys(records, closure_state["active_keys"])

    open_summary, open_attack = merge_condition_attack("open", records, attack_args, out)
    weak_summary, weak_attack = merge_condition_attack("weak_closure", records, attack_args, out, closure_state, weak=True)
    strong_summary, strong_attack = merge_condition_attack("strong_closure", active_records, attack_args, out)

    metrics = pd.DataFrame(closure_metrics_rows(closure_state))
    metrics.to_csv(out / "closure_metrics.csv", index=False)
    invariant_ids = class_a_invariant_ids(open_attack)
    dead_df = metrics[(metrics["class_id"].isin(invariant_ids)) & (metrics["closure_dead"] == True)].copy()
    active_df = metrics[metrics["closure_active"] == True].copy()
    dead_df.to_csv(out / "closure_dead_classes.csv", index=False)
    active_df.to_csv(out / "closure_active_classes.csv", index=False)

    decision = decide(open_summary, weak_summary, strong_summary, closure_state, dead_df, active_df)
    write_json(out / "open_summary.json", open_summary)
    write_json(out / "weak_closure_summary.json", weak_summary)
    write_json(out / "strong_closure_summary.json", strong_summary)
    write_json(out / "class_a_comparison.json", {"open": open_summary["class_a"], "weak": weak_summary["class_a"], "strong": strong_summary["class_a"]})
    write_json(out / "class_b_comparison.json", {"open": open_summary["class_b"], "weak": weak_summary["class_b"], "strong": strong_summary["class_b"]})
    write_json(out / "h2_vs_h3_decision.json", decision)
    write_json(out / "failure_examples.json", {
        "h2_counterexamples": dead_df.head(10).to_dict(orient="records"),
        "h3_counterexamples": strong_attack[(strong_attack["perturbation_class"] == "B") & (strong_attack["broken"] == True)].head(10).to_dict(orient="records"),
    })
    write_notes(out / "implementation_notes.md")
    write_final(out / "final_decision.md", decision, open_summary, weak_summary, strong_summary, closure_state, dead_df, active_df)
    print(json.dumps({
        "classification": decision["classification"],
        "closure_active_classes": len(active_df),
        "closure_dead_invariant_classes": len(dead_df),
        "open_class_b_survival": open_summary["class_b"]["surviving_fraction"],
        "strong_class_b_survival": strong_summary["class_b"]["surviving_fraction"],
        "outputs": str(out),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
