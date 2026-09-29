/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./scripts/**/*.py",
    "./src/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        heading: ['"Playfair Display"', "serif"],
        body: ['"Inter"', "sans-serif"],
      },
      colors: {
        brand: {
          red: "#AA1120",
          navy: "#0c2749",
        },
      },
    },
  },
  plugins: [],
};
