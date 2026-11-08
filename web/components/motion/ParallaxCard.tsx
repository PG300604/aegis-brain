"use client";

import React, { useRef, useState, useEffect } from "react";
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
  // and dim to create authentic 3D physical card deck depth
  const scale = useTransform(scrollYProgress, [0, 1], [1, 0.93]);
  const opacity = useTransform(scrollYProgress, [0, 0.85, 1], [1, 0.96, 0.82]);
  const y = useTransform(scrollYProgress, [0, 1], ["0px", "-12px"]);

  // Interactive 3D Mouse Movement Physics (Santioni Spirits Style)
  const rawMouseX = useMotionValue(0);
  const rawMouseY = useMotionValue(0);

  // Spring physics configuration for organic tactile damping
  const springConfig = { damping: 25, stiffness: 120, mass: 0.5 };
  const smoothMouseX = useSpring(rawMouseX, springConfig);
  const smoothMouseY = useSpring(rawMouseY, springConfig);

  // Derive 3D tilt angles from mouse coordinates
  const rotateX = useTransform(smoothMouseY, [-0.5, 0.5], [6, -6]);
  const rotateY = useTransform(smoothMouseX, [-0.5, 0.5], [-6, 6]);
  const shardX = useTransform(smoothMouseX, [-0.5, 0.5], [-24, 24]);
  const shardY = useTransform(smoothMouseY, [-0.5, 0.5], [-24, 24]);
  const reverseShardX = useTransform(smoothMouseX, [-0.5, 0.5], [30, -30]);
  const reverseShardY = useTransform(smoothMouseY, [-0.5, 0.5], [30, -30]);

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
  const topOffset = `${74 + index * 4}px`;

  return (
    <div
      id={id}
      ref={containerRef}
      className={`relative w-full min-h-[96vh] flex justify-center items-start pb-12 sm:pb-24 ${className}`}
      style={{ perspective: 1400 }}
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
        className="sticky w-full max-w-5xl px-3 sm:px-6 transition-transform ease-out"
      >
        {/* Floating 3D Graphic Novel Shards (Santioni Physics Debris) */}
        <motion.div
          style={{ x: shardX, y: shardY }}
          className="absolute -top-4 -left-3 pointer-events-none z-30 hidden md:block"
          aria-hidden="true"
        >
          <div className="w-4 h-9 bg-black/90 rotate-[24deg] border border-[#B91C1C] shadow-[3px_3px_0px_rgba(0,0,0,0.5)]" />
        </motion.div>

        <motion.div
          style={{ x: reverseShardX, y: reverseShardY }}
          className="absolute -bottom-6 -right-4 pointer-events-none z-30 hidden md:block"
          aria-hidden="true"
        >
          <div className="w-5 h-7 bg-[#B91C1C] rotate-[-18deg] border border-black shadow-[4px_4px_0px_rgba(0,0,0,0.6)]" />
        </motion.div>

        <motion.div
          style={{ x: reverseShardX, y: shardY }}
          className="absolute top-1/2 -right-6 pointer-events-none z-30 hidden lg:block"
          aria-hidden="true"
        >
          <div className="w-3 h-5 bg-[#D4AF37] rotate-[42deg] border border-black shadow-[2px_2px_0px_rgba(0,0,0,0.4)]" />
        </motion.div>

        {/* Physical 3D Card Shell with Depth Shadows */}
        <div className="w-full shadow-[0_-22px_60px_rgba(0,0,0,0.92)] rounded-2xl overflow-hidden border-2 border-black/85 bg-[#FAF8F5]">
          {children}
        </div>
      </motion.div>
    </div>
  );
}
