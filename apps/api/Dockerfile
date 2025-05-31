# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir poetry

# Copy project metadata
COPY apps/api/pyproject.toml apps/api/poetry.lock* ./

# Include the local database package so Poetry can install it
COPY packages/database ./packages/database

# Install dependencies without dev packages and without creating a venv
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the API source after dependencies are installed
COPY apps/api ./

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
