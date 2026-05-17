#!/usr/bin/env bash
# Train SAGA across all five seeds.
# Usage: bash scripts/train_saga.sh
# Set SAGA_SEED to override and run a single seed.

set -euo pipefail

CONFIG="${SAGA_CONFIG:-configs/saga_main.yaml}"
DATA_ROOT="${SAGA_DATA_ROOT:-data/synthetic}"
OUTPUT_DIR="${SAGA_OUTPUT_DIR:-outputs/checkpoints}"

SEEDS=(20260601 20260602 20260603 20260604 20260605)

if [ -n "${SAGA_SEED:-}" ]; then
  SEEDS=("${SAGA_SEED}")
  echo "INFO: Running single seed ${SAGA_SEED}."
fi

mkdir -p "${OUTPUT_DIR}"

for SEED in "${SEEDS[@]}"; do
  echo "INFO: Training seed ${SEED}..."
  python -m saga.training.train_loop \
    --config "${CONFIG}" \
    --seed "${SEED}" \
    --data-root "${DATA_ROOT}" \
    --output-dir "${OUTPUT_DIR}/seed_${SEED}"
  echo "INFO: Seed ${SEED} complete."
done

echo "INFO: All seeds complete. Checkpoints in ${OUTPUT_DIR}/"
