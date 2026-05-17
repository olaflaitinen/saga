# Inference latency benchmark: NVIDIA A100 40 GB

Hardware: NVIDIA A100 SXM4 40 GB, CUDA 12.1, cuDNN 8.9.2.
Measurement: 141,074 test-set individuals, batch size 512, M=500 Monte Carlo paths, h=20.

| Operation | Latency (ms/individual) |
|---|---|
| Tokenization | 1.2 |
| Transformer forward pass (10-year context) | 4.8 |
| Autoregressive decoding (h=1 to h=20, single path) | 9.3 |
| Monte Carlo sampling (M=500 paths, vectorized) | 31.4 |
| Lifetime discounting and aggregation | 1.1 |
| **Total (M=500, h=20)** | **43.0** |

Full test set throughput: 141,074 individuals in approximately 1.7 hours on a single A100.
