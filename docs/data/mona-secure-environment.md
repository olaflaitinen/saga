# MONA secure compute environment

## Table of contents

- [What is MONA](#what-is-mona)
- [SAGA project details](#saga-project-details)
- [Disclosure-control workflow](#disclosure-control-workflow)
- [Applying for independent MONA access](#applying-for-independent-mona-access)
- [Replication without MONA access](#replication-without-mona-access)
- [See also](#see-also)

## What is MONA

MONA (Microdata Online Access) is the Statistics Sweden secure remote computing environment
that provides approved researchers with access to individual-level administrative register data
under controlled conditions. MONA is operated by Statistics Sweden (Statistiska centralbyran,
SCB) and is the standard platform for research access to Swedish administrative microdata,
including LISA.

Inside MONA, researchers work on SCB-managed servers with access to approved datasets.
No data can be transferred out of the MONA environment directly. All analysis outputs (tables,
figures, model coefficients, trained model weights) must pass through a disclosure-control
review performed by Statistics Sweden before they can be released to the researcher.

## SAGA project details

- **Project reference:** Statistics Sweden MONA project SCB-MONA-2026-147
- **Ethics approval:** Swedish Ethical Review Authority decision 2026-04127-01
- **Project scope:** Probabilistic earnings forecasting and tax-benefit microsimulation using
  LISA register data for birth cohorts 1960-1990, panel years 1990-2022.
- **Data accessed:** LISA register, calendar years 1990-2022, birth cohorts 1960-1990.

All SAGA model training, baseline estimation, conformal calibration, evaluation, and synthetic
data generation were conducted exclusively within the SCB-MONA-2026-147 MONA project environment.
No row-level data, no individual-level predictions, and no intermediate outputs linked to
identifiable individuals left the secure environment.

## Disclosure-control workflow

Before any output was released from the MONA environment, it was reviewed by Statistics Sweden
under their standard disclosure-control procedures. Outputs released include:

- Aggregate performance metrics (MAE, RMSE, CRPS, PICP by horizon and subgroup)
- Lifetime earnings distributional statistics (mean, percentiles, Gini, top shares)
- Tax microsimulation aggregate statistics
- Trained model weights (released after disclosure-control review confirms that the weights do
  not memorize individual records, as evidenced by the membership-inference AUC of 0.512)
- Synthetic mirror dataset (500,000 individuals)

## Applying for independent MONA access

Researchers who wish to replicate the headline results at the bit level must apply independently
to Statistics Sweden for a new MONA project covering the same data. The application process
involves the following steps:

1. Obtain ethics approval from the Swedish Ethical Review Authority (Etikprovningsmyndigheten)
   for the specific research purpose. Applications are submitted at https://etikprovning.se.
2. Submit a data access application to Statistics Sweden including the ethics approval number,
   the specific variables and panel years requested, the analysis plan, and the institutional
   affiliation of the lead researcher.
3. If approved, execute the analysis inside the assigned MONA project environment.
4. Submit all outputs for disclosure-control review before downloading from MONA.

The SAGA project (SCB-MONA-2026-147) is specific to the first author's institutional
affiliation and research purpose; it cannot be accessed by other researchers.

## Replication without MONA access

Pipeline-level replication of the SAGA analysis workflow is possible without MONA access using
the synthetic mirror dataset (500,000 individuals) hosted at Zenodo under DOI `10.5281/zenodo.20260287`.
The synthetic mirror enables:

- Running the full training pipeline on a population with known statistical properties.
- Running conformal calibration and evaluating coverage on the synthetic test split.
- Running lifetime Monte Carlo aggregation and tax microsimulation.
- Executing all notebooks (00 through 07) from start to finish.

The synthetic mirror does not enable bit-level replication of the numerical results in the
manuscript, which are computed on the real LISA microdata.

## See also

- [Data: synthetic mirror](synthetic-mirror.md)
- [Ethics: data governance](../ethics/data-governance.md)
- [Reproducibility: full replication](../reproducibility/full-replication.md)
