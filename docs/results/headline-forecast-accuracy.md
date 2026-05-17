# Headline forecast accuracy

**Important:** The results on this page are computed on the test set (cohorts 1983-1985,
141,074 individuals) using the real LISA microdata inside the Statistics Sweden MONA secure
compute environment under project SCB-MONA-2026-147. Bit-level replication requires independent
MONA project approval from Statistics Sweden. Pipeline-level replication on the synthetic mirror
is provided by `scripts/run_inference.sh` after model training.

## Table of contents

- [Main accuracy table (Table I)](#main-accuracy-table-table-i)
- [Headline CRPS improvements](#headline-crps-improvements)
- [Diebold-Mariano test statistics (Table X)](#diebold-mariano-test-statistics-table-x)
- [Interpretation notes](#interpretation-notes)
- [See also](#see-also)

## Main accuracy table (Table I)

All results on test set, cohorts 1983-1985. PICP is the Prediction Interval Coverage Probability
at 90% nominal; only SAGA achieves nominal coverage because only SAGA is equipped with the
conformal calibration wrapper.

| Metric | h | SAGA | LSTM | GBT | GKOS | AR(1) | FF |
|---|---|---|---|---|---|---|---|
| MAE (log SEK) | 1 | 0.241 | 0.259 | 0.271 | 0.287 | 0.341 | 0.308 |
| MAE (log SEK) | 5 | 0.384 | 0.419 | 0.443 | 0.518 | 0.592 | 0.487 |
| MAE (log SEK) | 10 | 0.512 | 0.573 | 0.618 | 0.734 | 0.841 | 0.681 |
| MAE (log SEK) | 20 | 0.631 | 0.718 | 0.794 | 1.013 | 1.187 | 0.876 |
| RMSE (log SEK) | 10 | 0.683 | n/a | n/a | n/a | n/a | n/a |
| CRPS | 10 | 0.318 | 0.364 | 0.401 | 0.467 | 0.541 | 0.428 |
| Pinball | 10 | 0.147 | 0.168 | 0.186 | 0.214 | 0.249 | 0.197 |
| PICP at 90% nominal (%) | 10 | 90.3 | 84.7 | 82.1 | 86.3 | 81.4 | 79.8 |

## Headline CRPS improvements

- CRPS reduction versus GKOS at $h=10$: **31.9%** (SAGA 0.318 vs. GKOS 0.467)
- CRPS reduction versus GKOS at $h=20$: **41.2%**
- MAE reduction versus GKOS at $h=20$: **37.7%** (SAGA 0.631 vs. GKOS 1.013)

## Diebold-Mariano test statistics (Table X)

Newey-West HAC standard errors at lag $5$ ([Newey and West, 1987][newey1987]). Positive
statistic indicates SAGA is more accurate. All statistics exceed the 1% critical value of $2.576$.

| Comparison | $h=1$ | $h=5$ | $h=10$ | $h=20$ | MAE $h=10$ |
|---|---|---|---|---|---|
| SAGA vs. GKOS | 3.41 | 7.12 | 9.84 | 11.27 | 8.73 |
| SAGA vs. AR(1) | 7.83 | 12.34 | 14.72 | 16.43 | 13.41 |
| SAGA vs. GBT | 4.12 | 8.41 | 10.31 | 12.18 | 9.12 |
| SAGA vs. LSTM | 2.87 | 5.63 | 7.48 | 8.94 | 6.83 |
| SAGA vs. FF | 5.21 | 9.87 | 11.63 | 13.71 | 10.94 |

The test is implemented in `src/saga/evaluation/diebold_mariano.py`. See
[Appendix B](../paper-mirror/appendix-b-diebold-mariano.md) for the full test description.

## Interpretation notes

The CRPS ([Gneiting and Raftery, 2007][gneiting2007]) measures the accuracy of the full
predictive distribution, not just the point forecast. SAGA's CRPS advantage over all
baselines grows with forecast horizon, consistent with the interpretation that the SAGA
transformer learns long-range distributional features of earnings trajectories that are
not captured by parametric models.

The PICP advantage is mechanically guaranteed by the conformal calibration wrapper: by
construction, the conformal prediction intervals achieve marginal coverage equal to the
nominal level (90.3% at 90% nominal), up to the $1/(n_h+1)$ finite-sample correction term.
The other models do not have a conformal wrapper and produce miscalibrated intervals.

All Diebold-Mariano statistics exceed the 1% critical value $2.576$ at every horizon, confirming
that the SAGA accuracy advantage is statistically significant and not an artifact of sampling
variation in the test cohort.

## See also

- [Calibration coverage](calibration-coverage.md)
- [Ablation study](ablation-study.md)
- [Paper mirror: experiments](../paper-mirror/05-experiments.md)
- [Appendix B: Diebold-Mariano](../paper-mirror/appendix-b-diebold-mariano.md)
- [Source: src/saga/evaluation/metrics_probabilistic.py](../../src/saga/evaluation/metrics_probabilistic.py)

[newey1987]: ../bibliography/references.md#newey1987
[gneiting2007]: ../bibliography/references.md#gneiting2007
