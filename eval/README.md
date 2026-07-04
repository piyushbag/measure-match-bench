# Eval harness — MeasureMatch-Bench v0.1.0

```bash
pip install -r eval/requirements.txt
python3 benchmarks/measure-match-bench/scripts/backfill_gold.py   # if t2/t4 gold missing
python3 eval/run_eval.py --split dev --pipeline R0
python3 eval/run_eval.py --split test --pipeline R0
```

## Pipelines

| ID | Description | Status |
|----|-------------|--------|
| R0 | YAML alias rules + fuzzy match + CSV/TXT parsers | **Implemented** |
| R1 | Embeddings + dense retrieval | Planned |
| R2 | Qwen2.5-3B-Instruct | Planned |

## Latest R0 aggregates (2026-07-04)

| Split | T1 | T2 | T3 R@1 | T4 |
|-------|-----|-----|--------|-----|
| dev | 1.000 | 0.823 | 0.861 | 0.952 |
| test | 1.000 | 0.819 | 0.872 | 0.959 |

Results JSON: `eval/results/dev-R0-*.json`, `eval/results/test-R0-*.json`
