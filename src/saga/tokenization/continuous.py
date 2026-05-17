"""Continuous subvector encoder for SAGA tokenization.

Projects the 15 standardized continuous features to a 64-dimensional subvector via a
learned linear layer without bias, as described in Section III-A of the manuscript.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class ContinuousSubvectorEncoder(nn.Module):
    """Projects standardized continuous features to the continuous subvector.

    Args:
        n_features: Number of continuous input features (default 15).
        output_dim: Output dimension of the subvector (default 64).

    Attributes:
        projection: Linear layer mapping n_features to output_dim (no bias).
    """

    def __init__(self, n_features: int = 15, output_dim: int = 64) -> None:
        super().__init__()
        self.n_features = n_features
        self.output_dim = output_dim
        self.projection = nn.Linear(n_features, output_dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Project standardized continuous features to the continuous subvector.

        Args:
            x: Tensor of shape (..., n_features) containing standardized continuous features.
               Features must be pre-standardized using year-specific population statistics.

        Returns:
            Tensor of shape (..., output_dim).
        """
        return self.projection(x)  # type: ignore[no-any-return]
