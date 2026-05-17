"""Static feed-forward baseline (B5): six-layer FFN on the flattened conditioning window.

No temporal structure; the 10-year conditioning window is flattened to a fixed-length
vector and processed by a six-layer feed-forward network.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class StaticFeedForwardBaseline(nn.Module):
    """Six-layer feed-forward network on the flattened conditioning window.

    Args:
        input_dim: Total input dimension (default 2520 = 10 years x 252 pre-projection dims).
        hidden_dim: Hidden layer dimension (default 1024).
        n_quantiles: Number of quantile output heads (default 7).
        dropout: Dropout rate (default 0.1).

    Attributes:
        layers: ModuleList of six linear layers.
        point_head: Linear(hidden_dim, 1).
        quantile_head: Linear(hidden_dim, n_quantiles).
    """

    def __init__(
        self,
        input_dim: int = 2520,
        hidden_dim: int = 1024,
        n_quantiles: int = 7,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        dims = [input_dim] + [hidden_dim] * 5
        self.layers = nn.ModuleList(
            [nn.Linear(dims[i], dims[i + 1]) for i in range(5)]
        )
        self.drop = nn.Dropout(p=dropout)
        self.point_head = nn.Linear(hidden_dim, 1)
        self.quantile_head = nn.Linear(hidden_dim, n_quantiles)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the static feed-forward baseline.

        Args:
            x: Flattened conditioning window of shape (batch, input_dim).

        Returns:
            Tuple of point predictions (batch,) and quantile predictions (batch, n_quantiles).
        """
        h = x
        for layer in self.layers:
            h = self.drop(F.relu(layer(h)))
        point_preds = self.point_head(h).squeeze(-1)
        quantile_preds = self.quantile_head(h)
        return point_preds, quantile_preds
