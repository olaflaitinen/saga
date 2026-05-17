"""Combined MSE + pinball training loss for SAGA.

The combined loss is:
    L = 0.5 * MSE(point_pred, target) + sum_{q in Q} pinball_q(quantile_pred_q, target)

where Q = {0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95}.
Right-censored (masked) positions are excluded from the loss.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


_DEFAULT_QUANTILE_LEVELS: tuple[float, ...] = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)


def pinball_loss(
    predicted: torch.Tensor,
    target: torch.Tensor,
    quantile_levels: tuple[float, ...],
    mask: torch.Tensor | None = None,
) -> torch.Tensor:
    """Compute the sum of pinball losses across quantile levels.

    Args:
        predicted: Quantile predictions of shape (batch, seq_len, n_quantiles).
        target: True log-earnings of shape (batch, seq_len).
        quantile_levels: Tuple of n_quantiles quantile levels in (0, 1).
        mask: Boolean tensor of shape (batch, seq_len) where True indicates valid
            (non-masked) positions. If None, all positions are treated as valid.

    Returns:
        Scalar mean pinball loss, summed over quantile levels and averaged over valid positions.
    """
    target_expanded = target.unsqueeze(-1)
    q = torch.tensor(quantile_levels, device=predicted.device, dtype=predicted.dtype)
    errors = target_expanded - predicted
    loss_per_quantile = torch.max(q * errors, (q - 1.0) * errors)

    if mask is not None:
        loss_per_quantile = loss_per_quantile * mask.unsqueeze(-1).float()
        return loss_per_quantile.sum() / (mask.float().sum() * len(quantile_levels) + 1e-8)
    return loss_per_quantile.mean()


def combined_loss(
    point_pred: torch.Tensor,
    quantile_pred: torch.Tensor,
    target: torch.Tensor,
    quantile_levels: tuple[float, ...] = _DEFAULT_QUANTILE_LEVELS,
    mask: torch.Tensor | None = None,
) -> torch.Tensor:
    """Compute the combined MSE + pinball loss used for SAGA training.

    Args:
        point_pred: Point predictions of shape (batch, seq_len).
        quantile_pred: Quantile predictions of shape (batch, seq_len, n_quantiles).
        target: True log-earnings of shape (batch, seq_len).
        quantile_levels: Tuple of quantile levels (default 7 SAGA levels).
        mask: Boolean tensor of shape (batch, seq_len) indicating valid positions.

    Returns:
        Scalar combined loss: 0.5 * mse_loss + pinball_loss.
    """
    if mask is not None:
        valid_count = mask.float().sum() + 1e-8
        mse = (((point_pred - target) ** 2) * mask.float()).sum() / valid_count
    else:
        mse = F.mse_loss(point_pred, target)

    pb = pinball_loss(quantile_pred, target, quantile_levels, mask)
    return 0.5 * mse + pb
