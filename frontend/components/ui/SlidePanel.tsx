'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { slidePanelVariants, backdropVariants } from '@/lib/animations/variants';
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';
import { useEffect } from 'react';

interface SlidePanelProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

/**
 * Slide-out panel component for task editing.
 * Slides in from the right with backdrop overlay.
 * Supports click-outside-to-close and respects reduced motion.
 */
export function SlidePanel({ isOpen, onClose, title, children }: SlidePanelProps) {
  const reducedMotion = useReducedMotion();

  const panelVariants = reducedMotion
    ? { hidden: { x: 0, opacity: 1 }, visible: { x: 0, opacity: 1 }, exit: { x: 0, opacity: 1 } }
    : slidePanelVariants;

  const backdropVars = reducedMotion
    ? { hidden: { opacity: 0.5 }, visible: { opacity: 0.5 }, exit: { opacity: 0 } }
    : backdropVariants;

  // Prevent body scroll when panel is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50 z-40"
            variants={backdropVars}
            initial="hidden"
            animate="visible"
            exit="exit"
            onClick={onClose}
          />

          {/* Panel */}
          <motion.div
            className="fixed right-0 top-0 h-full w-full max-w-md bg-white dark:bg-gray-900 shadow-2xl z-50 overflow-y-auto"
            variants={panelVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
          >
            {/* Header */}
            <div className="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 p-6 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">{title}</h2>
              <button
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Close panel"
              >
                <X size={20} />
              </button>
            </div>

            {/* Content */}
            <div className="p-6">{children}</div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
