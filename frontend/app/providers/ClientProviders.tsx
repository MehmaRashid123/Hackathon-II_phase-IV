/**
 * Client Providers Wrapper
 *
 * Wraps all client-side providers for use in Server Components.
 */

"use client";

import { ReactNode } from "react";
import { WorkspaceProvider } from "@/lib/hooks/use-workspace";

interface ClientProvidersProps {
  children: ReactNode;
}

export function ClientProviders({ children }: ClientProvidersProps) {
  return <WorkspaceProvider>{children}</WorkspaceProvider>;
}
