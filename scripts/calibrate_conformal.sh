#!/usr/bin/env bash
# Calibrate conformal prediction intervals for horizons h=1 to h=20.
# Saves calibration quantiles to outputs/conformal/conformal_quantiles.npz.
# Usage: bash scripts/calibrate_conformal.sh

set -euo pipefail

CONFIG="${SAGA_CONFIG:-configs/saga_main.yaml}"
DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
CHECKPOINT_DIR="${SAGA_CHECKPOINT_DIR:-outputs/checkpoints}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/conformal}"

mkdir -p "${OUTPUT_DIR}"

python -m saga.conformal.calibrate \
  --config "${CONFIG}" \
  --checkpoint-dir "${CHECKPOINT_DIR}" \
  --data-root "${DATA_ROOT}" \
  --split calibration \
  --horizons 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 \
  --output-dir "${OUTPUT_DIR}"

echo "INFO: Conformal calibration complete. Quantiles in ${OUTPUT_DIR}/"
