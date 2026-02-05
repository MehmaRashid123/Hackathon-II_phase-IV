'use client'; // This directive makes the component a Client Component

import type { Metadata } from 'next'
import './globals.css'
import { useState } from 'react';
import { Sidebar } from '@/components/Sidebar'; // Import the Sidebar component
import { ThemeProvider } from '@/providers/ThemeProvider'; // Import ThemeProvider
import { CommandSearch } from '@/components/CommandSearch'; // Import CommandSearch
import { TopBar } from '@/components/TopBar'; // Import TopBar
import { AnimatedLayout } from '@/components/layout/AnimatedLayout' // Keep if still used inside main content area
import { AnimatePresence } from 'framer-motion'; // Import AnimatePresence
// Import any other layout components here

// Metadata will be exported from a Server Component or a layout route segment
// that does not use 'use client'.
// For now, we'll keep it here, but ideally, this would be in a parent Server Component layout.
export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A secure full-stack todo application with user authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
            <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />

            {/* Main content area */}
            <main className="flex-1 flex flex-col overflow-hidden">
              <TopBar /> {/* Integrated TopBar here */}

              {/* Main content with AnimatedLayout if needed */}
              <AnimatePresence mode="wait">
                <div className="flex-1 overflow-auto p-4">
                  <AnimatedLayout>{children}</AnimatedLayout>
                </div>
              </AnimatePresence>
            </main>
          </div>
          <CommandSearch /> {/* Integrated CommandSearch here */}
        </ThemeProvider>
      </body>
    </html>
  )
}
