"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { auth } from "@/lib/api/auth";
import { PageTransition } from "@/components/ui/PageTransition";
import ParticleBackground from "@/components/ParticleBackground"; // Import ParticleBackground

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to dashboard if already logged in
    if (auth.isAuthenticated()) {
      router.push("/dashboard");
    }
  }, [router]);

  return (
    <PageTransition>
      <div className="relative min-h-screen"> {/* Add relative positioning to contain particles */}
        <ParticleBackground /> {/* Render ParticleBackground */}
        <main className="relative z-10 flex min-h-screen flex-col items-center justify-center p-24">
          <div className="text-center space-y-6 glass-card p-8 rounded-lg">
            <h1 className="text-5xl font-bold mb-4">Todo App</h1>
            <p className="text-lg text-gray-600 mb-8">
              Full-stack todo application with secure authentication
            </p>

            <div className="flex gap-4 justify-center">
              <Link
                href="/signup"
                className="px-6 py-3 text-sm btn-primary"
              >
                Get Started
              </Link>
              <Link
                href="/login"
                className="px-6 py-3 text-sm glass-button"
              >
                Sign In
              </Link>
            </div>

            <div className="mt-8 text-sm text-gray-500">
              <p>✅ Authentication: Email + Password</p>
              <p>✅ Security: JWT Tokens + Bcrypt</p>
              <p>✅ Database: Neon PostgreSQL</p>
              <p>✅ Task Management: Full CRUD Operations</p>
            </div>
          </div>
        </main>
      </div>
    </PageTransition>
  );
}