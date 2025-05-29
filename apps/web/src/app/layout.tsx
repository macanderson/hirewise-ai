import '@/styles/globals.css';
import { Theme } from '@radix-ui/themes';
import { Metadata } from 'next';
import React from 'react';
import { Toaster } from 'react-hot-toast';
import localFont from 'next/font/local';

// Aeonik Sans for headings (semibold weight)
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

// Aeonik Fono for body text (regular weight)
const aeonikFono = localFont({
  src: [
    {
      path: '../../public/fonts/aeonik/fono/aeonikfono-regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../../public/fonts/aeonik/fono/aeonikfono-medium.woff2',
      weight: '500',
      style: 'normal',
    },
    {
      path: '../../public/fonts/aeonik/fono/aeonikfono-semibold.woff2',
      weight: '600',
      style: 'normal',
    },
  ],
  variable: '--font-aeonik-fono',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'),
  title: 'hirewise.ai - AI-powered agents for your business',
  description: 'AI-powered agent generation for your business',
  icons: {
    icon: [{ url: '/favicon.ico' }, { url: '/favicon.png', sizes: '32x32' }],
  },
  openGraph: {
    title: 'hirewise.ai – Build Multi-Agent Apps with Clicks, Not Code',
    description: 'Create powerful AI workflows using a visual, no-code interface.',
    images: ['/hirewise_social_preview.png'],
    url: 'https://app.hirewise.ai',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'hirewise.ai – Build Multi-Agent Apps with Clicks, Not Code',
    description: 'Create powerful AI workflows using a visual, no-code interface.',
    images: ['/hirewise_social_preview.png'],
  },
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${aeonikFono.variable} ${aeonikSans.variable}`}
    >
      <head>
        <link rel="apple-touch-icon" sizes="57x57" href="/apple-icon-57x57.png" />
        <link rel="apple-touch-icon" sizes="60x60" href="/apple-icon-60x60.png" />
        <link rel="apple-touch-icon" sizes="72x72" href="/apple-icon-72x72.png" />
        <link rel="apple-touch-icon" sizes="76x76" href="/apple-icon-76x76.png" />
        <link rel="apple-touch-icon" sizes="114x114" href="/apple-icon-114x114.png" />
        <link rel="apple-touch-icon" sizes="120x120" href="/apple-icon-120x120.png" />
        <link rel="apple-touch-icon" sizes="144x144" href="/apple-icon-144x144.png" />
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-icon-152x152.png" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-icon-180x180.png" />
        <link rel="icon" type="image/png" sizes="192x192" href="/android-icon-192x192.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="msapplication-TileColor" content="#ffffff" />
        <meta name="msapplication-TileImage" content="/ms-icon-144x144.png" />
        <meta name="theme-color" content="#ffffff"></meta>
      </head>
      <body suppressHydrationWarning className="antialiased min-h-screen flex flex-col">
        <Theme
          appearance="light"
          accentColor="yellow"
          radius="full"
          scaling="110%"
          panelBackground="translucent"
        >
          <div className="flex flex-col min-h-screen">{children}</div>
          <Toaster />
        </Theme>
      </body>
    </html>
  );
}
