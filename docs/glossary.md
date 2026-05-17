# Glossary

**AETR:** Average Effective Tax Rate. Total lifetime tax divided by total lifetime gross earnings.

**AR(1)+FE:** First-differenced AR(1) model with individual fixed effects, estimated by
Arellano-Bond GMM.

**bfloat16:** Brain floating-point 16-bit format, used for activations during SAGA training.
Has the same exponent range as float32 but with reduced mantissa precision.

**CRPS:** Continuous Ranked Probability Score. A proper scoring rule measuring the accuracy
of a full predictive distribution. Lower is better. See [Gneiting and Raftery (2007)][gneiting2007].

**Conformal prediction:** A distribution-free framework for constructing prediction intervals
with finite-sample marginal coverage guarantees. See [vovk2005full][vovk2005full].

**CQR:** Conformalized Quantile Regression. A conformal prediction method that uses
quantile regression predictions as the nonconformity score. See [Romano et al. (2019)][romano2019].

**DKW:** Dvoretzky-Kiefer-Wolfowitz inequality. Provides a concentration bound of the form
$P(\sup_t |F_n(t) - F(t)| > \varepsilon) \leq 2\exp(-2n\varepsilon^2)$
for the deviation between an empirical CDF $F_n$ and the true CDF $F$.

**FASIT:** The Swedish official tax-benefit microsimulation model maintained by Statistics
Sweden in collaboration with the Swedish Social Insurance Agency and the Tax Agency.

**GKOS:** Guvenen-Karahan-Ozkan-Song. The Gaussian mixture earnings dynamics model estimated
by GMM, used as the primary parametric baseline in SAGA. See [gkos2021][gkos2021].

**GELU:** Gaussian Error Linear Unit. The activation function used in SAGA's transformer decoder.
See [Hendrycks and Gimpel (2016)][hendrycks2016].

**GMM:** Generalized Method of Moments. Used to estimate the GKOS baseline.

**LISA:** Longitudinell integrationsdatabas for sjukforsakrings- och arbetsmarknadsstudier.
The Swedish longitudinal administrative register database used as the primary data source.

**MAE:** Mean Absolute Error, measured in log SEK.

**MONA:** Microdata Online Access. The Statistics Sweden secure compute environment for
accessing Swedish administrative register data.

**Monte Carlo:** The process of drawing $M=500$ autoregressive forecast paths per individual
to estimate the distribution of lifetime earnings.

**PICP:** Prediction Interval Coverage Probability. The empirical fraction of test individuals
whose true future earnings fall inside the predicted interval at a specified nominal level.

**Pre-LayerNorm:** Layer normalization applied before rather than after each sub-layer in the
transformer, following Xiong et al. (2020). Improves training stability.

**RMSE:** Root Mean Square Error, measured in log SEK.

**SAGA:** Sequence-Adaptive Generative Architecture. The name of the model introduced in the
manuscript.

**SNI2007:** Swedish standard industrial classification, 2007 revision. A two-digit industry
code is used in the categorical subvector.

**SSYK2012:** Swedish standard classification of occupations, 2012 revision. A three-digit
occupation code is used in the categorical subvector.

**Stochastic depth:** A training regularization technique that randomly drops residual
connections during training. See [Huang et al. (2016)][huang2016].

**Sun2000Niva:** Swedish education level classification (Niva = level), 2000 edition.
Used to classify highest attained education level into four categories.

**Sun2000Inr:** Swedish education field classification (Inriktning = orientation), 2000 edition.
Used to classify field of study at one-digit resolution.

[gneiting2007]: bibliography/references.md#gneiting2007
[vovk2005full]: bibliography/references.md#vovk2005full
[romano2019]: bibliography/references.md#romano2019
[gkos2021]: bibliography/references.md#gkos2021
[hendrycks2016]: bibliography/references.md#hendrycks2016
[huang2016]: bibliography/references.md#huang2016
