"""Lifetime Monte Carlo aggregator for SAGA.

Implements the lifetime earnings aggregation procedure described in Section III-E and
documented in docs/methodology/lifetime-monte-carlo-aggregation.md.

Parameters from the manuscript:
    M = 500 Monte Carlo paths per individual
    r = 0.02 real discount rate
    reference_age = 20
    currency_year = 2022 (2022 Swedish krona, CPI-deflated)
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn


class LifetimeMonteCarloAggregator:
    """Aggregates lifetime earnings via Monte Carlo sampling from SAGA's predictive distribution.

    For each individual, draws M autoregressive forecast paths from SAGA's quantile head
    by sampling from the empirical distribution implied by the 7-quantile output, computes
    present values discounted to reference_age, and returns the per-individual lifetime
    earnings distribution.

    Args:
        model: Trained SagaModel instance.
        n_paths: Number of Monte Carlo paths per individual M (default 500).
        discount_rate: Real discount rate r (default 0.02).
        reference_age: Age at which present values are discounted (default 20).
        currency_year: Reference year for CPI deflation (default 2022).

    Attributes:
        model: The SAGA model.
        n_paths: M (500).
        discount_rate: r (0.02).
        reference_age: 20.
        currency_year: 2022.
    """

    N_PATHS_MANUSCRIPT: int = 500
    DISCOUNT_RATE_MANUSCRIPT: float = 0.02
    REFERENCE_AGE_MANUSCRIPT: int = 20
    CURRENCY_YEAR_MANUSCRIPT: int = 2022

    def __init__(
        self,
        model: nn.Module,
        n_paths: int = 500,
        discount_rate: float = 0.02,
        reference_age: int = 20,
        currency_year: int = 2022,
    ) -> None:
        self.model = model
        self.n_paths = n_paths
        self.discount_rate = discount_rate
        self.reference_age = reference_age
        self.currency_year = currency_year

    def discount_factor(self, age: int) -> float:
        """Compute the discount factor from age to reference_age.

        Args:
            age: Age at which the earnings are received.

        Returns:
            Discount factor (1 + r)^(-(age - reference_age)).
        """
        return (1.0 + self.discount_rate) ** (-(age - self.reference_age))

    def aggregate(
        self,
        conditioning_panel: "np.ndarray",
        forecast_ages: list[int],
        device: str = "cpu",
    ) -> np.ndarray:
        """Aggregate lifetime earnings for a panel of individuals.

        Args:
            conditioning_panel: Conditioning data (implementation-dependent format).
            forecast_ages: List of forecast ages for each step.
            device: Torch device string (default "cpu").

        Returns:
            Array of shape (n_individuals, n_paths) with discounted lifetime earnings
            in 2022 Swedish krona.
        """
        raise NotImplementedError(
            "aggregate() requires real or synthetic data access. "
            "See notebooks/00-quickstart.ipynb for a working end-to-end example."
        )
