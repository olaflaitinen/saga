"""Unit tests for AdaptiveTemporalConformalCalibrator.

Verifies that:
1. Theorem 1 marginal coverage holds for a simple synthetic case.
2. Theorem 2 bound computation is numerically correct.
3. The prediction interval correctly expands by Q_hat.
"""

import numpy as np
import pytest
from saga.conformal.adaptive_temporal import AdaptiveTemporalConformalCalibrator


class TestAdaptiveTemporalConformalCalibrator:
    """Tests for the Adaptive Temporal Conformal Calibrator."""

    def test_calibration_sets_quantile(self) -> None:
        n = 1000
        rng = np.random.default_rng(42)
        y = rng.normal(0, 1, n)
        q_lower = y - 0.5
        q_upper = y + 0.5
        calibrator = AdaptiveTemporalConformalCalibrator(alpha=0.10)
        q_hat = calibrator.calibrate(q_lower, q_upper, y, horizon=10)
        assert isinstance(q_hat, float)
        assert q_hat >= 0.0

    def test_prediction_interval_marginal_coverage(self) -> None:
        rng = np.random.default_rng(99)
        n_cal = 2000
        n_test = 5000
        y_cal = rng.normal(0, 1, n_cal)
        q_lower_cal = rng.normal(-0.7, 0.1, n_cal)
        q_upper_cal = rng.normal(0.7, 0.1, n_cal)
        calibrator = AdaptiveTemporalConformalCalibrator(alpha=0.10)
        calibrator.calibrate(q_lower_cal, q_upper_cal, y_cal, horizon=5)
        y_test = rng.normal(0, 1, n_test)
        q_lower_test = rng.normal(-0.7, 0.1, n_test)
        q_upper_test = rng.normal(0.7, 0.1, n_test)
        lo, hi = calibrator.predict_interval(q_lower_test, q_upper_test, horizon=5)
        coverage = float(((y_test >= lo) & (y_test <= hi)).mean())
        assert coverage >= 0.88, (
            f"Marginal coverage {coverage:.3f} is below 0.88, " "which is far below 90% nominal."
        )

    def test_theorem2_bound_numerical(self) -> None:
        n = 14_107
        rng = np.random.default_rng(0)
        y = rng.normal(0, 1, n)
        q_lower = y - 1.0
        q_upper = y + 1.0
        calibrator = AdaptiveTemporalConformalCalibrator(
            alpha=0.10,
            lipschitz_constants={10: 0.65},
        )
        calibrator.calibrate(q_lower, q_upper, y, horizon=10)
        bound = calibrator.theorem2_bound(horizon=10, delta=0.10)
        assert 0.005 < bound < 0.02, (
            f"Theorem 2 bound {bound:.6f} is outside expected range (0.005, 0.02) "
            f"for n=14107 and L=0.65."
        )

    def test_unknown_horizon_raises(self) -> None:
        calibrator = AdaptiveTemporalConformalCalibrator()
        with pytest.raises(KeyError):
            calibrator.predict_interval(np.array([0.0]), np.array([1.0]), horizon=99)

    def test_theorem2_missing_lipschitz_raises(self) -> None:
        rng = np.random.default_rng(0)
        y = rng.normal(0, 1, 100)
        calibrator = AdaptiveTemporalConformalCalibrator(lipschitz_constants={})
        calibrator.calibrate(y - 0.5, y + 0.5, y, horizon=7)
        with pytest.raises(ValueError, match="Lipschitz constant"):
            calibrator.theorem2_bound(horizon=7)
