/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'sierra': {
          50: '#e6fff8',
          100: '#ccfff1',
          200: '#99ffe3',
          300: '#66ffd5',
          400: '#33ffc7',
          500: '#00D084',
          600: '#00b872',
          700: '#009960',
          800: '#007a4e',
          900: '#005c3c',
        }
      },
      fontFamily: {
        sans: ['GT America', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
