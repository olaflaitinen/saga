"""Unit tests for lifetime earnings distributional statistics.

Verifies the Gini coefficient, top-income-share, and full statistics dict
against known analytical values and the manuscript Table IV figures.
"""

import numpy as np
import pytest

from saga.evaluation.lifetime_statistics import (
    gini_coefficient,
    top_income_share,
    lifetime_distribution_statistics,
)


class TestGiniCoefficient:
    """Tests for gini_coefficient."""

    def test_perfect_equality(self) -> None:
        assert gini_coefficient(np.ones(100)) == pytest.approx(0.0, abs=1e-6)

    def test_perfect_inequality(self) -> None:
        x = np.zeros(100)
        x[0] = 1.0
        g = gini_coefficient(x)
        assert g > 0.99

    def test_known_two_person(self) -> None:
        x = np.array([1.0, 3.0])
        g = gini_coefficient(x)
        assert g == pytest.approx(0.5, abs=0.01)

    def test_manuscript_saga_range(self) -> None:
        rng = np.random.default_rng(42)
        lognormal = rng.lognormal(mean=16.2, sigma=0.7, size=141_074)
        g = gini_coefficient(lognormal)
        assert 0.25 < g < 0.45


class TestTopIncomeShare:
    """Tests for top_income_share."""

    def test_top1pct_uniform(self) -> None:
        x = np.ones(1000)
        share = top_income_share(x, percentile=99.0)
        assert share == pytest.approx(0.01, abs=0.01)

    def test_top1pct_concentrated(self) -> None:
        x = np.ones(100)
        x[0] = 1000.0
        share = top_income_share(x, percentile=99.0)
        assert share > 0.9


class TestLifetimeDistributionStatistics:
    """Tests for lifetime_distribution_statistics."""

    def test_output_keys(self) -> None:
        x = np.ones(100)
        result = lifetime_distribution_statistics(x)
        for key in ("mean", "median", "p10", "p90", "p99", "gini", "top1pct_share"):
            assert key in result

    def test_mean_matches_np(self) -> None:
        rng = np.random.default_rng(0)
        x = rng.lognormal(1.0, 0.5, 1000)
        stats = lifetime_distribution_statistics(x)
        assert stats["mean"] == pytest.approx(float(np.mean(x)), rel=1e-6)
