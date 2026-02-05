'use client';

import { motion } from 'framer-motion';
import { pageVariants } from '@/lib/animations/variants';
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';

interface PageTransitionProps {
  children: React.ReactNode;
  className?: string;
}

/**
 * Wrapper component that adds page entrance/exit animations.
 * Automatically disables animations when prefers-reduced-motion is enabled.
 */
export function PageTransition({ children, className = '' }: PageTransitionProps) {
  const reducedMotion = useReducedMotion();

  const variants = reducedMotion
    ? {
        initial: { opacity: 1, y: 0 },
        animate: { opacity: 1, y: 0, transition: { duration: 0 } },
        exit: { opacity: 1, y: 0, transition: { duration: 0 } },
      }
    : pageVariants;

  return (
    <motion.div
      className={className}
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {children}
    </motion.div>
  );
}
