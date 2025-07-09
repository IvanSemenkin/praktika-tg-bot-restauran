FROM nvcr.io/nvidia/cuda:12.2.2-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3.11-distutils \
    gcc \
    libprotobuf-dev \
    zlib1g-dev \
    libsm6 \
    libgl1 \
    libglib2.0-0 \
    redis-server \
    && rm -rf /var/lib/apt/lists/*


RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    ln -sf /usr/bin/pip3 /usr/bin/pip


ENV LOG_LEVEL=DEBUG
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6380

RUN python -m pip install --upgrade pip && \
    pip install --upgrade setuptools

COPY pyproject.toml .


RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -v --default-timeout=100 --retries 5 .

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "redis-server --daemonize yes && python main.py"]