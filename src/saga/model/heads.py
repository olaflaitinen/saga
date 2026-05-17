"""Output heads for SAGA: scalar point head and 7-dimensional quantile head.

The point head is a Linear(d, 1) projection trained with MSE loss (coefficient 0.5).
The quantile head is a Linear(d, 7) projection trained with pinball loss at quantile
levels {0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95}.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class PointHead(nn.Module):
    """Scalar point prediction head.

    Args:
        model_dim: Input dimension (default 384).

    Attributes:
        linear: Linear layer mapping model_dim to 1.
    """

    def __init__(self, model_dim: int = 384) -> None:
        super().__init__()
        self.linear = nn.Linear(model_dim, 1)

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        """Produce scalar point predictions.

        Args:
            hidden: Hidden state tensor of shape (batch, seq_len, model_dim).

        Returns:
            Point predictions of shape (batch, seq_len).
        """
        return self.linear(hidden).squeeze(-1)  # type: ignore[no-any-return]


class QuantileHead(nn.Module):
    """Multi-quantile prediction head.

    Args:
        model_dim: Input dimension (default 384).
        n_quantiles: Number of quantile levels (default 7).

    Attributes:
        linear: Linear layer mapping model_dim to n_quantiles.
        n_quantiles: Number of quantile outputs.
    """

    def __init__(self, model_dim: int = 384, n_quantiles: int = 7) -> None:
        super().__init__()
        self.n_quantiles = n_quantiles
        self.linear = nn.Linear(model_dim, n_quantiles)

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        """Produce multi-quantile predictions.

        Args:
            hidden: Hidden state tensor of shape (batch, seq_len, model_dim).

        Returns:
            Quantile predictions of shape (batch, seq_len, n_quantiles).
        """
        return self.linear(hidden)  # type: ignore[no-any-return]
