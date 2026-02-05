/**
 * TaskItem component - Individual task display with animations.
 *
 * Shows task with animated checkbox, Lucide icons, and hover effects.
 */

"use client";

import { motion } from "framer-motion";
import { Task } from "@/lib/types/task";
import { CheckCircle, Circle, Edit3, Trash2 } from "lucide-react";
import { staggerItemVariants, checkboxVariants } from "@/lib/animations/variants";
import { useReducedMotion } from "@/lib/hooks/useReducedMotion";

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: string) => void;
  onEdit?: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const reducedMotion = useReducedMotion();

  const itemVariants = reducedMotion
    ? { hidden: { opacity: 1 }, visible: { opacity: 1 }, exit: { opacity: 1 } }
    : staggerItemVariants;

  const checkVariants = reducedMotion
    ? { unchecked: {}, checked: {} }
    : checkboxVariants;

  return (
    <motion.div
      className="flex items-start gap-3 p-4 bg-white border border-gray-200 rounded-lg transition-all"
      variants={itemVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      whileHover={reducedMotion ? {} : { scale: 1.02, boxShadow: "0 10px 20px rgba(0,0,0,0.1)" }}
      layout
    >
      {/* Animated Checkbox with Lucide Icons */}
      <motion.button
        onClick={() => onToggleComplete(task.id)}
        className="mt-1 flex-shrink-0 cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
        variants={checkVariants}
        animate={task.is_completed ? "checked" : "unchecked"}
        whileTap={reducedMotion ? {} : { scale: 0.9 }}
      >
        {task.is_completed ? (
          <CheckCircle className="h-5 w-5 text-blue-600" />
        ) : (
          <Circle className="h-5 w-5 text-gray-400" />
        )}
      </motion.button>

      {/* Task Content */}
      <div className="flex-1 min-w-0">
        <h3
          className={`text-lg font-medium ${
            task.is_completed
              ? "line-through text-gray-400"
              : "text-gray-900"
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p
            className={`mt-1 text-sm ${
              task.is_completed ? "text-gray-400" : "text-gray-600"
            }`}
          >
            {task.description}
          </p>
        )}
        <p className="mt-2 text-xs text-gray-400">
          {new Date(task.created_at).toLocaleDateString()}
        </p>
      </div>

      {/* Actions with Lucide Icons */}
      <div className="flex gap-2">
        {onEdit && (
          <motion.button
            onClick={() => onEdit(task)}
            className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded-md transition-colors flex items-center gap-1"
            whileHover={reducedMotion ? {} : { scale: 1.05 }}
            whileTap={reducedMotion ? {} : { scale: 0.95 }}
          >
            <Edit3 size={14} />
            Edit
          </motion.button>
        )}
        <motion.button
          onClick={() => onDelete(task.id)}
          className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors flex items-center gap-1"
          whileHover={reducedMotion ? {} : { scale: 1.05 }}
          whileTap={reducedMotion ? {} : { scale: 0.95 }}
        >
          <Trash2 size={14} />
          Delete
        </motion.button>
      </div>
    </motion.div>
  );
}
