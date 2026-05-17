# Appendix B: Diebold-Mariano test statistics

This appendix reproduces the Diebold-Mariano test statistics from Table X of the manuscript
([Diebold and Mariano, 1995][diebold1995full]). Newey-West HAC standard errors at lag $5$
([Newey and West, 1987][newey1987]). A positive test statistic indicates that SAGA is more
accurate than the baseline. All statistics exceed the 1% critical value of $2.576$ at every
horizon reported, confirming statistical significance at the 1% level.

## Test statistics (Table X)

The test is a two-sided test of equal predictive accuracy. The null hypothesis is that SAGA
and the baseline have equal expected loss under the CRPS metric (CRPS columns) and the MAE
metric (MAE at $h=10$ column). Losses are computed on the test set (cohorts 1983-1985).

| Comparison | $h=1$ | $h=5$ | $h=10$ | $h=20$ | MAE $h=10$ |
|---|---|---|---|---|---|
| SAGA vs. GKOS | 3.41 | 7.12 | 9.84 | 11.27 | 8.73 |
| SAGA vs. AR(1) | 7.83 | 12.34 | 14.72 | 16.43 | 13.41 |
| SAGA vs. GBT | 4.12 | 8.41 | 10.31 | 12.18 | 9.12 |
| SAGA vs. LSTM | 2.87 | 5.63 | 7.48 | 8.94 | 6.83 |
| SAGA vs. FF | 5.21 | 9.87 | 11.63 | 13.71 | 10.94 |

All statistics exceed the 1% critical value of $2.576$. The SAGA vs. LSTM comparison at $h=1$
produces the smallest statistic ($2.87$), consistent with the relatively narrow performance gap
between SAGA and LSTM at short horizons.

## Implementation details

The Diebold-Mariano test is implemented in `src/saga/evaluation/diebold_mariano.py` using the
`DieboldMarianoTest` class. The implementation follows the standard procedure:

1. Compute per-individual loss differences $d_i = \ell(\hat{y}^{\text{SAGA}}_i, y_i) - \ell(\hat{y}^{\text{base}}_i, y_i)$ for the
   chosen loss function (CRPS or MAE).
2. Compute the Newey-West HAC covariance estimate of $\mathrm{Var}(\bar{d})$,
   using lag truncation $5$.
3. Compute the DM statistic as $\mathrm{DM} = \bar{d}\,/\,\sqrt{\widehat{\mathrm{Var}}(\bar{d})}$.
4. Compare to the standard normal critical value (two-sided, 1% level: $z_{0.005} = 2.576$).

See [bibliography: diebold1995full](../bibliography/references.md#diebold1995full) and
[bibliography: newey1987](../bibliography/references.md#newey1987).

## See also

- [Results: headline forecast accuracy](../results/headline-forecast-accuracy.md)
- [Source: src/saga/evaluation/diebold_mariano.py](../../src/saga/evaluation/diebold_mariano.py)
- [Tests: test_diebold_mariano.py](../../tests/unit/test_diebold_mariano.py)

[diebold1995full]: ../bibliography/references.md#diebold1995full
[newey1987]: ../bibliography/references.md#newey1987
