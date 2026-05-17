# Lifetime earnings distribution

**Important:** Results are computed on the test set using real LISA microdata inside the
Statistics Sweden MONA secure compute environment under project SCB-MONA-2026-147. The
"observed partial truth" column reflects the partially observed LISA earnings histories for
test cohort individuals (not a fully observed lifetime, because most individuals have not
yet reached age 64 at the 2022 panel end). Bit-level replication requires independent MONA
project approval.

## Table of contents

- [Lifetime earnings statistics (Table IV)](#lifetime-earnings-statistics-table-iv)
- [Gini and top-income-share discussion](#gini-and-top-income-share-discussion)
- [Aggregation methodology](#aggregation-methodology)
- [See also](#see-also)

## Lifetime earnings statistics (Table IV)

Lifetime earnings aggregated from $M=500$ Monte Carlo paths per individual on the test set
(cohorts 1983-1985). All amounts in millions of 2022 Swedish krona (MSEK), discounted at real
rate $r=0.02$ to reference age 20. Currency: 2022 Swedish krona, CPI-deflated.

| Statistic | SAGA | GKOS | AR(1) | Observed partial |
|---|---|---|---|---|
| Mean (MSEK) | 12.43 | 12.91 | 11.87 | 12.67 |
| Median (MSEK) | 10.84 | 11.03 | 10.21 | 11.12 |
| P10 (MSEK) | 4.73 | 4.29 | 3.98 | 4.91 |
| P90 (MSEK) | 21.37 | 23.84 | 22.14 | 22.08 |
| P99 (MSEK) | 38.42 | 47.13 | 44.87 | 39.71 |
| Gini coefficient | 0.327 | 0.378 | 0.396 | 0.341 |
| Top-1% income share (%) | 8.3 | 11.2 | 10.8 | 8.9 |

## Gini and top-income-share discussion

SAGA's Gini of 0.327 is closest to the observed partial truth (0.341) among all models,
underestimating inequality by 0.014 Gini points. GKOS overestimates inequality by 0.037
(Gini 0.378) and AR(1) by 0.055 (Gini 0.396). The primary driver of the GKOS overestimation
is the P99 lifetime earnings: GKOS produces a P99 of 47.13 MSEK versus the observed partial
truth of 39.71 MSEK and SAGA's 38.42 MSEK. The GKOS mixture-of-normals shock structure tends
to generate excessively large right-tail shocks at long horizons, inflating the top of the
income distribution.

SAGA's top-one-percent income share (8.3%) is close to the observed partial truth (8.9%).
GKOS produces 11.2% and AR(1) produces 10.8%, both substantially overestimating the
concentration at the top. This pattern is consistent with the MAE reduction of 37.7% at $h=20$,
which indicates that SAGA's long-horizon forecasts are substantially more accurate in absolute
terms.

## Aggregation methodology

For each test individual, $M=500$ autoregressive forecast paths are drawn from SAGA's predictive
distribution. Each path is exponentiated from log SEK to nominal SEK, CPI-deflated to 2022
values, and discounted at real rate $r=0.02$ to reference age 20. The discounted annual earnings
for each path are summed from the year after the conditioning window ends to the last in-panel
year on or before age 64 (or to 2022, whichever comes first). The per-individual lifetime
earnings estimate is the median of the $M=500$ path-level lifetime sums. The distributional
statistics (mean, P10, P90, P99, Gini, top-one-percent) are computed across individuals.

Full implementation: `src/saga/inference/monte_carlo_lifetime.py` and
`src/saga/evaluation/lifetime_statistics.py`. Configuration: `configs/lifetime_monte_carlo.yaml`.

## See also

- [Downstream tax microsimulation](downstream-tax-microsimulation.md)
- [Methodology: lifetime Monte Carlo aggregation](../methodology/lifetime-monte-carlo-aggregation.md)
- [Paper mirror: experiments](../paper-mirror/05-experiments.md)
- [Source: src/saga/inference/monte_carlo_lifetime.py](../../src/saga/inference/monte_carlo_lifetime.py)
