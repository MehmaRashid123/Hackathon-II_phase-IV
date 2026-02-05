# Data Model: UI Enhancement & Advanced Animations

**Feature**: 004-ui-enhancement
**Date**: 2026-02-05
**Note**: This feature is UI-only and does not introduce new database entities. This document describes component-level state management and animation state.

## Database Entities

**No new database entities** - This feature enhances the UI for existing entities:
- `User` (from spec 001 - unchanged)
- `Task` (from spec 002 - unchanged)

---

## Component State Models

### 1. AnimationState (Client-Side)

**Purpose**: Track animation playback state to prevent interaction during critical animations

**State Shape**:
```typescript
interface AnimationState {
  isAnimating: boolean;           // Prevents clicks during page transitions
  staggerIndex: number;            // Current item index in stagger sequence
  animationQueue: string[];        // Queue of pending animations
}
```

**State Transitions**:
- `idle` → `animating` (when animation starts)
- `animating` → `idle` (when animation completes)
- `animating` → `queued` (when new animation requested during current animation)

**Managed By**: Framer Motion's internal state + custom `useAnimation` hook

---

### 2. ThemeState (Client-Side)

**Purpose**: Manage dark/light mode preference (initially system-detected, can be extended for manual toggle)

**State Shape**:
```typescript
interface ThemeState {
  mode: 'light' | 'dark' | 'system'; // Current theme mode
  systemPreference: 'light' | 'dark'; // OS-level preference
}
```

**State Persistence**: N/A initially (follows system `prefers-color-scheme`)
**Future Extension**: Can be persisted to localStorage for manual override

**Managed By**: `useTheme` hook with `matchMedia` listener

---

### 3. MotionPreference (Client-Side)

**Purpose**: Detect and respect user's motion preference for accessibility

**State Shape**:
```typescript
interface MotionPreference {
  reducedMotion: boolean; // True if user prefers reduced motion
}
```

**State Source**: CSS media query `(prefers-reduced-motion: reduce)`

**Managed By**: `useReducedMotion` hook with `matchMedia` listener

---

### 4. ProgressBarState (Client-Side)

**Purpose**: Calculate and animate task completion percentage

**State Shape**:
```typescript
interface ProgressBarState {
  percentage: number;              // 0-100 completion percentage
  completedCount: number;          // Number of completed tasks
  totalCount: number;              // Total number of tasks
  isAnimating: boolean;            // True during fill animation
}
```

**Calculation Logic**:
```typescript
const percentage = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
```

**Debounce**: 100ms debounce on updates to prevent jank from rapid toggles

**Managed By**: Derived state in Dashboard component, animated by Framer Motion

---

### 5. SlidePanelState (Client-Side)

**Purpose**: Manage slide-out edit panel visibility and animation state

**State Shape**:
```typescript
interface SlidePanelState {
  isOpen: boolean;                 // Panel visibility
  editingTaskId: string | null;    // Task being edited (null for create)
  animationDirection: 'in' | 'out'; // Slide direction
}
```

**State Transitions**:
- `closed` → `opening` (user clicks edit)
- `opening` → `open` (animation completes)
- `open` → `closing` (user clicks close/outside)
- `closing` → `closed` (animation completes)

**Managed By**: `TaskForm` component state with AnimatePresence

---

## Animation Variants Library

**Purpose**: Reusable animation configurations for consistency

### Page Entrance Animations

```typescript
export const pageVariants = {
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

### Stagger List Animations

```typescript
export const staggerContainerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05, // 50ms delay between items
      delayChildren: 0.1,    // Wait 100ms before starting
    },
  },
};

export const staggerItemVariants = {
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

### Hover Animations

```typescript
export const hoverVariants = {
  initial: { scale: 1, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
  hover: {
    scale: 1.02,
    boxShadow: '0 10px 20px rgba(0,0,0,0.15)',
    transition: {
      duration: 0.2,
      ease: 'easeOut',
    },
  },
};
```

### Spring Physics Animations (Checkbox)

```typescript
export const springVariants = {
  unchecked: { scale: 1, rotate: 0 },
  checked: {
    scale: [1, 1.2, 1],
    rotate: [0, 10, 0],
    transition: {
      type: 'spring',
      stiffness: 120,
      damping: 15,
    },
  },
};
```

### Slide Panel Animations

```typescript
export const slidePanelVariants = {
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

export const backdropVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
  exit: { opacity: 0 },
};
```

### Progress Bar Animations

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
  complete: {
    width: '100%',
    transition: {
      duration: 0.5,
      ease: 'easeOut',
    },
  },
};
```

---

## Component Relationships

```
App Layout (AnimatePresence wrapper)
│
├── PageTransition (page entrance animations)
│   │
│   ├── Landing Page
│   │   └── AnimatedButton (hover effects)
│   │
│   ├── Login Page
│   │   └── AnimatedCard (glassmorphism)
│   │       └── AnimatedButton
│   │
│   ├── Signup Page
│   │   └── AnimatedCard
│   │       └── AnimatedButton
│   │
│   └── Dashboard Page
│       ├── AnimatedProgress (progress bar)
│       ├── ThemeProvider (dark/light context)
│       ├── TaskList (stagger container)
│       │   └── TaskItem (stagger child + hover + exit)
│       │       ├── Checkbox (spring animation)
│       │       ├── Edit Button (hover)
│       │       └── Delete Button (hover)
│       │
│       └── SlidePanel (edit form)
│           ├── TaskForm
│           └── Backdrop (click outside to close)
```

---

## State Persistence

**No server-side persistence required** - All animation and theme state is client-side only:

| State | Persistence Method | Rationale |
|-------|-------------------|-----------|
| Animation state | In-memory (component state) | Transient - resets on page load |
| Theme mode | System preference (no storage) | Follows OS setting automatically |
| Reduced motion | System preference (no storage) | Accessibility setting from OS |
| Progress bar | Calculated from tasks array | Derived state, no storage needed |
| Slide panel | In-memory (component state) | Transient - closes on navigation |

**Future Extension**: Theme mode could be persisted to localStorage for manual override

---

## Validation Rules

**No server-side validation changes** - Existing task validation rules remain unchanged:
- Title: 1-500 characters (unchanged)
- Description: 0-5000 characters (unchanged)
- is_completed: boolean (unchanged)

**New Client-Side Validation**:
- Animation duration: Must be >= 0 (accessibility - zero for reduced motion)
- Stagger delay: Capped at 50ms to prevent slow rendering of large lists
- Progress percentage: Clamped to 0-100 range

---

## Performance Considerations

**Animation State Updates**:
- Debounce progress bar updates (100ms) to prevent excessive re-renders
- Use `React.memo()` on TaskItem to prevent unnecessary re-animations
- Limit stagger animations to first 20 items (cap for performance)

**GPU Acceleration**:
- All animations use `transform` and `opacity` (GPU-accelerated)
- Avoid `width`, `height`, `margin`, `padding` in animations (causes layout thrashing)

**Memory Management**:
- Clean up `matchMedia` listeners on component unmount
- No persistent animation state (garbage collected on unmount)

---

## Next Steps

1. ✅ **Phase 1 Data Model Complete**: Component state documented
2. **Next**: Create `contracts/` directory with animation API contracts
3. **Next**: Create `quickstart.md` with setup instructions
