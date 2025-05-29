# hirewise.ai - AI Assistant for Resruiters

Build powerful AI workflows using a visual, no-code interface. hirewise.ai helps you create and manage multi-agent applications with ease.

## Features

- 🤖 **Multi-Agent Workflows**: Create complex AI agent interactions through a visual interface
- 🎨 **Modern UI**: Built with Next.js 15 and Radix UI components
- 🔧 **Robust Backend**: Python 3.13 FastAPI server for high-performance AI operations
- 📦 **Monorepo Architecture**:
  - Turborepo for efficient development
  - Shared UI components
  - Centralized configuration
- 🚀 **Production Ready**:
  - Vercel deployment support
  - PNPM package management
  - Custom cursor interactions
  - Responsive design

## Tech Stack

- **Frontend**: Next.js 15, Radix UI, TailwindCSS
- **Backend**: Python 3.13, FastAPI
- **Build Tools**: Turborepo, PNPM
- **Deployment**: Vercel

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

3. **Development**

   ```bash
   # Start the development server
   pnpm dev
   ```

4. **Build and Deploy**

   There are two deployment options available:

   ### Full Stack Deployment (Default)

   The default deployment includes both the Next.js frontend and Python FastAPI backend as serverless functions.

   ```bash
   # Build all packages and applications
   pnpm build

   # Deploy to Vercel
   vercel
   ```

   The Python backend will be automatically deployed as serverless functions using Vercel's Python runtime. Make sure your `vercel.json` is properly configured with the Python build settings.

   ### Web-Only Deployment

   For deploying just the Next.js frontend:

   ```bash
   # Build the web application
   cd apps/web && pnpm build

   # Deploy using web-only configuration
   vercel --config vercel-web-only.json
   ```

   This will deploy only the Next.js application without the Python backend.

## Documentation

Detailed documentation is available in the `/docs` directory:

- [Architecture Overview](/docs/architecture.md)
- [API Reference](/docs/api.md)
- [Component Library](/docs/components.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
