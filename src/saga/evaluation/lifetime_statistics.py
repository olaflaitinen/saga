"""Lifetime earnings distributional statistics.

Computes the statistics reported in Table IV of the manuscript:
mean, median, P10, P90, P99, Gini coefficient, and top-1% income share.
"""

from __future__ import annotations

import numpy as np


def gini_coefficient(x: np.ndarray) -> float:
    """Compute the Gini coefficient of a positive distribution.

    Args:
        x: Non-negative array of shape (n,) representing individual lifetime earnings.
            Must have at least 2 elements.

    Returns:
        Gini coefficient in [0, 1].

    Examples:
        >>> gini_coefficient(np.array([1.0, 1.0, 1.0]))
        0.0
    """
    x = np.asarray(x, dtype=float)
    x = x[x >= 0.0]
    if len(x) < 2 or x.sum() == 0:
        return 0.0
    x_sorted = np.sort(x)
    n = len(x_sorted)
    cumsum = np.cumsum(x_sorted)
    return float(2 * (np.arange(1, n + 1) * x_sorted).sum() / (n * cumsum[-1]) - (n + 1) / n)


def top_income_share(x: np.ndarray, percentile: float = 99.0) -> float:
    """Compute the income share of the top (100 - percentile) percent.

    Args:
        x: Non-negative array of shape (n,) with individual lifetime earnings.
        percentile: Threshold percentile (default 99.0 for top-1% share).

    Returns:
        Top income share in [0, 1].

    Examples:
        >>> top_income_share(np.array([1.0, 1.0, 100.0]), percentile=66.0)
        0.980...
    """
    threshold = float(np.percentile(x, percentile))
    total = x.sum()
    if total == 0:
        return 0.0
    return float(x[x > threshold].sum() / total)


def lifetime_distribution_statistics(
    lifetime_earnings: np.ndarray,
) -> dict[str, float]:
    """Compute all Table IV statistics for a distribution of lifetime earnings.

    Args:
        lifetime_earnings: Array of shape (n,) with individual lifetime discounted earnings
            in 2022 Swedish krona.

    Returns:
        Dictionary with keys: mean, median, p10, p90, p99, gini, top1pct_share.
        All monetary values are in the same units as lifetime_earnings (MSEK if divided by 1e6).
    """
    return {
        "mean": float(np.mean(lifetime_earnings)),
        "median": float(np.median(lifetime_earnings)),
        "p10": float(np.percentile(lifetime_earnings, 10)),
        "p90": float(np.percentile(lifetime_earnings, 90)),
        "p99": float(np.percentile(lifetime_earnings, 99)),
        "gini": gini_coefficient(lifetime_earnings),
        "top1pct_share": top_income_share(lifetime_earnings, percentile=99.0),
    }
