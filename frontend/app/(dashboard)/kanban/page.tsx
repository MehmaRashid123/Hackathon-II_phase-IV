/**
 * Kanban Board Page
 *
 * Premium Kanban board view with glassmorphism design and smooth drag-and-drop.
 */

"use client";

import React from "react";
import { KanbanBoard } from "@/components/kanban/KanbanBoard";
import { Plus } from "lucide-react";
import Link from "next/link";

export default function KanbanPage() {
  return (
    <div className="h-full w-full flex flex-col overflow-hidden">
      {/* Page header */}
      <div className="flex-shrink-0 px-6 py-4 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
              Kanban Board
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Drag and drop tasks to update their status
            </p>
          </div>

          {/* Create Task Button */}
          <Link
            href="/tasks"
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2"
          >
            <Plus size={20} />
            <span>Create Task</span>
          </Link>
        </div>
      </div>

      {/* Kanban board - Full height with proper overflow */}
      <div className="flex-1 overflow-hidden px-6 py-6">
        <KanbanBoard />
      </div>
    </div>
  );
}
