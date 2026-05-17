# Sample selection rules

The core analysis sample of 2,143,817 individuals is constructed from the LISA register using
four sample selection rules (SR1 through SR4), applied in sequence.

## SR1: Birth cohort restriction

Individuals are retained if their birth year falls in the range 1960-1990. The core analysis
sample uses cohorts 1960-1985. The out-of-time holdout uses cohorts 1986-1990. Individuals
born before 1960 are excluded because their age-16 entry into LISA (before 1976) predates
the 1990 start of the LISA panel, making a complete 10-year conditioning window at any
reasonable forecast origin unavailable.

## SR2: Residency and continuity requirement

Individuals are retained if they are observed in the LISA panel for at least 10 consecutive
calendar years, corresponding to the conditioning window length. Individuals who emigrated
permanently before accumulating 10 years of LISA coverage are excluded. Temporary absences
of at most 2 years are tolerated and imputed.

## SR3: Age at conditioning window end

Individuals are retained if they are between age 26 and age 54 at the end of their conditioning
window. This ensures that the forecast window contains at least 10 prime-working-age years
(ages 27 to 36 minimum) and that the individual has had at least 10 years of post-school labor
market exposure before the conditioning window begins.

## SR4: Non-trivial labor market attachment

Individuals are retained if they have positive labor earnings in at least 5 of the 10
conditioning window years. Individuals with fewer than 5 positive-earnings years in the
conditioning window are excluded because their earnings history contains insufficient signal
for trajectory forecasting. This rule excludes primarily individuals whose primary income
source is disability pension or social assistance throughout the conditioning window.

## Post-selection statistics

After applying SR1-SR4:

| Statistic | Value |
|---|---|
| Core analysis sample individuals | 2,143,817 |
| Core sample person-year observations | 61,284,903 |
| Train split (cohorts 1960-1979) | 1,834,201 individuals |
| Calibration split (cohorts 1980-1982) | 168,542 individuals |
| Test split (cohorts 1983-1985) | 141,074 individuals |
| Out-of-time holdout (cohorts 1986-1990) | 287,391 individuals |
| Share zero-earnings person-years | 7.4% |

## See also

- [LISA register overview](lisa-register-overview.md)
- [Train/calibration/test splits](train-cal-test-splits.md)
- [Source: src/saga/data/splits.py](../../src/saga/data/splits.py)
