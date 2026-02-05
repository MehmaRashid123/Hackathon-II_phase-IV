'use client';

import { motion } from 'framer-motion';
import { buttonVariants } from '@/lib/animations/variants';
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';

interface AnimatedButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  className?: string;
  variant?: 'glass' | 'primary' | 'secondary' | 'danger';
}

/**
 * Animated button with glassmorphism effect and hover/tap animations.
 * Supports multiple variants and respects reduced motion preferences.
 */
export function AnimatedButton({
  children,
  onClick,
  type = 'button',
  disabled = false,
  className = '',
  variant = 'glass',
}: AnimatedButtonProps) {
  const reducedMotion = useReducedMotion();

  const variants = reducedMotion
    ? { initial: {}, tap: {}, hover: {} }
    : buttonVariants;

  const variantClasses = {
    glass: 'glass-button',
    primary: 'bg-blue-600 text-white hover:bg-blue-700 border-none px-4 py-2 rounded-lg',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 border-none px-4 py-2 rounded-lg',
    danger: 'bg-red-600 text-white hover:bg-red-700 border-none px-4 py-2 rounded-lg',
  };

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${variantClasses[variant]} ${className} transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed`}
      variants={variants}
      initial="initial"
      whileHover={disabled ? undefined : "hover"}
      whileTap={disabled ? undefined : "tap"}
    >
      {children}
    </motion.button>
  );
}
