'use client';

import React from 'react';
import { ThemeToggle } from './ThemeToggle'; // Assuming ThemeToggle is in the same directory

export function TopBar() {
  return (
    <div className="flex items-center justify-between p-4 bg-white dark:bg-gray-800 shadow-sm">
      <div className="flex items-center space-x-4">
        <div className="text-xl font-bold text-gray-900 dark:text-white">TopBar</div>
        {/* Placeholder for Global Search */}
        <input
          type="text"
          placeholder="Global Search (Ctrl+K)"
          className="input-primary px-3 py-1 text-sm w-48"
        />
      </div>
      <ThemeToggle />
    </div>
  );
}