#!/usr/bin/env bash
# Run SAGA inference on the test set and save outputs to outputs/inference/.
# Usage: bash scripts/run_inference.sh

set -euo pipefail

CONFIG="${SAGA_CONFIG:-configs/saga_main.yaml}"
DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
CHECKPOINT_DIR="${SAGA_CHECKPOINT_DIR:-outputs/checkpoints}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/inference}"
MC_CONFIG="${SAGA_MC_CONFIG:-configs/lifetime_monte_carlo.yaml}"

mkdir -p "${OUTPUT_DIR}"

python -m saga.inference.run_inference \
  --config "${CONFIG}" \
  --mc-config "${MC_CONFIG}" \
  --checkpoint-dir "${CHECKPOINT_DIR}" \
  --data-root "${DATA_ROOT}" \
  --split test \
  --output-dir "${OUTPUT_DIR}"

echo "INFO: Inference complete. Results in ${OUTPUT_DIR}/"
