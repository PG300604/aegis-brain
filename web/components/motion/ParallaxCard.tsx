"use client";

import React, { useRef } from "react";
import { motion, useScroll, useTransform, useSpring, useMotionValue } from "motion/react";

interface ParallaxCardProps {
  children: React.ReactNode;
  index: number;
  total?: number;
  className?: string;
  id?: string;
}

export function ParallaxCard({
  children,
  index,
  total = 8,
  className = "",
  id,
}: ParallaxCardProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);

  // Framer Motion Scroll Tracking
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  });

  // Framer Card Stack Parallax:
  // As the next card approaches and covers this card, scale down slightly
  // and dim to create authentic physical card deck depth
  const scale = useTransform(scrollYProgress, [0, 1], [1, 0.94]);
  const opacity = useTransform(scrollYProgress, [0, 0.85, 1], [1, 0.97, 0.82]);
  const y = useTransform(scrollYProgress, [0, 1], ["0px", "-16px"]);

  // Interactive 3D Mouse Movement Physics (Santioni Spirits Style)
  const rawMouseX = useMotionValue(0);
  const rawMouseY = useMotionValue(0);

  // Spring physics configuration for organic tactile damping
  const springConfig = { damping: 30, stiffness: 140, mass: 0.6 };
  const smoothMouseX = useSpring(rawMouseX, springConfig);
  const smoothMouseY = useSpring(rawMouseY, springConfig);

  // Derive 3D tilt angles from mouse coordinates
  const rotateX = useTransform(smoothMouseY, [-0.5, 0.5], [4.5, -4.5]);
  const rotateY = useTransform(smoothMouseX, [-0.5, 0.5], [-4.5, 4.5]);

  // Dynamic 3D Lift Shadow offsets: shadow shifts opposite to tilt
  const shadowX = useTransform(smoothMouseX, [-0.5, 0.5], [18, -18]);
  const shadowY = useTransform(smoothMouseY, [-0.5, 0.5], [25, 5]);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    rawMouseX.set(x);
    rawMouseY.set(y);
  };

  const handleMouseLeave = () => {
    rawMouseX.set(0);
    rawMouseY.set(0);
  };

  // Card top offset: all cards stack near the top below the header
  const topOffset = `${72 + index * 4}px`;

  return (
    <div
      id={id}
      ref={containerRef}
      className={`relative w-full min-h-[96vh] flex justify-center items-start pb-16 sm:pb-28 ${className}`}
      style={{ perspective: 1600 }}
    >
      <motion.div
        ref={cardRef}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        style={{
          scale,
          opacity,
          y,
          rotateX,
          rotateY,
          transformOrigin: "top center",
          transformStyle: "preserve-3d",
          top: topOffset,
          zIndex: 10 + index,
        }}
        className="sticky w-full max-w-[1360px] px-3 sm:px-6 transition-transform ease-out"
      >
        {/* Physical 3D Card Shell with Deep Lift Shadows & Graphic Border */}
        <motion.div
          style={{
            boxShadow: "0 -25px 60px rgba(0,0,0,0.92), 0 35px 80px rgba(0,0,0,0.8)",
          }}
          className="w-full rounded-2xl overflow-hidden border-2 border-black/85 bg-[#FAF8F5] transition-shadow duration-300"
        >
          {children}
        </motion.div>
      </motion.div>
    </div>
  );
}
