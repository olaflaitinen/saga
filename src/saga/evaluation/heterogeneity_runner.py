"""Heterogeneity decomposition runner for Table VIII.

Defines the 15 demographic subgroups and their manuscript CRPS reductions vs. GKOS at h=10.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubgroupSpec:
    """Specification for a heterogeneity decomposition subgroup.

    Attributes:
        label: Short label for the subgroup.
        description: Human-readable description.
        n_core_sample: Subgroup sample size in the core analysis sample.
        crps_reduction_vs_gkos: CRPS reduction vs. GKOS at h=10 (Table VIII).
    """

    label: str
    description: str
    n_core_sample: int
    crps_reduction_vs_gkos: float


_SUBGROUP_SPECS: list[SubgroupSpec] = [
    SubgroupSpec("male", "Male", 891_432, 0.297),
    SubgroupSpec("female", "Female", 1_252_385, 0.348),
    SubgroupSpec("educ_compulsory", "Compulsory education only", 312_847, 0.412),
    SubgroupSpec("educ_upper_secondary", "Upper secondary education", 894_213, 0.314),
    SubgroupSpec("educ_short_tertiary", "Short tertiary education", 487_621, 0.283),
    SubgroupSpec("educ_long_tertiary", "Long tertiary education", 449_136, 0.247),
    SubgroupSpec("stable_employer", "Stable employer", 867_334, 0.241),
    SubgroupSpec("high_mobility", "Four or more employer changes", 312_143, 0.473),
    SubgroupSpec("income_q1", "Income quintile Q1", 428_763, 0.447),
    SubgroupSpec("income_q5", "Income quintile Q5", 428_819, 0.228),
    SubgroupSpec("stockholm", "Stockholm county", 412_834, 0.271),
    SubgroupSpec("gothenburg", "Gothenburg county", 198_437, 0.294),
    SubgroupSpec("malmo", "Malmo county", 143_216, 0.308),
    SubgroupSpec("other_urban", "Other urban", 673_418, 0.327),
    SubgroupSpec("rural", "Rural", 715_912, 0.363),
]


def get_subgroup_spec(label: str) -> SubgroupSpec:
    """Retrieve a subgroup specification by label.

    Args:
        label: Subgroup label.

    Returns:
        The corresponding SubgroupSpec.

    Raises:
        KeyError: If no subgroup with the given label exists.
    """
    for spec in _SUBGROUP_SPECS:
        if spec.label == label:
            return spec
    raise KeyError(f"No subgroup spec with label '{label}'.")
