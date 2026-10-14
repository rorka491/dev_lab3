FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV"

COPY docker.requirements .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r docker.requirements


FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY . .

EXPOSE 8000
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]