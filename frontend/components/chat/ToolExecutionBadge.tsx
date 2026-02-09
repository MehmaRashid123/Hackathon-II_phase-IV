/**
 * ToolExecutionBadge Component
 * Displays tool execution indicators
 */

import { ToolCall } from "@/lib/types/chat";
import { Wrench, CheckCircle } from "lucide-react";

interface ToolExecutionBadgeProps {
  toolCall: ToolCall;
}

export function ToolExecutionBadge({ toolCall }: ToolExecutionBadgeProps) {
  return (
    <div className="flex items-center gap-2 text-xs bg-white/10 dark:bg-black/10 px-2 py-1 rounded">
      <Wrench className="h-3 w-3" />
      <span className="font-medium">{toolCall.tool_name}</span>
      {toolCall.result && <CheckCircle className="h-3 w-3 text-green-500" />}
    </div>
  );
}
