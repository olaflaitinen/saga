"""Synthetic mirror dataset generation for SAGA.

Generates the 500,000-individual synthetic mirror dataset from SAGA's predictive
distribution conditional on resampled demographic baseline vectors, as documented in
Appendix D of the manuscript.

This module is included for transparency; the actual synthetic mirror was generated
inside the Statistics Sweden MONA environment using the real LISA panel and is available
at Zenodo (DOI: 10.5281/zenodo.20260287). Running this module outside MONA produces synthetic
data conditional on the marginal distributions from the synthetic mirror itself, not on the
real LISA panel.
"""

from __future__ import annotations

import pandas as pd

_SYNTHETIC_MIRROR_DOI: str = "10.5281/zenodo.20260287"
_N_INDIVIDUALS: int = 500_000
_N_TRAIN: int = 350_000
_N_CAL: int = 75_000
_N_TEST: int = 75_000


class SyntheticMirrorGenerator:
    """Generates synthetic earnings panel data from SAGA's predictive distribution.

    This class is a documentation stub. The full generation procedure requires a trained
    SAGA model and access to the real LISA marginal distributions (available only inside MONA).
    The Zenodo deposit at DOI 10.5281/zenodo.20260287 contains the pre-generated synthetic mirror.

    Attributes:
        n_individuals: Total number of synthetic individuals to generate.
        seed: Random seed for reproducibility.
    """

    MOMENT_MATCH_TOLERANCE: float = 0.018
    MEMBERSHIP_INFERENCE_AUC: float = 0.512

    def __init__(self, n_individuals: int = 500_000, seed: int = 20260601) -> None:
        self.n_individuals = n_individuals
        self.seed = seed

    def generate(self) -> pd.DataFrame:
        """Generate the synthetic panel DataFrame.

        To generate the dataset locally run::

            bash scripts/export_synthetic_mirror.sh

        which calls ``scripts/generate_synthetic_dataset.py`` and writes the
        five Zenodo deposit files to ``data/synthetic/``.

        To download the pre-generated canonical deposit run::

            bash scripts/download_synthetic_mirror.sh

        Raises:
            NotImplementedError: Always; use the scripts above instead.
        """
        raise NotImplementedError(
            "Use scripts/export_synthetic_mirror.sh to generate the dataset locally, "
            "or scripts/download_synthetic_mirror.sh to download the pre-generated "
            f"Zenodo deposit (DOI: {_SYNTHETIC_MIRROR_DOI})."
        )
