# ── builder ────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (cache layer)
COPY pyproject.toml uv.lock ./
COPY api/pyproject.toml ./api/

# Step 1: install deps only, not the project itself (preserves layer cache)
RUN uv sync --package dip-api --no-dev --no-install-project

# Copy application source
COPY api/src ./api/src

# Step 2: now install the project
RUN uv sync --package dip-api --no-dev

# ── runtime ────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/api/src ./api/src

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/api/src"

EXPOSE 8000

CMD ["uvicorn", "dip_api.main:app", "--host", "0.0.0.0", "--port", "8000"]