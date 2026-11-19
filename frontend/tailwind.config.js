/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#006D77', // Villa teal/blue from theme
          50: '#E6F3F4',
          100: '#CCE7E9',
          200: '#99CFD3',
          300: '#66B7BD',
          400: '#339FA7',
          500: '#006D77',
          600: '#005761',
          700: '#00414B',
          800: '#002B35',
          900: '#00151F',
        },
        secondary: {
          DEFAULT: '#EDB753', // Warm gold from theme
          50: '#FCF3E1',
          100: '#FAE7C3',
          200: '#F5CF87',
          300: '#F0B74B',
          400: '#EDB753',
          500: '#E8A217',
          600: '#C3870F',
          700: '#9E6C07',
          800: '#7A5100',
          900: '#563600',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Roboto Mono', 'monospace'],
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: true,
  },
};