# data/synthetic/ -- synthetic mirror dataset

This directory is the download target for the synthetic mirror dataset.
Run the following command to download and verify the files:

```bash
bash scripts/download_synthetic_mirror.sh
```

This will download from Zenodo (DOI: `10.5281/zenodo.20260287`) and place the following files here:

- `synthetic_train.parquet` (350,000 individuals)
- `synthetic_cal.parquet` (75,000 individuals)
- `synthetic_test.parquet` (75,000 individuals)
- `moment_validation.csv`
- `checksum.sha256`

All parquet files conform to the schema in `data/schema.yaml`.

See [docs/data/synthetic-mirror.md](../../docs/data/synthetic-mirror.md) for details.
