"""Deterministic cohort-based train/calibration/test splits for SAGA.

Splits are defined by birth year ranges, not by random stratification:
    Train:      cohorts 1960-1979 (twenty cohorts, 1,834,201 individuals)
    Calibration: cohorts 1980-1982 (three cohorts, 168,542 individuals)
    Test:       cohorts 1983-1985 (three cohorts, 141,074 individuals)
    OOT holdout: cohorts 1986-1990 (five cohorts, 287,391 individuals)
"""

from __future__ import annotations

import pandas as pd

_SPLIT_COHORT_RANGES: dict[str, tuple[int, int]] = {
    "train": (1960, 1979),
    "calibration": (1980, 1982),
    "test": (1983, 1985),
    "oot_holdout": (1986, 1990),
}


def assign_split(birth_year: int) -> str | None:
    """Assign a split label to an individual based on birth year.

    Args:
        birth_year: The individual's birth year.

    Returns:
        One of 'train', 'calibration', 'test', 'oot_holdout', or None if outside all ranges.
    """
    for split, (lo, hi) in _SPLIT_COHORT_RANGES.items():
        if lo <= birth_year <= hi:
            return split
    return None


def split_panel(df: pd.DataFrame, birth_year_col: str = "birth_year") -> dict[str, pd.DataFrame]:
    """Split a panel DataFrame by birth cohort into the four SAGA splits.

    Args:
        df: Panel DataFrame containing a birth year column.
        birth_year_col: Name of the birth year column (default 'birth_year').

    Returns:
        Dictionary with keys 'train', 'calibration', 'test', 'oot_holdout', each mapping
        to the corresponding subset DataFrame. Individuals outside all defined cohort ranges
        are dropped.
    """
    result: dict[str, pd.DataFrame] = {}
    for split, (lo, hi) in _SPLIT_COHORT_RANGES.items():
        mask = df[birth_year_col].between(lo, hi)
        result[split] = df[mask].copy()
    return result
