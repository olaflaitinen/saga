# LISA register overview

## Table of contents

- [What is LISA](#what-is-lisa)
- [Coverage and linkage](#coverage-and-linkage)
- [Panel years used in SAGA](#panel-years-used-in-saga)
- [Access restrictions](#access-restrictions)
- [See also](#see-also)

## What is LISA

LISA (longitudinell integrationsdatabas for sjukforsakrings- och arbetsmarknadsstudier) is a
longitudinal administrative database maintained by Statistics Sweden (Statistiska centralbyran,
SCB). It was established in 1990 and covers the universe of individuals resident in Sweden at
the end of each calendar year who are aged 16 or older. LISA is updated annually and is the
primary source for longitudinal labor market and social insurance research in Sweden.

## Coverage and linkage

LISA links individual-level records from the following Swedish administrative sources on an
annual basis:

- Tax register (Inkomst- och taxeringsregistret): labor income, capital income, transfer payments.
- Social insurance register: sickness absence, disability, parental leave, unemployment insurance.
- Education register (Utbildningsregistret): highest education level (Sun2000Niva), field of
  study (Sun2000Inr), enrollment status.
- Total population register (Registret over totalbefolkningen, RTB): birth date, sex, marital
  status, country of birth, regional residence (county).
- Business register (foretagsdatabasen): employer identity, industry (SNI2007), size class,
  sector.

The linkage key is the Swedish personal identity number (personnummer), which is a unique
identifier assigned to all Swedish residents at birth or immigration. The personnummer enables
exact, error-free record linkage across all administrative sources.

## Panel years used in SAGA

SAGA uses LISA data for calendar years 1990 to 2022 (33 years). The LISA panel is not publicly
available; access requires an approved project inside the Statistics Sweden MONA secure compute
environment. See [MONA secure environment](mona-secure-environment.md).

- Total panel coverage: 1990-2022
- Birth cohorts used in the core analysis sample: 1960-1985
- Out-of-time holdout cohorts: 1986-1990
- Total individuals in core sample: 2,143,817
- Total person-year observations: 61,284,903
- Share of zero-earnings person-years: 7.4%

## Access restrictions

The LISA register is classified as restricted-access personal data under Swedish law (the
Personal Data Act and the Statistics Act). Access requires:

1. A project-specific ethics approval from the Swedish Ethical Review Authority
   (Etikprovningsmyndigheten). The SAGA project received approval under decision 2026-04127-01.
2. An approved data access agreement with Statistics Sweden for a specific MONA project.
   The SAGA project operated under MONA project SCB-MONA-2026-147.
3. Execution of all data processing inside the MONA secure compute environment, with outputs
   subject to Statistics Sweden's disclosure-control review before release.

No row-level LISA data are included in this repository. The `data/real/` directory contains
documentation only.

## See also

- [Variable inventory](variable-inventory.md)
- [Sample selection rules](sample-selection-rules.md)
- [MONA secure environment](mona-secure-environment.md)
- [Ethics: ethical approval](../ethics/ethical-approval.md)
- [Paper mirror: data](../paper-mirror/04-data.md)
