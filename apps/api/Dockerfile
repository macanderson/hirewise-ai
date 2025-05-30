# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install poetry and dependencies
RUN pip install --no-cache-dir poetry==1.5.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry to create virtualenv inside project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Add poetry to PATH and run app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
