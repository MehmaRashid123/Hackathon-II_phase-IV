/**
 * MessageTimestamp Component
 * Displays formatted timestamp for messages
 */

import { formatDistanceToNow } from "date-fns";

interface MessageTimestampProps {
  timestamp: Date;
}

export function MessageTimestamp({ timestamp }: MessageTimestampProps) {
  const timeAgo = formatDistanceToNow(timestamp, { addSuffix: true });
  const fullTime = timestamp.toLocaleString();

  return (
    <p
      className="text-xs text-gray-500 dark:text-gray-400"
      title={fullTime}
    >
      {timeAgo}
    </p>
  );
}
