/**
 * ChatHeader Component
 * Header with conversation title and new conversation button
 */

import { Plus, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
  title?: string;
  onNewConversation: () => void;
}

export function ChatHeader({
  title = "AI Assistant",
  onNewConversation,
}: ChatHeaderProps) {
  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-full bg-white/20 flex items-center justify-center">
          <Bot className="h-6 w-6 text-white" />
        </div>
        <div>
          <h3 className="font-semibold text-white">{title}</h3>
          <p className="text-xs text-white/80">Powered by Gemini AI</p>
        </div>
      </div>
      <Button
        variant="ghost"
        size="sm"
        onClick={onNewConversation}
        className="text-white hover:bg-white/20"
      >
        <Plus className="h-5 w-5 mr-1" />
        New Chat
      </Button>
    </div>
  );
}
