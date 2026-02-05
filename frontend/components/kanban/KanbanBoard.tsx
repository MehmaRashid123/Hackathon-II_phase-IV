/**
 * KanbanBoard Component
 *
 * Premium Kanban board with drag-and-drop, optimistic updates, and celebrations.
 */

"use client";

import React, { useState, useEffect } from "react";
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  TouchSensor,
  useSensor,
  useSensors,
  closestCorners,
} from "@dnd-kit/core";
import { KanbanTask, TaskStatus, KANBAN_COLUMNS } from "@/lib/types/kanban";
import { KanbanColumn } from "./KanbanColumn";
import { KanbanCard } from "./KanbanCard";
import { KanbanService } from "@/lib/services/kanban-service";
import { useWorkspace } from "@/lib/hooks/use-workspace";
import { celebrateTaskCompletion } from "@/lib/utils/confetti";

interface KanbanBoardProps {
  initialTasks?: KanbanTask[];
}

export function KanbanBoard({ initialTasks = [] }: KanbanBoardProps) {
  const { currentWorkspace } = useWorkspace();
  const [tasks, setTasks] = useState<KanbanTask[]>(initialTasks);
  const [activeTask, setActiveTask] = useState<KanbanTask | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Configure sensors for better touch/pointer support
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement before drag starts
      },
    }),
    useSensor(TouchSensor, {
      activationConstraint: {
        delay: 200, // 200ms hold before drag starts on touch
        tolerance: 8,
      },
    })
  );

  // Load tasks on mount
  useEffect(() => {
    loadTasks();
  }, [currentWorkspace]);

  async function loadTasks() {
    try {
      setIsLoading(true);
      setError(null);

      // If workspace is selected, fetch workspace tasks
      if (currentWorkspace) {
        const workspaceTasks = await KanbanService.getWorkspaceTasks(
          currentWorkspace.id
        );
        setTasks(workspaceTasks);
      } else {
        // Fallback: fetch user tasks and convert to KanbanTask format
        const { taskApi } = await import("@/lib/api/tasks");
        const userTasks = await taskApi.list();

        // Load saved statuses from localStorage
        const savedStatuses = loadSavedStatuses();

        // Convert Task[] to KanbanTask[] with status from localStorage or default
        const kanbanTasks: KanbanTask[] = userTasks.map(task => ({
          ...task,
          status: savedStatuses[task.id] || task.status || (task.is_completed ? "DONE" : "TO_DO"),
          workspace_id: task.workspace_id || undefined
        }));

        setTasks(kanbanTasks);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  }

  // Helper functions for localStorage status persistence
  function loadSavedStatuses(): Record<string, TaskStatus> {
    if (typeof window === 'undefined') return {};
    try {
      const saved = localStorage.getItem('kanban-task-statuses');
      return saved ? JSON.parse(saved) : {};
    } catch {
      return {};
    }
  }

  function saveTaskStatus(taskId: string, status: TaskStatus) {
    if (typeof window === 'undefined') return;
    try {
      const statuses = loadSavedStatuses();
      statuses[taskId] = status;
      localStorage.setItem('kanban-task-statuses', JSON.stringify(statuses));
    } catch (err) {
      console.error('Failed to save task status:', err);
    }
  }

  function handleDragStart(event: DragStartEvent) {
    const { active } = event;
    const task = tasks.find((t) => t.id === active.id);
    if (task) {
      setActiveTask(task);
    }
  }

  async function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    setActiveTask(null);

    if (!over) return;

    const taskId = active.id as string;
    const newStatus = over.id as TaskStatus;

    const task = tasks.find((t) => t.id === taskId);
    if (!task) return;

    // Get actual current status (with fallback)
    const currentStatus = task.status || (task.is_completed ? "DONE" : "TO_DO");

    if (currentStatus === newStatus) return;

    const oldStatus = currentStatus;

    // Optimistic UI update (instant feedback)
    setTasks((prevTasks) =>
      prevTasks.map((t) =>
        t.id === taskId
          ? { ...t, status: newStatus, is_completed: newStatus === "DONE" }
          : t
      )
    );

    // Save to localStorage for non-workspace tasks
    if (!currentWorkspace) {
      saveTaskStatus(taskId, newStatus);
    }

    // Trigger confetti if moved to DONE
    if (newStatus === "DONE") {
      celebrateTaskCompletion();
    }

    try {
      // Backend update - choose based on workspace availability
      if (currentWorkspace) {
        await KanbanService.updateTaskStatus(
          currentWorkspace.id,
          taskId,
          newStatus
        );
      } else {
        // For non-workspace tasks, use toggleComplete API if moving to/from DONE
        const { taskApi } = await import("@/lib/api/tasks");

        // Update completion status if crossing DONE boundary
        const shouldBeCompleted = newStatus === "DONE";
        if (task.is_completed !== shouldBeCompleted) {
          await taskApi.toggleComplete(taskId);
        }
      }
    } catch (err) {
      // Rollback on error
      setTasks((prevTasks) =>
        prevTasks.map((t) =>
          t.id === taskId
            ? { ...t, status: oldStatus, is_completed: oldStatus === "DONE" }
            : t
        )
      );

      // Rollback localStorage
      if (!currentWorkspace) {
        saveTaskStatus(taskId, oldStatus);
      }

      // Show error notification
      setError(err instanceof Error ? err.message : "Failed to update task status");

      // Clear error after 5 seconds
      setTimeout(() => setError(null), 5000);
    }
  }

  // Group tasks by status for columns
  const groupedTasks = KanbanService.groupTasksByStatus(tasks);

  return (
    <div className="relative h-full">
      {/* Error notification */}
      {error && (
        <div className="absolute top-0 left-1/2 -translate-x-1/2 z-50 animate-in slide-in-from-top duration-300">
          <div className="px-6 py-3 rounded-xl bg-red-500/90 backdrop-blur-md text-white shadow-lg">
            <p className="font-medium">{error}</p>
          </div>
        </div>
      )}

      {/* Loading state */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="flex flex-col items-center space-y-4">
            <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Loading tasks...
            </p>
          </div>
        </div>
      ) : (
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          {/* Kanban columns - Responsive grid with proper scrolling */}
          <div className="h-full w-full overflow-x-auto overflow-y-hidden">
            <div className="flex gap-4 h-full min-w-max lg:grid lg:grid-cols-4 lg:gap-6">
              {KANBAN_COLUMNS.map((column) => (
                <KanbanColumn
                  key={column.id}
                  id={column.id}
                  title={column.title}
                  tasks={groupedTasks[column.id]}
                  color={column.color}
                />
              ))}
            </div>
          </div>

          {/* Drag overlay (card being dragged) */}
          <DragOverlay>
            {activeTask ? <KanbanCard task={activeTask} isDragging /> : null}
          </DragOverlay>
        </DndContext>
      )}

      {/* Mobile horizontal scroll hint */}
      <div className="lg:hidden mt-2 text-center flex-shrink-0">
        <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center justify-center gap-2">
          <span>←</span>
          <span>Swipe to view all columns</span>
          <span>→</span>
        </p>
      </div>
    </div>
  );
}
