# Docker environment

The SAGA Docker image `olaflaitinen/saga:v1.0.0` provides a fully self-contained environment
for running SAGA pipeline-level replication without installing Conda or any Python dependencies
on the host system.

## Image details

| Attribute | Value |
|---|---|
| Base image | `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04` |
| Python version | 3.11 (Mambaforge) |
| PyTorch version | 2.4 with CUDA 12.1 |
| Image tag | `olaflaitinen/saga:v1.0.0` |
| Image tag (latest) | `olaflaitinen/saga:latest` |

## Dependency rationale

Key dependency choices:

- **PyTorch 2.4:** Required for `torch.compile` support with bfloat16 activation accumulation.
  PyTorch 2.3 and earlier have a regression in bfloat16 gradient accumulation that causes
  a CRPS degradation of approximately $0.004$ at $h=10$.
- **numpy < 2.0:** LightGBM 4.3 links against the C API of numpy 1.x. numpy 2.0 introduced
  breaking changes to the C API that cause a LightGBM import error.
- **CUDA 12.1:** Matches the CUDA version used in the MONA compute environment. Using CUDA 12.0
  or 11.x will produce identical numerical results but may have slightly different throughput.

## Quickstart with Docker

```bash
# Pull the image
docker pull olaflaitinen/saga:v1.0.0

# Run the quickstart notebook inside Docker with GPU support
docker run --rm --gpus all \
    -v "$(pwd)/data/synthetic:/workspace/data/synthetic" \
    -v "$(pwd)/notebooks:/workspace/notebooks" \
    -v "$(pwd)/outputs:/workspace/outputs" \
    olaflaitinen/saga:v1.0.0 \
    jupyter nbconvert --to notebook --execute \
        --ExecutePreprocessor.timeout=7200 \
        notebooks/00-quickstart.ipynb \
        --output notebooks/00-quickstart.executed.ipynb
```

## Building the image locally

```bash
make docker-build
```

This executes `docker build -t olaflaitinen/saga:v1.0.0 -t olaflaitinen/saga:latest .`

## Docker Compose

For extended sessions with volume mounts for data and outputs:

```bash
docker compose up -d
docker compose exec saga bash
```

The `docker-compose.yaml` file mounts `data/synthetic/`, `configs/`, `scripts/`, and `outputs/`
into the container. See [docker-compose.yaml](../../docker-compose.yaml).

## See also

- [Dockerfile](../../Dockerfile)
- [docker-compose.yaml](../../docker-compose.yaml)
- [Quickstart](quickstart.md)
- [Hardware notes](hardware-notes.md)
