/**
 * MessageStatus Component
 * Displays message sending status with retry option
 */

import { MessageStatus as Status } from "@/lib/types/chat";
import { Check, CheckCheck, AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface MessageStatusProps {
  status: Status;
  onRetry?: () => void;
}

export function MessageStatus({ status, onRetry }: MessageStatusProps) {
  if (status === "sending") {
    return (
      <div className="flex items-center gap-1 text-xs text-gray-500">
        <RefreshCw className="h-3 w-3 animate-spin" />
        <span>Sending...</span>
      </div>
    );
  }

  if (status === "sent") {
    return (
      <div className="flex items-center gap-1 text-xs text-green-600 dark:text-green-400">
        <CheckCheck className="h-3 w-3" />
      </div>
    );
  }

  if (status === "failed") {
    return (
      <div className="flex items-center gap-1 text-xs text-red-600 dark:text-red-400">
        <AlertCircle className="h-3 w-3" />
        <span>Failed</span>
        {onRetry && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onRetry}
            className="h-5 px-2 text-xs"
          >
            Retry
          </Button>
        )}
      </div>
    );
  }

  return null;
}
