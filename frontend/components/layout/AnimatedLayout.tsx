'use client';

import { AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';

export function AnimatedLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <div key={pathname}>{children}</div>
    </AnimatePresence>
  );
}
