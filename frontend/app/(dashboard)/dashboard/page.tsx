/**
 * Dashboard Page - Main task management interface.
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
import { Plus } from "lucide-react";

export default function DashboardPage() {
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

  // Handle logout
  const handleLogout = () => {
    auth.clearAuth();
    router.push("/login");
  };

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
      <div className="min-h-screen bg-gray-50">
        {/* Navbar */}
        <nav className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-gray-900">Task Dashboard</h1>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600">{user.email}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium text-white glass-button bg-red-600 hover:bg-red-700 transition-colors"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        </nav>

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
                <h2 className="text-2xl font-bold text-gray-900">My Tasks</h2>
                <p className="text-sm text-gray-600 mt-1">
                  {tasks.length} {tasks.length === 1 ? "task" : "tasks"} total
                </p>
              </div>
              <button
                onClick={() => setShowForm(!showForm)}
                className="px-6 py-3 btn-primary shadow-sm flex items-center gap-2"
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
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
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
