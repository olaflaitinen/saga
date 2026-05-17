# Seed list

The five training seeds used for all SAGA results in the manuscript are:

| Seed | Python random | numpy | torch |
|---|---|---|---|
| 20260601 | 20260601 | 20260601 | 20260601 |
| 20260602 | 20260602 | 20260602 | 20260602 |
| 20260603 | 20260603 | 20260603 | 20260603 |
| 20260604 | 20260604 | 20260604 | 20260604 |
| 20260605 | 20260605 | 20260605 | 20260605 |

For each seed, the same integer is used to seed Python's `random` module, `numpy.random`,
and `torch.manual_seed` / `torch.cuda.manual_seed_all`. This is enforced by the
`src/saga/utils/seed.py` utility function `set_all_seeds(seed: int)`.

Manuscript results are the mean across all five seeds. Standard deviations across seeds
are reported in the manuscript supplementary material.

## Reproducing a single-seed run

```bash
SAGA_SEED=20260601 bash scripts/train_saga.sh
```

See [configs/saga_main.yaml](../../configs/saga_main.yaml) for the `seed` configuration key.

## See also

- [Full replication](full-replication.md)
- [Source: src/saga/utils/seed.py](../../src/saga/utils/seed.py)
