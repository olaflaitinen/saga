"""Positional encoders for age and calendar year in SAGA tokenization.

Provides learned embedding tables for integer age (range 16-64, 64 dimensions) and integer
calendar year (range 1990-2022, 32 dimensions), as described in Section III-A of the manuscript.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class PositionalEncoder(nn.Module):
    """Provides learned age and year positional embeddings.

    Args:
        age_embedding_dim: Output dimension for the age embedding (default 64).
        year_embedding_dim: Output dimension for the year embedding (default 32).
        age_min: Minimum age offset for the embedding table (default 16).
        age_max: Maximum age offset for the embedding table (default 64).
        year_min: Minimum calendar year offset for the embedding table (default 1990).
        year_max: Maximum calendar year offset for the embedding table (default 2022).

    Attributes:
        age_embedding: Embedding table of size (age_max - age_min + 1, age_embedding_dim).
        year_embedding: Embedding table of size (year_max - year_min + 1, year_embedding_dim).
        output_dim: Total dimension: age_embedding_dim + year_embedding_dim.
    """

    def __init__(
        self,
        age_embedding_dim: int = 64,
        year_embedding_dim: int = 32,
        age_min: int = 16,
        age_max: int = 64,
        year_min: int = 1990,
        year_max: int = 2022,
    ) -> None:
        super().__init__()
        self.age_min = age_min
        self.year_min = year_min
        self.age_embedding_dim = age_embedding_dim
        self.year_embedding_dim = year_embedding_dim
        self.output_dim = age_embedding_dim + year_embedding_dim

        n_ages = age_max - age_min + 1
        n_years = year_max - year_min + 1

        self.age_embedding = nn.Embedding(n_ages, age_embedding_dim)
        self.year_embedding = nn.Embedding(n_years, year_embedding_dim)

    def forward(self, age: torch.Tensor, year: torch.Tensor) -> torch.Tensor:
        """Embed age and year and concatenate to positional subvector.

        Args:
            age: Integer tensor of shape (...) with values in [age_min, age_max].
            year: Integer tensor of shape (...) with values in [year_min, year_max].

        Returns:
            Tensor of shape (..., output_dim) with age and year embeddings concatenated.
        """
        age_idx = age - self.age_min
        year_idx = year - self.year_min
        return torch.cat([self.age_embedding(age_idx), self.year_embedding(year_idx)], dim=-1)
