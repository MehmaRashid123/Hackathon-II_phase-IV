/**
 * Message Component
 * Displays an individual chat message
 */

import { ChatMessage } from "@/lib/types/chat";
import { Bot, User } from "lucide-react";
import { MessageContent } from "./MessageContent";
import { MessageTimestamp } from "./MessageTimestamp";
import { MessageStatus } from "./MessageStatus";
import { ToolExecutionBadge } from "./ToolExecutionBadge";

interface MessageProps {
  message: ChatMessage;
  onRetry?: (messageId: string) => void;
}

export function Message({ message, onRetry }: MessageProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";

  return (
    <div
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""} ${
        isSystem ? "justify-center" : ""
      }`}
    >
      {/* Avatar */}
      {!isSystem && (
        <div
          className={`h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0 ${
            isUser ? "bg-blue-600" : "bg-purple-600"
          }`}
        >
          {isUser ? (
            <User className="h-4 w-4 text-white" />
          ) : (
            <Bot className="h-4 w-4 text-white" />
          )}
        </div>
      )}

      {/* Message Content */}
      <div className={`flex-1 ${isUser ? "text-right" : ""} ${isSystem ? "text-center" : ""}`}>
        <div
          className={`inline-block p-3 rounded-2xl ${
            isUser
              ? "bg-blue-600 text-white"
              : isSystem
              ? "bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-sm"
              : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          }`}
        >
          <MessageContent content={message.content} />
          
          {/* Tool Execution Badges */}
          {message.toolCalls && message.toolCalls.length > 0 && (
            <div className="mt-2 space-y-1">
              {message.toolCalls.map((toolCall, index) => (
                <ToolExecutionBadge key={index} toolCall={toolCall} />
              ))}
            </div>
          )}
        </div>

        {/* Timestamp and Status */}
        {!isSystem && (
          <div className="flex items-center gap-2 mt-1">
            {isUser && <MessageStatus status={message.status} onRetry={() => onRetry?.(message.id)} />}
            <MessageTimestamp timestamp={message.timestamp} />
            {!isUser && <MessageStatus status={message.status} />}
          </div>
        )}
      </div>
    </div>
  );
}
