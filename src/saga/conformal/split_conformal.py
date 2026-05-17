"""Split conformal calibrator implementing Theorem 1.

Uses CQR-style nonconformity scores (max of lower quantile miss and upper quantile miss)
to produce prediction intervals with finite-sample marginal coverage guarantees.
"""

from __future__ import annotations

import numpy as np


class SplitConformalCalibrator:
    """Horizon-specific split conformal calibrator using CQR nonconformity scores.

    Implements Theorem 1 (standard split conformal coverage guarantee).
    For each forecast horizon h, a separate calibration quantile Q_hat_h is fitted
    from the conformity scores of the calibration set at that horizon.

    Attributes:
        alpha: Miscoverage rate (nominal level = 1 - alpha, default 0.10).
        quantile_lower_idx: Index into quantile_levels for the lower bound (default 1: q=0.10).
        quantile_upper_idx: Index into quantile_levels for the upper bound (default 5: q=0.90).
        _calibration_quantiles: Dict mapping horizon h to fitted Q_hat_h.
    """

    def __init__(
        self,
        alpha: float = 0.10,
        quantile_lower_idx: int = 1,
        quantile_upper_idx: int = 5,
    ) -> None:
        self.alpha = alpha
        self.quantile_lower_idx = quantile_lower_idx
        self.quantile_upper_idx = quantile_upper_idx
        self._calibration_quantiles: dict[int, float] = {}

    def calibrate(
        self,
        q_lower: np.ndarray,
        q_upper: np.ndarray,
        y_true: np.ndarray,
        horizon: int,
    ) -> float:
        """Fit the conformity quantile for a specific horizon.

        Args:
            q_lower: Predicted lower quantile bounds of shape (n_cal,).
            q_upper: Predicted upper quantile bounds of shape (n_cal,).
            y_true: True outcomes of shape (n_cal,).
            horizon: Forecast horizon h for which this calibration applies.

        Returns:
            The fitted conformity quantile Q_hat_h (a float).
        """
        scores = np.maximum(q_lower - y_true, y_true - q_upper)
        n = len(scores)
        level = np.ceil((1 - self.alpha) * (n + 1)) / n
        level = float(np.clip(level, 0.0, 1.0))
        q_hat = float(np.quantile(scores, level))
        self._calibration_quantiles[horizon] = q_hat
        return q_hat

    def predict_interval(
        self,
        q_lower: np.ndarray,
        q_upper: np.ndarray,
        horizon: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Produce conformal prediction intervals for a specific horizon.

        Args:
            q_lower: Predicted lower quantile bounds of shape (n,).
            q_upper: Predicted upper quantile bounds of shape (n,).
            horizon: Forecast horizon h for which to apply the calibrated quantile.

        Returns:
            Tuple of (lower_bound, upper_bound), each of shape (n,).

        Raises:
            KeyError: If calibrate has not been called for the given horizon.
        """
        if horizon not in self._calibration_quantiles:
            raise KeyError(f"Horizon {horizon} has not been calibrated. Call calibrate first.")
        q_hat = self._calibration_quantiles[horizon]
        return q_lower - q_hat, q_upper + q_hat

    def coverage_at_horizon(self, horizon: int) -> float | None:
        """Return the fitted conformity quantile for a given horizon, or None if uncalibrated.

        Args:
            horizon: Forecast horizon h.

        Returns:
            The fitted Q_hat_h, or None if not yet calibrated.
        """
        return self._calibration_quantiles.get(horizon)
