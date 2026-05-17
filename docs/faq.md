# Frequently asked questions

## Can I replicate the headline CRPS of 0.318 without MONA access?

No. Bit-level replication requires access to the real LISA microdata under an independent
Statistics Sweden MONA project. Pipeline-level replication on the synthetic mirror produces
results close to (but not identical to) the manuscript values. See
[docs/reproducibility/quickstart.md](reproducibility/quickstart.md).

## How do I download the synthetic mirror?

```bash
bash scripts/download_synthetic_mirror.sh
```

This downloads the Zenodo deposit (DOI: `10.5281/zenodo.20260287`) and verifies SHA-256 checksums.

## Why is the CRPS reduction larger at $h=20$ than at $h=10$?

SAGA's advantage over GKOS grows with horizon because the GKOS parametric mixture-of-normals
structure is adequate for short-horizon extrapolation but diverges at long horizons where
earnings trajectories fan out non-Gaussianly across the income distribution. SAGA learns the
empirical quantile function directly and avoids this divergence.

## What is the Zenodo DOI for the synthetic mirror?

The DOI placeholder `10.5281/zenodo.20260287` will be replaced with the actual Zenodo DOI when the
deposit is finalized. Check the `CITATION.cff` file or the Zenodo deposit page for the current
DOI.

## What is the difference between Theorem 1 and Theorem 2?

Theorem 1 is the standard split conformal marginal coverage guarantee (from Vovk et al., 2005
and Lei et al., 2018): for any new individual exchangeable with the calibration set, the
prediction interval covers the true outcome with probability at least $1 - \alpha$ in finite
samples, regardless of the underlying distribution.

Theorem 2 (Adaptive Temporal Conformal Prediction) strengthens this by bounding the
worst-case deviation of coverage from the nominal level within any subgroup, as a function
of the calibration set size $n_h$ and the Lipschitz constant $L_h$ of the conditional CDF near
its nominal quantile.

## Can I use SAGA for credit scoring or insurance pricing?

No. These uses are explicitly prohibited by the dual-use statement. See
[docs/ethics/dual-use-statement.md](ethics/dual-use-statement.md).

## What GPU do I need to run SAGA?

Any NVIDIA GPU with CUDA 12.1 support and at least 24 GB of VRAM is supported (with reduced
batch size). An A100 40 GB is recommended. CPU-only mode is supported but is approximately
40x slower. See [docs/reproducibility/hardware-notes.md](reproducibility/hardware-notes.md).

## How do I cite SAGA?

See the [Citation section of the README](../README.md#citation) or the `CITATION.cff` and
`CITATION.bib` files at the repository root.

## How do I report a bug or reproducibility issue?

Open a GitHub Issue using the appropriate template:
[Bug report](https://github.com/olaflaitinen/saga/issues/new?template=bug_report.yaml) or
[Reproducibility question](https://github.com/olaflaitinen/saga/issues/new?template=reproducibility_question.yaml).
