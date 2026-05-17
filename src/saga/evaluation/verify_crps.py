"""CLI module to verify the CRPS reduction against the headline manuscript value.

Used by scripts/verify_reproducibility.sh and scripts/run_quickstart_smoke.sh.

Usage:
    python -m saga.evaluation.verify_crps \\
        --expected-reduction 0.319 \\
        --tolerance 0.005 \\
        --inference-output outputs/inference \\
        --baseline gkos
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np


def main() -> None:
    """Verify the CRPS reduction from inference outputs."""
    parser = argparse.ArgumentParser(description="Verify CRPS reduction.")
    parser.add_argument("--expected-reduction", type=float, required=True)
    parser.add_argument("--tolerance", type=float, default=0.005)
    parser.add_argument("--inference-output", type=str, required=True)
    parser.add_argument("--baseline", type=str, default="gkos")
    args = parser.parse_args()

    output_dir = Path(args.inference_output)
    saga_crps_path = output_dir / "saga_crps_h10.npy"
    baseline_crps_path = output_dir / f"{args.baseline}_crps_h10.npy"

    if not saga_crps_path.exists():
        print(f"ERROR: SAGA CRPS file not found: {saga_crps_path}")
        print("       Run scripts/run_inference.sh before verifying.")
        sys.exit(1)

    if not baseline_crps_path.exists():
        print(f"ERROR: Baseline CRPS file not found: {baseline_crps_path}")
        sys.exit(1)

    crps_saga = float(np.load(str(saga_crps_path)))
    crps_baseline = float(np.load(str(baseline_crps_path)))

    if crps_baseline <= 0:
        print(f"ERROR: Baseline CRPS is non-positive: {crps_baseline:.4f}")
        sys.exit(1)

    actual_reduction = (crps_baseline - crps_saga) / crps_baseline
    expected = args.expected_reduction
    tol = args.tolerance

    print(f"SAGA CRPS at h=10:          {crps_saga:.4f}")
    print(f"Baseline ({args.baseline}) CRPS at h=10: {crps_baseline:.4f}")
    print(f"Actual CRPS reduction:      {actual_reduction:.4f} ({actual_reduction:.1%})")
    print(f"Expected CRPS reduction:    {expected:.4f} (+/- {tol:.4f})")

    if abs(actual_reduction - expected) > tol:
        print(
            f"FAIL: CRPS reduction {actual_reduction:.4f} deviates from expected "
            f"{expected:.4f} by more than tolerance {tol:.4f}."
        )
        sys.exit(1)

    print("PASS: CRPS reduction is within tolerance.")


if __name__ == "__main__":
    main()
