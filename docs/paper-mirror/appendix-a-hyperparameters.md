# Appendix A: hyperparameters

This appendix provides the complete hyperparameter inventory for the SAGA model and all
baseline models. All values are mirrored verbatim from the manuscript and are also reflected
in the corresponding YAML configuration files under `configs/`.

## Table of contents

- [SAGA main model (headline)](#saga-main-model-headline)
- [Tokenization subvectors](#tokenization-subvectors)
- [Training schedule](#training-schedule)
- [Auxiliary feature imputation network](#auxiliary-feature-imputation-network)
- [Ablation variants](#ablation-variants)
- [Baseline hyperparameters](#baseline-hyperparameters)
- [See also](#see-also)

## SAGA main model (headline)

Configuration file: `configs/saga_main.yaml`.

| Parameter | Value |
|---|---|
| Total parameters | 10,872,960 |
| Layers $L$ | 6 |
| Attention heads $H$ per layer | 8 |
| Model dimension $d$ | 384 |
| Feed-forward inner dimension | $1536 = 4d$ |
| Maximum context length | 45 yearly tokens |
| Activation | GELU |
| Normalization | pre-LayerNorm |
| Causal attention mask | lower-triangular, applied at every layer |
| Dropout rate (attention and feed-forward) | 0.1 |
| Stochastic depth on residual connections | 0.1 |

Output heads:
- Scalar point head, trained with mean squared error (coefficient $\tfrac{1}{2}$).
- 7-dimensional quantile head, trained with pinball loss.
- Quantile levels: $\mathcal{Q} = \{0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95\}$.

## Tokenization subvectors

| Subvector | Dimension |
|---|---|
| Continuous (15 features projected) | 64 |
| Categorical (10 tables, total) | 76 |
| ... occupation (SSYK2012 three-digit) | 24 |
| ... industry (SNI2007 two-digit) | 16 |
| ... region (21 Swedish counties) | 8 |
| ... highest education level (Sun2000Niva, 4 categories) | 4 |
| ... field of study (Sun2000Inr, one-digit) | 4 |
| ... sex | 4 |
| ... country of birth group (8 categories) | 4 |
| ... marital status | 4 |
| ... number of children | 4 |
| ... age of youngest child bucket | 4 |
| Missingness (16 binary indicators projected) | 16 |
| Age positional embedding | 64 |
| Year positional embedding | 32 |
| Concatenated subvector | $252 = 64+76+16+64+32$ |
| Final projection (linear with bias, 252 to 384) | 384 |

## Training schedule

Configuration file: `configs/saga_main.yaml`.

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Learning rate | $3\times10^{-4}$ |
| Weight decay | $10^{-2}$ |
| $\beta_1$ | $0.9$ |
| $\beta_2$ | $0.999$ |
| Schedule | cosine with 2,000 warmup steps |
| Total optimization steps | 300,000 |
| Per-device batch size | 512 sequences |
| Gradient accumulation steps | 4 |
| Effective batch size | 16,384 |
| Devices | 8 NVIDIA A100 40 GB |
| Precision | bfloat16 accumulating to float32 |
| Seeds | 20260601, 20260602, 20260603, 20260604, 20260605 |
| Single-seed wall clock | 14.8 hours |
| Per-seed accelerator hours | approximately 118 |
| Peak per-device GPU memory | 34.2 GB |
| Early stopping patience | 20 validation checks of 5,000 steps each |
| Early stopping criterion | validation pinball loss on calibration cohorts 1980-1982 |

## Auxiliary feature imputation network

| Parameter | Value |
|---|---|
| Architecture | three-layer feed-forward |
| Hidden dimension | 128 |
| Activation | ReLU |
| Parameter count | 312,485 |
| Inputs | predicted earnings trajectory plus exogenous demographic features |
| Outputs | predicted industry, occupation, region, employment indicators |
| Training loss | cross-entropy summed across categorical heads |

## Ablation variants

| Ablation | Key difference | Config file |
|---|---|---|
| A7 (dim 192) | Model dimension $d=192$, FFN$=768$ | `configs/saga_dim192.yaml` |
| A8 (dim 768) | Model dimension $d=768$, FFN$=3072$ | `configs/saga_dim768.yaml` |

All other ablations (A1-A6, A9-A13) are produced from `configs/saga_main.yaml` with
programmatic modifications described in `src/saga/evaluation/ablation_runner.py`.

## Baseline hyperparameters

| Baseline | Key hyperparameters | Config file |
|---|---|---|
| GKOS | 87 GMM moments, age bins 25-60 in 10-year windows | `configs/gkos_estimation.yaml` |
| AR(1)+FE | Arellano-Bond GMM, first differences | `configs/ar1_estimation.yaml` |
| LightGBM | One regressor per horizon, quantile variants for 7 levels | `configs/gbt_baseline.yaml` |
| LSTM | Two layers, hidden dimension $768$, $10{,}941{,}440$ parameters | `configs/lstm_baseline.yaml` |
| FF | Six layers, flattened 10-year conditioning window | `configs/ff_baseline.yaml` |

## See also

- [Configuration files](../../configs/)
- [Methodology: training objective](../methodology/training-objective.md)
- [Methodology: SAGA architecture](../methodology/saga-architecture.md)
- [Results: ablation study](../results/ablation-study.md)
