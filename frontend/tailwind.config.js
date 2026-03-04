/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    light: '#beef00', // Bright Green
                    dark: '#657a00',  // Deep Green
                    accent: '#ff0028', // Electric Red
                    blue: '#1400c6',  // Power Blue
                },
                background: '#f8fafc',
                foreground: '#0f172a',
            }
        },
    },
    plugins: [],
}
