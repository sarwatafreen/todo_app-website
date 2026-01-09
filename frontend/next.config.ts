import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  compiler: {
    styledComponents: true,
  },
  devIndicators: {
    buildActivity: false,
  },
};

export default nextConfig;