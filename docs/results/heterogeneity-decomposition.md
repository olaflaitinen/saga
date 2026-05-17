# Heterogeneity decomposition

**Important:** Results are computed on the test set using real LISA microdata inside the
Statistics Sweden MONA secure compute environment under project SCB-MONA-2026-147.

## Table of contents

- [Subgroup CRPS reductions (Table VIII)](#subgroup-crps-reductions-table-viii)
- [Interpretation](#interpretation)
- [See also](#see-also)

## Subgroup CRPS reductions (Table VIII)

CRPS reduction versus GKOS at $h=10$ by demographic subgroup. Test set (cohorts 1983-1985).

| Subgroup | n | CRPS reduction vs. GKOS (%) |
|---|---|---|
| Male | 891,432 | 29.7 |
| Female | 1,252,385 | 34.8 |
| Compulsory education | 312,847 | 41.2 |
| Upper secondary | 894,213 | 31.4 |
| Short tertiary | 487,621 | 28.3 |
| Long tertiary | 449,136 | 24.7 |
| Stable employer | 867,334 | 24.1 |
| Four or more employer changes | 312,143 | 47.3 |
| Income Q1 | 428,763 | 44.7 |
| Income Q5 | 428,819 | 22.8 |
| Stockholm | 412,834 | 27.1 |
| Gothenburg | 198,437 | 29.4 |
| Malmo | 143,216 | 30.8 |
| Other urban | 673,418 | 32.7 |
| Rural | 715,912 | 36.3 |

Note: subgroup sample sizes are from the core analysis sample (train + calibration + test),
not from the test set alone. Subgroups are not mutually exclusive (e.g., a rural female worker
in income Q1 appears in the female, rural, and Q1 subgroups simultaneously).

## Interpretation

SAGA's advantage over GKOS is largest in the subgroups with the most complex and heterogeneous
earnings trajectories. The highest gains are observed in:

- **Four or more employer changes (47.3%):** High job mobility creates highly non-linear
  earnings paths that GKOS's parametric structure cannot capture.
- **Income Q1 (44.7%):** Low-income individuals have trajectories that are sensitive to
  unemployment spells, disability, and program entry/exit, all of which are captured by
  SAGA's covariate-rich tokenization.
- **Compulsory education only (41.2%):** Workers with low formal education have the most
  volatile trajectories and benefit most from SAGA's non-parametric distributional modeling.
- **Female (34.8% vs. male 29.7%):** The larger female advantage likely reflects SAGA's
  ability to model part-time transitions and parental leave patterns that are more common
  among women in the Swedish labor market and are not adequately captured by GKOS.

The smallest gains are in high-income, highly educated, stable-employment subgroups (income
Q5: 22.8%, long tertiary: 24.7%, stable employer: 24.1%), where earnings trajectories are
more predictable and the parametric GKOS structure is adequate.

## See also

- [Headline forecast accuracy](headline-forecast-accuracy.md)
- [Robustness checks](robustness-checks.md)
- [Source: src/saga/evaluation/heterogeneity_runner.py](../../src/saga/evaluation/heterogeneity_runner.py)
- [Script: scripts/run_inference.sh](../../scripts/run_inference.sh)
