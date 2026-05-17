# Placebo and falsification tests

**Important:** Results are computed using real LISA microdata inside the Statistics Sweden
MONA secure compute environment under project SCB-MONA-2026-147.

## Table of contents

- [Placebo results (Table IX)](#placebo-results-table-ix)
- [Interpretation](#interpretation)
- [See also](#see-also)

## Placebo results (Table IX)

| Test | Value | Target | Interpretation |
|---|---|---|---|
| Permutation placebo CRPS ratio (placebo / headline) | 2.14 | Much greater than 1 | Signal is not spurious |
| Short-history placebo CRPS reduction vs. GKOS (5-year window) | 18.3% | Below 31.9% headline | Value of long history confirmed |
| Static feature-only placebo CRPS at $h=10$ | 0.623 | Far above 0.318 headline | Value of sequence confirmed |

## Interpretation

**Permutation placebo (CRPS ratio 2.14).** In the permutation placebo, the earnings history of
each test individual is randomly permuted before forecasting, destroying the temporal structure
of the conditioning window. The CRPS ratio of the permuted model to the headline model is $2.14$, confirming that SAGA's accuracy derives from the genuine temporal structure of earnings histories
and is not a spurious artifact of the training procedure.

**Short-history placebo (18.3% CRPS reduction).** In the short-history placebo, the conditioning
window is reduced from 10 years to 5 years. The CRPS reduction versus GKOS falls from the
headline $31.9\%$ to $18.3\%$, confirming that the longer conditioning window provides
substantial additional information for multi-horizon forecasting. The 5-year conditioning
advantage ($18.3\%$) is non-trivial, indicating that even with a shorter history, the SAGA
transformer extracts more signal than the GKOS parametric model.

**Static feature-only placebo (CRPS 0.623).** In the static feature-only placebo, the temporal
earnings history is removed entirely and the model receives only the time-invariant demographic
and educational baseline features (sex, birth cohort, education level, region of birth). The CRPS of $0.623$ is nearly twice the headline $0.318$, confirming that the earnings history
is the dominant source of predictive information and that the time-invariant features alone are
insufficient for accurate multi-horizon earnings forecasting.

## See also

- [Headline forecast accuracy](headline-forecast-accuracy.md)
- [Ablation study](ablation-study.md)
- [Source: src/saga/evaluation/robustness_runner.py](../../src/saga/evaluation/robustness_runner.py)
- [Script: scripts/run_all_placebos.sh](../../scripts/run_all_placebos.sh)
