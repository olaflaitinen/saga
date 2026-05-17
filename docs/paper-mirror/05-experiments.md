# Experiments

## Table of contents

- [Training setup](#training-setup)
- [Baselines](#baselines)
- [Headline forecast accuracy (Table I)](#headline-forecast-accuracy-table-i)
- [Conformal coverage (Tables II and III)](#conformal-coverage-tables-ii-and-iii)
- [Lifetime earnings statistics (Table IV)](#lifetime-earnings-statistics-table-iv)
- [Tax microsimulation (Table V)](#tax-microsimulation-table-v)
- [Ablation study (Table VI)](#ablation-study-table-vi)
- [Robustness checks (Table VII)](#robustness-checks-table-vii)
- [Heterogeneity decomposition (Table VIII)](#heterogeneity-decomposition-table-viii)
- [Placebo and falsification tests (Table IX)](#placebo-and-falsification-tests-table-ix)
- [Diebold-Mariano tests (Table X)](#diebold-mariano-tests-table-x)
- [Monte Carlo sensitivity (Table XI)](#monte-carlo-sensitivity-table-xi)
- [See also](#see-also)

## Training setup

The SAGA model is trained on the LISA train split (cohorts 1960-1979, 1,834,201 individuals)
using AdamW ([Loshchilov and Hutter, 2019][loshchilov2019]) with learning rate $3\times10^{-4}$,
weight decay $10^{-2}$, $\beta_1=0.9$, $\beta_2=0.999$. The learning rate schedule is cosine
decay with 2,000 warmup steps over 300,000 total optimization steps. The per-device batch size
is 512 sequences with gradient accumulation over 4 micro-batches, yielding an effective batch
size of $16{,}384$. Training uses
8 NVIDIA A100 40 GB GPUs with bfloat16 activations accumulating to float32. Per-seed wall-clock
time is 14.8 hours; per-seed accelerator hours are approximately 118. Peak per-device GPU memory
is 34.2 GB.

Five training seeds are used: 20260601, 20260602, 20260603, 20260604, 20260605. Early stopping
uses the validation pinball loss on calibration cohorts 1980-1982, with patience of 20 validation
checks performed every 5,000 steps.

Results in all tables are reported as the mean across the five seeds. Standard deviations across
seeds are reported in the supplementary material.

## Baselines

Five baselines are evaluated:

- **B1 (GKOS):** The Guvenen-Karahan-Ozkan-Song Gaussian mixture process estimated by GMM
  matching 87 moments. See [docs/methodology/baselines.md](../methodology/baselines.md).
- **B2 (AR(1)+FE):** First-differenced AR(1) with individual fixed effects, estimated by
  Arellano-Bond GMM ([Arellano and Bond, 1991][arellano1991]).
- **B3 (GBT):** LightGBM ([Ke et al., 2017][ke2017]) gradient boosted trees, one regressor per
  horizon, with quantile-loss variants for the seven probability levels.
- **B4 (LSTM):** Two-layer LSTM ([Hochreiter and Schmidhuber, 1997][hochreiter1997]) with hidden
  dimension $768$, totaling $10{,}941{,}440$ parameters (approximately matched to SAGA's parameter count).
- **B5 (FF):** Static six-layer feed-forward network on the flattened 10-year conditioning window,
  with no temporal structure.

## Headline forecast accuracy (Table I)

All results are on the test set (cohorts 1983-1985). CRPS improvement is relative to GKOS.

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

CRPS reduction vs. GKOS at $h=10$: 31.9%. CRPS reduction vs. GKOS at $h=20$: 41.2%.
MAE reduction vs. GKOS at $h=20$: 37.7%.

## Conformal coverage (Tables II and III)

Marginal conformal coverage at 90% nominal: 90.3%. The full coverage table by nominal level
and demographic subgroup (Table III in the manuscript) is reproduced in
[docs/results/calibration-coverage.md](../results/calibration-coverage.md).

Worst-case subgroup coverage at 90% nominal: 87.6%, observed in the lowest conditioning income
quintile (Q1). The worst-case deviation from nominal is 2.4 percentage points.

## Lifetime earnings statistics (Table IV)

Lifetime earnings aggregated from $M=500$ Monte Carlo paths per individual on the test set.
All amounts in millions of 2022 Swedish krona (MSEK), discounted at $r=0.02$ to age 20.

| Statistic | SAGA | GKOS | AR(1) | Observed partial |
|---|---|---|---|---|
| Mean (MSEK) | 12.43 | 12.91 | 11.87 | 12.67 |
| Median (MSEK) | 10.84 | 11.03 | 10.21 | 11.12 |
| P10 (MSEK) | 4.73 | 4.29 | 3.98 | 4.91 |
| P90 (MSEK) | 21.37 | 23.84 | 22.14 | 22.08 |
| P99 (MSEK) | 38.42 | 47.13 | 44.87 | 39.71 |
| Gini | 0.327 | 0.378 | 0.396 | 0.341 |
| Top-1% share (%) | 8.3 | 11.2 | 10.8 | 8.9 |

## Tax microsimulation (Table V)

Using the 2022 Swedish tax schedule applied uniformly to all forecast paths. Municipal tax:
32.4% (population-weighted average across 290 municipalities). State income tax: 20% above
the statutory breakpoint (brytpunkt) of SEK 554,900. Employee social security contribution: 7%,
capped at 8.07 income base amounts. The varnskatt of 5% was abolished in 2020 and is not applied.

| Statistic | SAGA | GKOS | AR(1) | Observed partial |
|---|---|---|---|---|
| Mean lifetime tax (MSEK) | 3.84 | 3.97 | 3.71 | 3.91 |
| Mean AETR (%) | 30.1 | 29.4 | 28.8 | 30.6 |
| P99 AETR (%) | 42.7 | 46.8 | 45.3 | 43.4 |
| Lifetime tax Gini | 0.341 | 0.397 | 0.412 | 0.358 |

## Ablation study (Table VI)

CRPS at $h=10$ on the test set for each ablation. Headline SAGA CRPS: $0.318$.

| Ablation | CRPS | $\Delta$ | % change |
|---|---|---|---|
| A1: drop occupation and industry | 0.334 | $+0.016$ | $+5.0\%$ |
| A2: drop family and household | 0.327 | +0.009 | +2.8% |
| A3: LSTM with matched parameters | 0.364 | +0.046 | +14.5% |
| A4: feed-forward on flattened window | 0.493 | +0.175 | +55.0% |
| A5: point head only | 0.347 | +0.029 | +9.1% |
| A6: drop year embedding | 0.341 | +0.023 | +7.2% |
| A7: dimension 192 | 0.328 | +0.010 | +3.1% |
| A8: dimension 768 | 0.319 | +0.001 | +0.3% |
| A9: drop missingness vector | 0.324 | +0.006 | +1.9% |
| A10: drop age embedding | 0.354 | +0.036 | +11.3% |
| A11: SAGA backbone, point head only, conformal off | 0.367 | +0.049 | +15.4% |
| A12: conformal layer on GKOS backbone | 0.451 | +0.133 | +41.8% |
| A13: SAGA backbone, GKOS-style mixture output head | 0.332 | +0.014 | +4.4% |

## Robustness checks (Table VII)

CRPS reduction versus GKOS at $h=10$ under each perturbation. Full discussion in
[docs/results/robustness-checks.md](../results/robustness-checks.md).

| Check | CRPS reduction (%) |
|---|---|
| R1: train on cohorts 1965-1979 only | 30.8 |
| R2: male sample only | 29.7 |
| R3: stable employer subsample only | 24.1 |
| R4: calibration set restricted to cohort 1985 | 31.9 |
| R5a: discount rate $r=0\%$ | 33.1 |
| R5b: discount rate $r=1\%$ | 32.7 |
| R5c: discount rate $r=3\%$ | 31.8 |
| R6: HICP deflator instead of CPI | 32.2 |
| R7: out-of-time holdout cohorts 1986-1990 | 28.4 |
| R8: PSID-inventory-restricted features (Sweden-internal portability ablation) | 21.4 |
| R9: recession-year test fold containing 2009 | 28.8 |

Note on R8: this row is a Sweden-internal feature-portability ablation that removes LISA features
with no close equivalent in the PSID variable inventory ([McGonagle et al., 2012][mcgonagle2012]).
No PSID microdata were accessed. This is not a replication on PSID data.

## Heterogeneity decomposition (Table VIII)

CRPS reduction versus GKOS at $h=10$ by demographic subgroup. Full discussion in
[docs/results/heterogeneity-decomposition.md](../results/heterogeneity-decomposition.md).

## Placebo and falsification tests (Table IX)

| Test | Value | Interpretation |
|---|---|---|
| Permutation placebo CRPS ratio (placebo / headline) | 2.14 | Must be >> 1; confirms signal is not spurious |
| Short-history placebo CRPS reduction (5-year window) | 18.3% | Below 31.9% headline, confirms value of long history |
| Static feature-only placebo CRPS at $h=10$ | $0.623$ | Far above $0.318$ headline, confirms value of sequence |

## Diebold-Mariano tests (Table X)

Newey-West HAC standard errors at lag $5$. Positive statistic indicates SAGA is more accurate.
All statistics exceed the 1% critical value of $2.576$.

See [docs/results/headline-forecast-accuracy.md](../results/headline-forecast-accuracy.md) for
the full table.

## Monte Carlo sensitivity (Table XI)

See [Appendix F](appendix-f-monte-carlo-sensitivity.md) and
[docs/results/calibration-coverage.md](../results/calibration-coverage.md).

## See also

- [Results: headline forecast accuracy](../results/headline-forecast-accuracy.md)
- [Results: calibration coverage](../results/calibration-coverage.md)
- [Results: ablation study](../results/ablation-study.md)
- [Results: robustness checks](../results/robustness-checks.md)
- [Appendix A: hyperparameters](appendix-a-hyperparameters.md)

[loshchilov2019]: ../bibliography/references.md#loshchilov2019
[arellano1991]: ../bibliography/references.md#arellano1991
[ke2017]: ../bibliography/references.md#ke2017
[hochreiter1997]: ../bibliography/references.md#hochreiter1997
[mcgonagle2012]: ../bibliography/references.md#mcgonagle2012
