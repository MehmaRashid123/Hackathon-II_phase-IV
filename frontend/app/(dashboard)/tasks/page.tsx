/**
 * Tasks Page - List view of all tasks.
 *
 * Protected route - requires authentication.
 */

"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api/auth";
import { useTasks } from "@/lib/hooks/useTasks";
import { useToast } from "@/lib/hooks/useToast";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskList } from "@/components/tasks/TaskList";
import { PageTransition } from "@/components/ui/PageTransition";
import { AnimatedProgress } from "@/components/ui/AnimatedProgress";
import { SkeletonCard } from "@/components/SkeletonCard";
import { Plus, Grid3x3, List } from "lucide-react";
import Link from "next/link";

export default function TasksPage() {
  const router = useRouter();
  const [user, setUser] = useState<{ email: string } | null>(null);
  const [showForm, setShowForm] = useState(false);

  const {
    tasks,
    loading,
    error: tasksError,
    createTask,
    toggleComplete,
    deleteTask,
  } = useTasks();

  const { toasts, showToast, removeToast } = useToast();

  // Calculate progress with debouncing (derived state)
  const { percentage, completedCount } = useMemo(() => {
    const completedCount = tasks.filter((t) => t.is_completed).length;
    const percentage = tasks.length > 0 ? (completedCount / tasks.length) * 100 : 0;
    return { percentage, completedCount };
  }, [tasks]);

  // Route protection - redirect if not authenticated
  useEffect(() => {
    const currentUser = auth.getUser();
    if (!currentUser) {
      router.push("/login");
      return;
    }
    setUser(currentUser);
  }, [router]);

  // Show toast for task errors
  useEffect(() => {
    if (tasksError) {
      showToast(tasksError, "error");
    }
  }, [tasksError, showToast]);

  // Handle create task
  const handleCreateTask = async (data: { title: string; description?: string }) => {
    try {
      await createTask(data);
      setShowForm(false);
      showToast("Task created successfully!", "success");
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Failed to create task", "error");
    }
  };

  // Handle toggle completion
  const handleToggleComplete = async (taskId: string) => {
    try {
      await toggleComplete(taskId);
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Failed to update task", "error");
    }
  };

  // Handle delete task
  const handleDeleteTask = async (taskId: string) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      await deleteTask(taskId);
      showToast("Task deleted successfully!", "success");
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Failed to delete task", "error");
    }
  };

  // Show loading while checking auth
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        {/* Header */}
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Tasks</h1>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Manage all your tasks in list view
                </p>
              </div>
              <div className="flex items-center gap-3">
                {/* View Toggle */}
                <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                  <button
                    className="px-3 py-2 rounded-md bg-white dark:bg-gray-600 shadow-sm text-gray-900 dark:text-white"
                    title="List View (Active)"
                  >
                    <List size={18} />
                  </button>
                  <Link
                    href="/kanban"
                    className="px-3 py-2 rounded-md hover:bg-white/50 dark:hover:bg-gray-600/50 text-gray-600 dark:text-gray-300 transition-colors"
                    title="Switch to Kanban View"
                  >
                    <Grid3x3 size={18} />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Progress Bar */}
          {tasks.length > 0 && (
            <div className="mb-8">
              <AnimatedProgress
                percentage={percentage}
                total={tasks.length}
                completed={completedCount}
              />
            </div>
          )}

          {/* Header with Create Button */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">My Tasks</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {tasks.length} {tasks.length === 1 ? "task" : "tasks"} total
                </p>
              </div>
              <button
                onClick={() => setShowForm(!showForm)}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2"
              >
                {showForm ? (
                  "Cancel"
                ) : (
                  <>
                    <Plus size={20} />
                    New Task
                  </>
                )}
              </button>
            </div>

            {/* Task Creation Form */}
            {showForm && (
              <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Create New Task
                </h3>
                <TaskForm
                  onSubmit={handleCreateTask}
                  submitLabel="Create Task"
                  onCancel={() => setShowForm(false)}
                />
              </div>
            )}
          </div>

          {/* Task List */}
          {loading && tasks.length === 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              loading={loading}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTask}
            />
          )}
        </main>

        {/* Toast Notifications */}
        <div className="fixed bottom-4 right-4 space-y-2 z-50">
          {toasts.map((toast) => (
            <div
              key={toast.id}
              className={`px-6 py-3 rounded-lg shadow-lg text-white flex items-center gap-3 ${
                toast.type === "success"
                  ? "bg-green-600"
                  : toast.type === "error"
                  ? "bg-red-600"
                  : "bg-blue-600"
              }`}
            >
              <span>{toast.message}</span>
              <button
                onClick={() => removeToast(toast.id)}
                className="text-white hover:text-gray-200"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>
    </PageTransition>
  );
}
