/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,tsx}"],
  theme: {
    extend: {
      colors: {
        'custom-blue': '#007ace',
        'custom-pink': '#ff49db',
        'custom-green': '#13ce66',
        'custom-orange': '#ff7849',
      },
    }
  },
  plugins: [],
}

