/**
 * Chat Store
 * Zustand store for managing chat state
 */

import { create } from "zustand";
import { ChatState, ChatMessage, Conversation } from "@/lib/types/chat";
import { sendChatMessage } from "@/lib/api/chat";
import { auth } from "@/lib/api/auth";

const generateTempId = () => `temp-${Date.now()}-${Math.random()}`;

export const useChatStore = create<ChatState>((set, get) => ({
  // Initial state
  currentConversationId: null,
  conversations: {},
  isLoading: false,
  isSending: false,
  error: null,

  // Add message to current conversation
  addMessage: (message: ChatMessage) => {
    const { currentConversationId, conversations } = get();
    if (!currentConversationId) return;

    const conversation = conversations[currentConversationId];
    if (!conversation) return;

    set({
      conversations: {
        ...conversations,
        [currentConversationId]: {
          ...conversation,
          messages: [...conversation.messages, message],
          lastMessageAt: message.timestamp,
        },
      },
    });
  },

  // Update existing message
  updateMessage: (id: string, updates: Partial<ChatMessage>) => {
    const { currentConversationId, conversations } = get();
    if (!currentConversationId) return;

    const conversation = conversations[currentConversationId];
    if (!conversation) return;

    set({
      conversations: {
        ...conversations,
        [currentConversationId]: {
          ...conversation,
          messages: conversation.messages.map((msg) =>
            msg.id === id ? { ...msg, ...updates } : msg
          ),
        },
      },
    });
  },

  // Send message with optimistic UI
  sendMessage: async (content: string) => {
    const { currentConversationId, conversations, addMessage, updateMessage } = get();
    
    // Get user ID
    const user = auth.getUser();
    if (!user?.id) {
      set({ error: "Please log in to send messages" });
      return;
    }

    // Create optimistic message
    const tempId = generateTempId();
    const userMessage: ChatMessage = {
      id: tempId,
      role: "user",
      content,
      timestamp: new Date(),
      status: "sending",
    };

    // Add optimistically
    addMessage(userMessage);
    set({ isSending: true, error: null });

    try {
      // Send to backend
      const response = await sendChatMessage(
        user.id,
        content,
        currentConversationId || undefined
      );

      // Update conversation ID if new
      if (response.conversation_id && !currentConversationId) {
        set({ currentConversationId: response.conversation_id });
        
        // Store in localStorage
        localStorage.setItem("currentConversationId", response.conversation_id);
        
        // Create conversation if it doesn't exist
        if (!conversations[response.conversation_id]) {
          const newConversation: Conversation = {
            id: response.conversation_id,
            title: content.slice(0, 50) + (content.length > 50 ? "..." : ""),
            messages: [],
            lastMessageAt: new Date(),
            isActive: true,
          };
          set({
            conversations: {
              ...conversations,
              [response.conversation_id]: newConversation,
            },
          });
        }
      }

      // Update message status to sent
      updateMessage(tempId, { status: "sent" });

      // Add AI response
      const aiMessage: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: response.message,
        timestamp: new Date(response.timestamp),
        status: "sent",
        toolCalls: response.tool_calls,
      };
      addMessage(aiMessage);

    } catch (error) {
      console.error("Error sending message:", error);
      
      // Update message status to failed
      updateMessage(tempId, { status: "failed" });
      
      const errorMsg = error instanceof Error ? error.message : "Failed to send message";
      set({ error: errorMsg });
    } finally {
      set({ isSending: false });
    }
  },

  // Retry failed message
  retryFailedMessage: async (messageId: string) => {
    const { currentConversationId, conversations, updateMessage } = get();
    if (!currentConversationId) return;

    const conversation = conversations[currentConversationId];
    if (!conversation) return;

    const message = conversation.messages.find((msg) => msg.id === messageId);
    if (!message || message.status !== "failed") return;

    // Update status to sending
    updateMessage(messageId, { status: "sending" });
    set({ isSending: true, error: null });

    const user = auth.getUser();
    if (!user?.id) {
      set({ error: "Please log in to send messages" });
      return;
    }

    try {
      // Resend message
      const response = await sendChatMessage(
        user.id,
        message.content,
        currentConversationId
      );

      // Update message status to sent
      updateMessage(messageId, { status: "sent" });

      // Add AI response
      const aiMessage: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: response.message,
        timestamp: new Date(response.timestamp),
        status: "sent",
        toolCalls: response.tool_calls,
      };
      get().addMessage(aiMessage);

    } catch (error) {
      console.error("Error retrying message:", error);
      
      // Update message status back to failed
      updateMessage(messageId, { status: "failed" });
      
      const errorMsg = error instanceof Error ? error.message : "Failed to send message";
      set({ error: errorMsg });
    } finally {
      set({ isSending: false });
    }
  },

  // Load conversation (placeholder - backend doesn't support this yet)
  loadConversation: async (id: string) => {
    set({ isLoading: true, error: null });
    
    try {
      // For now, just set the current conversation ID
      // In the future, this would fetch conversation history from backend
      set({ currentConversationId: id });
      localStorage.setItem("currentConversationId", id);
    } catch (error) {
      console.error("Error loading conversation:", error);
      const errorMsg = error instanceof Error ? error.message : "Failed to load conversation";
      set({ error: errorMsg });
    } finally {
      set({ isLoading: false });
    }
  },

  // Create new conversation
  createNewConversation: () => {
    // Clear current conversation ID to start fresh
    // Backend will create a new UUID-based conversation ID on first message
    set({
      currentConversationId: null,
      conversations: {},
    });

    localStorage.removeItem("currentConversationId");
  },

  // Clear error
  clearError: () => set({ error: null }),
}));
