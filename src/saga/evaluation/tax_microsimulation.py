"""Tax microsimulation using the 2022 Swedish tax schedule.

Applies the 2022 Swedish tax schedule to annual earnings forecast paths and computes
lifetime tax payments and effective average tax rates, as reported in Table V.

2022 Swedish tax schedule parameters (from configs/tax_microsimulation_2022_schedule.yaml):
    municipal_tax_rate: 0.324
    state_income_tax_rate: 0.20
    state_income_tax_breakpoint_sek: 554900
    employee_social_security_rate: 0.07
    employee_social_security_cap_income_base_amounts: 8.07
    income_base_amount_sek: 71000
    wealth_tax_rate: 0.0 (abolished)
"""

from __future__ import annotations

import numpy as np

_DEFAULT_SCHEDULE: dict[str, float] = {
    "municipal_tax_rate": 0.324,
    "state_income_tax_rate": 0.20,
    "state_income_tax_breakpoint_sek": 554_900.0,
    "employee_social_security_rate": 0.07,
    "employee_social_security_cap_income_base_amounts": 8.07,
    "income_base_amount_sek": 71_000.0,
}


def annual_tax(
    gross_earnings_sek: float | np.ndarray,
    schedule: dict[str, float] | None = None,
) -> float | np.ndarray:
    """Compute annual Swedish income tax for given gross earnings.

    Applies municipal tax, state income tax above the breakpoint, and employee
    social security contribution capped at 8.07 income base amounts.
    The varnskatt was abolished in 2020 and is not applied.

    Args:
        gross_earnings_sek: Annual gross labor earnings in nominal 2022 SEK.
            Can be a scalar or numpy array.
        schedule: Tax schedule parameters dict. Defaults to 2022 schedule.

    Returns:
        Annual tax in 2022 SEK, same shape as input.
    """
    s = schedule or _DEFAULT_SCHEDULE
    g = np.asarray(gross_earnings_sek, dtype=float)

    municipal = g * s["municipal_tax_rate"]

    breakpoint = s["state_income_tax_breakpoint_sek"]
    state = np.where(g > breakpoint, (g - breakpoint) * s["state_income_tax_rate"], 0.0)

    iba = s["income_base_amount_sek"]
    cap = s["employee_social_security_cap_income_base_amounts"] * iba
    soc_base = np.minimum(g, cap)
    soc = soc_base * s["employee_social_security_rate"]

    total = municipal + state + soc
    return float(total) if np.ndim(gross_earnings_sek) == 0 else total


def effective_average_tax_rate(
    gross_earnings_sek: np.ndarray,
    schedule: dict[str, float] | None = None,
) -> float:
    """Compute the effective average tax rate (AETR) for a lifetime earnings stream.

    Args:
        gross_earnings_sek: Annual gross earnings array of shape (n_years,) in 2022 SEK.
        schedule: Tax schedule parameters dict.

    Returns:
        Lifetime AETR: total lifetime tax / total lifetime gross earnings.
    """
    taxes = annual_tax(gross_earnings_sek, schedule)
    total_gross = float(np.asarray(gross_earnings_sek).sum())
    if total_gross <= 0:
        return 0.0
    return float(np.asarray(taxes).sum()) / total_gross
