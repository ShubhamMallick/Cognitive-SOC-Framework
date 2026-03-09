/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#007BFF',
          600: '#0056b3',
          700: '#004085',
          800: '#1e3a8a',
          900: '#1e293b',
        },
        health: {
          blue: '#007BFF',
          dark: '#0056b3',
          light: '#e3f2fd',
          gray: '#f8f9fa'
        }
      },
      fontFamily: {
        'health': ['Segoe UI', 'system-ui', 'sans-serif']
      },
      animation: {
        'fade-in-down': 'fadeInDown 0.8s ease',
        'fade-in-up': 'fadeInUp 0.8s ease',
        'spin': 'spin 1s linear infinite',
      },
      keyframes: {
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        spin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      }
    }
  },
  plugins: [],
}
