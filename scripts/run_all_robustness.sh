#!/usr/bin/env bash
# Run all 11 robustness checks (R1 through R9, including R5a-R5c) in sequence.
# Usage: bash scripts/run_all_robustness.sh

set -euo pipefail

DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/robustness}"

ROBUSTNESS_LABELS=("R1" "R2" "R3" "R4" "R5a" "R5b" "R5c" "R6" "R7" "R8" "R9")

mkdir -p "${OUTPUT_DIR}"

for LABEL in "${ROBUSTNESS_LABELS[@]}"; do
  echo "INFO: Running robustness check ${LABEL}..."
  python -m saga.evaluation.run_robustness \
    --label "${LABEL}" \
    --data-root "${DATA_ROOT}" \
    --output-dir "${OUTPUT_DIR}/${LABEL}"
  echo "INFO: Robustness check ${LABEL} complete."
done

echo "INFO: All robustness checks complete. Results in ${OUTPUT_DIR}/"
