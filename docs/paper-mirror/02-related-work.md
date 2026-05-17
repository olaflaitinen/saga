# Related work

## Table of contents

- [Earnings dynamics in labor economics](#earnings-dynamics-in-labor-economics)
- [Sequence models for administrative panel data](#sequence-models-for-administrative-panel-data)
- [Transformers for tabular and time-series data](#transformers-for-tabular-and-time-series-data)
- [Conformal prediction for time series](#conformal-prediction-for-time-series)
- [Tax-benefit microsimulation](#tax-benefit-microsimulation)
- [See also](#see-also)

## Earnings dynamics in labor economics

The econometric literature on earnings dynamics begins with [Lillard and Willis (1978)][lillard1978],
who decompose log earnings into a permanent individual effect and a transitory AR(1) component,
and [MaCurdy (1982)][mccurdy1982], who establishes conditions for identification of the
permanent-transitory decomposition in panel data. [Meghir and Pistaferri (2011)][meghir2011]
survey the subsequent four decades of theoretical and empirical development.

The key finding motivating SAGA is that the Gaussian shock assumption is systematically violated.
[Guvenen et al. (2021)][gkos2021] document large positive skewness and excess kurtosis in annual
earnings changes across the earnings distribution, and propose a Gaussian mixture-of-normals
model (the GKOS model) estimated by GMM matching 87 empirical moments. The GKOS model is the
primary parametric benchmark in this paper. [Karahan and Ozkan (2013)][karahan2013] document that
the persistence of earnings shocks varies substantially across the lifecycle and across the
earnings distribution. [Guvenen (2009)][guvenen2009] provides an empirical investigation of
heterogeneous income profiles.

[Halvorsen et al. (2024)][halvorsen2024] extend the earnings dynamics literature to Norwegian
administrative register data, demonstrating that the non-Gaussian features documented in the
U.S. (GKOS) replicate closely in Scandinavian panel data. [Browning et al. (2010)][browning2010]
propose a flexible semiparametric model of income processes. The SAGA paper is, to our knowledge,
the first to apply a large-scale transformer to Swedish register earnings data, and the first to
provide formal conformal coverage guarantees for long-horizon earnings forecasts.

## Sequence models for administrative panel data

[Savcisens et al. (2024)][savcisens2023] apply a BERT-style transformer to Danish administrative
registers, tokenizing sequences of life events (education, employment, benefits, health) and
pre-training with masked token prediction, to produce embeddings that predict a wide range of
life outcomes. SAGA differs from this approach in three respects: SAGA is autoregressive rather
than masked, SAGA is trained specifically for multi-horizon probabilistic earnings forecasting
rather than general embedding pre-training, and SAGA includes a formal conformal calibration
layer with a theoretical coverage guarantee.

## Transformers for tabular and time-series data

[Huang et al. (2020)][huang2020] (TabTransformer) apply attention to the categorical features of
tabular records, leaving continuous features unmodified. [Gorishniy et al. (2021)][gorishniy2021full]
revisit deep learning models for tabular data and introduce FT-Transformer, which applies attention
to all features via piecewise-linear or periodic numerical embeddings. [Gorishniy et al. (2022)][gorishniy2022]
extends this with improved numerical feature embeddings. [Hollmann et al. (2025)][hollmann2025]
demonstrate that a PFN-style in-context learner (TabPFN) matches or exceeds tree-based models
on small tabular classification tasks.

SAGA's typed-subvector tokenization is most closely related to the FT-Transformer's projection
of each feature into a common embedding space, but differs by maintaining separate projection
subspaces for continuous, categorical, missingness, and positional information before
concatenating to the final token.

For time series, [Nie et al. (2023)][nie2023] (PatchTST) apply a patch-based tokenization of
univariate channels to long-term forecasting. [Zhou et al. (2021)][zhou2021] (Informer) and
[Wu et al. (2021)][wu2021] (Autoformer) propose efficient attention mechanisms for long-range
dependencies. [Wen et al. (2023)][wen2023] survey the broader landscape of transformer models
for time series. SAGA differs from this literature by operating on multivariate administrative
panel records (not univariate sensor streams), by using a causally-masked decoder rather than
an encoder-decoder or encoder-only architecture, and by targeting administrative panel data
with missing values, categorical covariates, and per-individual sequence lengths that vary
across the conditioning window.

## Conformal prediction for time series

[Romano et al. (2019)][romano2019] (CQR) introduce conformalized quantile regression, which
wraps a quantile regressor with a split conformal layer to provide marginal coverage guarantees.
SAGA's conformal layer uses CQR-style nonconformity scores, stratified by forecast horizon.

[Stankeviciute et al. (2021)][stankeviciute2021] apply conformal prediction to sequential
health outcome forecasting, introducing horizon-conditional coverage as an evaluation criterion.
[Xu and Xie (2021)][xu2021] provide a conformal prediction interval for dynamic time series
under exchangeability. [Bhatnagar et al. (2024)][bhatnagar2024] propose adaptive conformal
autoregressive methods that update the calibration quantile over time. The Adaptive Temporal
Conformal Prediction theorem (Theorem 2) in the SAGA manuscript provides a bound on the
worst-case subgroup coverage deviation as a function of calibration set size and the Lipschitz
constant of the conditional CDF, building on the DKW inequality ([Dvoretzky et al., 1956][dvoretzky1956];
[Massart, 1990][massart1990]).

Vovk et al. (2005) [vovk2005full] provide the foundational theory of conformal prediction.
[Lei et al. (2018)][lei2018full] establish distribution-free predictive inference for regression.
[Angelopoulos and Bates (2023)][angelopoulos2023full] provide a comprehensive tutorial.

## Tax-benefit microsimulation

[Bourguignon and Spadaro (2006)][bourguignon2006] survey microsimulation as a tool for evaluating
redistributive policies. [Sutherland and Figari (2013)][sutherland2013] describe EUROMOD, the
EU-wide tax-benefit microsimulation model. The Swedish FASIT model ([Flood, 2024][flood2024]) is
the primary Swedish counterpart. TRIM3 ([Wheaton, 2008][wheaton2008]) is the U.S. equivalent
maintained by the Urban Institute. SAGA's tax microsimulation applies the 2022 Swedish tax
schedule uniformly across all forecast paths; the schedule details are documented in
[docs/results/downstream-tax-microsimulation.md](../results/downstream-tax-microsimulation.md).

## See also

- [Method](03-method.md)
- [Methodology: baselines](../methodology/baselines.md)
- [Bibliography: references](../bibliography/references.md)

[lillard1978]: ../bibliography/references.md#lillard1978
[mccurdy1982]: ../bibliography/references.md#mccurdy1982
[meghir2011]: ../bibliography/references.md#meghir2011
[gkos2021]: ../bibliography/references.md#gkos2021
[karahan2013]: ../bibliography/references.md#karahan2013
[guvenen2009]: ../bibliography/references.md#guvenen2009
[halvorsen2024]: ../bibliography/references.md#halvorsen2024
[browning2010]: ../bibliography/references.md#browning2010
[savcisens2023]: ../bibliography/references.md#savcisens2023
[huang2020]: ../bibliography/references.md#huang2020
[gorishniy2021full]: ../bibliography/references.md#gorishniy2021full
[gorishniy2022]: ../bibliography/references.md#gorishniy2022
[hollmann2025]: ../bibliography/references.md#hollmann2025
[nie2023]: ../bibliography/references.md#nie2023
[zhou2021]: ../bibliography/references.md#zhou2021
[wu2021]: ../bibliography/references.md#wu2021
[wen2023]: ../bibliography/references.md#wen2023
[romano2019]: ../bibliography/references.md#romano2019
[stankeviciute2021]: ../bibliography/references.md#stankeviciute2021
[xu2021]: ../bibliography/references.md#xu2021
[bhatnagar2024]: ../bibliography/references.md#bhatnagar2024
[dvoretzky1956]: ../bibliography/references.md#dvoretzky1956
[massart1990]: ../bibliography/references.md#massart1990
[vovk2005full]: ../bibliography/references.md#vovk2005full
[lei2018full]: ../bibliography/references.md#lei2018full
[angelopoulos2023full]: ../bibliography/references.md#angelopoulos2023full
[bourguignon2006]: ../bibliography/references.md#bourguignon2006
[sutherland2013]: ../bibliography/references.md#sutherland2013
[flood2024]: ../bibliography/references.md#flood2024
[wheaton2008]: ../bibliography/references.md#wheaton2008
