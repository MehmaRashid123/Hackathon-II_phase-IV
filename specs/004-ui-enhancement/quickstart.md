# Quickstart Guide: UI Enhancement & Advanced Animations

**Feature**: 004-ui-enhancement
**Date**: 2026-02-05
**Estimated Setup Time**: 15 minutes

## Prerequisites

- ✅ Specs 001-003 implemented and functional (auth, task API, current dashboard)
- ✅ Node.js 18+ installed
- ✅ Next.js 16.1.6 frontend running
- ✅ Tailwind CSS 3.4.1 configured
- ✅ TypeScript 5+ configured

---

## Step 1: Install Dependencies (5 minutes)

Navigate to frontend directory and install animation libraries:

```bash
cd frontend

# Install Framer Motion (animation library)
npm install framer-motion@^11.0.0

# Install Lucide React (icon library)
npm install lucide-react@^0.300.0

# Verify installation
npm list framer-motion lucide-react
```

**Expected Output**:
```
frontend@0.1.0 /path/to/frontend
├── framer-motion@11.x.x
└── lucide-react@0.x.x
```

**Bundle Size Impact**:
- Framer Motion: ~32KB gzipped
- Lucide React: ~15KB gzipped (tree-shakeable - only imported icons included)
- **Total**: ~47KB gzipped (within 50KB budget ✅)

---

## Step 2: Configure Tailwind for Glassmorphism (3 minutes)

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'media', // Enable system dark mode detection
  theme: {
    extend: {
      backdropBlur: {
        xs: '2px', // Extra small blur for subtle effects
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

## Step 3: Add Glassmorphism Utilities to Global CSS (2 minutes)

Update `app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Glassmorphism utility classes */
@layer components {
  .glass-card {
    @apply bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl shadow-xl;
  }

  .dark .glass-card {
    @apply bg-black/20 border-white/10;
  }

  .glass-card-hover {
    @apply glass-card transition-all duration-300;
  }

  .glass-card-hover:hover {
    @apply bg-white/20 backdrop-blur-xl shadow-2xl;
  }

  .dark .glass-card-hover:hover {
    @apply bg-black/30;
  }

  .glass-button {
    @apply bg-white/20 backdrop-blur-md border border-white/30 rounded-lg px-4 py-2;
    @apply hover:bg-white/30 hover:border-white/40 transition-all duration-200;
  }

  .dark .glass-button {
    @apply bg-black/30 border-white/20;
    @apply hover:bg-black/40 hover:border-white/30;
  }
}

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

## Step 4: Create Animation Utilities Directory (2 minutes)

Create the animation utilities structure:

```bash
mkdir -p frontend/lib/animations
mkdir -p frontend/lib/hooks
mkdir -p frontend/components/ui
```

---

## Step 5: Create Core Animation Variants (2 minutes)

Create `frontend/lib/animations/variants.ts`:

```typescript
import { Variants } from 'framer-motion';

export const pageVariants: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: 'easeOut' },
  },
  exit: { opacity: 0, y: -20, transition: { duration: 0.2 } },
};

export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1,
    },
  },
};

export const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: 'easeOut' },
  },
  exit: {
    opacity: 0,
    x: 100,
    transition: { duration: 0.2 },
  },
};

export const hoverVariants: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.02, transition: { duration: 0.2, ease: 'easeOut' } },
};
```

---

## Step 6: Create useReducedMotion Hook (1 minute)

Create `frontend/lib/hooks/useReducedMotion.ts`:

```typescript
'use client';

import { useEffect, useState } from 'react';

export function useReducedMotion(): boolean {
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
```

---

## Step 7: Verify Installation (1 minute)

Run the development server and check for errors:

```bash
npm run dev
```

**Expected Output**:
```
▲ Next.js 16.1.6
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 2.5s
```

**Verification Steps**:
1. Visit http://localhost:3000
2. Open browser DevTools Console
3. Should see no errors related to framer-motion or lucide-react
4. Check Network tab - bundle size should increase by ~50KB

---

## Quick Test: Animated Card Component

Create a test component to verify setup:

```tsx
// components/ui/TestAnimatedCard.tsx
'use client';

import { motion } from 'framer-motion';
import { CheckCircle } from 'lucide-react';

export function TestAnimatedCard() {
  return (
    <motion.div
      className="glass-card p-6 max-w-sm"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.05 }}
    >
      <div className="flex items-center gap-3">
        <CheckCircle className="text-green-500" size={24} />
        <p className="text-white">
          Setup successful! Framer Motion + Lucide React + Glassmorphism working.
        </p>
      </div>
    </motion.div>
  );
}
```

Add to landing page to test:

```tsx
// app/page.tsx
import { TestAnimatedCard } from '@/components/ui/TestAnimatedCard';

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-500 to-blue-500">
      <TestAnimatedCard />
    </main>
  );
}
```

**Expected Result**: Card fades in with slide-up animation, scales on hover, shows check icon

---

## Troubleshooting

### Issue: "Module not found: Can't resolve 'framer-motion'"

**Solution**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

### Issue: Glassmorphism not rendering (backdrop-blur invisible)

**Cause**: Browser doesn't support backdrop-filter
**Solution**: Check browser version (Chrome 76+, Firefox 103+, Safari 9+)

**Check Support**:
```javascript
// In browser console
CSS.supports('backdrop-filter', 'blur(10px)')
// Should return true
```

---

### Issue: Animations not working

**Possible Causes**:
1. Missing `'use client'` directive in component
2. AnimatePresence not wrapping exit animations
3. prefers-reduced-motion enabled (animations disabled for accessibility)

**Debug**:
```tsx
import { useReducedMotion } from '@/lib/hooks/useReducedMotion';

export function DebugComponent() {
  const reducedMotion = useReducedMotion();
  console.log('Reduced motion:', reducedMotion); // Should be false for animations to work
  return null;
}
```

---

### Issue: TypeScript errors with Framer Motion

**Solution**: Ensure proper types are installed:
```bash
npm install --save-dev @types/react @types/react-dom
```

---

## Next Steps

After setup is complete:

1. ✅ Run `/sp.tasks` to generate implementation tasks
2. ✅ Implement tasks using `nextjs-ui-builder` agent
3. ✅ Test animations in development environment
4. ✅ Verify accessibility (prefers-reduced-motion)
5. ✅ Measure performance (60fps, layout shift)

---

## Reference Links

- **Framer Motion Docs**: https://www.framer.com/motion/
- **Lucide React Icons**: https://lucide.dev/
- **Tailwind Dark Mode**: https://tailwindcss.com/docs/dark-mode
- **Backdrop Filter Support**: https://caniuse.com/css-backdrop-filter

---

## Success Checklist

- [ ] Framer Motion 11+ installed
- [ ] Lucide React 0.300+ installed
- [ ] Tailwind configured with glassmorphism utilities
- [ ] Global CSS updated with glass-card classes
- [ ] Animation variants created in lib/animations/variants.ts
- [ ] useReducedMotion hook created
- [ ] Dev server runs without errors
- [ ] Test animated card renders and animates
- [ ] Browser supports backdrop-filter (95%+ coverage)
- [ ] Bundle size increase < 50KB gzipped

**Estimated Total Time**: 15 minutes ✅
