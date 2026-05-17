"""Validation loop and early stopping for SAGA.

Evaluates the model on the calibration split every `validation_interval_steps` steps
and stops training when the validation pinball loss does not improve for
`early_stopping_patience` consecutive checks.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import torch
import torch.nn as nn


@dataclass
class EarlyStopping:
    """Tracks validation loss and signals when training should stop.

    Args:
        patience: Number of consecutive non-improving validation checks before stopping.
        min_delta: Minimum absolute improvement to count as an improvement (default 1e-5).

    Attributes:
        best_loss: Best validation loss observed so far.
        n_bad_checks: Number of consecutive non-improving checks.
        should_stop: True if training should halt.
        best_step: Optimization step at which the best checkpoint was saved.
    """

    patience: int = 20
    min_delta: float = 1e-5
    best_loss: float = field(default=math.inf, init=False)
    n_bad_checks: int = field(default=0, init=False)
    should_stop: bool = field(default=False, init=False)
    best_step: int = field(default=0, init=False)

    def update(self, val_loss: float, step: int) -> bool:
        """Update the early stopping tracker with a new validation loss.

        Args:
            val_loss: The current validation pinball loss.
            step: The current optimization step.

        Returns:
            True if this is the best checkpoint seen so far.
        """
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.best_step = step
            self.n_bad_checks = 0
            return True
        self.n_bad_checks += 1
        if self.n_bad_checks >= self.patience:
            self.should_stop = True
        return False


def evaluate_pinball_loss(
    model: nn.Module,
    dataloader: Any,
    quantile_levels: tuple[float, ...],
    device: torch.device,
) -> float:
    """Evaluate the validation pinball loss on the calibration split.

    Args:
        model: Trained SagaModel (in eval mode).
        dataloader: Calibration split dataloader.
        quantile_levels: Tuple of quantile levels.
        device: Torch device.

    Returns:
        Mean validation pinball loss over the calibration split.
    """
    from saga.training.losses import pinball_loss

    model.eval()
    total_loss = 0.0
    n_batches = 0

    with torch.no_grad():
        for batch in dataloader:
            continuous = batch["continuous"].to(device)
            categorical = {k: v.to(device) for k, v in batch["categorical"].items()}
            missingness = batch["missingness"].to(device)
            age = batch["age"].to(device)
            year = batch["year"].to(device)
            target = batch["target"].to(device)
            mask = batch.get("mask")
            if mask is not None:
                mask = mask.to(device)

            _, quantile_preds = model(continuous, categorical, missingness, age, year)
            loss = pinball_loss(quantile_preds, target, quantile_levels, mask)
            total_loss += float(loss)
            n_batches += 1

    return total_loss / max(n_batches, 1)
