# Baselines

## Table of contents

- [B1: GKOS (Guvenen-Karahan-Ozkan-Song)](#b1-gkos)
- [B2: AR(1) with fixed effects](#b2-ar1-with-fixed-effects)
- [B3: LightGBM gradient boosted trees](#b3-lightgbm-gradient-boosted-trees)
- [B4: LSTM](#b4-lstm)
- [B5: static feed-forward](#b5-static-feed-forward)
- [Source code](#source-code)
- [See also](#see-also)

## B1: GKOS

The Guvenen-Karahan-Ozkan-Song model ([Guvenen et al., 2021][gkos2021]) represents log earnings
as the sum of a persistent individual effect, an AR(1) permanent shock with Gaussian mixture
innovations, and a Gaussian mixture transitory shock. The model is estimated by GMM, matching
87 empirical moments (mean, variance, skewness, kurtosis, and fifth central moment of one-, three-,
and five-year log earnings changes within ten-year age bins from age 25 to age 60). The estimation
procedure and parameter estimates are documented in
[Appendix C](../paper-mirror/appendix-c-gkos-estimation.md).

GKOS is the primary econometric benchmark. Its CRPS at $h=10$ is $0.467$ (vs. $0.318$ for SAGA).

## B2: AR(1) with fixed effects

The AR(1)+FE baseline models log earnings as an AR(1) process with individual fixed effects,
estimated by Arellano-Bond GMM ([Arellano and Bond, 1991][arellano1991]) on first differences.
This baseline has 2 free parameters per individual (fixed effect and AR coefficient $\rho$).
The AR(1) CRPS at $h=10$ is $0.541$ (vs. $0.318$ for SAGA).

## B3: LightGBM gradient boosted trees

The GBT baseline uses LightGBM ([Ke et al., 2017][ke2017]) gradient boosted trees, with one
independent regressor per forecast horizon $h$. Quantile variants at the seven probability levels
$\mathcal{Q} = \{0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95\}$ are trained with pinball loss for
CRPS evaluation. The input features are the flattened 10-year conditioning window of earnings
and covariates. The GBT CRPS at $h=10$ is $0.401$ (vs. $0.318$ for SAGA).

## B4: LSTM

The LSTM baseline ([Hochreiter and Schmidhuber, 1997][hochreiter1997]) is a two-layer LSTM with
hidden dimension $768$, processing the same 10-year conditioning window as SAGA. The parameter
count is $10{,}941{,}440$, approximately matched to SAGA's $10{,}872{,}960$. The LSTM baseline
uses the same training schedule and loss function as SAGA (combined MSE $+$ pinball). The LSTM
CRPS at $h=10$ is $0.364$ (vs. $0.318$ for SAGA). The LSTM corresponds to ablation A3.

## B5: static feed-forward

The FF baseline is a six-layer feed-forward network with ReLU activation, applied to the flattened
10-year conditioning window of earnings and covariates as a fixed-length vector, with no recurrent
or attention structure. The parameter count is matched to SAGA's approximately. The FF CRPS at
$h=10$ is $0.428$ (vs. $0.318$ for SAGA). The FF corresponds to ablation A4.

## Source code

- `src/saga/baselines/gkos.py` - GKOSBaseline class
- `src/saga/baselines/ar1_fixed_effect.py` - AR1FixedEffectBaseline class
- `src/saga/baselines/lightgbm_baseline.py` - LightGBMBaseline class
- `src/saga/baselines/lstm_baseline.py` - LSTMBaseline class
- `src/saga/baselines/static_feedforward.py` - StaticFeedForwardBaseline class

All baselines expose the same `fit`, `predict`, and `predict_quantiles` interface as SagaModel.

## See also

- [Results: headline forecast accuracy](../results/headline-forecast-accuracy.md)
- [Results: ablation study](../results/ablation-study.md)
- [Appendix C: GKOS estimation](../paper-mirror/appendix-c-gkos-estimation.md)

[gkos2021]: ../bibliography/references.md#gkos2021
[arellano1991]: ../bibliography/references.md#arellano1991
[ke2017]: ../bibliography/references.md#ke2017
[hochreiter1997]: ../bibliography/references.md#hochreiter1997
