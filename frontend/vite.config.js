import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/analyze': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/results': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/policy': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/threat': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/impact': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/privacy': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/risk': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/coordinate': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/authority': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/execution': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/audit': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/outcome': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
