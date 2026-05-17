"""Reproducibility seeding utilities.

Sets the random seed for Python's random module, numpy, and torch simultaneously.
The five seeds used in the manuscript are:
    20260601, 20260602, 20260603, 20260604, 20260605
"""

from __future__ import annotations

import random

import numpy as np
import torch


def set_all_seeds(seed: int) -> None:
    """Set the random seed for Python, numpy, and torch.

    Args:
        seed: Integer seed value. Manuscript seeds: 20260601-20260605.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
