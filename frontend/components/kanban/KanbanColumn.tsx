/**
 * KanbanColumn Component
 *
 * Premium column container with glassmorphism and smooth drop zones.
 * Fully responsive with horizontal scroll on mobile.
 */

"use client";

import React from "react";
import { useDroppable } from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { KanbanTask, TaskStatus } from "@/lib/types/kanban";
import { KanbanCard } from "./KanbanCard";

interface KanbanColumnProps {
  id: TaskStatus;
  title: string;
  tasks: KanbanTask[];
  color: string;
}

export function KanbanColumn({ id, title, tasks, color }: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id: id,
  });

  // Count total tasks
  const taskCount = tasks.length;

  // Column color schemes
  const colorSchemes = {
    "bg-gray-500": {
      header: "bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900",
      border: "border-gray-300 dark:border-gray-600",
      text: "text-gray-700 dark:text-gray-300",
      badge: "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
    },
    "bg-blue-500": {
      header: "bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/40 dark:to-blue-800/40",
      border: "border-blue-300 dark:border-blue-600",
      text: "text-blue-700 dark:text-blue-300",
      badge: "bg-blue-200 dark:bg-blue-700 text-blue-800 dark:text-blue-200"
    },
    "bg-purple-500": {
      header: "bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/40 dark:to-purple-800/40",
      border: "border-purple-300 dark:border-purple-600",
      text: "text-purple-700 dark:text-purple-300",
      badge: "bg-purple-200 dark:bg-purple-700 text-purple-800 dark:text-purple-200"
    },
    "bg-green-500": {
      header: "bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/40 dark:to-green-800/40",
      border: "border-green-300 dark:border-green-600",
      text: "text-green-700 dark:text-green-300",
      badge: "bg-green-200 dark:bg-green-700 text-green-800 dark:text-green-200"
    }
  };

  const scheme = colorSchemes[color as keyof typeof colorSchemes] || colorSchemes["bg-gray-500"];

  return (
    <div className="flex flex-col h-full w-80 lg:w-full flex-shrink-0">
      {/* Column Header */}
      <div className={`flex-shrink-0 mb-3 p-3 rounded-xl ${scheme.header} border-2 ${scheme.border} shadow-lg`}>
        <div className="flex items-center justify-between">
          {/* Title with color indicator */}
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${color} shadow-md`} />
            <h2 className={`font-bold text-base ${scheme.text}`}>
              {title}
            </h2>
          </div>

          {/* Task count badge */}
          <div className={`px-2.5 py-1 rounded-full text-xs font-bold ${scheme.badge} shadow-sm min-w-[1.5rem] text-center`}>
            {taskCount}
          </div>
        </div>
      </div>

      {/* Droppable Task List - SCROLLABLE */}
      <div
        ref={setNodeRef}
        className={`
          flex-1 overflow-y-auto overflow-x-hidden
          p-3 rounded-xl
          bg-white/50 dark:bg-gray-800/50
          backdrop-blur-md backdrop-saturate-150
          border-2 border-dashed
          ${
            isOver
              ? "border-blue-500 bg-blue-50/50 dark:bg-blue-900/20 scale-[1.02]"
              : `${scheme.border} hover:border-opacity-70`
          }
          transition-all duration-300 ease-out
          min-h-[500px]
          shadow-inner
        `}
        style={{ maxHeight: 'calc(100vh - 250px)' }}
      >
        <SortableContext
          items={tasks.map((t) => t.id)}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-2">
            {tasks.length === 0 ? (
              // Empty state
              <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
                <svg
                  className="w-12 h-12 text-gray-300 dark:text-gray-600 mb-3"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  No tasks here
                </p>
                <p className="text-xs text-gray-400 dark:text-gray-500">
                  Drag tasks to this column
                </p>
              </div>
            ) : (
              // Task cards
              tasks.map((task) => <KanbanCard key={task.id} task={task} />)
            )}
          </div>
        </SortableContext>
      </div>
    </div>
  );
}
