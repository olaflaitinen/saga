#!/usr/bin/env bash
# Aggregate lifetime earnings using Monte Carlo sampling (M=500, r=2%).
# Requires: inference outputs in ${SAGA_OUTPUT_DIR}/inference.
# Usage: bash scripts/aggregate_lifetime_earnings.sh

set -euo pipefail

MC_CONFIG="${SAGA_MC_CONFIG:-configs/lifetime_monte_carlo.yaml}"
INFERENCE_DIR="${SAGA_OUTPUT_DIR:-outputs}/inference"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs}/lifetime"

mkdir -p "${OUTPUT_DIR}"

python -m saga.inference.aggregate_lifetime \
  --mc-config "${MC_CONFIG}" \
  --inference-dir "${INFERENCE_DIR}" \
  --output-dir "${OUTPUT_DIR}"

echo "INFO: Lifetime aggregation complete. Results in ${OUTPUT_DIR}/"
