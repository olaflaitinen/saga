# Appendix F: Monte Carlo sensitivity

This appendix reproduces the Monte Carlo sensitivity analysis from Table XI of the manuscript.
The study examines how the marginal and Q1 subgroup conformal coverage at the 90% nominal level
depends on the calibration set size $n_h$ and the estimation method (LOCO-CV versus bootstrap).

**Important:** The LOCO-CV and bootstrap studies reported below are conducted on the real LISA
calibration-cohort residuals, inside the Statistics Sweden MONA secure compute environment under
project SCB-MONA-2026-147. The reported values are not replicable without independent MONA access.
Pipeline-level replication using the synthetic mirror is provided by `scripts/run_mc_sensitivity.sh`
after downloading the synthetic mirror from Zenodo (DOI: `10.5281/zenodo.20260287`).

## Table of contents

- [Design](#design)
- [Results (Table XI)](#results-table-xi)
- [Interpretation](#interpretation)
- [See also](#see-also)

## Design

The sensitivity study varies two dimensions:

1. **Calibration set size $n_h$:** Three values are evaluated: 1,000, 5,000, and 14,107
   (the full $h=10$ calibration set).
2. **Estimation method:** LOCO-CV (leave-one-calibration-cohort-out cross-validation) and
   bootstrap (1,000 resamples of the calibration conformity scores with replacement).

For each $(n_h, \text{method})$ cell, $B = 1{,}000$ replicates are drawn. Each replicate samples $n_h$
conformity scores from the full $h=10$ calibration set (with replacement for bootstrap, without
for LOCO-CV), fits the conformal quantile, and evaluates coverage on the test set (cohorts
1983-1985) marginal and at income quintile Q1. The table reports means with standard deviations
in parentheses.

## Results (Table XI)

90% nominal level, $h=10$, real LISA calibration-cohort residuals. $B = 1{,}000$ replicates per cell.

| Method | $n_h$ | Marginal coverage (%) | Q1 coverage (%) |
|---|---|---|---|
| LOCO-CV | 1,000 | 90.1 (0.8) | 86.9 (2.0) |
| LOCO-CV | 5,000 | 90.0 (0.5) | 88.4 (1.2) |
| LOCO-CV | 14,107 | 90.0 (0.3) | 88.7 (0.9) |
| Bootstrap | 1,000 | 90.1 (0.7) | 87.2 (1.8) |
| Bootstrap | 5,000 | 90.0 (0.4) | 88.5 (1.1) |
| Bootstrap | 14,107 | 90.0 (0.3) | 88.9 (0.8) |

## Interpretation

The marginal coverage is uniformly close to 90.0% across all cells, confirming the
distribution-free marginal guarantee of Theorem 1. The Q1 coverage improves as $n_h$ increases,
from 86.9-87.2% at $n_h = 1{,}000$ to 88.7-88.9% at $n_h = 14{,}107$. This confirms the Theorem 2
prediction that the worst-case subgroup deviation decreases as $\mathcal{O}(L_h / \sqrt{n_h})$.

The standard deviations across replicates decrease monotonically with $n_h$ for both methods
and both subpopulations, confirming the $\sqrt{n_h}$ convergence rate.

The LOCO-CV and bootstrap methods produce nearly identical results at each $n_h$ level, indicating
that the choice of estimation method is not a material source of variation at any practically
relevant calibration set size $n_h$.

## See also

- [Results: calibration coverage](../results/calibration-coverage.md)
- [Appendix E: adaptive temporal conformal](appendix-e-adaptive-temporal-conformal.md)
- [Script: scripts/run_mc_sensitivity.sh](../../scripts/run_mc_sensitivity.sh)
- [Source: src/saga/conformal/coverage_diagnostics.py](../../src/saga/conformal/coverage_diagnostics.py)
