/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#1a2332',
          blue: '#2563eb',
          cyan: '#06b6d4',
          success: '#10b981',
          slate: '#475569',
          light: '#f8fafc',
        }
      }
    },
  },
  plugins: [],
}
