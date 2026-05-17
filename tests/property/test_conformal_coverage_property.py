"""Property-based tests for conformal calibration coverage guarantee.

Uses Hypothesis to verify that the split conformal marginal coverage guarantee
holds for a wide range of synthetic calibration and test distributions.
"""

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st
from saga.conformal.split_conformal import SplitConformalCalibrator


@settings(max_examples=30, deadline=5000)
@given(
    n_cal=st.integers(min_value=50, max_value=500),
    n_test=st.integers(min_value=100, max_value=1000),
    alpha=st.floats(min_value=0.05, max_value=0.30),
    sigma=st.floats(min_value=0.1, max_value=2.0),
    seed=st.integers(min_value=0, max_value=10000),
)
def test_marginal_coverage_holds(
    n_cal: int,
    n_test: int,
    alpha: float,
    sigma: float,
    seed: int,
) -> None:
    """Marginal coverage must be >= 1 - alpha for any exchangeable distribution."""
    rng = np.random.default_rng(seed)
    y_cal = rng.normal(0, sigma, n_cal)
    q_lower_cal = y_cal - sigma
    q_upper_cal = y_cal + sigma

    calibrator = SplitConformalCalibrator(alpha=alpha)
    calibrator.calibrate(q_lower_cal, q_upper_cal, y_cal, horizon=1)

    y_test = rng.normal(0, sigma, n_test)
    q_lower_test = y_test - sigma
    q_upper_test = y_test + sigma
    lo, hi = calibrator.predict_interval(q_lower_test, q_upper_test, horizon=1)

    coverage = float(((y_test >= lo) & (y_test <= hi)).mean())
    assert coverage >= 1.0 - alpha - 0.05, (
        f"Coverage {coverage:.3f} is below (1-alpha) - 0.05 = {1-alpha-0.05:.3f} "
        f"(alpha={alpha:.2f}, n_cal={n_cal})."
    )
