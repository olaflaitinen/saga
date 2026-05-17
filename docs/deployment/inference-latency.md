# Inference latency

## Headline latency

**43 milliseconds per individual** for lifetime inference with $M=500$ Monte Carlo paths and
$h=20$ forecast steps, on a single NVIDIA A100 40 GB GPU.

This enables processing 141,074 test-set individuals in approximately 1.7 hours on a single
A100 GPU.

## Detailed latency benchmarks

On NVIDIA A100 40 GB, batch size 512 individuals:

| Operation | Latency (ms/individual) |
|---|---|
| Tokenization | 1.2 |
| Forward pass (10-year conditioning window) | 4.8 |
| Autoregressive decoding ($h=1$ to $h=20$, single path) | 9.3 |
| Monte Carlo sampling ($M=500$ paths, vectorized) | 31.4 |
| Lifetime discounting and aggregation | 1.1 |
| **Total ($M=500$, $h=20$)** | **43.0** |

The Monte Carlo sampling step dominates. The $M=500$ paths are generated in a single vectorized
batch for each individual, so the per-path marginal cost is low (approximately $0.063$ ms/path).

Full latency benchmarks are in
[benchmarks/runtime/inference_latency_a100.md](../../benchmarks/runtime/inference_latency_a100.md).

## See also

- [Microsimulation integration](microsimulation-integration.md)
- [Results: computational cost](../results/computational-cost.md)
- [Benchmarks: inference latency](../../benchmarks/runtime/inference_latency_a100.md)
