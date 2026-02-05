# Glassmorphism Theme Contract

**Purpose**: Define glassmorphism styling patterns for light and dark modes using Tailwind CSS

## Tailwind Configuration

Add to `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'media', // Use system preference
  theme: {
    extend: {
      backdropBlur: {
        xs: '2px',
      },
      backgroundColor: {
        'glass-light': 'rgba(255, 255, 255, 0.1)',
        'glass-dark': 'rgba(0, 0, 0, 0.2)',
      },
      borderColor: {
        'glass-light': 'rgba(255, 255, 255, 0.2)',
        'glass-dark': 'rgba(255, 255, 255, 0.1)',
      },
    },
  },
  variants: {
    extend: {
      backdropBlur: ['hover', 'focus'],
      backgroundColor: ['hover', 'dark'],
    },
  },
};
```

---

## CSS Utility Classes

Add to `globals.css`:

```css
/* Glassmorphism base card */
.glass-card {
  @apply bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl shadow-xl;
}

.dark .glass-card {
  @apply bg-black/20 border-white/10;
}

/* Glassmorphism with hover effect */
.glass-card-hover {
  @apply glass-card transition-all duration-300;
}

.glass-card-hover:hover {
  @apply bg-white/20 backdrop-blur-xl shadow-2xl;
}

.dark .glass-card-hover:hover {
  @apply bg-black/30;
}

/* Glassmorphism button */
.glass-button {
  @apply bg-white/20 backdrop-blur-md border border-white/30 rounded-lg px-4 py-2;
  @apply hover:bg-white/30 hover:border-white/40 transition-all duration-200;
}

.dark .glass-button {
  @apply bg-black/30 border-white/20;
  @apply hover:bg-black/40 hover:border-white/30;
}

/* Glassmorphism input */
.glass-input {
  @apply bg-white/10 backdrop-blur-md border border-white/30 rounded-lg;
  @apply focus:bg-white/15 focus:border-white/50 focus:ring-2 focus:ring-white/20;
  @apply placeholder-white/50;
}

.dark .glass-input {
  @apply bg-black/20 border-white/20;
  @apply focus:bg-black/25 focus:border-white/40;
  @apply placeholder-white/40;
}

/* Glassmorphism navbar/header */
.glass-header {
  @apply bg-white/5 backdrop-blur-xl border-b border-white/10;
}

.dark .glass-header {
  @apply bg-black/10 border-white/5;
}
```

---

## Component Patterns

### 1. Glass Card Component

```tsx
// components/ui/AnimatedCard.tsx
import { motion } from 'framer-motion';
import { hoverVariants } from '@/lib/animations/variants';

interface AnimatedCardProps {
  children: React.ReactNode;
  className?: string;
}

export function AnimatedCard({ children, className = '' }: AnimatedCardProps) {
  return (
    <motion.div
      className={`glass-card p-6 ${className}`}
      variants={hoverVariants}
      initial="initial"
      whileHover="hover"
    >
      {children}
    </motion.div>
  );
}
```

---

### 2. Glass Button Component

```tsx
// components/ui/AnimatedButton.tsx
import { motion } from 'framer-motion';
import { buttonVariants } from '@/lib/animations/variants';

interface AnimatedButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'ghost';
  className?: string;
}

export function AnimatedButton({
  children,
  onClick,
  variant = 'primary',
  className = '',
}: AnimatedButtonProps) {
  const baseClass = variant === 'ghost' ? 'glass-button' : 'bg-blue-500/80 backdrop-blur-md';

  return (
    <motion.button
      className={`${baseClass} ${className}`}
      onClick={onClick}
      variants={buttonVariants}
      whileHover="hover"
      whileTap="tap"
    >
      {children}
    </motion.button>
  );
}
```

---

### 3. Glass Progress Bar

```tsx
// components/ui/AnimatedProgress.tsx
import { motion } from 'framer-motion';
import { progressBarVariants } from '@/lib/animations/variants';

interface AnimatedProgressProps {
  percentage: number; // 0-100
  showLabel?: boolean;
}

export function AnimatedProgress({ percentage, showLabel = true }: AnimatedProgressProps) {
  return (
    <div className="relative w-full">
      {/* Background track */}
      <div className="h-2 bg-white/10 backdrop-blur-md rounded-full overflow-hidden dark:bg-black/20">
        {/* Animated fill */}
        <motion.div
          className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
          variants={progressBarVariants}
          initial="initial"
          animate="animate"
          custom={percentage}
        />
      </div>

      {/* Optional percentage label */}
      {showLabel && (
        <span className="text-sm text-white/70 mt-1 block dark:text-white/60">
          {Math.round(percentage)}% complete
        </span>
      )}
    </div>
  );
}
```

---

## Color Palette (Dark/Light)

### Light Mode Colors

```javascript
{
  background: {
    base: '#ffffff',
    glass: 'rgba(255, 255, 255, 0.1)',
    glassFocus: 'rgba(255, 255, 255, 0.2)',
  },
  border: {
    glass: 'rgba(255, 255, 255, 0.2)',
    glassFocus: 'rgba(255, 255, 255, 0.4)',
  },
  text: {
    primary: '#1a1a1a',
    secondary: '#4a4a4a',
    muted: 'rgba(0, 0, 0, 0.5)',
  },
  shadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
}
```

### Dark Mode Colors

```javascript
{
  background: {
    base: '#0a0a0a',
    glass: 'rgba(0, 0, 0, 0.2)',
    glassFocus: 'rgba(0, 0, 0, 0.3)',
  },
  border: {
    glass: 'rgba(255, 255, 255, 0.1)',
    glassFocus: 'rgba(255, 255, 255, 0.2)',
  },
  text: {
    primary: '#ffffff',
    secondary: '#b0b0b0',
    muted: 'rgba(255, 255, 255, 0.5)',
  },
  shadow: '0 10px 30px rgba(0, 0, 0, 0.5)',
}
```

---

## Gradient Definitions

```css
/* Accent gradients for progress bars, buttons */
.gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.gradient-success {
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
}

.gradient-glass {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
}

.dark .gradient-glass {
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.2) 0%,
    rgba(0, 0, 0, 0.1) 100%
  );
}
```

---

## Browser Compatibility

**Backdrop Filter Support**:
- Chrome 76+ ✅
- Safari 9+ (with `-webkit-` prefix) ✅
- Firefox 103+ ✅
- Edge 79+ ✅

**Fallback Strategy** (for older browsers):
```css
/* Fallback for browsers without backdrop-filter support */
@supports not (backdrop-filter: blur(10px)) {
  .glass-card {
    @apply bg-white/80;
  }

  .dark .glass-card {
    @apply bg-black/80;
  }
}
```

---

## Performance Considerations

**Backdrop Blur Cost**:
- GPU-accelerated on modern browsers
- Expensive on low-end devices - use sparingly
- Avoid animating blur values (static blur only)

**Optimization Tips**:
- Apply `will-change: backdrop-filter` only on hover, not persistently
- Limit number of glassmorphism elements on screen (< 10 cards)
- Use `backdrop-blur-lg` (12px) instead of `backdrop-blur-3xl` (64px) for better performance

**CSS Pattern**:
```css
.glass-card {
  backdrop-filter: blur(12px); /* Static blur */
  transition: background-color 0.3s, box-shadow 0.3s; /* Animate cheap properties only */
}

.glass-card:hover {
  will-change: backdrop-filter; /* Enable GPU optimization on hover only */
  backdrop-filter: blur(16px);
}
```

---

## Accessibility

**Contrast Requirements**:
- Ensure text on glass backgrounds meets WCAG AA contrast ratio (4.5:1 for normal text)
- Use `text-shadow` or semi-opaque backgrounds for better readability

**High Contrast Mode**:
```css
@media (prefers-contrast: high) {
  .glass-card {
    @apply bg-white border-2 border-black;
  }

  .dark .glass-card {
    @apply bg-black border-2 border-white;
  }
}
```

---

## Testing Checklist

- [ ] Light mode glassmorphism renders correctly
- [ ] Dark mode glassmorphism renders correctly
- [ ] Hover states increase blur and opacity
- [ ] Text is readable on glass backgrounds (contrast check)
- [ ] Fallback styles work without backdrop-filter support
- [ ] Performance is acceptable on mid-range devices (60fps)
- [ ] High contrast mode disables glass effects
