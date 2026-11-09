"use client";

import React, { useRef } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import { useCursorPhysics } from "./CursorPhysicsProvider";

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

  // Consume smooth spring cursor physics for 3D card tilt & parallax
  const { tiltX, tiltY } = useCursorPhysics();

  // Scroll tracking on container with offset: ['start start', 'end start']
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  });

  // Sticky card deck stacking physics:
  // As next card scrolls up and stacks on top:
  // - smoothly scales down (1 -> 0.93)
  // - decreases opacity slightly (1 -> 0.75)
  // - adds subtle depth blur (0px -> 1.5px)
  // - recesses in 3D space (z: 0px -> -40px)
  // - lifts slightly on y axis (0px -> -18px)
  const scale = useTransform(scrollYProgress, [0, 1], [1, 0.93]);
  const opacity = useTransform(scrollYProgress, [0, 0.8, 1], [1, 0.95, 0.75]);
  const z = useTransform(scrollYProgress, [0, 1], [0, -40]);
  const filter = useTransform(scrollYProgress, [0, 1], ["blur(0px)", "blur(1.5px)"]);
  const y = useTransform(scrollYProgress, [0, 1], ["0px", "-18px"]);

  // Card top sticky offset: creates subtle cascading top margin
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
        style={{
          scale,
          opacity,
          y,
          z,
          filter,
          rotateX: tiltX,
          rotateY: tiltY,
          transformOrigin: "top center",
          transformStyle: "preserve-3d",
          top: topOffset,
          zIndex: 10 + index,
        }}
        className="sticky w-full max-w-[1360px] px-3 sm:px-6 transition-transform ease-out will-change-transform"
      >
        {/* Physical 3D Card Shell with Deep Luxury Lift Shadow */}
        <div
          style={{
            boxShadow:
              "0 -25px 60px rgba(0,0,0,0.85), 0 35px 80px rgba(0,0,0,0.8)",
          }}
          className="w-full rounded-2xl overflow-hidden border-2 border-black/85 bg-[#FAF8F5] transition-shadow duration-300"
        >
          {children}
        </div>
      </motion.div>
    </div>
  );
}
