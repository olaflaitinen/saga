"""Diebold-Mariano test for equal predictive accuracy.

Implements the DM test with Newey-West HAC standard errors at a specified lag truncation,
as described in Appendix B of the manuscript.

Reference: Diebold, F.X. and Mariano, R.S. (1995). Comparing predictive accuracy.
Journal of Business and Economic Statistics, 13(3), 253-263.

Newey-West: Newey, W.K. and West, K.D. (1987). A simple, positive semi-definite,
heteroskedasticity and autocorrelation consistent covariance matrix. Econometrica, 55(3),
703-708.
"""

from __future__ import annotations

import numpy as np


def newey_west_variance(d: np.ndarray, lag: int) -> float:
    """Compute the Newey-West HAC variance of the sample mean of d.

    Args:
        d: Loss differential time series of shape (n,).
        lag: Lag truncation for the HAC kernel (default 5 in the manuscript).

    Returns:
        HAC variance estimate of the sample mean.
    """
    n = len(d)
    d_demeaned = d - d.mean()
    gamma_0 = float((d_demeaned**2).mean())
    nw_var = gamma_0
    for j in range(1, lag + 1):
        gamma_j = float((d_demeaned[j:] * d_demeaned[:-j]).mean())
        nw_var += 2.0 * (1.0 - j / (lag + 1)) * gamma_j
    return nw_var / n


class DieboldMarianoTest:
    """Diebold-Mariano test for equal predictive accuracy.

    Args:
        lag: Newey-West HAC lag truncation (default 5, as used in the manuscript).

    Attributes:
        lag: The HAC lag truncation.
    """

    def __init__(self, lag: int = 5) -> None:
        self.lag = lag

    def test(
        self,
        loss_model: np.ndarray,
        loss_baseline: np.ndarray,
    ) -> tuple[float, float]:
        """Compute the DM test statistic and two-sided p-value.

        A positive statistic indicates that the model is more accurate (lower loss) than
        the baseline.

        Args:
            loss_model: Per-individual loss for the model under evaluation, shape (n,).
            loss_baseline: Per-individual loss for the baseline, shape (n,).

        Returns:
            Tuple of (dm_statistic, two_sided_p_value).
        """
        from scipy.stats import norm  # type: ignore

        d = loss_baseline - loss_model
        d_bar = d.mean()
        nw_var = newey_west_variance(d, self.lag)
        dm_stat = d_bar / (nw_var**0.5 + 1e-12)
        p_value = float(2.0 * norm.sf(abs(dm_stat)))
        return float(dm_stat), p_value
