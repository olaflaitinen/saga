"""Single transformer decoder block for SAGA.

Implements one block of the SAGA architecture: pre-LayerNorm + causal self-attention +
stochastic depth residual + pre-LayerNorm + feed-forward network + stochastic depth residual.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from saga.model.attention import CausalMultiHeadAttention


class StochasticDepth(nn.Module):
    """Stochastic depth (DropPath) applied to residual connections.

    During training, drops the entire residual branch with probability `drop_prob`.
    During evaluation, always passes through. Follows Huang et al. (2016).

    Args:
        drop_prob: Probability of dropping the residual branch (default 0.1).
    """

    def __init__(self, drop_prob: float = 0.1) -> None:
        super().__init__()
        self.drop_prob = drop_prob

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply stochastic depth.

        Args:
            x: Residual branch tensor of any shape.

        Returns:
            x, potentially zeroed out during training.
        """
        if not self.training or self.drop_prob == 0.0:
            return x
        keep_prob = 1.0 - self.drop_prob
        shape = (x.shape[0],) + (1,) * (x.ndim - 1)
        random_tensor = torch.rand(shape, dtype=x.dtype, device=x.device)
        random_tensor = torch.floor(random_tensor + keep_prob)
        return x * random_tensor / keep_prob


class TransformerBlock(nn.Module):
    """Single transformer decoder block with pre-LayerNorm and stochastic depth.

    Args:
        model_dim: Model dimension d (default 384).
        num_heads: Number of attention heads H (default 8).
        ffn_dim: Feed-forward inner dimension (default 1536).
        dropout: Dropout rate on attention and FFN outputs (default 0.1).
        stochastic_depth_rate: Drop probability for stochastic depth (default 0.1).

    Attributes:
        norm1: LayerNorm before the attention sub-layer.
        attn: CausalMultiHeadAttention.
        attn_drop: Dropout on attention output.
        stoch1: StochasticDepth on the first residual connection.
        norm2: LayerNorm before the FFN sub-layer.
        ffn_fc1: First linear layer of the FFN.
        ffn_fc2: Second linear layer of the FFN.
        ffn_drop: Dropout on FFN output.
        stoch2: StochasticDepth on the second residual connection.
    """

    def __init__(
        self,
        model_dim: int = 384,
        num_heads: int = 8,
        ffn_dim: int = 1536,
        dropout: float = 0.1,
        stochastic_depth_rate: float = 0.1,
    ) -> None:
        super().__init__()
        self.norm1 = nn.LayerNorm(model_dim)
        self.attn = CausalMultiHeadAttention(model_dim, num_heads, dropout)
        self.attn_drop = nn.Dropout(p=dropout)
        self.stoch1 = StochasticDepth(stochastic_depth_rate)

        self.norm2 = nn.LayerNorm(model_dim)
        self.ffn_fc1 = nn.Linear(model_dim, ffn_dim)
        self.ffn_fc2 = nn.Linear(ffn_dim, model_dim)
        self.ffn_drop = nn.Dropout(p=dropout)
        self.stoch2 = StochasticDepth(stochastic_depth_rate)

    def forward(self, x: torch.Tensor, key_padding_mask: torch.Tensor | None = None) -> torch.Tensor:
        """Forward pass through the transformer decoder block.

        Args:
            x: Input tensor of shape (batch, seq_len, model_dim).
            key_padding_mask: Optional boolean padding mask of shape (batch, seq_len).

        Returns:
            Output tensor of shape (batch, seq_len, model_dim).
        """
        attn_out = self.attn_drop(self.attn(self.norm1(x), key_padding_mask))
        x = x + self.stoch1(attn_out)

        ffn_out = self.ffn_fc2(self.ffn_drop(F.gelu(self.ffn_fc1(self.norm2(x)))))
        x = x + self.stoch2(ffn_out)
        return x
