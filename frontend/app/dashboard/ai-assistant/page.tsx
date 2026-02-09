/**
 * AI Assistant Page
 * Full-page chat interface for AI-powered task management
 */

"use client";

import { AIAssistantView } from "@/components/chat/AIAssistantView";
import { auth } from "@/lib/api/auth";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function AIAssistantPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // Check authentication
    const user = auth.getUser();
    if (!user?.id) {
      router.push("/login");
      return;
    }
    setUserId(user.id);
  }, [router]);

  if (!userId) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-4rem)] p-4">
      <AIAssistantView userId={userId} />
    </div>
  );
}
