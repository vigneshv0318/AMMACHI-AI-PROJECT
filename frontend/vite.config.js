import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'favicon-48x48.png', 'apple-touch-icon.png', 'logo/ammachi.svg'],
      manifest: {
        id: "/",
        name: "Ammachi – AI Native Language Learning",
        short_name: "Ammachi",
        description: "AI-Powered Native Language Learning Platform for NRI Children with Handwritten Tutor, Voice Agent, and Cultural Discovery.",
        theme_color: "#f59e0b",
        background_color: "#fffdf7",
        display: "standalone",
        display_override: ["standalone", "minimal-ui"],
        orientation: "portrait",
        start_url: "/",
        scope: "/",
        lang: "en",
        categories: ["education", "kids"],
        icons: [
          { src: "/pwa-192x192.png", sizes: "192x192", type: "image/png", purpose: "any" },
          { src: "/pwa-512x512.png", sizes: "512x512", type: "image/png", purpose: "any" },
          { src: "/pwa-maskable-512x512.png", sizes: "512x512", type: "image/png", purpose: "maskable" }
        ],
        // Shown in Android's richer install sheet
        screenshots: [
          { src: "/screenshots/home.jpg", sizes: "780x1688", type: "image/jpeg", form_factor: "narrow", label: "Your learning dashboard" },
          { src: "/screenshots/culture.jpg", sizes: "780x1688", type: "image/jpeg", form_factor: "narrow", label: "Festival stories and quizzes" }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}']
      }
    })
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});
