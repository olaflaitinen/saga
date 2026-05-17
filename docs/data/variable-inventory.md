# Variable inventory

This document lists all variables used in SAGA, organized by subvector type. All variables
are drawn from the LISA register for calendar years 1990-2022.

## Table of contents

- [15 continuous features](#15-continuous-features)
- [10 categorical features](#10-categorical-features)
- [16 missingness indicators](#16-missingness-indicators)
- [Age and year](#age-and-year)
- [See also](#see-also)

## 15 continuous features

These 15 variables are standardized by year and projected to the 64-dimensional continuous
subvector. All monetary amounts are in real 2022 Swedish krona, CPI-deflated.

| Index | Variable | LISA source | Notes |
|---|---|---|---|
| 1 | Log labor earnings (primary measure) | Tax register | Zero-earnings floored at log(1) = 0 |
| 2 | Log capital income | Tax register | |
| 3 | Log total transfer payments | Social insurance | Sum of all transfers |
| 4 | Log sickness benefit days | Social insurance | Days times daily benefit |
| 5 | Log parental leave days | Social insurance | |
| 6 | Log unemployment benefit days | Social insurance | Days times daily benefit |
| 7 | Log disability pension amount | Social insurance | |
| 8 | Log pension income | Tax register | |
| 9 | Log housing supplement | Social insurance | |
| 10 | Employment rate (weeks employed / 52) | Business register | Fraction, [0, 1] |
| 11 | Log employer earnings (employer-level mean) | Business register | |
| 12 | Log employer size (number of employees) | Business register | |
| 13 | Full-time indicator | Business register | Binary, 0 or 1 |
| 14 | Number of employers in the year | Business register | Count |
| 15 | Log spousal labor earnings (if partnered) | Tax register | 0 if single |

## 10 categorical features

These 10 variables are embedded in separate tables and concatenated to the 76-dimensional
categorical subvector.

| Index | Variable | Classification | Embedding width |
|---|---|---|---|
| 1 | Occupation | SSYK2012 three-digit | 24 |
| 2 | Industry | SNI2007 two-digit | 16 |
| 3 | Region | Swedish county (21 values) | 8 |
| 4 | Highest education level | Sun2000Niva (4 categories) | 4 |
| 5 | Field of study | Sun2000Inr one-digit | 4 |
| 6 | Sex | Binary (female=0, male=1) | 4 |
| 7 | Country of birth group | 8 aggregated groups | 4 |
| 8 | Marital status | Single, married, cohabiting, divorced, widowed | 4 |
| 9 | Number of children under 18 | Bucketed: 0, 1, 2, 3+ | 4 |
| 10 | Age of youngest child | Bucketed: none, infant, preschool, school-age, teen | 4 |

## 16 missingness indicators

A binary indicator for each of the 15 continuous features (indicating whether the feature
value is observed or imputed) plus one global missingness flag (indicating whether any feature
is missing). This 16-dimensional binary vector is projected to the 16-dimensional missingness
subvector.

## Age and year

- Integer age in [16, 64]: embedded to 64 dimensions via a learned lookup table.
- Integer calendar year in [1990, 2022]: embedded to 32 dimensions via a learned lookup table.

## See also

- [LISA register overview](lisa-register-overview.md)
- [Tokenization scheme](../methodology/tokenization-scheme.md)
- [Schema: data/schema.yaml](../../data/schema.yaml)
- [Source: src/saga/data/schema.py](../../src/saga/data/schema.py)
