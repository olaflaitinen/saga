"""Probabilistic forecast evaluation metrics.

Implements CRPS, MAE, RMSE, and PICP as defined in the manuscript.
All functions are vectorized over individuals and return scalar aggregate values.

Reference for CRPS: Gneiting, T. and Raftery, A.E. (2007). Strictly proper scoring rules,
prediction, and estimation. Journal of the American Statistical Association, 102(477), 359-378.
"""

from __future__ import annotations

import numpy as np


def crps_quantile(
    quantile_preds: np.ndarray,
    y_true: np.ndarray,
    quantile_levels: tuple[float, ...] = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95),
) -> float:
    """Estimate CRPS from a finite set of quantile forecasts using the pinball approximation.

    Args:
        quantile_preds: Quantile predictions of shape (n, n_quantiles).
        y_true: True outcomes of shape (n,).
        quantile_levels: Tuple of quantile levels corresponding to the last axis of
            quantile_preds.

    Returns:
        Scalar mean CRPS estimate (lower is better).
    """
    q = np.array(quantile_levels)
    errors = y_true[:, None] - quantile_preds
    pinball = np.where(errors >= 0, q * errors, (q - 1.0) * errors)
    return float(2.0 * pinball.mean())


def mae(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """Mean Absolute Error in log SEK.

    Args:
        y_pred: Point predictions of shape (n,).
        y_true: True outcomes of shape (n,).

    Returns:
        Scalar MAE.
    """
    return float(np.abs(y_pred - y_true).mean())


def rmse(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """Root Mean Square Error in log SEK.

    Args:
        y_pred: Point predictions of shape (n,).
        y_true: True outcomes of shape (n,).

    Returns:
        Scalar RMSE.
    """
    return float(np.sqrt(((y_pred - y_true) ** 2).mean()))


def picp(
    lower: np.ndarray,
    upper: np.ndarray,
    y_true: np.ndarray,
) -> float:
    """Prediction Interval Coverage Probability.

    Args:
        lower: Lower bounds of prediction intervals of shape (n,).
        upper: Upper bounds of prediction intervals of shape (n,).
        y_true: True outcomes of shape (n,).

    Returns:
        Scalar PICP in [0, 1].
    """
    return float(((y_true >= lower) & (y_true <= upper)).mean())


def crps_reduction_vs_baseline(
    crps_model: float, crps_baseline: float
) -> float:
    """Compute the CRPS reduction of a model relative to a baseline.

    Args:
        crps_model: CRPS of the model under evaluation.
        crps_baseline: CRPS of the reference baseline.

    Returns:
        Fractional CRPS reduction: (crps_baseline - crps_model) / crps_baseline.

    Examples:
        >>> crps_reduction_vs_baseline(0.318, 0.467)
        0.31906...
    """
    return (crps_baseline - crps_model) / crps_baseline
