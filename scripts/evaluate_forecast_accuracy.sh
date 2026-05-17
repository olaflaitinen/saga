#!/usr/bin/env bash
# Compute all forecast accuracy tables (Table I, Table X).
# Usage: bash scripts/evaluate_forecast_accuracy.sh

set -euo pipefail

INFERENCE_DIR="${SAGA_OUTPUT_DIR:-outputs}/inference"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs}/evaluation"

mkdir -p "${OUTPUT_DIR}"

python -m saga.evaluation.compute_accuracy_tables \
  --inference-dir "${INFERENCE_DIR}" \
  --output-dir "${OUTPUT_DIR}"

echo "INFO: Forecast evaluation complete. Tables in ${OUTPUT_DIR}/"
