# HireWise AI

HireWise, agentic AI for recruiters.

## Repository layout

- **apps/web** – Next.js 15 frontend
- **apps/api** – FastAPI backend
- **packages/database** – Prisma client and utilities
- **tools** – development helpers

## Quick start

### Prerequisites
- Node.js 18+
- Python 3.11+
- pnpm

### Installation
```bash
# clone the repository
git clone https://github.com/yourusername/hirewise-ai.git
cd hirewise-ai

# install dependencies
direnv allow || true
pnpm install
```

### Environment variables
Create `.env.local` files in `apps/web` and `apps/api` and provide the values required by each application. At minimum you will need:

```bash
DATABASE_URL=<database-url>
NEXT_PUBLIC_API_URL=http://localhost:8000
JWT_SECRET=<your-secret>
```

### Development
```bash
# run both applications
pnpm dev
```

### Production build
Each application can be built individually. For example:
```bash
# build the frontend
pnpm --filter ./apps/web build
```

## Documentation
Additional guides live in the [docs](./docs) directory:
- [Layout system](./docs/LAYOUTS.md)
- [Authentication](./docs/AUTHENTICATION.md)
- [Font configuration](./docs/FONTS.md)

## Contributing
Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full text.
