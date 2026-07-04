# Overleaf — MeasureMatch-Bench

## First draft ready (2026-07-04)

Upload these two files to a new **IEEE Conference Template** project:

| Local file | Overleaf upload name |
|------------|---------------------|
| `paper/latex/main.tex` | `main.tex` |
| `paper/latex/references.bib` | `references.bib` |

### Manual upload steps

1. Go to [overleaf.com](https://www.overleaf.com) → **New Project** → **Upload Project** (zip) **or** Blank IEEE template.
2. Delete default `main.tex` / `references.bib` if present.
3. Upload `paper/latex/main.tex` and `paper/latex/references.bib` from this repo.
4. Menu → Compiler: **pdfLaTeX**; run **Recompile**.
5. If `IEEEtran.cls` missing: use Overleaf's built-in IEEE template (includes class file).

### Endorsement brief (separate 2-page PDF)

| Local file | Notes |
|------------|-------|
| `paper/endorsement/arxiv-endorsement-brief.tex` | Upload as separate project or second doc; compile to PDF for email attachment |

### What is in draft v0.1

- Full abstract + Introduction + Related Work (differentiation table)
- Benchmark design (T1–T4, 46 scenarios, 24 corpora)
- **§VI Experiments with real R0 numbers** (dev + test splits)
- Discussion, Conclusion, Data Availability
- 8 references in `references.bib`

### Not yet in draft (expected v0.2)

- R1/R2 pipeline results (after implementation)
- Zenodo DOI (replace placeholder in Data Availability)
- Figure: corpus/schema diagram
- `\balance` may warn if refs short; add text or ignore for draft read

### Sync back

After Overleaf edits, download Source zip → merge into `paper/latex/` before GitHub release tag.
