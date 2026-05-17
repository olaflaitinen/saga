"""Year-specific feature standardization for SAGA continuous subvector.

Computes and applies year-specific means and standard deviations for the 15 continuous
features, as described in the tokenization scheme documentation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

_CONTINUOUS_COLUMNS: list[str] = [
    "log_labor_earnings",
    "log_capital_income",
    "log_total_transfers",
    "log_sickness_benefit_days",
    "log_parental_leave_days",
    "log_unemployment_benefit_days",
    "log_disability_pension",
    "log_pension_income",
    "log_housing_supplement",
    "employment_rate",
    "log_employer_earnings",
    "log_employer_size",
    "full_time_indicator",
    "n_employers",
    "log_spousal_earnings",
]


class YearSpecificStandardizer:
    """Fits and applies year-specific standardization to the 15 continuous features.

    Attributes:
        means: Dict mapping calendar year to per-feature mean array of shape (15,).
        stds: Dict mapping calendar year to per-feature std array of shape (15,).
        columns: List of continuous column names.
    """

    def __init__(self) -> None:
        self.means: dict[int, np.ndarray] = {}
        self.stds: dict[int, np.ndarray] = {}
        self.columns = _CONTINUOUS_COLUMNS

    def fit(self, df: pd.DataFrame) -> YearSpecificStandardizer:
        """Fit year-specific means and standard deviations from the training data.

        Args:
            df: Training panel DataFrame with a 'year' column and the 15 continuous features.

        Returns:
            self (for method chaining).
        """
        for year, group in df.groupby("year"):
            vals = group[self.columns].values.astype(np.float32)
            self.means[int(year)] = vals.mean(axis=0)  # type: ignore[arg-type]
            self.stds[int(year)] = vals.std(axis=0) + 1e-8  # type: ignore[arg-type]
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize the continuous features using fitted year-specific statistics.

        For years not seen during fitting, the global mean/std across all years is used.

        Args:
            df: Panel DataFrame to standardize.

        Returns:
            DataFrame with standardized continuous features (in-place copy).
        """
        df = df.copy()
        if not self.means:
            return df
        global_mean = np.stack(list(self.means.values())).mean(axis=0)
        global_std = np.stack(list(self.stds.values())).mean(axis=0)
        for year in df["year"].unique():
            mask = df["year"] == year
            mean = self.means.get(int(year), global_mean)
            std = self.stds.get(int(year), global_std)
            df.loc[mask, self.columns] = (df.loc[mask, self.columns].values - mean) / std
        return df

    def save(self, path: str | Path) -> None:
        """Save the fitted statistics to a .npz file.

        Args:
            path: Output path for the .npz file.
        """
        np.savez(
            str(path),
            years=np.array(sorted(self.means.keys()), dtype=np.int16),
            means=np.stack([self.means[y] for y in sorted(self.means)]),
            stds=np.stack([self.stds[y] for y in sorted(self.stds)]),
        )

    @classmethod
    def load(cls, path: str | Path) -> YearSpecificStandardizer:
        """Load a fitted standardizer from a .npz file.

        Args:
            path: Path to the .npz file produced by save().

        Returns:
            A fitted YearSpecificStandardizer instance.
        """
        data = np.load(str(path))
        obj = cls()
        for i, year in enumerate(data["years"].tolist()):
            obj.means[int(year)] = data["means"][i]
            obj.stds[int(year)] = data["stds"][i]
        return obj
