/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'ba-blue': '#002244',
                'ba-red': '#D71920',
                'ba-grey': '#F5F6F7',
            }
        },
    },
    plugins: [],
}
