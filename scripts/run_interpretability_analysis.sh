#!/usr/bin/env bash
# Run interpretability analysis (attention aggregation and integrated gradients).
# Usage: bash scripts/run_interpretability_analysis.sh

set -euo pipefail

DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
CHECKPOINT_DIR="${SAGA_CHECKPOINT_DIR:-outputs/checkpoints}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs}/interpretability"

mkdir -p "${OUTPUT_DIR}"

python -m saga.interpretability.run_analysis \
  --data-root "${DATA_ROOT}" \
  --checkpoint-dir "${CHECKPOINT_DIR}" \
  --output-dir "${OUTPUT_DIR}" \
  --n-individuals 500

echo "INFO: Interpretability analysis complete. Results in ${OUTPUT_DIR}/"
