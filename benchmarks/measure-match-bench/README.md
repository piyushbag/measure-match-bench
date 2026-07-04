# MeasureMatch-Bench

Benchmark for **semantic alignment and retrieval** over heterogeneous hardware validation measurement archives (paper §IV).

## Tasks

| Task | Name | Input | Output | Baselines |
|------|------|-------|--------|-----------|
| **T1** | Product identity resolution | Alias string + candidate catalog | Canonical product ID | Rules, fuzzy match, embedding, LLM |
| **T2** | Format detection + normalize | Raw file bytes / path | Unified schema record | Rule parsers, LLM extraction |
| **T3** | Scenario-targeted retrieval | Product + scenario + metric | File path + value slice | BM25, dense retrieval, RAG |
| **T4** | Cross-scenario QA | Natural-language query over corpus | Structured answer + citations | RAG, agent pipeline |

## Scenario taxonomy (v1 target: 46 types)

Synthetic labels only. Categories mirror production breadth without proprietary schemas:

- **PSU:** wall power, internal rail power, efficiency curves
- **Thermal:** inlet/outlet delta, hotspot sensors, ambient sweep
- **Fan:** RPM setpoints, CFM vs PWM, acoustic proxy
- **Throughput:** line rate, packet size sweep, buffer occupancy
- **Environmental:** altitude/temp chamber metadata (optional v1.1)

## Layout (planned)

```
schema/measurement_record.json   # unified normalized record
rules/alias_patterns.yaml        # T1 rule baseline
splits/dev.txt                   # corpus-001 .. corpus-004
splits/test.txt                  # corpus-005 .. corpus-012
scripts/generate_corpus.py       # synthetic generator
instances/<id>/
  raw/                           # heterogeneous txt/csv exports
  catalog/products.json          # canonical IDs + alias pool
  gold/t1_identity.jsonl
  gold/t2_normalized.jsonl
  gold/t3_retrieval.jsonl
  gold/t4_qa.jsonl
```

## Corpus v1.0 target

| Split | Corpora | Files / corpus | Products | Alias rate |
|-------|---------|----------------|----------|------------|
| dev   | 4       | 200–400        | 40–80    | high       |
| test  | 8       | 200–400        | 40–80    | high + OOV |

Instance count target: **12 corpora** (aligned with HW-Triage-Bench scale for comparability in private planning only; public repos are standalone).

## Eval harness

```bash
python eval/run_eval.py --split dev --pipeline R0
python eval/run_eval.py --split test --pipeline R1
```

Pipelines (planned):

- **R0** Rules + fuzzy string match
- **R1** Embedding retrieval + heuristic parsers
- **R2** LLM semantic matching + RAG
- **R3** Agentic multi-step (optional)

## Release checklist

- [x] 24 synthetic corpora (~6,000 measurement files + gold labels)
- [ ] JSON schema + alias rule baseline (`rules/alias_patterns.yaml`)
- [ ] Harness v0.1.0 with R0/R1/R2
- [ ] `dist/measure-match-bench-v1.0.0.tar.gz`
- [ ] Zenodo DOI
