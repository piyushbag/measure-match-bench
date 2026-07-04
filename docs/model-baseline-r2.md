# R2 LLM baseline — Qwen2.5-3B-Instruct

**Chosen:** 2026-07-04  
**Policy:** local/open-weight only (no API keys in harness)

## Model

| Field | Value |
|-------|-------|
| Model | [Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) |
| Params | 3B |
| License | Qwen license (research + commercial terms on HF card) |
| Runtime | `transformers` + `torch`; optional `llama.cpp` GGUF for CPU-only |

## Why this model (vs Llama-3.2-3B, Phi-3-mini)

1. **Structured extraction** — strong on short JSON/key-value outputs for T1 alias resolution and T2 normalize.  
2. **Efficiency** — fits consumer GPU (8 GB) or CPU GGUF for reproducible CI.  
3. **Benchmark precedent** — common in 2024–2025 open-weight evals; easy for reviewers to replicate.  
4. **Task fit** — entity matching and retrieval over short strings, not long codegen (VERT/CVDP use larger coder models).

## Harness integration (planned v0.1.0)

```
R0  rules + fuzzy string match
R1  sentence-transformers (e.g. all-MiniLM-L6-v2) + heuristic parsers
R2  Qwen2.5-3B-Instruct, zero-shot prompts per task (T1–T4)
R3  optional LangGraph agent (post v1.0.0)
```

Pin in `eval/requirements-r2.txt`:

- `transformers>=4.44`
- `torch>=2.2`
- `accelerate`
- Model revision pinned in `eval/config/r2_model.json`

## Reproducibility notes

- Record `model_revision` (HF commit hash) in every `eval/results/*.json`.  
- Default inference: `temperature=0`, `max_new_tokens=256`.  
- Document GPU/CPU and wall time in paper §VI.
