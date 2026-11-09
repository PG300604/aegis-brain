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
        {/* Physical 3D Card Shell with Deep Luxury Lift Shadow (Graphic Novel Editorial Plate) */}
        <div
          style={{
            boxShadow:
              "0 -35px 80px rgba(0,0,0,0.95), 0 35px 80px rgba(0,0,0,0.85)",
          }}
          className="w-full rounded-none overflow-hidden border-2 border-black bg-[#FAF8F5] transition-shadow duration-300"
        >
          {/* Sovereign Dossier Binder Top Tab - Eliminates raw white line & anchors card into dark background */}
          <div className="bg-[#0B0C10] border-b-2 border-black px-4 sm:px-6 py-2.5 flex items-center justify-between text-[11px] font-mono text-zinc-400 select-none">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-[#B91C1C] border border-black inline-block" />
              <span className="font-extrabold text-white tracking-widest uppercase">
                AEGIS // SPECIFICATION DOSSIER // DECK 0{index + 1}
              </span>
            </div>
            <div className="flex items-center gap-3 text-[10px] text-zinc-500 uppercase tracking-widest">
              <span className="hidden sm:inline">STATE: DETERMINISTIC</span>
              <span className="text-[#D4AF37] font-bold">SEC-LEVEL: SOVEREIGN</span>
            </div>
          </div>
          {children}
        </div>
      </motion.div>
    </div>
  );
}
