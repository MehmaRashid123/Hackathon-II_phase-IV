'use client'; // This directive makes the component a Client Component

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation'; // Import usePathname
import { LayoutDashboard, ListTodo, Columns3 } from 'lucide-react'; // Import Lucide icons

export function Sidebar({ isOpen, setIsOpen }: { isOpen: boolean; setIsOpen: (isOpen: boolean) => void }) {
  const [isMobile, setIsMobile] = useState(false);
  const pathname = usePathname(); // Get current pathname

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    handleResize(); // Set initial value
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const sidebarWidthClass = isMobile ? 'w-64' : (isOpen ? 'w-64' : 'w-20');
  const sidebarTransformClass = isMobile ? (isOpen ? 'translate-x-0' : '-translate-x-full') : 'translate-x-0';
  const sidebarPositionClass = isMobile ? 'fixed inset-y-0 left-0 z-40' : 'relative';

  // Helper function to determine if a link is active
  const isActive = (href: string) => pathname === href;

  return (
    <>
      <div
        className={`flex flex-col h-full bg-gray-800 text-white shadow-lg transition-all duration-300 ease-in-out ${sidebarWidthClass} ${sidebarTransformClass} ${sidebarPositionClass}`}
      >
        {/* Workspace Switcher Placeholder */}
        <div className="p-4 border-b border-gray-700 flex items-center justify-between">
          {(isOpen || !isMobile) && <h2 className="text-xl font-bold">Workspace</h2>}
          <button onClick={() => setIsOpen(!isOpen)} className="p-1 rounded-full hover:bg-gray-700">
            {/* Replace with a proper icon later */}
            {isOpen ? '<' : '>'}
          </button>
        </div>

        {/* Navigation Links Placeholder */}
        <nav className="flex-1 p-4 space-y-2">
          <Link href="/dashboard" className={`flex items-center space-x-2 p-2 rounded-md hover:bg-gray-700 ${isActive('/dashboard') ? 'bg-gray-700' : ''}`}>
            <LayoutDashboard className="w-5 h-5" />
            {(isOpen || !isMobile) && <span>Dashboard</span>}
          </Link>
          <Link href="/tasks" className={`flex items-center space-x-2 p-2 rounded-md hover:bg-gray-700 ${isActive('/tasks') ? 'bg-gray-700' : ''}`}>
            <ListTodo className="w-5 h-5" />
            {(isOpen || !isMobile) && <span>Tasks</span>}
          </Link>
          <Link href="/kanban" className={`flex items-center space-x-2 p-2 rounded-md hover:bg-gray-700 ${isActive('/kanban') ? 'bg-gray-700' : ''}`}>
            <Columns3 className="w-5 h-5" />
            {(isOpen || !isMobile) && <span>Kanban</span>}
          </Link>
          {/* More navigation links can go here */}
        </nav>

        {/* User Profile Placeholder */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex items-center space-x-2">
            {/* <UserAvatar /> */}
            {(isOpen || !isMobile) && (
              <div>
                <div className="font-medium">User Name</div>
                <div className="text-sm text-gray-400">user@example.com</div>
              </div>
            )}
          </div>
          <button className="mt-4 w-full text-left p-2 rounded-md hover:bg-gray-700 text-sm">
            {(isOpen || !isMobile) && 'Logout'}
          </button>
        </div>
      </div>

      {/* Backdrop for mobile overlay */}
      {isMobile && isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setIsOpen(false)}
        ></div>
      )}
    </>
  );
}
