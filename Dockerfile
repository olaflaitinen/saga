# Multi-stage Dockerfile for the SAGA repository.
# Base image: nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 (matches Section 14 of the
# repository construction specification).
# Image tags: olaflaitinen/saga:v1.0.0 and olaflaitinen/saga:latest.
#
# Stage 1 (builder): installs mambaforge, resolves the conda environment from
#   environment.yaml, and installs the saga-forecast package in editable mode.
# Stage 2 (runtime): copies the resolved environment and the source tree from the
#   builder stage, without build tooling, to produce a smaller final image.

# ---- Stage 1: builder ----
FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04 AS builder

LABEL org.opencontainers.image.title="SAGA builder stage"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov <olaf.laitinen@su.se>"
LABEL org.opencontainers.image.source="https://github.com/olaflaitinen/saga"
LABEL org.opencontainers.image.licenses="Apache-2.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV MAMBA_ROOT_PREFIX=/opt/conda

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Mambaforge (provides mamba and conda with Python 3.11)
RUN wget -qO /tmp/mambaforge.sh \
    "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh" \
    && bash /tmp/mambaforge.sh -b -p "${MAMBA_ROOT_PREFIX}" \
    && rm /tmp/mambaforge.sh

ENV PATH="${MAMBA_ROOT_PREFIX}/bin:${PATH}"

# Copy environment specification and source tree
WORKDIR /workspace
COPY environment.yaml ./
COPY pyproject.toml setup.cfg ./
COPY src/ ./src/

# Create the conda environment from the pinned environment.yaml
RUN mamba env create -f environment.yaml -n saga \
    && mamba clean -afy

# Install the saga-forecast package in editable mode inside the conda env
RUN /opt/conda/envs/saga/bin/pip install --no-build-isolation -e .

# ---- Stage 2: runtime ----
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04 AS runtime

LABEL org.opencontainers.image.title="SAGA"
LABEL org.opencontainers.image.description="Sequence-Adaptive Generative Architecture for probabilistic earnings forecasting"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov <olaf.laitinen@su.se>"
LABEL org.opencontainers.image.source="https://github.com/olaflaitinen/saga"
LABEL org.opencontainers.image.licenses="Apache-2.0"

ENV MAMBA_ROOT_PREFIX=/opt/conda
ENV PATH="/opt/conda/envs/saga/bin:${PATH}"
ENV PYTHONPATH="/workspace/src:${PYTHONPATH}"

# Copy resolved conda environment from builder
COPY --from=builder /opt/conda/envs/saga /opt/conda/envs/saga

# Copy source tree from builder
COPY --from=builder /workspace /workspace

WORKDIR /workspace

# Default command: open a Python REPL with the saga package available
CMD ["/opt/conda/envs/saga/bin/python", "-c", \
     "import saga; print('SAGA version', saga.__version__, 'ready.')"]
