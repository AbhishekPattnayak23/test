import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1976d2',
          light: '#42a5f5',
          dark: '#0d47a1',
        },
        secondary: {
          DEFAULT: '#dc004e',
          light: '#ff4081',
          dark: '#9a0036',
        },
        villa: {
          blue: '#2c3e50', // Dark blue for villa theme
          teal: '#1abc9c',  // Mediterranean teal
          sand: '#f5deb3',  // Beach sand color
          gold: '#f39c12',  // Luxury gold accent
        },
        success: '#4caf50',
        warning: '#ff9800',
        error: '#f44336',
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'villa': '0 4px 20px rgba(44, 62, 80, 0.1)',
        'villa-lg': '0 8px 30px rgba(44, 62, 80, 0.15)',
      },
    },
  },
  plugins: [],
}
export default config
