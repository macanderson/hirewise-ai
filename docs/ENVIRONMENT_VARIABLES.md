# Environment Variables

This document outlines the environment variables used across the **HireWise.ai** mono-repo and suggests where they should be defined. Keeping variables in `.env` files allows Turbo and the applications to pick them up consistently.

## Recommended `.env` locations

- **Root `.env`** – variables shared across the repo. Example: database connection and third‑party keys.
- **`apps/api/.env`** – backend‑specific settings.
- **`apps/web/.env`** – frontend settings exposed to Next.js.
- Use `.env.example` files to document required variables without secrets.

The development environment uses `.envrc` with `direnv` for local overrides.

## Common variables

| Variable | Description | Used in |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | Prisma, API, Turbo tasks |
| `DIRECT_URL` | Direct database URL for Prisma migrations | Prisma, Turbo tasks |
| `NEXT_PUBLIC_API_URL` | Base URL of the FastAPI server used by the web app | Next.js, Turbo tasks |
| `NEXT_PUBLIC_BASE_URL` | Public URL of the Next.js app | Next.js |
| `NEXT_PUBLIC_ENV` | Frontend runtime environment label | Next.js |
| `FASTAPI_ENV` | Backend runtime environment | `apps/api` |
| `API_HOST` / `API_PORT` | FastAPI host and port | `apps/api` |
| `API_DEBUG` | Enable FastAPI debug mode | `apps/api` |
| `JWT_SECRET_KEY` | Secret for signing JWT tokens | `apps/api` |
| `JWT_ALGORITHM` | JWT algorithm (default `HS256`) | `apps/api` |
| `LLM_MODEL` | Default OpenAI model (e.g. `gpt-4o`) | `apps/api` |
| `OPENAI_API_KEY` | API key for OpenAI | `apps/api` |
| `SUPABASE_URL` | Supabase project URL | future Supabase integration |
| `SUPABASE_KEY` / `SUPABASE_ANON_KEY` | Supabase API keys | future Supabase integration |
| `SUPABASE_SERVICE_SECRET` | Service role secret | future Supabase integration |
| `SUPABASE_JWT_SECRET` | Supabase JWT secret | future Supabase integration |

Other variables such as `FLY_API_TOKEN` are used in CI/CD workflows.

## Updating `turbo.json`

Turbo tasks can load environment variables listed in the `env` arrays. To ensure all packages get the correct values, extend the arrays in `turbo.json`:

```json
{
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true,
      "env": [
        "NODE_ENV",
        "DATABASE_URL",
        "DIRECT_URL",
        "NEXT_PUBLIC_API_URL",
        "NEXT_PUBLIC_BASE_URL",
        "NEXT_PUBLIC_ENV",
        "JWT_SECRET_KEY",
        "OPENAI_API_KEY",
        "LLM_MODEL",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "SUPABASE_SERVICE_SECRET",
        "SUPABASE_JWT_SECRET"
      ]
    }
  }
}
```

Apply the same set (or a subset) to the `build` and `test` tasks so Turbo can access these variables during CI and local runs.

For local development with `direnv`, values from `.envrc` will automatically populate the environment. For deployments, create `.env` files or configure your hosting provider's environment variables accordingly.
