# Font Configuration

This project uses custom Aeonik fonts integrated with Radix UI themes.

## Fonts Used

### Aeonik Sans (Headings)

- **File**: `public/fonts/aeonik/sans/aeonik-semibold.woff2` (600 weight)
- **File**: `public/fonts/aeonik/sans/aeonik-bold.woff2` (700 weight)
- **Usage**: All heading elements (h1-h6) and Radix UI `<Heading>` components
- **CSS Variable**: `--font-aeonik-sans`

### Aeonik Fono (Body Text)

- **File**: `public/fonts/aeonik/fono/aeonikfono-regular.woff2` (400 weight)
- **File**: `public/fonts/aeonik/fono/aeonikfono-medium.woff2` (500 weight)
- **File**: `public/fonts/aeonik/fono/aeonikfono-semibold.woff2` (600 weight)
- **Usage**: All body text, paragraphs, and Radix UI `<Text>` components
- **CSS Variable**: `--font-aeonik-fono`

## Implementation Details

### Next.js Font Loading
The fonts are loaded using `next/font/local` in `src/app/layout.tsx`:

```typescript
import localFont from 'next/font/local';

const aeonikSans = localFont({
  src: [
    {
      path: '../../public/fonts/aeonik/sans/aeonik-semibold.woff2',
      weight: '600',
      style: 'normal',
    },
    {
      path: '../../public/fonts/aeonik/sans/aeonik-bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-aeonik-sans',
  display: 'swap',
});

const aeonikFono = localFont({
  src: [
    {
      path: '../../public/fonts/aeonik/fono/aeonikfono-regular.woff2',
      weight: '400',
      style: 'normal',
    },
    // ... more weights
  ],
  variable: '--font-aeonik-fono',
  display: 'swap',
});
```

### Radix UI Theme Configuration
The fonts are configured in `src/styles/globals.css` to work with Radix UI themes:

```css
.radix-themes {
  /* Configure custom fonts for Radix UI themes */
  --default-font-family: var(--font-aeonik-fono), sans-serif;
  --heading-font-family: var(--font-aeonik-sans), sans-serif;
  --code-font-family: 'hirewise-code', monospace;
  --strong-font-family: var(--font-aeonik-fono), sans-serif;
  --em-font-family: var(--font-aeonik-fono), sans-serif;
  --quote-font-family: var(--font-aeonik-fono), sans-serif;
}
```

## Usage

### With Radix UI Components

```jsx
import { Heading, Text } from '@radix-ui/themes';

// This will use Aeonik Sans semibold
<Heading size="6" as="h1">Main Title</Heading>

// This will use Aeonik Fono regular
<Text size="3">Body text content</Text>
```

### With HTML Elements

```jsx
// These will automatically use the configured fonts
<h1>Heading with Aeonik Sans</h1>
<p>Paragraph with Aeonik Fono</p>
```

## Font Weights

### Aeonik Sans (Headings)

- **600 (Semibold)**: Default for all headings
- **700 (Bold)**: Available for emphasis

### Aeonik Fono (Body)

- **400 (Regular)**: Default for body text
- **500 (Medium)**: For emphasis and strong text
- **600 (Semibold)**: For strong emphasis

## CSS Import Order

To avoid CSS import order issues with Next.js and Radix UI, the styles are imported in this order in `globals.css`:

1. Tailwind base styles
2. Radix UI themes styles (`@import '@radix-ui/themes/styles.css'`)
3. Custom typography styles
4. Font variable configurations

This ensures that Radix UI styles don't override our custom font configurations.

## Browser Support

The fonts use the `woff2` format with `font-display: swap` for optimal loading performance and broad browser support.
