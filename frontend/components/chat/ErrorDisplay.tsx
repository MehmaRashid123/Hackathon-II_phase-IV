/**
 * ErrorDisplay Component
 * Displays inline error messages with dismiss option
 */

import { AlertCircle, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ErrorDisplayProps {
  error: string;
  onDismiss: () => void;
}

export function ErrorDisplay({ error, onDismiss }: ErrorDisplayProps) {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3 flex items-start gap-2">
      <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
      </div>
      <Button
        variant="ghost"
        size="sm"
        onClick={onDismiss}
        className="h-6 w-6 p-0 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/40"
      >
        <X className="h-4 w-4" />
      </Button>
    </div>
  );
}
