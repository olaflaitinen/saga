# Ablation study

**Important:** Results are computed on the test set using real LISA microdata inside the
Statistics Sweden MONA secure compute environment under project SCB-MONA-2026-147.

## Table of contents

- [Ablation results (Table VI)](#ablation-results-table-vi)
- [Key findings](#key-findings)
- [See also](#see-also)

## Ablation results (Table VI)

CRPS at $h=10$ on the test set (cohorts 1983-1985). Headline SAGA CRPS: **0.318**.

| Ablation | Description | CRPS | $\Delta$ | % change |
|---|---|---|---|---|
| **Headline** | SAGA main model | 0.318 | -- | -- |
| A1 | Drop occupation and industry features | 0.334 | $+0.016$ | $+5.0\%$ |
| A2 | Drop family and household features | 0.327 | $+0.009$ | $+2.8\%$ |
| A3 | LSTM with parameter-matched 768 hidden | 0.364 | $+0.046$ | $+14.5\%$ |
| A4 | Feed-forward on flattened 10-year window | 0.493 | $+0.175$ | $+55.0\%$ |
| A5 | Point head only (no quantile head) | 0.347 | $+0.029$ | $+9.1\%$ |
| A6 | Drop year positional embedding | 0.341 | $+0.023$ | $+7.2\%$ |
| A7 | Model dimension $d=192$, FFN$=768$ | 0.328 | $+0.010$ | $+3.1\%$ |
| A8 | Model dimension $d=768$, FFN$=3072$ | 0.319 | $+0.001$ | $+0.3\%$ |
| A9 | Drop missingness subvector | 0.324 | $+0.006$ | $+1.9\%$ |
| A10 | Drop age positional embedding | 0.354 | $+0.036$ | $+11.3\%$ |
| A11 | SAGA backbone, point head only, conformal off | 0.367 | $+0.049$ | $+15.4\%$ |
| A12 | Conformal layer on GKOS backbone | 0.451 | $+0.133$ | $+41.8\%$ |
| A13 | SAGA backbone, GKOS-style mixture output head | 0.332 | $+0.014$ | $+4.4\%$ |

## Key findings

**Architecture (A3, A4, A10):** The most important single component is the transformer
sequence architecture. Replacing the backbone with a parameter-matched LSTM (A3: +14.5%)
or a flattened feed-forward (A4: +55.0%) confirms that temporal attention is essential.
The age positional embedding (A10: +11.3%) is the second most important component, indicating
that SAGA exploits systematic variation in the earnings profile shape across the lifecycle.

**Conformal wrapper (A11, A12):** Removing the conformal wrapper from the full SAGA model
(A11: +15.4%) degrades distributional accuracy substantially. Applying the conformal wrapper
to the GKOS backbone (A12: +41.8% relative to headline) confirms that the conformal layer
alone cannot compensate for a misspecified backbone: good conformal coverage requires
accurate raw quantile estimates.

**Covariates (A1, A2, A9):** Occupation and industry (A1: +5.0%) contribute meaningfully.
Family and household variables (A2: +2.8%) and the missingness vector (A9: +1.9%) provide
smaller but non-negligible improvements.

**Output head design (A5, A13):** A quantile head is better than a point head alone
(A5: +9.1%). The GKOS-style mixture output head (A13: +4.4%) is slightly worse than the
pinball-trained quantile head, confirming that a non-parametric quantile head is preferable
to a parametric mixture.

**Model size (A7, A8):** The headline $d=384$ model is well-calibrated: the smaller $d=192$
variant loses 3.1% CRPS and the larger $d=768$ variant gains only 0.3%, suggesting marginal
returns to scale in the relevant capacity range.

## See also

- [Headline forecast accuracy](headline-forecast-accuracy.md)
- [Robustness checks](robustness-checks.md)
- [Paper mirror: experiments](../paper-mirror/05-experiments.md)
- [Config: configs/saga_dim192.yaml](../../configs/saga_dim192.yaml)
- [Config: configs/saga_dim768.yaml](../../configs/saga_dim768.yaml)
- [Source: src/saga/evaluation/ablation_runner.py](../../src/saga/evaluation/ablation_runner.py)
- [Script: scripts/run_all_ablations.sh](../../scripts/run_all_ablations.sh)
