/**
 * TypingIndicator Component
 * Animated typing indicator for AI responses
 */

import { Bot } from "lucide-react";
import { motion } from "framer-motion";

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      className="flex gap-3"
    >
      <div className="h-8 w-8 rounded-full bg-purple-600 flex items-center justify-center flex-shrink-0">
        <Bot className="h-4 w-4 text-white" />
      </div>
      <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-2xl">
        <div className="flex gap-1">
          <motion.div
            className="h-2 w-2 bg-gray-600 dark:bg-gray-400 rounded-full"
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
          />
          <motion.div
            className="h-2 w-2 bg-gray-600 dark:bg-gray-400 rounded-full"
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
          />
          <motion.div
            className="h-2 w-2 bg-gray-600 dark:bg-gray-400 rounded-full"
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
          />
        </div>
      </div>
    </motion.div>
  );
}
