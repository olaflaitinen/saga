"""Top-level SagaModel class.

Composes the TokenAssembler, TransformerDecoder, PointHead, and QuantileHead into the
complete SAGA model as described in Section III of the manuscript.

The headline model has 10,872,960 parameters. This count is asserted in the unit test
tests/unit/test_saga_model_forward.py.
"""

from __future__ import annotations

import torch
import torch.nn as nn

from saga.config import SagaConfig
from saga.model.decoder import TransformerDecoder
from saga.model.heads import PointHead, QuantileHead
from saga.tokenization.token_assembler import TokenAssembler


class SagaModel(nn.Module):
    """Complete SAGA model: tokenization + transformer decoder + output heads.

    Args:
        config: SagaConfig instance with all hyperparameters.

    Attributes:
        config: The SagaConfig used to construct this model.
        token_assembler: TokenAssembler (produces d-dimensional tokens).
        decoder: TransformerDecoder (L blocks).
        point_head: PointHead (d -> 1).
        quantile_head: QuantileHead (d -> n_quantiles).
    """

    def __init__(self, config: SagaConfig | None = None) -> None:
        super().__init__()
        self.config = config or SagaConfig()
        self.token_assembler = TokenAssembler(self.config)
        self.decoder = TransformerDecoder(
            num_layers=self.config.num_layers,
            model_dim=self.config.model_dim,
            num_heads=self.config.num_heads,
            ffn_dim=self.config.ffn_dim,
            dropout=self.config.dropout,
            stochastic_depth_rate=self.config.stochastic_depth_rate,
        )
        self.point_head = PointHead(self.config.model_dim)
        self.quantile_head = QuantileHead(self.config.model_dim, len(self.config.quantile_levels))

    def forward(
        self,
        continuous: torch.Tensor,
        categorical: dict[str, torch.Tensor],
        missingness: torch.Tensor,
        age: torch.Tensor,
        year: torch.Tensor,
        key_padding_mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the complete SAGA model.

        Args:
            continuous: Float tensor of shape (batch, seq_len, 15).
            categorical: Dict of integer tensors, each of shape (batch, seq_len).
            missingness: Float binary tensor of shape (batch, seq_len, 16).
            age: Integer tensor of shape (batch, seq_len) with values in [16, 64].
            year: Integer tensor of shape (batch, seq_len) with values in [1990, 2022].
            key_padding_mask: Optional boolean padding mask of shape (batch, seq_len).
                True indicates a padded (ignored) position.

        Returns:
            Tuple of:
                point_preds: Tensor of shape (batch, seq_len) with point predictions
                    (log-earnings for the next year at each position).
                quantile_preds: Tensor of shape (batch, seq_len, n_quantiles) with
                    quantile predictions for the 7 standard quantile levels.
        """
        tokens = self.token_assembler(continuous, categorical, missingness, age, year)
        hidden = self.decoder(tokens, key_padding_mask)
        point_preds = self.point_head(hidden)
        quantile_preds = self.quantile_head(hidden)
        return point_preds, quantile_preds

    def count_parameters(self) -> int:
        """Return the total number of trainable parameters.

        Returns:
            Total trainable parameter count (headline model: 10,872,960).
        """
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
