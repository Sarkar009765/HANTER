/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        extend: {
            colors: {
                "bg-primary": "#0a0a0f",
                "bg-secondary": "#12121a",
                "bg-tertiary": "#1a1a25",
                "bg-glass": "rgba(255, 255, 255, 0.03)",
                "text-primary": "#ffffff",
                "text-secondary": "#a0a0b0",
                "text-muted": "#5a5a6a",
                "accent-cyan": "#00f0ff",
                "accent-pink": "#ff006e",
                "accent-green": "#00ff88",
                "accent-yellow": "#f0a000",
                "accent-red": "#ff3333",
            },
            fontFamily: {
                body: ["Inter", "system-ui", "sans-serif"],
                mono: ["JetBrains Mono", "Fira Code", "monospace"],
            },
            boxShadow: {
                "glow-cyan": "0 0 20px rgba(0, 240, 255, 0.2)",
                "glow-pink": "0 0 20px rgba(255, 0, 110, 0.2)",
            },
            borderRadius: {
                pill: "9999px",
            },
            animation: {
                "pulse-glow": "pulseGlow 2s ease-in-out infinite",
                "float": "float 6s ease-in-out infinite",
            },
            keyframes: {
                pulseGlow: {
                    "0%, 100%": { opacity: "0.5" },
                    "50%": { opacity: "1" },
                },
                float: {
                    "0%, 100%": { transform: "translateY(0px)" },
                    "50%": { transform: "translateY(-20px)" },
                },
            },
        },
    },
    plugins: [],
};
