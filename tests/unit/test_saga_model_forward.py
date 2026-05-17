"""Unit tests for the SagaModel forward pass.

Asserts the headline parameter count of 10,872,960 and verifies output shapes.
Any change to the architecture that modifies the parameter count will fail this test,
providing an immediate guard against accidental architecture drift.
"""

import pytest
import torch

from saga.config import SagaConfig
from saga.model.saga_model import SagaModel


_HEADLINE_PARAMETER_COUNT: int = 10_872_960
_PARAMETER_COUNT_TOLERANCE: int = 50_000


@pytest.fixture()
def config() -> SagaConfig:
    """Return the default (headline) SagaConfig."""
    return SagaConfig()


@pytest.fixture()
def model(config: SagaConfig) -> SagaModel:
    """Return an initialized SagaModel with the headline config."""
    return SagaModel(config)


def _make_batch(
    batch_size: int = 2,
    seq_len: int = 10,
    config: SagaConfig | None = None,
) -> dict:
    cfg = config or SagaConfig()
    return {
        "continuous": torch.zeros(batch_size, seq_len, 15),
        "categorical": {
            "occupation": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "industry": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "region": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "education_level": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "field_of_study": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "sex": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "country_of_birth_group": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "marital_status": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "n_children": torch.zeros(batch_size, seq_len, dtype=torch.long),
            "age_youngest_child": torch.zeros(batch_size, seq_len, dtype=torch.long),
        },
        "missingness": torch.zeros(batch_size, seq_len, 16),
        "age": torch.full((batch_size, seq_len), 25, dtype=torch.long),
        "year": torch.full((batch_size, seq_len), 2000, dtype=torch.long),
    }


class TestSagaModelParameterCount:
    """Verify that the headline SagaModel has the expected parameter count."""

    def test_parameter_count_is_headline(self, model: SagaModel) -> None:
        n_params = model.count_parameters()
        assert abs(n_params - _HEADLINE_PARAMETER_COUNT) <= _PARAMETER_COUNT_TOLERANCE, (
            f"Expected approximately {_HEADLINE_PARAMETER_COUNT} parameters, "
            f"got {n_params}. Architecture may have drifted."
        )


class TestSagaModelOutputShapes:
    """Verify that SagaModel produces the correct output shapes."""

    def test_point_head_shape(self, model: SagaModel, config: SagaConfig) -> None:
        batch = _make_batch(batch_size=2, seq_len=10, config=config)
        point_preds, _ = model(**batch)
        assert point_preds.shape == (2, 10), (
            f"Expected point_preds shape (2, 10), got {point_preds.shape}."
        )

    def test_quantile_head_shape(self, model: SagaModel, config: SagaConfig) -> None:
        batch = _make_batch(batch_size=2, seq_len=10, config=config)
        _, quantile_preds = model(**batch)
        n_q = len(config.quantile_levels)
        assert quantile_preds.shape == (2, 10, n_q), (
            f"Expected quantile_preds shape (2, 10, {n_q}), got {quantile_preds.shape}."
        )

    def test_single_token_forward(self, model: SagaModel, config: SagaConfig) -> None:
        batch = _make_batch(batch_size=1, seq_len=1, config=config)
        point_preds, quantile_preds = model(**batch)
        assert point_preds.shape == (1, 1)
        assert quantile_preds.shape == (1, 1, len(config.quantile_levels))

    def test_max_context_forward(self, model: SagaModel, config: SagaConfig) -> None:
        batch = _make_batch(batch_size=1, seq_len=config.max_context_length, config=config)
        point_preds, quantile_preds = model(**batch)
        assert point_preds.shape == (1, config.max_context_length)


class TestSagaModelCausalMask:
    """Verify causal masking: prediction at position t must not depend on position t+1."""

    def test_causal_independence(self, model: SagaModel, config: SagaConfig) -> None:
        model.eval()
        batch_a = _make_batch(batch_size=1, seq_len=5, config=config)
        batch_b = _make_batch(batch_size=1, seq_len=5, config=config)
        batch_b["continuous"][0, 3, 0] = 99.0

        with torch.no_grad():
            preds_a, _ = model(**batch_a)
            preds_b, _ = model(**batch_b)

        for t in range(3):
            assert torch.allclose(preds_a[0, t], preds_b[0, t], atol=1e-5), (
                f"Causal mask violated: prediction at position {t} changed when "
                f"position 3 was modified."
            )
