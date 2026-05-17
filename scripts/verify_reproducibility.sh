#!/usr/bin/env bash
# Verify the reproducibility of the SAGA pipeline.
# Checks package version, data checksums, test suite, and quickstart CRPS.
# Usage: bash scripts/verify_reproducibility.sh

set -euo pipefail

EXPECTED_VERSION="1.0.0"
CRPS_TOLERANCE="0.005"
EXPECTED_CRPS_REDUCTION="0.319"

echo "=== SAGA Reproducibility Verification ==="

echo "--- Step 1: Verify package version ---"
INSTALLED_VERSION=$(python -c "import saga; print(saga.__version__)")
if [ "${INSTALLED_VERSION}" != "${EXPECTED_VERSION}" ]; then
  echo "ERROR: Expected saga version ${EXPECTED_VERSION}, got ${INSTALLED_VERSION}."
  exit 1
fi
echo "PASS: saga version ${INSTALLED_VERSION}"

echo "--- Step 2: Verify synthetic mirror checksums ---"
if [ -f "data/synthetic/checksum.sha256" ]; then
  sha256sum --check data/synthetic/checksum.sha256
  echo "PASS: Synthetic mirror checksums verified."
else
  echo "WARN: data/synthetic/checksum.sha256 not found. Run download_synthetic_mirror.sh first."
fi

echo "--- Step 3: Run unit and integration tests ---"
python -m pytest tests/unit tests/integration -q --tb=short
echo "PASS: Test suite passed."

echo "--- Step 4: Verify quickstart CRPS reduction on synthetic mirror ---"
python -m saga.evaluation.verify_crps \
  --expected-reduction "${EXPECTED_CRPS_REDUCTION}" \
  --tolerance "${CRPS_TOLERANCE}" \
  --inference-output outputs/inference \
  --baseline gkos
echo "PASS: CRPS reduction within tolerance."

echo "=== All verification checks passed. ==="
