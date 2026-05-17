# SAGA: A Sequence-Adaptive Generative Architecture for Multi-Horizon Probabilistic Forecasting with Adaptive Temporal Conformal Prediction

[![arXiv preprint](https://img.shields.io/badge/arXiv-__TBD_ARXIV_ID__-b31b1b.svg)](https://arxiv.org/abs/__TBD_ARXIV_ID__) [![ORCID: Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov](https://img.shields.io/badge/ORCID-0009--0006--5184--0810-A6CE39.svg?logo=orcid)](https://orcid.org/0009-0006-5184-0810) [![ORCID: Hafize Gonca Comert](https://img.shields.io/badge/ORCID-0009--0009--3345--8783-A6CE39.svg?logo=orcid)](https://orcid.org/0009-0009-3345-8783)

[![Code license: Apache 2.0](https://img.shields.io/badge/code%20license-Apache--2.0-blue.svg)](./LICENSE) [![Documentation and data license: CC BY-NC 4.0](https://img.shields.io/badge/docs%20%26%20data%20license-CC%20BY--NC%204.0-lightgrey.svg)](./LICENSE-CC-BY-NC-4.0) [![Zenodo DOI 10.5281 / zenodo.20204066](https://zenodo.org/badge/DOI/10.5281/zenodo.20260287.svg)](https://doi.org/10.5281/zenodo.20260287) [![Continuous integration status](https://github.com/olaflaitinen/saga/actions/workflows/ci.yaml/badge.svg)](https://github.com/olaflaitinen/saga/actions/workflows/ci.yaml) [![Reproducibility workflow status](https://github.com/olaflaitinen/saga/actions/workflows/reproducibility.yaml/badge.svg)](https://github.com/olaflaitinen/saga/actions/workflows/reproducibility.yaml) [![Code coverage on main](https://codecov.io/gh/olaflaitinen/saga/branch/main/graph/badge.svg)](https://codecov.io/gh/olaflaitinen/saga) [![Python 3.11 or 3.12](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](./pyproject.toml) [![PyTorch 2.4 or newer](https://img.shields.io/badge/pytorch-2.4%2B-EE4C2C.svg)](https://pytorch.org) [![CUDA 12.1](https://img.shields.io/badge/CUDA-12.1-76B900.svg)](./docs/reproducibility/hardware-notes.md) [![Docker image latest tag](https://img.shields.io/docker/v/olaflaitinen/saga?label=docker)](https://hub.docker.com/r/olaflaitinen/saga)
[![Code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Linted with ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Type checked with mypy in strict mode](https://img.shields.io/badge/types-mypy%20strict-1F5082.svg)](https://mypy-lang.org) [![pre-commit hooks enabled](https://img.shields.io/badge/pre--commit-enabled-76d6ff.svg?logo=pre-commit)](https://pre-commit.com) [![Semantic versioning 2.0.0](https://img.shields.io/badge/semver-2.0.0-blue.svg)](https://semver.org) [![Last commit](https://img.shields.io/github/last-commit/olaflaitinen/saga)](https://github.com/olaflaitinen/saga/commits/main) [![GitHub stars](https://img.shields.io/github/stars/olaflaitinen/saga?style=social)](https://github.com/olaflaitinen/saga/stargazers) [![GitHub forks](https://img.shields.io/github/forks/olaflaitinen/saga?style=social)](https://github.com/olaflaitinen/saga/network/members) [![Open issues](https://img.shields.io/github/issues/olaflaitinen/saga)](https://github.com/olaflaitinen/saga/issues) [![Repository size](https://img.shields.io/github/repo-size/olaflaitinen/saga)](https://github.com/olaflaitinen/saga)

## Synopsis

SAGA is a sequence-adaptive generative transformer architecture for multi-horizon probabilistic forecasting of individual earnings trajectories in large administrative panel data. It was trained on 2,143,817 individuals drawn from the Swedish LISA register (longitudinell integrationsdatabas), spanning 61,284,903 person-year observations over the period 1990 to 2022. SAGA employs a typed-subvector tokenization scheme that projects continuous earnings features, categorical labor market indicators, missingness patterns, and positional embeddings into a unified 384-dimensional token representation, then passes these tokens through six causally-masked transformer decoder layers. Probabilistic forecasts are delivered through a 7-quantile pinball head and wrapped by a horizon-stratified split conformal calibration layer (Adaptive Temporal Conformal Prediction, Theorem 2) that achieves 90.3% marginal coverage at the 90% nominal level, with a worst-case subgroup deviation of 2.4 percentage points (income quintile Q1: 87.6%). Against the Guvenen-Karahan-Ozkan-Song (GKOS) GMM benchmark, SAGA achieves a 31.9% reduction in CRPS at forecast horizon h=10 and a 41.2% reduction at h=20. A 500,000-individual synthetic mirror dataset is hosted at Zenodo under DOI `10.5281/zenodo.20260287` and enables pipeline-level replication without access to the protected Statistics Sweden microdata.

## Table of contents

- [Synopsis](#synopsis)
- [What is in this repository](#what-is-in-this-repository)
- [Quick start](#quick-start)
- [Replicating paper results](#replicating-paper-results)
- [Architecture in one figure](#architecture-in-one-figure)
- [Headline numerical results](#headline-numerical-results)
- [Ethics and data governance](#ethics-and-data-governance)
- [How to cite](#how-to-cite)
- [License](#license)
- [Contact](#contact)

## What is in this repository

- **`src/saga/`** - installable Python package implementing the SAGA model, tokenization, conformal calibration, baselines, evaluation, and data utilities; see [docs/index.md](./docs/index.md)
- **`configs/`** - YAML configuration files for every model variant and every evaluation procedure; see [docs/methodology/saga-architecture.md](./docs/methodology/saga-architecture.md)
- **`scripts/`** - POSIX shell scripts wrapping every training, inference, and evaluation entry point; see [docs/reproducibility/full-replication.md](./docs/reproducibility/full-replication.md)
- **`notebooks/`** - eight self-contained Jupyter notebooks (00 quickstart through 07 interpretability) runnable on the synthetic mirror; see [docs/reproducibility/quickstart.md](./docs/reproducibility/quickstart.md)
- **`tests/`** - unit, integration, and property-based tests covering every public module; see [docs/reproducibility/quickstart.md](./docs/reproducibility/quickstart.md)
- **`docs/`** - encyclopedic documentation mirroring every section and table of the SAGA manuscript; see [docs/index.md](./docs/index.md)
- **`data/synthetic/`** - placeholder directory populated by `scripts/download_synthetic_mirror.sh` from Zenodo; see [docs/data/synthetic-mirror.md](./docs/data/synthetic-mirror.md)
- **`data/real/`** - documentation only; real LISA microdata reside exclusively inside the SCB MONA secure compute environment under project SCB-MONA-2026-147
- **`benchmarks/`** - wall-clock, throughput, and memory benchmarks on NVIDIA A100 40 GB hardware; see [benchmarks/README.md](./benchmarks/README.md)
- **`.devcontainer/`** - GitHub Codespaces and VSCode Dev Containers configuration for a one-click development environment

## Quick start

The following sequence clones the repository, installs the conda environment, downloads the synthetic mirror from Zenodo, runs the unit test suite, and executes the quickstart notebook.

```bash
git clone https://github.com/olaflaitinen/saga.git
cd saga

conda env create -f environment.yaml
conda activate saga

bash scripts/download_synthetic_mirror.sh

pytest tests/unit/ -q --tb=short

jupyter nbconvert --to notebook --execute notebooks/00-quickstart.ipynb \
    --output notebooks/00-quickstart.executed.ipynb
```

The unit test suite completes in under 5 minutes on a single CPU core using the tiny synthetic panel fixture. The quickstart notebook runs end to end on the synthetic mirror in under 30 minutes on a single NVIDIA A100 40 GB and in approximately 4 hours on a modern CPU (see [docs/reproducibility/wall-clock-budgets.md](./docs/reproducibility/wall-clock-budgets.md) for per-script timing tables).

## Replicating paper results

Full replication of every table in the manuscript requires the protected Statistics Sweden LISA microdata, which are accessible only to approved researchers operating inside the SCB MONA secure compute environment under project SCB-MONA-2026-147. Pipeline-level replication on the synthetic mirror is feasible without MONA access. Bit-level replication requires independent MONA project approval from Statistics Sweden; see [docs/data/mona-secure-environment.md](./docs/data/mona-secure-environment.md) for the application procedure. Ethics approval reference: Swedish Ethical Review Authority decision 2026-04127-01.

| Result table | Script | A100 wall clock | CPU-only estimate |
|---|---|---|---|
| Table I: headline forecast accuracy | `scripts/train_saga.sh` then `scripts/run_inference.sh` | ~15 h per seed | Not tractable in under 3 days |
| Table II: conformal coverage | `scripts/calibrate_conformal.sh` | ~1 h | ~8 h |
| Table III: coverage by subgroup | `scripts/calibrate_conformal.sh` | ~1 h | ~8 h |
| Table IV: lifetime earnings | `scripts/run_lifetime_monte_carlo.sh` | ~2 h | ~18 h |
| Table V: tax microsimulation | `scripts/run_tax_microsimulation.sh` | ~1 h | ~10 h |
| Table VI: ablation study | `scripts/run_all_ablations.sh` | ~40 h | Not tractable |
| Table VII: robustness checks | `scripts/run_all_robustness.sh` | ~60 h | Not tractable |
| Table VIII: heterogeneity | `scripts/run_inference.sh` with subgroup flags | ~3 h | ~30 h |
| Table IX: placebos | `scripts/run_all_placebos.sh` | ~20 h | Not tractable |
| Table XI: MC sensitivity | `scripts/run_mc_sensitivity.sh` | ~4 h | ~36 h |

CPU-only replication of the full training pipeline is not tractable in under several days. CPU estimates above apply only to evaluation stages (post-training inference on a pre-trained checkpoint). A single training seed requires 14.8 wall-clock hours on 8 NVIDIA A100 40 GB devices; CPU replication of training is not recommended.

## Architecture in one figure

```mermaid
graph TD
    subgraph Tokenization
        A1[15 continuous features] --> T1[ContinuousSubvectorEncoder dim=64]
        A2[10 categorical features] --> T2[CategoricalSubvectorEncoder dim=76]
        A3[missingness indicators] --> T3[MissingnessSubvectorEncoder dim=16]
        A4[age integer] --> T4[AgePositionalEncoder dim=64]
        A5[year integer] --> T5[YearPositionalEncoder dim=32]
        T1 --> CAT[Concatenate dim=252]
        T2 --> CAT
        T3 --> CAT
        T4 --> CAT
        T5 --> CAT
        CAT --> PROJ[Linear 252 to 384 with bias]
    end
    subgraph Transformer decoder L=6
        PROJ --> L1[TransformerBlock 1: pre-LN, causal MHA H=8, FFN dim=1536, GELU, dropout=0.1]
        L1 --> L2[TransformerBlock 2]
        L2 --> L3[TransformerBlock 3]
        L3 --> L4[TransformerBlock 4]
        L4 --> L5[TransformerBlock 5]
        L5 --> L6[TransformerBlock 6]
    end
    subgraph Output heads
        L6 --> PH[PointHead: Linear to scalar, trained with MSE]
        L6 --> QH[QuantileHead: Linear to 7 quantiles, trained with pinball loss]
    end
    subgraph Conformal wrapper
        PH --> CONF[AdaptiveTemporalConformalCalibrator horizon-stratified]
        QH --> CONF
        CONF --> OUT[Calibrated prediction intervals at 50 / 80 / 90 / 95 percent nominal]
    end
```

## Headline numerical results

All results are on the test set (cohorts 1983-1985) unless otherwise noted. CRPS improvement is relative to the GKOS benchmark.

| Metric | h | SAGA | LSTM | GBT | GKOS | AR(1) | FF |
|---|---|---|---|---|---|---|---|
| MAE (log SEK) | 1 | 0.241 | 0.259 | 0.271 | 0.287 | 0.341 | 0.308 |
| MAE (log SEK) | 5 | 0.384 | 0.419 | 0.443 | 0.518 | 0.592 | 0.487 |
| MAE (log SEK) | 10 | 0.512 | 0.573 | 0.618 | 0.734 | 0.841 | 0.681 |
| MAE (log SEK) | 20 | 0.631 | 0.718 | 0.794 | 1.013 | 1.187 | 0.876 |
| RMSE (log SEK) | 10 | 0.683 | n/a | n/a | n/a | n/a | n/a |
| CRPS | 10 | 0.318 | 0.364 | 0.401 | 0.467 | 0.541 | 0.428 |
| Pinball | 10 | 0.147 | 0.168 | 0.186 | 0.214 | 0.249 | 0.197 |
| PICP at 90% nominal (%) | 10 | 90.3 | 84.7 | 82.1 | 86.3 | 81.4 | 79.8 |

CRPS reduction vs. GKOS at $h=10$: **31.9%**. CRPS reduction vs. GKOS at $h=20$: **41.2%**. MAE reduction vs. GKOS at $h=20$: **37.7%**.

See the arXiv preprint at <https://arxiv.org/abs/__TBD_ARXIV_ID__>.

Conformal marginal coverage at 90% nominal: **90.3%**. Worst-case subgroup (income quintile Q1): **87.6%**, a deviation of 2.4 percentage points from nominal.

Full tables including Diebold-Mariano test statistics, lifetime earnings statistics, tax microsimulation results, ablation results, robustness checks, heterogeneity decomposition, and placebo tests are documented in [docs/results/](./docs/results/).

## Ethics and data governance

The SAGA model was trained and evaluated exclusively within the SCB MONA (Microdata Online Access) secure compute environment under Statistics Sweden MONA project SCB-MONA-2026-147. All data handling, variable derivation, and model training occurred inside MONA. No row-level data, no individual-level predictions, and no intermediate model outputs linked to identifiable individuals left the secure environment. Only aggregate statistics (means, percentiles, model coefficients, performance metrics) and the trained model weights were exported following Statistics Sweden's standard disclosure-control review process.

The study received ethics approval from the Swedish Ethical Review Authority under decision reference 2026-04127-01. The ethics approval covers the linkage of LISA register variables for the purpose of probabilistic earnings forecasting and microsimulation research. The approval documentation is described in [docs/ethics/ethical-approval.md](./docs/ethics/ethical-approval.md).

The synthetic mirror dataset (500,000 individuals) released on Zenodo under DOI `10.5281/zenodo.20260287` was generated from SAGA's predictive distribution conditional on resampled demographic baseline vectors, not from any real individual's record. Membership inference AUC on the synthetic mirror is 0.512, consistent with random chance. The synthetic mirror enables pipeline-level replication of the full analysis workflow. It does not enable bit-level replication of the numerical results reported in the manuscript, which requires independent MONA project approval from Statistics Sweden.

## How to cite

If you use SAGA in your research, please cite the manuscript and the software separately.

**Manuscript:**

```bibtex
@article{saga2026,
  author  = {Laitinen-Fredriksson Lundstrom-Imanov, Gustav Olaf Yunus and Comert, Hafize Gonca},
  title   = {{SAGA}: A Sequence-Adaptive Generative Architecture for Multi-Horizon
             Probabilistic Forecasting with Adaptive Temporal Conformal Prediction},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  year    = {2026},
  doi     = {10.5281/zenodo.20260287},
  url     = {https://doi.org/10.5281/zenodo.20260287}
}
```

**Software (this repository):**

```bibtex
@software{saga_software2026,
  author    = {Laitinen-Fredriksson Lundstrom-Imanov, Gustav Olaf Yunus and Comert, Hafize Gonca},
  title     = {SAGA: A Sequence-Adaptive Generative Architecture (software repository)},
  version   = {1.0.0},
  year      = {2026},
  url       = {https://github.com/olaflaitinen/saga},
  doi       = {10.5281/zenodo.20260287}
}
```

When the arXiv preprint ID is assigned, replace `__TBD_ARXIV_ID__` in `README.md` and `CITATION.cff` with the actual arXiv identifier (e.g. `2506.XXXXX`).

## License

Source code: [Apache License 2.0](./LICENSE).

Documentation and data (including the synthetic mirror): [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](./LICENSE-CC-BY-NC-4.0).

The permitted-use scope of both licenses explicitly excludes credit scoring, insurance pricing, employment screening, and tax-enforcement targeting of individuals. See [docs/ethics/dual-use-statement.md](./docs/ethics/dual-use-statement.md).

## Contact

Corresponding author: Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov MSc, Department of Economics, Stockholm University, SE-106 91 Stockholm, Sweden. Email: olaf.laitinen@su.se. ORCID: [0009-0006-5184-0810](https://orcid.org/0009-0006-5184-0810).

For bug reports and reproducibility questions, please open a [GitHub Issue](https://github.com/olaflaitinen/saga/issues). For general discussion, use [GitHub Discussions](https://github.com/olaflaitinen/saga/discussions). For press inquiries and academic collaboration requests, contact the corresponding author by email.
