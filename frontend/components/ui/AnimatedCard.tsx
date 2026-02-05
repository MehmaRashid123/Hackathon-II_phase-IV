'use client';

import { motion } from 'framer-motion';
import { hoverVariants } from '@/lib/animations/variants';
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';

interface AnimatedCardProps {
  children: React.ReactNode;
  className?: string;
  enableHover?: boolean;
}

/**
 * Glassmorphism card component with optional hover animations.
 * Automatically adapts to light/dark mode and respects reduced motion preferences.
 */
export function AnimatedCard({
  children,
  className = '',
  enableHover = true
}: AnimatedCardProps) {
  const reducedMotion = useReducedMotion();

  const variants = reducedMotion || !enableHover
    ? { initial: {}, hover: {} }
    : hoverVariants;

  return (
    <motion.div
      className={`glass-card ${className}`}
      variants={variants}
      initial="initial"
      whileHover="hover"
    >
      {children}
    </motion.div>
  );
}
