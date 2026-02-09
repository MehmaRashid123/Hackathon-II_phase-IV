/**
 * MessageList Component
 * Scrollable list of chat messages
 */

import { useEffect, useRef } from "react";
import { ChatMessage as ChatMessageType } from "@/lib/types/chat";
import { Message } from "./Message";
import { TypingIndicator } from "./TypingIndicator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { AnimatePresence } from "framer-motion";

interface MessageListProps {
  messages: ChatMessageType[];
  isLoading: boolean;
  onRetry?: (messageId: string) => void;
}

export function MessageList({ messages, isLoading, onRetry }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <ScrollArea className="flex-1 p-4" ref={scrollRef}>
      <div className="space-y-4">
        {messages.map((message) => (
          <Message key={message.id} message={message} onRetry={onRetry} />
        ))}
        
        <AnimatePresence>
          {isLoading && <TypingIndicator />}
        </AnimatePresence>
      </div>
    </ScrollArea>
  );
}
