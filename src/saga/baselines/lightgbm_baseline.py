"""LightGBM gradient-boosted tree baseline (B3).

One regressor per forecast horizon per quantile level, trained with pinball loss.
Reference: Ke, G. et al. (2017). LightGBM: A highly efficient gradient boosting decision
tree. Advances in Neural Information Processing Systems, 30, 3146-3154.
"""

from __future__ import annotations

from typing import Any

import numpy as np

try:
    import lightgbm as lgb

    _LIGHTGBM_AVAILABLE = True
except ImportError:
    _LIGHTGBM_AVAILABLE = False


class LightGBMBaseline:
    """LightGBM baseline: one quantile regressor per (horizon, quantile_level) pair.

    Args:
        quantile_levels: Tuple of quantile levels (default 7 SAGA levels).
        horizons: List of forecast horizons to train (default [1, 5, 10, 20]).
        lgb_params: Additional LightGBM parameters to pass to lgb.train.

    Attributes:
        models: Dict mapping (horizon, quantile_level) to trained lgb.Booster.
    """

    def __init__(
        self,
        quantile_levels: tuple[float, ...] = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95),
        horizons: list[int] | None = None,
        lgb_params: dict[str, Any] | None = None,
    ) -> None:
        if not _LIGHTGBM_AVAILABLE:
            raise ImportError("lightgbm is required for LightGBMBaseline.")
        self.quantile_levels = quantile_levels
        self.horizons = horizons or [1, 5, 10, 20]
        self.lgb_params = lgb_params or {}
        self.models: dict[tuple[int, float], Any] = {}

    def fit(
        self,
        X_train: np.ndarray,
        y_train: dict[int, np.ndarray],
        num_boost_round: int = 500,
    ) -> None:
        """Fit one quantile regressor per (horizon, quantile_level) pair.

        Args:
            X_train: Feature matrix of shape (n_train, n_features).
            y_train: Dict mapping horizon h to log-earnings targets of shape (n_train,).
            num_boost_round: Number of boosting rounds (default 500).
        """
        for h in self.horizons:
            if h not in y_train:
                continue
            for q in self.quantile_levels:
                params = {
                    "objective": "quantile",
                    "alpha": q,
                    "verbose": -1,
                    **self.lgb_params,
                }
                dataset = lgb.Dataset(X_train, label=y_train[h])
                self.models[(h, q)] = lgb.train(
                    params, dataset, num_boost_round=num_boost_round
                )

    def predict_quantiles(
        self,
        X: np.ndarray,
        horizon: int,
    ) -> np.ndarray:
        """Predict quantiles at a given horizon.

        Args:
            X: Feature matrix of shape (n, n_features).
            horizon: Forecast horizon h.

        Returns:
            Array of shape (n, len(quantile_levels)) with quantile predictions.

        Raises:
            RuntimeError: If the model has not been fitted for the given horizon.
        """
        preds = []
        for q in self.quantile_levels:
            key = (horizon, q)
            if key not in self.models:
                raise RuntimeError(f"Model not fitted for horizon {horizon}, quantile {q}.")
            preds.append(self.models[key].predict(X))
        return np.stack(preds, axis=-1)
