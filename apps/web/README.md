# HireWise AI - Web Frontend

A modern Next.js frontend application for HireWise AI, built with Radix UI, TypeScript, and Tailwind CSS. Features a comprehensive layout system with dashboard and authentication interfaces.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm
- Git

### Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd hirewise-ai

# Install dependencies
pnpm install

# Start development server (from root directory)
pnpm dev
```

The web application will be available at:
- **Local**: http://localhost:3000 (or next available port)
- **Network**: http://192.168.1.6:3000

## 📁 Project Structure

```
apps/web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Master Layout (root)
│   │   ├── page.tsx           # Home page
│   │   ├── dashboard/         # Dashboard pages
│   │   │   ├── layout.tsx     # Dashboard Layout
│   │   │   └── page.tsx       # Dashboard home
│   │   └── (auth)/            # Authentication pages
│   │       ├── layout.tsx     # Auth Layout
│   │       ├── login/         # Login page
│   │       ├── sign-up/       # Sign up page
│   │       └── reset-password/ # Password reset
│   ├── components/            # Reusable components
│   │   └── ui/               # UI components
│   │       ├── logo.tsx      # Logo component
│   │       ├── footer.tsx    # Footer component
│   │       ├── header.tsx    # Dashboard header
│   │       ├── sidebar.tsx   # Dashboard sidebar
│   │       └── index.ts      # Component exports
│   ├── config/               # Configuration files
│   │   └── navigation.json   # Navigation structure
│   ├── lib/                  # Utility libraries
│   │   ├── auth.ts          # Authentication utilities
│   │   ├── api.ts           # API utilities
│   │   └── utils.ts         # General utilities
│   ├── styles/              # Global styles
│   │   ├── globals.css      # Global CSS + Radix UI
│   │   └── typography.css   # Typography styles
│   └── providers/           # React providers
├── public/                  # Static assets
│   ├── logo.svg            # Main logo
│   ├── fonts/              # Aeonik font files
│   └── [favicons]          # Favicon files
├── package.json            # Dependencies and scripts
├── next.config.ts          # Next.js configuration
├── tailwind.config.js      # Tailwind CSS config
├── tsconfig.json          # TypeScript config
└── README.md              # This file
```

## 🎨 Layout System

The application uses a three-tier layout system:

### 1. Master Layout (`src/app/layout.tsx`)
- **Purpose**: Root layout for entire application
- **Features**: Font loading, Radix UI theme, global footer, meta tags
- **Applies to**: All pages

### 2. Dashboard Layout (`src/app/dashboard/layout.tsx`)
- **Purpose**: Layout for authenticated dashboard pages
- **Features**: Header with logo, expandable sidebar navigation, responsive design
- **Applies to**: All `/dashboard/*` routes

### 3. Auth Layout (`src/app/(auth)/layout.tsx`)
- **Purpose**: Layout for authentication pages
- **Features**: Centered design, logo display, gradient background
- **Applies to**: All authentication routes (`/login`, `/sign-up`, etc.)

## 🧭 Navigation Configuration

The dashboard sidebar navigation is configured via JSON for easy maintenance:

### Configuration File: `src/config/navigation.json`

```json
{
  "navigation": [
    {
      "id": "dashboard",
      "label": "Dashboard",
      "href": "/dashboard",
      "icon": "dashboard",
      "children": []
    },
    {
      "id": "agents",
      "label": "AI Agents",
      "icon": "robot",
      "children": [
        {
          "id": "agents-list",
          "label": "All Agents",
          "href": "/dashboard/agents",
          "icon": "list"
        },
        {
          "id": "agents-create",
          "label": "Create Agent",
          "href": "/dashboard/agents/create",
          "icon": "plus"
        }
      ]
    }
  ]
}
```

### Navigation Item Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | ✅ | Unique identifier for the navigation item |
| `label` | string | ✅ | Display text for the navigation item |
| `href` | string | ❌ | URL path (required for leaf items) |
| `icon` | string | ✅ | Icon identifier (for future icon implementation) |
| `children` | array | ❌ | Nested navigation items (for expandable sections) |

### Adding New Navigation Items

1. **Simple Link**: Add to the navigation array
```json
{
  "id": "analytics",
  "label": "Analytics",
  "href": "/dashboard/analytics",
  "icon": "chart",
  "children": []
}
```

2. **Expandable Section**: Add with children
```json
{
  "id": "settings",
  "label": "Settings",
  "icon": "settings",
  "children": [
    {
      "id": "settings-profile",
      "label": "Profile",
      "href": "/dashboard/settings/profile",
      "icon": "user"
    }
  ]
}
```

### Navigation Features

- **Tree Structure**: Supports unlimited nesting levels
- **Expandable/Collapsible**: Parent items can be expanded/collapsed
- **Active State**: Automatically highlights current page and section
- **Responsive**: Adapts to mobile and desktop screens

## 🎨 Styling & Theming

### Design System

- **UI Framework**: Radix UI components
- **Styling**: Tailwind CSS utility classes
- **Typography**: Aeonik Sans (headings) + Aeonik Fono (body)
- **Theme**: Yellow accent color, light appearance
- **Responsive**: Mobile-first design approach

### Font Configuration

The application uses custom Aeonik fonts:

- **Aeonik Sans**: Headings (semibold 600, bold 700)
- **Aeonik Fono**: Body text (regular 400, medium 500, semibold 600)

Fonts are loaded via `next/font/local` and configured in `src/styles/globals.css`.

### Customizing Styles

1. **Component Styles**: Modify Tailwind classes in component files
2. **Global Theme**: Update Radix UI theme in `src/app/layout.tsx`
3. **Typography**: Customize font variables in `src/styles/globals.css`
4. **Colors**: Modify Tailwind config or Radix UI theme settings

## 🛠 Development

### Available Scripts

```bash
# Development server with Turbopack
pnpm dev

# Type checking
pnpm type-check

# Build for production
pnpm build

# Start production server
pnpm start

# Linting
pnpm lint
```

### Development Workflow

1. **Start Development**: Run `pnpm dev` from the root directory
2. **Make Changes**: Edit files in `src/` directory
3. **Hot Reload**: Changes automatically reflect in browser
4. **Type Check**: Run `pnpm type-check` before committing
5. **Build Test**: Run `pnpm build` to ensure production build works

### Adding New Pages

#### Dashboard Page
```tsx
// src/app/dashboard/new-page/page.tsx
export default function NewPage() {
  return (
    <div>
      <h1>New Dashboard Page</h1>
      {/* Content automatically gets dashboard layout */}
    </div>
  );
}
```

#### Auth Page
```tsx
// src/app/(auth)/new-auth/page.tsx
import { Card } from '@radix-ui/themes';

export default function NewAuthPage() {
  return (
    <Card>
      <h1>New Auth Page</h1>
      {/* Content automatically gets auth layout */}
    </Card>
  );
}
```

### Component Development

#### Creating UI Components
```tsx
// src/components/ui/new-component.tsx
import { Button } from '@radix-ui/themes';

interface NewComponentProps {
  title: string;
  onClick?: () => void;
}

export function NewComponent({ title, onClick }: NewComponentProps) {
  return (
    <Button onClick={onClick}>
      {title}
    </Button>
  );
}

export default NewComponent;
```

#### Exporting Components
```tsx
// src/components/ui/index.ts
export { NewComponent } from './new-component';
```

## 🔧 Configuration

### Environment Variables

Create `.env.local` in the web app directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENV=development
```

### Next.js Configuration

Key configurations in `next.config.ts`:
- Turbopack for faster development
- Image optimization settings
- API proxy configuration (if needed)

### TypeScript Configuration

The project uses strict TypeScript settings:
- Strict mode enabled
- Path aliases configured (`@/` points to `src/`)
- Next.js types included

## 📦 Dependencies

### Core Dependencies
- **Next.js 15.3.2**: React framework with App Router
- **React 19**: UI library
- **Radix UI**: Component library and theming
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type safety

### Development Dependencies
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Turbopack**: Fast bundler for development

## 🚀 Deployment

### Build Process
```bash
# Create production build
pnpm build

# Start production server
pnpm start
```

### Deployment Platforms
- **Vercel**: Recommended (zero-config deployment)
- **Netlify**: Static site deployment
- **Docker**: Container deployment

### Environment Setup
1. Set production environment variables
2. Configure domain and SSL
3. Set up CI/CD pipeline
4. Monitor performance and errors

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Radix UI Documentation](https://www.radix-ui.com/themes/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Layout System Documentation](./LAYOUTS.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run type checking and linting
5. Test the build process
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
