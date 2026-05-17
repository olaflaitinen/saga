# Training objective

## Table of contents

- [Loss function](#loss-function)
- [Optimization schedule](#optimization-schedule)
- [Early stopping](#early-stopping)
- [Source code](#source-code)
- [See also](#see-also)

## Loss function

The training loss combines a point prediction term and a distributional prediction term:

$$
\mathcal{L}(\theta) = \frac{1}{2}\,\mathrm{MSE}(\hat{y}, y)
+ \sum_{q \in \mathcal{Q}} \ell_q(\hat{y}_q, y)
$$

where:
- $\hat{y}$ is the scalar point head output (predicted log-earnings)
- $y$ is the true log-earnings for the next year
- $\hat{y}_q$ is the $q$-th quantile head output
- $\mathcal{Q} = \{0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95\}$ (seven quantile levels)
- The pinball (check) loss at level $q$ is:
$$\ell_q(\hat{y}_q, y) = q\,\max(y - \hat{y}_q,\,0) + (1-q)\,\max(\hat{y}_q - y,\,0)$$

The loss is summed over all (individual, year) pairs in the batch for which a future observation
is available. Right-censored years (where the individual has no observed future record) are
masked out before the loss computation.

## Optimization schedule

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Learning rate | $3\times10^{-4}$ |
| Weight decay | $10^{-2}$ |
| $\beta_1$ | $0.9$ |
| $\beta_2$ | $0.999$ |
| $\varepsilon$ | $10^{-8}$ |
| Schedule | cosine with linear warmup |
| Warmup steps | 2,000 |
| Total steps | 300,000 |
| Per-device batch size | 512 sequences |
| Gradient accumulation | 4 micro-batches |
| Effective batch size | 16,384 |
| Gradient clipping | max norm $1.0$ |
| Precision | bfloat16 accumulating to float32 |

AdamW follows [Loshchilov and Hutter (2019)][loshchilov2019]. Weight decay is applied only to
weight matrices and not to bias terms, embedding tables, or LayerNorm parameters, following
the standard AdamW convention.

## Early stopping

Early stopping monitors the validation pinball loss on calibration cohorts 1980-1982, evaluated
every 5,000 optimization steps. Training stops when the validation pinball loss does not improve
for 20 consecutive checks (a patience of 100,000 gradient steps). At the stopping point, the
model weights are restored to the checkpoint with the best validation pinball loss.

## Source code

- `src/saga/training/losses.py` - combined MSE + pinball loss
- `src/saga/training/optimizer.py` - AdamW wrapper
- `src/saga/training/scheduler.py` - cosine schedule with warmup
- `src/saga/training/train_loop.py` - training loop with gradient accumulation
- `src/saga/training/eval_loop.py` - validation loop and early stopping

## See also

- [SAGA architecture](saga-architecture.md)
- [Appendix A: hyperparameters](../paper-mirror/appendix-a-hyperparameters.md)
- [Config: configs/saga_main.yaml](../../configs/saga_main.yaml)

[loshchilov2019]: ../bibliography/references.md#loshchilov2019
