"""Unit tests for the 2022 Swedish tax microsimulation.

Verifies that the 2022 schedule produces correct tax amounts for known test cases,
including the breakpoint threshold and the social security cap.
"""

import numpy as np
import pytest
from saga.evaluation.tax_microsimulation import annual_tax, effective_average_tax_rate


class TestAnnualTax:
    """Tests for annual_tax with the 2022 Swedish schedule."""

    def test_zero_earnings(self) -> None:
        assert annual_tax(0.0) == pytest.approx(0.0, abs=1.0)

    def test_below_breakpoint(self) -> None:
        gross = 400_000.0
        tax = annual_tax(gross)
        expected_municipal = 400_000.0 * 0.324
        expected_soc = min(400_000.0, 8.07 * 71_000.0) * 0.07
        expected_total = expected_municipal + expected_soc
        assert tax == pytest.approx(expected_total, rel=1e-4)

    def test_above_breakpoint(self) -> None:
        gross = 700_000.0
        tax = annual_tax(gross)
        expected_municipal = 700_000.0 * 0.324
        expected_state = (700_000.0 - 554_900.0) * 0.20
        expected_soc = min(700_000.0, 8.07 * 71_000.0) * 0.07
        expected_total = expected_municipal + expected_state + expected_soc
        assert tax == pytest.approx(expected_total, rel=1e-4)

    def test_vectorized_input(self) -> None:
        gross = np.array([400_000.0, 700_000.0])
        tax = annual_tax(gross)
        assert tax.shape == (2,)
        assert tax[1] > tax[0]


class TestEffectiveAverageTaxRate:
    """Tests for effective_average_tax_rate."""

    def test_aetr_between_zero_and_one(self) -> None:
        earnings = np.full(10, 500_000.0)
        aetr = effective_average_tax_rate(earnings)
        assert 0.0 < aetr < 1.0

    def test_aetr_zero_for_zero_earnings(self) -> None:
        earnings = np.zeros(10)
        assert effective_average_tax_rate(earnings) == 0.0

    def test_aetr_increases_with_earnings(self) -> None:
        low_aetr = effective_average_tax_rate(np.full(5, 200_000.0))
        high_aetr = effective_average_tax_rate(np.full(5, 1_000_000.0))
        assert high_aetr > low_aetr
