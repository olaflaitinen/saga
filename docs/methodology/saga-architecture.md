# SAGA architecture

## Table of contents

- [Overview](#overview)
- [Architecture parameters](#architecture-parameters)
- [Transformer decoder block](#transformer-decoder-block)
- [Parameter count](#parameter-count)
- [Source code](#source-code)
- [See also](#see-also)

## Overview

SAGA is a causally-masked autoregressive transformer decoder. Each individual's administrative
earnings record is tokenized into a sequence of up to 45 yearly tokens (one per year of
observed history, spanning ages 16 to 60). The $384$-dimensional token sequence is processed
left to right through $L=6$ transformer decoder layers with causal attention masking, and the
final hidden state at the last observed year is used to produce point and quantile forecasts
for all future years via iterative autoregressive decoding.

## Architecture parameters

| Parameter | Value |
|---|---|
| Total parameters | 10,872,960 |
| Layers $L$ | 6 |
| Attention heads $H$ | 8 |
| Head dimension $d_k$ | $48 = d/H = 384/8$ |
| Model dimension $d$ | 384 |
| Feed-forward inner dimension | $1536 = 4d$ |
| Maximum context length | 45 yearly tokens |
| Activation | GELU |
| Normalization | pre-LayerNorm |
| Causal attention mask | lower-triangular |
| Dropout rate | 0.1 |
| Stochastic depth rate | 0.1 |

The parameter count of $10{,}872{,}960$ is asserted in the unit test
`tests/unit/test_saga_model_forward.py` so that any drift is caught immediately.

## Transformer decoder block

Each of the $6$ transformer decoder blocks consists of:

1. LayerNorm (pre-norm, applied before the attention sub-layer)
2. Multi-head causal self-attention with $H=8$ heads
3. Dropout (rate $0.1$) on attention output
4. Stochastic depth (rate $0.1$) applied to the residual connection
5. Residual add
6. LayerNorm (pre-norm, applied before the feed-forward sub-layer)
7. Feed-forward network: $\text{Linear}(384, 1536)$, GELU, $\text{Linear}(1536, 384)$
8. Dropout (rate $0.1$) on feed-forward output
9. Stochastic depth (rate $0.1$) applied to the residual connection
10. Residual add

Pre-LayerNorm ordering follows [Xiong et al. (2020)][xiong2020], which improves training
stability compared to the post-norm transformer of [Vaswani et al. (2017)][vaswani2017].
GELU activation follows [Hendrycks and Gimpel (2016)][hendrycks2016]. Stochastic depth
follows [Huang et al. (2016)][huang2016].

## Parameter count

The $10{,}872{,}960$ parameter total decomposes approximately as:

- Tokenization (ContinuousSubvectorEncoder, CategoricalSubvectorEncoder, MissingnessSubvectorEncoder,
  PositionalEncoder, TokenAssembler): approximately 600,000 parameters
- 6 transformer decoder blocks (attention, FFN, LayerNorms): approximately $9{,}960{,}960$ parameters
- Output heads (point head: $384\to1$, quantile head: $384\to7$): approximately $3{,}000$ parameters
- Auxiliary imputation network: $312{,}485$ parameters (separately counted)

## Source code

- `src/saga/model/saga_model.py` - top-level SagaModel class
- `src/saga/model/transformer_block.py` - single transformer decoder block
- `src/saga/model/attention.py` - multi-head causal self-attention
- `src/saga/model/decoder.py` - stack of 6 blocks
- `src/saga/model/heads.py` - point head and quantile head
- `src/saga/config.py` - SagaConfig dataclass with all default parameters

## See also

- [Tokenization scheme](tokenization-scheme.md)
- [Training objective](training-objective.md)
- [Appendix A: hyperparameters](../paper-mirror/appendix-a-hyperparameters.md)
- [Config: configs/saga_main.yaml](../../configs/saga_main.yaml)

[xiong2020]: ../bibliography/references.md#xiong2020
[vaswani2017]: ../bibliography/references.md#vaswani2017
[hendrycks2016]: ../bibliography/references.md#hendrycks2016
[huang2016]: ../bibliography/references.md#huang2016
