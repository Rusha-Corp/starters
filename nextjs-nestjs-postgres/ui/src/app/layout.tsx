import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Next.js + NestJS App',
  description: 'Full-stack application with Next.js and NestJS',
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
