# Wall-clock budgets

This document provides expected wall-clock times for each stage of the SAGA analysis pipeline
on the reference hardware (8 x A100 40 GB) and on a single A100 40 GB for pipeline-level
replication.

## Full manuscript reproduction (8 x A100 40 GB)

| Stage | Wall-clock time |
|---|---|
| Data preprocessing (LISA, inside MONA) | 2.1 hours |
| GKOS estimation (CPU, 32 cores) | 18.3 hours |
| AR(1)+FE estimation (CPU, 32 cores) | 1.4 hours |
| LightGBM training (one regressor per horizon per quantile) | 3.7 hours |
| LSTM training (5 seeds) | 11.2 hours |
| FF training (5 seeds) | 4.8 hours |
| SAGA training (5 seeds, 8 x A100) | 74.0 hours (14.8 h/seed x 5) |
| Conformal calibration (all horizons) | 0.4 hours |
| Inference on test set | 1.7 hours |
| Forecast evaluation (all tables) | 0.8 hours |
| All ablations (13 variants) | 38.0 hours |
| All robustness checks | 22.0 hours |
| All placebo tests | 3.1 hours |
| Lifetime Monte Carlo aggregation | 2.2 hours |
| Tax microsimulation | 0.6 hours |
| Interpretability analysis | 1.8 hours |
| Total (sequential) | approximately 186 hours |
| Total (parallel, SAGA training on dedicated nodes) | approximately 80 hours |

## Pipeline-level replication on synthetic mirror (single A100 40 GB, 1 seed)

| Stage | Wall-clock time |
|---|---|
| Download synthetic mirror | 5-15 minutes (network) |
| SAGA training (1 seed, 300,000 steps) | approximately 15 hours |
| SAGA training (1 seed, smoke test 50,000 steps) | approximately 2.5 hours |
| Conformal calibration | 5 minutes |
| Inference and evaluation | 30 minutes |
| Lifetime aggregation | 15 minutes |
| Notebooks 00-07 (full) | approximately 2 hours |
| **Total (full 1-seed)** | approximately 18 hours |
| **Total (smoke test)** | approximately 4 hours |

## See also

- [Hardware notes](hardware-notes.md)
- [Full replication](full-replication.md)
- [Computational cost](../results/computational-cost.md)
