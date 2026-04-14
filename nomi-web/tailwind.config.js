/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        nomi: {
          bg: '#f2ede4',
          text: '#1a1f2e',
          secondary: '#9aa0b0',
          accent: '#6aaad9',
          border: '#ddd8ce',
        },
      },
      fontFamily: {
        outfit: ['var(--font-outfit)', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
