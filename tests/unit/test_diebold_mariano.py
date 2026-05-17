"""Unit tests for the Diebold-Mariano test.

Verifies that the DM statistic is positive when model losses are systematically
lower than baseline losses, and that the p-value is below 0.05 for large samples.
"""

import numpy as np
import pytest

from saga.evaluation.diebold_mariano import DieboldMarianoTest, newey_west_variance


class TestNeweyWestVariance:
    """Tests for newey_west_variance."""

    def test_returns_positive(self) -> None:
        rng = np.random.default_rng(0)
        d = rng.normal(0, 1, 1000)
        var = newey_west_variance(d, lag=5)
        assert var > 0.0

    def test_iid_matches_sample_variance(self) -> None:
        rng = np.random.default_rng(42)
        d = rng.normal(0, 1, 100_000)
        var = newey_west_variance(d, lag=0)
        expected = float((d**2).mean() / len(d))
        assert abs(var - expected) < 1e-6


class TestDieboldMarianoTest:
    """Tests for DieboldMarianoTest."""

    def test_positive_statistic_when_model_better(self) -> None:
        rng = np.random.default_rng(5)
        n = 100_000
        loss_model = rng.gamma(1.0, 0.318, n)
        loss_baseline = rng.gamma(1.0, 0.467, n)
        dm = DieboldMarianoTest(lag=5)
        stat, pval = dm.test(loss_model, loss_baseline)
        assert stat > 0.0

    def test_pvalue_below_005_for_large_clear_difference(self) -> None:
        rng = np.random.default_rng(7)
        n = 141_074
        loss_model = rng.gamma(1.0, 0.318, n)
        loss_baseline = rng.gamma(1.0, 0.467, n)
        dm = DieboldMarianoTest(lag=5)
        _, pval = dm.test(loss_model, loss_baseline)
        assert pval < 0.001

    def test_equal_losses_near_zero_statistic(self) -> None:
        rng = np.random.default_rng(0)
        n = 10_000
        loss = rng.exponential(1.0, n)
        dm = DieboldMarianoTest(lag=5)
        stat, _ = dm.test(loss, loss)
        assert abs(stat) < 1e-6
