"use client";

import React, { createContext, useContext, useEffect, useMemo } from "react";
import {
  useMotionValue,
  useSpring,
  useTransform,
  type MotionValue,
} from "motion/react";

export interface CursorPhysicsContextValue {
  smoothMouseX: MotionValue<number>;
  smoothMouseY: MotionValue<number>;
  tiltX: MotionValue<number>;
  tiltY: MotionValue<number>;
  shadowX: MotionValue<number>;
  shadowY: MotionValue<number>;
}

const CursorPhysicsContext = createContext<CursorPhysicsContextValue | null>(null);

const SPRING_CONFIG = { damping: 32, stiffness: 130, mass: 0.5 };

export function CursorPhysicsProvider({ children }: { children: React.ReactNode }) {
  const rawMouseX = useMotionValue(0);
  const rawMouseY = useMotionValue(0);

  const smoothMouseX = useSpring(rawMouseX, SPRING_CONFIG);
  const smoothMouseY = useSpring(rawMouseY, SPRING_CONFIG);

  // Derived 3D tilt angles: [-0.5, 0.5] -> [5, -5] degrees
  const tiltX = useTransform(smoothMouseY, [-0.5, 0.5], [5, -5]);
  const tiltY = useTransform(smoothMouseX, [-0.5, 0.5], [-5, 5]);

  // Dynamic 3D shadow shift: shadow shifts opposite to tilt
  const shadowX = useTransform(smoothMouseX, [-0.5, 0.5], [20, -20]);
  const shadowY = useTransform(smoothMouseY, [-0.5, 0.5], [30, 5]);

  useEffect(() => {
    if (typeof window === "undefined") return;

    // Check for coarse pointer (touch devices)
    const isTouchOnly = window.matchMedia("(pointer: coarse) and (hover: none)").matches;
    if (isTouchOnly) return;

    const handleMouseMove = (e: MouseEvent) => {
      const width = window.innerWidth || 1;
      const height = window.innerHeight || 1;
      const normX = e.clientX / width - 0.5;
      const normY = e.clientY / height - 0.5;
      rawMouseX.set(normX);
      rawMouseY.set(normY);
    };

    const handleMouseLeave = () => {
      rawMouseX.set(0);
      rawMouseY.set(0);
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    window.addEventListener("mouseleave", handleMouseLeave);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseleave", handleMouseLeave);
    };
  }, [rawMouseX, rawMouseY]);

  const value = useMemo(
    () => ({
      smoothMouseX,
      smoothMouseY,
      tiltX,
      tiltY,
      shadowX,
      shadowY,
    }),
    [smoothMouseX, smoothMouseY, tiltX, tiltY, shadowX, shadowY]
  );

  return (
    <CursorPhysicsContext.Provider value={value}>
      {children}
    </CursorPhysicsContext.Provider>
  );
}

export function useCursorPhysics(): CursorPhysicsContextValue {
  const context = useContext(CursorPhysicsContext);
  if (!context) {
    throw new Error("useCursorPhysics must be used within a CursorPhysicsProvider");
  }
  return context;
}
