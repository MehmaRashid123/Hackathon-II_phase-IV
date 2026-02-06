/**
 * Dashboard Layout - Layout with Sidebar and TopBar for authenticated pages
 */

"use client";

import { LayoutClient } from "@/components/layout/LayoutClient";
import { WorkspaceProvider } from "@/lib/hooks/use-workspace";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <WorkspaceProvider>
      <LayoutClient>{children}</LayoutClient>
    </WorkspaceProvider>
  );
}
