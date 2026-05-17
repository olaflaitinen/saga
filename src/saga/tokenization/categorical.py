"""Categorical subvector encoder for SAGA tokenization.

Maintains 10 separate embedding tables (occupation, industry, region, education level,
field of study, sex, country of birth group, marital status, number of children,
age of youngest child) and concatenates their outputs to the 76-dimensional categorical
subvector, as described in Section III-A of the manuscript.
"""

from __future__ import annotations

import torch
import torch.nn as nn


_EMBEDDING_SPECS: list[tuple[str, int, int]] = [
    ("occupation", 430, 24),
    ("industry", 100, 16),
    ("region", 22, 8),
    ("education_level", 5, 4),
    ("field_of_study", 12, 4),
    ("sex", 3, 4),
    ("country_of_birth_group", 9, 4),
    ("marital_status", 6, 4),
    ("n_children", 5, 4),
    ("age_youngest_child", 6, 4),
]


class CategoricalSubvectorEncoder(nn.Module):
    """Embeds 10 categorical features and concatenates to a 76-dimensional subvector.

    Each categorical feature is embedded by a separate learned lookup table.
    The embeddings are concatenated (not summed) to form the categorical subvector.

    Attributes:
        embeddings: ModuleDict of embedding tables keyed by feature name.
        output_dim: Total concatenated output dimension (76).
    """

    def __init__(self) -> None:
        super().__init__()
        self.embeddings = nn.ModuleDict(
            {
                name: nn.Embedding(vocab_size, embed_dim, padding_idx=0)
                for name, vocab_size, embed_dim in _EMBEDDING_SPECS
            }
        )
        self.output_dim: int = sum(embed_dim for _, _, embed_dim in _EMBEDDING_SPECS)

    def forward(self, features: dict[str, torch.Tensor]) -> torch.Tensor:
        """Embed and concatenate all categorical features.

        Args:
            features: Dictionary mapping feature name to integer-coded index tensor.
                Each tensor has shape (...,) where ... is the leading batch/sequence dimensions.
                Unknown or missing categories should be encoded as index 0 (padding index).

        Returns:
            Tensor of shape (..., output_dim) with all embeddings concatenated.
        """
        parts = [
            self.embeddings[name](features[name])
            for name, _, _ in _EMBEDDING_SPECS
        ]
        return torch.cat(parts, dim=-1)
