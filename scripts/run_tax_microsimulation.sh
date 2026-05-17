#!/usr/bin/env bash
# Apply the 2022 Swedish tax schedule to lifetime earnings paths.
# Produces Table V (effective average tax rate decomposition).
# Usage: bash scripts/run_tax_microsimulation.sh

set -euo pipefail

TAX_CONFIG="${SAGA_TAX_CONFIG:-configs/tax_microsimulation_2022_schedule.yaml}"
LIFETIME_DIR="${SAGA_OUTPUT_DIR:-outputs}/lifetime"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs}/tax_microsim"

mkdir -p "${OUTPUT_DIR}"

python -m saga.evaluation.run_tax_microsimulation \
  --tax-config "${TAX_CONFIG}" \
  --lifetime-dir "${LIFETIME_DIR}" \
  --output-dir "${OUTPUT_DIR}"

echo "INFO: Tax microsimulation complete. Results in ${OUTPUT_DIR}/"
