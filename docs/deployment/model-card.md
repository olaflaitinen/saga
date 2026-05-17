# Model card

This model card follows the format of [Mitchell et al. (2019)](https://arxiv.org/abs/1810.03993).

## Model details

| Attribute | Value |
|---|---|
| Name | SAGA (Sequence-Adaptive Generative Architecture) |
| Version | 1.0.0 |
| Date | 2026-05-18 |
| Type | Causally-masked autoregressive transformer decoder |
| Architecture | $L=6$ layers, $H=8$ heads, $d=384$, $10{,}872{,}960$ parameters |
| Developers | Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov, Hafize Gonca Comert |
| License | Apache 2.0 (code); CC BY-NC 4.0 (documentation and data) |
| Contact | olaf.laitinen@su.se |

## Intended use

- **Primary use:** Multi-horizon probabilistic forecasting of individual earnings trajectories
  in Scandinavian administrative panel data for academic research and policy analysis.
- **Intended users:** Academic researchers in economics, public finance, labor economics, and
  machine learning. Policy analysts and microsimulation modelers in national statistics offices.
- **Out-of-scope uses:** Individual-level financial decisioning (credit, insurance, employment),
  commercial targeting. See [ethics/dual-use-statement.md](../ethics/dual-use-statement.md).

## Training data

- **Source:** Swedish LISA administrative register, 1990-2022.
- **Training split:** Birth cohorts 1960-1979, 1,834,201 individuals.
- **Protected:** The training data are not publicly available. Access requires MONA project
  approval from Statistics Sweden. A synthetic mirror (500,000 individuals) is available at
  Zenodo (DOI: `10.5281/zenodo.20260287`).

## Evaluation data

- **Test set:** Birth cohorts 1983-1985, 141,074 individuals, LISA register.
- **Out-of-time holdout:** Birth cohorts 1986-1990, 287,391 individuals, LISA register.

## Performance

| Metric | $h=10$ | $h=20$ |
|---|---|---|
| CRPS (SAGA) | 0.318 | - |
| CRPS (GKOS baseline) | 0.467 | - |
| CRPS reduction vs. GKOS | 31.9% | 41.2% |
| MAE in log SEK (SAGA) | 0.512 | 0.631 |
| PICP at 90% nominal (%) | 90.3 | - |
| Worst subgroup PICP at 90% nominal (%) | 87.6 (Q1) | - |

## Limitations

- Training data are specific to the Swedish labor market (1960-1985 birth cohorts, 1990-2022).
  Performance on other national or temporal contexts is untested.
- The conformal coverage guarantee is marginal, not conditional. Subgroup coverage can deviate
  by up to $2.4$ percentage points at the 90% nominal level.
- The auxiliary feature imputation network may propagate errors in multi-step autoregressive
  decoding at long horizons.

## Ethical considerations

See [ethics/ethical-approval.md](../ethics/ethical-approval.md),
[ethics/data-governance.md](../ethics/data-governance.md),
[ethics/broader-impact.md](../ethics/broader-impact.md), and
[ethics/dual-use-statement.md](../ethics/dual-use-statement.md).

## Caveats and recommendations

For policy applications, use per-subgroup calibrated conformal intervals rather than the
marginal calibration. Periodically retrain the model as new LISA waves become available.
