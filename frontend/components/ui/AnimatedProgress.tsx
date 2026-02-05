'use client';

import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { progressBarVariants } from '@/lib/animations/variants';
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';

interface AnimatedProgressProps {
  percentage: number;
  total: number;
  completed: number;
}

/**
 * Animated progress bar showing task completion percentage.
 * Shows celebratory pulse animation at 100% completion.
 */
export function AnimatedProgress({ percentage, total, completed }: AnimatedProgressProps) {
  const reducedMotion = useReducedMotion();
  const isComplete = percentage === 100;

  const barVariants = reducedMotion
    ? { initial: { width: `${percentage}%` }, animate: { width: `${percentage}%` } }
    : progressBarVariants;

  return (
    <div className="space-y-2">
      {/* Header with stats */}
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-2">
          <TrendingUp className={`h-4 w-4 ${isComplete ? 'text-green-600' : 'text-blue-600'}`} />
          <span className="font-medium text-gray-700 dark:text-gray-300">
            Progress
          </span>
        </div>
        <span className="text-gray-600 dark:text-gray-400">
          {completed}/{total} tasks ({Math.round(percentage)}%)
        </span>
      </div>

      {/* Progress bar container */}
      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          className={`h-full ${
            isComplete
              ? 'bg-green-600'
              : 'bg-gradient-to-r from-blue-500 to-blue-600'
          } rounded-full`}
          custom={percentage}
          variants={barVariants}
          initial="initial"
          animate={isComplete && !reducedMotion ? "complete" : "animate"}
          whileInView={
            isComplete && !reducedMotion
              ? {
                  scale: [1, 1.05, 1],
                  transition: { duration: 0.6, ease: 'easeInOut' },
                }
              : undefined
          }
        />
      </div>

      {/* Celebratory message at 100% */}
      {isComplete && (
        <motion.p
          className="text-sm font-medium text-green-600 dark:text-green-400 text-center"
          initial={reducedMotion ? { opacity: 1 } : { opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          🎉 All tasks completed!
        </motion.p>
      )}
    </div>
  );
}
