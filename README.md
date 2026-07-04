# MeasureMatch-Bench

Open research artifact for **LLM entity resolution and retrieval over unstructured hardware validation measurement corpora**: align inconsistent product identifiers, normalize heterogeneous instrument exports, and answer scenario-targeted queries across power, thermal, fan, and throughput measurements.

**Author:** Piyush Jagadish Bag · Independent Researcher · ECAD validation and test automation · [piyushbag.com](https://piyushbag.com)

## Problem

Hardware validation teams accumulate thousands of unstructured measurement files across hundreds of product SKUs. Product IDs appear under inconsistent aliases in filenames, headers, and folder paths. Engineers spend days manually searching shared drives to answer questions like "what was the wall power at line rate for SKU X?"

**Why it matters:** AI-for-test and LLM validation papers focus on RTL, assertions, or inference power — not **measurement corpus alignment**. See [`docs/why-measure-match-bench.md`](docs/why-measure-match-bench.md) for the full gap statement and venue landscape.

## This repo

| Path | Purpose |
|------|---------|
| [`paper/`](paper/) | LaTeX source, venue matrix, endorsement |
| [`benchmarks/measure-match-bench/`](benchmarks/measure-match-bench/) | Synthetic corpus + gold labels |
| [`eval/`](eval/) | Reproducible harness + baseline pipelines |
| [`dist/`](dist/) | Release tarballs |
| [`evidence/`](evidence/) | Publication trail (private tracking OK) |

## Paper

**Title:** MeasureMatch-Bench: LLM Entity Resolution and Retrieval over Unstructured Hardware Measurement Corpora

- **Overleaf:** see [`paper/overleaf.md`](paper/overleaf.md)
- **LaTeX:** [`paper/latex/`](paper/latex/) (scaffold)

## Status

| Milestone | Status |
|-----------|--------|
| Intake + wedge | Done (2026-07-03) |
| Benchmark spec | Draft |
| Synthetic corpus generator | Planned |
| Eval harness | Scaffold |
| Zenodo DOI | Planned |
| arXiv preprint | Not submitted |

## Citation

```bibtex
@misc{bag2026measurematch,
  title={MeasureMatch-Bench: LLM Entity Resolution and Retrieval over Unstructured Hardware Measurement Corpora},
  author={Bag, Piyush Jagadish},
  year={2026},
  note={Independent Researcher. Preprint forthcoming.}
}
```

## License

Apache-2.0 (code) · Paper text CC BY 4.0
