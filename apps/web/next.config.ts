import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/:path*`,
      },
    ];
  },
  eslint: {
    // Disable the built-in ESLint processing since we're using a flat config file
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
