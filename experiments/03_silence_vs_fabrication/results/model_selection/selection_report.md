# Model Selection Report

Backend: llama.cpp Vulkan server, `/v1/chat/completions` endpoint. ROCm server path was unavailable because required ROCm 7 shared libraries were missing.

| model | status | test forced-ranking | control forced-ranking | score | mean latency s |
|---|---|---:|---:|---:|---:|
| Llama-3.2-3B-Instruct-Q4_K_M.gguf | ok | 0.3333333333333333 | 0.6666666666666666 | 0.3333333333333333 | 0.5451221863428751 |
| Qwen3-32B-Q4_K_M.gguf | ok | 0.0 | 0.16666666666666666 | 0.16666666666666666 | 15.7475572625796 |
| Llama-3.3-70B-Instruct-Q4_K_M.gguf | ok | 0.3333333333333333 | 1.0 | 0.6666666666666667 | 8.883862654368082 |

Selected for full run: `Llama-3.3-70B-Instruct-Q4_K_M.gguf`.
