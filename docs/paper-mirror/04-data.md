# Data

## Table of contents

- [The Swedish LISA register](#the-swedish-lisa-register)
- [Sample selection](#sample-selection)
- [Train, calibration, and test splits](#train-calibration-and-test-splits)
- [Key sample statistics](#key-sample-statistics)
- [Access and disclosure](#access-and-disclosure)
- [See also](#see-also)

## The Swedish LISA register

**Important:** The results reported in this manuscript were produced entirely within the
Statistics Sweden MONA (Microdata Online Access) secure compute environment under project
SCB-MONA-2026-147. No row-level data, no individual-level predictions, and no intermediate
outputs linked to identifiable individuals left the secure environment. Bit-level replication
of the numerical results requires independent MONA project approval from Statistics Sweden.
Pipeline-level replication is possible using the synthetic mirror dataset hosted at Zenodo
under DOI `10.5281/zenodo.20260287`. See [docs/data/mona-secure-environment.md](../data/mona-secure-environment.md).

The Swedish LISA register (longitudinell integrationsdatabas for sjukforsak-ringsandarbetsmarknad)
is a longitudinal administrative database maintained by Statistics Sweden (Statistiska
centralbyran, SCB). LISA covers the universe of individuals resident in Sweden at the end of
each calendar year who are aged 16 or older, linked across the following administrative sources:
the tax register (Inkomst- och taxeringsregistret), the social insurance register, the education
register (Utbildningsregistret), the total population register (RTB), and the business register
(foretagsdatabasen). LISA has been maintained annually since 1990.

For each individual-year observation, LISA provides earnings (labor and capital), transfer
payments, employment status, employer identity (SNI2007 industry, SSYK2012 occupation), region
of residence (twenty-one counties), education level and field (Sun2000Niva, Sun2000Inr), and
household and family variables (marital status, number of children, age of youngest child). The
variable inventory used in SAGA is documented in detail in
[docs/data/variable-inventory.md](../data/variable-inventory.md).

## Sample selection

The core analysis sample is constructed from the LISA panel using four sample selection rules
(SR1 through SR4), which are documented in full in
[docs/data/sample-selection-rules.md](../data/sample-selection-rules.md). After applying all
four rules, the core analysis sample contains 2,143,817 individuals with 61,284,903 total
person-year observations. The share of zero-earnings observations in the person-year sample is 7.4%.

An additional out-of-time holdout pool, comprising birth cohorts 1986 to 1990, contains
287,391 individuals. This pool is kept entirely separate from the core sample during training
and conformal calibration; it is used only for the out-of-time robustness check R7 in Table VII.
For the $h=10$ evaluation in R7, the effective sample is restricted to cohorts 1986 to 1988
with effective $n = 168{,}734$.

The conditioning window length is 10 observed years per individual. The forecast window extends
from the year after the conditioning window ends to the last in-panel year on or before age 64.

## Train, calibration, and test splits

The core analysis sample is split deterministically by birth cohort, with no random stratification:

| Split | Cohorts | Individuals | Purpose |
|---|---|---|---|
| Train | 1960-1979 (twenty cohorts) | 1,834,201 | Model training |
| Calibration | 1980-1982 (three cohorts) | 168,542 | Conformal calibration; early stopping |
| Test | 1983-1985 (three cohorts) | 141,074 | Reported results |
| Out-of-time holdout | 1986-1990 | 287,391 | Robustness check R7 |

The calibration split (cohorts 1980-1982) serves two roles: early stopping of the main model
(validation pinball loss at steps of 5,000, patience 20 checks), and conformal calibration for
Theorem 1 and Theorem 2. The conformal calibration uses only non-censored $h=10$ conformity scores;
the number of unique calibration individuals contributing one non-censored $h=10$ conformity score
is $14{,}107$.

The validation pinball loss evaluated on calibration cohorts 1980-1982 is the early-stopping
criterion.

## Key sample statistics

- Total individuals in core sample: 2,143,817
- Total person-year observations in core sample: 61,284,903
- Share of zero-earnings person-years: 7.4%
- Train individuals: 1,834,201
- Calibration individuals: 168,542
- Test individuals: 141,074
- Out-of-time holdout individuals: 287,391
- Effective $n$ for $h=10$ out-of-time evaluation (cohorts 1986-1988): 168,734
- Unique $h=10$ conformal calibration individuals: 14,107
- Panel coverage: 1990 to 2022 (33 years)
- Birth cohorts retained for core sample: 1960 to 1985
- Currency unit: 2022 Swedish krona, CPI-deflated

## Access and disclosure

The real LISA panel is accessible exclusively to approved researchers operating inside the
Statistics Sweden MONA secure compute environment. The application procedure for independent
MONA access is described in [docs/data/mona-secure-environment.md](../data/mona-secure-environment.md).

The study received ethics approval from the Swedish Ethical Review Authority under decision
reference 2026-04127-01. The ethics approval covers the linkage of LISA register variables
for the purpose of probabilistic earnings forecasting and microsimulation research.

## See also

- [Data: LISA register overview](../data/lisa-register-overview.md)
- [Data: variable inventory](../data/variable-inventory.md)
- [Data: sample selection rules](../data/sample-selection-rules.md)
- [Data: train/calibration/test splits](../data/train-cal-test-splits.md)
- [Data: MONA secure environment](../data/mona-secure-environment.md)
- [Data: synthetic mirror](../data/synthetic-mirror.md)
- [Ethics: ethical approval](../ethics/ethical-approval.md)
