# Robustness checks

**Important:** Results are computed using real LISA microdata inside the Statistics Sweden
MONA secure compute environment under project SCB-MONA-2026-147.

## Table of contents

- [Robustness results (Table VII)](#robustness-results-table-vii)
- [Notes on specific checks](#notes-on-specific-checks)
- [See also](#see-also)

## Robustness results (Table VII)

CRPS reduction versus GKOS at $h=10$, recomputed under each perturbation.

| Check | CRPS reduction vs. GKOS (%) |
|---|---|
| R1: train on cohorts 1965-1979 only | 30.8 |
| R2: male sample only | 29.7 |
| R3: stable employer subsample only | 24.1 |
| R4: calibration set restricted to cohort 1985 | 31.9 |
| R5a: discount rate $r=0\%$ | 33.1 |
| R5b: discount rate $r=1\%$ | 32.7 |
| R5c: discount rate $r=3\%$ | 31.8 |
| R6: HICP deflator instead of CPI | 32.2 |
| R7: out-of-time holdout (cohorts 1986-1990) | 28.4 |
| R8: PSID-inventory-restricted features (Sweden-internal) | 21.4 |
| R9: recession-year test fold (forecast windows containing 2009) | 28.8 |

## Notes on specific checks

**R4 (calibration restricted to cohort 1985).** The headline conformal calibration uses cohorts
1980-1982. R4 uses only cohort 1985, which is part of the test split, but is evaluated on a
held-out subset. The identical CRPS reduction of 31.9% confirms that the conformal calibration
is not sensitive to the specific cohorts used, consistent with the exchangeability assumption A1.

**R7 (out-of-time holdout).** The holdout cohorts 1986-1990 (287,391 individuals) are kept
entirely separate from the training and calibration sets. For the $h=10$ evaluation, the
effective sample is restricted to cohorts 1986-1988 ($n = 168{,}734$) because cohorts 1989-1990
do not have 10 forecast years available within the 2022 panel end. The CRPS reduction of 28.4% is slightly
below the headline 31.9%, consistent with a mild out-of-distribution effect for the most recent
cohorts.

**R8 (PSID-inventory-restricted features).** This check is a Sweden-internal feature-portability
ablation that removes LISA features with no close equivalent in the Panel Study of Income Dynamics
(PSID) variable inventory, following [McGonagle et al. (2012)][mcgonagle2012]. The removed features
are the three-digit SSYK2012 occupation code and several employer-level covariates. **No PSID
microdata were accessed.** This is not a replication on PSID data; it is a within-Sweden test of
how much accuracy depends on the rich employer-level register information available in LISA but not
in household survey panels. The reduced CRPS reduction of 21.4% quantifies this feature-portability
gap.

**R9 (recession-year test fold).** The test fold is restricted to individuals whose forecast window
contains the 2009 financial crisis year (i.e., individuals for whom the 2009 forecast year falls
within their $h=1$ through $h=10$ forecast window). The CRPS reduction of 28.8% indicates that SAGA
retains a substantial accuracy advantage even in recession years, though the advantage is slightly
smaller than the full-sample headline of 31.9%.

## See also

- [Heterogeneity decomposition](heterogeneity-decomposition.md)
- [Placebo and falsification](placebo-and-falsification.md)
- [Source: src/saga/evaluation/robustness_runner.py](../../src/saga/evaluation/robustness_runner.py)
- [Script: scripts/run_all_robustness.sh](../../scripts/run_all_robustness.sh)

[mcgonagle2012]: ../bibliography/references.md#mcgonagle2012
