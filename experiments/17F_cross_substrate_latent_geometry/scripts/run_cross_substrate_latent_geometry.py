#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cross_substrate_latent_geometry.analysis import analyze_substrate, ensure, write_json  # noqa: E402
from cross_substrate_latent_geometry.substrates import (  # noqa: E402
    dfa_substrate,
    directed_graph_substrate,
    load_causal_dag_baseline,
    rewrite_substrate,
)


def global_decision(summary: pd.DataFrame) -> dict[str, object]:
    cls = dict(zip(summary["substrate"], summary["local_classification"]))
    non_causal = [s for s in summary["substrate"] if s != "S1_causal_dag"]
    non_causal_multi = [s for s in non_causal if cls.get(s) == "multi_axis"]
    s1_multi = cls.get("S1_causal_dag") == "multi_axis"
    control_like = int((summary["local_classification"] == "control_artifact").sum())
    no_structure = int((summary["local_classification"] == "no_structure").sum())
    if s1_multi and not non_causal_multi:
        classification = "DAG_artifact"
        interpretation = "Only the causal-DAG substrate reproduced the 17E multi-axis pattern."
    elif s1_multi and len(non_causal_multi) == len(non_causal):
        classification = "Finite_generator_generic"
        interpretation = "All tested finite substrates reproduced the 17E pattern."
    elif s1_multi and non_causal_multi:
        classification = "Mixed"
        interpretation = "The pattern reproduced outside causal DAGs, but not uniformly enough to claim genericity."
    elif control_like >= 2:
        classification = "Metric_artifact"
        interpretation = "Controls or metric artifacts dominate multiple substrates."
    elif no_structure >= 2:
        classification = "Inconclusive"
        interpretation = "Too many substrates collapsed or lacked enough structure for a clean falsification."
    else:
        classification = "Causality_required" if s1_multi else "Inconclusive"
        interpretation = "Current evidence does not support generic cross-substrate reproduction."
    return {
        "classification": classification,
        "interpretation": interpretation,
        "local_classifications": cls,
        "non_causal_multi_axis_count": len(non_causal_multi),
        "substrate_count": int(len(summary)),
        "kill_conditions": {
            "only_S1_reproduces_pattern": bool(s1_multi and not non_causal_multi),
            "non_causal_reproduces_pattern": bool(non_causal_multi),
            "at_least_two_nontrivial_failures": int(sum(1 for s in non_causal if cls.get(s) != "multi_axis")) >= 2,
            "controls_reproduce_across_substrates": control_like >= 2,
        },
    }


def write_comparison(path: Path, summary: pd.DataFrame, decision: dict[str, object]) -> None:
    lines = [
        "# Experiment 17F - Cross-Substrate Comparison",
        "",
        f"Global classification: `{decision['classification']}`",
        "",
        str(decision["interpretation"]),
        "",
        "| substrate | classes | Class A survive | Class B survive | M135 R2 k=1 | AUC latent1 | AUC latent2 | AUC latent3 | controls AUC | local |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary.to_dict(orient="records"):
        lines.append(
            "| {substrate} | {class_count} | {class_a_survival:.4f} | {class_b_survival:.4f} | "
            "{m135_reconstruction_r2_k1:.4f} | {class_b_auc_latent1:.4f} | {class_b_auc_latent2:.4f} | "
            "{class_b_auc_latent3:.4f} | {controls_auc:.4f} | {local_classification} |".format(**row)
        )
    lines += [
        "",
        "## Required Questions",
        "",
        "1. Does the 17E pattern reproduce outside causal DAGs? See non-causal rows classified as `multi_axis`.",
        "2. Is causal/interventional structure required? It is not required if any non-causal substrate is `multi_axis`.",
        "3. Do non-causal finite systems show similar geometry? See S2/S3/S4 local decisions.",
        "4. Are M1/M3/M5 clustered? See `m135_reconstruction_r2_k1`.",
        "5. Is one axis enough to reconstruct metrics? Usually yes when R2 is high.",
        "6. Is one axis enough to predict perturbation survival? Compare latent1 vs latent2/latent3 AUC.",
        "7. Are controls sufficient? Compare controls AUC and local control-artifact decisions.",
        f"8. Best supported global hypothesis: `{decision['classification']}`.",
        "",
        "No claim is made that meaning or universal semantic geometry has been proven.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment 17F cross-substrate latent geometry")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-objects", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17F")
    args = parser.parse_args()
    out = ensure(args.outputs)

    substrates = {
        "S1_causal_dag": load_causal_dag_baseline(ROOT, args.seed),
        "S2_directed_graph": directed_graph_substrate(args.seed, args.num_objects, args.max_depth),
        "S3_term_rewrite": rewrite_substrate(args.seed, args.num_objects, args.max_depth),
        "S4_finite_automata": dfa_substrate(args.seed, args.num_objects, args.max_depth),
    }
    summaries = []
    for name, df in substrates.items():
        summaries.append(analyze_substrate(name, df, out, args.seed))
    summary = pd.DataFrame(summaries)
    ordered = [
        "substrate",
        "class_count",
        "class_a_survival",
        "class_b_survival",
        "m135_reconstruction_r2_k1",
        "class_b_auc_latent1",
        "class_b_auc_latent2",
        "class_b_auc_latent3",
        "controls_auc",
        "local_classification",
        "all_raw_auc",
        "pc1_control_variance_explained",
        "pc1_f1_explained_variance",
    ]
    summary = summary[[c for c in ordered if c in summary.columns]]
    summary.to_csv(out / "cross_substrate_summary.csv", index=False)
    decision = global_decision(summary)
    write_json(out / "cross_substrate_decision.json", decision)
    write_json(out / "final_decision.json", decision)
    write_comparison(out / "substrate_comparison.md", summary, decision)
    write_comparison(out / "final_report.md", summary, decision)
    (out / "implementation_notes.md").write_text(
        "# Implementation Notes\n\n"
        "S1 reuses the validated 17E causal-DAG feature matrix and attack labels. "
        "S2-S4 are independent bounded toy substrates with internally generated consequences, metric panels, and perturbation labels. "
        "Class A perturbations are representation-preserving by construction; Class B labels are generated from substrate-local robustness features, not from M1/M3/M5 directly. "
        "This is a falsification-oriented toy cross-substrate test, not evidence of real-world semantics.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "classification": decision["classification"],
                "local_classifications": decision["local_classifications"],
                "outputs": str(out),
            },
            indent=2,
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()

