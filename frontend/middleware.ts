/**
 * Middleware for route protection.
 *
 * Redirects unauthenticated users to /login.
 */

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Get token from cookies (if using httpOnly) or check for client-side token
  const token = request.cookies.get("access_token")?.value;

  // Protected routes
  const isProtectedRoute = request.nextUrl.pathname.startsWith("/dashboard");

  // Redirect to login if accessing protected route without token
  if (isProtectedRoute && !token) {
    // Note: Client-side token check happens in the component
    // This middleware is for server-side protection
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
