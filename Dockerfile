# Production FastAPI Dockerfile for monorepo setup
# Build context should be set to workspace root (../..) to access packages/database

# ================================
# Base Python Image
# ================================
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.3 \
    PRISMA_HOME_DIR=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# ================================
# Dependencies Stage
# ================================
FROM base AS dependencies

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Copy Poetry files for API
COPY apps/api/pyproject.toml apps/api/poetry.lock ./apps/api/

# Copy database package for local dependency
COPY packages/database/ ./packages/database/

# Install dependencies
WORKDIR /app/apps/api

# Configure Poetry to create venv in project
RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.path .venv

# Install dependencies
RUN poetry install --only=main --no-root && \
    rm -rf $POETRY_CACHE_DIR && \
    ls -la .venv/

# after installing your dependencies
RUN poetry install --no-root

# fetch the Linux Prisma engine binary
RUN poetry run prisma py fetch

# ================================
# Production Stage
# ================================
FROM base AS production

# Create non-root user
RUN groupadd -r fastapi && useradd -r -g fastapi fastapi

# Set working directory
WORKDIR /app

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/apps/api/.venv /app/apps/api/.venv
# Copy Prisma query engine binaries
COPY --from=dependencies /app/.cache /app/.cache

# Copy application code
COPY apps/api/src/ ./src/
COPY packages/database/src/ ./packages/database/src/

# Copy configuration files
COPY apps/api/logging.conf ./logging.conf

# Create data directory for volumes
RUN mkdir -p /app/data /app/static && \
    chown -R fastapi:fastapi /app

# Set Python path to include both src directories
ENV PYTHONPATH="/app/src:/app/packages/database/src"
ENV PATH="/app/apps/api/.venv/bin:$PATH"
ENV PRISMA_HOME_DIR=/app


# Switch to non-root user
USER fastapi

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Default command (can be overridden by fly.toml processes)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "uvloop"]
