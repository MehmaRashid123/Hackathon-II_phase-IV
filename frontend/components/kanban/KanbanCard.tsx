/**
 * KanbanCard Component
 *
 * Premium glassmorphism card for Kanban tasks with smooth drag animations.
 * Shows completion status with different colors and visual indicators.
 */

"use client";

import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { KanbanTask, TaskStatus } from "@/lib/types/kanban";
import { CheckCircle2, Circle, Clock, Eye, CheckCheck } from "lucide-react";

interface KanbanCardProps {
  task: KanbanTask;
  isDragging?: boolean;
}

export function KanbanCard({ task, isDragging }: KanbanCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition: transition || "transform 200ms cubic-bezier(0.4, 0, 0.2, 1)",
  };

  const isBeingDragged = isDragging || isSortableDragging;

  // Ensure task has a status field (backward compatibility)
  const taskStatus: TaskStatus = task.status || (task.is_completed ? "DONE" : "TO_DO");

  // Status-based colors and icons
  const statusConfig: Record<TaskStatus, {
    bgColor: string;
    textColor: string;
    icon: any;
    iconColor: string;
    badge: string;
    label: string;
  }> = {
    TO_DO: {
      bgColor: "bg-gray-50 dark:bg-gray-800/60 border-gray-300 dark:border-gray-600",
      textColor: "text-gray-700 dark:text-gray-300",
      icon: Circle,
      iconColor: "text-gray-400",
      badge: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
      label: "To Do"
    },
    IN_PROGRESS: {
      bgColor: "bg-blue-50 dark:bg-blue-900/20 border-blue-300 dark:border-blue-600",
      textColor: "text-blue-900 dark:text-blue-200",
      icon: Clock,
      iconColor: "text-blue-500",
      badge: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
      label: "In Progress"
    },
    REVIEW: {
      bgColor: "bg-purple-50 dark:bg-purple-900/20 border-purple-300 dark:border-purple-600",
      textColor: "text-purple-900 dark:text-purple-200",
      icon: Eye,
      iconColor: "text-purple-500",
      badge: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
      label: "Review"
    },
    DONE: {
      bgColor: "bg-green-50 dark:bg-green-900/20 border-green-300 dark:border-green-600",
      textColor: "text-green-900 dark:text-green-200",
      icon: CheckCheck,
      iconColor: "text-green-500",
      badge: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
      label: "Completed"
    }
  };

  // Get config with fallback to TO_DO if status is invalid
  const config = statusConfig[taskStatus] || statusConfig["TO_DO"];
  const StatusIcon = config.icon;

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`
        group relative cursor-grab active:cursor-grabbing
        transition-all duration-200 ease-out
        ${isBeingDragged ? "opacity-50 scale-105 rotate-3" : "opacity-100 scale-100"}
      `}
    >
      {/* Glassmorphism Card */}
      <div
        className={`
          relative overflow-hidden rounded-lg p-3
          ${config.bgColor}
          backdrop-blur-md backdrop-saturate-150
          border-2
          shadow-md hover:shadow-lg
          transition-all duration-200 ease-out
          hover:scale-[1.02]
          ${isBeingDragged ? "shadow-2xl ring-2 ring-blue-500/50" : ""}
        `}
      >
        {/* Completion status indicator stripe */}
        <div className={`absolute top-0 left-0 w-full h-1 ${
          task.is_completed
            ? "bg-gradient-to-r from-green-400 to-green-600"
            : "bg-gradient-to-r from-gray-300 to-gray-400 dark:from-gray-600 dark:to-gray-700"
        }`} />

        {/* Card content */}
        <div className="relative space-y-2 mt-1">
          {/* Header with status icon */}
          <div className="flex items-start gap-2">
            <div className={`mt-0.5 flex-shrink-0 ${config.iconColor}`}>
              <StatusIcon size={18} strokeWidth={2.5} />
            </div>

            {/* Title with completion indicator */}
            <h3 className={`flex-1 font-semibold text-sm ${config.textColor} ${
              task.is_completed ? "line-through opacity-75" : ""
            } line-clamp-2`}>
              {task.title}
            </h3>

            {/* Completion checkmark */}
            {task.is_completed && (
              <CheckCircle2
                className="flex-shrink-0 text-green-500"
                size={16}
                fill="currentColor"
              />
            )}
          </div>

          {/* Description */}
          {task.description && (
            <p className={`text-xs ${
              task.is_completed
                ? "text-gray-500 dark:text-gray-500 line-through opacity-60"
                : "text-gray-600 dark:text-gray-400"
            } line-clamp-2`}>
              {task.description}
            </p>
          )}

          {/* Metadata footer */}
          <div className="flex items-center justify-between pt-1">
            {/* Status badge */}
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${config.badge}`}>
              {config.label}
            </span>

            {/* Date */}
            <span className="text-xs text-gray-500 dark:text-gray-500">
              {new Date(task.created_at).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
              })}
            </span>
          </div>
        </div>

        {/* Drag handle indicator */}
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <svg
            className="w-3 h-3 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 8h16M4 16h16"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
