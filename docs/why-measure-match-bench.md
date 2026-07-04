# Why MeasureMatch-Bench?

Public significance statement for GitHub, Zenodo, and endorsement outreach.  
Modeled on strong benchmark papers (VERT, CVDP, Koios): **quantified problem → named gap → three contributions → open artifacts → who benefits**.

---

## 1. Problem (quantified)

Post-silicon validation teams collect instrument exports across many products and test scenarios. In production-scale programs, corpora reach **thousands of files** and **hundreds to thousands of product identifiers**, often with:

- inconsistent aliases in filenames, headers, and paths  
- heterogeneous formats (CSV, plain text, ad hoc key=value blocks)  
- scenario-specific folder conventions (power, thermal, fan, throughput)

Retrieving one validated metric slice (e.g., wall power at line rate for a given SKU) can take **days of manual search** across shared drives and email threads. Dashboards and analytics pipelines fail silently when entity alignment is wrong.

This is a **data integration and retrieval** problem at validation scale, not a missing instrument problem.

---

## 2. What exists today (and why it is insufficient)

| Area | Representative work | Limitation |
|------|---------------------|------------|
| LLM inference power | TokenPowerBench | Measures GPU/node power during inference, not lab validation archives |
| HDL / verification LLM benchmarks | CVDP, FIXME, VERT | RTL, assertions, testbenches — not measurement file corpora |
| Aerospace test documents | De Santis et al. (LLM + KG) | Single-domain case study; no public multi-task harness |
| Test analytics agents | IEA-Plugin | Industrial agent front-end; no reproducible public corpus |
| Entity matching (general) | AnyMatch, MatchGPT | Product/table matching — not hardware validation alias chaos |

**Gap:** There is no public benchmark that evaluates **product identity resolution**, **format normalization**, **scenario-targeted retrieval**, and **cross-corpus QA** over synthetic hardware validation measurement archives at ~6k-file scale.

---

## 3. Contributions (benchmark-first)

1. **MeasureMatch-Bench corpus** — 24 synthetic corpora, ~6,000 files, **46 scenario types** (PSU, thermal, fan, throughput, environmental), with gold labels for T1–T4.  
2. **Reproducible harness** — rule (R0), embedding (R1), and **open-weight LLM** (R2) pipelines; optional agent baseline (R3). Local-only models for reproducibility.  
3. **Empirical study** — head-to-head comparison showing where semantic LLM matching beats classical string/embedding baselines on alias-heavy validation identifiers (numbers only after harness run on release tarball).

---

## 4. Who benefits

| Audience | Benefit |
|----------|---------|
| Validation engineers | Shared task definitions for "find the right file" automation |
| ML / IR researchers | Realistic alias noise + scenario conditioning absent from Wiki-style EM datasets |
| Tool vendors | Neutral benchmark for RAG/entity products without proprietary customer data |
| Conference reviewers | Reproducible artifact path (GitHub tag + Zenodo DOI + harness semver) |

---

## 5. Why this matters now

- **AI-for-test** is an explicit CFP track at ITC (Track B) and a recurring DATE theme.  
- **LLM + validation data** papers are appearing (2024–2026), but mostly as case studies or HDL tasks.  
- **FAIR benchmarks** win citations when they enable comparisons (see VERT on OpenTitan/CVA6, CVDP on 783 RTL tasks).

MeasureMatch-Bench fills the missing **measurement corpus** slot in that landscape.

---

## 6. Open artifacts (no "pending")

| Artifact | Location |
|----------|----------|
| Corpus + gold labels | `benchmarks/measure-match-bench/` |
| Harness | `eval/run_eval.py` |
| Release tarball | `dist/measure-match-bench-v1.0.0.tar.gz` |
| DOI | Zenodo (mint at v1.0.0) |
| Paper | arXiv after endorsement; IEEEtran source in `paper/latex/` |

---

## 7. Honest limitations

- **Synthetic only** — patterns are plausible, not proprietary exports.  
- **No claim** of production deployment metrics in public text.  
- **Scenario taxonomy** is representative, not exhaustive of every lab instrument vendor format.

---

## 8. Citation

```bibtex
@misc{bag2026measurematch,
  title={MeasureMatch-Bench: LLM Entity Resolution and Retrieval over Unstructured Hardware Measurement Corpora},
  author={Bag, Piyush Jagadish},
  year={2026},
  howpublished={GitHub release + arXiv preprint forthcoming}
}
```

---

*Last updated: 2026-07-03*
