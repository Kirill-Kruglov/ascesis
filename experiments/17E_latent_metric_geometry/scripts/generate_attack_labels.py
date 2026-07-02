#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXP17A2_SRC = ROOT.parents[0] / "17A.2_Semantic_Perturbation_Taxonomy" / "src"
EXP17A_SRC = ROOT.parents[0] / "17A_backbone_consequence" / "src"
EXP16_SRC = ROOT.parents[0] / "16_consequence_vs_feature" / "src"
sys.path.insert(0, str(EXP17A2_SRC))
sys.path.insert(0, str(EXP17A_SRC))
sys.path.insert(0, str(EXP16_SRC))

RUN17A2 = ROOT.parents[0] / "17A.2_Semantic_Perturbation_Taxonomy" / "scripts" / "run_semantic_taxonomy.py"
spec = importlib.util.spec_from_file_location("run_semantic_taxonomy", RUN17A2)
run17a2 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run17a2)  # type: ignore[union-attr]

CLASS_A = {"P4_alpha_rename", "P9_split_node", "P10_replace_subgraph"}
CLASS_B = set(run17a2.ALL_OPS) - CLASS_A


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate optional per-class perturbation labels for experiment 17E")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-dags", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--exprs-per-dag-depth", type=int, default=80)
    parser.add_argument("--max-analyzed-classes", type=int, default=1200)
    parser.add_argument("--pairs-per-class", type=int, default=2)
    parser.add_argument("--cross-pairs-per-class", type=int, default=2)
    parser.add_argument("--max-attack-budget", type=int, default=4)
    parser.add_argument("--candidate-budget", type=int, default=80)
    parser.add_argument("--beam-width", type=int, default=8)
    parser.add_argument("--outputs", type=Path, default=ROOT / "outputs_17E" / "attack_labels.csv")
    args = parser.parse_args()

    args.outputs.parent.mkdir(parents=True, exist_ok=True)
    records = run17a2.build_records(args.seed, args.num_dags, args.max_depth, args.exprs_per_dag_depth)
    attack_args = SimpleNamespace(**vars(args))
    _, class_a = run17a2.analyze(records, CLASS_A, attack_args, "17E_class_A")
    _, class_b = run17a2.analyze(records, CLASS_B, attack_args, "17E_class_B")

    a = class_a[["class_id", "broken"]].rename(columns={"broken": "class_a_broken"})
    b = class_b[["class_id", "broken", "attack_cost", "auc_gns"]].rename(
        columns={"broken": "class_b_broken", "attack_cost": "class_b_attack_cost", "auc_gns": "class_b_auc_gns"}
    )
    labels = a.merge(b, on="class_id", how="outer")
    labels["class_a_survives"] = ~labels["class_a_broken"].fillna(False).astype(bool)
    labels["class_b_survives"] = ~labels["class_b_broken"].fillna(False).astype(bool)
    labels = labels.drop(columns=["class_a_broken", "class_b_broken"])
    labels.to_csv(args.outputs, index=False)
    print(
        {
            "labels_written": str(args.outputs),
            "rows": int(len(labels)),
            "class_b_survival_rate": float(labels["class_b_survives"].mean()) if len(labels) else None,
        },
        flush=True,
    )


if __name__ == "__main__":
    main()

