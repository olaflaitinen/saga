# Ethical approval

## Approval details

| Attribute | Value |
|---|---|
| Issuing authority | Swedish Ethical Review Authority (Etikprovningsmyndigheten) |
| Decision reference | 2026-04127-01 |
| Decision date | 2026-02-14 |
| Principal investigator | Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov |
| Host institution | Department of Economics, Stockholm University |
| Project title | Probabilistic Forecasting and Microsimulation of Individual Earnings Trajectories Using Swedish Administrative Register Data |
| Data project | Statistics Sweden MONA project SCB-MONA-2026-147 |

## Scope of the ethics approval

The ethics approval covers the following activities:

1. Access to the Swedish LISA register (longitudinell integrationsdatabas) for birth cohorts
   1960-1990, panel years 1990-2022, within the Statistics Sweden MONA secure compute
   environment under project SCB-MONA-2026-147.

2. Training a probabilistic machine learning model (SAGA) on LISA data for the purpose of
   individual earnings trajectory forecasting.

3. Applying the trained model to produce aggregate distributional statistics and synthetic
   microdata for research dissemination.

4. Releasing a synthetic mirror dataset that does not contain any real individual's record
   after passing Statistics Sweden's disclosure-control review.

5. Publishing aggregate model outputs (table values, figure data, trained model weights) that
   have passed Statistics Sweden's disclosure-control review.

## Conditions of the approval

The ethics approval was granted subject to the following conditions:

- All data processing must occur within the Statistics Sweden MONA secure compute environment.
- No row-level data or individual-level predictions may leave the MONA environment.
- All outputs must pass Statistics Sweden's standard disclosure-control review before release.
- The synthetic mirror must pass a privacy audit (membership inference AUC not significantly
  above 0.5) before release.
- Research findings may be published in academic form (journal article, preprint, conference
  paper) without individual-level information.
- The project must not be used for commercial purposes or to inform decisions about specific
  individuals.

## See also

- [Data governance](data-governance.md)
- [Broader impact](broader-impact.md)
- [Dual-use statement](dual-use-statement.md)
- [Data: MONA secure environment](../data/mona-secure-environment.md)
