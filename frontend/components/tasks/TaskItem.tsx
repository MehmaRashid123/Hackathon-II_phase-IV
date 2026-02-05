/**
 * TaskItem component - Individual task display with animations.
 *
 * Shows task with animated checkbox, status colors, and hover effects.
 * Different colors for: Complete (Green), In Progress (Blue), Pending (Gray)
 */

"use client";

import { motion } from "framer-motion";
import { Task } from "@/lib/types/task";
import { CheckCircle2, Circle, Clock, Eye, CheckCheck, Edit3, Trash2 } from "lucide-react";
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

  // Status configuration with colors and icons
  const getStatusConfig = () => {
    // Determine status: use task.status if available, otherwise infer from is_completed
    const status = task.status || (task.is_completed ? "DONE" : "TO_DO");

    if (status === "DONE" || task.is_completed) {
      return {
        bgColor: "bg-green-50 dark:bg-green-900/20 border-green-300 dark:border-green-600",
        textColor: "text-green-900 dark:text-green-200",
        badgeColor: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
        icon: CheckCheck,
        iconColor: "text-green-500",
        label: "Completed",
        stripeColor: "bg-gradient-to-r from-green-400 to-green-600"
      };
    }

    switch (status) {
      case "IN_PROGRESS":
        return {
          bgColor: "bg-blue-50 dark:bg-blue-900/20 border-blue-300 dark:border-blue-600",
          textColor: "text-blue-900 dark:text-blue-200",
          badgeColor: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
          icon: Clock,
          iconColor: "text-blue-500",
          label: "In Progress",
          stripeColor: "bg-gradient-to-r from-blue-400 to-blue-600"
        };
      case "REVIEW":
        return {
          bgColor: "bg-purple-50 dark:bg-purple-900/20 border-purple-300 dark:border-purple-600",
          textColor: "text-purple-900 dark:text-purple-200",
          badgeColor: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
          icon: Eye,
          iconColor: "text-purple-500",
          label: "Review",
          stripeColor: "bg-gradient-to-r from-purple-400 to-purple-600"
        };
      case "TO_DO":
      default:
        return {
          bgColor: "bg-gray-50 dark:bg-gray-800/60 border-gray-300 dark:border-gray-600",
          textColor: "text-gray-700 dark:text-gray-300",
          badgeColor: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
          icon: Circle,
          iconColor: "text-gray-400",
          label: "To Do",
          stripeColor: "bg-gradient-to-r from-gray-400 to-gray-500"
        };
    }
  };

  const config = getStatusConfig();
  const StatusIcon = config.icon;

  return (
    <motion.div
      className={`
        relative overflow-hidden
        flex items-start gap-4 p-5
        ${config.bgColor}
        border-2 rounded-xl
        shadow-md hover:shadow-xl
        transition-all duration-300
      `}
      variants={itemVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      whileHover={reducedMotion ? {} : { scale: 1.02, y: -2 }}
      layout
    >
      {/* Status stripe */}
      <div className={`absolute top-0 left-0 w-full h-1.5 ${config.stripeColor}`} />

      {/* Status Icon & Checkbox */}
      <div className="flex flex-col items-center gap-2 pt-1">
        <div className={`${config.iconColor}`}>
          <StatusIcon size={24} strokeWidth={2.5} />
        </div>

        <motion.button
          onClick={() => onToggleComplete(task.id)}
          className="flex-shrink-0 cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-full p-1"
          variants={checkVariants}
          animate={task.is_completed ? "checked" : "unchecked"}
          whileTap={reducedMotion ? {} : { scale: 0.9 }}
          title={task.is_completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.is_completed ? (
            <CheckCircle2 className="h-6 w-6 text-green-600 fill-green-100" />
          ) : (
            <Circle className="h-6 w-6 text-gray-400 hover:text-gray-600" />
          )}
        </motion.button>
      </div>

      {/* Task Content */}
      <div className="flex-1 min-w-0 space-y-2">
        {/* Title with completion checkmark */}
        <div className="flex items-start gap-2">
          <h3
            className={`flex-1 text-lg font-semibold ${config.textColor} ${
              task.is_completed
                ? "line-through opacity-75"
                : ""
            }`}
          >
            {task.title}
          </h3>

          {task.is_completed && (
            <CheckCircle2
              className="flex-shrink-0 text-green-500 animate-in zoom-in duration-300"
              size={20}
              fill="currentColor"
            />
          )}
        </div>

        {/* Description */}
        {task.description && (
          <p
            className={`text-sm ${
              task.is_completed
                ? "text-gray-500 dark:text-gray-500 line-through opacity-60"
                : "text-gray-600 dark:text-gray-400"
            }`}
          >
            {task.description}
          </p>
        )}

        {/* Footer: Status badge & date */}
        <div className="flex items-center justify-between pt-2">
          <span className={`px-3 py-1.5 rounded-full text-xs font-semibold ${config.badgeColor}`}>
            {config.label}
          </span>

          <span className="text-xs text-gray-500 dark:text-gray-400">
            {new Date(task.created_at).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric"
            })}
          </span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col gap-2 pt-1">
        {onEdit && (
          <motion.button
            onClick={() => onEdit(task)}
            className="p-2 text-blue-600 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors"
            whileHover={reducedMotion ? {} : { scale: 1.1 }}
            whileTap={reducedMotion ? {} : { scale: 0.95 }}
            title="Edit task"
          >
            <Edit3 size={18} />
          </motion.button>
        )}
        <motion.button
          onClick={() => onDelete(task.id)}
          className="p-2 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg transition-colors"
          whileHover={reducedMotion ? {} : { scale: 1.1 }}
          whileTap={reducedMotion ? {} : { scale: 0.95 }}
          title="Delete task"
        >
          <Trash2 size={18} />
        </motion.button>
      </div>
    </motion.div>
  );
}
