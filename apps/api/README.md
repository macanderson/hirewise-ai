# API Service

This directory contains the FastAPI backend for HireWise AI.

## Development

### Prerequisites
- Python 3.11+
- Poetry

### Setup
```bash
cd apps/api
poetry install
```

### Running in development
```bash
poetry run uvicorn src.api.main:app --reload
```

Tests are executed with `poetry run pytest`.

### Environment variables
The service expects a few values to be provided in `.env`:

```
DATABASE_URL=<database-url>
JWT_SECRET=<jwt-secret>
```

See the root README for more information on running the entire project.
