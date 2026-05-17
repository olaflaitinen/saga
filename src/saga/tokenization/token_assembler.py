"""Token assembler for SAGA tokenization.

Concatenates all five subvectors (continuous, categorical, missingness, age, year) and
projects the result to the model dimension d via a learned linear layer with bias.
Input dimension: 64+76+16+64+32 = 252. Output dimension: d (default 384).
"""

from __future__ import annotations

import torch
import torch.nn as nn

from saga.config import SagaConfig
from saga.tokenization.categorical import CategoricalSubvectorEncoder
from saga.tokenization.continuous import ContinuousSubvectorEncoder
from saga.tokenization.missingness import MissingnessSubvectorEncoder
from saga.tokenization.positional import PositionalEncoder


class TokenAssembler(nn.Module):
    """Assembles all five subvectors into a single d-dimensional token.

    Args:
        config: SagaConfig instance with all subvector and model dimension settings.

    Attributes:
        continuous_encoder: ContinuousSubvectorEncoder (15 features -> 64 dims).
        categorical_encoder: CategoricalSubvectorEncoder (10 tables -> 76 dims).
        missingness_encoder: MissingnessSubvectorEncoder (16 indicators -> 16 dims).
        positional_encoder: PositionalEncoder (age 64 dims + year 32 dims).
        projection: Final linear layer (252 -> model_dim, with bias).
    """

    def __init__(self, config: SagaConfig) -> None:
        super().__init__()
        self.continuous_encoder = ContinuousSubvectorEncoder(
            n_features=15,
            output_dim=config.continuous_dim,
        )
        self.categorical_encoder = CategoricalSubvectorEncoder()
        self.missingness_encoder = MissingnessSubvectorEncoder(
            n_indicators=16,
            output_dim=config.missingness_dim,
        )
        self.positional_encoder = PositionalEncoder(
            age_embedding_dim=config.age_embedding_dim,
            year_embedding_dim=config.year_embedding_dim,
            age_min=config.age_min,
            age_max=config.age_max,
            year_min=config.year_min,
            year_max=config.year_max,
        )
        self.projection = nn.Linear(
            config.token_pre_projection_dim,
            config.model_dim,
            bias=True,
        )

    def forward(
        self,
        continuous: torch.Tensor,
        categorical: dict[str, torch.Tensor],
        missingness: torch.Tensor,
        age: torch.Tensor,
        year: torch.Tensor,
    ) -> torch.Tensor:
        """Assemble all subvectors into a d-dimensional token sequence.

        Args:
            continuous: Float tensor of shape (batch, seq_len, 15) with standardized features.
            categorical: Dictionary of integer tensors, each of shape (batch, seq_len).
            missingness: Float binary tensor of shape (batch, seq_len, 16).
            age: Integer tensor of shape (batch, seq_len) with values in [16, 64].
            year: Integer tensor of shape (batch, seq_len) with values in [1990, 2022].

        Returns:
            Token tensor of shape (batch, seq_len, model_dim).
        """
        cont_vec = self.continuous_encoder(continuous)
        cat_vec = self.categorical_encoder(categorical)
        miss_vec = self.missingness_encoder(missingness)
        pos_vec = self.positional_encoder(age, year)

        pre_proj = torch.cat([cont_vec, cat_vec, miss_vec, pos_vec], dim=-1)
        return self.projection(pre_proj)  # type: ignore[no-any-return]
