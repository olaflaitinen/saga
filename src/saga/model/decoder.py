"""Transformer decoder stack for SAGA.

Stacks L TransformerBlock instances to produce the full decoder.
"""

from __future__ import annotations

import torch
import torch.nn as nn

from saga.model.transformer_block import TransformerBlock


class TransformerDecoder(nn.Module):
    """Stack of L transformer decoder blocks.

    Args:
        num_layers: Number of TransformerBlock layers L (default 6).
        model_dim: Model dimension d (default 384).
        num_heads: Number of attention heads H (default 8).
        ffn_dim: FFN inner dimension (default 1536).
        dropout: Dropout rate (default 0.1).
        stochastic_depth_rate: Stochastic depth rate (default 0.1).

    Attributes:
        blocks: ModuleList of TransformerBlock instances.
        final_norm: LayerNorm applied after the last block.
    """

    def __init__(
        self,
        num_layers: int = 6,
        model_dim: int = 384,
        num_heads: int = 8,
        ffn_dim: int = 1536,
        dropout: float = 0.1,
        stochastic_depth_rate: float = 0.1,
    ) -> None:
        super().__init__()
        self.blocks = nn.ModuleList(
            [
                TransformerBlock(model_dim, num_heads, ffn_dim, dropout, stochastic_depth_rate)
                for _ in range(num_layers)
            ]
        )
        self.final_norm = nn.LayerNorm(model_dim)

    def forward(
        self, x: torch.Tensor, key_padding_mask: torch.Tensor | None = None
    ) -> torch.Tensor:
        """Pass token sequence through all decoder blocks.

        Args:
            x: Input tensor of shape (batch, seq_len, model_dim).
            key_padding_mask: Optional boolean padding mask of shape (batch, seq_len).

        Returns:
            Output tensor of shape (batch, seq_len, model_dim) after final LayerNorm.
        """
        for block in self.blocks:
            x = block(x, key_padding_mask)
        return self.final_norm(x)  # type: ignore[no-any-return]
