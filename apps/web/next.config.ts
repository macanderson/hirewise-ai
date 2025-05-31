import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://hirewise-api.fly.dev/:path*',
      },
    ];
  },
  eslint: {
    // Disable the built-in ESLint processing since we're using a flat config file
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
