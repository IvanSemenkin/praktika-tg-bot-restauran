FROM nvcr.io/nvidia/cuda:12.2.2-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    gcc \
    libprotobuf-dev \
    zlib1g-dev \
    libsm6 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    ln -sf /usr/bin/pip3 /usr/bin/pip


RUN python -m pip install --upgrade pip
COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -v .
COPY . .
    
EXPOSE 8000

ENTRYPOINT python main.py