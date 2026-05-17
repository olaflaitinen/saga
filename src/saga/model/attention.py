"""Multi-head causal self-attention module for SAGA.

Implements the causally-masked multi-head self-attention sub-layer used in each
transformer decoder block. The causal mask is lower-triangular, applied at every layer
to prevent any token from attending to future tokens in the conditioning window.
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class CausalMultiHeadAttention(nn.Module):
    """Causally-masked multi-head self-attention.

    Args:
        model_dim: Model dimension d (default 384).
        num_heads: Number of attention heads H (default 8).
        dropout: Dropout rate on attention weights (default 0.1).

    Attributes:
        qkv_proj: Linear layer projecting d to 3d for Q, K, V.
        out_proj: Linear layer projecting d back to d.
        dropout: Dropout applied to attention weights.
        head_dim: Dimension per head (model_dim // num_heads).
        scale: Scaling factor 1/sqrt(head_dim).
    """

    def __init__(
        self,
        model_dim: int = 384,
        num_heads: int = 8,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        assert model_dim % num_heads == 0, (
            f"model_dim {model_dim} must be divisible by num_heads {num_heads}"
        )
        self.model_dim = model_dim
        self.num_heads = num_heads
        self.head_dim = model_dim // num_heads
        self.scale = math.sqrt(self.head_dim) ** -1

        self.qkv_proj = nn.Linear(model_dim, 3 * model_dim, bias=True)
        self.out_proj = nn.Linear(model_dim, model_dim, bias=True)
        self.attn_dropout = nn.Dropout(p=dropout)

    def forward(self, x: torch.Tensor, key_padding_mask: torch.Tensor | None = None) -> torch.Tensor:
        """Compute causally-masked multi-head self-attention.

        Args:
            x: Input tensor of shape (batch, seq_len, model_dim).
            key_padding_mask: Optional boolean tensor of shape (batch, seq_len) where True
                indicates that the corresponding position should be masked (padded). Used to
                mask out padding tokens at the end of short sequences.

        Returns:
            Output tensor of shape (batch, seq_len, model_dim).
        """
        B, T, C = x.shape
        qkv = self.qkv_proj(x).reshape(B, T, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)

        causal_mask = torch.ones(T, T, device=x.device, dtype=torch.bool).triu(1)

        attn_bias: torch.Tensor | None = None
        if key_padding_mask is not None:
            padding_bias = key_padding_mask[:, None, None, :].float() * -1e9
            attn_bias = padding_bias

        attn_logits = torch.matmul(q, k.transpose(-2, -1)) * self.scale
        attn_logits = attn_logits.masked_fill(causal_mask, float("-inf"))
        if attn_bias is not None:
            attn_logits = attn_logits + attn_bias

        attn_weights = F.softmax(attn_logits, dim=-1)
        attn_weights = self.attn_dropout(attn_weights)

        out = torch.matmul(attn_weights, v)
        out = out.transpose(1, 2).contiguous().reshape(B, T, C)
        return self.out_proj(out)
