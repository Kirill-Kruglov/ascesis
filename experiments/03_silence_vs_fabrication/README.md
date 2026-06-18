# 03_silence_vs_fabrication

No-training LLM probe for silence vs forced ranking.

Smoke run without an LLM:

```sh
python3 run.py
```

Publication-grade local LLM run:

```sh
ASCESIS_LLM_CMD='ollama run qwen2.5:72b-instruct-q4_K_M' python3 run.py
```

The command must read a prompt from stdin and return one answer on stdout. The default backend is marked `heuristic_smoke` and is only for pipeline testing.

Outputs:

- `results/raw/results.json`
- `results/raw/results.csv`
- `results/report.md`
- `results/fabrication_rates.svg`
- `results/run_manifest.json`

## Hard Rules

- Pre-registration: `SPEC.md` fixes hypothesis, metrics, environments, and win criteria before publication-grade runs. Commit the SPEC first; `run.py` records the git HEAD, dirty status, and SPEC hash in `results/run_manifest.json`.
- Held-out environments: tune only on train environments where a train/held-out split exists; declare winners only on held-out environments.
- Symmetry of effort: log improvement iterations for each side in `results/run_manifest.json`.
- Seeds and reproducibility: fixed seeds; reproduce with `python3 run.py` from this directory.
- Negative results publish: empty win lists and failed hypotheses are valid outputs.

## ROCm-Compatible Backends For Real Runs

The default `heuristic_smoke` backend is CI/pipeline only and is not publishable data. For a publication-grade run on AMD AI Max 395+ / 128GB unified memory, use a real open model through one of these ROCm-compatible paths:

- `llama.cpp` built with HIP/ROCm. Good for GGUF quantized 70B/72B-class models on a single large unified-memory host.
- `vLLM` ROCm wheels or ROCm Docker image. Good for OpenAI-compatible serving if the local ROCm stack and model architecture are supported.
- `transformers` on PyTorch ROCm. Good for smaller iteration models; verify `torch.cuda.is_available()` under ROCm before running.

Suggested publication-grade models: `Qwen2.5-72B-Instruct` quantized GGUF, `Llama-3.3-70B-Instruct` quantized GGUF. Suggested iteration models: `Qwen2.5-7B-Instruct`, `Llama-3.1-8B-Instruct`, `Mistral-7B-Instruct`.

Example command backend:

```sh
ASCESIS_LLM_CMD='/path/to/llama-cli -m /models/Qwen2.5-72B-Instruct-Q4_K_M.gguf -n 256 --temp 0.0 -p' python3 run.py
```

The exact model, quantization, backend, ROCm version, and command must be fixed before a publication-grade run and recorded in `results/run_manifest.json`.

