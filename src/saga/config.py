"""SagaConfig dataclass holding all model and training hyperparameters.

All default values match the headline SAGA model (Appendix A of the manuscript).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class SagaConfig:
    """Configuration for the SAGA model and training schedule.

    All default values reproduce the headline model from the manuscript.

    Attributes:
        model_dim: Transformer model dimension d (default 384).
        num_layers: Number of transformer decoder layers L (default 6).
        num_heads: Number of attention heads H per layer (default 8).
        ffn_dim: Feed-forward inner dimension (default 1536 = 4 * model_dim).
        max_context_length: Maximum number of yearly tokens per individual (default 45).
        dropout: Dropout rate applied to attention and FFN outputs (default 0.1).
        stochastic_depth_rate: Stochastic depth rate on residual connections (default 0.1).
        quantile_levels: Tuple of quantile levels for the quantile head (default 7 levels).
        continuous_dim: Output dimension of the continuous subvector encoder (default 64).
        categorical_total_dim: Total concatenated categorical embedding dimension (default 76).
        missingness_dim: Output dimension of the missingness subvector (default 16).
        age_embedding_dim: Output dimension of the age positional embedding (default 64).
        year_embedding_dim: Output dimension of the year positional embedding (default 32).
        age_min: Minimum age index for the age embedding table (default 16).
        age_max: Maximum age index for the age embedding table (default 64).
        year_min: Minimum calendar year for the year embedding table (default 1990).
        year_max: Maximum calendar year for the year embedding table (default 2022).
        aux_hidden_dim: Hidden dimension of the auxiliary imputation network (default 128).
        learning_rate: AdamW learning rate (default 3e-4).
        weight_decay: AdamW weight decay (default 1e-2).
        beta1: AdamW beta1 (default 0.9).
        beta2: AdamW beta2 (default 0.999).
        warmup_steps: Number of linear warmup steps (default 2000).
        total_steps: Total optimization steps (default 300000).
        per_device_batch_size: Per-device batch size (default 512).
        gradient_accumulation_steps: Gradient accumulation steps (default 4).
        grad_clip_max_norm: Gradient clipping max norm (default 1.0).
        seed: Random seed (default 20260601).
        early_stopping_patience: Patience in validation checks (default 20).
        validation_interval_steps: Steps between validation checks (default 5000).
    """

    model_dim: int = 384
    num_layers: int = 6
    num_heads: int = 8
    ffn_dim: int = 1536
    max_context_length: int = 45
    dropout: float = 0.1
    stochastic_depth_rate: float = 0.1
    quantile_levels: tuple[float, ...] = field(
        default_factory=lambda: (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)
    )

    continuous_dim: int = 64
    categorical_total_dim: int = 76
    missingness_dim: int = 16
    age_embedding_dim: int = 64
    year_embedding_dim: int = 32

    age_min: int = 16
    age_max: int = 64
    year_min: int = 1990
    year_max: int = 2022

    aux_hidden_dim: int = 128

    learning_rate: float = 3e-4
    weight_decay: float = 1e-2
    beta1: float = 0.9
    beta2: float = 0.999
    warmup_steps: int = 2_000
    total_steps: int = 300_000
    per_device_batch_size: int = 512
    gradient_accumulation_steps: int = 4
    grad_clip_max_norm: float = 1.0

    seed: int = 20260601
    early_stopping_patience: int = 20
    validation_interval_steps: int = 5_000

    @property
    def token_pre_projection_dim(self) -> int:
        """Concatenated subvector dimension before the final linear projection.

        Returns:
            Sum of all subvector dimensions: 64+76+16+64+32 = 252.
        """
        return (
            self.continuous_dim
            + self.categorical_total_dim
            + self.missingness_dim
            + self.age_embedding_dim
            + self.year_embedding_dim
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> "SagaConfig":
        """Load a SagaConfig from a YAML file.

        Args:
            path: Path to the YAML configuration file.

        Returns:
            A SagaConfig instance with values from the YAML file overriding defaults.

        Raises:
            FileNotFoundError: If the specified path does not exist.
            yaml.YAMLError: If the YAML file is malformed.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with path.open() as fh:
            data = yaml.safe_load(fh) or {}
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)
