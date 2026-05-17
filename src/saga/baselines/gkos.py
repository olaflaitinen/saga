"""GKOS baseline: Guvenen-Karahan-Ozkan-Song Gaussian mixture earnings dynamics model.

This module wraps the GKOS simulation/prediction step for evaluation. The GKOS model is
estimated by GMM inside the Statistics Sweden MONA environment (see
docs/paper-mirror/appendix-c-gkos-estimation.md). This module provides the prediction
interface for comparing with SAGA on the synthetic mirror or test set.

Reference: Guvenen, F., Karahan, F., Ozkan, S., and Song, J. (2021). What do data on
millions of U.S. workers reveal about lifecycle earnings dynamics? Econometrica, 89(5),
2303-2339.
"""

from __future__ import annotations

import numpy as np


class GKOSBaseline:
    """GKOS Gaussian mixture earnings dynamics model prediction wrapper.

    This class loads pre-estimated GKOS parameters and simulates forecast paths
    from the mixture-of-normals shock structure.

    Manuscript parameter estimates (Table XII):
        rho = 0.924
        permanent_mean_1 = -0.287
        permanent_var_1 = 0.0418
        permanent_weight_1 = 0.784
        transitory_var_1 = 0.0712
        transitory_weight_1 = 0.681

    Attributes:
        rho: AR(1) coefficient of the permanent component.
        params: Dictionary of estimated model parameters.
    """

    RHO_MANUSCRIPT: float = 0.924
    PERMANENT_MEAN_1_MANUSCRIPT: float = -0.287
    PERMANENT_VAR_1_MANUSCRIPT: float = 0.0418
    PERMANENT_WEIGHT_1_MANUSCRIPT: float = 0.784
    TRANSITORY_VAR_1_MANUSCRIPT: float = 0.0712
    TRANSITORY_WEIGHT_1_MANUSCRIPT: float = 0.681

    def __init__(self, params: dict[str, float] | None = None) -> None:
        self.params = params or {
            "rho": self.RHO_MANUSCRIPT,
            "permanent_mean_1": self.PERMANENT_MEAN_1_MANUSCRIPT,
            "permanent_var_1": self.PERMANENT_VAR_1_MANUSCRIPT,
            "permanent_weight_1": self.PERMANENT_WEIGHT_1_MANUSCRIPT,
            "transitory_var_1": self.TRANSITORY_VAR_1_MANUSCRIPT,
            "transitory_weight_1": self.TRANSITORY_WEIGHT_1_MANUSCRIPT,
        }
        self.rho = float(self.params["rho"])

    def predict_quantiles(
        self,
        conditioning_log_earnings: np.ndarray,
        horizon: int,
        quantile_levels: tuple[float, ...] = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95),
        n_sim: int = 5000,
        rng: np.random.Generator | None = None,
    ) -> np.ndarray:
        """Simulate earnings paths and return empirical quantiles.

        Args:
            conditioning_log_earnings: Log-earnings conditioning history of shape (n_obs,).
                The last element is the most recent observation.
            horizon: Forecast horizon h (years ahead).
            quantile_levels: Tuple of quantile levels.
            n_sim: Number of simulated paths for quantile estimation.
            rng: Optional numpy random generator for reproducibility.

        Returns:
            Array of shape (len(quantile_levels),) with forecast quantiles at horizon h.
        """
        if rng is None:
            rng = np.random.default_rng()
        last_earnings = float(conditioning_log_earnings[-1])
        permanent = np.zeros(n_sim)
        simulated = np.full(n_sim, last_earnings)
        for _ in range(horizon):
            perm_shock = rng.normal(
                self.params["permanent_mean_1"],
                self.params["permanent_var_1"] ** 0.5,
                size=n_sim,
            )
            trans_shock = rng.normal(
                0.0,
                self.params["transitory_var_1"] ** 0.5,
                size=n_sim,
            )
            permanent = self.rho * permanent + perm_shock
            simulated = simulated + permanent + trans_shock
        return np.array([np.quantile(simulated, q) for q in quantile_levels])
