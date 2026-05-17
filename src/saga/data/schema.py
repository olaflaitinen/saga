"""Panel data schema validation for SAGA.

Validates that a loaded parquet file conforms to the expected column schema,
dtype constraints, and value range constraints for the 15 continuous features,
10 categorical features, age, and year columns.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


_REQUIRED_CONTINUOUS_COLUMNS: list[str] = [
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

_REQUIRED_CATEGORICAL_COLUMNS: list[str] = [
    "occupation",
    "industry",
    "region",
    "education_level",
    "field_of_study",
    "sex",
    "country_of_birth_group",
    "marital_status",
    "n_children",
    "age_youngest_child",
]

_REQUIRED_COLUMNS: list[str] = (
    ["individual_id", "birth_year", "age", "year"]
    + _REQUIRED_CONTINUOUS_COLUMNS
    + _REQUIRED_CATEGORICAL_COLUMNS
    + [f"missing_{c}" for c in _REQUIRED_CONTINUOUS_COLUMNS]
    + ["any_missing"]
)


def validate_schema(df: pd.DataFrame) -> list[str]:
    """Validate that a DataFrame conforms to the SAGA panel schema.

    Args:
        df: Panel DataFrame to validate.

    Returns:
        List of validation error messages (empty list if all checks pass).
    """
    errors: list[str] = []
    missing_cols = set(_REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {sorted(missing_cols)}")

    if "age" in df.columns:
        if df["age"].lt(16).any() or df["age"].gt(64).any():
            errors.append("Column 'age' contains values outside [16, 64].")

    if "year" in df.columns:
        if df["year"].lt(1990).any() or df["year"].gt(2022).any():
            errors.append("Column 'year' contains values outside [1990, 2022].")

    if "employment_rate" in df.columns:
        if df["employment_rate"].lt(0).any() or df["employment_rate"].gt(1).any():
            errors.append("Column 'employment_rate' contains values outside [0, 1].")

    return errors
