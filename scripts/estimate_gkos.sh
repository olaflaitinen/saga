#!/usr/bin/env bash
# Estimate the GKOS baseline (GMM Gaussian mixture model).
# Requires: SAGA_DATA_ROOT with real or synthetic LISA panel.
# Usage: bash scripts/estimate_gkos.sh

set -euo pipefail

DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/baselines/gkos}"

mkdir -p "${OUTPUT_DIR}"

python -m saga.baselines.gkos_estimator \
  --data-root "${DATA_ROOT}" \
  --output-dir "${OUTPUT_DIR}"

echo "INFO: GKOS estimation complete. Parameters in ${OUTPUT_DIR}/"
