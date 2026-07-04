# Venue matrix — MeasureMatch-Bench (10+ targets)

Research pass: 2026-07-03 (from scratch).  
Paper wedge: **LLM entity resolution + retrieval over unstructured hardware validation measurement corpora** (not chip-level DPT, not LLM inference power).

**Strategy (confirmed 2026-07-04):** artifact-first → arXiv → **ITC 2027 Track B** primary conference → **DATE 2027** backup.

---

## Conferences (6)

| # | Venue | Track / angle | Fit | Deadline (next cycle) | Framing |
|---|-------|---------------|-----|------------------------|---------|
| 1 | **IEEE ITC 2027** | Track B: AI for Test Efficiency & Innovation; data-driven test analytics | **5/5** | ~Mar 2027 (est.; ITC 2026 closed Apr 2026) | Direct CFP language on LLM test automation + analytics |
| 2 | **DATE 2027** | Test, dependability, embedded analytics, ML for design | **4/5** | Reg Sep 13, paper Sep 20, 2026 AoE | European archival; validation data-plane angle |
| 3 | **IEEE VTS 2027** | Power and thermal issues in test; ML for test; post-silicon validation | **4/5** | ~Nov 2026 (est.; VTS 2026 was Apr 2026) | Thermal/power **measurement in validation**, not DPT fixture papers |
| 4 | **DesignCon 2027** | Track 12: Applying Test & Measurement Methodology; Track 14: ML & AI | **4/5** | **Likely closed** Jun 23–30, 2026 (verify for 2028) | Practitioner audience; measurement methodology + AI |
| 5 | **VALID 2027** | "Testing semantic matching"; big datasets validation; hardware testing | **4/5** | ~Apr 2027 (est.; VALID 2026 Sep 2026 Barcelona) | Explicit semantic-matching track language |
| 6 | **IEEE ITC India 2027** | Theme: intelligent silicon / AI in testing | **3/5** | ~Mar 2027 (est.) | Regional visibility; same ITC family |

---

## Journals (5)

| # | Venue | Type | Fit | Cycle | Framing |
|---|-------|------|-----|-------|---------|
| 7 | **Journal of Electronic Testing (JETTA)** | Springer, peer-reviewed | **5/5** | Rolling | Only journal dedicated to electronic testing; data-driven analytics fits |
| 8 | **IEEE Design & Test (D&T)** | IEEE magazine + peer-reviewed articles | **4/5** | Rolling | Industry-facing validation/test automation audience |
| 9 | **ACM TODAES** | Journal | **4/5** | Rolling | Precedent: VERT assertion dataset (2025); benchmark + open dataset |
| 10 | **MDPI Electronics** | OA journal | **3/5** | Rolling | ML test automation case studies (e.g. universal automated testing system) |
| 11 | **MDPI Hardware** | OA, instrumentation focus | **3/5** | Rolling | If paper emphasizes measurement corpus + FAIR artifact over LLM novelty |

**Journal fallback if conference rejects:** JETTA extended version with full ablation appendix.

---

## Trade magazines & practitioner outlets (4)

Not peer-reviewed, but useful for **significance**, **community visibility**, and **endorsement social proof**.

| # | Outlet | Fit | Use |
|---|--------|-----|-----|
| 12 | **EE Times / EE Times Asia** | 4/5 | Practitioner essay: "Why validation teams need measurement corpus benchmarks" |
| 13 | **Electronic Design** | 4/5 | Test/measurement methodology column after arXiv |
| 14 | **Power Electronics News** | 3/5 | Power/thermal measurement angle (position carefully vs DPT/WBG papers) |
| 15 | **Design News** (DesignCon) | 3/5 | Conference recap or benchmark launch note |

---

## Ranked submission order

1. GitHub `v1.0.0` + Zenodo DOI + green harness  
2. arXiv (cs.AR primary; cs.SE + cs.DB cross-list)  
3. **ITC 2027 Track B** full paper  
4. **DATE 2027** if timeline slips or ITC feedback suggests systems angle  
5. **JETTA** journal extension (6–12 months post-arXiv)

## Deadlines watchlist

| Date | Action |
|------|--------|
| Sep 13–20, 2026 | DATE 2027 registration + paper (backup path) |
| Jun 2026 | DesignCon 2027 CFP — **may have just closed**; monitor DesignCon 2028 |
| ~Mar 2027 | ITC 2027 abstract (primary) |
| ~Nov 2026 | VTS 2027 CFP (optional third venue) |

## Differentiation reminder (venue pitch)

| Neighbor | Why we are not them |
|----------|---------------------|
| TokenPowerBench | LLM **inference** energy, not lab measurement archives |
| CVDP / FIXME / VERT | RTL/verification HDL, not post-silicon measurement files |
| De Santis 2408.01700 | Aerospace case study, not open multi-task benchmark |
| IEA-Plugin 2504.11496 | Agent UI for analytics, no public corpus |

---

## Research loop status

**Target:** ≥10 relevant venues — **met (15 listed).**  
Next loop tick: verify ITC 2027 CFP dates when posted; add EDFAS if failure-analysis data angle strengthens.
