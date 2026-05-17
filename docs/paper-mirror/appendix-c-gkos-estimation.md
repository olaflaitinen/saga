# Appendix C: GKOS estimation

This appendix documents the GKOS model estimation results from Table XII of the manuscript.
The GKOS model ([Guvenen et al., 2021][gkos2021]) is estimated by GMM matching 87 empirical
moments covering the mean, variance, skewness, kurtosis, and fifth central moment of 1-, 3-,
and 5-year log earnings changes within ten-year age bins from age 25 to age 60,
on the LISA training cohorts 1960-1979.

**Important:** These results were computed within the Statistics Sweden MONA secure compute
environment under project SCB-MONA-2026-147. Bit-level replication requires independent MONA
access. Pipeline-level replication using the synthetic mirror is possible with
`scripts/estimate_gkos.sh` after downloading the synthetic mirror from Zenodo
(DOI: `10.5281/zenodo.20260287`).

## GKOS parameter estimates (Table XII)

Bootstrap standard errors in parentheses, 1,000 resamples.

| Parameter | Estimate | Bootstrap SE |
|---|---|---|
| $\rho$ (AR(1) coefficient) | 0.924 | 0.018 |
| Permanent shock mean (component 1) | -0.287 | 0.043 |
| Permanent shock variance (component 1) | 0.0418 | 0.0062 |
| Permanent shock weight (component 1) | 0.784 | 0.031 |
| Transitory variance (component 1) | 0.0712 | 0.0089 |
| Transitory weight (component 1) | 0.681 | 0.024 |

The 87 moments matched in GMM cover: mean, variance, skewness, kurtosis, and fifth central
moment of one-, three-, and five-year log earnings changes within ten-year age bins from
age 25 to age 60.

## GMM moment specification

The GMM objective function is the weighted sum of squared deviations between the model-implied
and empirically observed moment vectors:

$$
Q(\theta) = \bigl(\hat{m} - m(\theta)\bigr)^\top W^{-1} \bigl(\hat{m} - m(\theta)\bigr)
$$

where $\hat{m}$ is the $87\times1$ vector of empirical moments, $m(\theta)$ is the model-implied
moment vector, and $W$ is the bootstrap-estimated variance-covariance matrix of $\hat{m}$
(1,000 resamples). The 87 moments decompose as:

- 5 moments (mean, variance, skewness, kurtosis, 5th central) $\times$ 3 differencing intervals
  (1-, 3-, 5-year) $\times$ 5 age bins (25-34, 30-39, 35-44, 40-49, 50-59) $= 75$ base
  moments, plus 12 cross-age covariance moments.

## Configuration

The GKOS estimation is configured in `configs/gkos_estimation.yaml`. The estimation is
run by `scripts/estimate_gkos.sh`, which calls `src/saga/baselines/gkos.py`.

## See also

- [Methodology: baselines](../methodology/baselines.md)
- [Source: src/saga/baselines/gkos.py](../../src/saga/baselines/gkos.py)
- [Config: configs/gkos_estimation.yaml](../../configs/gkos_estimation.yaml)

[gkos2021]: ../bibliography/references.md#gkos2021
