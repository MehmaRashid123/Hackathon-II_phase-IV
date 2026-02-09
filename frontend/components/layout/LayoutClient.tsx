/**
 * LayoutClient Component
 *
 * Client-side wrapper for interactive layout elements.
 * Handles sidebar state and animations.
 */

"use client";

import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import { Sidebar } from "@/components/Sidebar";
import { TopBar } from "@/components/TopBar";
import { AnimatedLayout } from "@/components/layout/AnimatedLayout";
import { CommandSearch } from "@/components/CommandSearch";
import { ChatBot } from "@/components/chatbot/ChatBot";

interface LayoutClientProps {
  children: React.ReactNode;
}

export function LayoutClient({ children }: LayoutClientProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
      <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />

      {/* Main content area */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        <TopBar />

        {/* Scrollable content area with glassmorphism background */}
        <AnimatePresence mode="wait">
          <div className="flex-1 overflow-auto p-6">
            <AnimatedLayout>{children}</AnimatedLayout>
          </div>
        </AnimatePresence>
      </main>

      <CommandSearch />
      <ChatBot />
    </div>
  );
}
