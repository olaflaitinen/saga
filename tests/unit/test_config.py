"""Unit tests for SagaConfig.

Verifies default values match the headline manuscript hyperparameters and that
from_yaml round-trips correctly.
"""

import tempfile
from pathlib import Path

import pytest
import yaml

from saga.config import SagaConfig


class TestSagaConfigDefaults:
    """Verify that default SagaConfig matches manuscript Appendix A values."""

    def test_model_dim(self) -> None:
        assert SagaConfig().model_dim == 384

    def test_num_layers(self) -> None:
        assert SagaConfig().num_layers == 6

    def test_num_heads(self) -> None:
        assert SagaConfig().num_heads == 8

    def test_ffn_dim(self) -> None:
        assert SagaConfig().ffn_dim == 1536

    def test_max_context_length(self) -> None:
        assert SagaConfig().max_context_length == 45

    def test_dropout(self) -> None:
        assert SagaConfig().dropout == 0.1

    def test_learning_rate(self) -> None:
        assert SagaConfig().learning_rate == 3e-4

    def test_warmup_steps(self) -> None:
        assert SagaConfig().warmup_steps == 2_000

    def test_total_steps(self) -> None:
        assert SagaConfig().total_steps == 300_000

    def test_seed(self) -> None:
        assert SagaConfig().seed == 20260601

    def test_quantile_levels(self) -> None:
        assert len(SagaConfig().quantile_levels) == 7

    def test_token_pre_projection_dim(self) -> None:
        cfg = SagaConfig()
        expected = 64 + 76 + 16 + 64 + 32
        assert cfg.token_pre_projection_dim == expected == 252


class TestSagaConfigFromYAML:
    """Verify SagaConfig.from_yaml round-trips."""

    def test_from_yaml_overrides_defaults(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as fh:
            yaml.dump({"model_dim": 192, "num_layers": 4}, fh)
            tmp_path = fh.name
        cfg = SagaConfig.from_yaml(tmp_path)
        assert cfg.model_dim == 192
        assert cfg.num_layers == 4
        assert cfg.dropout == 0.1

    def test_from_yaml_missing_file(self) -> None:
        with pytest.raises(FileNotFoundError):
            SagaConfig.from_yaml("/nonexistent/path/config.yaml")
