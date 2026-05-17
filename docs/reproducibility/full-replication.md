# Full replication

This document describes the two replication levels available for the SAGA manuscript results.

## Level 1: pipeline-level replication (synthetic mirror)

Pipeline-level replication uses the synthetic mirror dataset (Zenodo DOI `10.5281/zenodo.20260287`)
and runs the full analysis workflow from training through evaluation. All scripts and notebooks
in this repository support pipeline-level replication without any access to the protected LISA
microdata. See [quickstart.md](quickstart.md) for the five-command path.

The expected CRPS reduction on the synthetic mirror at $h=10$ is approximately $31.9\% \pm 0.5$ pp,
depending on training seed. Deviations larger than 0.5 percentage points should be reported
as a reproducibility issue.

## Level 2: bit-level replication (MONA access required)

Bit-level replication requires access to the real LISA microdata inside the Statistics Sweden
MONA secure compute environment. See
[docs/data/mona-secure-environment.md](../data/mona-secure-environment.md) for the access
procedure. The specific project that produced the manuscript results is SCB-MONA-2026-147
(not transferable to other researchers); an independent MONA project is required for bit-level
replication.

Inside MONA, the full replication script sequence is:

```bash
# Assumes data is available at ${SAGA_DATA_ROOT}/real/lisa_panel.parquet
# as assembled from the LISA register extract.

# 1. Preprocess the LISA panel (apply sample selection rules SR1-SR4)
bash scripts/preprocess_lisa_data.sh

# 2. Estimate all five baselines
bash scripts/estimate_gkos.sh
bash scripts/estimate_ar1_fe.sh
bash scripts/train_lightgbm_baseline.sh
bash scripts/train_lstm_baseline.sh
bash scripts/train_ff_baseline.sh

# 3. Train SAGA (5 seeds, 8 x A100 40 GB, approximately 14.8 hours per seed)
bash scripts/train_saga.sh

# 4. Calibrate conformal intervals (all horizons h=1 to h=20)
bash scripts/calibrate_conformal.sh

# 5. Run inference on the test set (cohorts 1983-1985)
bash scripts/run_inference.sh

# 6. Evaluate forecast accuracy (Table I, Table X)
bash scripts/evaluate_forecast_accuracy.sh

# 7. Run all ablations (Table VI)
bash scripts/run_all_ablations.sh

# 8. Run all robustness checks (Table VII)
bash scripts/run_all_robustness.sh

# 9. Run all placebo tests (Table IX)
bash scripts/run_all_placebos.sh

# 10. Aggregate lifetime earnings (Table IV)
bash scripts/aggregate_lifetime_earnings.sh

# 11. Run tax microsimulation (Table V)
bash scripts/run_tax_microsimulation.sh

# 12. Run interpretability analysis
bash scripts/run_interpretability_analysis.sh

# 13. Verify overall reproducibility
bash scripts/verify_reproducibility.sh
```

## Numerical tolerance

Results reported in the manuscript are the mean across five training seeds. Individual-seed
CRPS values at $h=10$ vary by approximately $\pm 0.003$ around the mean. All table values in
the manuscript are rounded to the precision shown.

## See also

- [Quickstart](quickstart.md)
- [Docker environment](docker-environment.md)
- [Seed list](seed-list.md)
- [Wall-clock budgets](wall-clock-budgets.md)
- [MONA secure environment](../data/mona-secure-environment.md)
