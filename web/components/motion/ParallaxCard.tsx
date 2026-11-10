"use client";

import React, { useRef, useEffect } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import { useCursorPhysics } from "./CursorPhysicsProvider";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

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

  // Entrance scroll tracking (as card enters from bottom into sticky dock)
  const { scrollYProgress: entranceProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "start 0.25"],
  });

  // Sticky card deck stacking physics (as next card scrolls up and stacks on top)
  const { scrollYProgress: exitProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  });

  // Subtle, very light cinematic whoosh sound when card transitions into screen
  useEffect(() => {
    let triggered = false;
    const unsubscribe = entranceProgress.on("change", (v) => {
      if (v > 0.15 && v < 0.85 && !triggered) {
        triggered = true;
        triggerSoundEffect("whoosh");
      } else if (v < 0.05) {
        triggered = false;
      }
    });
    return () => unsubscribe();
  }, [entranceProgress]);

  // Alternating directional entrance on scroll:
  // Even index cards slide in from LEFT (-80px, -2.5deg)
  // Odd index cards slide in from RIGHT (+80px, +2.5deg)
  const isLeft = index % 2 === 0;
  const enterX = useTransform(
    entranceProgress,
    [0, 1],
    [isLeft ? "-80px" : "80px", "0px"]
  );
  const enterRotateZ = useTransform(
    entranceProgress,
    [0, 1],
    [isLeft ? -2.4 : 2.4, 0]
  );
  const enterOpacity = useTransform(entranceProgress, [0, 0.4, 1], [0.35, 0.85, 1]);

  // Stacking exit transformations
  const scale = useTransform(exitProgress, [0, 1], [1, 0.93]);
  const exitOpacity = useTransform(exitProgress, [0, 0.8, 1], [1, 0.95, 0.75]);
  const z = useTransform(exitProgress, [0, 1], [0, -40]);
  const filter = useTransform(exitProgress, [0, 1], ["blur(0px)", "blur(1.5px)"]);
  const y = useTransform(exitProgress, [0, 1], ["0px", "-18px"]);

  // Combined opacity
  const combinedOpacity = useTransform(
    [enterOpacity, exitOpacity],
    ([en, ex]) => {
      const e1 = typeof en === "number" ? en : 1;
      const e2 = typeof ex === "number" ? ex : 1;
      return Math.min(e1, e2);
    }
  );

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
          x: enterX,
          rotateZ: enterRotateZ,
          scale,
          opacity: combinedOpacity,
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
          {children}
        </div>
      </motion.div>
    </div>
  );
}
