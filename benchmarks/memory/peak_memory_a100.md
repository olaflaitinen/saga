# Peak GPU memory benchmark: NVIDIA A100 40 GB

Hardware: NVIDIA A100 SXM4 40 GB, CUDA 12.1, cuDNN 8.9.2.

| Scenario | Per-device peak memory |
|---|---|
| Training (batch=512, bfloat16) | 34.2 GB |
| Inference (batch=512, M=500, h=20) | approximately 7.1 GB |
| Inference (batch=128, M=500, h=20) | approximately 3.8 GB |

Training at the per-device batch size of 512 requires at least 36 GB of VRAM.
On GPUs with less than 36 GB, reduce `per_device_batch_size` to 256 and increase
`gradient_accumulation_steps` to 8 to maintain effective batch size 16,384.
