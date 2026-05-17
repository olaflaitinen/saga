"""Robustness check runner for Table VII (R1-R9) and placebo tests for Table IX.

Each robustness check perturbs one aspect of the evaluation procedure (training cohort
restriction, subsample, discount rate, deflator, out-of-time holdout, feature restriction,
or recession-year fold) and reports the CRPS reduction versus GKOS.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RobustnessSpec:
    """Specification for a single robustness check.

    Attributes:
        label: Short label (e.g., 'R1').
        description: Human-readable description.
        crps_reduction_manuscript: CRPS reduction vs. GKOS at h=10 (Table VII).
    """

    label: str
    description: str
    crps_reduction_manuscript: float


_ROBUSTNESS_SPECS: list[RobustnessSpec] = [
    RobustnessSpec(
        label="R1",
        description="Train on cohorts 1965-1979 only",
        crps_reduction_manuscript=0.308,
    ),
    RobustnessSpec(
        label="R2",
        description="Male sample only",
        crps_reduction_manuscript=0.297,
    ),
    RobustnessSpec(
        label="R3",
        description="Stable employer subsample only",
        crps_reduction_manuscript=0.241,
    ),
    RobustnessSpec(
        label="R4",
        description="Calibration set restricted to cohort 1985",
        crps_reduction_manuscript=0.319,
    ),
    RobustnessSpec(
        label="R5a",
        description="Discount rate 0%",
        crps_reduction_manuscript=0.331,
    ),
    RobustnessSpec(
        label="R5b",
        description="Discount rate 1%",
        crps_reduction_manuscript=0.327,
    ),
    RobustnessSpec(
        label="R5c",
        description="Discount rate 3%",
        crps_reduction_manuscript=0.318,
    ),
    RobustnessSpec(
        label="R6",
        description="HICP deflator instead of CPI",
        crps_reduction_manuscript=0.322,
    ),
    RobustnessSpec(
        label="R7",
        description="Out-of-time holdout (cohorts 1986-1990)",
        crps_reduction_manuscript=0.284,
    ),
    RobustnessSpec(
        label="R8",
        description="PSID-inventory-restricted features (Sweden-internal)",
        crps_reduction_manuscript=0.214,
    ),
    RobustnessSpec(
        label="R9",
        description="Recession-year test fold (forecast windows containing 2009)",
        crps_reduction_manuscript=0.288,
    ),
]


@dataclass(frozen=True)
class PlaceboSpec:
    """Specification for a placebo or falsification test (Table IX).

    Attributes:
        label: Short label.
        description: Human-readable description.
        metric_name: Name of the reported metric.
        value_manuscript: Value from the manuscript (Table IX).
    """

    label: str
    description: str
    metric_name: str
    value_manuscript: float


_PLACEBO_SPECS: list[PlaceboSpec] = [
    PlaceboSpec(
        label="P1",
        description="Permutation placebo",
        metric_name="CRPS ratio (placebo / headline)",
        value_manuscript=2.14,
    ),
    PlaceboSpec(
        label="P2",
        description="Short-history placebo (5-year window)",
        metric_name="CRPS reduction vs. GKOS (%)",
        value_manuscript=0.183,
    ),
    PlaceboSpec(
        label="P3",
        description="Static feature-only placebo",
        metric_name="CRPS at h=10",
        value_manuscript=0.623,
    ),
]


def get_robustness_spec(label: str) -> RobustnessSpec:
    """Retrieve a robustness specification by label.

    Args:
        label: Check label (e.g., 'R1').

    Returns:
        The corresponding RobustnessSpec.

    Raises:
        KeyError: If no check with the given label exists.
    """
    for spec in _ROBUSTNESS_SPECS:
        if spec.label == label:
            return spec
    raise KeyError(f"No robustness spec with label '{label}'.")
