# Interpretability: attention and integrated gradients

This document describes the attention pattern analysis and integrated gradients interpretation
of the SAGA model. All analyses are conducted on the test set (cohorts 1983-1985).

## Table of contents

- [Attention pattern analysis](#attention-pattern-analysis)
- [Integrated gradients](#integrated-gradients)
- [Limitations of interpretability analysis](#limitations-of-interpretability-analysis)
- [See also](#see-also)

## Attention pattern analysis

Attention patterns are aggregated across the $H=8$ attention heads and $L=6$ transformer layers
on the test set. For a forecast at horizon $h$, the attention weight at position $t$ in the
conditioning window reflects the relative importance of year $t$ for predicting year $t+h$.

Key findings from the attention analysis:

- **Recency bias at short horizons.** At $h=1$, attention is concentrated in the 3 most recent
  conditioning years (the last year receives approximately 40% of average attention weight).
  This reflects the high autocorrelation of annual earnings at short horizons.

- **Long-range attention at long horizons.** At $h=10$ and $h=20$, attention becomes more
  distributed across the full conditioning window, with the most distant year (the first
  conditioning year, approximately 10 years before the forecast origin) receiving non-trivial
  attention weight (approximately 8% on average). This reflects the informational content of
  early career earnings for long-term trajectory prediction.

- **Layer specialization.** Lower transformer layers ($L=1,2$) develop attention patterns
  that track year-over-year earnings changes (first differences). Upper layers ($L=5,6$)
  develop longer-range patterns sensitive to the overall level and trend of the earnings
  trajectory.

The attention aggregator is implemented in `src/saga/interpretability/attention_aggregator.py`.

## Integrated gradients

Integrated gradients ([Sundararajan et al., 2017][sundararajan2017]) are applied to five
representative test individuals: a low-earnings worker with stable employment, a high-earnings
worker with a career interruption, a part-time worker with frequent employment transitions,
a worker with a late-career earnings surge, and a worker with an early-career high followed
by a long-run decline.

Key findings:

- **Age embedding** is consistently one of the top-5 most important input dimensions for
  all five representative individuals, confirming the ablation result A10 (drop age embedding:
  +11.3% CRPS).

- **Occupation code (SSYK2012)** appears as a high-importance feature for the high-earnings
  and stable-employment representative individuals, consistent with the ablation result A1
  (drop occupation and industry: +5.0% CRPS).

- **Year embedding** contributes more to forecasts in calendar years overlapping with the
  2008-2009 financial crisis, consistent with the hypothesis that SAGA learns calendar-year
  effects in earnings dynamics.

The integrated gradients implementation is in `src/saga/interpretability/integrated_gradients.py`.

## Limitations of interpretability analysis

Attention weights are not a reliable measure of feature importance in the mathematical sense:
high attention to a token does not imply that the token causally drives the prediction, because
attention patterns can be distributed or concentrated for reasons unrelated to predictive
relevance. The integrated gradients analysis provides a more principled attribution, but is
sensitive to the choice of baseline (the zero-earnings path is used here) and to the
approximation of the integral via the Gauss-Legendre quadrature with 50 steps.

The five representative individuals are chosen by the analyst for illustrative purposes.
Systematic population-level attribution analysis is a planned future-work direction.

## See also

- [Ablation study](ablation-study.md)
- [Source: src/saga/interpretability/](../../src/saga/interpretability/)
- [Notebook: notebooks/07-interpretability-attention-and-ig.ipynb](../../notebooks/07-interpretability-attention-and-ig.ipynb)

[sundararajan2017]: ../bibliography/references.md#sundararajan2017
