# Quickstart: pipeline-level replication

This document describes the five-command quickstart path for pipeline-level replication of
the SAGA analysis workflow using the synthetic mirror dataset.

**Important:** The quickstart produces results on the synthetic mirror (500,000 individuals,
Zenodo DOI `10.5281/zenodo.20260287`), not on the real LISA microdata. CRPS reductions on the
synthetic mirror will be close to the headline values (31.9% at $h=10$) but will not match them
exactly. Bit-level replication requires independent MONA project access from Statistics Sweden.
See [docs/data/mona-secure-environment.md](../data/mona-secure-environment.md).

## Prerequisites

- Linux or macOS (Windows is supported via Docker or WSL2)
- Git
- Conda (Mambaforge recommended)
- 16 GB RAM minimum; 32 GB recommended
- An NVIDIA GPU with CUDA 12.1 support is strongly recommended. CPU-only mode is supported but
  training will be slow (approximately 40x longer than on A100).
- At least 20 GB of free disk space for the synthetic mirror and checkpoint files.

## Five-command quickstart

```bash
# 1. Clone the repository
git clone https://github.com/olaflaitinen/saga.git && cd saga

# 2. Create and activate the conda environment
conda env create -f environment.yaml && conda activate saga

# 3. Install the SAGA package in editable mode and set up pre-commit hooks
pip install -e ".[dev]" && pre-commit install

# 4. Download the synthetic mirror from Zenodo and verify checksums
bash scripts/download_synthetic_mirror.sh

# 5. Run the quickstart notebook end to end
jupyter nbconvert --to notebook --execute \
    --ExecutePreprocessor.timeout=7200 \
    notebooks/00-quickstart.ipynb \
    --output notebooks/00-quickstart.executed.ipynb
```

After command 5 completes successfully, the executed notebook
`notebooks/00-quickstart.executed.ipynb` will contain:

- A trained SAGA model (3 seeds instead of 5 for speed) fit on `synthetic_train.parquet`.
- Evaluation on `synthetic_test.parquet`: CRPS at $h=10$ and $h=20$, MAE at $h=10$.
- Conformal coverage at 90% nominal: expected approximately 89.5% to 90.5%.
- Lifetime Monte Carlo paths and a Gini coefficient estimate.
- A comparison table with the GKOS and LSTM baselines.

## Expected wall-clock times

| Step | Time on A100 | Time on CPU only |
|---|---|---|
| Download synthetic mirror | 5-15 minutes (network) | 5-15 minutes |
| Training (3 seeds) | approximately 5 hours | approximately 8 days |
| Evaluation | approximately 30 minutes | approximately 6 hours |

For a faster smoke test (single seed, 50,000 steps), use:

```bash
bash scripts/run_quickstart_smoke.sh
```

This completes in approximately 1.5 hours on a single A100 GPU.

## See also

- [Full replication](full-replication.md)
- [Docker environment](docker-environment.md)
- [Hardware notes](hardware-notes.md)
- [Notebook: notebooks/00-quickstart.ipynb](../../notebooks/00-quickstart.ipynb)
