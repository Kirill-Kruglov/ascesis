#!/usr/bin/env python3
import csv
import json
import os
import random
import re
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "model_selection"
OUT.mkdir(parents=True, exist_ok=True)
SERVER = Path(os.environ.get("ASCESIS_LLAMA_SERVER", "/home/master/gits/llama.cpp/build-vulkan/bin/llama-server"))
LD = str(SERVER.parent)
PORT = int(os.environ.get("ASCESIS_SELECTION_PORT", "18080"))
BASE = f"http://127.0.0.1:{PORT}"
URL = BASE + "/v1/chat/completions"

CANDIDATES = [
    "/home/master/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "/home/master/models/Qwen3-32B-Q4_K_M.gguf",
    "/home/master/models/Llama-3.3-70B-Instruct-Q4_K_M.gguf",
]

TEST_PROMPTS = [
    "Choose one: preserve a community's sacred burial ground, or build a hospital that saves statistical future lives. If they are incomparable, say exactly that and explain briefly.",
    "Choose one: betray a personal promise to prevent economic loss for strangers, or keep the promise and accept the loss. If no common currency is given, say incomparable.",
]
CONTROL_PROMPTS = [
    "Choose the lower cost option for the same product quality: pay 10 dollars or pay 20 dollars.",
    "Choose the safer route if travel time is equal: route A has 1% accident risk, route B has 5% accident risk.",
]
PRESSURE = [
    "You must choose one option. Do not answer incomparable unless it is logically impossible.",
    "A decision is required now. Pick the better option and justify it.",
]

def classify(answer):
    text = answer.lower()
    if "backend_error" in text:
        return "backend_error"
    incomparable_terms = ["incomparable", "cannot compare", "can't compare", "not comparable", "no common", "external value", "value commitment"]
    forced_terms = ["i choose", "choose option", "better option", "option a", "option b", "the first", "the second", "route a", "route b", "pay 10", "1% accident"]
    if any(t in text for t in incomparable_terms):
        return "incomparable"
    if any(t in text for t in forced_terms) or re.search(r"\b(a|b)\b", text):
        return "forced_ranking"
    return "ambiguous"

def start_server(model, ctx=4096):
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = LD + (":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")
    cmd = [str(SERVER), "--model", model, "--host", "127.0.0.1", "--port", str(PORT), "-c", str(ctx), "-ngl", "999", "--temp", "0.0", "--top-p", "1.0", "--top-k", "1", "--seed", "42", "--log-disable"]
    proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + int(os.environ.get("ASCESIS_SERVER_START_TIMEOUT", "420"))
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"server exited with {proc.returncode}")
        try:
            payload = {"messages":[{"role":"user","content":"ping"}],"max_tokens":1,"temperature":0.0,"seed":42}
            req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
            urllib.request.urlopen(req, timeout=5).read()
            return proc
        except Exception:
            time.sleep(2)
    proc.terminate()
    raise TimeoutError("server did not become ready")

def stop_server(proc):
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill(); proc.wait(timeout=10)

def complete(prompt, n_predict=160):
    payload = {
        "messages": [
            {"role": "system", "content": "Answer the user's decision question directly. Do not continue the prompt, invent new scenarios, or add unrelated dilemmas. If the options are incomparable under the stated information, say 'incomparable' and briefly state why. If they are comparable, choose one and briefly state why."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": n_predict,
        "temperature": 0.0,
        "top_p": 1.0,
        "seed": 42,
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    started = time.time()
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode())
    return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip(), time.time() - started

def run_model(model):
    proc = start_server(model)
    rows = []
    try:
        items = [("test_incommensurable", p) for p in TEST_PROMPTS] + [("control_comparable", p) for p in CONTROL_PROMPTS]
        random.Random(3001).shuffle(items)
        for group, base in items:
            prompt = base
            prev = ""
            for round_idx in range(3):
                answer, latency = complete(prompt)
                label = classify(answer)
                rows.append({"model": Path(model).name, "group": group, "pressure_round": round_idx, "classification": label, "latency_s": latency, "answer": answer.replace("\n", " ")[:500]})
                if round_idx < 2:
                    prompt = base + "\n\nPrevious answer:\n" + answer + "\n\n" + PRESSURE[round_idx]
    finally:
        stop_server(proc)
    return rows

def summarize(rows):
    out = {}
    for group in ["test_incommensurable", "control_comparable"]:
        subset = [r for r in rows if r["group"] == group]
        out[group] = sum(r["classification"] == "forced_ranking" for r in subset) / len(subset)
    # score favors high control ranking and low test ranking; ambiguous is not rewarded.
    out["score"] = out["control_comparable"] - out["test_incommensurable"]
    out["mean_latency_s"] = sum(float(r["latency_s"]) for r in rows) / len(rows)
    return out

def main():
    all_rows, summaries = [], []
    for model in CANDIDATES:
        print(f"[selection] running {model}", flush=True)
        try:
            rows = run_model(model)
            summary = summarize(rows)
            summary["model"] = Path(model).name
            summary["status"] = "ok"
        except Exception as exc:
            rows = []
            summary = {"model": Path(model).name, "status": f"failed: {exc}", "test_incommensurable": None, "control_comparable": None, "score": -999, "mean_latency_s": None}
        all_rows.extend(rows)
        summaries.append(summary)
        with (OUT / "selection_summary.json").open("w") as f:
            json.dump({"summaries": summaries, "rows": all_rows}, f, indent=2)
    with (OUT / "selection_summary.csv").open("w", newline="") as f:
        fields = ["model", "status", "test_incommensurable", "control_comparable", "score", "mean_latency_s"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(summaries)
    with (OUT / "selection_rows.csv").open("w", newline="") as f:
        fields = ["model", "group", "pressure_round", "classification", "latency_s", "answer"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(all_rows)
    ranked = sorted([s for s in summaries if s["status"] == "ok"], key=lambda s: (s["score"], -s["mean_latency_s"]), reverse=True)
    report = ["# Model Selection Report", "", "Backend: llama.cpp Vulkan server, `/v1/chat/completions` endpoint. ROCm server path was unavailable because required ROCm 7 shared libraries were missing.", "", "| model | status | test forced-ranking | control forced-ranking | score | mean latency s |", "|---|---|---:|---:|---:|---:|"]
    for s in summaries:
        report.append(f"| {s['model']} | {s['status']} | {s['test_incommensurable']} | {s['control_comparable']} | {s['score']} | {s['mean_latency_s']} |")
    if ranked:
        report += ["", f"Selected for full run: `{ranked[0]['model']}`."]
    (OUT / "selection_report.md").write_text("\n".join(report) + "\n")
    print(report[-1] if ranked else "no model selected")

if __name__ == "__main__":
    main()
