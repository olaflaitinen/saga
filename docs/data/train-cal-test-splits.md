# Train, calibration, and test splits

## Split design

The core analysis sample is divided into four non-overlapping splits, partitioned by birth
cohort. No random stratification is used; the partition is deterministic given birth year.

| Split | Cohorts | Individuals | Role |
|---|---|---|---|
| Train | 1960-1979 (twenty cohorts) | 1,834,201 | SAGA and baseline model training |
| Calibration | 1980-1982 (three cohorts) | 168,542 | Conformal calibration; early stopping |
| Test | 1983-1985 (three cohorts) | 141,074 | All reported results |
| Out-of-time holdout | 1986-1990 (five cohorts) | 287,391 | Robustness check R7 only |

The calibration split serves two distinct roles:

1. **Early stopping criterion:** The validation pinball loss is evaluated on all calibration
   cohort individuals every 5,000 training steps. Training stops when this metric does not
   improve for 20 consecutive checks.

2. **Conformal calibration:** For each forecast horizon $h$, the subset of calibration individuals
   with a non-censored observed outcome at horizon $h$ is used to fit the conformal quantile
   $\hat{Q}_h$. For $h=10$, this yields $n_{10} = 14{,}107$ unique calibration individuals.

## Cohort-based split rationale

The cohort-based (rather than individual-based random) split is designed to prevent information
leakage between the splits. In a random individual-level split, older cohort members in the
calibration or test set might share correlated earnings shocks (common macro shocks, industry
shocks, regional shocks) with training set members of the same cohort. The cohort-based split
ensures that no member of any cohort appears in more than one split, preventing this form of
leakage.

## Out-of-time holdout details

The out-of-time holdout (cohorts 1986-1990, 287,391 individuals) is used exclusively for
robustness check R7 in Table VII. For the $h=10$ evaluation, the effective sample is restricted
to cohorts 1986-1988, because cohorts 1989-1990 do not have 10 forecast years available within
the 2022 LISA panel end. The effective $n$ for the $h=10$ R7 evaluation is $168{,}734$.

## Source code

- `src/saga/data/splits.py` - deterministic cohort-based split utility

## See also

- [Sample selection rules](sample-selection-rules.md)
- [MONA secure environment](mona-secure-environment.md)
- [Paper mirror: data](../paper-mirror/04-data.md)
