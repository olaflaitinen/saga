# Appendix G: reproducibility

This appendix documents the full reproducibility record for the SAGA manuscript results.
It cross-references the ethics approval, the MONA data access project, the training seeds,
the hardware configuration, and the synthetic mirror.

## Ethics and data governance

All empirical results in the manuscript were computed within the Statistics Sweden MONA
(Microdata Online Access) secure compute environment under project SCB-MONA-2026-147.
The study received ethics approval from the Swedish Ethical Review Authority under decision
reference 2026-04127-01. No row-level data, no individual-level predictions, and no
intermediate outputs linked to identifiable individuals left the secure environment.

Bit-level replication requires independent MONA project approval from Statistics Sweden.
The application procedure is documented in
[docs/data/mona-secure-environment.md](../data/mona-secure-environment.md).

Pipeline-level replication using the synthetic mirror (DOI: `10.5281/zenodo.20260287`) is possible
without MONA access, using the scripts and notebooks in this repository. See
[docs/reproducibility/quickstart.md](../reproducibility/quickstart.md) for the five-command
quickstart path.

## Training seeds

The five training seeds are: 20260601, 20260602, 20260603, 20260604, 20260605.

All five seeds are documented in [docs/reproducibility/seed-list.md](../reproducibility/seed-list.md).
Results in the manuscript are reported as the mean across all five seeds. Standard deviations
across seeds are reported in the supplementary material.

## Hardware configuration

Training was conducted on 8 NVIDIA A100 40 GB GPUs. The per-seed wall-clock time is 14.8 hours.
Per-seed accelerator hours are approximately 118. Peak per-device GPU memory is 34.2 GB.

Details are documented in:
- [docs/reproducibility/hardware-notes.md](../reproducibility/hardware-notes.md)
- [docs/reproducibility/wall-clock-budgets.md](../reproducibility/wall-clock-budgets.md)
- [benchmarks/runtime/train_throughput_a100.md](../../benchmarks/runtime/train_throughput_a100.md)

## Software stack

- Python 3.11
- PyTorch 2.4 with CUDA 12.1
- SAGA version 1.0.0 (this repository, tag v1.0.0)
- Full dependency list: `environment.yaml`
- Docker image: `olaflaitinen/saga:v1.0.0`

## Synthetic mirror

The synthetic mirror dataset (500,000 individuals) hosted at Zenodo under DOI
`10.5281/zenodo.20260287` was generated from SAGA's predictive distribution as documented in
[Appendix D](appendix-d-synthetic-data-protocol.md). The moment match to the real LISA panel
is within 1.8% at every age within every demographic subgroup. Membership inference AUC: 0.512.

## Repository checksum verification

The `scripts/verify_reproducibility.sh` script verifies the integrity of the repository by:

1. Checking that the installed `saga` package version matches the repository tag (`v1.0.0`).
2. Verifying the SHA-256 checksums of the synthetic mirror parquet files against
   `data/synthetic/checksum.sha256`.
3. Running the full unit and integration test suites.
4. Executing the quickstart notebook and asserting that the headline CRPS reduction on the
   synthetic mirror is within 0.5 percentage points of 31.9%.

## Self-check

The `SELF_CHECK.md` file at the repository root reports the pass/fail status of all 25
acceptance criteria (A1 through A25) as of the v1.0.0 release.

## See also

- [Reproducibility: quickstart](../reproducibility/quickstart.md)
- [Reproducibility: full replication](../reproducibility/full-replication.md)
- [Reproducibility: seed list](../reproducibility/seed-list.md)
- [Ethics: ethical approval](../ethics/ethical-approval.md)
- [Data: MONA secure environment](../data/mona-secure-environment.md)
