/**
 * Next.js config: rewrite /api/* to the Flask backend in development.
 * Adjust the target host/port via environment variables when running Next.
 */
const backendHost = process.env.BACKEND_HOST || 'http://localhost:5000'

/** @type {import('next').NextConfig} */
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${backendHost}/api/:path*`,
      },
    ];
  },
}
