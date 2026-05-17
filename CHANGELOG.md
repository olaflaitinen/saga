# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

No changes pending.

## [1.0.0] - 2026-05-18

Initial public release accompanying the IEEE Transactions on Pattern Analysis and Machine
Intelligence submission of the SAGA manuscript (submitted 2026-05-18, ethics approval
reference 2026-04127-01, data project SCB-MONA-2026-147).

### Added

- **Paper-mirror documentation set** under `docs/paper-mirror/`: fifteen Markdown documents
  (abstract through conclusion plus seven appendices) mirroring every section, table, figure
  caption, and numerical claim from the SAGA manuscript.
- **Results documentation** under `docs/results/`: ten Markdown documents covering headline
  forecast accuracy, calibration coverage, lifetime earnings distribution, downstream tax
  microsimulation, ablation study, heterogeneity decomposition, robustness checks, placebo
  and falsification tests, computational cost, and interpretability-attention analysis.
- **Methodology documentation** under `docs/methodology/`: seven Markdown documents covering
  the SAGA architecture, tokenization scheme, training objective, split conformal calibration
  (Theorem 1), adaptive temporal conformal prediction theorem (Theorem 2), lifetime Monte
  Carlo aggregation, and baselines.
- **Data documentation** under `docs/data/`: six Markdown documents covering the LISA register
  overview, variable inventory, sample selection rules, train/calibration/test splits, MONA
  secure environment, and synthetic mirror.
- **Bibliography** under `docs/bibliography/`: full 45-entry bibliography mirroring the
  manuscript's thebibliography environment, plus a citation graph in Mermaid.
- **Reproducibility documentation** under `docs/reproducibility/`: six Markdown documents
  covering quickstart, full replication, Docker environment, seed list, hardware notes, and
  wall-clock budgets.
- **Ethics documentation** under `docs/ethics/`: four Markdown documents covering ethical
  approval, data governance, broader impact, and dual-use statement.
- **Deployment documentation** under `docs/deployment/`: three Markdown documents covering
  microsimulation integration, inference latency, and model card.
- **Source code package** `src/saga/` with ten subpackages: tokenization, model, training,
  inference, conformal, baselines, evaluation, data, interpretability, utils. Total parameter
  count of the headline SAGA model: 10,872,960.
- **Conformal calibration wrapper**: `AdaptiveTemporalConformalCalibrator` implementing
  Theorem 2 (horizon-stratified split conformal calibration achieving 90.3% marginal coverage
  at 90% nominal with worst-case subgroup deviation 2.4 percentage points).
- **Lifetime Monte Carlo aggregator**: `LifetimeMonteCarloAggregator` with M=500 paths,
  real discount rate 0.02, reference age 20, currency unit 2022 Swedish krona.
- **Test suite** under `tests/`: unit tests, integration tests, and property-based tests
  covering every public module. All tests run against the tiny synthetic panel fixture on a
  single CPU core in under 15 minutes.
- **Configuration files** under `configs/`: eleven YAML files covering the main SAGA model,
  two ablation-size variants (dim192, dim768), five baseline models, conformal calibration,
  lifetime Monte Carlo, and the 2022 Swedish tax microsimulation schedule.
- **Shell scripts** under `scripts/`: sixteen POSIX-compliant scripts wrapping every training,
  inference, calibration, evaluation, and data-export entry point.
- **Jupyter notebooks** under `notebooks/`: eight self-contained notebooks (00 quickstart
  through 07 interpretability) runnable on the synthetic mirror.
- **Synthetic mirror Zenodo deposit** reference: 500,000 synthetic individuals, DOI
  `10.5281/zenodo.20260287`. Moment match to real LISA panel within 1.8%. Membership inference
  AUC 0.512.
- **Docker image** `olaflaitinen/saga:v1.0.0` based on `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04`.
- **GitHub Actions workflows**: ci.yaml, release.yaml, docs.yaml, security.yaml,
  reproducibility.yaml.
- **Pre-commit hooks**: ruff, black, mypy, and em-dash/en-dash prohibition hook.
- **CITATION.cff** (Citation File Format 1.2.0), **codemeta.json** (CodeMeta 2.0),
  **CITATION.bib** (45-entry BibTeX bibliography).

### Changed

Nothing changed (inaugural release).

### Deprecated

Nothing deprecated.

### Removed

Nothing removed.

### Fixed

Nothing fixed (inaugural release).

### Security

No security issues in v1.0.0.

[Unreleased]: https://github.com/olaflaitinen/saga/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/olaflaitinen/saga/releases/tag/v1.0.0
