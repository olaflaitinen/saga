"""Missingness subvector encoder for SAGA tokenization.

Projects a 16-dimensional binary missingness indicator vector (15 per-feature indicators plus
one global flag) to a 16-dimensional subvector via a learned linear layer, as described in
Section III-A of the manuscript.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class MissingnessSubvectorEncoder(nn.Module):
    """Projects binary missingness indicators to the missingness subvector.

    Args:
        n_indicators: Number of binary missingness indicators (default 16:
            15 per-continuous-feature indicators plus 1 global flag).
        output_dim: Output dimension of the subvector (default 16).

    Attributes:
        projection: Linear layer mapping n_indicators to output_dim (with bias).
    """

    def __init__(self, n_indicators: int = 16, output_dim: int = 16) -> None:
        super().__init__()
        self.n_indicators = n_indicators
        self.output_dim = output_dim
        self.projection = nn.Linear(n_indicators, output_dim, bias=True)

    def forward(self, mask: torch.Tensor) -> torch.Tensor:
        """Project binary missingness indicators to the missingness subvector.

        Args:
            mask: Binary float tensor of shape (..., n_indicators) where 1.0 indicates
                that the corresponding continuous feature is missing or imputed, and 0.0
                indicates that it is observed.

        Returns:
            Tensor of shape (..., output_dim).
        """
        return self.projection(mask)  # type: ignore[no-any-return]
