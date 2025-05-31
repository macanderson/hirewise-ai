# Database Package

This package contains the Prisma schema and generated client used by the project.

## Commands

Run these scripts from the repository root:

```bash
# generate client
pnpm db:generate

# apply migrations
pnpm db:migrate

# open Prisma Studio
pnpm db:studio
```

The schema is located in `src/database/client/schema.prisma`.
