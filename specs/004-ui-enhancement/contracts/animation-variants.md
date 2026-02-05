# Animation Variants Contract

**File**: `frontend/lib/animations/variants.ts`
**Purpose**: Centralized animation configurations for consistent transitions across components

## Exported Variants

### 1. Page Transition Variants

```typescript
export const pageVariants: Variants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.2,
    },
  },
};
```

**Usage**:
```tsx
<motion.div variants={pageVariants} initial="initial" animate="animate" exit="exit">
  {children}
</motion.div>
```

---

### 2. Stagger List Variants

```typescript
export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05, // 50ms between items
      delayChildren: 0.1,
    },
  },
};

export const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    x: 100,
    transition: {
      duration: 0.2,
    },
  },
};
```

**Usage**:
```tsx
<motion.ul variants={staggerContainerVariants} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={staggerItemVariants} exit="exit">
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

---

### 3. Hover Interaction Variants

```typescript
export const hoverVariants: Variants = {
  initial: { scale: 1 },
  hover: {
    scale: 1.02,
    transition: {
      duration: 0.2,
      ease: 'easeOut',
    },
  },
};

export const hoverShadowVariants: Variants = {
  initial: { boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
  hover: {
    boxShadow: '0 10px 20px rgba(0,0,0,0.15)',
    transition: {
      duration: 0.2,
    },
  },
};
```

**Usage**:
```tsx
<motion.div
  variants={hoverVariants}
  initial="initial"
  whileHover="hover"
>
  {children}
</motion.div>
```

---

### 4. Spring Physics Variants (Checkbox)

```typescript
export const checkboxVariants: Variants = {
  unchecked: { scale: 1, rotate: 0 },
  checked: {
    scale: [1, 1.2, 1], // Overshoot and settle
    rotate: [0, 10, 0],
    transition: {
      type: 'spring',
      stiffness: 120,
      damping: 15,
    },
  },
};
```

**Usage**:
```tsx
<motion.div
  variants={checkboxVariants}
  animate={isChecked ? 'checked' : 'unchecked'}
>
  <CheckIcon />
</motion.div>
```

---

### 5. Slide Panel Variants

```typescript
export const slidePanelVariants: Variants = {
  hidden: { x: '100%', opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 30,
    },
  },
  exit: {
    x: '100%',
    opacity: 0,
    transition: {
      duration: 0.3,
      ease: 'easeIn',
    },
  },
};

export const backdropVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.2 },
  },
  exit: {
    opacity: 0,
    transition: { duration: 0.2 },
  },
};
```

**Usage**:
```tsx
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        variants={backdropVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
        onClick={onClose}
      />
      <motion.div
        variants={slidePanelVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
      >
        {panelContent}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

---

### 6. Progress Bar Variants

```typescript
export const progressBarVariants = {
  initial: { width: '0%' },
  animate: (percentage: number) => ({
    width: `${percentage}%`,
    transition: {
      duration: 0.5,
      ease: 'easeOut',
    },
  }),
};
```

**Usage**:
```tsx
<motion.div
  variants={progressBarVariants}
  initial="initial"
  animate="animate"
  custom={percentage} // Pass percentage as custom prop
/>
```

---

### 7. Button Press Variants

```typescript
export const buttonVariants: Variants = {
  initial: { scale: 1 },
  tap: { scale: 0.95 },
  hover: { scale: 1.05 },
};
```

**Usage**:
```tsx
<motion.button
  variants={buttonVariants}
  whileHover="hover"
  whileTap="tap"
>
  Click me
</motion.button>
```

---

## Type Definitions

```typescript
import { Variants } from 'framer-motion';

export interface AnimationConfig {
  variants: Variants;
  initial?: string;
  animate?: string;
  exit?: string;
  whileHover?: string;
  whileTap?: string;
}
```

---

## Accessibility Integration

All variants should be conditionally disabled when `prefers-reduced-motion` is detected:

```typescript
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';

export function getVariants(baseVariants: Variants, reducedMotion: boolean): Variants {
  if (reducedMotion) {
    // Return instant transitions
    return Object.keys(baseVariants).reduce((acc, key) => {
      acc[key] = {
        ...baseVariants[key],
        transition: { duration: 0 },
      };
      return acc;
    }, {} as Variants);
  }
  return baseVariants;
}
```

---

## Performance Notes

- All variants use GPU-accelerated properties (`transform`, `opacity`)
- Avoid `width`, `height`, `margin`, `padding` in animations (causes layout recalculation)
- Use `will-change` sparingly (only on hover/focus states)
- Stagger delays capped at 50ms to prevent slow rendering
