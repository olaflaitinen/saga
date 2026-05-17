# Appendix D: synthetic data protocol

This appendix documents the procedure used to generate the synthetic mirror dataset of
500,000 individuals, hosted at Zenodo under DOI `10.5281/zenodo.20260287`. The synthetic mirror
enables pipeline-level replication of the full SAGA analysis workflow without access to the
protected Statistics Sweden LISA microdata.

## Table of contents

- [Generation procedure](#generation-procedure)
- [Validation statistics](#validation-statistics)
- [Privacy guarantees](#privacy-guarantees)
- [File inventory](#file-inventory)
- [See also](#see-also)

## Generation procedure

The synthetic mirror is generated from SAGA's predictive distribution in three steps.

**Step 1: baseline demographic vector resampling.** For each of the 500,000 synthetic
individuals, a baseline demographic and educational vector is drawn by conditional resampling
from the empirical marginal distribution of the training cohorts (cohorts 1960-1979). The
resampled vector includes birth year, sex, country of birth group, region of residence at
age 20, and educational attainment level and field (Sun2000Niva and Sun2000Inr) as observed
in the LISA register. The resampling is stratified by birth cohort so that the synthetic
panel covers the same cohort range as the core sample.

**Step 2: earnings sequence sampling.** Given the resampled baseline vector, an initial
observed earnings history of 10 years (the conditioning window) is drawn from a kernel density
estimate fitted to the joint distribution of ten-year earnings histories conditional on the
baseline vector in the training cohorts. SAGA's autoregressive decoder then produces $M=1$
forecast path per synthetic individual, extending the earnings sequence from age after the
conditioning window ends to age 64. The auxiliary feature imputation network supplies predicted
industry, occupation, region, and employment indicators at each forecast step.

**Step 3: post-processing and disclosure review.** The synthetic sequences are post-processed
to enforce logical consistency (no negative nominal earnings, no earnings below the 0.01st
percentile of the real training-cohort distribution at each age-year cell). The resulting
dataset is submitted to the Statistics Sweden disclosure-control review process before release.

## Validation statistics

The synthetic mirror matches the real LISA panel within 1.8% on first through fourth order
moments (mean, variance, skewness, kurtosis) at every age within every demographic subgroup
defined by sex, education level, and birth cohort decade. This 1.8% figure is the maximum
relative deviation across all (age, subgroup, moment) triples.

Membership inference AUC: 0.512, consistent with random chance. The membership inference
attack follows [Shokri et al. (2017)][shokri2017] with a shadow-model approach trained on
50,000 held-out synthetic individuals and 50,000 held-out real individuals. The near-random
AUC confirms that the synthetic mirror does not memorize individual real records.

## Privacy guarantees

The synthetic mirror does not contain any real individual's record. No row in the synthetic
dataset corresponds to a real person in the LISA register. The generation procedure is
entirely based on SAGA's learned predictive distribution and the empirical marginal
distributions of the training cohorts, not on any form of data augmentation or perturbation
of real records. The disclosure-control review performed by Statistics Sweden before release
confirmed that the synthetic mirror satisfies the statistical disclosure limitation standards
applied to all SCB MONA outputs.

## File inventory

The Zenodo deposit (DOI: `10.5281/zenodo.20260287`) contains the following files:

- `synthetic_train.parquet`: 350,000 synthetic individuals assigned to the training split.
- `synthetic_cal.parquet`: 75,000 synthetic individuals assigned to the calibration split.
- `synthetic_test.parquet`: 75,000 synthetic individuals assigned to the test split.
- `moment_validation.csv`: per-age, per-subgroup, per-moment validation statistics comparing
  the synthetic mirror to the real LISA panel.

All parquet files conform to the schema defined in `data/schema.yaml` and validated by
`src/saga/data/schema.py`.

## See also

- [Data: synthetic mirror](../data/synthetic-mirror.md)
- [Source: src/saga/data/synthetic_generator.py](../../src/saga/data/synthetic_generator.py)
- [Script: scripts/export_synthetic_mirror.sh](../../scripts/export_synthetic_mirror.sh)
- [Script: scripts/download_synthetic_mirror.sh](../../scripts/download_synthetic_mirror.sh)

[shokri2017]: ../bibliography/references.md#shokri2017
