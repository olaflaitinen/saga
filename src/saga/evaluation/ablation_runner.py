"""Ablation study runner.

Manages the 13 ablation variants (A1 through A13) defined in Table VI of the manuscript.
Each ablation is a SagaConfig variant with one component disabled or replaced.
"""

from __future__ import annotations

from dataclasses import dataclass

from saga.config import SagaConfig


@dataclass(frozen=True)
class AblationSpec:
    """Specification for a single ablation variant.

    Attributes:
        label: Short label (e.g., 'A1').
        description: Human-readable description.
        crps_manuscript: CRPS at h=10 from the manuscript (Table VI).
        config_overrides: Dict of SagaConfig field overrides.
    """

    label: str
    description: str
    crps_manuscript: float
    config_overrides: dict


_ABLATION_SPECS: list[AblationSpec] = [
    AblationSpec(
        label="headline",
        description="SAGA main model",
        crps_manuscript=0.318,
        config_overrides={},
    ),
    AblationSpec(
        label="A1",
        description="Drop occupation and industry features",
        crps_manuscript=0.334,
        config_overrides={"drop_occupation": True, "drop_industry": True},
    ),
    AblationSpec(
        label="A2",
        description="Drop family and household features",
        crps_manuscript=0.327,
        config_overrides={"drop_family_features": True},
    ),
    AblationSpec(
        label="A3",
        description="LSTM with parameter-matched 768 hidden",
        crps_manuscript=0.364,
        config_overrides={"use_lstm_backbone": True},
    ),
    AblationSpec(
        label="A4",
        description="Feed-forward on flattened 10-year window",
        crps_manuscript=0.493,
        config_overrides={"use_feedforward_backbone": True},
    ),
    AblationSpec(
        label="A5",
        description="Point head only (no quantile head)",
        crps_manuscript=0.347,
        config_overrides={"point_head_only": True},
    ),
    AblationSpec(
        label="A6",
        description="Drop year positional embedding",
        crps_manuscript=0.341,
        config_overrides={"year_embedding_dim": 0},
    ),
    AblationSpec(
        label="A7",
        description="Model dimension d=192, FFN=768",
        crps_manuscript=0.328,
        config_overrides={"model_dim": 192, "ffn_dim": 768},
    ),
    AblationSpec(
        label="A8",
        description="Model dimension d=768, FFN=3072",
        crps_manuscript=0.319,
        config_overrides={"model_dim": 768, "ffn_dim": 3072},
    ),
    AblationSpec(
        label="A9",
        description="Drop missingness subvector",
        crps_manuscript=0.324,
        config_overrides={"missingness_dim": 0},
    ),
    AblationSpec(
        label="A10",
        description="Drop age positional embedding",
        crps_manuscript=0.354,
        config_overrides={"age_embedding_dim": 0},
    ),
    AblationSpec(
        label="A11",
        description="SAGA backbone, point head only, conformal off",
        crps_manuscript=0.367,
        config_overrides={"point_head_only": True, "conformal_off": True},
    ),
    AblationSpec(
        label="A12",
        description="Conformal layer on GKOS backbone",
        crps_manuscript=0.451,
        config_overrides={"use_gkos_backbone": True},
    ),
    AblationSpec(
        label="A13",
        description="SAGA backbone, GKOS-style mixture output head",
        crps_manuscript=0.332,
        config_overrides={"use_mixture_head": True},
    ),
]


def get_ablation_spec(label: str) -> AblationSpec:
    """Retrieve an ablation specification by label.

    Args:
        label: Ablation label (e.g., 'A1', 'headline').

    Returns:
        The corresponding AblationSpec.

    Raises:
        KeyError: If no ablation with the given label exists.
    """
    for spec in _ABLATION_SPECS:
        if spec.label == label:
            return spec
    raise KeyError(f"No ablation spec with label '{label}'.")


def list_ablation_labels() -> list[str]:
    """Return all ablation labels in Table VI order.

    Returns:
        List of ablation label strings.
    """
    return [spec.label for spec in _ABLATION_SPECS]
