# Layout System Documentation

This document describes the three-layout system implemented for the HireWise AI web application.

## Overview

The application uses a hierarchical layout system with three main layouts:

1. **Master Layout** - Root layout for the entire application
2. **Dashboard Layout** - Layout for authenticated dashboard pages
3. **Auth Layout** - Layout for authentication pages (login, signup, etc.)

## 1. Master Layout (`src/app/layout.tsx`)

The Master Layout is the root layout that wraps the entire application.

### Features

- **Font Configuration**: Loads and configures Aeonik Sans and Aeonik Fono fonts
- **Radix UI Theme**: Sets up the global Radix UI theme with yellow accent color
- **Global Styles**: Includes global CSS and typography styles
- **Footer**: Includes a global footer with copyright and links
- **Meta Tags**: Comprehensive meta tags for SEO and social sharing
- **Favicon Support**: Complete favicon setup for all devices

### Structure
```tsx
<html>
  <body>
    <Theme>
      <div className="flex flex-col min-h-screen">
        {children} // Dashboard or Auth layouts
        <Footer />
      </div>
      <ThemePanel />
      <Toaster />
    </Theme>
  </body>
</html>
```

## 2. Dashboard Layout (`src/app/dashboard/layout.tsx`)

The Dashboard Layout provides the structure for authenticated user pages.

### Dashboard Features

- **Header**: Top navigation bar with logo and user menu
- **Sidebar**: Collapsible navigation sidebar with tree structure
- **Responsive Design**: Adapts to different screen sizes
- **Navigation Configuration**: JSON-based navigation structure

### Dashboard Components

- `Header` - Top navigation with logo and user actions
- `Sidebar` - Left navigation with expandable menu items

### Dashboard Structure

```tsx
<div className="flex h-screen bg-gray-50">
  <Sidebar />
  <div className="flex-1 flex flex-col overflow-hidden">
    <Header />
    <main className="flex-1 overflow-y-auto p-6">
      {children} // Dashboard pages
    </main>
  </div>
</div>
```

### Dashboard Navigation Configuration

The sidebar navigation is configured via `src/config/navigation.json`:

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
        }
      ]
    }
  ]
}
```

### Navigation Features

- **Tree Structure**: Supports nested navigation items
- **Expandable/Collapsible**: Parent items can be expanded/collapsed
- **Active State**: Highlights current page and section
- **Icon Support**: Each item can have an icon identifier

## 3. Auth Layout (`src/app/(auth)/layout.tsx`)

The Auth Layout provides a clean, centered design for authentication pages.

### Auth Features

- **Centered Design**: Centers content vertically and horizontally
- **Logo Display**: Shows the HireWise AI logo at the top
- **Gradient Background**: Subtle yellow gradient background
- **Responsive**: Adapts to mobile and desktop screens
- **Footer**: Simple copyright footer

### Auth Structure

```tsx
<div className="min-h-screen bg-gradient-to-br from-yellow-50 to-white flex flex-col">
  <div className="flex justify-center pt-8 pb-4">
    <Logo />
  </div>
  <div className="flex-1 flex items-center justify-center">
    <div className="max-w-md w-full">
      {children} // Auth pages (login, signup, etc.)
    </div>
  </div>
  <div className="pb-8 text-center">
    <p>© 2024 HireWise AI. All rights reserved.</p>
  </div>
</div>
```

## Components

### Logo Component (`src/components/ui/logo.tsx`)

Reusable logo component that displays the HireWise AI logo from `/logo.svg`.

```tsx
<Logo width={120} height={40} className="custom-class" />
```

### Footer Component (`src/components/ui/footer.tsx`)

Global footer with copyright and navigation links.

### Header Component (`src/components/ui/header.tsx`)

Dashboard header with logo and user menu.

### Sidebar Component (`src/components/ui/sidebar.tsx`)

Dashboard sidebar with expandable navigation tree.

## Usage Examples

### Dashboard Page

```tsx
// src/app/dashboard/agents/page.tsx
export default function AgentsPage() {
  return (
    <div>
      <h1>AI Agents</h1>
      {/* This will be wrapped by Dashboard Layout */}
    </div>
  );
}
```

### Auth Page

```tsx
// src/app/(auth)/signup/page.tsx
export default function SignupPage() {
  return (
    <Card>
      <h1>Sign Up</h1>
      {/* This will be wrapped by Auth Layout */}
    </Card>
  );
}
```

## Styling

The layouts use:

- **Tailwind CSS** for utility classes
- **Radix UI** for components and theming
- **Aeonik Fonts** for typography
- **Custom CSS Variables** for consistent theming

## File Structure

```text
src/
├── app/
│   ├── layout.tsx              # Master Layout
│   ├── dashboard/
│   │   └── layout.tsx          # Dashboard Layout
│   └── (auth)/
│       └── layout.tsx          # Auth Layout
├── components/ui/
│   ├── logo.tsx               # Logo component
│   ├── footer.tsx             # Footer component
│   ├── header.tsx             # Header component
│   └── sidebar.tsx            # Sidebar component
└── config/
    └── navigation.json        # Navigation configuration
```

## Customization

### Adding Navigation Items
Edit `src/config/navigation.json` to add new navigation items:

```json
{
  "id": "new-section",
  "label": "New Section",
  "icon": "icon-name",
  "children": [
    {
      "id": "new-page",
      "label": "New Page",
      "href": "/dashboard/new-page",
      "icon": "page-icon"
    }
  ]
}
```

### Styling Customization

- Modify Tailwind classes in component files
- Update Radix UI theme in `src/app/layout.tsx`
- Customize fonts in `src/styles/globals.css`

## Best Practices

1. **Use the appropriate layout** for each page type
2. **Keep navigation configuration** in the JSON file for maintainability
3. **Follow the component structure** for consistency
4. **Use Radix UI components** for consistent theming
5. **Test responsive behavior** on different screen sizes
