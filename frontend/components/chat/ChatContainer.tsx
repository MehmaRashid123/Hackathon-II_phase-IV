/**
 * ChatContainer Component
 * Main wrapper for chat interface
 */

import { ChatMessage } from "@/lib/types/chat";
import { ChatHeader } from "./ChatHeader";
import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import { ErrorDisplay } from "./ErrorDisplay";

interface ChatContainerProps {
  conversationTitle?: string;
  messages: ChatMessage[];
  isLoading: boolean;
  isSending: boolean;
  error: string | null;
  onSendMessage: (content: string) => void;
  onRetry: (messageId: string) => void;
  onNewConversation: () => void;
  onClearError: () => void;
}

export function ChatContainer({
  conversationTitle,
  messages,
  isLoading,
  isSending,
  error,
  onSendMessage,
  onRetry,
  onNewConversation,
  onClearError,
}: ChatContainerProps) {
  return (
    <div className="h-full bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-800 flex flex-col overflow-hidden">
      {/* Header */}
      <ChatHeader
        title={conversationTitle}
        onNewConversation={onNewConversation}
      />

      {/* Messages */}
      <MessageList
        messages={messages}
        isLoading={isLoading}
        onRetry={onRetry}
      />

      {/* Error Display */}
      {error && (
        <div className="px-4 pb-2">
          <ErrorDisplay error={error} onDismiss={onClearError} />
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-800">
        <ChatInput
          onSend={onSendMessage}
          disabled={isSending}
          placeholder="Ask me to manage your tasks..."
        />
      </div>
    </div>
  );
}
