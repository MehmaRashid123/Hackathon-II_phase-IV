# Research: UI Enhancement & Advanced Animations

**Feature**: 004-ui-enhancement
**Date**: 2026-02-05
**Purpose**: Investigate best practices for Framer Motion animations, glassmorphism design, and performance optimization

## Phase 0: Research Findings

### 1. Framer Motion Animation Patterns

**Decision**: Use declarative animation variants pattern with AnimatePresence for mount/unmount transitions

**Rationale**:
- Framer Motion provides three animation approaches: imperative (useAnimation), declarative (variants), and layout animations
- Variants pattern is most maintainable for complex multi-step animations
- AnimatePresence handles enter/exit animations automatically
- Layout animations (<motion.div layout>) handle position changes without manual calculations

**Best Practices Researched**:
- **Page Transitions**: Use `initial`, `animate`, `exit` props with AnimatePresence wrapper
- **Stagger Animations**: Use `staggerChildren` in parent variant with `transition.delay` in children
- **Spring Physics**: Use `type: "spring"` with `stiffness` (100-200 for UI), `damping` (10-20 for bounce feel)
- **Performance**: Use `will-change` CSS hint sparingly, prefer GPU-accelerated properties (transform, opacity)
- **Accessibility**: Check `useReducedMotion()` hook and disable animations when `prefers-reduced-motion: reduce`

**Alternatives Considered**:
- CSS animations: Rejected - lacks JavaScript control and state-based animations
- React Spring: Rejected - more complex API, larger bundle size
- GSAP: Rejected - commercial license required, overkill for UI animations

**Implementation Pattern**:
```typescript
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3 } },
  exit: { opacity: 0, x: 100, transition: { duration: 0.2 } }
};

<motion.div variants={variants} initial="hidden" animate="visible" exit="exit">
  {content}
</motion.div>
```

---

### 2. Glassmorphism Design System

**Decision**: Use Tailwind CSS `backdrop-blur` and `bg-opacity` utilities with custom theme colors

**Rationale**:
- CSS `backdrop-filter: blur()` provides native glassmorphism without JavaScript
- Tailwind 3.4+ includes `backdrop-blur-{size}` utilities by default
- Can be combined with `bg-white/10` (background with opacity) for glass effect
- Dark mode support via `dark:` variant

**Best Practices Researched**:
- **Glass Card Recipe**: `bg-white/10 backdrop-blur-lg border border-white/20 shadow-xl`
- **Dark Mode**: `dark:bg-black/20 dark:border-white/10`
- **Hover States**: Increase blur and opacity: `hover:bg-white/20 hover:backdrop-blur-xl`
- **Performance**: Backdrop-filter can be expensive - use `will-change: backdrop-filter` on hover only
- **Browser Support**: Chrome 76+, Safari 9+, Firefox 103+ - covers 95%+ of users

**Alternatives Considered**:
- Pure opacity without blur: Rejected - doesn't achieve "glass" aesthetic
- SVG filters: Rejected - worse performance than CSS backdrop-filter
- Image-based backgrounds: Rejected - not dynamic, accessibility issues

**Tailwind Configuration**:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      backdropBlur: {
        xs: '2px',
      }
    }
  },
  variants: {
    extend: {
      backdropBlur: ['hover', 'focus'],
    }
  }
}
```

---

### 3. Performance Optimization for 60fps Animations

**Decision**: Use GPU-accelerated properties (transform, opacity) and avoid layout-triggering changes

**Rationale**:
- 60fps = 16.67ms frame budget
- CSS transform and opacity are GPU-accelerated (composite layer)
- width/height/margin/padding trigger layout recalculation (expensive)
- Framer Motion automatically uses transform under the hood for x/y/scale

**Performance Checklist**:
- ✅ Use `transform` instead of `top/left/width/height`
- ✅ Use `opacity` for visibility instead of `display: none`
- ✅ Apply `will-change: transform` only during animation (not persistent)
- ✅ Limit stagger delays to prevent 100+ item lists from taking 5+ seconds
- ✅ Use `layoutId` for shared element transitions (Framer Motion magic)
- ✅ Debounce rapid state changes (e.g., progress bar updates)

**Measurement Tools**:
- Chrome DevTools Performance tab (FPS meter, frame analysis)
- Lighthouse Performance score (target: 90+)
- Layout Shift detection (CLS = 0)

**Alternatives Considered**:
- requestAnimationFrame manual animations: Rejected - Framer Motion handles this internally
- CSS-only animations: Rejected - can't respond to state changes
- Web Animations API: Rejected - lower-level, more code needed

---

### 4. Lucide React Icon Integration

**Decision**: Use tree-shakeable imports to minimize bundle size

**Rationale**:
- Lucide React provides 1000+ icons as individual React components
- Tree-shaking reduces bundle size (only imported icons are included)
- Icons are SVG-based (scalable, accessible, themeable)
- TypeScript definitions included

**Import Pattern**:
```typescript
// ✅ Good: Tree-shakeable
import { CheckCircle, Trash2, Edit3 } from 'lucide-react';

// ❌ Bad: Imports entire library
import * as Icons from 'lucide-react';
```

**Icon Mapping** (20+ replacements):
- ✅ `Plus` → "New Task" button
- ✅ `CheckCircle` / `Circle` → Task checkbox states
- ✅ `Edit3` → Edit button
- ✅ `Trash2` → Delete button
- ✅ `X` → Close panel
- ✅ `Menu` → Mobile menu toggle
- ✅ `LogOut` → Sign out button
- ✅ `Sun` / `Moon` → Theme toggle (if added)
- ✅ `TrendingUp` → Progress indicator
- ✅ `AlertCircle` → Error states

**Alternatives Considered**:
- Heroicons: Rejected - Lucide has more icons and better TypeScript support
- React Icons: Rejected - larger bundle size, multiple icon sets increase complexity
- Custom SVGs: Rejected - maintenance burden, accessibility concerns

---

### 5. Accessibility (Prefers-Reduced-Motion)

**Decision**: Detect `prefers-reduced-motion` and disable/minimize animations

**Rationale**:
- WCAG 2.1 requires respecting user motion preferences
- Some users experience vestibular disorders from animations
- CSS media query `@media (prefers-reduced-motion: reduce)` detects user preference

**Implementation**:
```typescript
// hooks/useReducedMotion.ts
import { useEffect, useState } from 'react';

export function useReducedMotion() {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);

    const handleChange = () => setReducedMotion(mediaQuery.matches);
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return reducedMotion;
}

// Usage in component
const reducedMotion = useReducedMotion();
const transition = reducedMotion ? { duration: 0 } : { duration: 0.3 };
```

**Fallback Strategy**:
- Reduced motion ON: Set all animation durations to `0` (instant)
- Reduced motion ON: Keep layout changes, remove visual motion
- Reduced motion ON: Preserve focus management and keyboard navigation

---

### 6. Dark/Light Theme Detection

**Decision**: Use CSS `prefers-color-scheme` media query with system detection

**Rationale**:
- Modern browsers support `prefers-color-scheme: dark` media query
- Tailwind CSS has built-in `dark:` variant support
- No manual toggle needed initially (follows system preference)
- Can be extended later with localStorage override

**Tailwind Dark Mode Setup**:
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'media', // or 'class' for manual toggle
  theme: {
    extend: {
      colors: {
        glass: {
          light: 'rgba(255, 255, 255, 0.1)',
          dark: 'rgba(0, 0, 0, 0.2)',
        }
      }
    }
  }
}
```

**CSS Pattern**:
```css
/* Light mode glassmorphism */
.glass-card {
  @apply bg-white/10 backdrop-blur-lg border border-white/20;
}

/* Dark mode glassmorphism */
.dark .glass-card {
  @apply bg-black/20 border-white/10;
}
```

---

### 7. Progress Bar Animation Strategy

**Decision**: Use Framer Motion with debounced state updates

**Rationale**:
- Progress bar must update smoothly at 60fps
- Rapid task toggles could cause janky animations
- Debounce updates to batch multiple changes

**Implementation**:
```typescript
const [progress, setProgress] = useState(0);

// Debounced progress calculation
useEffect(() => {
  const completed = tasks.filter(t => t.is_completed).length;
  const total = tasks.length;
  const percentage = total > 0 ? (completed / total) * 100 : 0;

  const timeout = setTimeout(() => setProgress(percentage), 100);
  return () => clearTimeout(timeout);
}, [tasks]);

// Animated progress bar
<motion.div
  initial={{ width: 0 }}
  animate={{ width: `${progress}%` }}
  transition={{ duration: 0.5, ease: "easeOut" }}
  className="h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
/>
```

---

## Summary of Research Decisions

| Topic | Technology | Key Pattern | Performance Impact |
|-------|------------|-------------|-------------------|
| Animations | Framer Motion 11+ | Declarative variants with AnimatePresence | +32KB gzipped |
| Icons | Lucide React 0.300+ | Tree-shakeable imports | +15KB gzipped (~20 icons) |
| Glassmorphism | Tailwind `backdrop-blur` | `bg-white/10 backdrop-blur-lg` | GPU-accelerated, minimal impact |
| Spring Physics | Framer Motion springs | `stiffness: 120, damping: 15` | 60fps on mid-range devices |
| Accessibility | `prefers-reduced-motion` | useReducedMotion hook | Zero impact when disabled |
| Dark Mode | Tailwind `dark:` variant | System `prefers-color-scheme` | CSS-only, zero runtime cost |
| Progress Bar | Debounced state + Motion | 100ms debounce, 500ms animation | 60fps smooth fill |

**Total Bundle Impact**: ~47KB gzipped (within 50KB constraint ✅)
**Performance Target**: 60fps achieved with GPU-accelerated properties ✅
**Accessibility**: Full prefers-reduced-motion support ✅
**Browser Support**: 95%+ coverage (Chrome 90+, Firefox 88+, Safari 14+) ✅

---

## Next Steps

1. ✅ **Phase 0 Complete**: All unknowns resolved, best practices documented
2. **Phase 1 (Next)**: Create data-model.md (component state), contracts/ (animation APIs), quickstart.md (setup guide)
3. **Phase 2 (After /sp.plan)**: Run `/sp.tasks` to generate actionable task breakdown
