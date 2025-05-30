# hirewise.ai - AI Assistant for Recruiters

Build powerful AI workflows using a visual, no-code interface. hirewise.ai helps you create and manage multi-agent applications with ease.

## Features

- 🤖 **Multi-Agent Workflows**: Create complex AI agent interactions through a visual interface
- 🎨 **Modern UI**: Built with Next.js 15 and Radix UI components
- 🔧 **Robust Backend**: Python 3.13 FastAPI server for high-performance AI operations
- 📦 **Monorepo Architecture**:
  - Managed with **Turborepo** and **pnpm** workspaces
  - Shared packages under `/packages` and tools under `/tools`
  - FastAPI backend in `apps/api` managed with **Poetry**
  - Next.js frontend in `apps/web`
- 🚀 **Production Ready**:
  - Vercel frontend deployment
  - Fly.io backend deployment
  - PNPM package management
  - Custom cursor interactions
  - Responsive design

## Tech Stack

- **Frontend**: Next.js 15, Radix UI, TailwindCSS
- **Backend**: Python 3.13, FastAPI
- **Build Tools**: Turborepo, PNPM
- **Deployment**: Vercel (frontend) & Fly.io (backend)

## Getting Started

1. **Prerequisites**
   - Node.js 18+
   - Python 3.13
   - PNPM

2. **Installation**

   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/hirewise.git
   cd hirewise-ai

   # Install dependencies
   pnpm install
   ```

3. **Environment Variables**

   Create `.env.local` files in `apps/web` and `apps/api` with the following variables:

   ```bash
   # Shared
   DATABASE_URL=<database-url>
   DIRECT_URL=<direct-database-url>

   # Web
   NEXT_PUBLIC_API_URL=http://localhost:8000

   # API
   JWT_SECRET_KEY=<your-secret>
   ```

4. **Development**

   ```bash
   # Start the development server
   pnpm dev
   ```

5. **Build and Deploy**

    Deploy the frontend to Vercel. The FastAPI backend is deployed separately on Fly.io.

    ```bash
    cd apps/web
    pnpm build
    vercel
    ```

## Documentation

Detailed documentation is available in the `/docs` directory:

- [Architecture Overview](/docs/architecture.md)
- [API Reference](/docs/api.md)
- [Component Library](/docs/components.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
