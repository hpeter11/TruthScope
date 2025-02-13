/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  safelist: [
    'border-red-500',
    'border-green-500',
    'border-orange-500',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};