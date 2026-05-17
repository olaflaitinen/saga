"""Integrated Gradients attribution for SAGA.

Implements the axiomatic integrated gradients method of Sundararajan et al. (2017) for
attributing SAGA's predictions to individual input features.

Reference: Sundararajan, M., Taly, A., and Yan, Q. (2017). Axiomatic attribution for
deep networks. Proceedings of the 34th ICML, PMLR 70, 3319-3328.
"""

from __future__ import annotations

import numpy as np
import torch

from saga.model.saga_model import SagaModel


class IntegratedGradients:
    """Compute integrated gradients attributions for SAGA's continuous features.

    Args:
        model: Trained SagaModel instance.
        n_steps: Number of Gauss-Legendre quadrature steps (default 50).
        baseline_value: Value used for the baseline (zero-earnings) path (default 0.0).

    Attributes:
        model: The SAGA model.
        n_steps: Number of quadrature steps.
        baseline_value: Baseline value for continuous features.
    """

    def __init__(
        self,
        model: SagaModel,
        n_steps: int = 50,
        baseline_value: float = 0.0,
    ) -> None:
        self.model = model
        self.n_steps = n_steps
        self.baseline_value = baseline_value

    def attribute(
        self,
        continuous: torch.Tensor,
        categorical: dict[str, torch.Tensor],
        missingness: torch.Tensor,
        age: torch.Tensor,
        year: torch.Tensor,
        target_position: int = -1,
    ) -> np.ndarray:
        """Compute integrated gradients for the continuous input features.

        Args:
            continuous: Continuous features of shape (1, seq_len, 15).
            categorical: Categorical features dict with tensors of shape (1, seq_len).
            missingness: Missingness indicators of shape (1, seq_len, 16).
            age: Age tensor of shape (1, seq_len).
            year: Year tensor of shape (1, seq_len).
            target_position: Sequence position whose output is attributed (default -1 for last).

        Returns:
            Attribution array of shape (seq_len, 15) with integrated gradients for each
            continuous feature at each conditioning year.
        """
        baseline = torch.full_like(continuous, self.baseline_value)
        alphas = torch.linspace(0.0, 1.0, self.n_steps)
        grad_sum = torch.zeros_like(continuous)

        for alpha in alphas:
            interp = baseline + alpha * (continuous - baseline)
            interp.requires_grad_(True)
            point_preds, _ = self.model(interp, categorical, missingness, age, year)
            score = point_preds[:, target_position].sum()
            score.backward()
            if interp.grad is not None:
                grad_sum += interp.grad.detach()

        ig = (continuous - baseline) * grad_sum / self.n_steps
        return ig.squeeze(0).numpy()
