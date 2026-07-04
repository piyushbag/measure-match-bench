# Literature review seed — MeasureMatch-Bench (2026-07-03)

## Direct neighbors (same failure mode: messy validation data + AI)

| Paper | arXiv | Task | Data | Gap vs us |
|-------|-------|------|------|-----------|
| De Santis et al. | 2408.01700 | LLM+KG extract/validate test docs | Aerospace boards | Case study, not benchmark |
| IEA-Plugin | 2504.11496 | Agent front-end for test analytics | Industrial backend | No public corpus |
| HiRMed (medical) | 2501.02727 | RAG tree retrieval | Medical tests | Wrong domain; method reference |

## Entity matching (methods, not HW domain)

| Paper | arXiv | Notes |
|-------|-------|-------|
| AnyMatch | 2409.04073 | Zero-shot EM; throughput vs GPT-class |

## Power measurement (different problem)

| Paper | arXiv | Notes |
|-------|-------|-------|
| TokenPowerBench | 2512.03024 | LLM **inference** joules/token |
| CARAML / jpwr | 2409.12994 | ML training energy on accelerators |

## Differentiation thesis

MeasureMatch-Bench is the first **open** benchmark for:
1. Product alias resolution at validation-archive scale
2. Multi-format measurement ingest → unified schema
3. Scenario-conditioned retrieval (46 synthetic scenario types)
4. Cross-corpus QA with citation to source files

Not: chip power modeling, LLM inference energy, or ECAD log triage.

## Next: verify IDs + download 8+ related works for §III table
