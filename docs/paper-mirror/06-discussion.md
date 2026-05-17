# Discussion

## Table of contents

- [Interpretation of headline results](#interpretation-of-headline-results)
- [Conformal coverage and subgroup equity](#conformal-coverage-and-subgroup-equity)
- [Lifetime earnings and distributional accuracy](#lifetime-earnings-and-distributional-accuracy)
- [Tax microsimulation fidelity](#tax-microsimulation-fidelity)
- [Ablation insights](#ablation-insights)
- [Robustness and generalizability](#robustness-and-generalizability)
- [Limitations](#limitations)
- [See also](#see-also)

## Interpretation of headline results

The 31.9% CRPS reduction at $h=10$ and 41.2% at $h=20$ versus GKOS reflect two complementary
advantages of SAGA over the parametric benchmark. First, SAGA directly learns the conditional
distribution of earnings given the full labor market history of each individual, without
imposing the parametric mixture-of-normals structure of GKOS. Second, SAGA exploits the
high-dimensional covariate information encoded in the categorical subvector (occupation at
three-digit SSYK2012, industry at two-digit SNI2007, region, education) that is outside the
scope of the GKOS GMM estimation framework.

The advantage grows with forecast horizon, from 16.0% at $h=1$ to 41.2% at $h=20$ (in CRPS).
This pattern is consistent with the interpretation that the GKOS parametric structure is
adequate for short-horizon extrapolation but diverges from the data at long horizons where
earnings trajectories fan out non-Gaussianly across the income distribution.

The PICP of 90.3% at the 90% nominal level (versus 84.7% for LSTM, 82.1% for GBT, 86.3%
for GKOS, 81.4% for AR(1), and 79.8% for FF) confirms that only SAGA achieves nominal
coverage, because only SAGA is equipped with the conformal calibration wrapper. The other
models produce miscalibrated prediction intervals because their implicit distributional
assumptions (normality for GKOS and AR(1), isotonic regression for GBT, no explicit
calibration for LSTM and FF) do not match the empirical distribution of the test cohorts.

## Conformal coverage and subgroup equity

The worst-case subgroup coverage deficit of 2.4 percentage points (Q1 income quintile: 87.6%)
is in precise quantitative agreement with the bound derived from Theorem 2 at $n_{10} = 14{,}107$
and $\hat{L}_{10} = 0.65$. This provides an empirical validation of the theorem's coverage-deviation
bound in a large-scale real-data setting.

The Q1 deficit reflects the fact that individuals in the lowest income quintile have the
most dispersed and heterogeneous earnings trajectories, making the conformity score distribution
at fixed h more variable for this subgroup than for the marginal population. The per-subgroup
coverage figures in Table III of the manuscript are reproduced in
[docs/results/calibration-coverage.md](../results/calibration-coverage.md).

## Lifetime earnings and distributional accuracy

SAGA's lifetime Gini of 0.327 is much closer to the observed partial-truth Gini of 0.341 than
GKOS (0.378) or AR(1) (0.396). The key source of GKOS's overestimation of lifetime earnings
inequality is the GKOS model's tendency to generate excessively large positive shocks at the
right tail of the income distribution, as reflected in the P99 lifetime earnings of 47.13 MSEK
for GKOS versus 38.42 MSEK for SAGA and 39.71 MSEK for the observed partial truth. The
non-parametric approach of SAGA avoids this tail overestimation by learning the empirical
quantile function directly.

## Tax microsimulation fidelity

The SAGA mean lifetime effective average tax rate of 30.1% is within 0.5 percentage points of
the partial-observed truth of 30.6%, compared to 29.4% for GKOS and 28.8% for AR(1). The
improvement in the P99 AETR (42.7% for SAGA vs. 43.4% observed, vs. 46.8% for GKOS) directly
reflects the tail earnings accuracy discussed above.

## Ablation insights

The most important single component is the sequence architecture: replacing the transformer
backbone with the parameter-matched LSTM (A3, +14.5% CRPS) or the flattened feed-forward
(A4, +55.0% CRPS) demonstrates that temporal structure and attention are essential for
multi-horizon earnings forecasting. The conformal layer is independently valuable: removing it
from the full SAGA model (A11, +15.4% CRPS) degrades the distributional accuracy substantially,
and applying it to the GKOS backbone (A12, +41.8% relative to headline) confirms that the
conformal layer alone cannot recover the distributional accuracy lost by using a misspecified
backbone.

## Robustness and generalizability

The CRPS reduction is robust to training cohort restriction (R1: 30.8%), sex subsamples
(R2 male: 29.7%), deflation choice (R6: 32.2%), out-of-time evaluation (R7: 28.4%), and
recession-year test folds (R9: 28.8%). The largest reduction is in the stable employer
subsample (R3: 24.1%) and the PSID-feature-portability ablation (R8: 21.4%), both of which
are expected: stable employers have less information variance in their trajectories (reducing
the advantage of the full covariate set), and the PSID inventory restriction removes the most
informative categorical features.

## Limitations

The principal limitation of SAGA is data access: training on the protected LISA microdata
requires MONA project approval from Statistics Sweden. External researchers cannot replicate
the headline numerical results without independent MONA access. The synthetic mirror addresses
pipeline reproducibility but not bit-level replication.

A second limitation is that the conformal guarantee of Theorem 2 is marginal, not conditional
on all covariates simultaneously. The Q1 deficit of $2.4$ percentage points is the worst-case
among the subgroups reported in Table III, but further disaggregation would likely reveal larger
deficits for more granular subpopulations.

A third limitation is the potential for structural change: the model is trained on cohorts
1960-1979 and evaluated on cohorts 1983-1985. The out-of-time holdout (R7) provides one check,
but the model has not been evaluated on post-2022 earnings or on cohorts entering the labor
market after 2022. Periodic retraining is listed as a planned future-work direction in
[docs/roadmap.md](../roadmap.md).

## See also

- [Results: headline forecast accuracy](../results/headline-forecast-accuracy.md)
- [Results: calibration coverage](../results/calibration-coverage.md)
- [Results: ablation study](../results/ablation-study.md)
- [Results: robustness checks](../results/robustness-checks.md)
- [Conclusion](07-conclusion.md)
