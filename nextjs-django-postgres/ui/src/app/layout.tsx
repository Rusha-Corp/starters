import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Next.js + Django Starter",
  description: "A starter template for Next.js with Django and PostgreSQL",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
