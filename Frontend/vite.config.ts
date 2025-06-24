import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://34.100.203.46:3001', // Backend server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Remove '/api' prefix
        secure: false,
      },
      '/run-way': {
        target: 'http://34.100.203.46:3001', // Proxy requests to run-way directly
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
