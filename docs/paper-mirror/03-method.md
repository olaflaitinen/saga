# Method

## Table of contents

- [Typed-subvector tokenization](#typed-subvector-tokenization)
- [Transformer decoder architecture](#transformer-decoder-architecture)
- [Output heads](#output-heads)
- [Auxiliary feature imputation network](#auxiliary-feature-imputation-network)
- [Adaptive Temporal Conformal Prediction](#adaptive-temporal-conformal-prediction)
- [Lifetime Monte Carlo aggregation](#lifetime-monte-carlo-aggregation)
- [See also](#see-also)

## Typed-subvector tokenization

Each yearly record for individual $i$ at age $t$ is tokenized into a $384$-dimensional vector
via the following typed-subvector pipeline. The five subvectors are produced independently and
then concatenated to a $252$-dimensional vector, which is projected to $384$ dimensions by a
learned linear layer with bias.

**Continuous subvector (dimension 64).** The 15 continuous features in each yearly record are
standardized using year-specific population means and standard deviations estimated on the
training cohorts, then projected to 64 dimensions via a learned linear layer with no bias.
The 15 continuous features are enumerated in
[docs/data/variable-inventory.md](../data/variable-inventory.md).

**Categorical subvector (dimension 76).** The 10 categorical features are each passed through a
learned embedding table. The embedding widths are: occupation (three-digit SSYK2012, 24 dimensions),
industry (two-digit SNI2007, 16 dimensions), region (twenty-one Swedish counties, 8 dimensions),
highest education level (four categories Sun2000Niva, 4 dimensions), field of study
(one-digit Sun2000Inr, 4 dimensions), sex (4 dimensions), country of birth group
(eight categories, 4 dimensions), marital status (4 dimensions), number of children
(4 dimensions), age of youngest child bucket (4 dimensions). The sum is
$24 + 16 + 8 + 4 + 4 + 4 + 4 + 4 + 4 + 4 = 76$.

**Missingness subvector (dimension 16).** A binary indicator vector for each of the 15 continuous
features plus one global missingness flag (total 16 binary inputs) is projected to 16 dimensions
via a learned linear layer. This subvector allows the transformer to distinguish between true
zero earnings and imputed or missing values.

**Age positional embedding (dimension 64).** The integer age of the individual at each yearly
token is embedded into 64 dimensions via a learned lookup table indexed over the range $[16, 64]$.

**Year positional embedding (dimension 32).** The calendar year of each yearly token is embedded
into 32 dimensions via a learned lookup table indexed over the range $[1990, 2022]$.

**Concatenation and projection.** The five subvectors are concatenated:
$64 + 76 + 16 + 64 + 32 = 252$ dimensions. A linear layer with bias projects $252$ to $384$.

## Transformer decoder architecture

The $384$-dimensional token sequence is processed by a stack of $L=6$ transformer decoder blocks.
Each block uses pre-LayerNorm ([Xiong et al., 2020][xiong2020]), multi-head causal self-attention
with $H=8$ heads and head dimension $d_k = d/H = 384/8 = 48$, a position-wise feed-forward
network with inner dimension $1536 = 4d$, GELU activation ([Hendrycks and Gimpel, 2016][hendrycks2016]),
dropout at rate $0.1$ applied to both the attention weights and the feed-forward activations, and
stochastic depth ([Huang et al., 2016][huang2016]) on residual connections at rate $0.1$. The
causal attention mask is lower-triangular, applied at every layer to prevent any token from
attending to future tokens in the conditioning window.

The maximum context length is 45 yearly tokens, sufficient to span ages 16 to 60. The architecture
has $10{,}872{,}960$ parameters in total.

## Output heads

**Point head.** A linear projection from $384$ to $1$ is applied to each token's hidden state.
The output is the point prediction of log-earnings for the next year. The point head is trained
with mean squared error loss (coefficient $\tfrac{1}{2}$ in the combined loss).

**Quantile head.** A linear projection from $384$ to $7$ is applied to each token's hidden state.
The 7 outputs correspond to the quantile levels $\mathcal{Q} = \{0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95\}$.
The quantile head is trained with pinball loss, summed across the seven quantile levels. The
combined training loss is:

$$
\mathcal{L}(\theta) = \tfrac{1}{2}\,\mathrm{MSE}(\hat{y}, y)
+ \sum_{q \in \mathcal{Q}} \ell_q(\hat{y}_q, y)
$$

where $\ell_q(\hat{y}_q, y) = q\,\max(y - \hat{y}_q, 0) + (1-q)\,\max(\hat{y}_q - y, 0)$
is the pinball loss at level $q$, and $y$ is the true log-earnings for the next year.

## Auxiliary feature imputation network

To enable autoregressive multi-horizon forecasting beyond the conditioning window, SAGA employs
a three-layer feed-forward auxiliary network with hidden dimension 128 and ReLU activation.
The network has 312,485 parameters. Its inputs are the running predicted log-earnings trajectory
plus exogenous demographic features (sex, birth cohort, and education level, which are fixed for
each individual). Its outputs are the predicted industry, occupation, region, and employment
indicators for the next forecast year. These auxiliary predictions are fed back into the
categorical subvector for the next step of autoregressive decoding.

The auxiliary network is trained jointly with the main model using cross-entropy loss summed
across the four categorical prediction heads.

## Adaptive Temporal Conformal Prediction

The conformal calibration wrapper implements Theorem 2 (Adaptive Temporal Conformal Prediction).
For each forecast horizon $h$ independently, SAGA computes the nonconformity score for
calibration individual $j$ as the CQR-style score:

$$
s_j = \max\!\bigl(\hat{q}_{\alpha}^{\text{lo}}(\mathbf{x}_j) - y_j,\;
y_j - \hat{q}_{\alpha}^{\text{hi}}(\mathbf{x}_j)\bigr)
$$

where $\hat{q}_{\alpha}^{\text{lo}}$ and $\hat{q}_{\alpha}^{\text{hi}}$ are the predicted
quantile bounds at the chosen nominal level $\alpha$.

The horizon-$h$ calibration set consists of all individuals in calibration cohorts 1980-1982 for
whom a complete $h$-year forecast sequence is available and not right-censored. For $h=10$, this
yields $n_{10} = 14{,}107$ unique calibration individuals.

Theorem 2 states: under exchangeability of augmented conformity scores at fixed horizon $h$ (A1)
and an $L_h$-Lipschitz conditional CDF in a neighborhood of its $(1-\alpha)$ quantile (A2),
with probability at least $1-\delta$ over the calibration draw, the coverage gap satisfies:

$$
\left|P\!\bigl(Y_{i,h} \in C_h(\mathbf{x}_i)\bigr) - (1-\alpha)\right|
\;\leq\;
\frac{1}{n_h+1} + L_h\,\sqrt{\frac{\log(2/\delta)}{2n_h}}
$$

At $h=10$ with $n_{10} = 14{,}107$ and empirical Lipschitz constant $\hat{L}_{10} = 0.65$,
the predicted worst-case deviation is approximately $0.024$, in agreement with the observed
$2.4$ percentage point deficit in income quintile Q1 (87.6% coverage at 90% nominal).

The full proof of Theorem 2 is given in [Appendix E](appendix-e-adaptive-temporal-conformal.md).

## Lifetime Monte Carlo aggregation

Lifetime earnings are estimated by drawing $M = 500$ autoregressive forecast paths per individual,
exponentiating from log to nominal SEK, applying the real discount rate $r = 0.02$ to compute
present values at age 20, and summing over all forecast years from the year after the conditioning
window ends to the last in-panel year on or before age 64. All amounts are in 2022 Swedish krona,
CPI-deflated. Lifetime statistics (mean, median, P10, P90, P99, Gini, top-one-percent share) are
computed from the empirical distribution of path-level lifetime sums.

Full details are in [docs/methodology/lifetime-monte-carlo-aggregation.md](../methodology/lifetime-monte-carlo-aggregation.md).

## See also

- [Methodology: SAGA architecture](../methodology/saga-architecture.md)
- [Methodology: tokenization scheme](../methodology/tokenization-scheme.md)
- [Methodology: training objective](../methodology/training-objective.md)
- [Appendix E: adaptive temporal conformal](appendix-e-adaptive-temporal-conformal.md)
- [Source: src/saga/model/](../../src/saga/model/)
- [Source: src/saga/tokenization/](../../src/saga/tokenization/)
- [Source: src/saga/conformal/](../../src/saga/conformal/)

[xiong2020]: ../bibliography/references.md#xiong2020
[hendrycks2016]: ../bibliography/references.md#hendrycks2016
[huang2016]: ../bibliography/references.md#huang2016
