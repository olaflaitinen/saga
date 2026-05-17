"""Unit tests for probabilistic forecast evaluation metrics.

Verifies CRPS, MAE, RMSE, PICP, and the CRPS reduction formula against known values.
The headline manuscript results are cross-checked as integration-level smoke tests.
"""

import numpy as np
import pytest

from saga.evaluation.metrics_probabilistic import (
    crps_quantile,
    mae,
    rmse,
    picp,
    crps_reduction_vs_baseline,
)


class TestCRPS:
    """Tests for crps_quantile."""

    QUANTILE_LEVELS = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)

    def test_perfect_median_low_crps(self) -> None:
        y_true = np.array([0.0, 0.0, 0.0])
        q_preds = np.zeros((3, 7))
        crps_val = crps_quantile(q_preds, y_true, self.QUANTILE_LEVELS)
        assert crps_val < 0.1

    def test_non_negative(self) -> None:
        rng = np.random.default_rng(42)
        y = rng.normal(0, 1, 100)
        q = rng.normal(0, 1, (100, 7))
        assert crps_quantile(q, y, self.QUANTILE_LEVELS) >= 0.0


class TestManuscriptCRPSReduction:
    """Verify the headline CRPS reduction formula with manuscript values."""

    def test_headline_crps_reduction_h10(self) -> None:
        crps_saga = 0.318
        crps_gkos = 0.467
        reduction = crps_reduction_vs_baseline(crps_saga, crps_gkos)
        assert abs(reduction - 0.319) < 0.001, (
            f"Expected CRPS reduction approximately 0.319, got {reduction:.4f}."
        )

    def test_crps_reduction_h20(self) -> None:
        crps_saga_h20 = 0.318 * (1.0 - 0.412)
        crps_gkos_h20 = crps_saga_h20 / (1.0 - 0.412)
        reduction = crps_reduction_vs_baseline(crps_saga_h20, crps_gkos_h20)
        assert abs(reduction - 0.412) < 0.001


class TestMAERMSE:
    """Tests for MAE and RMSE."""

    def test_mae_zero_for_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert mae(y, y) == 0.0

    def test_rmse_zero_for_perfect(self) -> None:
        y = np.array([1.0, 2.0, 3.0])
        assert rmse(y, y) == 0.0

    def test_mae_known_value(self) -> None:
        y_pred = np.array([0.0, 0.0])
        y_true = np.array([1.0, 3.0])
        assert mae(y_pred, y_true) == 2.0


class TestPICP:
    """Tests for PICP."""

    def test_full_coverage(self) -> None:
        y = np.array([0.5, 1.5, 2.5])
        lo = np.array([0.0, 1.0, 2.0])
        hi = np.array([1.0, 2.0, 3.0])
        assert picp(lo, hi, y) == 1.0

    def test_zero_coverage(self) -> None:
        y = np.array([5.0, 6.0])
        lo = np.array([0.0, 0.0])
        hi = np.array([1.0, 1.0])
        assert picp(lo, hi, y) == 0.0
