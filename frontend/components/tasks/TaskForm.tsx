/**
 * TaskForm component - Create and edit tasks.
 *
 * Handles form validation and submission.
 */

"use client";

import { useState, FormEvent } from "react";
import { Task, TaskCreateInput } from "@/lib/types/task";

interface TaskFormProps {
  onSubmit: (data: TaskCreateInput) => Promise<void>;
  initialData?: Task;
  submitLabel?: string;
  onCancel?: () => void;
}

export function TaskForm({
  onSubmit,
  initialData,
  submitLabel = "Add Task",
  onCancel,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(
    initialData?.description || ""
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    if (title.length > 500) {
      setError("Title must be less than 500 characters");
      return;
    }

    if (description.length > 5000) {
      setError("Description must be less than 5000 characters");
      return;
    }

    try {
      setLoading(true);
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Clear form on success (only for create mode)
      if (!initialData) {
        setTitle("");
        setDescription("");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Title Input */}
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          maxLength={500}
          className="w-full px-4 py-2 input-primary"
          required
        />
        <p className="mt-1 text-xs text-gray-500">
          {title.length}/500 characters
        </p>
      </div>

      {/* Description Input */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details about this task (optional)"
          maxLength={5000}
          rows={3}
          className="w-full px-4 py-2 input-primary resize-none"
        />
        <p className="mt-1 text-xs text-gray-500">
          {description.length}/5000 characters
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 px-4 py-2 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Saving..." : submitLabel}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-100 text-gray-700 font-medium rounded-xl hover:bg-gray-200 transition-colors shadow-sm"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
