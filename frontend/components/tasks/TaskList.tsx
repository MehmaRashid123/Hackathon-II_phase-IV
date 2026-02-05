/**
 * TaskList component - Display all tasks with stagger animations.
 *
 * Handles empty state, loading state, and animates task items with 50ms stagger delay.
 */

"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Task } from "@/lib/types/task";
import { TaskItem } from "./TaskItem";
import { staggerContainerVariants } from "@/lib/animations/variants";
import { useReducedMotion } from "@/lib/hooks/useReducedMotion";
import { Loader2, AlertCircle } from "lucide-react";

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  onToggleComplete: (taskId: string) => void;
  onEdit?: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export function TaskList({
  tasks,
  loading,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskListProps) {
  const reducedMotion = useReducedMotion();

  // Cap stagger animations for large lists (performance optimization)
  const shouldStagger = tasks.length <= 20 && !reducedMotion;

  const containerVariants = reducedMotion
    ? { hidden: { opacity: 1 }, visible: { opacity: 1 } }
    : shouldStagger
    ? staggerContainerVariants
    : { hidden: { opacity: 1 }, visible: { opacity: 1 } };

  // Loading state with animated spinner
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="h-12 w-12 text-blue-600 animate-spin" />
        <p className="mt-4 text-sm text-gray-500">Loading tasks...</p>
      </div>
    );
  }

  // Empty state
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks yet</h3>
        <p className="mt-1 text-sm text-gray-500">
          Get started by creating a new task above.
        </p>
      </div>
    );
  }

  // Task list with stagger animations
  return (
    <motion.div
      className="space-y-3"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <AnimatePresence mode="popLayout">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggleComplete={onToggleComplete}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </AnimatePresence>
    </motion.div>
  );
}
