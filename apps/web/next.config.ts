import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://hirewise-ai.fly.dev/:path*',
      },
    ];
  },
};

export default nextConfig;
