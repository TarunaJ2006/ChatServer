import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // Listen on all addresses, so your app is reachable on your LAN
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    open: true,
    // Allow connections from any origin (useful for network access)
    cors: true,
    // Configure WebSocket proxy if needed for development
    hmr: {
      host: 'localhost'
    }
  }
})
