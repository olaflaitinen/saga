#!/usr/bin/env bash
# Download the SAGA synthetic mirror dataset from Zenodo and verify checksums.
# Usage: bash scripts/download_synthetic_mirror.sh
# Requires: curl, sha256sum

set -euo pipefail

ZENODO_DOI="10.5281/zenodo.20260287"
TARGET_DIR="data/synthetic"
CHECKSUM_FILE="${TARGET_DIR}/SHA256SUMS.txt"

echo "INFO: Synthetic mirror Zenodo DOI: ${ZENODO_DOI}"
echo "INFO: Target directory: ${TARGET_DIR}"

if [ "${ZENODO_DOI}" = "__TBD_ZENODO_DOI__" ]; then
  echo "ERROR: The Zenodo DOI is not yet finalized. Replace __TBD_ZENODO_DOI__ in this"
  echo "       script with the actual DOI once the Zenodo deposit is published."
  echo "       Example: ZENODO_DOI=\"10.5281/zenodo.XXXXXXX\""
  exit 1
fi

# Extract the Zenodo record ID from the full DOI (e.g. 10.5281/zenodo.12345678 -> 12345678)
ZENODO_RECORD_ID="${ZENODO_DOI##*/}"
mkdir -p "${TARGET_DIR}"

BASE_URL="https://zenodo.org/records/${ZENODO_RECORD_ID}/files"
FILES=(
  "synthetic_train.parquet"
  "synthetic_cal.parquet"
  "synthetic_test.parquet"
  "moment_validation.csv"
  "SHA256SUMS.txt"
)

for FILE in "${FILES[@]}"; do
  DEST="${TARGET_DIR}/${FILE}"
  if [ -f "${DEST}" ]; then
    echo "INFO: ${FILE} already present, skipping download."
  else
    echo "INFO: Downloading ${FILE} ..."
    curl --fail --location --progress-bar \
      "${BASE_URL}/${FILE}?download=1" \
      --output "${DEST}"
  fi
done

echo "INFO: Verifying SHA-256 checksums ..."
sha256sum --check "${CHECKSUM_FILE}"
echo "INFO: All checksums verified. Synthetic mirror is ready in ${TARGET_DIR}/"
