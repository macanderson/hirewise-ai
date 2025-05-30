# Building a Scalable SaaS Platform: A Comprehensive Guide to Monorepo Architecture with Turborepo

__Next.js Frontend + FastAPI Backend__ are the two main technologies powering this application. FastAPI was chosen for the backend due to Python's extensive ecosystem of AI/ML libraries and tools, while Next.js was selected for the frontend because of its robust server-side rendering capabilities and developer experience.

This guide will walk you through setting up a modern monorepo for hirewise.ai using Next.js for the frontend and FastAPI for the backend. We'll use Turborepo to manage our workspace and PNPM as our package manager for the Next.js frontend and Poetry as the package manager for the FastAPI/Python backend. Let's get started!

## Project Structure

```text
hirewise/
├── apps/
│   ├── web/                    # Next.js frontend
│   ├── api/                    # FastAPI backend
│   └── docs/                   # Documentation site
├── packages/
│   ├── ui/                     # Shared UI components
│   ├── database/               # Prisma schema & client
│   ├── auth/                   # Shared auth utilities
│   └── types/                  # Shared TypeScript types
├── tools/
│   └── eslint-config/          # Shared ESLint config
├── .github/
│   └── workflows/              # GitHub Actions
├── turbo.json
├── package.json
├── pnpm-workspace.yaml
└── README.md
```

## 1. Root Configuration

### package.json

```json
{
  "name": "my-app",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "type-check": "turbo run type-check",
    "clean": "turbo run clean",
    "db:generate": "turbo run db:generate",
    "db:push": "turbo run db:push",
    "db:migrate": "turbo run db:migrate"
  },
  "devDependencies": {
    "@turbo/gen": "^1.10.12",
    "turbo": "^1.10.12",
    "prettier": "^3.0.0"
  },
  "packageManager": "pnpm@8.6.10",
  "engines": {
    "node": ">=18"
  }
}
```

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["__/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/__", "!.next/cache/__", "dist/__"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "type-check": {},
    "test": {},
    "clean": {
      "cache": false
    },
    "db:generate": {
      "cache": false
    },
    "db:push": {
      "cache": false
    },
    "db:migrate": {
      "cache": false
    }
  }
}
```

## 2. Database Package (packages/database)

### package.json

```json
{
  "name": "@hirewise/database",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "db:generate": "prisma generate",
    "db:push": "prisma db push",
    "db:migrate": "prisma migrate dev",
    "db:studio": "prisma studio",
    "db:seed": "tsx src/seed.ts"
  },
  "dependencies": {
    "@prisma/client": "^5.6.0"
  },
  "devDependencies": {
    "prisma": "^5.6.0",
    "typescript": "^5.2.0",
    "tsx": "^4.0.0"
  }
}
```

### schema.prisma

```prisma
generator client {
  provider = "prisma-client-js"
}

generator docs {
  provider = "prisma-docs-generator"
  output   = "./../../apps/docs/schema"
}

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}

model Tenant {
  id         String   @id @default(cuid())
  name       String
  domain     String   @unique
  created_at Int      @default(dbgenerated("extract(epoch from now())::int"))
  updated_at Int      @default(dbgenerated("extract(epoch from now())::int"))
  deleted_at Int?
  created_by String?
  updated_by String?
  deleted_by String?

  // Relations
  users User[]

  @@map("tenants")
}

model User {
  id         String  @id @default(cuid())
  email      String  @unique
  name       String?
  tenant_id  String
  created_at Int     @default(dbgenerated("extract(epoch from now())::int"))
  updated_at Int     @default(dbgenerated("extract(epoch from now())::int"))
  deleted_at Int?
  created_by String?
  updated_by String?
  deleted_by String?

  // Relations
  tenant Tenant @relation(fields: [tenant_id], references: [id])

  // Indexes
  @@map("users")
}
```

### src/index.ts

```typescript
import { PrismaClient } from '@prisma/client'

export const prisma = new PrismaClient()
export * from '@prisma/client'
```

## 3. FastAPI Backend (apps/api)

### pyproject.toml

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "api"
version = "0.1.0"
description = "FastAPI backend"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
python-multipart = "^0.0.6"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
supabase = "^2.3.0"
httpx = "^0.25.0"
python-decouple = "^3.8"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
black = "^23.0.0"
isort = "^5.12.0"
mypy = "^1.7.0"
pyright = "^1.1.0"

[tool.pyright]
include = ["src"]
exclude = ["__/__pycache__"]
venvPath = "."
venv = ".venv"

[tool.isort]
profile = "black"
```

### @hirewise/api package.json

```json
{
  "name": "@hirewise/api",
  "scripts": {
    "dev": "poetry run uvicorn src.main:app --reload --port 8000",
    "build": "echo 'Python build complete'",
    "test": "poetry run pytest",
    "type-check": "poetry run pyright",
    "lint": "poetry run black src/ && poetry run isort src/"
  }
}
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /code

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* /code/

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy application
COPY src /code/src

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### fly.toml

```toml
app = "hirewise-api"
primary_region = "sjc"

[build]

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/health"

[processes]
  app = "uvicorn src.main:app --host 0.0.0.0 --port 8000"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### src/main.py

```python
"""
FastAPI application main module.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .middleware.tenant import TenantMiddleware
from .routes.v1 import api_router
from .core.config import settings

app = FastAPI(
    title="My App API",
    description="FastAPI backend for My App",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tenant middleware
app.add_middleware(TenantMiddleware)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### src/core/config.py

```python
"""
Application configuration settings.
"""
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str
    DIRECT_URL: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Mailgun
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### src/middleware/tenant.py

```python
"""
Tenant middleware for multi-tenant support.
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class TenantMiddleware(BaseHTTPMiddleware):
    """Middleware to handle tenant context."""

    async def dispatch(self, request: Request, call_next):
        """Process request and add tenant context."""

        # Skip tenant check for health and auth endpoints
        if request.url.path in ["/health", "/api/v1/auth/login", "/api/v1/auth/callback"]:
            return await call_next(request)

        # Get tenant ID from header
        tenant_id = request.headers.get("X-Tenant-Id")

        if not tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-Id header required")

        # Add tenant to request state
        request.state.tenant_id = tenant_id

        response = await call_next(request)
        return response
```

### src/routes/v1/__init__.py

```python
"""
API v1 routes module.
"""
from fastapi import APIRouter
from .auth import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
```

### src/routes/v1/auth.py

```python
"""
Authentication routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from supabase import create_client, Client

from ...core.config import settings

router = APIRouter()

def get_supabase() -> Client:
    """Get Supabase client."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

@router.post("/login")
async def login(
    email: str,
    password: str,
    supabase: Client = Depends(get_supabase)
):
    """Login endpoint."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {"access_token": response.session.access_token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/callback")
async def auth_callback(request: Request):
    """OAuth callback endpoint."""
    # Handle OAuth callback logic here
    return RedirectResponse(url="http://localhost:3000/dashboard")

@router.post("/logout")
async def logout(supabase: Client = Depends(get_supabase)):
    """Logout endpoint."""
    supabase.auth.sign_out()
    return {"message": "Logged out successfully"}

@router.post("/reset-password")
async def reset_password(
    email: str,
    supabase: Client = Depends(get_supabase)
):
    """Reset password endpoint."""
    try:
        supabase.auth.reset_password_email(email)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to send reset email")
```

## 4. Next.js Frontend (apps/web)

### @hirewise/web package.json

```json
{
  "name": "@hirewise/web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@hirewise/ui": "workspace:*",
    "@hirewise/database": "workspace:*",
    "@supabase/ssr": "^0.0.10",
    "@supabase/supabase-js": "^2.38.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.292.0",
    "tailwind-merge": "^2.0.0",
    "js-cookie": "^3.0.5"
  },
  "devDependencies": {
    "@types/node": "^20.8.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/js-cookie": "^3.0.6",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.52.0",
    "eslint-config-next": "^14.0.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.2.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^6.0.0"
  }
}
```

### vercel.json

```json
{
  "buildCommand": "cd ../.. && npx turbo run build --filter=web",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "installCommand": "cd ../.. && pnpm install",
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase_url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase_anon_key",
    "NEXT_PUBLIC_API_URL": "@api_url"
  }
}
```

### next.config.js

```javascript
/__ @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["@hirewise/ui", "@hirewise/database"],
  experimental: {
    appDir: true,
  },
}

module.exports = nextConfig
```

### src/lib/supabase.ts

```typescript
import { createBrowserClient } from '@supabase/ssr'

export const createClient = () => {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### src/middleware.ts

```typescript
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value,
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  // Get tenant from subdomain or header
  const tenantId = request.headers.get('x-tenant-id') || 'default'

  // Add tenant to response headers for API calls
  response.headers.set('x-tenant-id', tenantId)

  await supabase.auth.getUser()

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

## 5. GitHub Actions (.github/workflows)

### ci.yml

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test-and-build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        uses: snok/install-poetry@v1

      - name: Install Python dependencies
        run: cd apps/api && poetry install

      - name: Type check
        run: pnpm turbo type-check

      - name: Lint
        run: pnpm turbo lint

      - name: Test
        run: pnpm turbo test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Build
        run: pnpm turbo build
```

### deploy-api.yml

```yaml
name: Deploy API to Fly.io

on:
  push:
    branches: [main]
    paths: ['apps/api/__']

jobs:
  deploy:
    name: Deploy API
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: superfly/flyctl-actions/setup-flyctl@master

      - run: |
          cd apps/api
          flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## 6. Deployment Instructions

### Backend Deployment (Fly.io)

1. __Install Fly CLI__:

   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. __Login to Fly__:

   ```bash
   flyctl auth login
   ```

3. __Initialize Fly app__:

   ```bash
   cd apps/api
   flyctl launch --no-deploy
   ```

4. __Set environment variables__:

   ```bash
   flyctl secrets set DATABASE_URL="your-postgres-url"
   flyctl secrets set SUPABASE_URL="your-supabase-url"
   flyctl secrets set SUPABASE_ANON_KEY="your-supabase-anon-key"
   flyctl secrets set SECRET_KEY="your-secret-key"
   ```

5. __Deploy__:

   ```bash
   flyctl deploy
   ```

### Frontend Deployment (Vercel)

1. __Install Vercel CLI__:

   ```bash
   pnpm install -g vercel
   ```

2. __Login to Vercel__:

   ```bash
   vercel login
   ```

3. __Deploy from web directory__:

   ```bash
   cd apps/web
   vercel --prod
   ```

## 7. Development Workflow

### Local Development

1. __Start database__:

   ```bash
   # Set up Supabase locally or use cloud instance
   pnpm db:push
   ```

2. __Start backend__:

   ```bash
   cd apps/api
   poetry run uvicorn src.main:app --reload
   ```

3. __Start frontend__:

   ```bash
   pnpm dev
   ```

### Database Management

```bash
# Generate Prisma client
pnpm db:generate

# Push schema changes
pnpm db:push

# Create migration
pnpm db:migrate

# View database
cd packages/database && pnpm db:studio
```

This setup provides a production-ready monorepo with proper separation of concerns, type safety, multi-tenancy support, and modern deployment practices using Fly.io for the backend and Vercel for the frontend.
