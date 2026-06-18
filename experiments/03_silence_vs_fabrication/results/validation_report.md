# Validation Report: 03 Silence vs Fabrication

## Measures
Does a ready-made LLM fabricate rankings on incommensurable dilemmas and remain stable under pressure? Links: `questions.md` Active Spine Questions and Bet-Hedging Challenge.

Model: `Llama-3.3-70B-Instruct-Q4_K_M.gguf`

Runtime: `llama.cpp Vulkan /v1/chat/completions`

## Artifact Checks

| check | result | interpretation |
|---|---|---|
| real_backend | passed | `heuristic_smoke` is not data; publication-grade run needs `ASCESIS_LLM_CMD`. |
| control_forced_ranking | passed | Comparable controls should rank; otherwise the probe/classifier is broken. |
| test_group_interpretation | passed | High test forced-ranking would be a finding about silence instability, not by itself a bug. |

## Raw And Human-Readable Outputs

- Raw: `results/raw/results.json`, `results/raw/results.csv`
- Human-readable: `results/report.md`, `results/fabrication_rates.svg`

## Verdict

valid result. Publication-grade status: publishable only if `real_backend` and `control_forced_ranking` pass and model/backend metadata are recorded.

## Interpretation Limitation

This test should not be read as "LLMs cannot stay silent" in general. It tests a narrower behavior: an instruction-following model prioritizes obedience to forced-choice framing over preserving incomparability under pressure. The protocol is therefore a pressure/obedience probe, not a direct measurement of a trained non-scalar agent.
