# Synthetic mirror dataset

## Table of contents

- [Overview](#overview)
- [Generation procedure](#generation-procedure)
- [Validation statistics](#validation-statistics)
- [Download](#download)
- [File inventory](#file-inventory)
- [Permitted use](#permitted-use)
- [See also](#see-also)

## Overview

The synthetic mirror dataset contains 500,000 synthetic individuals generated from SAGA's
predictive distribution conditional on resampled demographic baseline vectors drawn from the
training cohort marginal distribution. It is hosted at Zenodo under DOI `10.5281/zenodo.20260287`.

The synthetic mirror enables pipeline-level replication of the full SAGA analysis without
access to the protected Statistics Sweden LISA microdata. It does NOT enable bit-level
replication of the manuscript's numerical results.

## Generation procedure

Full documentation of the generation procedure is in
[Appendix D: synthetic data protocol](../paper-mirror/appendix-d-synthetic-data-protocol.md).

In brief:
1. 500,000 demographic baseline vectors are drawn by conditional resampling from the training
   cohort marginal distribution.
2. A 10-year earnings history is sampled from a kernel density estimate fitted to the joint
   distribution of training-cohort conditioning windows conditional on the baseline vector.
3. SAGA's autoregressive decoder produces one forecast path per individual, extended to age 64.
4. Auxiliary feature paths are supplied by the auxiliary feature imputation network.
5. The synthetic sequences are post-processed for logical consistency and submitted to
   Statistics Sweden disclosure-control review.

## Validation statistics

- **Moment match:** Within 1.8% on first through fourth order moments (mean, variance,
  skewness, kurtosis) at every age within every demographic subgroup defined by sex, education
  level, and birth cohort decade. The 1.8% figure is the maximum relative deviation across
  all (age, subgroup, moment) triples.

- **Membership inference AUC:** 0.512, consistent with random chance. The membership inference
  attack follows [Shokri et al. (2017)][shokri2017] with a shadow-model approach on 50,000
  held-out synthetic and 50,000 held-out real individuals.

## Download

```bash
bash scripts/download_synthetic_mirror.sh
```

This script downloads the synthetic mirror parquet files from Zenodo (DOI `10.5281/zenodo.20260287`)
into `data/synthetic/` and verifies SHA-256 checksums against `data/synthetic/checksum.sha256`.

## File inventory

The Zenodo deposit contains:

| File | Rows | Description |
|---|---|---|
| `synthetic_train.parquet` | 350,000 individuals | Training split |
| `synthetic_cal.parquet` | 75,000 individuals | Calibration split |
| `synthetic_test.parquet` | 75,000 individuals | Test split |
| `moment_validation.csv` | per (age, subgroup, moment) | Validation vs. real LISA |

All parquet files conform to the schema in `data/schema.yaml`.

## Permitted use

The synthetic mirror is released under Creative Commons Attribution-NonCommercial 4.0
International (CC BY-NC 4.0). The permitted-use scope explicitly excludes credit scoring,
insurance pricing, employment screening, and tax-enforcement targeting of individuals.
See [docs/ethics/dual-use-statement.md](../ethics/dual-use-statement.md).

## See also

- [Appendix D: synthetic data protocol](../paper-mirror/appendix-d-synthetic-data-protocol.md)
- [MONA secure environment](mona-secure-environment.md)
- [Source: src/saga/data/synthetic_generator.py](../../src/saga/data/synthetic_generator.py)
- [Script: scripts/download_synthetic_mirror.sh](../../scripts/download_synthetic_mirror.sh)

[shokri2017]: ../bibliography/references.md#shokri2017
