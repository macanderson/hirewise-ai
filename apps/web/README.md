# Web Frontend

The web application is built with Next.js 15, Radix UI and Tailwind CSS.

## Getting started

### Prerequisites
- Node.js 18+
- pnpm

### Development
```bash
# from the repository root
pnpm dev
```
The site runs at `http://localhost:3000` by default.

## Project layout

```
apps/web/
├── src/              # application source
│   ├── app/          # Next.js app router
│   ├── components/   # shared components
│   ├── styles/       # global styles and fonts
│   └── config/       # navigation configuration
├── public/           # static assets
└── package.json
```

See [../../docs/LAYOUTS.md](../../docs/LAYOUTS.md) for details about the layout system.
