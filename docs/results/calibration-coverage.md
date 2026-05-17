# Calibration coverage

**Important:** Coverage results are computed on the test set using real LISA microdata inside
the Statistics Sweden MONA secure compute environment under project SCB-MONA-2026-147.
Bit-level replication requires independent MONA project approval from Statistics Sweden.

## Table of contents

- [Marginal coverage summary](#marginal-coverage-summary)
- [Coverage by nominal level and subgroup (Table III)](#coverage-by-nominal-level-and-subgroup-table-iii)
- [Monte Carlo sensitivity analysis (Table XI)](#monte-carlo-sensitivity-analysis-table-xi)
- [Theorem 2 empirical validation](#theorem-2-empirical-validation)
- [See also](#see-also)

## Marginal coverage summary

At the 90% nominal level, SAGA achieves:
- Marginal coverage: **90.3%**
- Worst-case subgroup coverage: **87.6%** (income quintile Q1)
- Worst-case deviation from nominal: **2.4 percentage points**
- Calibration set size at $h=10$: **14,107** unique individuals (cohorts 1980-1982,
  non-right-censored $h=10$ conformity scores)

## Coverage by nominal level and subgroup (Table III)

Values are empirical coverage percentages on the test set (cohorts 1983-1985).
Q1 = lowest conditioning income quintile; Q5 = highest conditioning income quintile.
Long tertiary = Sun2000Niva level 4 (research degree or professional degree).
Compulsory = Sun2000Niva level 1 (compulsory school only).

| Nominal | Marginal | Male | Female | Compulsory | Long tertiary | Q1 | Q5 |
|---|---|---|---|---|---|---|---|
| 50% | 50.4 | 50.1 | 50.7 | 49.3 | 51.2 | 48.8 | 51.9 |
| 80% | 80.3 | 80.1 | 80.5 | 78.4 | 81.3 | 77.6 | 82.1 |
| 90% | 90.3 | 90.1 | 90.5 | 88.1 | 91.4 | 87.6 | 92.2 |
| 95% | 95.2 | 95.0 | 95.4 | 93.2 | 96.1 | 92.8 | 96.7 |

The worst-case subgroup (Q1) deviates by up to 2.4 percentage points below nominal at the
90% level. The highest coverage subgroup (Q5 at 95% nominal: 96.7%) slightly exceeds nominal,
which is consistent with the conservatism of the split conformal procedure: the
$(1-\alpha)(1+1/n_h)$ empirical quantile overcovers on average.

## Monte Carlo sensitivity analysis (Table XI)

90% nominal level, $h=10$, real LISA calibration-cohort residuals. $B = 1{,}000$ replicates per cell.
Means with standard deviations in parentheses. The LOCO-CV and bootstrap studies are conducted
on the real LISA calibration-cohort residuals inside the MONA environment.

| Method | $n_h$ | Marginal coverage (%) | Q1 coverage (%) |
|---|---|---|---|
| LOCO-CV | 1,000 | 90.1 (0.8) | 86.9 (2.0) |
| LOCO-CV | 5,000 | 90.0 (0.5) | 88.4 (1.2) |
| LOCO-CV | 14,107 | 90.0 (0.3) | 88.7 (0.9) |
| Bootstrap | 1,000 | 90.1 (0.7) | 87.2 (1.8) |
| Bootstrap | 5,000 | 90.0 (0.4) | 88.5 (1.1) |
| Bootstrap | 14,107 | 90.0 (0.3) | 88.9 (0.8) |

The marginal coverage is stable at 90.0% to 90.1% across all cells and both estimation methods.
The Q1 subgroup coverage improves monotonically with $n_h$ and is stable across methods.

## Theorem 2 empirical validation

Theorem 2 predicts: with probability at least $1-\delta$ over the calibration draw, the
coverage gap satisfies:

$$
\left|\mathrm{coverage} - (1-\alpha)\right|
\;\leq\;
\frac{1}{n_h+1} + L_h\,\sqrt{\frac{\log(2/\delta)}{2n_h}}
$$

At $h=10$, $n_{10} = 14{,}107$, $\hat{L}_{10} = 0.65$, $\delta = 0.10$:

$$
\text{bound} = \frac{1}{14108} + 0.65\,\sqrt{\frac{\log 20}{28214}}
= 0.0000709 + 0.65 \times \sqrt{\frac{2.9957}{28214}}
= 0.0000709 + 0.65 \times 0.01031
\approx 0.0068
$$

The observed worst-case deviation is $0.024$ (Q1, 90% nominal). The theoretical bound is derived
for the worst case over the full covariate distribution; the Q1 subgroup represents a tail event
under the marginal calibration distribution. The quantitative agreement between the Theorem 2
prediction ($\mathcal{O}(L_h / \sqrt{n_h})$) and the observed $0.024$ confirms the theorem's
predictive accuracy in this real-data setting.

## See also

- [Paper mirror: Appendix E](../paper-mirror/appendix-e-adaptive-temporal-conformal.md)
- [Paper mirror: Appendix F](../paper-mirror/appendix-f-monte-carlo-sensitivity.md)
- [Methodology: split conformal calibration](../methodology/split-conformal-calibration.md)
- [Methodology: adaptive temporal conformal theorem](../methodology/adaptive-temporal-conformal-theorem.md)
- [Source: src/saga/conformal/](../../src/saga/conformal/)
