"""Attention weight aggregator for SAGA interpretability analysis.

Aggregates multi-head attention weights across layers and heads to produce an
attention heatmap over the conditioning window for each individual.
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import torch
import torch.nn as nn

from saga.model.saga_model import SagaModel


class AttentionAggregator:
    """Extracts and aggregates attention weights from all layers and heads.

    Args:
        model: Trained SagaModel instance.
        aggregation: Aggregation method across heads ('mean' or 'max', default 'mean').

    Attributes:
        model: The SAGA model.
        aggregation: Head aggregation method.
        _hooks: List of registered forward hooks.
        _attention_weights: Captured attention weights per layer.
    """

    def __init__(self, model: SagaModel, aggregation: str = "mean") -> None:
        if aggregation not in ("mean", "max"):
            raise ValueError(f"aggregation must be 'mean' or 'max', got '{aggregation}'.")
        self.model = model
        self.aggregation = aggregation
        self._hooks: list[torch.utils.hooks.RemovableHandle] = []
        self._attention_weights: list[torch.Tensor] = []

    def _make_hook(self) -> Callable[[nn.Module, tuple[torch.Tensor, ...], torch.Tensor], None]:
        def hook(
            module: nn.Module, input: tuple[torch.Tensor, ...], output: torch.Tensor
        ) -> None:
            self._attention_weights.append(output.detach().cpu())

        return hook

    def aggregate(
        self,
        continuous: torch.Tensor,
        categorical: dict[str, torch.Tensor],
        missingness: torch.Tensor,
        age: torch.Tensor,
        year: torch.Tensor,
    ) -> np.ndarray:
        """Run a forward pass and return aggregated attention weights.

        Args:
            continuous: Continuous features tensor.
            categorical: Categorical features dict.
            missingness: Missingness indicators tensor.
            age: Age tensor.
            year: Year tensor.

        Returns:
            Attention weight array of shape (batch, seq_len, seq_len), averaged
            across all layers and heads.
        """
        self._attention_weights.clear()
        with torch.no_grad():
            _ = self.model(continuous, categorical, missingness, age, year)
        if not self._attention_weights:
            raise RuntimeError(
                "No attention weights captured. Register hooks before calling aggregate()."
            )
        stacked = torch.stack(self._attention_weights, dim=0)
        aggregated = stacked.mean(dim=0) if self.aggregation == "mean" else stacked.amax(dim=0)
        return aggregated.numpy()
