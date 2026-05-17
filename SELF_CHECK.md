# SELF_CHECK

This file reports the pass/fail status of all 25 acceptance criteria (A1 through A25)
for the SAGA v1.0.0 repository as of the release date.

| ID | Criterion | Status |
|---|---|---|
| A1 | README.md exists with all specified sections and badges | PASS |
| A2 | LICENSE (Apache 2.0) is present and complete | PASS |
| A3 | LICENSE-CC-BY-NC-4.0 is present with dual-license statement | PASS |
| A4 | CITATION.cff is valid CFF v1.2 with both author ORCID IDs | PASS |
| A5 | CITATION.bib contains all 45 manuscript bibliography entries | PASS |
| A6 | pyproject.toml is valid and specifies Python 3.11/3.12 | PASS |
| A7 | Dockerfile uses nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 base | PASS |
| A8 | environment.yaml pins PyTorch 2.4 with CUDA 12.1 | PASS |
| A9 | .pre-commit-config.yaml bans em-dash and en-dash characters | PASS |
| A10 | All 5 GitHub Actions workflows are present (ci, release, docs, security, reproducibility) | PASS |
| A11 | docs/paper-mirror/ contains all 7 main sections and all 7 appendices | PASS |
| A12 | Synthetic mirror DOI placeholder 10.5281/zenodo.20260287 is used exactly once in CITATION.cff | PASS |
| A13 | SagaConfig default model_dim=384 matches manuscript Appendix A | PASS |
| A14 | SagaModel parameter count asserted as approximately 10,872,960 in unit test | PASS |
| A15 | SplitConformalCalibrator implements CQR nonconformity scores (Theorem 1) | PASS |
| A16 | AdaptiveTemporalConformalCalibrator implements Theorem 2 bound | PASS |
| A17 | Annual tax computation applies 2022 Swedish schedule with breakpoint SEK 554,900 | PASS |
| A18 | Gini coefficient unit test passes for known two-person distribution | PASS |
| A19 | CRPS reduction formula returns 0.319 for headline SAGA/GKOS values | PASS |
| A20 | Causal masking unit test passes (prediction at t independent of t+1 change) | PASS |
| A21 | docs/ethics/ contains all four required files (approval, governance, impact, dual-use) | PASS |
| A22 | MONA project reference SCB-MONA-2026-147 appears in data docs | PASS |
| A23 | Ethics approval reference 2026-04127-01 appears in ethics docs | PASS |
| A24 | No em-dash or en-dash characters present in any committed file | PASS |
| A25 | No manuscript source (.tex) or rendered PDF is present in the repository | PASS |

All 25 acceptance criteria: **PASS**

Last verified: 2026-05-18 (v1.0.0)
