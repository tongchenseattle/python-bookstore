import type { Metadata } from "next";
import React from "react";

export const metadata: Metadata = {
  title: "Pseudo Bookstore",
  description: "Layered bookstore application",
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
