FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY /docs/requirements.txt .
RUN pip install --upgrade pip==25.0.1 && \
    pip install --no-cache-dir \
    --use-deprecated=legacy-resolver \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]