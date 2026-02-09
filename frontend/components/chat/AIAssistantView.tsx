/**
 * AIAssistantView Component
 * Main container for the AI Assistant chat interface
 */

"use client";

import { useEffect } from "react";
import { useChatStore } from "@/lib/stores/chatStore";
import { ChatContainer } from "./ChatContainer";
import { ChatMessage } from "@/lib/types/chat";

interface AIAssistantViewProps {
  userId: string;
  initialConversationId?: string;
}

export function AIAssistantView({
  userId,
  initialConversationId,
}: AIAssistantViewProps) {
  const {
    currentConversationId,
    conversations,
    isLoading,
    isSending,
    error,
    sendMessage,
    retryFailedMessage,
    createNewConversation,
    clearError,
  } = useChatStore();

  // Initialize conversation on mount
  useEffect(() => {
    // Try to restore conversation from localStorage or URL
    const storedConversationId =
      initialConversationId || localStorage.getItem("currentConversationId");

    if (storedConversationId) {
      // Load existing conversation (backend will validate UUID)
      useChatStore.getState().loadConversation(storedConversationId);
    }
    // If no stored conversation, leave it null - backend will create one on first message
  }, [initialConversationId]);

  // Get current conversation
  const currentConversation = currentConversationId
    ? conversations[currentConversationId]
    : null;

  // Get messages or show welcome message
  const messages: ChatMessage[] = currentConversation?.messages || [
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hi! I'm your AI task management assistant powered by Gemini. I can help you create, update, and manage your tasks. Try asking me to 'add a task' or 'show my tasks'!",
      timestamp: new Date(),
      status: "sent",
    },
  ];

  return (
    <div className="h-full">
      <ChatContainer
        conversationTitle={currentConversation?.title}
        messages={messages}
        isLoading={isLoading}
        isSending={isSending}
        error={error}
        onSendMessage={sendMessage}
        onRetry={retryFailedMessage}
        onNewConversation={createNewConversation}
        onClearError={clearError}
      />
    </div>
  );
}
