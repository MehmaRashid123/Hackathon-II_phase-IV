/**
 * Chat API Service
 * 
 * Handles communication with the Gemini-powered chat backend.
 */

import { auth } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ToolCall {
  tool_name: string;
  parameters: Record<string, any>;
  result?: Record<string, any>;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
  tool_calls?: ToolCall[];
  timestamp: string;
}

/**
 * Send a chat message to the Gemini-powered backend
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  try {
    // Get JWT token from localStorage
    const token = auth.getToken();
    if (!token) {
      throw new Error("Not authenticated. Please log in.");
    }

    const url = `${API_URL}/api/${userId}/chat`;
    console.log("📤 Sending chat request:", {
      url,
      userId,
      messageLength: message.length,
      hasConversationId: !!conversationId,
      tokenPreview: token.substring(0, 20) + "..."
    });

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({
        message: message,
        conversation_id: conversationId,
      }),
    });

    console.log("📥 Response status:", response.status, response.statusText);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Error response:", errorText);
      
      if (response.status === 401) {
        throw new Error("Session expired. Please log in again.");
      }
      if (response.status === 403) {
        throw new Error("Access denied.");
      }
      
      try {
        const errorData = JSON.parse(errorText);
        throw new Error(errorData.detail || `Chat API error: ${response.status}`);
      } catch {
        throw new Error(`Chat API error: ${response.status} - ${errorText}`);
      }
    }

    const data = await response.json();
    console.log("✅ Chat response:", data);
    return data;
  } catch (error) {
    console.error("❌ Error sending chat message:", error);
    throw error;
  }
}

/**
 * Process natural language command through Gemini chat API
 * This is the main function used by the chatbot component
 */
export async function processMCPCommand(
  userId: string,
  command: string,
  conversationId?: string
): Promise<ChatResponse> {
  try {
    const response = await sendChatMessage(userId, command, conversationId);
    return response;
  } catch (error) {
    console.error("Error processing chat command:", error);
    throw error;
  }
}
