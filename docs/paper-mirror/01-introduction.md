# Introduction

## Table of contents

- [Motivation](#motivation)
- [Contributions](#contributions)
- [Organization of this document](#organization-of-this-document)
- [See also](#see-also)

## Motivation

The distribution of lifetime earnings is a central object of study in labor economics, public
finance, and social policy. Precise probabilistic forecasts of individual earnings trajectories
enable downstream analyses that require not just point predictions but full distributional
information: tax and transfer microsimulation, pension liability estimation, credit risk
assessment for public programs, and welfare analysis of redistributive reforms.

Classical income dynamics models, following the tradition of [Lillard and Willis (1978)][lillard1978],
[MaCurdy (1982)][mccurdy1982], and [Meghir and Pistaferri (2011)][meghir2011], represent
earnings as the sum of a highly persistent individual fixed effect, an AR(1) permanent shock,
and a transitory component. The Guvenen-Karahan-Ozkan-Song (GKOS) model
[Guvenen et al., 2021][gkos2021] extends this framework to a Gaussian mixture-of-normals
representation that captures the substantial non-Gaussianity of earnings shocks documented
in U.S. and European administrative data, and estimates the model by GMM matching 87 empirical
moments covering the mean, variance, skewness, kurtosis, and fifth central moment of one-, three-,
and five-year log earnings changes within ten-year age bins from age 25 to age 60. The GKOS model
is the current state-of-the-art parametric benchmark in earnings dynamics and its performance on
long-horizon forecasting is the primary baseline in this paper.

At the same time, the machine learning community has produced a rich literature on transformer
architectures ([Vaswani et al., 2017][vaswani2017]) applied to sequential prediction tasks,
including tabular data modeling ([Huang et al., 2020][huang2020]; [Gorishniy et al., 2021][gorishniy2021full];
[Hollmann et al., 2025][hollmann2025]) and time series forecasting ([Nie et al., 2023][nie2023];
[Zhou et al., 2021][zhou2021]; [Wu et al., 2021][wu2021]). Recent work applying sequence models
to administrative panel data includes [Savcisens et al. (2024)][savcisens2023], who use a BERT-style
life-event model on Danish administrative registers to predict a range of life outcomes.

SAGA bridges these two traditions. It is a causally-masked autoregressive transformer trained
end-to-end on administrative earnings panel data, with a tokenization scheme designed specifically
for the structure of register data (typed subvectors for continuous, categorical, missingness, and
positional information), a dual point-and-quantile output head, and a conformal prediction wrapper
(Theorem 2) that provides finite-sample horizon-specific coverage guarantees.

The conformal prediction layer is motivated by the literature on predictive inference
([Vovk et al., 2005][vovk2005full]; [Romano et al., 2019][romano2019]; [Lei et al., 2018][lei2018full];
[Angelopoulos and Bates, 2023][angelopoulos2023full]) and specifically the extensions to
time-series settings ([Stankeviciute et al., 2021][stankeviciute2021]; [Xu and Xie, 2021][xu2021];
[Bhatnagar et al., 2024][bhatnagar2024]). The Adaptive Temporal Conformal Prediction theorem
(Theorem 2 of the manuscript) provides a bound on the worst-case subgroup coverage deviation
as a function of the calibration set size and the Lipschitz constant of the conditional CDF
near its nominal quantile.

The microsimulation application follows the tradition of [Bourguignon and Spadaro (2006)][bourguignon2006],
[Sutherland and Figari (2013)][sutherland2013], and the Swedish FASIT model ([Flood, 2024][flood2024]),
applying the 2022 Swedish tax schedule uniformly across all forecast paths to estimate the
distribution of lifetime effective average tax rates.

## Contributions

The manuscript makes the following contributions:

1. SAGA architecture: a typed-subvector tokenization scheme and causally-masked transformer
   decoder for autoregressive earnings forecasting, with $10{,}872{,}960$ parameters and a maximum
   context length of 45 yearly tokens (ages 16 to 60).

2. Adaptive Temporal Conformal Prediction (Theorem 2): a horizon-stratified split conformal
   calibration layer with a finite-sample bound on the worst-case subgroup coverage deviation
   as a function of calibration set size $n_h$ and Lipschitz constant $L_h$.

3. Empirical evaluation on the Swedish LISA register: 2,143,817 individuals, 61,284,903
   person-year observations, cohorts 1960 to 1985, producing headline CRPS reductions of
   31.9% at $h=10$ and 41.2% at $h=20$ versus GKOS.

4. Lifetime earnings microsimulation: Monte Carlo aggregation of $M=500$ paths per individual,
   discounted at $r=0.02$ to age 20, producing Gini and top-one-percent estimates substantially
   closer to the partial observed truth than GKOS or AR(1)+FE.

5. Synthetic mirror dataset: 500,000 individuals generated from SAGA's predictive distribution,
   moment-matched within 1.8%, membership-inference AUC 0.512, hosted on Zenodo.

## Organization of this document

The paper-mirror documentation tree follows the manuscript section structure:
[Related work](02-related-work.md), [Method](03-method.md), [Data](04-data.md),
[Experiments](05-experiments.md), [Discussion](06-discussion.md),
[Conclusion](07-conclusion.md), and Appendices A through G.

## See also

- [Methodology: SAGA architecture](../methodology/saga-architecture.md)
- [Data: LISA register overview](../data/lisa-register-overview.md)
- [Results: headline forecast accuracy](../results/headline-forecast-accuracy.md)
- [Bibliography: references](../bibliography/references.md)

[lillard1978]: ../bibliography/references.md#lillard1978
[mccurdy1982]: ../bibliography/references.md#mccurdy1982
[meghir2011]: ../bibliography/references.md#meghir2011
[gkos2021]: ../bibliography/references.md#gkos2021
[vaswani2017]: ../bibliography/references.md#vaswani2017
[huang2020]: ../bibliography/references.md#huang2020
[gorishniy2021full]: ../bibliography/references.md#gorishniy2021full
[hollmann2025]: ../bibliography/references.md#hollmann2025
[nie2023]: ../bibliography/references.md#nie2023
[zhou2021]: ../bibliography/references.md#zhou2021
[wu2021]: ../bibliography/references.md#wu2021
[savcisens2023]: ../bibliography/references.md#savcisens2023
[vovk2005full]: ../bibliography/references.md#vovk2005full
[romano2019]: ../bibliography/references.md#romano2019
[lei2018full]: ../bibliography/references.md#lei2018full
[angelopoulos2023full]: ../bibliography/references.md#angelopoulos2023full
[stankeviciute2021]: ../bibliography/references.md#stankeviciute2021
[xu2021]: ../bibliography/references.md#xu2021
[bhatnagar2024]: ../bibliography/references.md#bhatnagar2024
[bourguignon2006]: ../bibliography/references.md#bourguignon2006
[sutherland2013]: ../bibliography/references.md#sutherland2013
[flood2024]: ../bibliography/references.md#flood2024
