import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/options': 'http://localhost:8000',
      '/start': 'http://localhost:8000',
      '/command': 'http://localhost:8000',
    },
  },
})
