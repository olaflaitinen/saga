# Split conformal calibration (Theorem 1)

## Table of contents

- [Overview](#overview)
- [Theorem 1 statement](#theorem-1-statement)
- [SAGA implementation](#saga-implementation)
- [Source code](#source-code)
- [See also](#see-also)

## Overview

Split conformal prediction ([Vovk et al., 2005][vovk2005full]; [Lei et al., 2018][lei2018full];
[Angelopoulos and Bates, 2023][angelopoulos2023full]) wraps any regression model with a
distribution-free marginal coverage guarantee, using a held-out calibration set to compute the
nonconformity quantile. SAGA uses conformalized quantile regression (CQR;
[Romano et al., 2019][romano2019]) as the nonconformity score, adapted to the panel data setting
by stratifying on forecast horizon $h$.

## Theorem 1 statement

Let $\mathcal{S}_{\mathrm{cal}}$ be a calibration set of $n$ individuals with observed outcomes
$Y_j$ and conditioning information $\mathbf{x}_j$. For each $j$, define the nonconformity score:

$$
s_j = \max\!\bigl(\hat{q}_{\alpha}^{\text{lo}}(\mathbf{x}_j) - Y_j,\;
Y_j - \hat{q}_{\alpha}^{\text{hi}}(\mathbf{x}_j)\bigr)
$$

where $\hat{q}_{\alpha}^{\text{lo}}$ and $\hat{q}_{\alpha}^{\text{hi}}$ are the predicted lower
and upper quantile bounds at the chosen nominal coverage level $(1-\alpha)$.

Let $\hat{Q} = \lceil(1-\alpha)(n+1)\rceil$-th order statistic of $\{s_1, \ldots, s_n\}$.
Then for any new individual $i$ with outcome $Y_i$ and conditioning information $\mathbf{x}_i$
exchangeable with the calibration set:

$$
P\!\bigl(Y_i \in C(\mathbf{x}_i)\bigr) \;\geq\; 1 - \alpha
$$

where $C(\mathbf{x}_i) = \bigl\{y : \max(\hat{q}_{\alpha}^{\text{lo}}(\mathbf{x}_i) - y,\;
y - \hat{q}_{\alpha}^{\text{hi}}(\mathbf{x}_i)) \leq \hat{Q}\bigr\}$.

This guarantee holds in finite samples, without any distributional assumptions on $Y_i \mid \mathbf{x}_i$,
provided that the augmented sequence $(s_1, \ldots, s_n, s_{n+1})$ is exchangeable.

## SAGA implementation

SAGA stratifies the conformal calibration by forecast horizon $h$, fitting a separate conformity
quantile $\hat{Q}_h$ for each $h$ independently. This horizon stratification, combined with the
Lipschitz continuity assumption A2, yields the stronger per-horizon coverage guarantee stated
in Theorem 2 (see [Adaptive Temporal Conformal theorem](adaptive-temporal-conformal-theorem.md)).

The calibration set for each horizon $h$ is the subset of cohorts 1980-1982 with a non-censored
observed outcome at horizon $h$. For $h=10$, this yields $n_{10} = 14{,}107$ individuals.

## Source code

- `src/saga/conformal/split_conformal.py` - SplitConformalCalibrator class
- `src/saga/conformal/coverage_diagnostics.py` - marginal and conditional coverage evaluation

## See also

- [Adaptive Temporal Conformal theorem](adaptive-temporal-conformal-theorem.md)
- [Results: calibration coverage](../results/calibration-coverage.md)
- [Appendix E](../paper-mirror/appendix-e-adaptive-temporal-conformal.md)

[vovk2005full]: ../bibliography/references.md#vovk2005full
[lei2018full]: ../bibliography/references.md#lei2018full
[angelopoulos2023full]: ../bibliography/references.md#angelopoulos2023full
[romano2019]: ../bibliography/references.md#romano2019
