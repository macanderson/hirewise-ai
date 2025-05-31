# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.3

# Configure Poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Copy only dependency files first
COPY apps/api/pyproject.toml apps/api/poetry.lock ./

# Install dependencies without installing the project itself
RUN poetry install --no-root --no-interaction --no-ansi

# Copy application code
COPY apps/api/src ./src
COPY packages/database ./packages/database

# Create a simple README to satisfy Poetry if needed later
RUN echo "# Hello World" > README.md

# Set Python path
ENV PYTHONPATH=/app/src:/app/packages/database/src

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
