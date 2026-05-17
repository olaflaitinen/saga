"""Adaptive Temporal Conformal Calibrator implementing Theorem 2.

Provides horizon-stratified split conformal calibration with a finite-sample bound on the
worst-case subgroup coverage deviation as a function of n_h and L_h (Theorem 2).

Reference values from the manuscript (h=10):
    n_10 = 14,107 unique calibration individuals
    L_10_hat = 0.65
    Predicted worst-case deviation: approximately 0.024
    Observed worst-case deviation (Q1, 90% nominal): 0.024
"""

from __future__ import annotations

import math

import numpy as np

from saga.conformal.split_conformal import SplitConformalCalibrator


class AdaptiveTemporalConformalCalibrator(SplitConformalCalibrator):
    """Horizon-stratified split conformal calibrator with Theorem 2 coverage bound.

    Extends SplitConformalCalibrator by providing the Theorem 2 worst-case deviation bound
    for any calibrated horizon.

    Args:
        alpha: Miscoverage rate (default 0.10 for 90% nominal).
        quantile_lower_idx: Index of the lower quantile level (default 1: q=0.10).
        quantile_upper_idx: Index of the upper quantile level (default 5: q=0.90).
        lipschitz_constants: Optional dict mapping horizon h to empirical L_h estimate.
            Defaults to the manuscript value {10: 0.65} if not provided.
    """

    _MANUSCRIPT_LIPSCHITZ: dict[int, float] = {10: 0.65}

    def __init__(
        self,
        alpha: float = 0.10,
        quantile_lower_idx: int = 1,
        quantile_upper_idx: int = 5,
        lipschitz_constants: dict[int, float] | None = None,
    ) -> None:
        super().__init__(alpha, quantile_lower_idx, quantile_upper_idx)
        self._lipschitz = lipschitz_constants or dict(self._MANUSCRIPT_LIPSCHITZ)
        self._calibration_sizes: dict[int, int] = {}

    def calibrate(
        self,
        q_lower: np.ndarray,
        q_upper: np.ndarray,
        y_true: np.ndarray,
        horizon: int,
    ) -> float:
        """Fit the conformity quantile for a specific horizon and record calibration size.

        Args:
            q_lower: Predicted lower quantile bounds of shape (n_cal,).
            q_upper: Predicted upper quantile bounds of shape (n_cal,).
            y_true: True outcomes of shape (n_cal,).
            horizon: Forecast horizon h.

        Returns:
            The fitted conformity quantile Q_hat_h.
        """
        self._calibration_sizes[horizon] = len(y_true)
        return super().calibrate(q_lower, q_upper, y_true, horizon)

    def theorem2_bound(self, horizon: int, delta: float = 0.10) -> float:
        """Compute the Theorem 2 worst-case coverage deviation bound.

        The bound is:
            1 / (n_h + 1) + L_h * sqrt(log(2 / delta) / (2 * n_h))

        Args:
            horizon: Forecast horizon h for which to compute the bound.
            delta: Probability level for the concentration inequality (default 0.10).

        Returns:
            The Theorem 2 upper bound on worst-case coverage deviation.

        Raises:
            KeyError: If horizon has not been calibrated.
            ValueError: If L_h is not available for the given horizon.
        """
        if horizon not in self._calibration_sizes:
            raise KeyError(f"Horizon {horizon} has not been calibrated.")
        if horizon not in self._lipschitz:
            raise ValueError(
                f"Lipschitz constant not available for horizon {horizon}. "
                f"Provide lipschitz_constants at construction time."
            )
        n_h = self._calibration_sizes[horizon]
        l_h = self._lipschitz[horizon]
        finite_sample_term = 1.0 / (n_h + 1)
        concentration_term = l_h * math.sqrt(math.log(2.0 / delta) / (2.0 * n_h))
        return finite_sample_term + concentration_term
