"""Training loop for SAGA with gradient accumulation and early stopping.

Implements the training procedure described in Section IV of the manuscript:
AdamW with cosine schedule, 2,000 warmup steps, 300,000 total steps, bfloat16
accumulating to float32, gradient clipping, early stopping on validation pinball loss.
"""

from __future__ import annotations

import structlog
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR

from saga.config import SagaConfig

log = structlog.get_logger(__name__)


def build_optimizer(model: nn.Module, config: SagaConfig) -> AdamW:
    """Build the AdamW optimizer with weight decay applied only to weight matrices.

    Args:
        model: The SagaModel instance.
        config: SagaConfig with optimizer hyperparameters.

    Returns:
        Configured AdamW optimizer.
    """
    decay_params = [p for n, p in model.named_parameters() if p.requires_grad and p.ndim >= 2]
    no_decay_params = [p for n, p in model.named_parameters() if p.requires_grad and p.ndim < 2]
    return AdamW(
        [
            {"params": decay_params, "weight_decay": config.weight_decay},
            {"params": no_decay_params, "weight_decay": 0.0},
        ],
        lr=config.learning_rate,
        betas=(config.beta1, config.beta2),
    )


def build_scheduler(optimizer: AdamW, config: SagaConfig) -> SequentialLR:
    """Build the cosine decay schedule with linear warmup.

    Args:
        optimizer: The AdamW optimizer.
        config: SagaConfig with schedule hyperparameters.

    Returns:
        SequentialLR combining linear warmup and cosine decay.
    """
    warmup = LinearLR(optimizer, start_factor=1e-4, end_factor=1.0, total_iters=config.warmup_steps)
    cosine = CosineAnnealingLR(
        optimizer, T_max=config.total_steps - config.warmup_steps, eta_min=0.0
    )
    return SequentialLR(optimizer, schedulers=[warmup, cosine], milestones=[config.warmup_steps])
