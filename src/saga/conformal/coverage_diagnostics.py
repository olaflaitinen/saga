"""Coverage diagnostic utilities for conformal prediction evaluation.

Computes marginal and conditional coverage rates for comparison with the results in
Tables II and III of the manuscript.
"""

from __future__ import annotations

import numpy as np


def marginal_coverage(
    y_true: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
) -> float:
    """Compute marginal coverage rate.

    Args:
        y_true: True outcomes of shape (n,).
        lower: Lower bounds of prediction intervals of shape (n,).
        upper: Upper bounds of prediction intervals of shape (n,).

    Returns:
        Empirical coverage fraction in [0, 1].
    """
    covered = (y_true >= lower) & (y_true <= upper)
    return float(covered.mean())


def conditional_coverage(
    y_true: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
    subgroup_mask: np.ndarray,
) -> float:
    """Compute conditional coverage rate for a specific subgroup.

    Args:
        y_true: True outcomes of shape (n,).
        lower: Lower bounds of shape (n,).
        upper: Upper bounds of shape (n,).
        subgroup_mask: Boolean array of shape (n,) selecting the subgroup.

    Returns:
        Empirical coverage fraction within the subgroup, in [0, 1].

    Raises:
        ValueError: If the subgroup mask selects no individuals.
    """
    n_sub = subgroup_mask.sum()
    if n_sub == 0:
        raise ValueError("subgroup_mask selects no individuals.")
    covered = (y_true[subgroup_mask] >= lower[subgroup_mask]) & (
        y_true[subgroup_mask] <= upper[subgroup_mask]
    )
    return float(covered.mean())
