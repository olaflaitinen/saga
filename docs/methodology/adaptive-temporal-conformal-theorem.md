# Adaptive Temporal Conformal theorem (Theorem 2)

See the full statement and proof in
[Appendix E: Adaptive Temporal Conformal Prediction](../paper-mirror/appendix-e-adaptive-temporal-conformal.md).

## Key parameters at $h=10$

- Calibration set size: $n_{10} = 14{,}107$ unique individuals
- Empirical Lipschitz constant: $\hat{L}_{10} = 0.65$
- Predicted worst-case coverage deviation: approximately $0.024$
- Observed worst-case deviation (Q1, 90% nominal): 2.4 percentage points $= 0.024$

## Source code

- `src/saga/conformal/adaptive_temporal.py` - AdaptiveTemporalConformalCalibrator class

## See also

- [Split conformal calibration](split-conformal-calibration.md)
- [Results: calibration coverage](../results/calibration-coverage.md)
- [Appendix E](../paper-mirror/appendix-e-adaptive-temporal-conformal.md)
