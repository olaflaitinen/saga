"""Unit tests for cohort-based panel splits.

Verifies that the split boundaries exactly match the manuscript specification:
    Train: 1960-1979, Calibration: 1980-1982, Test: 1983-1985, OOT: 1986-1990.
"""

import pandas as pd
import pytest

from saga.data.splits import assign_split, split_panel


class TestAssignSplit:
    """Tests for assign_split."""

    def test_train_cohort_first(self) -> None:
        assert assign_split(1960) == "train"

    def test_train_cohort_last(self) -> None:
        assert assign_split(1979) == "train"

    def test_calibration_cohort(self) -> None:
        assert assign_split(1981) == "calibration"

    def test_test_cohort_first(self) -> None:
        assert assign_split(1983) == "test"

    def test_test_cohort_last(self) -> None:
        assert assign_split(1985) == "test"

    def test_oot_cohort(self) -> None:
        assert assign_split(1988) == "oot_holdout"

    def test_outside_all_splits(self) -> None:
        assert assign_split(1950) is None
        assert assign_split(1995) is None


class TestSplitPanel:
    """Tests for split_panel."""

    def _make_df(self) -> pd.DataFrame:
        return pd.DataFrame({"birth_year": list(range(1960, 1991))})

    def test_returns_four_splits(self) -> None:
        df = self._make_df()
        result = split_panel(df)
        assert set(result.keys()) == {"train", "calibration", "test", "oot_holdout"}

    def test_train_size(self) -> None:
        df = self._make_df()
        result = split_panel(df)
        assert len(result["train"]) == 20

    def test_calibration_size(self) -> None:
        df = self._make_df()
        result = split_panel(df)
        assert len(result["calibration"]) == 3

    def test_test_size(self) -> None:
        df = self._make_df()
        result = split_panel(df)
        assert len(result["test"]) == 3

    def test_oot_size(self) -> None:
        df = self._make_df()
        result = split_panel(df)
        assert len(result["oot_holdout"]) == 5
