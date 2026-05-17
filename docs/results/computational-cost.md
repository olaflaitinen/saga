# Computational cost

This document reports the training throughput, inference latency, and memory footprint of the
SAGA model on NVIDIA A100 40 GB hardware.

## Table of contents

- [Training cost](#training-cost)
- [Inference latency](#inference-latency)
- [Memory footprint](#memory-footprint)
- [Comparison to GKOS](#comparison-to-gkos)
- [See also](#see-also)

## Training cost

| Metric | Value |
|---|---|
| Devices | 8 NVIDIA A100 40 GB |
| Per-seed wall-clock time | 14.8 hours |
| Per-seed accelerator hours ($8 \times 14.8$) | approximately 118 GPU-hours |
| Total accelerator hours (5 seeds) | approximately 590 GPU-hours |
| Peak per-device GPU memory | 34.2 GB |
| Effective batch size | $16{,}384$ sequences ($512 \times 4 \times 8$) |
| Total optimization steps | 300,000 |
| Precision | bfloat16 activations, float32 accumulation |

Full training throughput benchmarks are documented in
[benchmarks/runtime/train_throughput_a100.md](../../benchmarks/runtime/train_throughput_a100.md).

## Inference latency

Per-individual lifetime inference ($M=500$ Monte Carlo paths, $h$ up to 20 forecast steps):
**43 milliseconds** per individual on a single A100 40 GB GPU.

This figure enables processing the full test set of 141,074 individuals in approximately
1.7 hours on a single A100 GPU. Full latency benchmarks are documented in
[benchmarks/runtime/inference_latency_a100.md](../../benchmarks/runtime/inference_latency_a100.md).

## Memory footprint

Peak per-device GPU memory during training: **34.2 GB** (out of 40 GB available on the A100
SXM4 40 GB used for training). The 34.2 GB figure corresponds to the peak occupancy during a
forward-backward pass at the full per-device batch size of 512 sequences, with bfloat16
activations and float32 gradient accumulation.

Peak per-device memory during inference: substantially lower than 34.2 GB (approximately 6-8 GB
for the model weights plus activation memory for 512 sequences), but not formally benchmarked
because inference is typically run on smaller batch sizes.

Full memory benchmarks are documented in
[benchmarks/memory/peak_memory_a100.md](../../benchmarks/memory/peak_memory_a100.md).

## Comparison to GKOS

The GKOS model is estimated by GMM and has no GPU requirement. The estimation runs on CPU
and requires approximately 18.3 hours on a modern 32-core workstation for the full training
cohort. This comparison is apples-to-oranges: GKOS estimation uses a CPU-parallelized GMM
optimizer while SAGA training uses 8 A100 GPUs. The GKOS 18.3 CPU-hour figure is included
here for completeness, not as a comparable cost metric. SAGA's per-GPU training time
(14.8 hours on 8 GPUs in parallel) is not directly comparable to a CPU-only estimation.

## See also

- [Reproducibility: wall-clock budgets](../reproducibility/wall-clock-budgets.md)
- [Reproducibility: hardware notes](../reproducibility/hardware-notes.md)
- [Benchmarks: training throughput](../../benchmarks/runtime/train_throughput_a100.md)
- [Benchmarks: inference latency](../../benchmarks/runtime/inference_latency_a100.md)
- [Benchmarks: peak memory](../../benchmarks/memory/peak_memory_a100.md)
