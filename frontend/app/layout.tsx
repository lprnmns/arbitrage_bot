import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Arbitrage Dashboard",
  description: "Phase 0+1 placeholder UI"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
