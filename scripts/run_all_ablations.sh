#!/usr/bin/env bash
# Run all 13 ablation variants (A1 through A13) in sequence.
# Usage: bash scripts/run_all_ablations.sh

set -euo pipefail

DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/ablations}"

ABLATION_LABELS=("A1" "A2" "A3" "A4" "A5" "A6" "A7" "A8" "A9" "A10" "A11" "A12" "A13")

mkdir -p "${OUTPUT_DIR}"

for LABEL in "${ABLATION_LABELS[@]}"; do
  echo "INFO: Running ablation ${LABEL}..."
  python -m saga.evaluation.run_ablation \
    --label "${LABEL}" \
    --data-root "${DATA_ROOT}" \
    --output-dir "${OUTPUT_DIR}/${LABEL}" \
    --seed 20260601
  echo "INFO: Ablation ${LABEL} complete."
done

echo "INFO: All ablations complete. Results in ${OUTPUT_DIR}/"
