/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'media', // Enable system dark mode detection
  theme: {
    extend: {
      backdropBlur: {
        xs: '2px', // Extra small blur for subtle effects
      },
      backgroundColor: {
        'glass-light': 'rgba(255, 255, 255, 0.1)',
        'glass-dark': 'rgba(0, 0, 0, 0.2)',
      },
      borderColor: {
        'glass-light': 'rgba(255, 255, 255, 0.2)',
        'glass-dark': 'rgba(255, 255, 255, 0.1)',
      },
    },
  },
  variants: {
    extend: {
      backdropBlur: ['hover', 'focus'],
      backgroundColor: ['hover', 'dark'],
    },
  },
  plugins: [],
}
