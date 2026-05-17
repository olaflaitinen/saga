# Training throughput benchmark: NVIDIA A100 40 GB

Hardware: 8 x NVIDIA A100 SXM4 40 GB, NVLink 3.0, CUDA 12.1, cuDNN 8.9.2.

| Metric | Value |
|---|---|
| Per-device batch size | 512 sequences |
| Gradient accumulation steps | 4 |
| Effective batch size | 16,384 |
| Per-device GPU memory peak | 34.2 GB |
| Steps per second (8 GPU aggregate) | approximately 5.6 |
| Per-seed wall-clock time (300,000 steps) | 14.8 hours |
| Per-seed GPU-hours | approximately 118 |
| Precision | bfloat16 activations, float32 accumulation |

These benchmarks are from the production training run in the Statistics Sweden MONA
environment and may differ slightly from runs on commodity A100 hardware due to
interconnect and storage differences.
