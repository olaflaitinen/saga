"""Integration smoke test for the SAGA pipeline.

Verifies that the full forward pass from raw batch data through the model,
conformal calibration, and metric computation runs without errors on a tiny
synthetic batch (no real data required).

This test is marked as 'integration' and excluded from unit-only CI runs.
"""

import numpy as np
import pytest
import torch

from saga.config import SagaConfig
from saga.conformal.adaptive_temporal import AdaptiveTemporalConformalCalibrator
from saga.evaluation.metrics_probabilistic import crps_quantile, picp
from saga.model.saga_model import SagaModel


pytestmark = pytest.mark.integration


def _make_tiny_batch(batch_size: int = 4, seq_len: int = 10) -> dict:
    """Create a minimal batch for smoke testing."""
    config = SagaConfig()
    return {
        "continuous": torch.randn(batch_size, seq_len, 15),
        "categorical": {
            name: torch.zeros(batch_size, seq_len, dtype=torch.long)
            for name in [
                "occupation", "industry", "region", "education_level",
                "field_of_study", "sex", "country_of_birth_group",
                "marital_status", "n_children", "age_youngest_child",
            ]
        },
        "missingness": torch.zeros(batch_size, seq_len, 16),
        "age": torch.full((batch_size, seq_len), 30, dtype=torch.long),
        "year": torch.full((batch_size, seq_len), 2005, dtype=torch.long),
    }


class TestFullPipelineSmoke:
    """Smoke tests for the full SAGA inference + calibration pipeline."""

    def test_model_to_calibrated_interval(self) -> None:
        config = SagaConfig()
        model = SagaModel(config)
        model.eval()
        batch = _make_tiny_batch(batch_size=50, seq_len=10)

        with torch.no_grad():
            point_preds, quantile_preds = model(**batch)

        q_lower_np = quantile_preds[:, -1, 1].numpy()
        q_upper_np = quantile_preds[:, -1, 5].numpy()
        y_true_np = point_preds[:, -1].numpy() + np.random.default_rng(0).normal(0, 0.3, 50)

        calibrator = AdaptiveTemporalConformalCalibrator(
            alpha=0.10, lipschitz_constants={10: 0.65}
        )
        calibrator.calibrate(q_lower_np, q_upper_np, y_true_np, horizon=10)
        lo, hi = calibrator.predict_interval(q_lower_np, q_upper_np, horizon=10)

        coverage = picp(lo, hi, y_true_np)
        assert coverage >= 0.0
        assert coverage <= 1.0

    def test_crps_computes_on_model_output(self) -> None:
        config = SagaConfig()
        model = SagaModel(config)
        model.eval()
        batch = _make_tiny_batch(batch_size=20, seq_len=5)

        with torch.no_grad():
            point_preds, quantile_preds = model(**batch)

        q_np = quantile_preds[:, -1, :].numpy()
        y_np = point_preds[:, -1].numpy()

        crps_val = crps_quantile(q_np, y_np, config.quantile_levels)
        assert crps_val >= 0.0
        assert np.isfinite(crps_val)
