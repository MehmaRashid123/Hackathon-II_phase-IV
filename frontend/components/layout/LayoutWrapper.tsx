'use client'

import { useState } from 'react'
import { AnimatePresence } from 'framer-motion'
import { Sidebar } from '@/components/Sidebar'
import { ThemeProvider } from '@/providers/ThemeProvider'
import { CommandSearch } from '@/components/CommandSearch'
import { TopBar } from '@/components/TopBar'
import { AnimatedLayout } from '@/components/layout/AnimatedLayout'

export function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
        <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />

        {/* Main content area */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <TopBar />

          {/* Scrollable content area with glassmorphism background */}
          <AnimatePresence mode="wait">
            <div className="flex-1 overflow-auto p-6">
              <AnimatedLayout>{children}</AnimatedLayout>
            </div>
          </AnimatePresence>
        </main>
      </div>
      <CommandSearch />
    </ThemeProvider>
  )
}
