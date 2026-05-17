#!/usr/bin/env bash
# Export the SAGA synthetic mirror dataset.
#
# This script wraps scripts/generate_synthetic_dataset.py and produces the
# five files required for the Zenodo deposit:
#
#   data/synthetic/synthetic_train.parquet
#   data/synthetic/synthetic_cal.parquet
#   data/synthetic/synthetic_test.parquet
#   data/synthetic/moment_validation.csv
#   data/synthetic/SHA256SUMS.txt
#
# Inside the SCB MONA environment this script is run after training to generate
# the canonical 500,000-individual synthetic mirror from the trained SAGA model
# and the real LISA marginal distributions.  Outside MONA (e.g. on the public
# GitHub repository) it runs generate_synthetic_dataset.py directly, which uses
# a parametric AR(1) model instead of the trained SAGA decoder.
#
# Usage
# -----
#   bash scripts/export_synthetic_mirror.sh
#   bash scripts/export_synthetic_mirror.sh --n-individuals 50000   # quick test
#
# Requirements: conda environment "saga" must be active.

set -euo pipefail

OUTPUT_DIR="${OUTPUT_DIR:-data/synthetic}"
SEED="${SEED:-20260601}"
N_INDIVIDUALS="${N_INDIVIDUALS:-500000}"

# Parse optional CLI overrides
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)   OUTPUT_DIR="$2";   shift 2 ;;
    --seed)         SEED="$2";         shift 2 ;;
    --n-individuals) N_INDIVIDUALS="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

echo "================================================================"
echo "SAGA synthetic mirror export"
echo "================================================================"
echo "  Output directory : ${OUTPUT_DIR}"
echo "  Seed             : ${SEED}"
echo "  N individuals    : ${N_INDIVIDUALS}"
echo ""

mkdir -p "${OUTPUT_DIR}"

python scripts/generate_synthetic_dataset.py \
  --output-dir "${OUTPUT_DIR}" \
  --seed "${SEED}" \
  --n-individuals "${N_INDIVIDUALS}"

echo ""
echo "================================================================"
echo "Export complete.  Files are in ${OUTPUT_DIR}/"
echo ""
echo "Next steps:"
echo "  1. Log in to https://zenodo.org and create a new upload."
echo "  2. Upload all five files from ${OUTPUT_DIR}/:"
echo "       synthetic_train.parquet"
echo "       synthetic_cal.parquet"
echo "       synthetic_test.parquet"
echo "       moment_validation.csv"
echo "       SHA256SUMS.txt"
echo "  3. Fill in the metadata from .zenodo.json (title, authors, keywords, etc.)."
echo "  4. Publish the deposit and note the assigned DOI."
echo "  5. Replace 10.5281/zenodo.20260287 across the repository:"
echo "       grep -rl '10.5281/zenodo.20260287' . | xargs sed -i 's/10.5281/zenodo.20260287/10.5281\/zenodo.XXXXXXX/g'"
echo "================================================================"
