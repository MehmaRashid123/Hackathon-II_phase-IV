/**
 * Dashboard Layout - Layout with Sidebar and TopBar for authenticated pages
 */

"use client";

import { LayoutClient } from "@/components/layout/LayoutClient";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <LayoutClient>{children}</LayoutClient>;
}
