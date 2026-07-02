#!/usr/bin/env python3
from __future__ import annotations

import argparse, importlib.util, json, math, sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXP16_SRC = ROOT.parents[0] / "16_consequence_vs_feature" / "src"
EXP17A2_SRC = ROOT.parents[0] / "17A.2_Semantic_Perturbation_Taxonomy" / "src"
EXP17A_SRC = ROOT.parents[0] / "17A_backbone_consequence" / "src"
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(EXP16_SRC)); sys.path.insert(0, str(EXP17A2_SRC)); sys.path.insert(0, str(EXP17A_SRC))

from closure_metric_robustness.metrics import compute_metric_scores, select_top_fraction  # noqa: E402

RUN17A2 = ROOT.parents[0] / "17A.2_Semantic_Perturbation_Taxonomy" / "scripts" / "run_semantic_taxonomy.py"
spec = importlib.util.spec_from_file_location("run_semantic_taxonomy", RUN17A2)
run17a2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(run17a2)  # type: ignore
CLASS_A = {"P4_alpha_rename", "P9_split_node", "P10_replace_subgraph"}
CLASS_B = set(run17a2.ALL_OPS) - CLASS_A
REAL = ["M1_original", "M2_intervention", "M3_reuse", "M4_compression", "M5_perturbation_centrality"]
CONTROLS = ["M6_frequency_control", "M7_random_matched"]


def ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True); return path

def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

def records_for_keys(records, keys):
    return [r for r in records if r["consequence_key"] in keys]

def pearson(xs, ys):
    n=len(xs)
    if n<2: return None
    mx=sum(xs)/n; my=sum(ys)/n
    vx=sum((x-mx)**2 for x in xs); vy=sum((y-my)**2 for y in ys)
    if vx==0 or vy==0: return None
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/math.sqrt(vx*vy)

def ranks(vals):
    order=sorted(range(len(vals)), key=lambda i: vals[i])
    r=[0.0]*len(vals)
    for rank,i in enumerate(order): r[i]=rank
    return r

def spearman(a,b,keys):
    xs=[a[k] for k in keys]; ys=[b[k] for k in keys]
    return pearson(ranks(xs), ranks(ys))

def overlap_rows(active, scores):
    names=list(active)
    rows=[]
    all_keys=set().union(*active.values()) if active else set()
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            a,b=active[names[i]],active[names[j]]
            inter=len(a&b); union=len(a|b)
            rows.append({"metric_i":names[i],"metric_j":names[j],"jaccard":inter/union if union else 0,"overlap_coefficient":inter/min(len(a),len(b)) if min(len(a),len(b)) else 0,"spearman_rank_correlation":spearman(scores[names[i]],scores[names[j]],list(scores[names[i]].keys()))})
    return rows

def attack_metric(metric, active_keys, records, args):
    subset=records_for_keys(records, active_keys)
    a_sum,a_df=run17a2.analyze(subset, CLASS_A, args, f"{metric}_A")
    b_sum,b_df=run17a2.analyze(subset, CLASS_B, args, f"{metric}_B")
    return a_sum,b_sum,a_df,b_df

def summarize_decision(metric_summaries, active, dead_recheck):
    real_pairs=[]; control_pairs=[]
    # approximate from precomputed pairwise later in main; use summaries here
    m1=metric_summaries["M1_original"]
    real_b=[metric_summaries[m]["Class_B_surviving_fraction"] for m in REAL]
    ctrl_b=[metric_summaries[m]["Class_B_surviving_fraction"] for m in CONTROLS]
    real_similar=max(real_b)-min(real_b) < 0.20
    controls_reproduce=any(abs(c - m1["Class_B_surviving_fraction"]) < 0.05 for c in ctrl_b)
    dead_total=dead_recheck.get("dead_invariant_total",0)
    dead_still=dead_recheck.get("dead_invariant_remain_dead_majority",0)
    if controls_reproduce:
        cls="Frequency_artifact"; interp="Frequency/random controls reproduce the closure behavior too closely."
    elif real_similar and dead_still/max(1,dead_total) > 0.5:
        cls="Functional_core_supported"; interp="Independent internal metrics converge on a stable active core and controls do not reproduce the effect."
    elif not real_similar:
        cls="Metric_artifact"; interp="Active subsets or Class B behavior vary strongly across internal metrics."
    else:
        cls="Inconclusive"; interp="Metrics show partial convergence but not enough to separate controls/artifacts cleanly."
    return {"classification":cls,"interpretation":interp}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,default=42); ap.add_argument("--num-dags",type=int,default=500); ap.add_argument("--max-depth",type=int,default=6)
    ap.add_argument("--exprs-per-dag-depth",type=int,default=80); ap.add_argument("--max-analyzed-classes",type=int,default=450)
    ap.add_argument("--pairs-per-class",type=int,default=2); ap.add_argument("--cross-pairs-per-class",type=int,default=2); ap.add_argument("--max-attack-budget",type=int,default=4)
    ap.add_argument("--candidate-budget",type=int,default=50); ap.add_argument("--beam-width",type=int,default=8); ap.add_argument("--outputs",type=Path,default=ROOT/"outputs_17D")
    args=ap.parse_args(); out=ensure(args.outputs)
    records=run17a2.build_records(args.seed,args.num_dags,args.max_depth,args.exprs_per_dag_depth)
    features,scores=compute_metric_scores(records,args.seed)
    m1_fraction=0.40  # matched to 17C strong closure default quantile
    active={m:select_top_fraction(s,m1_fraction) for m,s in scores.items()}
    score_rows=[]; active_rows=[]
    for k,feat in features.items():
        cid=run17a2.stable_id(k)
        row={"class_id":cid, **feat}
        for m in scores: row[m]=scores[m][k]
        score_rows.append(row)
        for m in scores: active_rows.append({"class_id":cid,"metric":m,"active":k in active[m],"score":scores[m][k]})
    pd.DataFrame(score_rows).to_csv(out/"metric_scores.csv",index=False)
    pd.DataFrame(active_rows).to_csv(out/"metric_active_sets.csv",index=False)
    pairwise=pd.DataFrame(overlap_rows(active,scores)); pairwise.to_csv(out/"pairwise_overlap.csv",index=False); pairwise.to_csv(out/"rank_correlations.csv",index=False)
    metric_summaries={}; class_a_rows=[]; class_b_rows=[]
    attack_args=SimpleNamespace(**vars(args))
    for m in scores:
        a,b,adf,bdf=attack_metric(m,active[m],records,attack_args)
        metric_summaries[m]={"total_classes":len(features),"active_classes":len(active[m]),"active_fraction":len(active[m])/len(features),"mean_score":sum(scores[m].values())/len(scores[m]),"Class_A_surviving_fraction":a["surviving_fraction"],"Class_B_surviving_fraction":b["surviving_fraction"],"mean_auc_gns_Class_A":a["mean_auc_gns"],"mean_auc_gns_Class_B":b["mean_auc_gns"],"mean_attack_cost_broken":b.get("mean_attack_cost_broken")}
        class_a_rows.append({"metric":m,**a}); class_b_rows.append({"metric":m,**b})
    pd.DataFrame(class_a_rows).to_csv(out/"class_a_by_metric.csv",index=False); pd.DataFrame(class_b_rows).to_csv(out/"class_b_by_metric.csv",index=False)
    write_json(out/"metric_summaries.json",metric_summaries)
    real_counts={k:sum(1 for m in REAL if k in active[m]) for k in features}
    functional={k for k,c in real_counts.items() if c>=3}; strict={k for k,c in real_counts.items() if c>=4}
    def core_df(keys):
        return pd.DataFrame([{ "class_id":run17a2.stable_id(k),"selected_by":real_counts[k], **features[k]} for k in keys])
    core_df(functional).to_csv(out/"functional_core.csv",index=False); core_df(strict).to_csv(out/"strict_core.csv",index=False)
    core_summary={"functional_core_size":len(functional),"strict_core_size":len(strict),"total_classes":len(features),"functional_core_fraction":len(functional)/len(features),"strict_core_fraction":len(strict)/len(features)}
    write_json(out/"functional_core_summary.json",core_summary)
    # Dead invariant recheck from 17C if available
    dead_path=ROOT.parents[0]/"17C_interpretive_closure_test"/"outputs_17C"/"closure_dead_classes.csv"
    dead_rows=[]
    if dead_path.exists():
        dead_ids=set(pd.read_csv(dead_path)["class_id"])
        id_to_key={run17a2.stable_id(k):k for k in features}
        for cid in dead_ids:
            k=id_to_key.get(cid)
            if k is None: continue
            row={"class_id":cid}
            active_count=0
            for m in scores:
                is_active=k in active[m]; active_count+=int(is_active); row[f"{m}_active"]=is_active; row[f"{m}_score"]=scores[m][k]
            row["active_metric_count"]=active_count; dead_rows.append(row)
    dead_df=pd.DataFrame(dead_rows); dead_df.to_csv(out/"dead_invariant_recheck.csv",index=False)
    dead_summary={"dead_invariant_total":len(dead_rows),"dead_invariant_remain_dead_majority":int((dead_df.get("active_metric_count",pd.Series(dtype=int))<3).sum()) if len(dead_df) else 0}
    control={"M6_frequency_control":metric_summaries["M6_frequency_control"],"M7_random_matched":metric_summaries["M7_random_matched"],"real_metrics_mean_Class_B_survival":sum(metric_summaries[m]["Class_B_surviving_fraction"] for m in REAL)/len(REAL),"controls_mean_Class_B_survival":sum(metric_summaries[m]["Class_B_surviving_fraction"] for m in CONTROLS)/len(CONTROLS)}
    write_json(out/"control_comparison.json",control)
    decision={**summarize_decision(metric_summaries,active,dead_summary),"metric_summaries":metric_summaries,"functional_core_summary":core_summary,"dead_invariant_recheck":dead_summary,"control_comparison":control}
    write_json(out/"final_decision.json",decision)
    write_json(out/"failure_examples.json",{"m1_not_in_functional_core":[run17a2.stable_id(k) for k in list(active["M1_original"]-functional)[:20]],"dead_invariant_becomes_active":dead_df[dead_df.get("active_metric_count",0)>=3].head(20).to_dict(orient="records") if len(dead_df) else []})
    (out/"implementation_notes.md").write_text("# Implementation Notes\n\nAll metrics use only internally derived class features from the existing DAG/verifier substrate. M7 is a shuffled matched-size random control. Perturbation behavior reuses the 17A.2 Class A/Class B analyzer without changing operators or verifier.\n",encoding="utf-8")
    report=["# Experiment 17D - Closure Metric Robustness", "", f"## Final Decision\n\nClassification: `{decision['classification']}`.\n\n{decision['interpretation']}", "", "## Core Results", "", f"Functional core: {len(functional)} / {len(features)}", f"Strict core: {len(strict)} / {len(features)}", f"Dead invariant recheck: {dead_summary}", "", "## Metric Summaries", ""]
    for m,s in metric_summaries.items(): report.append(f"- {m}: active={s['active_classes']}, ClassA_survive={s['Class_A_surviving_fraction']:.4g}, ClassB_survive={s['Class_B_surviving_fraction']:.4g}")
    report += ["", "## Required Questions", "", "1. Does 17C active subset survive replacement? See pairwise_overlap.csv and functional_core.csv.", "2. Do metrics converge? Functional/strict core sizes above.", "3. Are closure-dead invariant classes still dead? See dead_invariant_recheck.csv.", "4. Controls? See control_comparison.json.", "5. Interpretation is in final_decision.json.", "6. Strongest counterexamples in failure_examples.json.", "7. Stable core evidence in functional_core.csv."]
    (out/"final_report.md").write_text("\n".join(report),encoding="utf-8")
    print(json.dumps({"classification":decision["classification"],"functional_core_size":len(functional),"strict_core_size":len(strict),"dead_recheck":dead_summary,"outputs":str(out)},indent=2),flush=True)
if __name__=="__main__": main()
