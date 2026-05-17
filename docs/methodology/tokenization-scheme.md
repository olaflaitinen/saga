# Tokenization scheme

## Table of contents

- [Overview](#overview)
- [Subvector dimensions](#subvector-dimensions)
- [Continuous subvector](#continuous-subvector)
- [Categorical subvector](#categorical-subvector)
- [Missingness subvector](#missingness-subvector)
- [Positional embeddings](#positional-embeddings)
- [Concatenation and projection](#concatenation-and-projection)
- [Source code](#source-code)
- [See also](#see-also)

## Overview

Each yearly administrative record for individual $i$ at age $t$ is tokenized by projecting five
independently constructed subvectors into a single $384$-dimensional token. The five subvectors
encode: (1) continuous earnings and labor market features, (2) categorical labor market
identifiers, (3) missingness patterns, (4) age, and (5) calendar year.

## Subvector dimensions

| Subvector | Raw input | Dimension |
|---|---|---|
| Continuous | 15 features | 64 |
| Categorical | 10 embedding tables | 76 |
| Missingness | 16 binary indicators | 16 |
| Age positional | integer age $[16, 64]$ | 64 |
| Year positional | integer year $[1990, 2022]$ | 32 |
| Concatenated | -- | 252 |
| Final projection | $252 \to 384$, linear with bias | 384 |

Total concatenated dimension: $64 + 76 + 16 + 64 + 32 = 252$.

## Continuous subvector

The 15 continuous features are standardized using year-specific means and standard deviations
computed on the training cohorts. The standardized features are projected to 64 dimensions via
a learned linear layer without bias. The 15 features are enumerated in
[docs/data/variable-inventory.md](../data/variable-inventory.md).

## Categorical subvector

Ten categorical embedding tables with the following widths (total: 76 dimensions):

| Feature | Vocabulary | Embedding width |
|---|---|---|
| Occupation (SSYK2012 three-digit) | ~400 codes | 24 |
| Industry (SNI2007 two-digit) | ~90 codes | 16 |
| Region (21 Swedish counties) | 21 | 8 |
| Highest education level (Sun2000Niva) | 4 categories | 4 |
| Field of study (Sun2000Inr one-digit) | ~10 codes | 4 |
| Sex | 2 categories | 4 |
| Country of birth group | 8 categories | 4 |
| Marital status | ~5 categories | 4 |
| Number of children | bucketed | 4 |
| Age of youngest child | bucketed | 4 |

Total: $24 + 16 + 8 + 4 + 4 + 4 + 4 + 4 + 4 + 4 = 76$.

The embeddings from all 10 tables are concatenated (not summed) to form the categorical
subvector.

## Missingness subvector

A 16-dimensional binary indicator vector is projected to 16 dimensions via a learned linear
layer. The 16 binary inputs are: one indicator per continuous feature (15 indicators) plus one
global missingness flag. This allows the transformer to distinguish true zero earnings from
imputed or missing values.

## Positional embeddings

**Age embedding (64 dimensions):** A learned embedding table indexed by integer age in the
range $[16, 64]$, producing a $64$-dimensional vector per token.

**Year embedding (32 dimensions):** A learned embedding table indexed by integer calendar year
in the range $[1990, 2022]$, producing a $32$-dimensional vector per token.

Both embeddings are learned from scratch (not sinusoidal), following the empirical observation
that learned positional embeddings perform better than sinusoidal ones in the tabular data
setting.

## Concatenation and projection

The five subvectors are concatenated along the feature dimension to produce a $252$-dimensional
pre-token vector. A single linear layer with bias maps $252$ dimensions to $384$ (the model
dimension $d$), producing the final token that is passed to the transformer decoder stack.

## Source code

- `src/saga/tokenization/continuous.py` - ContinuousSubvectorEncoder
- `src/saga/tokenization/categorical.py` - CategoricalSubvectorEncoder
- `src/saga/tokenization/missingness.py` - MissingnessSubvectorEncoder
- `src/saga/tokenization/positional.py` - PositionalEncoder (age and year)
- `src/saga/tokenization/token_assembler.py` - TokenAssembler (concatenation + projection)

## See also

- [SAGA architecture](saga-architecture.md)
- [Data: variable inventory](../data/variable-inventory.md)
- [Appendix A: hyperparameters](../paper-mirror/appendix-a-hyperparameters.md)
