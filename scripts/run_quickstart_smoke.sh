#!/usr/bin/env bash
# Quickstart smoke test: one seed, 50,000 steps, synthetic mirror.
# Expected wall-clock: approximately 2.5 hours on a single A100 40 GB GPU.
# Usage: bash scripts/run_quickstart_smoke.sh

set -euo pipefail

export SAGA_DATA_ROOT="data/synthetic"
export SAGA_OUTPUT_DIR="outputs/smoke"
export SAGA_SEED="20260601"

mkdir -p "${SAGA_OUTPUT_DIR}"

echo "INFO: Starting quickstart smoke test (1 seed, 50000 steps)."

python -m saga.training.train_loop \
  --config configs/saga_main.yaml \
  --seed "${SAGA_SEED}" \
  --total-steps 50000 \
  --data-root "${SAGA_DATA_ROOT}" \
  --output-dir "${SAGA_OUTPUT_DIR}/checkpoints/seed_${SAGA_SEED}"

bash scripts/calibrate_conformal.sh
bash scripts/run_inference.sh

python -m saga.evaluation.verify_crps \
  --expected-reduction "0.319" \
  --tolerance "0.010" \
  --inference-output "${SAGA_OUTPUT_DIR}/inference" \
  --baseline gkos

echo "INFO: Smoke test complete."
