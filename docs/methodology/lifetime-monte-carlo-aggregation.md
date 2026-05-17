# Lifetime Monte Carlo aggregation

## Table of contents

- [Procedure](#procedure)
- [Parameters](#parameters)
- [Empirical lifetime coverage](#empirical-lifetime-coverage)
- [Source code](#source-code)
- [See also](#see-also)

## Procedure

For each test individual $i$:

1. Draw $M=500$ autoregressive forecast paths from SAGA's predictive distribution, conditioned
   on the 10-year observed earnings history.
2. For each path $m$, compute the sequence of nominal annual earnings by exponentiating the
   log-earnings forecast: $Y_{i,t,m} = \exp(\log \tilde{Y}_{i,t,m})$.
3. Apply CPI deflation to express all amounts in 2022 Swedish krona.
4. Compute the present value of each annual earnings amount, discounted at real rate $r=0.02$
   to reference age 20:
$$
\mathrm{PV}_{i,t,m} = \frac{Y_{i,t,m}}{(1 + r)^{\,\mathrm{age}_{i,t} - 20}}
$$
5. Sum the discounted earnings from the year after the conditioning window ends to the last
   in-panel year on or before age 64:
$$
\mathrm{LW}_{i,m} = \sum_{t} \mathrm{PV}_{i,t,m}
$$
6. The per-individual lifetime earnings point estimate is the median of
   $\{\mathrm{LW}_{i,m} : m = 1, \ldots, M\}$.
7. Distributional statistics (mean, median, P10, P90, P99, Gini, top-one-percent share) are
   computed across individuals.

## Parameters

| Parameter | Value |
|---|---|
| Number of Monte Carlo paths $M$ | 500 |
| Real discount rate $r$ | 0.02 |
| Reference age | 20 |
| Currency | 2022 Swedish krona, CPI-deflated |
| Forecast window | from year after conditioning end to last year on or before age 64 |

Configuration file: `configs/lifetime_monte_carlo.yaml`.

## Empirical lifetime coverage

The empirical lifetime coverage of the lifetime prediction interval (derived by computing the
empirical $(1-\alpha)$ and $\alpha$ quantiles of $\{\mathrm{LW}_{i,m}\}$ across paths $m$) at the 90% nominal level
is 89.2% on the test set. This is slightly below the 90.3% marginal per-horizon coverage,
consistent with the fact that the lifetime aggregation introduces additional uncertainty not
fully captured by the per-horizon conformal intervals.

Formal lifetime aggregate coverage guarantees are listed as future work in
[docs/roadmap.md](../roadmap.md).

## Source code

- `src/saga/inference/monte_carlo_lifetime.py` - LifetimeMonteCarloAggregator class
- `src/saga/evaluation/lifetime_statistics.py` - lifetime distributional statistics

## See also

- [Results: lifetime earnings distribution](../results/lifetime-earnings-distribution.md)
- [Results: downstream tax microsimulation](../results/downstream-tax-microsimulation.md)
- [Config: configs/lifetime_monte_carlo.yaml](../../configs/lifetime_monte_carlo.yaml)
