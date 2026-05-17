# Hardware notes

## Training hardware

| Attribute | Value |
|---|---|
| GPU model | NVIDIA A100 SXM4 40 GB |
| Number of GPUs | 8 |
| CUDA version | 12.1 |
| cuDNN version | 8.9.2 |
| Interconnect | NVLink 3.0 |
| CPU (host) | 2 x Intel Xeon Platinum 8358 (32 cores each) |
| Host RAM | 512 GB |
| Storage | NVMe SSD, internal MONA project storage |
| Operating system | Ubuntu 22.04 LTS |

## Training performance

- Per-seed wall-clock time: 14.8 hours
- Per-seed GPU-hours: approximately 118 (8 GPUs x 14.8 h)
- Total GPU-hours for 5 seeds: approximately 590 GPU-hours
- Peak per-device GPU memory: 34.2 GB

## Minimum hardware for pipeline-level replication

The full 5-seed training run from the manuscript requires 8 x A100 40 GB GPUs. For
pipeline-level replication on the synthetic mirror with reduced seeds and steps, the minimum
requirements are:

| Tier | GPU | RAM | Training time |
|---|---|---|---|
| Recommended | 1 x A100 40 GB | 32 GB | approximately 3-5 hours (smoke test) |
| Supported | 1 x A100 80 GB | 32 GB | approximately 3-4 hours |
| Supported | 1 x RTX 4090 24 GB | 32 GB | approximately 6-8 hours (reduce batch size) |
| CPU only | None | 64 GB | Multiple days |

For CPU-only mode, set the batch size to 64 in `configs/saga_main.yaml` and expect
approximately 40x slower training.

## Known hardware-specific considerations

- The 34.2 GB peak GPU memory footprint is close to the 40 GB capacity of the A100 SXM4.
  On GPUs with less than 36 GB of VRAM, reduce `per_device_batch_size` in
  `configs/saga_main.yaml` from 512 to 256 and increase `gradient_accumulation_steps` from
  4 to 8 to maintain the effective batch size of 16,384.
- On RTX 4090 (24 GB VRAM), `per_device_batch_size` must be 128 or lower with
  `gradient_accumulation_steps` 128 to maintain effective batch size. This will increase
  wall-clock time substantially.

## See also

- [Wall-clock budgets](wall-clock-budgets.md)
- [Computational cost](../results/computational-cost.md)
- [Benchmarks: training throughput](../../benchmarks/runtime/train_throughput_a100.md)
