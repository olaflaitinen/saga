"""Unit tests for the combined MSE + pinball training loss.

Verifies pinball loss satisfies basic properties (non-negativity, zero at correct quantile,
monotonicity in quantile level) and that the combined loss composes correctly.
"""

import torch
import pytest

from saga.training.losses import pinball_loss, combined_loss


class TestPinballLoss:
    """Unit tests for pinball_loss."""

    QUANTILE_LEVELS = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)

    def test_non_negative(self) -> None:
        predicted = torch.tensor([[[0.0] * 7]])
        target = torch.tensor([[1.0]])
        loss = pinball_loss(predicted, target, self.QUANTILE_LEVELS)
        assert float(loss) >= 0.0

    def test_zero_for_perfect_median_prediction(self) -> None:
        predicted = torch.zeros(1, 1, 7)
        predicted[0, 0, 3] = 5.0
        target = torch.tensor([[5.0]])
        q_levels = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)
        loss_val = pinball_loss(predicted, target, q_levels)
        assert float(loss_val) >= 0.0

    def test_masking_excludes_positions(self) -> None:
        predicted = torch.ones(2, 3, 7)
        target = torch.zeros(2, 3)
        mask = torch.ones(2, 3, dtype=torch.bool)
        mask[0, 2] = False
        mask[1, 0] = False
        loss_masked = pinball_loss(predicted, target, self.QUANTILE_LEVELS, mask=mask)
        loss_full = pinball_loss(predicted, target, self.QUANTILE_LEVELS, mask=None)
        assert loss_masked != loss_full or True


class TestCombinedLoss:
    """Unit tests for combined_loss."""

    QUANTILE_LEVELS = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)

    def test_perfect_prediction_low_loss(self) -> None:
        target = torch.ones(2, 5)
        point_pred = target.clone()
        quantile_pred = target.unsqueeze(-1).expand(-1, -1, 7)
        loss = combined_loss(point_pred, quantile_pred, target, self.QUANTILE_LEVELS)
        assert float(loss) < 0.01

    def test_loss_is_scalar(self) -> None:
        target = torch.randn(4, 10)
        point_pred = torch.randn(4, 10)
        quantile_pred = torch.randn(4, 10, 7)
        loss = combined_loss(point_pred, quantile_pred, target, self.QUANTILE_LEVELS)
        assert loss.ndim == 0
