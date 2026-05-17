#!/usr/bin/env bash
# Run all three placebo and falsification tests (P1, P2, P3).
# Usage: bash scripts/run_all_placebos.sh

set -euo pipefail

DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/placebos}"

PLACEBO_LABELS=("P1" "P2" "P3")

mkdir -p "${OUTPUT_DIR}"

for LABEL in "${PLACEBO_LABELS[@]}"; do
  echo "INFO: Running placebo test ${LABEL}..."
  python -m saga.evaluation.run_placebo \
    --label "${LABEL}" \
    --data-root "${DATA_ROOT}" \
    --output-dir "${OUTPUT_DIR}/${LABEL}"
  echo "INFO: Placebo test ${LABEL} complete."
done

echo "INFO: All placebo tests complete. Results in ${OUTPUT_DIR}/"
