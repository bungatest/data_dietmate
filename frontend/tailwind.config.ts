import type { Config } from "tailwindcss";

const config: Config = {
    content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
    theme: {
        extend: {
            colors: {
                dietmate: {
                    dark: "#28543C",
                    deep: "#173D2B",
                    light: "#EAF3EC",
                    accent: "#478461",
                    card: "#244735",
                    canvas: "#EDF2EE"
                }
            },
            boxShadow: {
                soft: "0 8px 24px rgba(23, 61, 43, 0.08)"
            }
        }
    },
    plugins: []
};

export default config;
