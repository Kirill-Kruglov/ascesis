#!/usr/bin/env python3
import json
import os
import sys
import urllib.request

prompt = sys.stdin.read()
base = os.environ.get("ASCESIS_LLAMA_SERVER_BASE", "http://127.0.0.1:18080")
mode = os.environ.get("ASCESIS_LLAMA_MODE", "chat")
if mode == "completion":
    url = os.environ.get("ASCESIS_LLAMA_SERVER_URL", base + "/completion")
    payload = {
        "prompt": prompt,
        "n_predict": int(os.environ.get("ASCESIS_N_PREDICT", "192")),
        "temperature": float(os.environ.get("ASCESIS_TEMPERATURE", "0.0")),
        "top_p": float(os.environ.get("ASCESIS_TOP_P", "1.0")),
        "top_k": int(os.environ.get("ASCESIS_TOP_K", "1")),
        "min_p": float(os.environ.get("ASCESIS_MIN_P", "0.0")),
        "seed": int(os.environ.get("ASCESIS_SEED", "42")),
        "cache_prompt": False,
    }
else:
    url = os.environ.get("ASCESIS_LLAMA_SERVER_URL", base + "/v1/chat/completions")
    payload = {
        "messages": [
            {"role": "system", "content": os.environ.get("ASCESIS_SYSTEM_PROMPT", "Answer the user's decision question directly. Do not continue the prompt, invent new scenarios, or add unrelated dilemmas. If the options are incomparable under the stated information, say 'incomparable' and briefly state why. If they are comparable, choose one and briefly state why.")},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": int(os.environ.get("ASCESIS_N_PREDICT", "192")),
        "temperature": float(os.environ.get("ASCESIS_TEMPERATURE", "0.0")),
        "top_p": float(os.environ.get("ASCESIS_TOP_P", "1.0")),
        "seed": int(os.environ.get("ASCESIS_SEED", "42")),
    }
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=int(os.environ.get("ASCESIS_TIMEOUT", "300"))) as resp:
        data = json.loads(resp.read().decode())
    if mode == "completion":
        print(data.get("content", "").strip())
    else:
        print(data.get("choices", [{}])[0].get("message", {}).get("content", "").strip())
except Exception as exc:
    print(f"BACKEND_ERROR: {exc}")
