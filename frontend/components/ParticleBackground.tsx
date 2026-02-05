'use client';

import React, { useEffect, useState } from 'react';

// A simple CSS-based particle effect for demonstration
const ParticleBackground: React.FC = () => {
  const [particleCount, setParticleCount] = useState(150);

  useEffect(() => {
    const handleResize = () => {
      setParticleCount(window.innerWidth < 768 ? 50 : 150);
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Check for reduced motion preference
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);
    const listener = (event: MediaQueryListEvent) => setPrefersReducedMotion(event.matches);
    mediaQuery.addEventListener('change', listener);
    return () => mediaQuery.removeEventListener('change', listener);
  }, []);

  if (prefersReducedMotion) {
    return null; // Do not render particles if reduced motion is preferred
  }

  const particles = Array.from({ length: particleCount }).map((_, i) => (
    <div
      key={i}
      className="particle absolute bg-white rounded-full opacity-0"
      style={{
        left: `${Math.random() * 100}vw`,
        top: `${Math.random() * 100}vh`,
        width: `${Math.random() * 5 + 1}px`,
        height: `${Math.random() * 5 + 1}px`,
        animationDelay: `${Math.random() * 10}s`,
        animationDuration: `${Math.random() * 30 + 10}s`,
        animationName: 'moveParticles',
      }}
    />
  ));

  return (
    <div className="absolute inset-0 overflow-hidden -z-10">
      <style jsx global>{`
        @keyframes moveParticles {
          0% {
            transform: translateY(0) translateX(0) scale(1);
            opacity: 0;
          }
          20% {
            opacity: 1;
          }
          80% {
            opacity: 1;
          }
          100% {
            transform: translateY(-100vh) translateX(50vw) scale(0.5);
            opacity: 0;
          }
        }
        .particle {
          animation-iteration-count: infinite;
          animation-timing-function: linear;
        }
      `}</style>
      {particles}
    </div>
  );
};

export default ParticleBackground;