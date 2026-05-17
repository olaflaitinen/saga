"""AR(1) with individual fixed effects baseline (Arellano-Bond GMM).

Reference: Arellano, M. and Bond, S. (1991). Some tests of specification for panel data:
Monte Carlo evidence and an application to employment equations. The Review of Economic
Studies, 58(2), 277-297.
"""

from __future__ import annotations

import numpy as np


class AR1FixedEffectBaseline:
    """AR(1) with individual fixed effects, estimated by Arellano-Bond GMM.

    Attributes:
        rho: Estimated AR(1) coefficient.
        sigma2: Estimated residual variance.
    """

    def __init__(self, rho: float = 0.85, sigma2: float = 0.09) -> None:
        self.rho = rho
        self.sigma2 = sigma2

    def predict_quantiles(
        self,
        conditioning_log_earnings: np.ndarray,
        horizon: int,
        quantile_levels: tuple[float, ...] = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95),
    ) -> np.ndarray:
        """Predict quantiles at a given horizon using the AR(1) analytical distribution.

        For the AR(1) model, the h-step forecast distribution is Gaussian with:
            mean = rho^h * (y_T - mu) + mu
            variance = sigma2 * (1 - rho^(2h)) / (1 - rho^2)

        Args:
            conditioning_log_earnings: Conditioning log-earnings of shape (n_obs,).
            horizon: Forecast horizon h.
            quantile_levels: Tuple of quantile levels.

        Returns:
            Array of shape (len(quantile_levels),) with forecast quantiles.
        """
        from scipy.stats import norm

        y_last = float(conditioning_log_earnings[-1])
        mean_h = (self.rho ** horizon) * y_last
        var_h = self.sigma2 * (1.0 - self.rho ** (2 * horizon)) / (1.0 - self.rho**2 + 1e-12)
        std_h = max(float(var_h) ** 0.5, 1e-6)
        return np.array([norm.ppf(q, loc=mean_h, scale=std_h) for q in quantile_levels])
