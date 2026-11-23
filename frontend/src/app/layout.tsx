import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DietMate AI — Personalized Diet Planner",
  description:
    "Rencana menu personal berdasarkan profil, kebutuhan nutrisi, preferensi, dan basis resep DietMate."
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#28543C"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body>
        <div className="app-frame">{children}</div>
      </body>
    </html>
  );
}
