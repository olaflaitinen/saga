"""LSTM baseline (B4): two-layer LSTM with parameter-matched capacity.

Two-layer LSTM with hidden dimension 768, parameter count approximately 10,941,440,
matched to SAGA's 10,872,960. Trained with the same combined MSE + pinball loss.

Reference: Hochreiter, S. and Schmidhuber, J. (1997). Long short-term memory.
Neural Computation, 9(8), 1735-1780.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class LSTMBaseline(nn.Module):
    """Two-layer LSTM baseline with point and quantile output heads.

    Args:
        input_dim: Input dimension per timestep (default 252, same as SAGA pre-projection).
        hidden_dim: LSTM hidden dimension (default 768).
        num_layers: Number of LSTM layers (default 2).
        dropout: LSTM inter-layer dropout (default 0.1).
        n_quantiles: Number of quantile output heads (default 7).

    Attributes:
        lstm: Two-layer LSTM module.
        point_head: Linear(hidden_dim, 1) point prediction head.
        quantile_head: Linear(hidden_dim, n_quantiles) quantile head.
    """

    def __init__(
        self,
        input_dim: int = 252,
        hidden_dim: int = 768,
        num_layers: int = 2,
        dropout: float = 0.1,
        n_quantiles: int = 7,
    ) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.point_head = nn.Linear(hidden_dim, 1)
        self.quantile_head = nn.Linear(hidden_dim, n_quantiles)

    def forward(
        self,
        x: torch.Tensor,
        lengths: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the LSTM baseline.

        Args:
            x: Input tensor of shape (batch, seq_len, input_dim).
            lengths: Optional tensor of valid sequence lengths for packing.

        Returns:
            Tuple of point predictions (batch, seq_len) and quantile predictions
            (batch, seq_len, n_quantiles).
        """
        out, _ = self.lstm(x)
        point_preds = self.point_head(out).squeeze(-1)
        quantile_preds = self.quantile_head(out)
        return point_preds, quantile_preds
